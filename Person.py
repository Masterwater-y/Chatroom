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
		self.curtag=curtag
		self.send_icon_func=send_icon_func
		self.ask_inform_func=ask_inform_func
		self.get_inform_func=get_inform_func
		self.send_inform_func=send_inform_func
		self.sex_box=None
		self.age_box=None
		Toplevel.__init__(self,self.parent, padx=1, pady=1,bg='white')#初始化父类
		#self.overrideredirect(True)#去除标题框
		#self.withdraw()#初始化不出现
		self.geometry('400x600')
		top_img=itk.PhotoImage(file='image/person_top.png')
		self.edit_img=itk.PhotoImage(file='image/edit_top.png')
		self.top_label=Label(self,image=top_img)#标签
		self.top_label.grid(row=0,column=0,sticky=W+E)
		path='data/icon/'+curtag+'b.png'
		icon_img=itk.PhotoImage(file=path)
		icon_canva=Canvas(self,bg='white',width=125,height=125,borderwidth=0,highlightthickness=0)
		icon_canva.create_image(63,63,image=icon_img)
		print('flag=',flag)
		if flag:
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
		self.ask_inform_func(self.curtag)
		time.sleep(0.1)#给时间下载个人信息
		self.inform=self.get_inform_func()
		print(self.inform)
		for i in range(5):
			self.content.append(StringVar())
			self.content[i].set(str(self.inform[i]))
			length,longt=self.getlen(self.inform[i])
			print(length,' ',longt)
			self.entrys.append(Entry(self.bg_canva,textvariable=self.content[i],font=('宋体',-16),highlightthickness=0,borderwidth=0,width=length,bg='white',state=DISABLED))
			self.entrys[i].place(x=370-longt,y=25+50*i,height=25)
		self.entrys[0].configure(state=DISABLED)

		save_btn_img=itk.PhotoImage(file='image/save_btn.png')
		edit_btn_img=itk.PhotoImage(file='image/edit_btn.png')
		self.save_btn=Button(self,image=save_btn_img,command=self.bind_save,borderwidth=0,highlightthickness=0)
		self.edit_btn=Button(self,image=edit_btn_img,command=self.edit,borderwidth=0,highlightthickness=0)
		self.edit_btn.place(x=338,y=14)
		#self.bind_save()
		#self.content[0].set(self.curtag)
		#id_self.entrys=self.entrys(self.bg_canva,highlightthickness=0,borderwidth=0,width=18).place(x=250,y=30)
		self.mainloop()


	def bind_icon(self,event):
		path=filedialog.askopenfilename()
		if path=='':#没选择图片
			return
		self.send_icon_func(self.curtag,path)

	def edit(self):
		self.top_label.configure(image=self.edit_img)
		self.entrys[1].configure(state=NORMAL)
		self.entrys[3].configure(state=NORMAL)
		self.entrys[2].place_forget()
		self.entrys[4].place_forget()
		self.sex_box=ttk.Combobox(self.bg_canva,width=3,state='readonly')
		self.sex_box['values']=('男','女','其他')
		self.sex_box.current(0)
		self.sex_box.place(x=330,y=125)
		self.age_box=ttk.Combobox(self.bg_canva,width=3,state='readonly')
		self.age_box['values']=('0','1')
		for i in range(2,121,1):
			self.age_box['values']+=(str(i),)
		self.age_box.current(0)
		self.age_box.place(x=330,y=225)
		self.save_btn.place(x=338,y=14)
		self.edit_btn.place_forget()

	def bind_save(self):
		val=[]
		for i in range(1,5,1):
			now=self.content[i].get()
			if i==2:
				now=self.sex_box.get()
			elif i==4:
				now=self.age_box.get()
			val.append(now)
		self.send_inform_func(val)
		messagebox.showinfo('提示','保存成功')
		self.withdraw()

	def getlen(self,content):#-12=12px, 中文12px,英文和符号6px
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

