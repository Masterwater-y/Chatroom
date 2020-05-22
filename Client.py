import socket
import math
class Client:
	def __init__(self): 
		self.sk=socket.socket()#为实例创建一个socket
		self.sk.connect(('127.0.0.1',13333))#绑定到服务器和对应端口

	def send_string(self,content):#先发送内容长度，再发送内容
		print(1)
		self.sk.sendall(len(bytes(content,encoding='utf-8')).to_bytes(4,byteorder='big'))
		self.sk.sendall(bytes(content,encoding='utf-8'))
		
	def recv_string(self):
		length=int.from_bytes(self.sk.recv(4),byteorder='big')
		maxsize=3*1024
		content=''
		time=math.ceil(length/maxsize)
		for i in range(time):
			if i==time-1:
				content=content+str(self.sk.recv(length%maxsize),encoding='utf-8')
			else:
				content=content+str(self.sk.recv(maxsize),encoding='utf-8')
		return content

	def check_login(self,user,key):
		self.send_string('1')# 1登录请求
		self.send_string(user)
		self.send_string(key)
		return self.recv_string()

	def check_register(self,user,key):
		self.send_string('2')# 2注册请求
		self.send_string(user)
		self.send_string(key)
		return self.recv_string()

	def refresh_req(self):
		self.send_string('4')

	def send_message(self,content):
		self.send_string('3')#发送信息请求
		self.send_string(content)

	def private_sending(self,target,content):
		self.send_string('5')
		self.send_string(target)
		self.send_string(content)

