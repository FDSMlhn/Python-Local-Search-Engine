from tkinter import *
from PIL import Image,ImageTk

app = Tk()
spider = ImageTk.PhotoImage(Image.open('/Users/Dreamland/Desktop/spider.png'))
#spider=PhotoImage('/Users/Dreamland/Desktop/spider.png')

labelframe = LabelFrame(app,text="Greatest local search engine ever")
labelframe.pack(fill="both",expand="yes")
ent =Entry(labelframe)
#C = Canvas(labelframe,height=250,width=300)


var=StringVar()
label = Label(labelframe,textvariable=var,relief="raised")
label2 = Label(labelframe,image=spider)
label2.image=spider
label2.pack()
#label_pic = tkinter.Canvas(labelframe,image=spider)
#label_pic.pack()
#arc = canvas.create_arc(coord,start=0,extent=150)
# Code to add widgets will go here...
#C.pack()
var.set("Please enter your keywords here")
label.pack()
ent.pack(side="right")
app.mainloop()
