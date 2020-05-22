import socket
from threading import Thread
import math

online_user=[]#list  dont use tuple 在线的socket
sock_user={}#字典 存储socket对应的名字
user_sock={}#名字对应socket

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

def check_login(username,key):#服务器检查登录
	is_user=True #第一行为账号，第二行为密码，判断当前行是否为账号
	flag=False
	user=username
	i=0
	print('in check_login')
	with open('data\\user.in','r',encoding='utf-8') as data:
		for content in data:
			content=content.replace('\n','')
			i=i+1
			if i==1:#从第一行开始存储会出错，未找到原因只好从第二行开始
				continue
			if (is_user) and (content==user):
				flag=True
				#print('hello',flag)
			if (not is_user) and flag:
				print('key=',key,' final check=',content==key)
				return(content==key)
			is_user=not is_user
	return(False)



def handle_login(sock): #处理登录请求
	print('ready to check the user and key')
	user=recv_string(sock)#从客户端接收账号和密码
	key=recv_string(sock)
	print('user:'+user,' key'+key)
	check_login(user,key)
	if check_login(user,key):
		if user not in sock_user.values():#如果不在已登录列表
			print('存储socket信息')
			online_user.append(sock)#加入在线socket列表
			print(str(len(online_user)))
			sock_user[sock]=user
			user_sock[user]=sock 
			send_string(sock,'0')#0为成功
			handle_onlinelist()#更新在线列表
		else:
			send_string(sock,'2')#已登录
	else:
		send_string(sock,'1')#密码错误

def handle_register(sock):#处理注册请求
	user=recv_string(sock)
	key=recv_string(sock)
	is_user=True
	Flag=True
	with open('data\\user.in','r',encoding='utf-8') as data:
		for content in data:
			content=content.rstrip('\n')
			if is_user and content==user:
				Flag=False
				send_string(sock,'1')
				return#已被注册
			is_user=not is_user
	with open('data\\user.in','a',encoding='utf-8') as data:
		data.write(user+'\n')
		data.write(key+'\n')
	send_string(sock,'0')
	print(user+'注册成功')#0 注册成功-
	return

def handle_sending(sock):#处理发送消息请求，即服务器把收到的信息分发给所有在线的人
	content=recv_string(sock)
	print('收到消息:'+content)
	#print(str(len(online_user)))
	for user in online_user:#遍历在线的socket
		send_string(user,'0')#发送0告知客户端后面要接收消息数据
		print('sending tips 0')
		send_string(user,sock_user[sock])#发送消息来源人
		send_string(user,content)#发送内容

def handle_private_send(sock):
	user=sock_user[sock]
	target=user_sock[recv_string(sock)]
	content=recv_string(sock)
	send_string(target,'2')
	send_string(target,user)
	send_string(target,content)
	send_string(target,user)
	send_string(sock,'2')
	send_string(sock,sock_user[target])
	send_string(sock,content)
	send_string(sock,user)



def handle_onlinelist():#处理更新在线列表请求
	num=str(len(online_user))
	print(num)
	for user in online_user:
		send_string(user,'1')#先发送1告知客户端将要接收更新在线列表的消息
		send_string(user,num)
		for name in online_user:
			send_string(user,sock_user[name])


def handle(sock,addr):#处理请求
	try:
		while True:
			_type=str(sock.recv(1),'utf-8')#先接收一个4字节数字 表示请求的类型
			print('type=',_type)
			if _type=='1':
				print('开始处理登录请求')
				handle_login(sock)
			elif _type=='2':
				print('开始处理注册请求')
				handle_register(sock)
			elif _type=='3':
				print('开始处理发送信息')
				handle_sending(sock)
			elif _type=='4':
				print('开始处理刷新列表')
				handle_onlinelist()
			elif _type=='5':
				handle_private_send(sock)
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

sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
sk.bind(('127.0.0.1',13333))#socket绑定到ip地址 127.0.0.1表示本地，13333是端口
sk.listen(10)#最大连接数
print("服务器启动成功，开始监听...")
while True:
	sock, addr=sk.accept() #socket address
	Thread(target=handle,args=(sock, addr)).start()#给监听到的每一个socket新建一个线程运行handle