import sys
from PyQt5.QtWidgets import *
from socket import *
import os
import threading
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI

KEY = "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"
# API key가 잘 연결되었는지 확인
os.environ["OPENAI_API_KEY"] = KEY

EOF = "\r\n"

# GPT 함수
def gpt(prompt):
    llm = ChatOpenAI(temperature=0.7,  # 창의성 (0.0 ~ 2.0)
                     max_tokens=2048,  # 최대 토큰수
                     model_name='gpt-3.5-turbo',  # 모델명
                     )
    # 질의내용

    answer = llm.predict(prompt)
    # 질의
    return answer

class Server(threading.Thread):

    def __init__(self, text_edit):

        threading.Thread.__init__(self)
        self.text_edit = text_edit

    def run(self):

        port = 8080
        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.bind(('', port))
        serverSock.listen(1)
        self.update_text(f'{port}번 포트로 접속 대기중...')

        while True:

            connectionSock, addr = serverSock.accept()
            self.update_text(f'{str(addr)} 에서 접속되었습니다.')
            client_thread = threading.Thread(target=self.recvAndSend, args=(connectionSock,))
            client_thread.start()

    def recvAndSend(self, connectionSock):

        while True:

            try:
                recvData = ''
                while True:
                    recvTemp = connectionSock.recv(1024).decode('utf-8')
                    if EOF in recvTemp:
                        recvData += recvTemp[:recvTemp.find(EOF)]
                        break
                    recvData += recvTemp
                if not recvData:
                    break
                self.update_text(f'상대방: {recvData}')
                response = gpt(recvData) + EOF
                connectionSock.send(response.encode('utf-8'))

            except Exception as e:

                self.update_text(f'오류 발생: {str(e)}')
                connectionSock.send("잠시 후 이용해주세요.\r\n".encode('utf-8'))

    def update_text(self, message):

        self.text_edit.append(message)

class ServerWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('Server')
        self.setGeometry(200, 200, 500, 500)

        layout = QVBoxLayout()

        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        layout.addWidget(self.logTextEdit)

        self.startButton = QPushButton('서버 시작', self)
        self.startButton.clicked.connect(self.start_server)
        layout.addWidget(self.startButton)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def start_server(self):

        self.server_thread = Server(self.logTextEdit)
        self.server_thread.start()

if __name__ == '__main__':
    server = QApplication(sys.argv)
    serWin = ServerWindow()
    serWin.show()
    sys.exit(server.exec_())
