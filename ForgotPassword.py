from PIL import Image, ImageTk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import os
import cx_Oracle

def validateUser(user_id, proof):
	con = None
	cursor = None
	details=[]
	password = "0"
	try:
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql="select emp_id, password, proof_id from login"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			details.append((d[0],d[1],d[2]))
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

	for d in details:
		if d[0]==int(user_id) and d[2]==int(proof):
			password = d[1]
	return password

def validateAllFields():
	if id_var.get()=="":
		messagebox.showerror('Invalid Data', 'Please enter EmpID to proceed')
	elif proof_var.get()=="":
		messagebox.showerror('Invalid Data', 'Please enter the proof ID')
	else:
		status= validateUser(id_var.get(), proof_var.get())
		if status.isalpha():	
			messagebox.showinfo('Success', 'Your password is '+status)
		else:
			messagebox.showerror('Error', 'Please Try Again')
			clearAllFields()

def clearAllFields():
	id_var.set("")
	proof_var.set("")

def callRegistration():
	window.destroy()
	os.system('python Registration.py')
def callLogin():
	window.destroy()
	os.system('python LoginScreen.py')

window= Tk()
window.title("Forgot Password")
window.geometry('550x550+450+150')
window.config(background="#222831")
title = Label(window, text="Forgot Password", font=('Times new roman',20,"bold"), bg="#222831", fg="#f0ece2")
title.pack(pady=20)


load= Image.open ("C:\demo\Python\Project\pay_roll\pandu.png").resize((300,250))
render = ImageTk.PhotoImage(load)
Label(window, image = render, bg="#222831").pack(side = TOP)

id_var= StringVar()
proof_var= StringVar()

lb_id= Label(window,text="Employee ID", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_id.place(x=80,y=300)
entry_id= Entry(window, textvariable =id_var, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_id.place(x=240,y=300)

lb_proof= Label(window,text="Proof ID", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_proof.place(x=80,y=350)
entry_proof= Entry(window, textvariable =proof_var, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_proof.place(x=240,y=350)

btn_forgot= Button(window, text='Get Password', font=('Times new roman',15,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=15,command=validateAllFields).place(x=175,y=415)
btn_login= Button(window, text='Login', font=('Times new roman',15,"bold"), bg="#d72323", fg="#f0ece2", bd=5, height=1, width=10, command=callLogin).place(x=50, y=475)
btn_clear= Button(window, text='Clear', font=('Times new roman',15,"bold"), bg="#d72323", fg="#f0ece2", bd=5, height=1, width=10, command=clearAllFields).place(x=200, y=475)
btn_newuser= Button(window, text='New User', font=('Times new roman',15,"bold"), bg="#d72323", fg="#f0ece2", bd=5, height=1, width=10, command=callRegistration).place(x=350,y=475)
window.mainloop()