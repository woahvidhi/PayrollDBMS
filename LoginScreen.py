from PIL import Image, ImageTk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re
import os
import cx_Oracle

def validateUser(user_id, pwd):
	con = None
	cursor = None
	details=[]
	try:
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql="select emp_id, password from login"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			details.append((d[0],d[1]))

	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

	for d in details:
		if(user_id==str(d[0]) and pwd==str(d[1])):
			return 1
		else:
			return 3

def validateAllFields():
	if id_var.get()=="":
		messagebox.showerror('Invalid Data', 'Please enter EmpID to proceed')
	elif pwd_var.get()=="":
		messagebox.showerror('Invalid Data', 'Please enter the password')
	else:
		status= validateUser(id_var.get(), pwd_var.get())
		if status == 1:	
			messagebox.showinfo('Success', 'Log in Successful!')
			window.destroy()
			os.system('python EmployeeManagement.py')
		elif status == 2:
			messagebox.showwarning('Error', 'Access Denied')
		else:
			messagebox.showerror('Error', 'Please Try Again')
			clearAllFields()

def clearAllFields():
	id_var.set("")
	pwd_var.set("")

def callRegistration():
	window.destroy()
	os.system('python Registration.py')

def callForgot():
	window.destroy()
	os.system('python ForgotPassword.py')

window= Tk()
window.title("Login Screen")
window.geometry('550x550+450+150')
window.config(background="#222831")
title = Label(window, text="Payroll Login", font=('Times new roman',20,"bold"), bg="#222831", fg="#f0ece2")
title.pack(pady=20)


load= Image.open ("C:\demo\Python\Project\pay_roll\piggy.png").resize((200,200))
render = ImageTk.PhotoImage(load)
Label(window, image = render, bg="#222831").pack(side = TOP)

id_var= StringVar()
pwd_var= StringVar()

lb_id= Label(window,text="Employee ID", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_id.place(x=80,y=300)
entry_id= Entry(window, textvariable =id_var, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_id.place(x=240,y=300)

lb_pwd= Label(window,text="Password", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_pwd.place(x=80,y=350)
entry_pwd= Entry(window, show="*", textvariable =pwd_var, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_pwd.place(x=240,y=350)

btn_login= Button(window, text='Login', font=('Times new roman',15,"bold"), bg="#d72323", fg="#f0ece2", bd=5, height=1, width=10, command=validateAllFields).place(x=50, y=415)
btn_clear= Button(window, text='Clear', font=('Times new roman',15,"bold"), bg="#d72323", fg="#f0ece2", bd=5, height=1, width=10, command=clearAllFields).place(x=200, y=415)
btn_newuser= Button(window, text='New User', font=('Times new roman',15,"bold"), bg="#d72323", fg="#f0ece2", bd=5, height=1, width=10, command=callRegistration).place(x=350,y=415)
btn_forgot= Button(window, text='Forgot Password?', font=('Times new roman',15,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=15, command=callForgot).place(x=175,y=475)
window.mainloop()
