import sqlite3
from tkinter import *
from tkinter import ttk, messagebox


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory management system ")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        self.cat_list = []
        self.sup_list = []

        # Functions
        self.create_product_table()
        self.fetch_cat_sup()

        # Frame
        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_frame.place(x=10, y=10, width=450, height=480)

        # Title
        title = Label(product_frame, text="Manage Product Details", font=("goudy old style", 18), bg="#0f4d7d",
                      fg="white")
        title.pack(side=TOP, fill=X)

        # Column 1
        lbl_category = Label(product_frame, text="Category", font=("goudy old style", 18), bg="white")
        lbl_category.place(x=30, y=60)

        lbl_supplier = Label(product_frame, text="Supplier", font=("goudy old style", 18), bg="white")
        lbl_supplier.place(x=30, y=110)

        lbl_productname = Label(product_frame, text="Name", font=("goudy old style", 18), bg="white")
        lbl_productname.place(x=30, y=160)

        lbl_price = Label(product_frame, text="Price", font=("goudy old style", 18), bg="white")
        lbl_price.place(x=30, y=210)

        lbl_quantity = Label(product_frame, text="Quantity", font=("goudy old style", 18), bg="white")
        lbl_quantity.place(x=30, y=260)

        lbl_status = Label(product_frame, text="Status", font=("goudy old style", 18), bg="white")
        lbl_status.place(x=30, y=310)

        # Column 2
        cmb_cat = ttk.Combobox(product_frame, textvariable=self.var_cat, values=self.cat_list, state='readonly',
                               justify=CENTER, font=("goudy old style", 15,))
        cmb_cat.place(x=150, y=60, width=200)
        cmb_cat.current(0)

        cmb_sup = ttk.Combobox(product_frame, textvariable=self.var_sup, values=self.sup_list, state='readonly',
                               justify=CENTER, font=("goudy old style", 15,))
        cmb_sup.place(x=150, y=110, width=200)
        cmb_sup.current(0)

        txt_sup = Entry(product_frame, textvariable=self.var_name, font=("goudy old style", 15,), bg="lightyellow")
        txt_sup.place(x=150, y=160, width=200)

        txt_price = Entry(product_frame, textvariable=self.var_price, font=("goudy old style", 15,), bg="lightyellow")
        txt_price.place(x=150, y=210, width=200)

        txt_qty = Entry(product_frame, textvariable=self.var_qty, font=("goudy old style", 15,), bg="lightyellow")
        txt_qty.place(x=150, y=260, width=200)

        cmb_status = ttk.Combobox(product_frame, textvariable=self.var_status, values=("Active", "Inactive",),
                                  state='readonly', justify=CENTER, font=("goudy old style", 15,))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # Buttons
        btn_add = Button(product_frame, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3",
                         fg="white", cursor="hand2")
        btn_add.place(x=10, y=400, width=100, height=40)

        btn_update = Button(product_frame, text="Update", command=self.update, font=("goudy old style", 15),
                            bg="#4caf50", fg="white", cursor="hand2")
        btn_update.place(x=120, y=400, width=100, height=40)

        btn_delete = Button(product_frame, text="Delete", command=self.delete, font=("goudy old style", 15),
                            bg="#f44336", fg="white", cursor="hand2")
        btn_delete.place(x=230, y=400, width=100, height=40)

        btn_clear = Button(product_frame, text="Clear", command=self.clear, font=("goudy old style", 15),
                           bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.place(x=340, y=400, width=100, height=40)

        # Search Frame
        searchFrame = LabelFrame(self.root, text="Search Product", bg="white")
        searchFrame.place(x=480, y=10, width=600, height=80)

        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby,
                                  values=("Select", "Category", "Supplier", "Name"), state='readonly',
                                  justify=CENTER, font=("goudy old style", 15,))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15),
                           bg="lightyellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(searchFrame, text="Search", command=self.search, font=("goudy old style", 15),
                            bg="#4caf50", fg="white", cursor="hand2")
        btn_search.place(x=410, y=9, width=150, height=30)

        # Product Details
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame, columns=("pid", "Category", "Supplier", "Name", "Price", "qty",
                                                            "Status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="P ID")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Supplier", text="Supplier")
        self.product_table.heading("Name", text="Name")
        self.product_table.heading("Price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("Status", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=90)
        self.product_table.column("Category", width=100)
        self.product_table.column("Supplier", width=100)
        self.product_table.column("Name", width=100)
        self.product_table.column("Price", width=100)
        self.product_table.column("qty", width=100)
        self.product_table.column("Status", width=100)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1> ", self.get_data)

        self.show()

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select name from category")
            cat = cur.fetchall()

            if len(cat) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from supplier")
            sup = cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_sup.get() == "Select" \
                    or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("Select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already present, try different", parent=self.root)
                else:
                    cur.execute("Insert into product(Category,Supplier,Name,Price,qty,Status) values(?,?,?,?,?,?)", (
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        self.var_pid.set(row[0]),
        self.var_cat.set(row[1]),
        self.var_sup.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please Select product from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product ID ", parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Supplier=?,Name=?,Price=?,qty=?,Status=? where pid=?",
                                (
                                    self.var_cat.get(),
                                    self.var_sup.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_qty.get(),
                                    self.var_status.get(),
                                    self.var_pid.get()
                                ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select product from list", parent=self.root)
            else:
                cur.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product ", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("delete from product where pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select search By Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("Select * from product where " + self.var_searchby.get() + " LIKE '%" +
                            self.var_searchtxt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def create_product_table(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS product (
                            pid INTEGER PRIMARY KEY AUTOINCREMENT,
                            Category TEXT,
                            Supplier TEXT,
                            Name TEXT,
                            Price REAL,
                            qty INTEGER,
                            Status TEXT
                        )''')
            con.commit()
            con.close()
            print("Product table created successfully")
        except Exception as ex:
            print(f"Error: {ex}")





if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
