import psycopg2 as dbapi2
from dsn_conf import get_dsn

dsn = get_dsn()

tempLoggedUser = "pk1"  # temporary userID


class Message:
    def __init__(self, senderID, room, text):
        self.id = None
        self.senderID = senderID
        self.room = room
        self.text = text
        self.date = None
        self.isRead = None

    def save(self):
        if self.id is not None:  # if id is not none it has been in db already
            return
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" INSERT INTO MESSAGE (ID, TEXT, RoomID, SenderID)
                                             VALUES ( DEFAULT, %(text)s, %(RoomID)s, %(SenderID)s ) RETURNING ID""",
                               {'text': self.text, 'RoomID': self.room.id, 'SenderID': self.senderID})

                self.id = cursor.fetchone()[0]

                # okunacak listesine ekle
                for participant in self.room.participants:
                    if participant != tempLoggedUser:  # todo userID
                        cursor.execute(""" INSERT INTO MESSAGE_STATUS (MessageID, ReceiverID)
                                              VALUES ( %(MessageID)s, %(ReceiverID)s )""",
                                       {'MessageID': self.id, 'ReceiverID': participant})

    def load_status(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT COUNT(*) FROM MESSAGE_STATUS
                                    WHERE MessageID=%(MessageID)s""",
                               {'MessageID': self.id})
                res = cursor.fetchone()
                self.isRead = (res[0] == 0)

    def read(self, userID):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" DELETE FROM MESSAGE_STATUS
                                    WHERE MessageID=%(MessageID)s AND
                                          ReceiverID=%(UserID)s """,
                               {'MessageID': self.id, 'UserID': userID})

    @staticmethod
    def get_messages(room, receiverID):
        messages = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT * FROM MESSAGE
                                    WHERE MESSAGE.RoomID=%(RoomID)s AND
                                          MESSAGE.DATE >= (
                                            SELECT JoinDate FROM MESSAGE_PARTICIPANT
                                              WHERE UserID=%(ReceiverID)s AND
                                                    RoomID=%(RoomID)s
                                          )""",
                               {'RoomID': room.id, 'ReceiverID': receiverID})
                result = cursor.fetchall()

                for res in result:
                    msg = Message(res[4], room, res[1])
                    msg.id = res[0]
                    msg.date = res[2]
                    msg.read(tempLoggedUser)  # todo userID
                    msg.load_status()
                    messages.append(msg)

        return messages


