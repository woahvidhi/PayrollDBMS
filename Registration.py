from tkcalendar import DateEntry
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
import os
import cx_Oracle

def insertData():
	Valid = validateAllFields()
	if False in Valid:
		messagebox.showerror('Error', 'Registration Failed')
	else:
		con = None
		cursor = None
		try:
			empid = int(v_empid.get())
			fname = v_fName.get()
			lname = v_lname.get()
			dpt = int(v_dpt.get())
			pwd = v_pwd.get()
			dob = str(Cal_DOB.get_date())
			doj = str(Cal_DOJ.get_date())
			phone = int(v_phoneNo.get())
			age = int(v_age.get())
			exp = v_exp.get()
			proof = int(v_proof.get())
			email = v_emailId.get()
			gender = v_gender.get()
			des = v_des.get()
			add = v_add.get()
			country=v_country.get()
			
			con = cx_Oracle.connect("system/abc123")
			cursor = con.cursor()
			sql1="insert into register values('%d','%s','%s','%d','%s','%s','%s','%d','%d','%s','%d','%s','%s','%s','%s','%s')"
			args1=(empid,fname,lname,dpt,pwd,dob,doj,phone,age,exp,proof,email,gender,des,add,country)
			cursor.execute(sql1%args1)
			con.commit()
			msg = str(cursor.rowcount)+" record inserted" 
			messagebox.showinfo("Success",msg)
		except cx_Oracle.DatabaseError as e:
			con.rollback()
			print(e)
			messagebox.showerror("Failure",e)
		finally:
			if cursor is not None:
				cursor.close()
			if con is not None:
				con.close()

def validate_phoneno(user_phone):
	if user_phone.isdigit() and len(str(user_phone))==10:
		return True
	else:
		messagebox.showerror('Error', 'Only 10 digits are allowed')
		return False

def isValidEmail(user_email):
	if len(user_email) > 7:
		if re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', user_email)!=None:
			return True
		else:
			messagebox.showerror('Error', 'This is not a valid email')
			return False
	else:
		messagebox.showerror('Error', 'This is not a valid email')
		return False

def validateAllFields():
	Valid=set()
	if v_empid.get()=="":
		messagebox.showerror('Error', 'Please enter employee ID to proceed')
	elif v_dpt.get()=="":
		messagebox.showerror('Error', 'Please enter department ID to proceed')
	elif v_fName.get()=="":
		messagebox.showerror('Error', 'Please enter first name to proceed')
	elif v_lname.get()=="":
		messagebox.showerror('Error', 'Please enter last name to proceed')
	elif v_pwd.get()=="":
		messagebox.showerror('Error', 'Please enter the password')
	elif v_repwd.get()=="":
		messagebox.showerror('Error', 'Please enter the Re-password')
	elif v_phoneNo.get()=="":
		messagebox.showerror('Error', 'Please enter 10 digit contact no')
	elif v_age.get()=="":
		messagebox.showerror('Error', 'Please enter age')
	elif v_emailId.get()=="":
		messagebox.showerror('Error', 'Please enter email')
	elif v_exp.get()=="":
		messagebox.showerror('Error', 'Please enter experience')
	elif v_gender.get()=="":
		messagebox.showerror('Error', 'Please select gender')
	elif v_proof.get()=="":
		messagebox.showerror('Error', 'Please enter proof ID')
	elif v_country.get()=="" or v_country.get()=="Select Your Country":
		messagebox.showerror('Error', 'Please select country')
	elif entry_add.get()=="":
		messagebox.showerror('Error', 'Please enter address')
	elif v_des=="":
		messagebox.showerror('Error', 'Please select Designation to proceed')
	else:
		Valid.add(True)
	if v_emailId.get()!="":
		Valid.add(isValidEmail(v_emailId.get()))
	if v_phoneNo.get()!="":
		Valid.add(validate_phoneno(v_phoneNo.get()))
	if v_empid.get().isdigit() and v_dpt.get().isdigit() and v_age.get().isdigit() and v_proof.get().isdigit():
		Valid.add(True)
	return(Valid)

def clearAllFields():
	v_empid.set("")
	v_dpt.set("")
	v_lname.set("")
	v_repwd.set("")
	v_fName.set("")
	v_age.set("")
	v_exp.set("")
	v_gender.set("")
	v_proof.set("")
	v_des.set("")
	v_add.set("")
	v_pwd.set("")
	v_phoneNo.set("")
	v_emailId.set("")

def callNewScreen():
	window.destroy()
	os.system('python LoginScreen.py')

#---------------------------------------------------
window= Tk()
window.title("Registration")
window.geometry('800x550+450+150')
window.config(background="#222831")
title = Label(window, text="Registration Page", font=('Times new roman',20,"bold"), bg="#222831", fg="#f0ece2")
title.pack(pady=20)


