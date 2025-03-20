import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
       super().__init__()
       self.ui = Ui_MainWindow()
       self.ui.setupUi(self)

       # Kết nối đúng với nút trong giao diện
       self.ui.pushButton.clicked.connect(self.call_api_encrypt)
       self.ui.pushButton_2.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.textEdit.toPlainText(),  # Sửa txt_plain_text thành textEdit
            "key": self.ui.lineEdit.text()  # Sửa txt.key thành lineEdit
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit_2.setText(data["encrypted_message"])  # Sửa txt_cipher_text thành textEdit_2
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encryption successful")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % str(e))  # Sửa e.message thành str(e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.textEdit_2.toPlainText(),  # Sửa txt_cipher_text thành textEdit_2
            "key": self.ui.lineEdit.text()  # Sửa txt_key thành lineEdit
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textEdit.setText(data["decrypted_message"])  # Sửa txt_plain_text thành textEdit
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decryption successful")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % str(e))  # Sửa e.message thành str(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
