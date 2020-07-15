import socket
from threading import Thread
import math
import struct
import os

online_user=[]#list  dont use tuple 在线的socket
sock_user={}#字典 存储socket对应的id
user_sock={}#id对应socket
user_nick={}#id对应昵称

def send_string(sock,content): #socket通信发送数据，需要把数据转换为byte类型，并且先告知数据的长度
	sock.sendall(len(bytes(content,encoding='utf-8')).to_bytes(4,byteorder='big'))#将发送的内容的长度以utf-8协议转换为4字节的byte byteorder是指字节序
	sock.sendall(bytes(content,encoding='utf-8')) #将发送的内容转换为Byte类型
def recv_string(sock):#接收客户端发来的数据
	length=int.from_bytes(sock.recv(4),byteorder='big') #接收4字节长的数据长度
	maxsize=3*1024 #规定每次接收的最大数据长度 一般小于8M
	content='' 
	time=math.ceil(length/maxsize)#超过3M的数据分多次接收 math.ceil表示向上取整
	for i in range(time):
		if i==time-1:
			content=content+str(sock.recv(length%maxsize),encoding='utf-8')
		else:
			content=content+str(sock.recv(maxsize),encoding='utf-8')
	return content

def check_login(user,key):#服务器检查登录
	is_user=True #第一行为账号，第二行为密码，判断当前行是否为账号
	flag=False
	i=0
	with open('server\\data\\user.in','r',encoding='utf-8') as data:
		for content in data:
			content=content.replace('\n','')
			i=i+1
			#if i==1:#从第一行开始存储会出错，未找到原因只好从第二行开始
				#continue
			if (is_user) and (content==user):
				flag=True
			if (not is_user) and flag:
				return(content==key)
			is_user=not is_user
	return(False)

def loading(sock):
	user=sock_user[sock]
	path=os.path.join('server','data',user)
	isExist=os.path.exists(path)
	if not isExist:
		print('为新用户生成文件夹:',path)
		os.makedirs(path)
	with open(path+'/inform.txt','a+',encoding='utf-8') as inform:
		flag=os.path.getsize(path+'/inform.txt')
		if not flag:
			inform.write(user+'\n')
			inform.write(user+'\n')
			inform.write('4'+'\n')
			inform.write('未填写'+'\n')
			inform.write('-1'+'\n')

def handle_login(sock): #处理登录请求
	print(divide)
	print('开始处理登录请求')
	print('准备验证账号密码')
	user=recv_string(sock)#从客户端接收账号和密码
	key=recv_string(sock)
	print('账号:'+user,' 密码:'+key)
	check_login(user,key)
	if check_login(user,key):
		if user not in sock_user.values():#如果不在已登录列表
			print(user,':登录验证成功')
			print('存储socket信息')
			online_user.append(sock)#加入在线socket列表
			sock_user[sock]=user
			user_sock[user]=sock 
			send_string(sock,'0')#0为成功
			handle_onlinelist()#更新在线列表
			loading(sock)
			for users in online_user:
				send_string(users,'#rIcon#')
				send_icon(users,user)
				send_string(users,'#refresh#')
		else:
			send_string(sock,'2')#已登录
			print(user,':已登录')
	else:
		send_string(sock,'1')#密码错误
		print(user,':密码错误')
	print(divide)

def handle_register(sock):#处理注册请求
	print(divide)
	print('开始处理注册请求')
	user=recv_string(sock)
	key=recv_string(sock)
	is_user=True
	with open('server\\data\\user.in','a',encoding='utf-8') as data:
		pass
	with open('server\\data\\user.in','r',encoding='utf-8') as data:
		for content in data:
			content=content.rstrip('\n')
			if is_user and content==user:
				Flag=False
				send_string(sock,'1')
				print(user+'已被注册')
				print(divide)
				return#已被注册
			is_user=not is_user
	with open('server\\data\\user.in','a',encoding='utf-8') as data:
		data.write(user+'\n')
		data.write(key+'\n')
	send_string(sock,'0')
	print(user+':注册成功')#0 注册成功-
	print(divide)
	return


