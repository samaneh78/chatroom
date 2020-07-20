from main import *
from PyQt5.QtWidgets import *
from skt import *
from chatRoom import *


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle("چت روم: ورود")

        gridLayout = QGridLayout()

        self.usernameLE = QLineEdit()
        self.usernameLE.setPlaceholderText("برای مثال: user")
        gridLayout.addWidget(self.usernameLE, 0, 0)
        label = QLabel("نام کاربری:")
        gridLayout.addWidget(label, 0, 1)

        self.passwordLE = QLineEdit()
        self.passwordLE.setEchoMode(QLineEdit.Password)
        self.passwordLE.setPlaceholderText("برای مثال: 123456")
        gridLayout.addWidget(self.passwordLE, 1, 0)
        label = QLabel("رمز عبور:")
        gridLayout.addWidget(label, 1, 1)

        loginBtn = QPushButton("ورود")
        loginBtn.clicked.connect(self.login)
        gridLayout.addWidget(loginBtn, 2, 0)

        backBtn = QPushButton("برگشت")
        backBtn.clicked.connect(self.back)
        gridLayout.addWidget(backBtn, 3, 0)

        

        self.setLayout(gridLayout)
        self.show()

    def login(self):
        username = self.usernameLE.text()
        password = self.passwordLE.text()
        if(len(username) > 2):
            if(len(password) > 2):
                sendDate = {
                    "job": "login",
                    "username": username,
                    "password": password
                }

                res = sendSocket(sendDate)
                try:
                    if(res["error"] == "" and res["userId"]):
                        userId = res["userId"]
                        self.chatRoom = ChatWindow(userId, username)
                        self.close()
                    else:
                        self.errorLabel.setText(res["error"])
                except:
                    pass

    def back(self):
        self.start = Start()
        self.close()
