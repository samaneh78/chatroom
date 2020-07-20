from main import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from skt import *


class ChatWindow(QWidget):
    def __init__(self, userId, username):
        self.userId = userId
        self.username = username
        self.lastMsgId = 0
        super().__init__()
        self.setGeometry(100, 100, 400, 600)
        self.setWindowTitle("چت روم")

        gridLayout = QGridLayout()

        label = QLabel("متن پیام: ")
        gridLayout.addWidget(label, 0, 1)

        self.msgLE = QLineEdit()
        gridLayout.addWidget(self.msgLE, 0, 0)

        sendBtn = QPushButton("ارسال")
        sendBtn.clicked.connect(self.send)
        gridLayout.addWidget(sendBtn, 1, 0)

        sendBtn = QPushButton("تازه سازی")
        sendBtn.clicked.connect(self.getMsg)
        gridLayout.addWidget(sendBtn, 2, 0)

        self.msgLW = QListWidget()
        gridLayout.addWidget(self.msgLW, 3, 0)

        self.getMsg()

        self.setLayout(gridLayout)
        self.show()

    def send(self):
        msgText = self.msgLE.text()
        if(len(msgText) > 0):
            sendData = {
                "job": "msg",
                "userId": self.userId,
                "text": msgText,
                "lastMsgId": self.lastMsgId
            }

            res = sendSocket(sendData)

            if(res["error"] == ""):
                self.msgLE.setText("")
                messages = res["messages"]

                if messages:
                    self.lastMsgId = messages[-1]["msgId"]
                    for msg in messages:
                        username = msg["username"]
                        userId = msg["userId"]
                        msgText = msg["text"]

                        color = QColor("#fff")
                        if(userId == self.userId):
                            color = QColor("#ddd")
                            username = self.username

                        item = QListWidgetItem()
                        item.setText(f"{username}: {msgText}")
                        item.setBackground(color)
                        self.msgLW.insertItem(0, item)

    def getMsg(self):
        sendData = {
            "job": "msg",
            "userId": 0,
            "text": "",
            "lastMsgId": self.lastMsgId
        }

        res = sendSocket(sendData)

        if(res["error"] == ""):
            messages = res["messages"]
            if messages:
                self.lastMsgId = messages[-1]["msgId"]
                for msg in messages:
                    username = msg["username"]
                    userId = msg["userId"]
                    msgText = msg["text"]

                    color = QColor("#fff")
                    if(userId == self.userId):
                        color = QColor("#ddd")
                        username = self.username

                    item = QListWidgetItem()
                    item.setText(f"{username}: {msgText}")
                    item.setBackground(color)
                    self.msgLW.insertItem(0, item)
