import socket
import math
import os
class Client:
	def __init__(self): 
		self.sk=socket.socket()#为实例创建一个socket
		#self.sk.settimeout(600)
		self.sk.connect(('127.0.0.1',13333))#绑定到服务器和对应端口
		#self.filesize=0

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

	def send_pic(self,path,target):
		self.send_string('#Picture#')
		self.send_string(target)
		self.send_string(os.path.basename(path))
		self.send_string(str(os.stat(path).st_size))
		print ('client filepath: ',path)
		print(os.stat(path).st_size)
		# with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
		file=open(path,'rb')
		while True:
			filedata=file.read(1024)
			if not filedata:
				break
			self.sk.sendall(filedata)
		file.close()
		print ('send over...')

	def recv_pic(self,user,target):
		filename=self.recv_string()
		filesize=int(self.recv_string())
		file_route=os.path.join('data','file_recv',user,filename)#本地存放的地址
		i=0
		while os.path.exists(file_route):
			i+=1
			for j in range(len(file_route)-1,-1,-1):
				if file_route[j]=='.':
					break
			file_route=file_route[0:j]+'('+str(i)+')'+file_route[j:]
		print ('file new name is %s, self.filesize is %s' %(file_route,filesize))
		recvd_size = 0 #定义接收了的文件大小
		file = open(file_route,'wb')
		print ('stat receiving...')
		while not recvd_size == filesize:
			if filesize - recvd_size > 1024:
				rdata = self.sk.recv(1024)
				recvd_size += len(rdata)
			else:
				rdata = self.sk.recv(filesize - recvd_size) 
				recvd_size = filesize
			file.write(rdata)
		file.close()
		return file_route

