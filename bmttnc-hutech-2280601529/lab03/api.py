import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút với API
        self.ui.pushButton.clicked.connect(self.call_api_gen_keys)
        self.ui.pushButton_2.clicked.connect(self.call_api_encrypt)
        self.ui.pushButton_3.clicked.connect(self.call_api_decrypt)
        self.ui.pushButton_4.clicked.connect(self.call_api_sign)
        self.ui.pushButton_5.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/genereate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data['message'])
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.textBrowser.toPlainText(),  # Plain text
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textBrowser_2.setText(data['encrypted_text'])  # Cipher text
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encryption Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "cipher_text": self.ui.textBrowser_2.toPlainText(),  # Cipher text
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textBrowser_3.setText(data['decrypted_message'])  # Information
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decryption Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.textBrowser_3.toPlainText()  # Information
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textBrowser_4.setText(data['signature'])  # Signature
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signature Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.textBrowser_3.toPlainText(),  # Information
            "signature": self.ui.textBrowser_4.toPlainText()  # Signature
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Verified Successfully" if data['is_verified'] else "Verification Failed")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())