import sqlite3
import datetime
import json
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QPlainTextEdit, QSpinBox

try:
    conn = sqlite3.connect('members.db')
    print('Database connection successful!')
except sqlite3.Error as e:
    print(f'Database connection error: {e}')


class LoggedInWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Logged In')
        self.setGeometry(200, 200, 400, 300)

        self.text_edit = QPlainTextEdit(self)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show()

    def search(self):
        search_term = self.search_txt.text()
        repetitions = self.repeat_spin.value()
        self.text_edit.setPlainText(f'Search term: {search_term}\nRepetitions: {repetitions}')


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 300, 150)

        # Create widgets
        lbl_name = QLabel('Name:', self)
        self.txt_name = QLineEdit(self)
        lbl_password = QLabel('Password:', self)
        self.txt_password = QLineEdit(self)
        self.btn_login = QPushButton('Login', self)

        # Set password mode
        self.txt_password.setEchoMode(QLineEdit.Password)

        # Create layout
        layout = QVBoxLayout(self)
        layout.addWidget(lbl_name)
        layout.addWidget(self.txt_name)
        layout.addWidget(lbl_password)
        layout.addWidget(self.txt_password)
        layout.addWidget(self.btn_login)

        # Connect signal to slot
        self.btn_login.clicked.connect(self.login)

        self.show()

    def login(self):
        # Fetch the allowed date from the web server
        api_url = ' http://192.168.35.223:8000/api/allowed-date'
        response = requests.get(api_url)
        if response.status_code != 200:
            QMessageBox.warning(self, 'Error', 'Failed to fetch the allowed date from the server')
            return
        allowed_date_str = response.json().get('allowed_date')
        allowed_date = datetime.datetime.strptime(allowed_date_str, '%Y-%m-%d').date()

        current_date = datetime.date.today()

        if current_date > allowed_date:
            QMessageBox.warning(self, 'Login', 'Error9142')
            return

        name = self.txt_name.text()
        password = self.txt_password.text()

        # Check if the login credentials match the membership information in the database
        conn = sqlite3.connect('members.db')
        c = conn.cursor()
        c.execute('SELECT * FROM members WHERE name = ? AND password = ?', (name, password))
        member = c.fetchone()
        conn.close()

        if member is not None:
            QMessageBox.information(self, 'Login', 'Logged in successfully!')
            self.hide()

            # Run the AutoHotkey script
            script_path = r'C:\Users\pc\Desktop\코딩\test.ahk' # Replace with your actual script path

            # Run the script using AutoHotkey
            os.system(f'autohotkey.exe "{script_path}"')
        else:
            QMessageBox.warning(self, 'Login', 'Invalid name or password')


if __name__ == '__main__':
    app = QApplication([])
    login = Login()
    app.exec_()