#col1
v_empid=StringVar()
v_fName= StringVar()
v_pwd=StringVar()
v_phoneNo= StringVar()
v_emailId= StringVar()
v_gender=StringVar()
v_country=StringVar()
v_des= StringVar()

lb_empid= Label(window, text="Employee ID", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_fname= Label(window, text="First Name", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_pwd= Label(window, text="Password",font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_dob= Label(window, text="D.O.B.", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_phoneno=Label(window, text="Phone No.", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_email= Label(window, text="Email ID",font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")

lb_empid.place(x=50, y=90)
lb_fname.place(x=50, y=130)
lb_pwd.place(x=50, y=170)
lb_dob.place(x=50, y=210)
lb_phoneno.place(x=50, y=250)
lb_email.place(x=50, y=290)

entry_empid= Entry(window, textvariable= v_empid, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_fname= Entry(window, textvariable= v_fName, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_pwd=Entry(window, show="*", textvariable= v_pwd, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_phoneno= Entry(window, textvariable= v_phoneNo, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_email= Entry(window, textvariable= v_emailId, font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)

entry_empid.place(x=170, y=90)
entry_fname.place(x=170, y=130)
entry_pwd.place(x=170, y=170)
entry_phoneno.place(x=170, y=250)
entry_email.place(x=170, y=290)

Cal_DOB = DateEntry(window, date_pattern='y-mm-dd', width=30, year=2000, month=1, day=1, bg='#222831', fg="#f0ece2")
Cal_DOB.place(x=170, y=210)

lb_gender= Label(window, text="Gender", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_gender.place(x=50, y=330)
gender= ttk.Combobox(window, width=30, textvariable=v_gender)
gender['values'] = ("Female", "Male", "Other", "Rather Not Say")
gender.place(x=170, y=330)
gender.current()

lb_des= Label(window, text="Designation", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_des.place(x=50, y=370)
DesName= ttk.Combobox(window, width=30, textvariable=v_des)
DesName['values'] = ("Intern","Team Assistant","Team Leader", "Project Assistant", "Project Manager")
DesName.place(x=170, y=370)
DesName.current()

lb_country= Label(window, text="Country", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_country.place(x=50, y=410)
list_country= ['India', 'Canada', 'UK','Germany','Spain'];
droplist= OptionMenu(window, v_country, *list_country)
droplist.config(width=18, height=1, font=('Times new roman',14), bg="#393e46", fg="#f0ece2", bd=0)
v_country.set('Select Your Country')
droplist.place(x=170, y=410)

#row2

lb_deptid= Label(window, text="Dept ID", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_lname= Label(window, text="Last Name", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_repwd= Label(window, text="Re-Password",font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_doj= Label(window, text="D.O.J.", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_age=Label(window, text="Age", font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_exp= Label(window, text="Experience",font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_proof= Label(window, text="Proof ID",font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")
lb_add = Label(window, text="Address",font=('Times new roman',15,"bold"), bg="#222831", fg="#f0ece2")

lb_deptid.place(x=425, y=90)
lb_lname.place(x=425, y=130)
lb_repwd.place(x=425, y=170)
lb_doj.place(x=425, y=210)
lb_age.place(x=425, y=250)
lb_exp.place(x=425, y=290)
lb_proof.place(x=425, y=330)
lb_add.place(x=425, y=370)

v_dpt = StringVar()
v_lname = StringVar()
v_repwd = StringVar()
v_age = StringVar()
v_exp = StringVar()
v_proof = StringVar()
v_add= StringVar()

entry_deptid = Entry(window, textvariable=v_dpt,font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_lname = Entry(window, textvariable=v_lname,font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_repwd = Entry(window, show="*", textvariable=v_repwd,font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_age = Entry(window, textvariable=v_age,font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_exp = Entry(window, textvariable=v_exp,font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_proof = Entry(window, textvariable=v_proof,font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)
entry_add = Entry(window,textvariable=v_add,font=('Times new roman',15), bg="#393e46", fg="#f0ece2",bd=0)

entry_deptid.place(x=560,y=90)
entry_lname.place(x=560,y=130)
entry_repwd.place(x=560,y=170)
entry_age.place(x=560,y=250)
entry_exp.place(x=560,y=290)
entry_proof.place(x=560,y=330)
entry_add.place(x=560,y=370)

Cal_DOJ = DateEntry(window, width=30, date_pattern='y-mm-dd', year=2021, month=1, day=1, bg='#222831', fg="#f0ece2")
Cal_DOJ.place(x=560, y=210)

btn_register= Button(window, text="Register", command= insertData, font=('Times new roman',15,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=10).place(x=200, y=475)
btn_clear= Button(window, text="Clear", command= clearAllFields, font=('Times new roman',15,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=10).place(x=350, y=475)
btn_existinguser= Button(window, text="Existing user", command= callNewScreen, font=('Times new roman',15,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=10).place(x=500, y=475)

window.mainloop()

