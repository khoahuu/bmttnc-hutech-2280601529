import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
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
            "message": self.ui.txt_info.toPlainText(),
            
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_info.settext(data['decrypted_text'])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decryption Successfuly")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error:%s"% e.message)