from socket import *
import json
import os
from threading import Thread
from tkinter import *

def register(array,name,passwd):
    stuDict = {} # 定义字典保存单个学生信息
    for i in range(len(array)):
        if array[i]['name'] == name:
            print("该用户名已存在")
            return

    stuDict['name'] = name
    stuDict['passwd'] = passwd
    array.append(stuDict)  # 把单个添加到总列表中
    with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            for i in range(len(array)):
                if i == len(array)-1 :
                    f.write(str(array[i]).replace("\n", ""))
                else:
                    f.write(str(array[i]).replace("\n", "") + "\n")
            f.close()
    print("注册成功")
    return'0'

def logIn(array,name,passwd):
    for i in range(len(array)):
        dict1 = array[i]
        if dict1['name'] == name and dict1['passwd']==passwd:
            print('用户密码正确')
            return '1'
    print("用户名或密码错误")
    return '0'

class ReceiveThread(Thread):
    def __init__(self, tcpCliSock, BUFSIZ=1024):
        Thread.__init__(self)
        self.daemon = True  # 守护线程
        self.tcpCliSock = tcpCliSock
        self.BUFSIZ = BUFSIZ

    def run(self):
        while True:
            data = tcpCliSock.recv(self.BUFSIZ)
            if not data:
                tcpCliSock.close()
                root.destroy()
            else:
                Output.insert(END, data.decode('utf-8'))

def sendMessage():
    # 发送消息
    msg1 = Input.get('1.0', END)
    msg='2'+name+':'+msg1
    tcpCliSock.send(msg.encode('utf-8'))
    Input.delete('1.0', END)

def onClosing():
    msg2='12'+name
    tcpCliSock.send(msg2.encode('utf-8'))
    tcpCliSock.shutdown(SHUT_WR)

flag='0'
while flag == '0':
 array = [] #定义list用于保存信息
 filename = 'users.txt' #文件名
 if not os.path.exists(filename) : # 判断文件是否存在
    file = open(filename, 'w') # 不存在就创建文件
    file.close()
 f = open(filename, "r")
 content = f.readlines()
 array.extend(content)
 array_temp = [] # 临时变量
 for i in range(len(array)): # 遍历转成字典
    print("第"+str(i)+"行:", array[i])
    if isinstance(array[i], str):  # 判断是否为字符串
        dict1 = json.loads(array[i].replace("'", "\"")) # 字符串转字典(json)
        array_temp.append(dict1)
 del array
 array = array_temp

 print('登录请输入1，注册请输入2')
 key=int(input('请输入1或2:'))
 name=input('请输入用户名')
 passwd=input('请输入密码')
 if key==1:
     flag=logIn(array,name,passwd)
     
 elif key==2:
     flag=register(array,name,passwd)


HOST = '127.0.0.1'  #客户端IP
POST = 13141        #客户端端口
BUFSIZ = 1024      #定义缓冲大小
ADDR = (HOST,POST)
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

root = Tk()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.geometry('+{}+{}'.format((sw-430)//2, (sh-340)//2))
root.title('Python聊天群 ({})'.format(name))

frameT = Frame(root, width=460, height=320)
frameB = Frame(root, width=460, height=80)
frameT.pack(expand='yes', fill='both')
frameB.pack(expand='yes', fill='both')

Input = Text(frameB, height=6)
Output = Text(frameT)
Input.pack(expand='yes', fill='both')
Output.pack(expand='yes', fill='both')

btnFrame = Frame(frameB, height=24, background='White')
btnFrame.pack(expand='yes', fill='both')

Button(btnFrame, text='发送', width=8, bg='DodgerBlue', fg='White', command=sendMessage).pack(side=RIGHT)

notice='11'+name
tcpCliSock.send(notice.encode('utf-8'))
ReceiveThread(tcpCliSock).start()  # 启动消息接收线程
root.protocol("WM_DELETE_WINDOW", onClosing)  # 退出时处理
root.mainloop()






