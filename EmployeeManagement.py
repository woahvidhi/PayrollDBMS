from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
import re
import os
import cx_Oracle
from datetime import datetime
import os.path
expression = ""
 
def press(num):
	global expression
	expression = expression + str(num)
	equation.set(expression)
 
def equalpress():
	try:
		global expression
		total = str(eval(expression))
		equation.set(total)
		expression = ""
	except:
		equation.set(" error ")
		expression = ""

def clear():
	global expression
	expression = ""
	equation.set("")

def deleteData():
	con = None
	cursor = None
	emp = int(v_emp.get())
	try:
		con=cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql = "delete from register where emp_id='%d'"
		args=(emp)
		cursor.execute(sql%args)
		con.commit()
		msg = str(cursor.rowcount)+" record deleted"
		messagebox.showinfo("Success",msg)
		clearDisplay()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()


def clearDisplay():
	stData.delete(1.0,END)
	dis.delete(1.0,END)
	Ent_EmpId.delete(0, END)
	Ent_FName.delete("1.0", "end")
	Ent_LName.delete("1.0", "end")
	Ent_DeptId.delete("1.0", "end")
	Ent_Gender.delete("1.0", "end")
	Ent_Exp.delete("1.0", "end")
	Ent_Age.delete("1.0", "end")
	Ent_Email.delete("1.0", "end")
	Ent_Add.delete("1.0", "end")
	Ent_Phone.delete("1.0", "end")
	Ent_DOB.delete("1.0", "end")
	Ent_DOJ.delete("1.0", "end")
	Ent_PrId.delete("1.0", "end")
	Ent_Month.set('')
	Ent_Year.set('')
	Ent_Total.delete(0, END)
	Ent_Absent.delete(0, END)
	Ent_Salary.delete(0, END)
	Ent_Bonus.delete(0, END)
	Ent_MA.delete(0, END)
	Ent_PT.delete(0, END)
	Ent_CA.delete(0, END)

	Ent_NetSalary.delete("1.0", "end")

def saveData():
	con = None
	cursor = None
	try:
		emp = int(v_emp.get())
		month = Ent_Month.get()
		year = Ent_Year.get()
		month_year = month+" "+year
		net_salary=float(Ent_NetSalary.get("1.0","end-1c"))
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql="insert into payment values('%d','%s','%f')"
		args=(emp,month_year,net_salary)
		cursor.execute(sql%args)
		con.commit()
		msg = str(cursor.rowcount)+" record inserted" 
		messagebox.showinfo("Success",msg)
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
				cursor.close()
		if con is not None:
			con.close()

def updateDisplay():
	dis.delete(1.0,END)
	con = None
	cursor = None
	emp = int(v_emp.get())
	m_data="Month"+"\t\t\t"+"Net Salary"+"\n" 
	sql2="select month_year, net_salary from payment where emp_id='%d'"
	try:
		args2=(emp)
		cursor.execute(sql2%args2)
		data2 = cursor.fetchall()
		print(data2)
		for d in data2:
			m_data = m_data+ d[0] +"\t\t\t"+str(d[1])+'\n'
		dis.insert(INSERT, m_data)	
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

def display():
	con = None
	cursor = None
	emp = int(v_emp.get())
	m_data="Month"+"\t\t\t"+"Net Salary"+"\n" 
	try:
		con = cx_Oracle.connect("system/abc123")
		cursor = con.cursor()
		sql1="select first_name,last_name, dept_id, gender, exp, age, email_id, address, phone_no,DOB,DOJ,proof_id from register where emp_id = '%d'"
		args1=(emp)
		cursor.execute(sql1%args1)
		data1 = cursor.fetchall()
		sql2="select month_year, net_salary from payment where emp_id='%d'"
		args2=(emp)
		cursor.execute(sql2%args2)
		data2 = cursor.fetchall()

		for d in data1:
			Ent_FName.insert(INSERT,d[0])
			Ent_LName.insert(INSERT,d[1])
			Ent_DeptId.insert(INSERT,d[2])
			Ent_Gender.insert(INSERT,d[3])
			Ent_Exp.insert(INSERT,d[4])
			Ent_Age.insert(INSERT,d[5])
			Ent_Email.insert(INSERT,d[6])
			Ent_Add.insert(INSERT,d[7])
			Ent_Phone.insert(INSERT,d[8])
			Ent_DOB.insert(INSERT,d[9])
			Ent_DOJ.insert(INSERT,d[10])
			Ent_PrId.insert(INSERT,d[11])
		for d in data2:
			m_data = m_data+ d[0] +"\t\t\t"+str(d[1])+'\n'
		dis.insert(INSERT, m_data)	
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

