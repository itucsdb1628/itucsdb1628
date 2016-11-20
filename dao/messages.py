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

    def save(self):
        if self.id is not None:  # if id is not none it has been in db already
            return
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" INSERT INTO MESSAGE (ID, TEXT, RoomID, SenderID)
                                             VALUES ( DEFAULT, %(text)s, %(RoomID)s, %(SenderID)s ) RETURNING ID""",
                               {'text': self.text, 'RoomID': self.room.id, 'SenderID': self.senderID})

                self.id = cursor.fetchone()[0]

                for participant in self.room.participants:
                    cursor.execute(""" INSERT INTO MESSAGE_STATUS (MessageID, ReceiverID)
                                          VALUES ( %(MessageID)s, %(ReceiverID)s )""",
                                   {'MessageID': self.id, 'ReceiverID': participant})

    @staticmethod
    def get_messages(room):
        messages = []
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" SELECT * FROM MESSAGE WHERE MESSAGE.RoomID=%(RoomID)s""",
                               {'RoomID': room.id})
                result = cursor.fetchall()

                for res in result:
                    msg = Message(res[4], room, res[1])
                    msg.id = res[0]
                    msg.date = res[2]
                    messages.append(msg)

        return messages


class Room:
    def __init__(self, name=None, participants=None):
        self.id = None
        self.name = name if name is not None and len(name) > 0 else None
        self.participants = [] if participants is None else participants
        self.messages = []

    def save(self):
        if self.id is not None:  # if id is not none it has been in db already
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
        return self.id

    def update(self):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(""" UPDATE MESSAGE_ROOM SET NAME=%(name)s
                                      WHERE ID=%(id)s""",
                               {'name': self.name, 'id': self.id})

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
        self.messages = Message.get_messages(self)

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
        return room
