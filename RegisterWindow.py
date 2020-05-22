from tkinter import *
from PIL import ImageTk as itk
from PIL import Image as Img
class RegWindow:

	def __init__(self,reg_back,reg_func):
		self.reg_window=None #=Tk()不直接写避免出现多个窗口
		self.reg_back=reg_back
		self.reg_func=reg_func
		self.key=None
		self.user=None
		self.confirm=None

	def show(self):
		self.reg_window=Tk()#创建一个窗口
		
		#新UI
		screen_height=self.reg_window.winfo_screenheight()
		screen_width=self.reg_window.winfo_screenwidth()#获取当前屏幕的宽度
		self.reg_window_width=600 #登录窗口的宽度
		self.reg_window_height=375
		self.reg_window.title('注册')
		self.reg_window_px=(screen_width-self.reg_window_width)/2 #登录窗口以屏幕左上角为原点的x轴位置 目的是使窗口在屏幕中央出现
		self.reg_window_py=(screen_height-self.reg_window_height)/2
		self.reg_window_size='%dx%d+%d+%d' %(self.reg_window_width,self.reg_window_height,self.reg_window_px,self.reg_window_py)
		self.reg_window.geometry(self.reg_window_size) #定义窗口大小和位置
		frame1=Frame(self.reg_window, bg='yellow',width=self.reg_window_width,height=self.reg_window_height).grid(row=0,column=0)
		bg_img=itk.PhotoImage(file='image/bgx.jpg')
		bg_canva=Canvas(frame1,width=self.reg_window_width,height=self.reg_window_height)
		bg_canva.create_image(300,187,image=bg_img)
		top_img=itk.PhotoImage(file='image/reg_top.png')
		bg_canva.create_image(self.reg_window_width/2,60,image=top_img)
		bg_canva.grid(row=0,column=0)
		self.user=StringVar()
		self.key=StringVar()
		self.confirm=StringVar()
		self.user.set('请分别输入用户名、密码、重复密码')
		reg_img=itk.PhotoImage(file='image/reg_btn.png')
		user_img=itk.PhotoImage(file='image/userx.png')
		key_img=itk.PhotoImage(file='image/keyx.png')
		back_img=itk.PhotoImage(file='image/back_btn.png')
		confirm_img=itk.PhotoImage(file='image/reg_confirm.png')
		bg_canva.create_image(172,124,image=user_img)
		bg_canva.create_image(172,185,image=key_img)
		bg_canva.create_image(172,252,image=confirm_img)
		self.reg_window.bind('<Return>',self.bind_register)
		user_entry=Entry(self.reg_window,textvariable=self.user,width=30).place(x=211,y=115,height=30)
		key_entry=Entry(self.reg_window,textvariable=self.key,show='*',width=30).place(x=211,y=175,height=30)
		confirm_entry=Entry(self.reg_window,textvariable=self.confirm,show='*',width=30).place(x=211,y=235,height=30)
		reg_btn=Button(self.reg_window,image=reg_img,borderwidth=0,highlightthickness=0,command=self.reg_func).place(x=215,y=300)
		back_btn=Button(self.reg_window,image=back_img,borderwidth=0,highlightthickness=0,command=self.reg_back).place(x=15,y=19)
		self.reg_window.mainloop()
	#获取用户名和密码
	def getinput(self):
		return self.user.get(), self.key.get(), self.confirm.get()
	def bind_register(self,event):
		self.reg_func()
	def close(self):
		self.reg_window.destroy()