def handle_sending(sock):#处理发送消息请求，即服务器把收到的信息分发给所有在线的人
	print(divide)
	print('开始处理发送信息')
	content=recv_string(sock)
	print('收到消息:'+content)
	for user in online_user:#遍历在线的socket
		send_string(user,'0')#发送0告知客户端后面要接收消息数据
		send_string(user,'!Group!')#发送消息来源人
		send_string(user,content)#发送内容
		send_string(user,sock_user[sock])
	print('消息:{}发送完成'.format(content))
	print(divide)

def handle_private_send(sock):
	print(divide)
	print('开始处理私聊请求')
	user=sock_user[sock]
	target=user_sock[recv_string(sock)]
	content=recv_string(sock)
	print('获取发送内容:',content)
	send_string(target,'2')
	send_string(target,user)#当前通话对象
	send_string(target,content)
	send_string(target,user)#发送者
	if sock_user[target]!=user:#不是发给自己
		send_string(sock,'2')
		send_string(sock,sock_user[target])#当前通话对象
		send_string(sock,content)
		send_string(sock,user)#发送者
	print('发送成功')
	print(divide)

def recv_pic(sock):
	target=recv_string(sock)
	filename=recv_string(sock)#不含路径的文件名
	filesize=int(recv_string(sock))
	file_route=os.path.join('server','data',sock_user[sock],filename)#服务器中存放的地址
	i=0
	while os.path.exists(file_route):#防止文件名重复被覆盖
		i+=1
		for j in range(len(file_route)-1,-1,-1):
			if file_route[j]=='.':
				break
		file_route=file_route[0:j]+'('+str(i)+')'+file_route[j:]
	recvd_size = 0 #接收了的文件大小
	file = open(file_route,'wb')
	print ('开始接收图片')
	while not recvd_size == filesize:#recv是阻塞的，接收完要停止
		if filesize - recvd_size > 1024:
			rdata = sock.recv(1024)
			recvd_size += len(rdata)
		else:
			rdata = sock.recv(filesize - recvd_size) 
			recvd_size = filesize
		file.write(rdata)
	file.close()
	return target,filename,filesize,file_route
	print ('图片接收完成')

def recv_icon(sock):#获取头像
	user=sock_user[sock]
	filename=user+'.png'#不含路径的文件名
	filesize=int(recv_string(sock))
	file_route=os.path.join('server','icon',filename)#服务器中存放的地址
	recvd_size = 0 #定义接收了的文件大小
	file = open(file_route,'wb')
	print ('开始接收头像')
	while not recvd_size == filesize:
		if filesize - recvd_size > 1024:
			rdata = sock.recv(1024)
			recvd_size += len(rdata)
		else:
			rdata = sock.recv(filesize - recvd_size) 
			recvd_size = filesize
		file.write(rdata)
	file.close()
	return file_route
	print ('头像接收完成')

def send_icon(sock,user):#发送头像
	send_string(sock,user)
	path=os.path.join('server','icon',user+'.png')
	if not os.path.exists(path):
		path=os.path.join('server','icon','default.png')
	print(path)
	send_string(sock,str(os.stat(path).st_size))
	print(str(os.stat(path).st_size))
	file=open(path,'rb')
	while True:
		filedata=file.read(1024)
		if not filedata:
			break
		sock.sendall(filedata)
	file.close()

def handle_onlinelist():#处理更新在线列表请求
	print(divide)
	print('开始处理刷新列表')
	num=str(len(online_user))
	print('在线人数:',num)
	print('在线列表:')
	for user in online_user:
		send_string(user,'1')#先发送1告知客户端将要接收更新在线列表的消息
		send_string(user,num)
		print(sock_user[user])
		for name in online_user:
			send_string(user,sock_user[name])
	print('刷新列表处理完成')
	print(divide)



