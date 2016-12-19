import psycopg2 as dbapi2
from datetime import datetime
from dsn_conf import get_dsn
from enum import Enum
from flask_login import current_user
from userdata import select_a_user_from_login as get_user_by_id
from userdata import select_users_from_login as get_fr_list

dsn = get_dsn()


class Events(Enum):
    JOIN = 0
    LEFT = 1
    ADMIN = 2


class Event:
    def __init__(self, room_id, user, action):
        self.id = None
        self.room_id = room_id
        self.user = user
        self.action = action
        self.date = None
        self.text = self.user.username
        self.text += " joined conversation" if action == Events.JOIN\
            else " left conversation" if action == Events.LEFT\
            else " is Admin"

    def create(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ INSERT
                          INTO message_room_event ( room_id, user_id, action_id )
                          VALUES ( %(room_id)s, %(user_id)s, %(action_id)s ) """, {
                        'room_id': self.room_id,
                        'user_id': self.user.id,
                        'action_id': self.action.value
                    })


class Message:
    def __init__(self, sender, room_id, text):
        self.id = None
        self.sender = sender
        self.room_id = room_id
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
                        'room_id': self.room_id,
                        'sender_id': self.sender.id,
                        'text': self.text
                    })

                self.id = cursor.fetchone()[0]

                # okunacak listesine ekle
                cursor.execute(
                    """ INSERT
                          INTO message_status ( message_id, receiver_id )
                          ( SELECT %(message_id)s AS message_id, user_id AS receiver_id
                              FROM message_participant
                                WHERE room_id = %(room_id)s
                                  AND user_id != %(user_id)s )""", {
                        'message_id': self.id,
                        'room_id': self.room_id,
                        'user_id': self.sender.id
                    })


class Room:
    def __init__(self, name=None, admin=None, participants=None):
        self.id = None
        self.name = name if name is not None and len(name.strip()) > 0 else None
        self.admin = admin
        self.participants = [] if participants is None else participants
        self.items = []
        self.unread_count = 0
        self.last_message = ""

    def create(self):
        if self.id is not None or self.admin is None:  # if id is not none it has been in db already
            return

        if len(self.participants) == 2:
            rid = Room.get_room_id_with(self.participants[0].id if self.participants[1].id == current_user.id
                                        else self.participants[1].id)
            if rid is not None:
                return rid

        # create room in db
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ INSERT
                          INTO message_room ( id, room_name, admin_id )
                          VALUES ( DEFAULT, %(room_name)s, %(admin_id)s )
                          RETURNING id """, {
                        'room_name': self.name,
                        'admin_id': self.admin.id
                    })

                self.id = cursor.fetchone()[0]

        self.update_participants()
        Event(self.id, self.admin, Events.ADMIN).create()

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
        self.name = name.strip() if name is not None and len(name.strip()) > 0 else None
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
        return self.name if self.name is not None else " ".join([p.username for p in self.participants if p.id != current_user.id])[:15]

    def add_participant(self, participant):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ INSERT
                          INTO message_participant ( room_id, user_id )
                          VALUES ( %(room_id)s, %(user_id)s )""", {
                        'room_id': self.id,
                        'user_id': participant.id
                    })

                self.participants.append(participant)
                Event(self.id, participant, Events.JOIN).create()

    def remove_participant(self, participant):
        self.read_all(participant)
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ DELETE
                          FROM message_participant
                          WHERE room_id = %(room_id)s
                            AND user_id = %(user_id)s """, {
                        'room_id': self.id,
                        'user_id': participant.id
                    })

                self.participants.remove(participant)
                Event(self.id, participant, Events.LEFT).create()

                # check admin
                if self.admin.id == participant.id:
                    self.update_admin(self.participants[0])

    def update_participants(self, participants=None):
        if participants is None:  # ilk kayit.
            participants = self.participants
            self.participants = []

        old_ids = set([p.id for p in self.participants])
        new_ids = set([p.id for p in participants])

        for deleted in self.participants:  # eski listede olup yeni listede olmayan
            if deleted.id not in new_ids:
                self.remove_participant(deleted)

        for added in participants:  # eski listede olmayip yeni listede olan
            if added.id not in old_ids:
                self.add_participant(added)

    def read_all(self, user):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ DELETE
                          FROM message_status
                          WHERE receiver_id = %(user_id)s
                            AND message_id = ANY( SELECT id
                                                    FROM message
                                                    WHERE room_id = %(room_id)s ) """, {
                        'user_id': user.id,
                        'room_id': self.id
                    })

    def update_admin(self, user):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ UPDATE message_room
                          SET admin_id = %(admin_id)s
                          WHERE id = %(room_id)s """, {
                        'room_id': self.id,
                        'admin_id': user.id
                    })
                self.admin = user
                Event(self.id, user, Events.ADMIN).create()

    def send_message(self, content):
        if content is not None and len(content.strip()) > 0:
            Message(current_user, self.id, content.strip()).create()
            self.activate()

    def activate(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ UPDATE message_room
                          SET activity_date = %(activity_date)s
                          WHERE id = %(id)s """, {
                        'id': self.id,
                        'activity_date': datetime.now()
                    })

    @staticmethod
    def get_room_id_with(user_id):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT room_id
                          FROM ( SELECT room_id, ARRAY_AGG(user_id) AS users
                                   FROM message_participant
                                     GROUP BY room_id
                                     HAVING COUNT(room_id) = 2 ) AS U
                          WHERE %(uid1)s = ANY(users)
                            AND %(uid2)s = ANY(users) """, {
                        'uid1': current_user.id,
                        'uid2': user_id
                    })
                res = cursor.fetchone()
                return res[0] if res is not None else None

    @staticmethod
    def get_headers(text=None):
        """ Load All Room Headers of User participated"""
        rooms = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT id, room_name, activity_date, msg.unread_cnt, participant.participants, messages.note
                          FROM message_room
                            RIGHT JOIN ( SELECT room_id
                                           FROM message_participant
                                           WHERE user_id = %(user_id)s ) AS rooms
                              ON message_room.id = rooms.room_id
                            LEFT JOIN ( SELECT COUNT(*) AS unread_cnt, message.room_id AS mid
                                          FROM message_status
                                            JOIN message
                                              ON message_status.message_id = message.id
                                              AND message_status.receiver_id = %(user_id)s
                                          GROUP BY message.room_id ) AS msg
                              ON msg.mid = message_room.id
                            LEFT JOIN ( SELECT ARRAY_AGG(user_id) AS participants, room_id
                                          FROM message_participant
                                          GROUP BY room_id ) AS participant
                              ON participant.room_id = message_room.id
                            LEFT JOIN ( SELECT note, room_id
                                          FROM message
                                          ORDER BY message_date DESC LIMIT 1 ) AS messages
                              ON messages.room_id = message_room.id""", {
                        'user_id': current_user.id
                    })

                result = cursor.fetchall()

                for res in result:
                    room = Room(name=res[1])
                    room.id = res[0]
                    room.last_message_date = res[2]
                    room.unread_count = res[3]
                    room.participants = [get_user_by_id(pid) for pid in res[4]]
                    room.last_message = res[5][:60]
                    if text is not None:
                        for p in room.participants:
                            if p.username.startswith(text):
                                rooms.append(room)
                                continue
                    else:
                        rooms.append(room)

        return rooms

    @staticmethod
    def get_details(room_id):
        room = None
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ SELECT id, room_name, admin_id, participant.participants, msg.content, evt.content
                          FROM message_room
                            LEFT JOIN ( SELECT ARRAY_AGG(user_id) AS participants, room_id
                                          FROM message_participant
                                          GROUP BY room_id ) AS participant
                              ON participant.room_id = message_room.id
                            LEFT JOIN ( SELECT (join_date - interval '00:00:00.500') AS join_date, room_id
                                          FROM message_participant
                                          WHERE user_id = %(user_id)s ) AS j_date
                              ON j_date.room_id = message_room.id
                            LEFT JOIN LATERAL ( SELECT JSON_AGG((id, note, message_date, sender_id, status.wait_cnt)) AS content, room_id
                                                  FROM message
                                                    LEFT JOIN ( SELECT COUNT(*) AS wait_cnt, message_id
                                                                  FROM message_status
                                                                  GROUP BY message_id ) AS status
                                                      ON status.message_id = message.id
                                                  WHERE message_date >= j_date.join_date
                                                  GROUP BY room_id ) AS msg
                              ON msg.room_id = message_room.id
                            LEFT JOIN LATERAL ( SELECT JSON_AGG((user_id, action_id, event_date)) AS content, room_id
                                                  FROM message_room_event
                                                  WHERE event_date >= j_date.join_date
                                                  GROUP BY room_id ) AS evt
                              ON evt.room_id = message_room.id
                          WHERE message_room.id = %(room_id)s """, {
                        'room_id': room_id,
                        'user_id': current_user.id
                    })

                result = cursor.fetchone()
                if result:
                    room = Room(name=result[1])
                    room.id = result[0]
                    room.admin = get_user_by_id(result[2])
                    room.participants = [get_user_by_id(pid) for pid in result[3]]
                    if result[4] is not None:
                        for m in result[4]:
                            msg = Message(get_user_by_id(m['f4']), room, m['f2'])
                            msg.id = m['f1']
                            msg.date = datetime.strptime(m['f3'], "%Y-%m-%d %H:%M:%S.%f")
                            msg.isRead = (m['f5'] is None)  # == 0 ?
                            room.items.append(msg)
                    if result[5] is not None:
                        for e in result[5]:
                            event = Event(room.id, get_user_by_id(e['f1']), Events(e['f2']))
                            event.date = datetime.strptime(e['f3'], "%Y-%m-%d %H:%M:%S.%f")
                            room.items.append(event)
        room.read_all(current_user)
        return room


def get_unread_count():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """ SELECT COUNT(*)
                      FROM message_status
                      WHERE message_status.receiver_id = %(user_id)s """, {
                    'user_id': current_user.id
                })
            return cursor.fetchone()[0]
