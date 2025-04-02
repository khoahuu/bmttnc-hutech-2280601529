import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import requests
class RSACipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_key(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        self.save_key()

    def save_key(self):
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open("private_key.pem", "wb") as priv_file:
            priv_file.write(private_pem)

        with open("public_key.pem", "wb") as pub_file:
            pub_file.write(public_pem)

    def load_key(self):
        with open("private_key.pem", "rb") as priv_file:
            private_pem = priv_file.read()
            private_key = serialization.load_pem_private_key(private_pem, password=None)

        with open("public_key.pem", "rb") as pub_file:
            public_pem = pub_file.read()
            public_key = serialization.load_pem_public_key(public_pem)

        return private_key, public_key
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
        url="http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response=requests.get(url)
            if response.status_code==200:
                data=response.json()
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data['message'])
                msg.exec_()
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
            "message": self.ui.txt_cipher_text.toPlainText(),
            "key_type":"private"
             }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.settext(data['decrypted_message'])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decryption Successfuly")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)
    def call_api_sign(self):
        url="http://127.0.0.1:5000/api/rsa/sign"
        payload={
            "message":self.ui.txt_info.toPlainText()
        }
        try:
            response=requests.post(url,json=payload)
            if response.status_code==200:
                data=response.json()
                self.ui.txt_sign.settext(data['signature'])
                msg=QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signature Successfuly")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)
    def call_api_verify(self):
        url="http://127.0.0.1:5000/api/rsa/verify"
        payload={
            "message":self.ui.txt_info.toPlainText(),
            "signature":self.ui.txt_sign.toPlainText()
        }
        try:
            response=requests.post(url,json=payload)
            if response.status_code==200:
                data=response.json()
                if (data['verified']):
                    msg=QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verified Successfully")
                    msg.exec_()
                else:
                    msg=QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Verification Failed")
                    msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)
if __name__ == "__main__":
    app=QApplication(sys.argv)
    window=MyApp()
    window.show()
    sys.exit(app.exec_())
        