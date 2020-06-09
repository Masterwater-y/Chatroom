from tkinter import *

class Tips(Toplevel):#是顶级窗口的子类

	def __init__(self,wdgt,msg):
		self.wdgt=wdgt
		self.parent=self.wdgt.master#绑定控件的父亲
		Toplevel.__init__(self,self.parent, padx=1, pady=1)#初始化父类
		self.overrideredirect(True)#去除标题框
		self.withdraw()#初始化不出现
		self.msgvar=StringVar()
		self.msgvar.set(msg)
		Message(self,textvariable=self.msgvar,bg='#FFFFDD',aspect=1000).grid()#标签
		self.wdgt.bind( '<Enter>', self.show, '+' )#绑定鼠标悬浮事件
		self.wdgt.bind( '<Leave>', self.hide, '+' )


	def show(self,event):
		self.geometry( '+%i+%i' % ( event.x_root+10, event.y_root+10 ) )#在鼠标附近出现
		self.deiconify()#显示被隐藏的窗口
	def hide(self,event):
		self.withdraw()
