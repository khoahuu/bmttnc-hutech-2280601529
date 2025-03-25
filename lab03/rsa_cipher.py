import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.rsa import Ui_MainWindow
import requests
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)
    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/genereate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_public_key.settext(data['public_key'])
                self.ui.txt_private_key.settext(data['private_key'])
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_Plain_text.toPlainText(),
            "key_type":"public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_Cipher_text.settext(data['encrypted_text'])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encryption Successfuly")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "cipher_text": self.ui.txt_Cipher_text.toPlainText(),
            "key_type":"private"
            
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_info.settext(data['decrypted_message'])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decryption Successfuly")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_Plain_text.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_signature.settext(data['signature'])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signature Successfuly")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)
    def call_api_verify(self):
        Url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_Plain_text.toPlainText(),
            "signature": self.ui.txt_signature.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data['is_verified']:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Signature Verified")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Signature Not Verified")
                    msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
                    

                    
            