
The Inventory Management System is a desktop application developed using Python with Tkinter for the graphical user interface and MySQL for the database.
This system helps manage inventory efficiently by tracking employees, products, suppliers, and warehouse stock levels.

# Features
- User Authentication: Secure login and signup functionality.
- Employee Management: Add, update, and manage employee records.
- Product Management: Add, update, delete, and view products.
- Supplier Management: Maintain supplier details and manage relationships.
- Warehouse Management: Track stock levels and inventory movement.

# Technologies Used
- Programming Language: Python (Tkinter for GUI)
- Database: MySQL
- Libraries & Tools:
  - `tkinter` for GUI
  - `mysql-connector-python` for database connectivity
  - `Pillow` for handling images (if needed)

# Modules
1. **Login & Signup Module**
   - User authentication and registration.
   - Secure password storage and validation.
2. **Employee Module**
   - Add, update, and delete employee records.
   - Search and filter employees.
3. **Product Module**
   - Manage product details including name, price, and quantity.
   - Stock level monitoring.
4. **Supplier Module**
   - Store and update supplier information.
   - Track supplier transactions.
5. **Warehouse Module**
   - Manage inventory storage and stock levels.
   - Track incoming and outgoing inventory.

## Installation & Setup
1. **Install Dependencies:**
   ```sh
   pip install mysql-connector-python pillow
   ```
2. **Set Up Database:**
   - Create a MySQL database.
   - Import the provided SQL file (`database.sql`) to initialize tables.
3. **Run the Application:**
   ```sh
   python main.py
   ```


## Future Enhancements
- Implement user roles and permissions.
- Generate detailed reports for inventory analysis.
- Improve UI with better styling and responsiveness.



