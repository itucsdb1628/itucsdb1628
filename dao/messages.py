from enum import Enum

import datetime
import psycopg2 as dbapi2
from dsn_conf import get_dsn

dsn = get_dsn()

tempLoggedUser = "pk1"  # temporary userID


def get_user_id():
    """ pseudo layer for user id that logged in. """
    return tempLoggedUser  # todo get actual logged in userID


class Events(Enum):
    JOIN = 0
    LEFT = 1
    ADMIN = 2


class Event:
    def __init__(self, room_id, user_id, action):
        self.id = None
        self.room_id = room_id
        self.user_id = user_id
        self.action = action
        self.date = None
        if action == Events.JOIN:
            self.text = user_id + " joined conversation"
        elif action == Events.LEFT:
            self.text = user_id + " left conversation"
        else:
            self.text = user_id + " is Admin"

    def create(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ INSERT
                          INTO message_room_event ( room_id, user_id, action_id )
                          VALUES ( %(room_id)s, %(user_id)s, %(action_id)s ) """, {
                        'room_id': self.room_id,
                        'user_id': self.user_id,
                        'action_id': self.action.value
                    })

    @staticmethod
    def get(room_id):
        events = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT user_id, action_id, event_date
                          FROM message_room_event
                          WHERE room_id = %(room_id)s
                            AND event_date >= ( SELECT join_date
                                                  FROM message_participant
                                                  WHERE user_id = %(user_id)s
                                                    AND room_id = %(room_id)s
                                              ) """, {
                        'room_id': room_id,
                        'user_id': get_user_id()
                    })

                result = cursor.fetchall()

                for res in result:
                    event = Event(room_id, res[0], Events(res[1]))
                    event.date = res[2]
                    events.append(event)

        return events


class Message:
    def __init__(self, senderID, room, text):
        self.id = None
        self.senderID = senderID
        self.room = room
        self.text = text
        self.date = None
        self.isRead = None

    def create(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ INSERT
                          INTO message ( id, note, room_id, sender_id )
                          VALUES ( DEFAULT, %(text)s, %(room_id)s, %(sender_id)s )
                          RETURNING ID """, {
                        'room_id': self.room.id,
                        'sender_id': self.senderID,
                        'text': self.text
                    })

                self.id = cursor.fetchone()[0]

                # okunacak listesine ekle
                for participant in self.room.participants:
                    if participant != get_user_id():
                        cursor.execute(
                            """ INSERT
                                  INTO message_status ( message_id, receiver_id )
                                  VALUES ( %(message_id)s, %(receiver_id)s )""", {
                                'message_id': self.id,
                                'receiver_id': participant
                            })

    def read(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ DELETE
                          FROM message_status
                          WHERE message_id = %(message_id)s
                            AND receiver_id = %(receiver_id)s """, {
                        'message_id': self.id,
                        'receiver_id': get_user_id()
                    })

    def load_status(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT COUNT(*)
                          FROM message_status
                            WHERE message_id = %(message_id)s """, {
                        'message_id': self.id
                    })
                self.isRead = (cursor.fetchone()[0] == 0)

    @staticmethod
    def get(room):
        receiver_id = get_user_id()
        messages = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT id, note, message_date, sender_id
                          FROM message
                            WHERE room_id = %(room_id)s
                              AND message_date >= ( SELECT join_date
                                                      FROM message_participant
                                                      WHERE user_id = %(receiver_id)s
                                                        AND room_id = %(room_id)s
                                                  ) """, {
                        'room_id': room.id,
                        'receiver_id': receiver_id
                    })

                result = cursor.fetchall()

                for res in result:
                    msg = Message(res[3], room, res[1])
                    msg.id = res[0]
                    msg.date = res[2]
                    msg.read()
                    msg.load_status()
                    messages.append(msg)

        return messages