def taxCalculation():
	stData.delete(1.0,END)
	display_receipt=[]
	emp = int(v_emp.get())
	full_name = Ent_FName.get("1.0","end-1c") +" " +Ent_LName.get("1.0","end-1c")
	month = Ent_Month.get()
	year = Ent_Year.get()
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	total_days = int(Ent_Total.get())
	absent_days = int(Ent_Absent.get())
	present_days = total_days - absent_days
	total_salary = float(Ent_Salary.get())
	bonus_allowance = float(Ent_Bonus.get())
	conveyance_allowance = float(Ent_CA.get())
	medical_allowance = float(Ent_MA.get())
	tax_professional = float(Ent_PT.get())
	tax_source = 0.1*total_salary
	tax_provident = 0.12*total_salary
	total_tax = tax_provident + tax_source + tax_professional
	gross_salary = total_salary + bonus_allowance + medical_allowance + conveyance_allowance
	net_salary = gross_salary - total_tax
	Ent_NetSalary.insert(INSERT,net_salary)
	display_receipt.append("Employee ID: "+str(emp)+"\t"+dt_string+"\n")
	display_receipt.append("Employee Name: "+full_name+"\n")
	display_receipt.append("Salary Slip of "+str(month)+str(year)+"\n")
	display_receipt.append("--------------------------"+"\n")
	display_receipt.append("Total days: "+str(total_days)+"\n")
	display_receipt.append("Absent days: "+str(absent_days)+"\n")
	display_receipt.append("Present days: "+str(present_days)+"\n")
	display_receipt.append("--------------------------"+"\n")
	display_receipt.append("Salary: "+str(total_salary)+"\n")
	display_receipt.append("Conveyance Amount: "+str(conveyance_allowance)+"\n")
	display_receipt.append("Medical Amount: "+str(medical_allowance) +"\n")
	display_receipt.append("Bonus Amount: "+str(bonus_allowance)+"\n")
	display_receipt.append("Total Gross Salary: "+str(gross_salary)+"\n")
	display_receipt.append("--------------------------"+"\n")
	display_receipt.append("Professional Tax"+str(tax_professional)+"\n")
	display_receipt.append("Source Tax (10% of Salary): "+str(tax_source)+"\n")
	display_receipt.append("Provident Funds (12% of Salary): "+str(tax_provident)+"\n")
	display_receipt.append("Total Deduction: "+str(total_tax)+"\n")
	display_receipt.append("--------------------------"+"\n")
	display_receipt.append("Net Salary: "+str(net_salary)+"\n")
	for i in range(len(display_receipt)):
		stData.insert(INSERT, display_receipt[i])

def downloadFile():
	emp = str(v_emp.get())
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y")
	file_name = emp+"-"+dt_string+".txt"
	f = None
	try:
		f = open(file_name, "w")
		data = str(stData.get("1.0",END))
		f.write(data)
		messagebox.showinfo("Success",file_name+" created")
	except Exception as e:
		messagebox.showerror("Failure",e)
	finally:
		if f is not None:
			f.close()

def LogOff():
	window.destroy()
	os.system('python LoginScreen.py')

window = Tk()
window.title("Employee Management")
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))
window.config(background="#222831")
title = Label(window, text="Employee Management System", font=('Times new roman',30,"bold"), bg="#222831", fg="#f0ece2")
title.pack()

#---------------------------------Frame_informartion----------------------------------------
Frame_information = Frame(window, highlightthickness=1, relief=RIDGE, bg="#393e46")
Frame_information.place(x=20, y=70, width=700, height=400)
Frame_information.config(highlightbackground = "#313131", highlightcolor= "#313131")
Frame_information_title = Label(Frame_information,text="Employee Information", font=('Times new roman',20,"bold"), bg="#393e46", fg="#f0ece2")
Frame_information_title.place(x=5, y=10)
separator1 = ttk.Separator(Frame_information, orient='horizontal')
separator1.place(x=280, y=27, width=400, height=2)

