import tkinter as tk
from PIL import Image,ImageTk
import os
from stemming.porter2 import stem
import pandas as pd
import numpy as np
import math
import re
from tkinter import messagebox


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
		spider = ImageTk.PhotoImage(nw_im)
		self.entryVariable=tk.StringVar()
		self.entry = tk.Entry(self,textvariable=self.entryVariable)
		self.entry.grid(column=0,row=0,sticky='EW')
		self.entry.bind("<Return>",self.PressEnter) #only when enter clicked in the text field!
		self.entryVariable.set("Enter text here.")

		self.entryVariable_2=tk.StringVar()
		self.entry_2 = tk.Entry(self,textvariable=self.entryVariable_2)
		self.entry_2.grid(column=0,row=3,sticky='EW')
		self.entry_2.bind("<Return>",self.PressEnter2) #only when enter clicked in the text field!
		self.entryVariable_2.set("Paper you want to go.")

		self.topic=tk.StringVar()
		self.topic.set("Topics")
		self.Menu = tk.Menubutton(self,text=self.topic.get(),underline=0)
		#self.listBox.insert(1,"Python")
		self.Menu.menu = tk.Menu(self.Menu)
		for item in ['U.S.','World','Health','Opinion','Sport','Entertainment','Tech']:
			self.Menu.menu.add_radiobutton(label = item,variable= self.topic,value=item)
		self.Menu['menu'] = self.Menu.menu
		self.Menu.grid(column=0,row=4,sticky="w")

		self.button = tk.Button(self,text=u"Search",command=self.ButtonClick)
		self.button.grid(column=1,row=0)
		self.button1 = tk.Button(self,text=u"Go",command=self.ButtonClick2)
		self.button1.grid(column=1,row=3)
		self.button2=tk.Button(self,text=u"Draw",command=self.ButtonClick3)
		self.button2.grid(column=1,row=4)

		self.button_refresh = tk.Button(self, text="Refresh",command=self.ButtonClick_refresh)
		self.button_refresh.grid(column=1,row=2)
		# self.buttonVariable=tk.StringVar()
		# self.button1 = tk.Button(self,textvariable=self.buttonVariable,command=self.ButtonClick)
		# self.button1.grid(column=0,row=2)
		# self.buttonVariable.set("First you should know")

		self.labelVariable=tk.StringVar()
		label = tk.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="grey")
		label.grid(column=0,row=1,columnspan=1,sticky='EW')
		self.labelVariable.set("Hello!")
		# self.labelVariable1=tk.StringVar()
		# label = tk.Label(self,textvariable=self.labelVariable1,anchor="w",fg="white",bg="grey")
		# label.grid(column=0,row=2.5,columnspan=1,sticky='EW')
		# self.labelVariable2=tk.StringVar()
		# label = tk.Label(self,textvariable=self.labelVariable2,anchor="w",fg="white",bg="grey")
		# label.grid(column=0,row=3,columnspan=1,sticky='EW')
		# self.labelVariable3=tk.StringVar()
		# label = tk.Label(self,textvariable=self.labelVariable3,anchor="w",fg="white",bg="grey")
		# label.grid(column=0,row=4,columnspan=1,sticky='EW')
		# self.labelVariable4=tk.StringVar()
		# label = tk.Label(self,textvariable=self.labelVariable4,anchor="w",fg="white",bg="grey")
		# label.grid(column=0,row=5,columnspan=1,sticky='EW')
		self.T = tk.Text(self, height=5, width=100)
		self.T.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
		self.T.grid(column=0,row=2)
		#T.bind("<Configure>",lambda e: T.configure(width=e.width-10))

		label_pic = tk.Label(self,image=spider,anchor='s')
		label_pic.img=spider
		#label_pic.pack(side = "bottom", fill = "both", expand = "yes")
		#label_pic.place(x=1,y=1,width=nw_im.size[0],height=nw_im.size[1])
		label_pic.grid(column=0,row=5,rowspan=1,columnspan=5,sticky="s")
		# label_pic.pack()
		# self.grid_rowconfigure(2,weight=1)

		self.entry.focus_set()
		self.entry.selection_range(0,tk.END)
		#self.grid_columnconfigure(0,weight=2)
		self.resizable(False,False)

	def ButtonClick(self):
		global Fileaddr
		Fileaddr=[]
		self.T.delete(1.0,tk.END)
		KW_ori =[i.lower() for i in self.entryVariable.get().split()]
		KW=[stem(j) for j in KW_ori]
		TF = [KW.count(i) for i in datasource.columns]
		tool = (np.array(TF) * idf_table.transpose()).transpose()
		result=[]
		for i in range(datasource.shape[0]):
			result.append(float(np.dot(datasource.iloc[i],tool)/(math.sqrt(np.dot(tool.T,tool)) *  math.sqrt(np.dot(datasource.iloc[i],datasource.iloc[i])))))
		num_ad= result
		num_ad = [num_ad[i] + num_ad[i+int(len(num_ad)/2)] for i in range(0,int(len(num_ad)/2))]
		outcome = sorted([x for x in num_ad if x > 0],reverse=True)
		if len(outcome) >=5:
			outcome = outcome[:5]
		outcome = sorted(list(set(outcome)),reverse=True)
		for i in outcome:
			for j in find_all_index(num_ad, i):
				Fileaddr.append(txt_list[j])
				if len(txt_list[j])>100:
					self.T.insert(tk.END,txt_list[j][:100]+"\n")
				else:
					self.T.insert(tk.END,txt_list[j]+"\n")
		self.labelVariable.set("Keyword you entered: " + " ".join(KW_ori))
		self.entry.focus_set()
		self.entry.selection_range(0,tk.END)

	def PressEnter(self,event):
		global Fileaddr
		Fileaddr=[]
		self.T.delete(1.0,tk.END)
		KW_ori =[i.lower() for i in self.entryVariable.get().split()]
		KW=[stem(j) for j in KW_ori]
		TF = [KW.count(i) for i in datasource.columns]
		tool = (np.array(TF) * idf_table.transpose()).transpose()
		result=[]
		for i in range(datasource.shape[0]):
			result.append(float(np.dot(datasource.iloc[i],tool)/(math.sqrt(np.dot(tool.T,tool)) *  math.sqrt(np.dot(datasource.iloc[i],datasource.iloc[i])))))
		num_ad= result
		num_ad = [num_ad[i] + num_ad[i+int(len(num_ad)/2)] for i in range(0,int(len(num_ad)/2))]
		outcome = sorted([x for x in num_ad if x > 0],reverse=True)
		if len(outcome) >=5:
			outcome = outcome[:5]
		outcome = sorted(list(set(outcome)),reverse=True)
		for i in outcome:
			for j in find_all_index(num_ad, i):
				Fileaddr.append(txt_list[j])
				if len(txt_list[j])>100:
					self.T.insert(tk.END,txt_list[j][:100]+"\n")
				else:
					self.T.insert(tk.END,txt_list[j]+"\n")
		self.labelVariable.set("Keyword you entered: " + " ".join(KW_ori))
		self.entry.focus_set()
		self.entry.selection_range(0,tk.END)

	def ButtonClick2(self):
		global Fileaddr
		num = int(self.entryVariable_2.get())
		File= Fileaddr[num-1]
		txtfilepath = os.path.join(file_path,File)
		print(txtfilepath)
		os.system("open \""+txtfilepath+"\"")


	def PressEnter2(self,event):
		global Fileaddr
		num = int(self.entryVariable_2.get())
		File= Fileaddr[num-1]
		txtfilepath = os.path.join(file_path,File)
		print(txtfilepath)
		os.system("open \""+txtfilepath+"\"")

	def ButtonClick3(self):
		KW = self.topic.get()
		os.system("python3.5 Word_cloud.py "+ KW)

	def ButtonClick_refresh(self):
		a = messagebox.askquestion("Alert","Do you really want to update your data? It might take some time here.")
		if a == "yes":
		    messagebox.showinfo("Alert","Do not close the APP")
		    os.system("python3.5 data_scraping.py")
		    os.system("python3.5 directly_word.py")
		    os.system("python3.5 stem_word.py")
		    messagebox.showinfo("Congratulation!","All data has been updated")
		else:
			print("OK")

		
def find_all_index(wordlist,value):
	return [i for i,j in enumerate(wordlist) if j==value]

if __name__ == "__main__":
	#Reading all things into python
	Fileaddr=[]
	PATH = os.getcwd()
	data_path = os.path.join(PATH, "stem_weight_table_wf.csv")
	file_path = PATH + "/dw_field_data"
	txt_list = os.listdir(file_path)[1:]
	datasource = pd.read_csv(data_path)
	idf_table = pd.read_csv(os.path.join(PATH, "stem_idf_table.csv"),header=None)
	app = simpleapp_tk(None)
	app.title('Dive into everything')
	app.mainloop()