class Room:
    def __init__(self, name=None, admin=None, participants=None):
        self.id = None
        self.name = name if name is not None and len(name) > 0 else None
        self.admin = admin
        self.participants = [] if participants is None else participants
        self.messages = []
        self.unread_count = 0

    def save(self):
        if self.id is not None or self.admin is None:  # if id is not none it has been in db already
            return

        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                # first create room entry
                cursor.execute(""" INSERT INTO MESSAGE_ROOM (ID, NAME)
                                      VALUES ( DEFAULT, %(name)s ) RETURNING ID""",
                               {'name': self.name})

                self.id = cursor.fetchone()[0]

                # and create participant entry for each participant and roomID
                for participant in self.participants:
                    cursor.execute(""" INSERT INTO MESSAGE_PARTICIPANT (RoomID, UserID)
                                          VALUES ( %(RoomID)s, %(UserID)s )""",
                                   {'RoomID': self.id, 'UserID': participant})

                # and create admin of this room
                cursor.execute(""" INSERT INTO MESSAGE_ROOM_ADMINS (RoomID, UserID)
                                          VALUES ( %(RoomID)s, %(UserID)s)""",
                               {'RoomID': self.id, 'UserID': self.admin})
        return self.id

    def update(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" UPDATE MESSAGE_ROOM SET NAME=%(name)s
                                      WHERE ID=%(id)s""",
                               {'name': self.name, 'id': self.id})

    def update_participants(self, new_participants):
        if self.admin != tempLoggedUser:
            return

        old_p = set(self.participants)
        new_p = set(new_participants)

        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                for deleted in [p for p in old_p if p not in new_p]:
                    cursor.execute(""" DELETE FROM MESSAGE_PARTICIPANT
                                          WHERE RoomID=%(RoomID)s AND UserID=%(UserID)s""",
                                   {'RoomID': self.id, 'UserID': deleted})
                for added in [p for p in new_p if p not in old_p]:
                    cursor.execute(""" INSERT INTO MESSAGE_PARTICIPANT (RoomID, UserID)
                                          VALUES ( %(RoomID)s, %(UserID)s )""",
                                   {'RoomID': self.id, 'UserID': added})
                self.participants = new_participants

    def leave(self):
        if len(self.participants) < 2:
            return
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                if self.admin == tempLoggedUser:
                    cursor.execute(""" DELETE FROM MESSAGE_ROOM_ADMINS
                                        WHERE RoomID=%(RoomID)s AND UserID=%(UserID)s""",
                                   {'RoomID': self.id, 'UserID': tempLoggedUser})
                    # add new Admin
                    cursor.execute(""" INSERT INTO MESSAGE_ROOM_ADMINS (RoomID, UserID)
                                           VALUES ( %(RoomID)s, %(UserID)s)""",
                                   {'RoomID': self.id, 'UserID': self.participants[0]})

                cursor.execute(""" DELETE FROM MESSAGE_PARTICIPANT
                                        WHERE RoomID=%(RoomID)s AND UserID=%(UserID)s""",
                               {'RoomID': self.id, 'UserID': tempLoggedUser})

    def delete(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" DELETE FROM MESSAGE_ROOM
                                        WHERE ID=%(RoomID)s""", {'RoomID': self.id})

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

    def load_unread_message_count(self, userID):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT COUNT(*)
                                     FROM MESSAGE_STATUS
                                       JOIN MESSAGE
                                         ON MESSAGE_STATUS.MessageID=MESSAGE.ID
                                       JOIN MESSAGE_ROOM
                                         ON MESSAGE.RoomID=MESSAGE_ROOM.ID
                                     WHERE
                                       MESSAGE_STATUS.ReceiverID=%(UserID)s AND
                                       MESSAGE_ROOM.ID=%(RoomID)s """,
                               {'RoomID': self.id, 'UserID': userID})

                result = cursor.fetchone()
                self.unread_count = result[0]

    def load_participants(self):
        participants = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT UserID FROM MESSAGE_PARTICIPANT
                                        WHERE RoomID=%(RoomID)s AND UserID!=%(SelfID)s """,
                               {'RoomID': self.id, 'SelfID': tempLoggedUser})

                result = cursor.fetchall()

                for res in result:
                    participants.append(res[0])

        self.participants = participants

    def load_messages(self):
        self.messages = Message.get_messages(self, tempLoggedUser)  # todo userID

    def load_admin(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT UserID FROM MESSAGE_ROOM_ADMINS
                                                WHERE RoomID=%(RoomID)s """,
                               {'RoomID': self.id})

                result = cursor.fetchone()
                self.admin = result[0]

    @staticmethod
    def get_room_headers(userID):
        """ Load All Room Headers of User participated"""
        rooms = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT RoomID, NAME FROM MESSAGE_ROOM LEFT JOIN MESSAGE_PARTICIPANT
                                        ON MESSAGE_ROOM.ID=MESSAGE_PARTICIPANT.RoomID
                                        WHERE MESSAGE_PARTICIPANT.UserID=%(UserID)s""",
                               {'UserID': userID})
                result = cursor.fetchall()

                for res in result:
                    room = Room(name=res[1])
                    room.id = res[0]

                    room.load_unread_message_count(userID)

                    if room.name is None:
                        room.load_participants()  # oda ismi yoksa participantslar gorunecek. so it is necessary to load participants

                    rooms.append(room)

        return rooms

    @staticmethod
    def get_room_by_id(room_id):
        room = None
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT * FROM MESSAGE_ROOM WHERE MESSAGE_ROOM.ID=%(ID)s""",
                               {'ID': room_id})

                result = cursor.fetchone()
                if result:
                    room = Room(name=result[1])
                    room.id = result[0]
                    room.load_participants()
                    room.load_messages()
                    room.load_admin()
        return room


def get_unread_count():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(""" SELECT COUNT(*)
                                 FROM MESSAGE_STATUS
                                 WHERE
                                   MESSAGE_STATUS.ReceiverID=%(UserID)s """,
                           {'UserID': tempLoggedUser})  # todo userID

            result = cursor.fetchone()
            return result[0]
