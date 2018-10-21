from tkinter import *

top = Tk()

frame = Frame(top)
frame.pack(side=LEFT)
frame2 = Frame(top)
frame2.pack(side=LEFT, expand=1)

b1=Button(frame, text="one")
b2=Button(frame, text="two")
b3=Button(frame, text="three")
b4=Button(frame, text="four")

b1.grid(row=0,column=0)
b2.grid(row=0,column=1)
b3.grid(row=1,column=0)
b4.grid(row=1,column=1)

top.mainloop()