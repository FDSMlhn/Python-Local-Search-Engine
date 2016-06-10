import tkinter as tk
from PIL import Image,ImageTk


class simpleapp_tk(tk.Tk):
	"""docstring for simpleapp_tk"""
	def __init__(self, parent):
		tk.Tk.__init__(self,parent)
		self.parent=parent
		self.initialize()

	def initialize(self):
		self.grid()
		# labelframe = tk.LabelFrame(self,text="Greatest local search engine ever")
		# labelframe.grid(column=0,row=0)
		im = Image.open('/Users/Dreamland/Desktop/学校的各种杂物/2016下学期课/领域数据学/car_spiders.png')
		nw_im = im.resize((300,200))
		nw_im.show()
		spider = ImageTk.PhotoImage(nw_im)
		self.entryVariable=tk.StringVar()
		self.entry = tk.Entry(self,textvariable=self.entryVariable)
		self.entry.grid(column=0,row=0,sticky='EW')
		self.entry.bind("<Return>",self.PressEnter) #only when enter clicked in the text field!
		self.entryVariable.set("Enter text here.")

		self.button = tk.Button(self,text=u"Search",command=self.ButtonClick)
		self.button.grid(column=1,row=0)

		self.labelVariable=tk.StringVar()
		label = tk.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="grey")
		label.grid(column=0,row=1,columnspan=2,sticky='EW')
		self.labelVariable.set("Hello!")

		label_pic = tk.Label(self,image=spider,anchor='s')
		label_pic.img=spider
		#label_pic.pack(side = "bottom", fill = "both", expand = "yes")
		#label_pic.place(x=1,y=1,width=nw_im.size[0],height=nw_im.size[1])
		label_pic.grid(column=0,row=2,rowspan=5,columnspan=10)
		# label_pic.pack()

		# self.grid_rowconfigure(2,weight=1)
		self.entry.focus_set()
		self.entry.selection_range(0,tk.END)
		self.grid_columnconfigure(0,weight=1)

	def ButtonClick(self):
		self.labelVariable.set(self.entryVariable.get()+"You clicked the button!")
		self.entry.focus_set()
		self.entry.selection_range(0,tk.END)

	def PressEnter(self,event):
		self.labelVariable.set(self.entryVariable.get()+"You pressed enter!")
		self.entry.focus_set()
		self.entry.selection_range(0,tk.END)

if __name__ == "__main__":
	# pic=Image.open('/Users/Dreamland/Desktop/学校的各种杂物/2016下学期课/领域数据学/car_spiders.png')
	# pic.show()
	app = simpleapp_tk(None)
	app.title('my application')
	app.mainloop()

