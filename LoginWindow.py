from tkinter import *
from PIL import ImageTk as itk
from PIL import Image as Img
class LoginWindow: #类的定义


	def __init__(self,login_func,reg_func,close_func): #__init__ 方法是每个类都必须有的，名字也是固定的，相当于定义全局变量
	                                                   #方法可以理解为函数，但是定义方法一定要有self参数
		self.login_window=None #=Tk()不直接写避免出现多个窗口
		self.login_func=login_func
		self.reg_func=reg_func
		self.key=None
		self.user=None
		self.close_func=close_func



	def show(self):
		self.login_window=Tk()#创建一个窗口
		self.login_window.protocol("WM_DELETE_WINDOW", self.close_func)#protocol wm_delete_window判断关闭窗口事件，保证socket关闭
		
		#新UI
		screen_height=self.login_window.winfo_screenheight()
		screen_width=self.login_window.winfo_screenwidth()#获取当前屏幕的宽度
		self.login_window_width=600 #登录窗口的宽度
		self.login_window_height=375
		self.login_window_px=(screen_width-self.login_window_width)/2 #登录窗口以屏幕左上角为原点的x轴位置 目的是使窗口在屏幕中央出现
		self.login_window_py=(screen_height-self.login_window_height)/2
		self.login_window_size='%dx%d+%d+%d' %(self.login_window_width,self.login_window_height,self.login_window_px,self.login_window_py)
		self.login_window.geometry(self.login_window_size) #定义窗口大小和位置
		frame1=Frame(self.login_window, bg='yellow',width=self.login_window_width,height=self.login_window_height).grid(row=0,column=0)
		top_img=itk.PhotoImage(file='image/bgx.jpg')
		bg_canva=Canvas(frame1,width=self.login_window_width,height=self.login_window_height)
		bg_canva.create_image(300,187,image=top_img)
		icon_img=itk.PhotoImage(file='image/iconx.png')
		bg_canva.create_image(self.login_window_width/2,80,image=icon_img)
		bg_canva.grid(row=0,column=0)
		self.user=StringVar()
		self.key=StringVar()
		self.user.set('请输入用户名')
		btn_img=itk.PhotoImage(file='image/btnx.png')
		reg_img=itk.PhotoImage(file='image/reg.png')
		user_img=itk.PhotoImage(file='image/userx.png')
		key_img=itk.PhotoImage(file='image/keyx.png')
		bg_canva.create_image(172,157,image=user_img)
		bg_canva.create_image(172,220,image=key_img)
		#react=self.login_window.register(self.clean_entry)
		user_entry=Entry(self.login_window,textvariable=self.user,width=30).place(x=211,y=150,height=30)
		key_entry=Entry(self.login_window,textvariable=self.key,show='*',width=30).place(x=211,y=207,height=30)
		self.login_window.bind('<Return>',self.bind_login)
		login_btn=Button(self.login_window,image=btn_img,borderwidth=0,highlightthickness=0,command=self.login_func).place(x=215,y=281)
		register_btn=Button(self.login_window,image=reg_img,borderwidth=0,highlightthickness=0,command=self.reg_func).place(x=431,y=154)
		self.login_window.mainloop()
	#获取用户名和密码
	
	'''def clean_entry(self,content,flag):
		print(flag)
		print("Entry:"+content)
		exit(True)'''

	def bind_login(self,event):
		self.login_func()
	def getinput(self): #返回账号和密码
		return self.user.get(), self.key.get()
	def close(self):
		self.login_window.destroy()