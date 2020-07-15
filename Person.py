from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
from Tips import Tips
from PIL import ImageTk as itk
from PIL import Image as Img
import sys
import time

class Person(Toplevel):#是顶级窗口的子类
	def __init__(self,parent,curtag,send_icon_func,flag,ask_inform_func,get_inform_func,send_inform_func):
		self.parent=parent#绑定控件的父亲
		self.curtag=curtag#该窗口的用户
		self.send_icon_func=send_icon_func#向服务器发送头像
		self.ask_inform_func=ask_inform_func#向服务器发送获取个人信息请求
		self.get_inform_func=get_inform_func#获取个人信息
		self.send_inform_func=send_inform_func#发送新个人信息
		self.sex_box=None
		self.age_box=None
		Toplevel.__init__(self,self.parent, padx=1, pady=1,bg='white')#初始化父类
		self.geometry('400x600')
		top_img=itk.PhotoImage(file='image/person_top.png')
		self.edit_img=itk.PhotoImage(file='image/edit_top.png')
		self.top_label=Label(self,image=top_img)#标签
		self.top_label.grid(row=0,column=0,sticky=W+E)
		path='data/icon/'+curtag+'b.png'
		icon_img=itk.PhotoImage(file=path)
		icon_canva=Canvas(self,bg='white',width=125,height=125,borderwidth=0,highlightthickness=0)
		icon_canva.create_image(63,63,image=icon_img)
		#print('flag=',flag)
		if flag:#更改资料权限
			icon_canva.configure(cursor='hand2')
			icon_tips=Tips(icon_canva,'更改头像')
			icon_canva.bind('<Button-1>',self.bind_icon)
		icon_canva.grid(row=1,column=0,pady=(35,0))

		frame_img=itk.PhotoImage(file='image/infframe.png')
		self.bg_canva=Canvas(self,width=400,height=293,highlightthickness=0,borderwidth=0,bg='blue')
		self.bg_canva.create_image(200,293/2-1,image=frame_img)
		self.bg_canva.grid(row=2,column=0,pady=(20,0))
		self.entrys=[]
		self.content=[]
		self.inform=[]
		self.place_longt=None
		self.ask_inform_func(self.curtag)#向服务器发送获取个人信息请求
		time.sleep(2)#给时间下载个人信息，否则后面渲染出错
		self.inform=self.get_inform_func()
		self.inform[2]=self.trans_inform(0,self.inform[2])
		divide='---------------------'
		print()
		print(divide)
		print('获取个人信息:',self.inform)
		for i in range(5):
			self.content.append(StringVar())
			self.content[i].set(str(self.inform[i]))
			length,longt=self.getlen(self.inform[i])
			if i==3:
				self.place_longt=longt
			self.entrys.append(Entry(self.bg_canva,textvariable=self.content[i],font=('宋体',-16),highlightthickness=0,borderwidth=0,width=length,bg='white',state=DISABLED))
			self.entrys[i].place(x=370-longt,y=25+50*i,height=25)
		self.entrys[0].configure(state=DISABLED)

		save_btn_img=itk.PhotoImage(file='image/save_btn.png')
		edit_btn_img=itk.PhotoImage(file='image/edit_btn.png')
		self.save_btn=Button(self,image=save_btn_img,command=self.bind_save,borderwidth=0,highlightthickness=0)
		self.edit_btn=Button(self,image=edit_btn_img,command=self.edit,borderwidth=0,highlightthickness=0)
		if flag:#修改资料权限
			self.edit_btn.place(x=338,y=14)
		print(self.curtag,'个人信息窗口渲染完毕')
		print(divide)
		print()
		self.mainloop()

	def trans_inform(self,_type,val):
		if _type==0:
			if val=='1':
				return('男')
			elif val=='2':
				return('女')
			elif val=='3':
				return('其他')
			else:
				return('未填写')
	def bind_icon(self,event):
		path=filedialog.askopenfilename()
		if path=='':#没选择图片
			return
		self.send_icon_func(self.curtag,path)#向服务器发送新头像

	def edit(self):#编辑资料
		self.top_label.configure(image=self.edit_img)
		self.entrys[1].configure(state=NORMAL)
		self.entrys[3].configure(state=NORMAL,width=50)
		self.entrys[3].place(x=370-self.place_longt-50,y=25+50*3)
		self.entrys[2].place_forget()
		self.entrys[4].place_forget()
		self.sex_box=ttk.Combobox(self.bg_canva,width=3,state='readonly')
		self.sex_box['values']=('男','女','其他')
		self.sex_box.current(0)#默认值
		self.sex_box.place(x=330,y=125)
		#性别选择框
		self.age_box=ttk.Combobox(self.bg_canva,width=3,state='readonly')
		self.age_box['values']=('0','1')
		for i in range(2,121,1):
			self.age_box['values']+=(str(i),)
		self.age_box.current(0)
		#年龄选择框
		self.age_box.place(x=330,y=225)
		self.save_btn.place(x=338,y=14)
		self.edit_btn.place_forget()

	def bind_save(self):#保存个人资料
		val=[]
		for i in range(1,5,1):
			now=self.content[i].get()
			if i==2:
				now=self.sex_box.get()
			elif i==4:
				now=self.age_box.get()
			val.append(now)
		self.send_inform_func(val)#向服务器发送新个人信息
		messagebox.showinfo('提示','保存成功')
		self.withdraw()#保存后关闭窗口

	def getlen(self,content):#-12=12px, 中文12px,英文和符号6px  目的是使右对齐
		length=0
		longt=0
		for ch in content.encode('utf-8').decode('utf-8'):
			if u'\u4e00' <= ch <= u'\u9fff':
				longt+=16
				length+=2
			else:
				length+=1
				longt+=8
		return(length,longt)