#---------- Column 1 ----------------------
Lbl_EmpId = Label(Frame_information,text="Employee ID", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_FName = Label(Frame_information,text="First Name", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Gender = Label(Frame_information,text="Gender", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Exp = Label(Frame_information,text="Experience", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Age = Label(Frame_information,text="Age", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Email = Label(Frame_information,text="Email ID", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Add = Label(Frame_information,text="Address", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")

Lbl_EmpId.place(x=20, y=70)
Lbl_FName.place(x=20, y=110)
Lbl_Gender.place(x=20, y=150)
Lbl_Exp.place(x=20, y=190)
Lbl_Age.place(x=20, y=230)
Lbl_Email.place(x=20, y=270)
Lbl_Add.place(x=20, y=310)

#---------- Column 2 ----------------------
v_emp = StringVar()
Ent_EmpId = Entry(Frame_information, textvariable=v_emp, font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0)
Ent_FName = Text(Frame_information, height = 1, width = 20, font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0)
Ent_Gender = Text(Frame_information, height = 1, width = 20, font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0)
Ent_Exp = Text(Frame_information, height = 1, width = 20, font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0)
Ent_Age = Text(Frame_information, height = 1, width = 20, font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0)
Ent_Email = Text(Frame_information, height = 1, width = 20, font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0)

Ent_EmpId.place(x=150, y=75)
Ent_FName.place(x=150, y=115)
Ent_Gender.place(x=150,y=155)
Ent_Exp.place(x=150, y=195)
Ent_Age.place(x=150, y=235)
Ent_Email.place(x=150, y=275)

Ent_Add = Text(Frame_information, height = 1, width = 20, bg="#222831",font=('Times new roman',15), fg="#f0ece2",bd=0)
Ent_Add.place(x=150, y=315)

btn_search = Button(Frame_information, command=display, text="Search", font=('Times new roman',12,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=10)
btn_search.place(x=375, y=60)
#---------- Column 3----------------------

Lbl_DeptId = Label(Frame_information,text="Dept ID", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_LName = Label(Frame_information,text="Last Name", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Phone = Label(Frame_information,text="Phone No.", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_DOB = Label(Frame_information,text="D.O.B.", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_DOJ = Label(Frame_information,text="D.O.J", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_PrId = Label(Frame_information,text="Proof ID", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")

Lbl_DeptId.place(x=375, y=110)
Lbl_LName.place(x=375, y=150)
Lbl_Phone.place(x=374,y=190)
Lbl_DOB.place(x=375, y=230)
Lbl_DOJ.place(x=375, y=270)
Lbl_PrId.place(x=375, y=310)

#---------- Column 4  ----------------------
Ent_DeptId = Text(Frame_information, height = 1, width = 20, bg="#222831",font=('Times new roman',15), fg="#f0ece2",bd=0)
Ent_LName = Text(Frame_information, height = 1, width = 20, bg="#222831",font=('Times new roman',15), fg="#f0ece2",bd=0)
Ent_Phone = Text(Frame_information, height = 1, width = 20, bg="#222831",font=('Times new roman',15), fg="#f0ece2",bd=0)
Ent_DOB = Text(Frame_information, height = 1, width = 20, bg="#222831",font=('Times new roman',15), fg="#f0ece2",bd=0)
Ent_DOJ = Text(Frame_information, height = 1, width = 20, bg="#222831",font=('Times new roman',15), fg="#f0ece2",bd=0)
Ent_PrId = Text(Frame_information, height = 1, width = 20, bg="#222831",font=('Times new roman',15), fg="#f0ece2",bd=0)


Ent_DeptId.place(x=480,y=115)
Ent_LName.place(x=480,y=155)
Ent_Phone.place(x=480,y=195)
Ent_DOB.place(x=480, y=235)
Ent_DOJ.place(x=480, y=275)
Ent_PrId.place(x=480,y=315)

#---------------------------------Frame_display-----------------------------------------------

Frame_display = Frame(window, highlightthickness=1, relief=RIDGE, bg="#393e46")
Frame_display.place(x=20, y=500, width=700, height=280)
Frame_display.config(highlightbackground = "#313131", highlightcolor= "#313131")
Frame_display_title = Label(Frame_display,text="Employee Status", font=('Times new roman',20,"bold"), bg="#393e46", fg="#f0ece2")
Frame_display_title.place(x=5, y=10)
separator3 = ttk.Separator(Frame_display, orient='horizontal')
separator3.place(x=215, y=27, width=465, height=2)
dis= scrolledtext.ScrolledText(Frame_display, width=60, height=9, font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0)
dis.place(x=20, y=50)





#---------------------------------Frame_Work---------------------------------------------

Frame_work= Frame(window, highlightthickness=1, relief=RIDGE, bg="#393e46")
Frame_work.place(x=750, y=70, width=750, height=400)
Frame_work.config(highlightbackground = "#313131", highlightcolor= "#313131")
Frame_work_title = Label(Frame_work,text="Work Information", font=('Times new roman',20,"bold"), bg="#393e46", fg="#f0ece2")
Frame_work_title.place(x=5, y=10)
separator4 = ttk.Separator(Frame_work, orient='horizontal')
separator4.place(x=240, y=27, width=490, height=2)

#row 1
Lbl_Month = Label(Frame_work,text="Month", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Year = Label(Frame_work,text="Year", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Salary = Label(Frame_work,text="Salary", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2", width=4)

Lbl_Month.place(x=20, y=70)
Lbl_Year.place(x=270, y=70)
Lbl_Salary.place(x=500, y=70)

mon = StringVar()
Ent_Month = ttk.Combobox(Frame_work, width=20, textvariable=mon)
Ent_Month['values'] = (	"January", "February", "March",
						"March", "April", "May", "June",
						"July", "August", "October",
						"November","December")
Ent_Month.place(x=95,y=75)

yr=[]
for i in range (1950,2022):
	yr.append(str(i))
yr.reverse()
year = StringVar()
Ent_Year = ttk.Combobox(Frame_work, width=20, textvariable=year)
Ent_Year['values'] = tuple(yr)
Ent_Year.place(x=320,y=75)

Ent_Salary = Entry(Frame_work,font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0, width=17)
Ent_Salary.place(x=560, y=75)

#row 2

Lbl_Total = Label(Frame_work,text="Total Days", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_Absent = Label(Frame_work,text="Absent", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_MA = Label(Frame_work,text="Medical", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")

Lbl_Total.place(x=20, y=110)
Lbl_Absent.place(x=270, y=110)
Lbl_MA.place(x=500, y=110)

Ent_Total = Entry(Frame_work,font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0, width=11)
Ent_Absent = Entry(Frame_work,font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0, width=12)
Ent_MA = Entry(Frame_work,font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0, width=15)

Ent_Total.place(x=125,y=115)
Ent_Absent.place(x=340,y=115)
Ent_MA.place(x=580,y=115)

#row 2

Lbl_Bonus = Label(Frame_work,text="Bonus", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_CA = Label(Frame_work,text="Conveyance", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_PT = Label(Frame_work,text="PT", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")

Lbl_Bonus.place(x=20, y=150)
Lbl_CA.place(x=270, y=150)
Lbl_PT.place(x=500, y=150)

Ent_Bonus = Entry(Frame_work,font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0, width=15)
Ent_CA = Entry(Frame_work,font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0, width=8)
Ent_PT = Entry(Frame_work,font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0, width=19)

Ent_Bonus.place(x=85,y=155)
Ent_CA.place(x=380,y=155)
Ent_PT.place(x=540,y=155)

#row 3

Lbl_NetSalary = Label(Frame_work,text="Net Salary", font=('Times new roman',15,"bold"), bg="#393e46", fg="#f0ece2")
Lbl_NetSalary.place(x=20, y=190)

Ent_NetSalary = Text(Frame_work,font=('Times new roman',15), bg="#222831", fg="#f0ece2", bd=0, height=1, width=11)
Ent_NetSalary.place(x=125,y=195)

Btn_Clear = Button(Frame_work, text='Clear', command =clearDisplay, font=('Times new roman',15,"bold"), bg="#d72323", fg="#f0ece2", bd=5, height=1, width=10)
Btn_Clear.place(x=310,y=195)

Btn_Save = Button(Frame_work,command=saveData, text='Save', font=('Times new roman',15,"bold"), bg="#d72323", fg="#f0ece2", bd=5, height=1, width=10)
Btn_Save.place(x=550,y=195)

#row 4

Btn_Calculate = Button(Frame_work, command=taxCalculation, text='Calculate', font=('Times new roman',15,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=10)
Btn_Calculate.place(x=80,y=250)

Btn_Update = Button(Frame_work, text='Update',command=updateDisplay, font=('Times new roman',15,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=10)
Btn_Update.place(x=310,y=250)

Btn_Delete = Button(Frame_work,command=deleteData, text='Delete', font=('Times new roman',15,"bold"), bg="#84142d", fg="#f0ece2", bd=5, height=1, width=10)
Btn_Delete.place(x=550,y=250)

#row 5
Btn_Download = Button(Frame_work, text='Download Receipt',command=downloadFile, font=('Times new roman',15,"bold"), bg="#44000d", fg="#f0ece2", bd=5, height=1, width=20)
Btn_Download.place(x=50,y=325)

Btn_LogOut = Button(Frame_work, text='Log Out', font=('Times new roman',15,"bold"), bg="#44000d", fg="#f0ece2", bd=5, height=1, width=20, command=LogOff)
Btn_LogOut.place(x=450,y=325)


#------------------------------Frame_functions----------------------------------------------
Frame_functions = Frame(window, highlightthickness=1, relief=RIDGE, bg="#393e46")
Frame_functions.place(x=750, y=500, width=750, height=280)
Frame_functions.config(highlightbackground = "#313131", highlightcolor= "#313131")
Frame_functions_title = Label(Frame_functions,text="Receipt", font=('Times new roman',20,"bold"), bg="#393e46", fg="#f0ece2")
Frame_functions_title.place(x=480, y=10)
separator3 = ttk.Separator(Frame_functions, orient='vertical')
separator3.place(x=345, y=27, width=2, height=224)

#Calculator
Frame_cal = Frame(Frame_functions, highlightthickness=1, relief=RIDGE, bg="#313131")
Frame_cal.place(x=20, y=40, width=310, height=200)
equation = StringVar()
expression_field = Entry(Frame_cal, textvariable=equation)
expression_field.grid(row=1, columnspan=3,ipadx=57,ipady=10)
Decimal= Button(Frame_cal, text='.', command=lambda: press('.'), height=2, width=10)
Decimal.grid(row=1, column=3)
button1 = Button(Frame_cal, text=' 1 ',command=lambda: press(1), height=2, width=10)
button1.grid(row=2, column=0)
button2 = Button(Frame_cal, text=' 2 ',command=lambda: press(2), height=2, width=10)
button2.grid(row=2, column=1)
button3 = Button(Frame_cal, text=' 3 ',command=lambda: press(3), height=2, width=10)
button3.grid(row=2, column=2)
button4 = Button(Frame_cal, text=' 4 ',command=lambda: press(4), height=2, width=10)
button4.grid(row=3, column=0)
button5 = Button(Frame_cal, text=' 5 ',command=lambda: press(5), height=2, width=10)
button5.grid(row=3, column=1)
button6 = Button(Frame_cal, text=' 6 ',command=lambda: press(6), height=2, width=10)
button6.grid(row=3, column=2)
button7 = Button(Frame_cal, text=' 7 ',command=lambda: press(7), height=2, width=10)
button7.grid(row=4, column=0)
button8 = Button(Frame_cal, text=' 8 ',command=lambda: press(8), height=2, width=10)
button8.grid(row=4, column=1)
button9 = Button(Frame_cal, text=' 9 ',command=lambda: press(9), height=2, width=10)
button9.grid(row=4, column=2)
button0 = Button(Frame_cal, text=' 0 ',command=lambda: press(0), height=2, width=10)
button0.grid(row=5, column=0)
plus = Button(Frame_cal, text=' + ', command=lambda: press("+"), height=2, width=10)
plus.grid(row=2, column=3)
minus = Button(Frame_cal, text=' - ',command=lambda: press("-"), height=2, width=10)
minus.grid(row=3, column=3)
multiply = Button(Frame_cal, text=' * ',command=lambda: press("*"), height=2, width=10)
multiply.grid(row=4, column=3)
divide = Button(Frame_cal, text=' / ', command=lambda: press("/"), height=2, width=10)
divide.grid(row=5, column=3)
equal = Button(Frame_cal, text=' = ', command=equalpress, height=2, width=10)
equal.grid(row=5, column=2)
clear = Button(Frame_cal, text='Clear',command=clear, height=2, width=10)
clear.grid(row=5, column=1)
#Receipt
stData = scrolledtext.ScrolledText(Frame_functions, width=35, height=9, font=('Times new roman',15), bg="#222831", fg="#f0ece2",bd=0)
stData.place(x=355, y=50)



window.mainloop()