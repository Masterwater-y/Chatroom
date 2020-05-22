from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import time
import os
from PIL import ImageTk as itk
from PIL import Image as Img

class MainWindow():
	def __init__(self,username,send_func,refresh_func,close_func,send_pic_func):
		self.main_window=None#=Tk()不直接写避免出现多个窗口
		self.online_list=None
		self.send_func=send_func
		self.username=username
		self.messagebox=None
		self.input_box=None
		self.refresh_func=refresh_func
		self.close_func=close_func
		self.curtag='!Group!' #current target
		self.title_var=None
		self.unread={}
		self.send_pic_func=send_pic_func
		self.img=[]#存储消息记录中的图片
		self.num=-1
	def show(self):
		self.main_window=Tk()
		self.main_window.configure(bg='#333333')
		self.main_window.protocol("WM_DELETE_WINDOW", self.close_func)
		screen_height=self.main_window.winfo_screenheight()
		screen_width=self.main_window.winfo_screenwidth()
		main_width=870
		main_height=600
		main_px=(screen_width-main_width)/2
		main_py=(screen_height-main_height)/2
		main_size='%dx%d+%d+%d' %(main_width,main_height,main_px,main_py)
		self.main_window.geometry(main_size)
		self.main_window.title('Chatroom')
		self.title_var=StringVar()
		self.title_var.set('!Group!')
		self.Title_Label=Label(self.main_window,bg='#444444',textvariable=self.title_var,font=('黑体',18),fg='white').grid(row=0,column=0,sticky=E+W,columnspan=4,ipady=10)
		self.online_list=Listbox(self.main_window,height=30,bg='#333333',fg='white',font=('宋体',12))
		self.online_list.grid(row=1, column=0, rowspan=4, sticky=N + S, padx=10, pady=(0, 5))
		online_list_bar=Scrollbar(self.main_window)
		online_list_bar.grid(row=1,column=0,sticky=E+N+S,rowspan=4,padx=(0,10))
		online_list_bar['command'] = self.online_list.yview#绑定滚动条和列表
		self.online_list['yscrollcommand'] = online_list_bar.set

		self.messagebox=Text(self.main_window,width=97,state=DISABLED)  #消息记录框 常态下无法输入
		self.messagebox_history(self.curtag)

		self.messagebox.grid(row=1,column=1,sticky=N+S,rowspan=2)
		messagebox_bar=Scrollbar(self.main_window)
		messagebox_bar['command']=self.messagebox.yview
		self.messagebox['yscrollcommand']=messagebox_bar.set
		messagebox_bar.grid(row=1,column=1,stick=E+N+S,rowspan=2)

		self.input_box=Text(self.main_window,width=97,height=2)#输入框 
		self.input_box.grid(row=3,column=1,sticky=N+S,pady=(40,0))
		input_box_bar=Scrollbar(self.main_window)
		input_box_bar['command']=self.input_box.yview
		self.input_box['yscrollcommand']=input_box_bar.set
		input_box_bar.grid(row=3,column=1,stick=E+N+S,pady=(40,0))
		btn_frame=Frame(self.main_window,bg='#333333')
		send_btn=Button(btn_frame,text='发送',bg='lightgreen',width=5,font=('黑体',14),command=self.send_func).grid(row=0,column=0,sticky=W,padx=(50,100))
		send_btn=Button(btn_frame,text='清空',bg='red',width=5,font=('黑体',14),command=self.input_box_clean).grid(row=0,column=1,sticky=E,padx=(30,0))
		btn_frame.place(x=200,y=530)  

		send_pic_btn=Button(self.main_window,text='发送图片',command=self.send_pic_func).place(x=200,y=370)
		clean_rec_btn=Button(self.main_window,text='清空聊天记录',command=self.messagebox_clean).place(x=300,y=370)

		refresh_btn=Button(self.main_window,text='刷新在线列表',command=self.refresh_func).grid(row=5,column=0)
		self.messagebox.tag_config('green',foreground='green') #foreground字体颜色 background填充背景颜色
		self.messagebox.tag_config('blue',foreground='blue')
		self.online_list.bind('<Double Button-1>',self.change_target)
		self.main_window.bind('<Return>',self.bind_send)
		self.main_window.mainloop()

	def refresh(self,name):#刷新在线列表
		self.online_list.delete(0,END)#0 END表示从第一个到最后一个
		group_un='!Group!'
		self.unread.setdefault(group_un,0)
		if self.unread['!Group!']!=0:
			group_un+='('+str(self.unread['!Group!'])+')'
		self.online_list.insert(END,group_un)
		self.name=name
		for names in name:
			self.unread.setdefault(names,0)
			if self.unread[names]!=0:
				names=names+'('+str(self.unread[names])+')'
			self.online_list.insert(END,names)#在列表末尾插入names

	def messagebox_clean(self):#清空消息记录
		user=self.username
		target=self.curtag
		file_name=self.getfile(user,target)
		with open(file_name,'w',encoding='utf-8') as record:
			pass
		self.messagebox_history(target)

	def bind_send(self,event):#绑定发送消息请求
		self.send_func()

	def get_pic(self):#选择发送图片的路径
		path=filedialog.askopenfilename()
		return path,self.curtag

	def deal_repeat(self,pos):#处理文件名重复,防止影响历史记录读取
		origin=self.online_list.get(pos)
		pos1=-1
		for i in range(len(origin)-1,-1,-1):
			if origin[i]=='(':
				pos1=i
				break
			if origin[i] not in ('0123456789()'):
				break
		if pos1==-1:
			self.curtag=origin
		else:
			self.curtag=origin[0:pos1]

	def change_target(self,event):# 切换聊天对象   bind会返回event
		pos=self.online_list.curselection()[0]#返回的是元组
		self.deal_repeat(pos)
		if self.curtag==self.username:
			return
		self.title_var.set(self.curtag)
		path=self.getfile(self.username,self.curtag)
		flag=os.path.isfile(path)
		if not flag:
			with open(path,'a+',encoding='utf-8') as record:
				pass
		self.messagebox_history(self.curtag)
		self.unread[self.curtag]=0
		self.refresh_func()
		#print(self.curtag)

	def input_box_clean(self):#清除输入框
		self.input_box.delete(0.0,END) # %d.%d表示x行y列 ，可以加''   表示从输入框的(0,0)处到末尾
		
	def getfile(self,user,target):#获取消息记录文件名
		file_name='data\\record\\'+user+'\\'
		file_name+=target+'.txt'
		return file_name

	def message_box_recv(self,target,content,sender):#消息记录框新增内容
		#self.messagebox.config(state=NORMAL)#先将消息记录框从只读状态变为可修改状态
		head=sender+'  '+time.strftime("%Y-%m-%d %X")#一个显示当前日期的方法，可以百度time.strftime
		file_name=self.getfile(self.username,target)
		with open(file_name,'a',encoding='utf-8') as record:
			record.write(sender+' '+head+'\n')
			record.write(' '+content+'\n')
		now=self.curtag
		if now==target:
			self.messagebox_history(now)
			return
		if sender==self.username:
			return
		if target=='!Group!':
			self.unread.setdefault('!Group!',0)
			self.unread['!Group!']+=1
			return
		self.unread.setdefault(sender,0)
		self.unread[sender]=self.unread[sender]+1
		#print(self.unread)

	def messagebox_history(self,target):#读取消息记录并显示
		self.messagebox.config(state=NORMAL)
		self.messagebox.delete(0.0,END)
		user=self.username
		file_name=self.getfile(user,target)
		with open(file_name,'r',encoding='utf-8') as record:
			for content in record:
				pos=content.find(' ',0)
				user=content[0:pos]
				content=content[pos+1:].rstrip('\n')
				flag=os.path.exists(content)#如果内容是路径就判定为图片
				if pos==0:
					if flag:
						self.num=self.num+1
						self.img.append(itk.PhotoImage(file=content))
						self.messagebox.image_create(END,image=self.img[self.num])#img用全局变量，否则图片显示空白，且每张图都要单独用一个变量
						self.messagebox.insert(END,'\n')
					else:
						self.messagebox.insert(END,content+'\n')
					continue
				if user==self.username:#如果是本人发的就是绿色，否则是蓝色
					self.messagebox.insert(END,content+'\n','green')
				else:
					self.messagebox.insert(END,content+'\n','blue')
			self.messagebox.config(state=DISABLED)
		self.messagebox.see(END)

	def send_name(self):#发送当前聊天对象
		return self.curtag

	def get_name(self):
		return self.username
	def getinput(self):#获取消息框内容
		content=self.input_box.get(0.0,END)
		if content=='' or content=='\n':
			messagebox.showerror('错误','消息为空')
			return -1
		return content





