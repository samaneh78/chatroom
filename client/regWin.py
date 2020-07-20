from main import *
from PyQt5.QtWidgets import *
from skt import *
from chatRoom import *


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle("چت روم: ثبت نام")

        gridLayout = QGridLayout()

        self.usernameLE = QLineEdit()
        self.usernameLE.setPlaceholderText("برای مثال: user")
        gridLayout.addWidget(self.usernameLE, 0, 0)
        label = QLabel("نام کاربری:")
        gridLayout.addWidget(label, 0, 1)

        self.passwordLE = QLineEdit()
        self.passwordLE.setPlaceholderText("برای مثال: 123456")
        gridLayout.addWidget(self.passwordLE, 1, 0)
        label = QLabel("رمز عبور:")
        gridLayout.addWidget(label, 1, 1)

        self.errorLabel = QLabel("")
        gridLayout.addWidget(self.errorLabel, 2, 0)

        loginBtn = QPushButton("ثبت نام")
        loginBtn.clicked.connect(self.register)
        gridLayout.addWidget(loginBtn, 3, 0)

        self.setLayout(gridLayout)
        self.show()

    def register(self):
        username = self.usernameLE.text()
        password = self.passwordLE.text()
        if(len(username) > 2):
            if(len(password) > 2):
                sendDate = {
                    "job": "register",
                    "username": username,
                    "password": password
                }

                res = sendSocket(sendDate)

                if(res["error"] == ""):
                    userId = res["userId"]
                    self.chatRoom = ChatWindow(userId, username)
                    self.close()
                else:
                    self.errorLabel.setText(res["error"])
