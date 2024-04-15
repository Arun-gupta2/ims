from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from employee import EmployeeManagement
from supplier import supplierclass
from category import categoryclass
from product import productClass
from warehouse import WarehouseManagement

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory management system")
        self.root.config(bg="white")
        self.logged_in = False  # Flag to track login status
        self.user_role = ""  # To store the user's role (admin/employee). Default value is empty string.

        # ----------TITLE-----------------
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor='w', padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # ------btn_logout--------
        self.btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"), bg="yellow",
                            cursor="hand2", command=self.logout, state=DISABLED)
        self.btn_logout.place(x=1100, y=10, height=50, width=150)

        #========clock========
        self.lbl_clock = Label(self.root,
                               text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15,), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #==========left Menu===========
        self.MenuLogo = Image.open("images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.ANTIALIAS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="blue")
        LeftMenu.place(x=0, y=102, width=200, height=565)
        lbl_menulogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP, fill=X)

        #=======LEFT mENU BUTTONS===========
        self.icon_side = PhotoImage(file="images/side.png")

        lbl_menu = Button(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688", cursor="hand2")
        lbl_menu.pack(side=TOP, fill=X)

        btn_employee = Button(LeftMenu, text="Employee", command=self.employee, image=self.icon_side,
                              compound=LEFT, padx=5, anchor="w", font=("times new roman", 20, "bold"),
                              bg="white", bd=3, cursor="hand2")
        btn_employee.pack(side=TOP, fill=X)
        btn_supplier = Button(LeftMenu, text="Supplier", command=self.supplier, image=self.icon_side, compound=LEFT, padx=5,
                              anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X)
        btn_departement = Button(LeftMenu, text="Category", command=self.category, image=self.icon_side, compound=LEFT, padx=5,
                                 anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_departement.pack(side=TOP, fill=X)
        btn_product = Button(LeftMenu, text="Product", command=self.product, image=self.icon_side, compound=LEFT, padx=5,
                             anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_product.pack(side=TOP, fill=X)
        btn_warehouse = Button(LeftMenu, text="Warehouse", command=self.warehouse, image=self.icon_side, compound=LEFT, padx=5,
                             anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_warehouse.pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu, text="Exit", image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                          font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2")
        btn_exit.pack(side=TOP, fill=X)

        #######==========content========
        self.lbl_employee = Label(self.root, text="Total Employee\n[0]", bd=5, relief=RIDGE, bg="#33bbf9",
                                  fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n[0]", bd=5, relief=RIDGE, bg="#ff5772",
                                  fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=650, y=120, height=150, width=300)

        # self.lbl_departement = Label(self.root, text="Total Departments\n[0]", bd=5, relief=RIDGE, bg="#009688",
        #                               fg="white", font=("goudy old style", 20, "bold"))
        # self.lbl_departement.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(self.root, text="Total Products\n[0]", bd=5, relief=RIDGE, bg="#607db8",
                                 fg="white", font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        #######======footer=======
        self.lbl_clock = Label(self.root,
                               text="IMS-Inventory Management System ",
                               font=("times new roman", 15,), bg="#4d636d", fg="white")
        self.lbl_clock.pack(side=BOTTOM, fill=X)

        # Login Page
        self.create_login_page()

    def create_login_page(self):
        self.login_frame = Frame(self.root, bd=5, relief=GROOVE, bg="white")
        self.login_frame.place(x=400, y=200)

        lbl_user = Label(self.login_frame, text="Email", font=("times new roman", 20), bg="white")
        lbl_user.grid(row=0, column=0, padx=20, pady=10)
        self.txt_user = Entry(self.login_frame, font=("times new roman", 15), bd=5)
        self.txt_user.grid(row=0, column=1, padx=20)

        lbl_pass = Label(self.login_frame, text="Password", font=("times new roman", 20), bg="white")
        lbl_pass.grid(row=1, column=0, padx=20, pady=10)
        self.txt_pass = Entry(self.login_frame, font=("times new roman", 15), bd=5, show="*")
        self.txt_pass.grid(row=1, column=1, padx=20)

        lbl_role = Label(self.login_frame, text="Role", font=("times new roman", 20), bg="white")
        lbl_role.grid(row=2, column=0, padx=20, pady=10)
        self.role_var = StringVar()
        self.role_var.set("admin")  # Default role is admin
        self.role_menu = OptionMenu(self.login_frame, self.role_var, "admin", "employee")
        self.role_menu.config(font=("times new roman", 15), bg="white", bd=5)
        self.role_menu.grid(row=2, column=1, padx=20)

        btn_login = Button(self.login_frame, text="Login", font=("times new roman", 15, "bold"), bg="yellow", fg="black",
                           cursor="hand2", command=self.login)
        btn_login.grid(row=3, columnspan=2, pady=10)

    def login(self):
        email = self.txt_user.get()
        password = self.txt_pass.get()
        role = self.role_var.get()
        
        # Connect to the SQLite database
        conn = sqlite3.connect("ims.db")
        cursor = conn.cursor()

        # Query the database to retrieve user details
        cursor.execute("SELECT * FROM employee WHERE email=? AND pass=? AND utype=?", (email, password, role))
        user = cursor.fetchone()

        if user:
            self.user_role = role  # Fetch the role from the database
            messagebox.showinfo("Login Success", f"Welcome {email}!")
            self.logged_in = True
            self.open_dashboard()  # Redirect to Dashboard
            self.btn_logout.config(state=NORMAL)  # Enable logout button
            self.login_frame.destroy()  # Destroy login frame after successful login
        else:
            messagebox.showerror("Login Error", "Invalid Email, Password, or Role")

        conn.close()  # Close the database connection

    def open_dashboard(self):
        if self.logged_in:
            if self.user_role == "admin":
                # Implement admin dashboard logic here
                pass
            elif self.user_role == "employee":
                pass
                # Implement employee dashboard logic here (with restricted access)
            else:
                messagebox.showerror("Access Denied", "Unknown user role.")
        else:
            messagebox.showerror("Access Denied", "Please login first.")

    def employee(self):
        if self.logged_in:
            if self.user_role != "employee":
                self.__new_win = Toplevel(self.root)
                self.__new_obj = EmployeeManagement(self.__new_win)
            else:
                messagebox.showerror("Access Denied", "Employees are not allowed to access this module.")
        else:
            messagebox.showerror("Access Denied", "Please login first.")

    def warehouse(self):
        if self.logged_in:
            self.__new_win = Toplevel(self.root)
            self.__new_obj = WarehouseManagement(self.__new_win)
        else:
            messagebox.showerror("Access Denied", "Please login first.")

    def supplier(self):
        if self.logged_in:
            self.__new_win = Toplevel(self.root)
            self.__new_obj = supplierclass(self.__new_win)
        else:
            messagebox.showerror("Access Denied", "Please login first.")

    def category(self):
        if self.logged_in:
            self.__new_win = Toplevel(self.root)
            self.__new_obj = categoryclass(self.__new_win)
        else:
            messagebox.showerror("Access Denied", "Please login first.")

    def product(self):
        if self.logged_in:
            self.__new_win = Toplevel(self.root)
            self.__new_obj = productClass(self.__new_win)
        else:
            messagebox.showerror("Access Denied", "Please login first.")

    def logout(self):
        self.logged_in = False
        self.btn_logout.config(state=DISABLED)  # Disable logout button
        self.create_login_page()  # Recreate login page after logout

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
