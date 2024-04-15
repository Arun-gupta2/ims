import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

class EmployeeManagement:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        self.create_database()  # Create the database and the employee table
        self.create_variables()
        self.create_search_frame()
        self.create_title()
        self.create_content()
        self.create_buttons()
        self.create_employee_details_frame()

        self.show_employee_records()

    def create_database(self):
        # Connect to the database
        self.conn = sqlite3.connect('ims.db')
        self.cursor = self.conn.cursor()

        # Create the employee table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee (
                eid INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                contact TEXT,
                dob TEXT,
                doj TEXT,
                pass TEXT,
                utype TEXT,
                address TEXT,
                post TEXT
            )
        ''')

    def create_variables(self):
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_name = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_post = StringVar()

    def create_search_frame(self):
        search_frame = LabelFrame(self.root, text="Search Employee", bg="white")
        search_frame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_searchby,
                                  values=("Email", "Name", "Contact"), state='readonly', justify=CENTER,
                                  font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        Entry(search_frame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(
            x=200, y=10)
        Button(search_frame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50",
               fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

    def create_title(self):
        Label(self.root, text="Employee Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=50,
                                                                                                                y=100,
                                                                                                                width=1000)

    def create_content(self):
        # Content
        labels = ["Emp ID", "Gender", "Contact", "Name", "D.O.B", "D.O.J", "Email", "Password", "User Type"]
        entries = [self.var_emp_id, self.var_gender, self.var_contact, self.var_name, self.var_dob, self.var_doj,
                   self.var_email, self.var_pass, self.var_utype]
        x_positions = [50, 350, 750]

        for i, (label, entry) in enumerate(zip(labels, entries)):
            Label(self.root, text=label, font=("goudy old style", 15), bg="WHITE").place(x=x_positions[i % 3],
                                                                                          y=150 + 40 * (i // 3))
            if label == "Gender":
                cmb_gender = ttk.Combobox(self.root, textvariable=entry, values=("Male", "Female", "Others"),
                                          state='readonly', justify=CENTER, font=("goudy old style", 15,))
                cmb_gender.place(x=x_positions[i % 3] + 100, y=150 + 40 * (i // 3), width=180)
                cmb_gender.current(0)
            else:
                Entry(self.root, textvariable=entry, font=("goudy old style", 15), bg="lightyellow").place(
                    x=x_positions[i % 3] + 100, y=150 + 40 * (i // 3), width=180)

        # Address and Post
        Label(self.root, text="Address", font=("goudy old style", 15), bg="WHITE").place(x=50, y=270)
        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        Label(self.root, text="Post", font=("goudy old style", 15), bg="WHITE").place(x=500, y=270)
        Entry(self.root, textvariable=self.var_post, font=("goudy old style", 15), bg="lightyellow").place(x=600,
                                                                                                             y=270,
                                                                                                             width=180)

    def create_buttons(self):
        Button(self.root, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white",
               cursor="hand2").place(x=500, y=305, width=110, height=28)
        Button(self.root, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white",
               cursor="hand2").place(x=620, y=305, width=110, height=28)
        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white",
               cursor="hand2").place(x=740, y=305, width=110, height=28)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white",
               cursor="hand2").place(x=860, y=305, width=110, height=28)

    def create_employee_details_frame(self):
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.employeetable = ttk.Treeview(emp_frame,
                                          columns=("eid", "name", "email", "gender", "contact", "dob", "doj",
                                                   "pass", "utype", "address", "post"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.employeetable.xview)
        scrolly.config(command=self.employeetable.yview)

        self.employeetable.heading("eid", text="EMP ID")
        self.employeetable.heading("name", text="NAME")
        self.employeetable.heading("email", text="EMAIL")
        self.employeetable.heading("gender", text="GENDER")
        self.employeetable.heading("contact", text="CONTACT")
        self.employeetable.heading("dob", text="D.O.B")
        self.employeetable.heading("doj", text="D.O.J")
        self.employeetable.heading("pass", text="PASSWORD")
        self.employeetable.heading("utype", text="USER TYPE")
        self.employeetable.heading("address", text="ADDRESS")
        self.employeetable.heading("post", text="POST")

        self.employeetable["show"] = "headings"
        self.employeetable.pack(fill=BOTH, expand=1)
        self.employeetable.bind("<ButtonRelease-1> ", self.get_data)

    def add(self):
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                self.cursor.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = self.cursor.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    self.cursor.execute(
                        "INSERT INTO Employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,post) "
                        "VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0', END),
                            self.var_post.get(),
                        ))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Employee Added Successfully", parent=self.root)
                    self.show_employee_records()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_employee_records(self):
        try:
            self.cursor.execute("SELECT * FROM employee")
            rows = self.cursor.fetchall()
            self.employeetable.delete(*self.employeetable.get_children())
            for row in rows:
                self.employeetable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.employeetable.focus()
        content = (self.employeetable.item(f))
        row = content['values']
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[9])
        self.var_post.set(row[10])

    def update(self):
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                self.cursor.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = self.cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    self.cursor.execute(
                        "UPDATE Employee SET name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,"
                        "address=?,post=? WHERE eid=?", (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0', END),
                            self.var_post.get(),
                            self.var_emp_id.get(),
                        ))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show_employee_records()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID Must be required", parent=self.root)
            else:
                self.cursor.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = self.cursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        self.cursor.execute("DELETE FROM Employee WHERE eid=?", (self.var_emp_id.get(),))
                        self.conn.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("")
        self.txt_address.delete('1.0', END)
        self.var_post.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("")
        self.show_employee_records()

    def search(self):
        try:
            if self.var_searchby.get() == "":
                messagebox.showerror("Error", "Select search By Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                self.cursor.execute("SELECT * FROM employee WHERE " + self.var_searchby.get() + " LIKE ?",
                                    ('%' + self.var_searchtxt.get() + '%',))
                rows = self.cursor.fetchall()
                if len(rows) != 0:
                    self.employeetable.delete(*self.employeetable.get_children())
                    for row in rows:
                        self.employeetable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeManagement(root)
    root.mainloop()
