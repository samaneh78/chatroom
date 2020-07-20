import socket
import time
import pickle
import mysql.connector


f = open("C:/Users/pars/Desktop/chat room/ChatRoom/port.txt", "r")
port = int(f.read())

sqlPass = "hono1371lulu78"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", port))
s.listen(100)

clients_socket = []


def main():
    while True:
        serverSocket, address = s.accept()

        msg = serverSocket.recv(1024)
        data = pickle.loads(msg)
        sendData = {
            "error": "ناموفق"
        }
        if(data["job"] == "register"):
            username = data["username"]
            userId = register(username, data["password"])
            if(userId):
                sendData = {
                    "username": username,
                    "userId": userId,
                    "error": ""
                }

            else:
                sendData = {
                    "username": username,
                    "password": data["password"],
                    "error": "ثبت نام با مشکل مواجه شد"
                }
        elif(data["job"] == "login"):
            username = data["username"]
            password = data["password"]
            userId = login(username, password)
            if(userId):
                # chats_list_names = getChats(userId)
                sendData = {
                    "userId": userId,
                    "error": ""
                }
            else:
                sendData = {
                    "userId": 0,
                    "error": "نام کاربری یا رمزعبور اشتباه است"
                }

        elif(data["job"] == "msg"):
            messages = getMsgs(data["userId"], data["text"], data["lastMsgId"])

            sendData = {
                "messages": messages,
                "error": ""
            }

        serverSocket.send(pickle.dumps(sendData))
    s.close()


def getMsgs(userId, msgText, lastMsgId):
    messages = []
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=sqlPass,
            database="chat_room"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT text, userId, sentTime, msgId FROM messages where msgId>{lastMsgId}"
        mycursor.execute(sql)
        for x in mycursor:
            msg = {
                "text": x[0],
                "userId": x[1],
                "sentTime": x[2],
                "msgId": x[3],
                "username": "",
            }
            messages.append(msg)
        mydb.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0

    for msg in messages:
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password=sqlPass,
                database="chat_room"
            )
            mycursor = mydb.cursor()
            sql = f"SELECT username FROM users where userId={msg['userId']}"
            mycursor.execute(sql)
            for x in mycursor:
                msg["username"] = x[0]
                break
            mydb.close()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 0
    if(userId and msgText):
        msgId = 0
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password=sqlPass,
                database="chat_room"
            )
            mycursor = mydb.cursor()
            sql = f"INSERT INTO messages (userId,text) VALUES ({userId}, '{msgText}')"
            mycursor.execute(sql)
            mydb.commit()
            msgId = mycursor.lastrowid

            print("New message with id: ", msgId)
            mydb.close()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return 0

        if msgId:
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=sqlPass,
                    database="chat_room"
                )
                mycursor = mydb.cursor()
                sql = f"SELECT text, userId, sentTime FROM messages where msgId={msgId}"
                mycursor.execute(sql)
                for x in mycursor:
                    msg = {
                        "text": x[0],
                        "userId": x[1],
                        "sentTime": x[2],
                        "msgId": msgId,
                        "username": userId
                    }
                    messages.append(msg)
                mydb.close()
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                return 0
    return messages


def login(username, password):
    userId = 0
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=sqlPass,
            database="chat_room"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT userId,username,password FROM users where username='{username}'"
        mycursor.execute(sql)
        for x in mycursor:
            if x[2] == password:
                userId = x[0]
                break
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
    return userId


def register(username, password):
    userId = 0
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=sqlPass,
            database="chat_room"
        )
        mycursor = mydb.cursor()
        sql = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        mycursor.execute(sql)
        mydb.commit()
        userId = mycursor.lastrowid
        print("New user registered with id: ", userId)
        mydb.close()
        return userId
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return 0
    return userId


main()
