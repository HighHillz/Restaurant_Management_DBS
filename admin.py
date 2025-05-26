import tkinter as tk 
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as conn

class UI:
    def __init__(self, window, window_dim):
        self.window = window
        self.window_width, self.window_height = window_dim
        self.show_passwd = False
    
    def connect_db(self):
        self.mydb = conn.connect(host="localhost", user="root", passwd="root", database="restaurant")
        if self.mydb.is_connected():
            print(f"Connection with {__name__} has been established!")
        else:
            exit(-1)

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT order_id FROM logtable")
        self.order_id = max([row[0] for row in self.mycursor.fetchall()] or [0]) + 1

    def admin_page(self):
        def toggle_passwd(field) :
            self.show_passwd = not self.show_passwd

            if self.show_passwd :
                field.config(show="")
                show_passwd_btn.config(text="Hide")
            else :
                field.config(show="*")
                show_passwd_btn.config(text="Show")
        
        # Clear the current frame
        for widget in self.window.winfo_children():
            widget.destroy()

        # Admin login frame
        login_frame = tk.Frame(self.window, bg="#222222")
        login_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Username label and entry field
        tk.Label(login_frame, text="Username:", font=("Consolas", 12), bg="#222222", fg="#E8E8E8").grid(row=0, column=0, pady=10)
        username_entry = tk.Entry(login_frame, font=("Consolas", 12), bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8")
        username_entry.grid(row=0, column=1, pady=10)

        # Password label and entry field (with obscured text)
        tk.Label(login_frame, text="Password:", font=("Consolas", 12), bg="#222222", fg="#E8E8E8").grid(row=1, column=0, pady=10)
        password_entry = tk.Entry(login_frame, font=("Consolas", 12), show="*", bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8")
        password_entry.grid(row=1, column=1, pady=10)
        
        show_passwd_btn = tk.Button(
            login_frame, text="Show", width=5, height=1, cursor="hand2",
            bg="#222222", fg="white", font=("Consolas", 8),
            command=lambda: toggle_passwd(password_entry), activebackground="black", activeforeground="#E8E8E8"
        )
        show_passwd_btn.grid(row=1, column=2, padx=10)

        # Message label for displaying errors
        message_label = tk.Label(login_frame, text="", font=("Consolas", 10), bg="#222222")
        message_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Login button
        login_but = tk.Button(
            login_frame, text="Login", width=6, height=1, cursor="hand2",
            bg="#4CAF50", fg="white", font=("Consolas", 12, "bold"),
            command=lambda: self.verify_admin_login(username_entry.get(), password_entry.get(), message_label), activebackground="black", activeforeground="#E8E8E8"
        )
        login_but.grid(row=2, column=0, columnspan=2, pady=10)

    def verify_admin_login(self, username, password, message_label):
        # Simple placeholder credentials for demonstration
        admin_credentials = {"": ""}

        # Check if the credentials match
        if username in admin_credentials and admin_credentials[username] == password:
            message_label.config(text="Login successful!", fg="green")
            self.open_admin_dashboard()  # Proceed to the admin dashboard after successful login
        else:
            message_label.config(text="Invalid credentials. Please try again.", fg="#ff7b6f")

    def open_admin_dashboard(self):
        # Clear the current frame
        for widget in self.window.winfo_children():
            widget.destroy()

        # Admin dashboard frame
        dashboard_frame = tk.Frame(self.window, bg="#222222")
        dashboard_frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(dashboard_frame, text="Welcome to the Admin Dashboard!", font=("Consolas", 14), bg="#222222", fg="#E8E8E8").pack(pady=20)
        
        # Manage Restaurant button
        manage_restaurant_but = tk.Button(
            dashboard_frame, text="Manage Restaurant", width=20, height=2, cursor="hand2",
            bg="#4CAF50", fg="white", font=("Consolas", 12, "bold"),
            command=lambda: self.manage_restaurant(), activebackground="black", activeforeground="#E8E8E8"
        )
        manage_restaurant_but.pack(pady=10)

        # Purchase Log button
        purchase_log_but = tk.Button(
            dashboard_frame, text="Purchase Log", width=20, height=2, cursor="hand2",
            bg="#2196F3", fg="white", font=("Consolas", 12, "bold"),
            command=lambda: self.view_purchase_log(), activebackground="black", activeforeground="#E8E8E8"
        )
        purchase_log_but.pack(pady=10)
        
        # Example: Log out button
        logout_but = tk.Button(
            dashboard_frame, text="Log Out", width=12, height=2, cursor="hand2",
            bg="#f44336", fg="white", font=("Consolas", 12, "bold"),
            command=lambda: self.admin_page(), activebackground="black", activeforeground="#E8E8E8"
        )
        logout_but.pack(pady=20)

    def manage_restaurant(self):
        # Clear the current frame
        for widget in self.window.winfo_children():
            widget.destroy()

        tk.Label(self.window, text="Manage Restaurant", font=("Consolas", 16), bg="#222222", fg="#E8E8E8").pack(pady=10)

        # Filter Frame
        filter_frame = tk.Frame(self.window, bg="#222222")
        filter_frame.pack(pady=10)

        # Category Filter
        tk.Label(filter_frame, text="Category:", font=("Consolas", 12), bg="#222222", fg="#E8E8E8").grid(row=0, column=0, padx=5)
        category_var = tk.StringVar()
        category_dropdown = tk.OptionMenu(filter_frame, category_var, *self.get_unique_values("Category"))
        category_dropdown.config(bg="#222222", fg="#E8E8E8", activebackground="black", activeforeground="#E8E8E8", font=("Consolas", 10))
        category_dropdown["menu"].config(bg="#222222", fg="#e8e8e8", font=("Consolas", 10))
        category_dropdown.grid(row=0, column=1, padx=5)

        # Type Filter
        tk.Label(filter_frame, text="Type:", font=("Consolas", 12), bg="#222222", fg="#E8E8E8").grid(row=0, column=2, padx=5)
        type_var = tk.StringVar()
        type_dropdown = tk.OptionMenu(filter_frame, type_var, *self.get_unique_values("Type"))
        type_dropdown.config(bg="#222222", fg="#E8E8E8", activebackground="black", activeforeground="#E8E8E8", font=("Consolas", 10))
        type_dropdown["menu"].config(bg="#222222", fg="#e8e8e8", font=("Consolas", 10))
        type_dropdown.grid(row=0, column=3, padx=5)

        # Name Filter
        tk.Label(filter_frame, text="Name:", font=("Consolas", 12), bg="#222222", fg="#E8E8E8").grid(row=0, column=4, padx=5)
        name_var = tk.StringVar()
        name_entry = tk.Entry(filter_frame, textvariable=name_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12))
        name_entry.grid(row=0, column=5, padx=5)

        # Filter Button
        search_but = tk.Button(
            filter_frame, text="Search", cursor="hand2", bg="#4CAF50", fg="white", font=("Consolas", 12),
            command=lambda: self.filter_items(category_var.get(), type_var.get(), name_var.get()), activebackground="black", activeforeground="#E8E8E8"
        )
        search_but.grid(row=0, column=6, padx=10)

        # Cancel Button (Clear Filters)
        cancel_but = tk.Button(
            filter_frame, text="Clear", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 12),
            command=lambda: self.manage_restaurant(), activebackground="black", activeforeground="#E8E8E8"  # Reset the entire page
        )
        cancel_but.grid(row=0, column=7, padx=10)

        # Editable fields frame
        global item_fields_frame
        item_fields_frame = ctk.CTkScrollableFrame(self.window, width=self.window_width-200, height=400)
        item_fields_frame.pack(pady=20)

        # New Item Button
        create_item_but = tk.Button(
            self.window, text="Create New Item", cursor="hand2", bg="#4CAF50", fg="white", font=("Consolas", 12),
            command=lambda: self.create_new_item(), activebackground="black", activeforeground="#E8E8E8"
        )
        create_item_but.pack(pady=10)

        # Back Button
        back_but = tk.Button(
            self.window, text="Back to Dashboard", cursor="hand2", bg="#3eb7c1", fg="white", font=("Consolas", 12),
            command=lambda: self.open_admin_dashboard(), activebackground="black", activeforeground="#E8E8E8"
        )
        back_but.place(x=self.window_width-200,y=self.window_height-50)

    def get_unique_values(self, column_name):
        self.mycursor.execute(f"SELECT DISTINCT {column_name} FROM food")
        return [row[0] for row in self.mycursor.fetchall()]

    def filter_items(self, category, type_, name):
        query = "SELECT ID, Name, Category, Type, Price FROM food WHERE 1=1"
        params = []

        if category:
            query += " AND Category = %s"
            params.append(category)
        if type_:
            query += " AND Type = %s"
            params.append(type_)
        if name:
            query += " AND Name LIKE %s"
            params.append(f"%{name}%")

        self.mycursor.execute(query, params)
        items = self.mycursor.fetchall()

        # Clear previous results
        for widget in item_fields_frame.winfo_children():
            widget.destroy()

        if items:
            for item in items:
                self.create_editable_item_fields(item)
        else:
            tk.Label(item_fields_frame, text="No items found", font=("Consolas", 12), bg="#2b2b2b", fg="#e8e8e8").pack()

    def create_editable_item_fields(self, item, is_new=False):
        item_id, item_name, item_category, item_type, item_price = item

        # Check if the header already exists before creating
        if not item_fields_frame.winfo_children():
            header_frame = tk.Frame(item_fields_frame, bg="#2b2b2b")
            header_frame.pack(pady=5, anchor="n")

            # Add column headers
            headers = ["Category", "Type", "Name", "Price"]
            for col, text in enumerate(headers):
                tk.Label(header_frame, text=text, bg="#2b2b2b", fg="#E8E8E8", font=("Consolas", 12), width=12).grid(row=0, column=col, padx=5)

            tk.Label(header_frame, bg="#2b2b2b", width=8).grid(row=0, column=4)
            tk.Label(header_frame, bg="#2b2b2b", width=8).grid(row=0, column=5)

        # Frame for editable fields
        frame = tk.Frame(item_fields_frame, bg="#2b2b2b")
        frame.pack(pady=5)

        # Editable fields for category, type, name, and price
        category_var = tk.StringVar(value=item_category)
        tk.Entry(frame, textvariable=category_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12), width=12).grid(row=0, column=0, padx=5)

        type_var = tk.StringVar(value=item_type)
        tk.Entry(frame, textvariable=type_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12), width=12).grid(row=0, column=1, padx=5)

        name_var = tk.StringVar(value=item_name)
        tk.Entry(frame, textvariable=name_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12), width=12).grid(row=0, column=2, padx=5)

        price_var = tk.StringVar(value=item_price)
        tk.Entry(frame, textvariable=price_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12), width=12).grid(row=0, column=3, padx=5)

        # Save Button
        if not is_new :
            save_but = tk.Button(
                frame, text="Save", cursor="hand2", bg="#4CAF50", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
                command=lambda: [self.save_item(item_id, category_var.get(), type_var.get(), name_var.get(), price_var.get())]
            )
            save_but.grid(row=0, column=4, padx=4)
        else :
            tk.Button(
                frame, text="Create", cursor="hand2", bg="#4CAF50", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
                command=lambda: [self.create_item(category_var.get(), type_var.get(), name_var.get(), price_var.get())]
            ).grid(row=0, column=4, padx=4)

        # Delete Button
        delete_but = tk.Button(
            frame, text="Delete", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
            command=lambda: self.delete_item(item_id)
        )
        delete_but.grid(row=0, column=5, padx=5)

    def create_new_item(self):
        # Add new item with empty fields and reset view
        self.manage_restaurant()
        self.create_editable_item_fields((None, "", "", "", ""), is_new=True)
        self.mydb.commit()

    def save_item(self, item_id, category, type_, name, price):
        if not category or not type_ or not name or not price:
            messagebox.showerror('Error', "All fields must be filled out.")
            return 
        else:
            messagebox.showinfo("Success!", "Item has been successfully modified")   
        
        self.mycursor.execute(
            "UPDATE food SET Name=%s, Category=%s, Type=%s, Price=%s WHERE ID=%s",
            (name, category, type_, price, item_id)
        )

        self.mydb.commit()
        self.manage_restaurant()  # Reload the page after saving

    def create_item(self, category, type_, name, price) :
        try :
            if round(float(price), 0) <= 0 :
                messagebox.showerror('Error', "Price must be greater than 0.")
                return
        except :
            messagebox.showerror('Error', "Price must be a number.")
            return
        
        self.mycursor.execute("select category, type, name from food")
        for i in self.mycursor.fetchall() :
            if category.lower() == i[0].lower() and type_.lower() == i[1].lower() and name.lower() == i[2].lower() :
                messagebox.showerror("Error", "Item already exists!")
                break
        else :
            self.mycursor.execute("insert into food (name, category, type, price) values('{}', '{}', '{}', {})".format(name.title(), category.title(), type_.title(), price))
            messagebox.showinfo("Success!", "Item has been successfully added")   
            self.mydb.commit()
            self.manage_restaurant()

    def delete_item(self, item_id):

        res = messagebox.askquestion("Confirmation", "Do you want to delete this item?")

        if res == "yes" :
            self.mycursor.execute("DELETE FROM food WHERE ID = %s", (item_id,))
            self.mydb.commit()
            self.manage_restaurant()  # Reload the page after deleting

    def view_purchase_log(self):
        def clear_items():
            if log_records == [] :
                messagebox.showinfo("Empty", "No records to clear")
            else :
                res = messagebox.askquestion("Confirmation", "Do you want to clear all records?")
                if res == "yes" :
                    self.mycursor.execute('DELETE FROM logtable')
                    self.mydb.commit()
                    self.view_purchase_log()
                    messagebox.showinfo("Success", "All records have been cleared")
                    self.order_id = 1

        # Clear the current frame
        for widget in self.window.winfo_children():
            widget.destroy()

        tk.Label(self.window, text="Purchase Log", font=("Consolas", 16), bg="#222222", fg="#e8e8e8").pack(pady=20)

        log_frame = ctk.CTkScrollableFrame(self.window, width=self.window_width-150, height=400)
        log_frame.pack(pady=10)

        # Define the column headers
        headers = ["Order ID", "Name", "Quantity", "Total Amount", "Date"] 

        # Add headers to the log frame
        for col in range(len(headers)):
            tk.Label(log_frame, text=headers[col], width=18, font=("Consolas", 12, "bold"), 
                    fg="#e8e8e8", bg="#333333", borderwidth=1, relief='ridge').grid(row=0, column=col, pady=5, padx=2)

        # Fetch and display the log details from the database
        log_records = []
        self.mycursor.execute("SELECT * FROM logtable")
        log_records = self.mycursor.fetchall()

        if log_records:
            row = 1  # Start from row 1 to leave space for headers
            for record in log_records:
                for col in range(len(record)):
                    tk.Label(log_frame, text=record[col], width=20, font=("Consolas", 10), 
                            fg="#e8e8e8", bg="#2b2b2b", borderwidth=1, relief='ridge').grid(row=row, column=col, pady=5, padx=2)
                row += 1

        # Example: Add button to go back to the dashboard
        back_but = tk.Button(
            self.window, text="Back to Dashboard", cursor="hand2", bg="#3eb7c1", fg="white", font=("Consolas", 12),
            command=lambda: self.open_admin_dashboard(), activebackground="black", activeforeground="#E8E8E8"
        )
        back_but.place(x=self.window_width-200, y=self.window_height-50)

        clear_but = tk.Button(
            self.window, text="Clear", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 12),
            command=lambda: clear_items(), activebackground="black", activeforeground="#E8E8E8"
        )
        clear_but.pack(pady=10)
    
    def establish(self):
        self.connect_db()
        self.admin_page()