def handle_pic(sock):#处理发送图片请求
	print(divide)
	print('开始处理图片发送请求')
	sender=sock_user[sock]
	targets,filename,filesize,file_route=recv_pic(sock)
	filesize=str(filesize)#转为str传输
	print('图片发送目标:{}, 文件名:{}, 文件大小:{}, 服务器存储路径:{}'.format(targets,filename,filesize,file_route))
	if targets=='!Group!':
		for user in online_user:#群聊给每个人都发
			send_string(user,'#Picture#')
			send_string(user,sender)
			send_string(user,'!Group!')
			send_string(user,filename)
			send_string(user,filesize)
			file=open(file_route,'rb')
			while True:
				filedata=file.read(1024)
				if not filedata:
					break
				user.sendall(filedata)
			file.close()
	else:
		target=user_sock[targets]#私聊只发对象
		send_string(target,'#Picture#')
		send_string(target,sender)
		send_string(target,sock_user[sock])
		send_string(target,filename)
		send_string(target,filesize)
		file=open(file_route,'rb')
		while True:
			filedata=file.read(1024)
			if not filedata:
				break
			target.sendall(filedata)
		file.close()
		send_string(sock,'#Picture#')
		send_string(sock,sender)
		send_string(sock,targets)
		send_string(sock,filename)
		send_string(sock,filesize)
		file=open(file_route,'rb')
		while True:
			filedata=file.read(1024)
			if not filedata:
				break
			sock.sendall(filedata)
		file.close()
	print('图片发送成功')
	print(divide)

def handle_gIcon(sock):#给登录者发送所有在线者的最新头像
	for user in online_user:
		send_string(sock,'#rIcon#')#refresh icon
		username=sock_user[user]
		send_icon(sock,username)
	#print('user:',user)

def handle_rIcon(sock):#向所有人发送头像更新者的新头像
	username=sock_user[sock]
	print(username)
	recv_icon(sock)
	for user in online_user:
		send_string(user,'#rIcon#')
		send_icon(user,username)
		send_string(user,'#refresh#')

def handle_Inform(sock):#发送个人信息
	user=recv_string(sock)
	path=os.path.join('server','data',user)
	print('user=',user)
	send_string(sock,'#Inform#')
	with open(path+'/inform.txt','r',encoding='utf-8') as inform:
		for content in inform:
			content=content.rstrip('\n')
			send_string(sock,content)

def handle_rInform(sock):#接收新个人信息
	user=sock_user[sock]
	path=os.path.join('server','data',user)
	val=[]
	val.append(user)
	for i in range(4):
		val.append(recv_string(sock))
	with open(path+'/inform.txt','w',encoding='utf-8') as inform:
		for content in val:
			inform.write(content+'\n')


def handle(sock,addr):#处理请求
	try:
		while True:
			_type=recv_string(sock)#请求的类型
			if _type=='1':
				handle_login(sock)
			elif _type=='2':
				handle_register(sock)
			elif _type=='3':
				handle_sending(sock)
			elif _type=='4':
				handle_onlinelist()
			elif _type=='5':
				handle_private_send(sock)
			elif _type=='#Picture#':
				handle_pic(sock)
			elif _type=='#gIcon#':
				print('here')
				handle_gIcon(sock)
			elif _type=='#rIcon#':
				print('here')
				handle_rIcon(sock)
			elif _type=='#Inform#':#获取个人信息请求
				handle_Inform(sock)
			elif _type=='#rInform#':#更新个人信息请求
				handle_rInform(sock)
	except Exception as e:
		print(str(addr) + " 连接异常，准备断开: " + str(e))
	finally:#如果连接断开，将对应的人清除出列表
		try:
			sock.close()
			online_user.remove(sock)
			sock_user.pop(sock)
			handle_onlinelist()
		except:
			print(str(addr)+'连接关闭异常')
			#handle onlinelist

def connect_db():#连接数据库
	global db,cursor
	db = pymysql.connect(
	host='localhost',
	user='admin',password='admin',
	database='Chatroom',
	charset='utf8')
	cursor=db.cursor()
	cursor.execute('use Chatroom')

#connect_db()
sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)#使用TCP协议
divide='------------------------'#分割线
#sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.bind(('172.18.28.174',1234))#socket绑定到ip地址 172.18.28.174是租借的阿里云的私有ip
sk.listen(10)#最大连接数
print("服务器启动成功，开始监听...")
try:
	while True:
		sock, addr=sk.accept() #socket address
		Thread(target=handle,args=(sock, addr)).start()#给监听到的每一个socket新建一个线程运行handle
except Exception as e:
	sk.close()
	#cursor.close()
	#db.close()
