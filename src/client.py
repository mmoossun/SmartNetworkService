import sys
from PyQt5.QtWidgets import *
from socket import *
import threading

EOF = "\r\n"

class Client(threading.Thread):

    def __init__(self, update_text_callback):

        threading.Thread.__init__(self)
        self.update_text_callback = update_text_callback
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 8080))

    def run(self):

        while True:
            recvData = ''
            while True:
                recvTemp = self.sock.recv(1024).decode('utf-8')
                if EOF in recvTemp:
                    recvData += recvTemp[:recvTemp.find(EOF)]
                    break
                recvData += recvTemp
            if not recvData:
                break
            self.update_text_callback(f'상대방 : {recvData}')

    def send_message(self, message):

        self.update_text_callback(f'나 : {message}')
        self.sock.send((message + EOF).encode('utf-8'))

class ClientWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('Client')
        self.setGeometry(700, 200, 500, 500)

        layout = QVBoxLayout()

        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        layout.addWidget(self.logTextEdit)

        self.messageLineEdit = QLineEdit()
        layout.addWidget(self.messageLineEdit)

        self.sendButton = QPushButton('메시지 보내기', self)
        self.sendButton.clicked.connect(self.send_message)
        layout.addWidget(self.sendButton)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.client_thread = Client(self.update_text)
        self.client_thread.start()

    def update_text(self, message):

        self.logTextEdit.append(message)

    def send_message(self):

        message = self.messageLineEdit.text()
        self.client_thread.send_message(message)
        self.messageLineEdit.clear()

if __name__ == '__main__':
    cli = QApplication(sys.argv)
    cliWin = ClientWindow()
    cliWin.show()
    sys.exit(cli.exec_())