class Room:
    def __init__(self, name=None, admin=None, participants=None):
        self.id = None
        self.name = name if name is not None and len(name.strip()) > 0 else None
        self.admin = admin
        self.participants = [] if participants is None else participants
        self.items = []
        self.unread_count = 0

    def create(self):
        if self.id is not None or self.admin is None:  # if id is not none it has been in db already
            return

        # create room in db
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ INSERT
                          INTO message_room ( id, room_name )
                          VALUES ( DEFAULT, %(room_name)s )
                          RETURNING id """, {
                        'room_name': self.name
                    })

                self.id = cursor.fetchone()[0]

        self.update_participants()
        self.update_admin()

        return self.id

    def delete(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ DELETE
                          FROM message_room
                          WHERE id = %(id)s""", {
                        'id': self.id
                    })

    def update_name(self, name):
        name = name.strip()
        self.name = name if name is not None and len(name) > 0 else None

        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ UPDATE message_room
                          SET room_name = %(room_name)s
                          WHERE id = %(id)s """, {
                        'id': self.id,
                        'room_name': self.name
                    })

    def get_display_name(self):
        """ Room name or First n char of participants name """
        if self.name is not None:
            return self.name

        l = 0
        nick = ""
        for fr in self.participants:
            nick = nick + fr[:15 - l] + " "
            l = len(nick)
            if l > 15:
                break

        return nick

    def add_participant(self, participant):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ INSERT
                          INTO message_participant ( room_id, user_id )
                          VALUES ( %(room_id)s, %(user_id)s )""", {
                        'room_id': self.id,
                        'user_id': participant
                    })

                self.participants.append(participant)
                self.create_event(participant, Events.JOIN)

    def remove_participant(self, participant):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ DELETE
                          FROM message_participant
                          WHERE room_id = %(room_id)s
                            AND user_id = %(user_id)s """, {
                        'room_id': self.id,
                        'user_id': participant
                    })

                self.participants.remove(participant)
                self.create_event(participant, Events.LEFT)
                print(self.admin, participant)
                # check admin
                if self.admin == participant:
                    self.update_admin(self.participants[0])

    def update_participants(self, participants=None):
        if participants is None:  # ilk kayit.
            participants = self.participants
            self.participants = []

        old_p = set(self.participants)
        new_p = set(participants)

        for deleted in [p for p in old_p if p not in new_p]:  # eski listede olup yeni listede olmayan
            self.remove_participant(deleted)

        for added in [p for p in new_p if p not in old_p]:  # eski listede olmayip yeni listede olan
            self.add_participant(added)

    def update_admin(self, user_id=None):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                if user_id is not None:  # ilk kayit degilse.
                    cursor.execute(
                        """ DELETE
                              FROM message_room_admins
                              WHERE room_id = %(room_id)s
                                AND user_id = %(user_id)s""", {
                            'room_id': self.id,
                            'user_id': self.admin
                        })
                else:
                    user_id = self.admin

                cursor.execute(
                    """ INSERT
                          INTO message_room_admins ( room_id, user_id )
                          VALUES ( %(room_id)s, %(user_id)s ) """, {
                        'room_id': self.id,
                        'user_id': user_id
                    })
                self.admin = user_id
                self.create_event(user_id, Events.ADMIN)

    def create_event(self, user_id, event):
        event = Event(self.id, user_id, event)
        event.create()

    def send_message(self, content):
        msg = Message(get_user_id(), self, content)
        msg.create()
        self.activate()

    def activate(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ UPDATE message_room
                          SET activity_date = %(activity_date)s
                          WHERE id = %(id)s """, {
                        'id': self.id,
                        'activity_date': datetime.datetime.now()
                    })

    def load_participants(self):
        participants = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT user_id
                          FROM message_participant
                            WHERE room_id = %(room_id)s """, {
                        'room_id': self.id
                    })

                result = cursor.fetchall()

                for res in result:
                    participants.append(res[0])

        self.participants = participants

    def load_admin(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT user_id
                          FROM message_room_admins
                          WHERE room_id = %(room_id)s """, {
                        'room_id': self.id
                    })

                self.admin = cursor.fetchone()[0]

    def load_items(self):
        self.items = Message.get(self) + Event.get(self.id)

    @staticmethod
    def get_headers():
        """ Load All Room Headers of User participated"""
        rooms = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT id, room_name, activity_date, msg.unread_cnt
                          FROM message_room
                            JOIN message_participant
                              ON message_room.id = message_participant.room_id
                            LEFT JOIN ( SELECT COUNT(*) AS unread_cnt, message.room_id AS mid
                                          FROM message_status
                                            JOIN message
                                              ON message_status.message_id = message.id
                                              AND message_status.receiver_id = %(user_id)s
                                          GROUP BY (message.room_id)
                                      ) AS msg
                              ON msg.mid = message_room.id
                          WHERE message_participant.user_id = %(user_id)s """, {
                        'user_id': get_user_id()
                    })

                result = cursor.fetchall()

                for res in result:
                    room = Room(name=res[1])
                    room.id = res[0]
                    room.last_message_date = res[2]
                    room.unread_count = res[3]

                    if room.name is None:
                        room.load_participants()  # oda ismi yoksa participantslar gorunecek. so it is necessary to load participants

                    rooms.append(room)

        return rooms

    @staticmethod
    def get_details(room_id):
        room = None
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT *
                          FROM message_room
                          WHERE message_room.id = %(id)s""", {
                        'id': room_id
                    })

                result = cursor.fetchone()
                if result:
                    room = Room(name=result[1])
                    room.id = result[0]
                    room.load_participants()
                    room.load_items()
                    room.load_admin()
        return room


def get_unread_count():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT COUNT(*)
                      FROM message_status
                      WHERE message_status.receiver_id = %(user_id)s """, {
                    'user_id': get_user_id()
                })

            return cursor.fetchone()[0]
