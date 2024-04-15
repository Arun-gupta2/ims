import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, Frame, Scrollbar, END, messagebox, ttk

class WarehouseManagement:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Warehouse Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_product_id = StringVar()
        self.var_name = StringVar()
        self.var_quantity = StringVar()
        self.var_location = StringVar()
        self.var_capacity = StringVar()

        # Title
        self.create_title()

        # Input
        self.create_input()

        # Buttons
        self.create_buttons()

        # Product Details
        self.create_product_details()

        # Create product table if not exists
        self.create_product_table()

        # Show products
        self.show_products()

    def create_title(self):
        lbl_title = Label(self.root, text="Manage Products in Warehouse", font=("goudy old style ",30), bg="darkorange", fg="white", bd=3, relief="ridge")
        lbl_title.pack(side="top", fill="x", padx=10, pady=20)

    def create_input(self):
        lbl_name = Label(self.root, text="Product Name", font=("goudy old style ",20), bg="white")
        lbl_name.place(x=50, y=100)
        self.txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style ",20), bg="lightyellow")
        self.txt_name.place(x=50, y=140, width=300)

        lbl_quantity = Label(self.root, text="Quantity", font=("goudy old style ",20), bg="white")
        lbl_quantity.place(x=50, y=200)
        self.txt_quantity = Entry(self.root, textvariable=self.var_quantity, font=("goudy old style ",20), bg="lightyellow")
        self.txt_quantity.place(x=50, y=240, width=300)

        lbl_location = Label(self.root, text="Location", font=("goudy old style ",20), bg="white")
        lbl_location.place(x=50, y=300)
        self.txt_location = Entry(self.root, textvariable=self.var_location, font=("goudy old style ",20), bg="lightyellow")
        self.txt_location.place(x=50, y=340, width=300)

        lbl_capacity = Label(self.root, text="Capacity", font=("goudy old style ",20), bg="white")
        lbl_capacity.place(x=50, y=400)
        self.txt_capacity = Entry(self.root, textvariable=self.var_capacity, font=("goudy old style ",20), bg="lightyellow")
        self.txt_capacity.place(x=50, y=440, width=300)

    def create_buttons(self):
        btn_add = Button(self.root, text="ADD", command=self.add_product, font=("goudy old style ",15), bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=50, y=500, width=150, height=40)
        btn_del = Button(self.root, text="Delete", command=self.delete_product, font=("goudy old style ",15), bg="red", fg="white", cursor="hand2")
        btn_del.place(x=210, y=500, width=150, height=40)

    def create_product_details(self):
        product_frame = Frame(self.root, bd=3, relief="ridge")
        product_frame.place(x=400, y=100, width=650, height=440)

        scrolly = Scrollbar(product_frame, orient="vertical")
        scrollx = Scrollbar(product_frame, orient="horizontal")

        self.product_table = ttk.Treeview(product_frame, columns=("pid", "name", "quantity", "location", "capacity"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side="bottom", fill="x")
        scrolly.pack(side="right", fill="y")
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="ID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("quantity", text="Quantity")
        self.product_table.heading("location", text="Location")
        self.product_table.heading("capacity", text="Capacity")
        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=60)
        self.product_table.column("name", width=150)
        self.product_table.column("quantity", width=90)
        self.product_table.column("location", width=90)
        self.product_table.column("capacity", width=90)
        self.product_table.pack(fill="both", expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_product_data)

    def create_product_table(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS products (
                            pid INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            location TEXT NOT NULL,
                            capacity INTEGER NOT NULL
                        )''')
            con.commit()
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error in creating product table: {str(ex)}", parent=self.root)

    def add_product(self):
        try:
            if self.var_name.get() == "" or self.var_quantity.get() == "" or self.var_location.get() == "" or self.var_capacity.get() == "":
                messagebox.showerror("Error", "Please enter all product details", parent=self.root)
            else:
                con = sqlite3.connect(database=r'ims.db')
                cur = con.cursor()
                cur.execute("INSERT INTO products(name, quantity, location, capacity) VALUES (?, ?, ?, ?)", (self.var_name.get(), self.var_quantity.get(), self.var_location.get(), self.var_capacity.get()))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                self.show_products()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_products(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error in fetching products: {str(ex)}", parent=self.root)

    def get_product_data(self, ev):
        try:
            selected_row = self.product_table.focus()
            values = self.product_table.item(selected_row, "values")
            if values:
                self.var_product_id.set(values[0])
                self.var_name.set(values[1])
                self.var_quantity.set(values[2])
                self.var_location.set(values[3])
                self.var_capacity.set(values[4])
        except IndexError:
            pass

    def delete_product(self):
        try:
            if self.var_product_id.get() == "":
                messagebox.showerror("Error", "Please select product from the list", parent=self.root)
            else:
                con = sqlite3.connect(database=r'ims.db')
                cur = con.cursor()
                cur.execute("SELECT * FROM products WHERE pid=?", (self.var_product_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Error, please try again", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM products WHERE pid=?", (self.var_product_id.get(),))
                        con.commit()
                    messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                    self.show_products()
                    self.var_product_id.set("")
                    self.var_name.set("")
                    self.var_quantity.set("")
                    self.var_location.set("")
                    self.var_capacity.set("")
                con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = WarehouseManagement(root)
    root.mainloop()
