from socket import *
from select import select
from json import loads


HOST = ''  #监听所有的IP
POST = 13141
BUFSIZ = 1024
ADDR = (HOST,POST)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
tcpSerSock.setblocking(False)# 将tcpSerSock设置为非租塞模式

inputs = [tcpSerSock]

print('waiting for connnecting...')
users=[]
while True:
    rlist, wlist, xlist = select(inputs, [], [])
    for s in rlist:
        if s is tcpSerSock:
            tcpCliSock, addr = s.accept()
            print('...connecting from:', addr)
            tcpCliSock.setblocking(False) # 将tcpCliSock设置为非租塞模式
            inputs.append(tcpCliSock)# 将tcpCliSock插入inputs中
            
        else:
            data = s.recv(BUFSIZ)
#无限循环检查 inputs 中套接字的可读性，当有满足条件套接字时（客户端连接请求和客户端发送消息）返回 rlist、wlist、xlist 三个变量，
#遍历 rlist 中所有套接字，如果 s 是连接套接字（tcpCliSock），那么就接受客户端的连接请求，
#并将返回的新套接字插入 inputs 中。如果 s 是通信套接字，那么就接受信息，处理并返回。

            if not data:
                inputs.remove(s)
                s.close()
                continue
 
            data = data.decode('utf-8')
            if data[0]=='1':
              if data[1]=='1':
               name=data[2:]
               users.append(name)
               notice1=name+'加入了聊天,当前在线人有'+','.join(users)+'\n'
              elif data[1]=='2':
               name=data[2:]
               users.remove(name)
               notice1=name+'离开了聊天,当前在线人有'+','.join(users)+'\n'
              for sock in inputs:
                if sock is not tcpSerSock:
                    sock.send(notice1.encode('utf-8'))

            elif data[0]=='2':
              data=data[1:]
              for sock in inputs:
                if sock is not tcpSerSock:
                    sock.send(data.encode('utf-8'))
            print(data)

        




     

