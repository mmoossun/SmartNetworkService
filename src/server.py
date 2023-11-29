from socket import *
import os
KEY = "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"
os.environ["OPENAI_API_KEY"] = KEY
# API key가 잘 연결되었는지 확인
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
def gpt(prompt):
    llm = ChatOpenAI(temperature=0.7,               # 창의성 (0.0 ~ 2.0) 
                 max_tokens=2048,             # 최대 토큰수
                 model_name='gpt-4-turbo',  # 모델명
                )
    # 질의내용
    
    answer = llm.predict(prompt)
    # 질의
    return answer

def send(sock,question):
    #sendData = input('>>>')
    aa = question.encode('utf-8')
    sock.send(aa)


def receive(sock):
    recvData = sock.recv(1024)
    print('상대방 :', recvData.decode('utf-8'))
    prompt = recvData.decode('utf-8')
    return gpt(prompt)

port = 8080

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print('%d번 포트로 접속 대기중...'%port)

connectionSock, addr = serverSock.accept()

print(str(addr), '에서 접속되었습니다.')

while True:
    question = receive(connectionSock)  # 클라이언트로부터의 메시지를 받음
    send(connectionSock, question) 