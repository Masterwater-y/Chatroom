from LoginWindow import LoginWindow
from MainWindow import MainWindow
from RegisterWindow import RegWindow
from Client import Client
from tkinter import messagebox
import tkinter
import time
from threading import Thread
from PIL import ImageTk as itk
from PIL import Image as Img
import os

def open_mainwindow(user):
	global main_window
	main_window=MainWindow(user,send_message,refresh,close_main_window) #创建一个主界面的实例
	Thread(target=recv_data).start() #为当前主界面接收数据新开一个线程
	main_window.show() #显示主界面


def refresh(): #刷新在线列表
	client.refresh_req() #客户端向服务器发送刷新在线列表请求

def close_socket():
	print('尝试断开连接')
	client.sk.close() #关闭套接字

def close_main_window():
	close_socket() #关闭套接字，使服务器知道该连接断开
	main_window.main_window.destroy()#关闭主界面

def close_login_window():
	close_socket()
	login_window.login_window.destroy()

def mkdir(path):
	path=path.strip()
	path=path.rstrip('\\')
	isExist=os.path.exists(path)
	if not isExist:
		os.makedirs(path)

def login():#登录按钮绑定的函数
	user,key=login_window.getinput()# 获取登录窗口输入框的内容
	print(user+'   '+key)
	result=client.check_login(user,key)
	#print(result)
	if result=='0':#验证成功
		path='data\\record\\'+user+'\\'
		mkdir(path)
		with open(path+'group.txt','a+',encoding='utf-8') as record:
			pass
		login_window.close()#先关闭登录窗口 再开mainwindow，否则无法关闭登录窗口
		open_mainwindow(user) #打开主界面的函数
	elif result=='1':
		messagebox.showerror(title="错误", message="用户名或者密码错误")
	elif result=='2':
		messagebox.showerror(title="错误", message="账号已登录")
	else:
		messagebox.showerror(title="错误", message="未知错误")

def recv_data(): #客户端从服务器接收数据函数
	time.sleep(1)#等待主界面渲染好再接受数据，否则调用主界面的函数可能会出错
	print('接受消息线程启动')
	while True:
		try:
			_type=client.recv_string() #服务器先发送一个数字来告知操作类型 0 message  1 onlinelist
			if _type=='':
				continue
			print('type='+_type)
			if _type=='0': #接收的是群聊消息
				print('接受到服务器发来的消息')
				user=client.recv_string()
				content=client.recv_string()
				sender=user
				main_window.message_box_recv(user,content,0,sender)#收到消息后修改消息记录框
			elif _type=='1':#接收的是刷新在线列表
				print('refresh')
				name=[]
				num=int(client.recv_string())#在线人数
				for i in range(num): #接收在线人员名单
					name.append(client.recv_string())
				main_window.refresh(name)
			elif _type=='2':
				user=client.recv_string()
				content=client.recv_string()
				sender=client.recv_string()
				main_window.message_box_recv(user,content,1,sender)
		except Exception as e: #出现任何错误
			print('接受服务器消息错误:'+str(e))#！！！不加break退出会崩溃
			break


def send_message(): #主界面发送消息 函数
	content=main_window.getinput() #获取输入框的内容
	if content!=-1:#-1为空
		target=main_window.send_name()
		if target=='#Group#':
			client.send_message(content) #客户端向服务器发送内容
		else:
			client.private_sending(target,content) 
		main_window.input_box_clean() #发送之后清空输入框

def reg_back():# 注册界面返回按钮绑定的函数
	reg_window.close()
	login_window.show()

def reg_check():# 注册检测
	user,key,keycheck=reg_window.getinput() #注册界面获得的输入
	if key=='' or keycheck=='':
		messagebox.showerror(title='错误',message='密码为空')
		return
	if key==keycheck:
		flag=client.check_register(user,key)
		if flag=='0':
			messagebox.showinfo(title="提示", message="注册成功")
			reg_back()
		elif flag=='1':
			messagebox.showerror(title="错误", message="该账号已被占用")
		else:
			messagebox.showerror(title="错误", message="注册错误")
	else:
		messagebox.showerror(title="错误", message="两次密码输入不同")

def register(): #注册按钮绑定的函数
	login_window.close()
	global reg_window
	reg_window=RegWindow(reg_back,reg_check)#括号里传入的是上面定义的函数
	reg_window.show()
	

login_window=LoginWindow(login,register,close_login_window) # 创建登录窗口 括号里传入三个上面定义的函数
client=Client() #建立客户端socket
login_window.show()


