from tkinter import *
from tkinter import messagebox
import time
import os

class MainWindow():
	def __init__(self,username,send_func,refresh_func,close_func):
		self.main_window=None#=Tk()不直接写避免出现多个窗口
		self.online_list=None
		self.send_func=send_func
		self.username=username
		self.messagebox=None
		self.input_box=None
		self.refresh_func=refresh_func
		self.close_func=close_func
		self.curtag='#Group#' #current target

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
		Title_Labal=Label(self.main_window,bg='#444444',text='Chatroom',font=('黑体',18),fg='white').grid(row=0,column=0,sticky=E+W,columnspan=4,ipady=10)
		self.online_list=Listbox(self.main_window,height=30,bg='#333333',fg='white',font=('宋体',12))
		self.online_list.grid(row=1, column=0, rowspan=4, sticky=N + S, padx=10, pady=(0, 5))
		online_list_bar=Scrollbar(self.main_window)
		online_list_bar.grid(row=1,column=0,sticky=E+N+S,rowspan=4,padx=(0,10))
		online_list_bar['command'] = self.online_list.yview#绑定滚动条和列表
		self.online_list['yscrollcommand'] = online_list_bar.set

		self.messagebox=Text(self.main_window,width=97,state=DISABLED)  #消息记录框 常态下无法输入
		self.messagebox_history(0,0)
		self.messagebox.grid(row=1,column=1,sticky=N+S,rowspan=2)
		messagebox_bar=Scrollbar(self.main_window)
		messagebox_bar['command']=self.messagebox.yview
		self.messagebox['yscrollcommand']=messagebox_bar.set
		messagebox_bar.grid(row=1,column=1,stick=E+N+S,rowspan=2)

		self.input_box=Text(self.main_window,width=97,height=2)#输入框 
		self.input_box.grid(row=3,column=1,sticky=N+S,pady=(10,0))
		input_box_bar=Scrollbar(self.main_window)
		input_box_bar['command']=self.input_box.yview
		self.input_box['yscrollcommand']=input_box_bar.set
		input_box_bar.grid(row=3,column=1,stick=E+N+S,pady=(10,0))
		btn_frame=Frame(self.main_window,bg='#333333')
		send_btn=Button(btn_frame,text='发送',bg='lightgreen',width=5,font=('黑体',14),command=self.send_func).grid(row=0,column=0,sticky=W,padx=(50,100))
		send_btn=Button(btn_frame,text='清空',bg='red',width=5,font=('黑体',14),command=self.input_box_clean).grid(row=0,column=1,sticky=E,padx=(30,0))
		btn_frame.grid(row=4,column=1,sticky=E+W)  #

		refresh_btn=Button(self.main_window,text='刷新在线列表',command=self.refresh_func).grid(row=5,column=0)
		self.messagebox.tag_config('green',foreground='green') #foreground字体颜色 background填充背景颜色
		self.messagebox.tag_config('blue',foreground='blue')
		self.online_list.bind('<Double Button-1>',self.change_target)
		self.main_window.mainloop()

	def refresh(self,name):#刷新在线列表
		self.online_list.delete(0,END)#0 END表示从第一个到最后一个
		for names in name:
			self.online_list.insert(END,names)#在列表末尾插入names


	def change_target(self,event):# bind会返回event
		pos=self.online_list.curselection()[0]#返回的是元组
		self.curtag=self.online_list.get(pos)
		path=self.getfile(1,self.username,self.curtag)
		flag=os.path.isfile(path)
		if not flag:
			with open(path,'a+',encoding='utf-8') as record:
				pass
		if self.curtag=='#Group#':
			_type=0
		else:
			_type=1
		self.messagebox_history(_type,self.curtag)
		self.messagebox_history(_type,self.curtag)
		print(self.curtag)

	def input_box_clean(self):#清除输入框
		print(type(self.online_list))
		#self.online_list.insert(END,'在线列表')
		self.input_box.delete(0.0,END) # %d.%d表示x行y列 ，可以加''   表示从输入框的(0,0)处到末尾
		
	def getfile(self,_type,user,target):
		file_name='data\\record\\'+user+'\\'
		if _type==0:
			file_name+='group.txt'
		elif _type==1:
			file_name+=target+'.txt'
		return file_name

	def message_box_recv(self,user,content,_type,sender):#消息记录框新增内容
		#self.messagebox.config(state=NORMAL)#先将消息记录框从只读状态变为可修改状态
		head=sender+'  '+time.strftime("%Y-%m-%d %X")#一个显示当前日期的方法，可以百度time.strftime
		file_name=self.getfile(_type,self.username,user)
		with open(file_name,'a',encoding='utf-8') as record:
			record.write(sender+' '+head+'\n')
			record.write(' '+content)
		if self.curtag=='#Group#' and _type==0:
			self.messagebox_history(_type,self.curtag)
		elif self.curtag==user and _type==1:
			self.messagebox_history(_type,self.curtag)


	def messagebox_history(self,_type,target):
		self.messagebox.config(state=NORMAL)
		self.messagebox.delete(0.0,END)
		user=self.username
		file_name=self.getfile(_type,user,target)
		with open(file_name,'r',encoding='utf-8') as record:
			for content in record:
				pos=content.find(' ',0)
				user=content[0:pos]
				content=content[pos+1:-1]
				if pos==0:
					self.messagebox.insert(END,content+'\n')
					continue
				if user==self.username:#如果是本人发的就是绿色，否则是蓝色
					self.messagebox.insert(END,content+'\n','green')
				else:
					self.messagebox.insert(END,content+'\n','blue')
			self.messagebox.config(state=DISABLED)
		self.messagebox.see(END)

	def send_name(self):
		return self.curtag

	def getinput(self):#获取消息框内容
		content=self.input_box.get(0.0,END)
		if content=='' or content=='\n':
			messagebox.showerror('错误','消息为空')
			return -1
		return content





