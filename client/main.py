import os
import socket
import pickle
import sys
from PyQt5.QtWidgets import *
import loginWin
import regWin


class Start(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle("چت روم")

        form = QFormLayout()

        registernBtn = QPushButton("ثبت نام")
        registernBtn.clicked.connect(self.register)
        form.addRow(registernBtn)

        loginBtn = QPushButton("ورود")
        loginBtn.clicked.connect(self.login)
        form.addRow(loginBtn)

        self.setLayout(form)
        self.show()

    def register(self):
        self.reg = regWin.RegisterWindow()
        self.close()

    def login(self):
        self.login = loginWin.LoginWindow()
        self.close()


def main():
    App = QApplication(sys.argv)
    window = Start()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
