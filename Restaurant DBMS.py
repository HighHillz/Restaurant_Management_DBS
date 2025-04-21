import tkinter as tk 
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as conn
import csv

def welcome_page():
    """Display the welcome page with two buttons: Admin and Customer."""

    for widget in window.winfo_children() :
        widget.destroy()
    
    # Quit button
    quit_but = tk.Button(
        window, text="Quit", cursor="hand2", foreground="white", bg="#f44336",
        font=("Consolas", 12), command=lambda: window.destroy(), activebackground="black", activeforeground="#E8E8E8"
    )
    quit_but.place(x=window_width-100, y=window_height-50)

    welcome_frame = tk.Frame(window, bg="#222222")
    welcome_frame.place(relx=0.5, rely=0.4, anchor="center")
        
    # Window Title
    tk.Label(welcome_frame, text="Welcome to A2N Cafe", font=("Consolas", 24), bg="#222222", fg="#E8E8E8").pack(pady=50)

    # Admin button
    admin_but = tk.Button(
        welcome_frame, text="Admin", width=15, height=2, cursor="hand2",
        bg="#3eb7c1", fg="white", font=("Consolas", 12, "bold"),
        command=lambda: admin_page(), activebackground="black", activeforeground="#E8E8E8"
    )
    admin_but.pack(pady=10)

    # Customer button
    customer_but = tk.Button(
        welcome_frame, text="Customer", width=15, height=2, cursor="hand2",
        bg="#3eb7c1", fg="white", font=("Consolas", 12, "bold"),
        command=lambda: list_category(), activebackground="black", activeforeground="#E8E8E8"
    )
    customer_but.pack(pady=10)

def list_category():
    """List all available categories for selecting on the customer home page."""
    global cat_but

    # Clear any existing widgets on the window
    for widget in window.winfo_children():
        widget.destroy()
        
    #Cart button
    order_but = tk.Button(
        window, text="Show Order", cursor="hand2", foreground="black", bg="#ffef00",
        font=("Consolas", 12), command=lambda: open_order(), activebackground="black", activeforeground="#E8E8E8"
    )
    order_but.place(x=window_width-220, y=window_height-50)
    
    # Quit button
    quit_but = tk.Button(
        window, text="Quit", cursor="hand2", foreground="white", bg="#f44336",
        font=("Consolas", 12), command=lambda: window.destroy(), activebackground="black", activeforeground="#E8E8E8"
    )
    quit_but.place(x=window_width-100, y=window_height-50)
    
    # Create a new frame for categories on the left side of the window
    cat_frame = ctk.CTkScrollableFrame(window, width=150, height=500, fg_color="transparent", scrollbar_fg_color="#272727")
    cat_frame.place(relx=0, rely=0)

    # Query categories from the database
    mycursor.execute("SELECT DISTINCT category FROM food")
    categories = mycursor.fetchall()

    cat_but = {}  # Dictionary to hold buttons

    # Create a button for each category
    for category in categories:
        cat = category[0]
        cat_but[cat] = tk.Button(
            cat_frame, text=cat, width=12, height=3, cursor="hand2",
            bg="#3eb7c1", fg="white", font=("Consolas", 12, "bold"),
            command=lambda m=cat: list_items(m), activebackground="black", activeforeground="#E8E8E8"
        )
        cat_but[cat].pack(pady=10)  # Arrange buttons vertically with padding

def list_items(category):
    """List available food items in the selected category and display them on the right side."""
    global item_but

    # Create a new frame for items on the right side of the window
    items_frame = ctk.CTkScrollableFrame(window, width=500, height=400)
    items_frame.place(relx=0.6, rely=0.4, anchor="center")

    # Fetch items from the database for the selected category
    items = []
    mycursor.execute("SELECT Name, Price FROM food WHERE category = %s", (category,))
    items = mycursor.fetchall()

    # Create a title label in the items frame
    tk.Label(items_frame, text=category, font=("Consolas", 14, "bold"), fg="#E8E8E8", bg="#2b2b2b").pack(pady=10)

    item_but = {}  # Dictionary to hold item buttons

    # Check if items exist for the selected category
    if items:
        # Create a button for each item in the selected category
        for item in items:
            item_name, item_price = item
            item_but[item_name] = tk.Button(
                items_frame, text=f"{item_name} - ₹{item_price}", width=30, height=2, cursor="hand2",
                bg="#216f75", fg="white", font=("Consolas", 10),
                command=lambda m=item_name: open_popup(m), activebackground="black", activeforeground="#E8E8E8"
            )
            item_but[item_name].pack(pady=5)
    else:
        # If no items found, display a message
        tk.Label(items_frame, text="No items available", font=("Consolas", 12), fg="#E8E8E8", bg="#2b2b2b").pack(pady=20)

def open_popup(item_name):
    """Open a popup to enter quantity for the selected item."""
    global money
    
    def submit() :
        """Ensure validity of input value."""
        global money
        i = quantity_entry.get()
        try :
            z = int(i)
            mycursor.execute("select name from orders where name = '%s'" %(item_name))
            r = mycursor.fetchone()
            #Statements to add to order
            if r :
                mycursor.execute("update orders set qty=qty+%s where name = '%s'" %(z, item_name))
                mycursor.execute("update orders set total_price=total_price+%s where name = '%s'" %(price*z, item_name))
            else :
                mycursor.execute("insert into orders values('%s', %s, %s, %s)" %(item_name, z, price, price*z))
            money += price*z
            mydb.commit()
            top.destroy()
        except ValueError:
            messagebox.showerror('Error', "Please provide an integer value")
        except conn.errors.DatabaseError :
            messagebox.showerror('Error', "Please provide a value greater than 0")
    
    mycursor.execute("SELECT Price FROM food WHERE Name = '%s'" %(item_name,))
    price = mycursor.fetchall()[0][0]

    top = tk.Toplevel(window)
    top.geometry("300x300")
    top.config(bg="#222222")
    top.grab_set()
    top.resizable(0,0)

    tk.Label(top, text="Please enter the quantity", font=("Consolas", 12), fg="#E8E8E8", bg="#222222").pack(pady=20)
    tk.Message(top, width=300, text=f"Food item: {item_name}", font=("Consolas", 10), fg="#E8E8E8", bg="#222222").pack()
    tk.Message(top, width=200, text=f"Price per item: ₹{price}", font=("Consolas", 10), fg="#E8E8E8", bg="#222222").pack()

    quantity_entry = tk.Entry(top, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12))
    quantity_entry.pack(pady=10)

    tk.Button(top, cursor="hand2", text="Add to order", command=lambda : submit(), bg="#4CAF50", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8").place(x=70,y=150)
    tk.Button(top, cursor="hand2", text="Cancel", command=lambda : top.destroy(), bg="#f44336", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8").place(x=170,y=150)

def open_order():
    """Show the list of items selected for placing an order."""
    global money  # Ensure global variables are used

    # Check if order is empty and show a message
    mycursor.execute("select * from orders")
    rows = mycursor.fetchall()

    if not rows:
        empty_order_message = tk.Toplevel(window)
        empty_order_message.geometry("300x200")
        empty_order_message.resizable(0,0)
        empty_order_message.config(bg="#222222")
        empty_order_message.grab_set()
        tk.Label(empty_order_message, text="Your order is empty!",fg="#E8E8E8", bg="#222222", font=("Consolas", 12)).pack(pady=50)
        tk.Button(
            empty_order_message, text="Okay", command=lambda: empty_order_message.destroy(),
            font=("Consolas", 10), bg="#4CAF50", fg="white", cursor="hand2", activebackground="black", activeforeground="#E8E8E8"
        ).pack(pady=10)
        return

    # Define the payment process function
    def pay_money():
        """Handle payment process and clear the order after payment."""
        global money  # Ensure we modify the global order and money variables

        payPage = tk.Toplevel(order_window)
        payPage.resizable(0,0)
        payPage.geometry("300x200")
        payPage.config(bg="#222222")
        payPage.grab_set()

        # Display amount to be paid
        tk.Message(payPage, width=200, text=f"Amount to pay: ₹{money}", fg="#E8E8E8", bg="#222222").place(x=70, y=50)
        
        # Pay button
        tk.Button(
            payPage, cursor="hand2", text="Pay", command=lambda: complete_payment(payPage),
            bg="#4CAF50", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8"
        ).place(x=110, y=100)

    def complete_payment(payPage):
        """Complete payment, clear order, and reset money."""
        global money
        for i in rows:
            mycursor.execute("Insert into logtable values('{}', {}, {},NOW())".format(i[0], i[1], i[3]))
        mycursor.execute("delete from orders")
        money = 0     # Reset the money variable
        payPage.destroy()  # Close the payment page
        order_window.destroy()  # Close the order window
        list_category() # Goes back to menu for the next user
        mydb.commit()
    
        # Show a message indicating successful payment
        success_message = tk.Tk()
        success_message.geometry("300x200")
        success_message.config(bg="#222222")
        success_message.resizable(0,0)
        success_message.grab_set()
        tk.Label(success_message, text="Payment successful!", fg="#E8E8E8", bg="#222222", font=("Consolas", 12)).pack(pady=50)
        tk.Button(
            success_message, text="Okay", command=lambda: success_message.destroy(),
            font=("Consolas", 10), bg="#4CAF50", fg="white", cursor="hand2", activebackground="black", activeforeground="#E8E8E8"
        ).pack(pady=10)
        success_message.mainloop()
    
    def populate_order(data) :
        for col in range(len(data)):
            tk.Label(order_frame, text=data[col], width=20, font=("Consolas", 10), 
                                fg="#e8e8e8", bg="#2b2b2b", borderwidth=1, relief='ridge').grid(row=row, column=col, pady=5, padx=2)

            # Delete Button
            delete_but = tk.Button(
                order_frame, text="Delete", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
                command=lambda: delete_order_item(data[0])
            )
            delete_but.grid(row=row, column=4, padx=5)

    def delete_order_item(item) :  
        global money
        """Delete an item from the database."""

        res = messagebox.askquestion("Confirmation", "Do you want to delete this item?")

        if res == "yes" :
            print(item)
            mycursor.execute(f"select total_price from orders where name = '{item}'")
            money -= mycursor.fetchone()[0]
            mycursor.execute("delete from orders where name = '{}'".format(item))
            mydb.commit()
            list_category()

            mycursor.execute("select * from orders")
            if mycursor.fetchall() :
                open_order()

    # Create a new window for the order
    for widget in window.winfo_children() :
        widget.destroy()
        
    tk.Label(window, text="Your Order", font=("Consolas", 16), bg="#222222", fg="#e8e8e8").pack(pady=20)

    order_window = ctk.CTkScrollableFrame(window, width=window_width-100, height=400)
    order_window.pack()
    
    order_frame = tk.Frame(order_window, bg="#2b2b2b")
    order_frame.pack(pady=10)
    
    # Define the column headers
    headers = ["Name", "Quantity", "Price", "Total Price"] 

    # Add headers to the log frame
    for col in range(len(headers)):
        tk.Label(order_frame, text=headers[col], width=18, font=("Consolas", 12, "bold"), 
                 fg="#e8e8e8", bg="#333333", borderwidth=1, relief='ridge').grid(row=0, column=col, pady=5, padx=2)

    if rows:
        row = 1  # Start from row 1 to leave space for headers
        for record in rows:
            populate_order(record)
            row += 1

    # Display total amount to be paid
    tk.Label(window, text=f"Total Amount: ₹{money}", font=("Consolas", 14), fg="#E8E8E8", bg="#222222").place(x=100,y=window_height-50)

    # Hide Cart button
    tk.Button(
        window, cursor="hand2", text="Hide Order", command=lambda: list_category(),
        bg="#ffef00", fg="black", font=("Consolas", 12), activebackground="black", activeforeground="#E8E8E8"
    ).place(x=window_width-220, y=window_height-50)

    # Purchase button
    tk.Button(
        window, cursor="hand2", text="Purchase", command=lambda: pay_money(),
        bg="green", fg="white", font=("Consolas", 12), activebackground="black", activeforeground="#E8E8E8"
    ).place(x=window_width-320, y=window_height-50)

def admin_page():
    """Display Admin login page with username and password fields."""

    def toggle_passwd(field) :
        global show_passwd
        show_passwd = not show_passwd

        if show_passwd :
            field.config(show="")
            show_passwd_btn.config(text="Hide")
        else :
            field.config(show="*")
            show_passwd_btn.config(text="Show")
    
    # Clear the current frame
    for widget in window.winfo_children():
        widget.destroy()

    # Admin login frame
    login_frame = tk.Frame(window, bg="#222222")
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
        command=lambda: verify_admin_login(username_entry.get(), password_entry.get(), message_label), activebackground="black", activeforeground="#E8E8E8"
    )
    login_but.grid(row=2, column=0, columnspan=2, pady=10)

    # Back button
    back_but = tk.Button(
        window, text="Back", cursor="hand2", foreground="white", bg="#3eb7c1",
        font=("Consolas", 12), command=lambda: welcome_page(), activebackground="black", activeforeground="#E8E8E8"
    )
    back_but.place(x=600, y=600)

def verify_admin_login(username, password, message_label):
    """Function to verify admin login and handle UI accordingly."""
    # Simple placeholder credentials for demonstration
    admin_credentials = {"": ""}

    # Check if the credentials match
    if username in admin_credentials and admin_credentials[username] == password:
        message_label.config(text="Login successful!", fg="green")
        open_admin_dashboard()  # Proceed to the admin dashboard after successful login
    else:
        message_label.config(text="Invalid credentials. Please try again.", fg="#ff7b6f")

def open_admin_dashboard():
    """Display the admin dashboard after successful login."""
    # Clear the current frame
    for widget in window.winfo_children():
        widget.destroy()

    # Admin dashboard frame
    dashboard_frame = tk.Frame(window, bg="#222222")
    dashboard_frame.place(relx=0.5, rely=0.4, anchor="center")

    tk.Label(dashboard_frame, text="Welcome to the Admin Dashboard!", font=("Consolas", 14), bg="#222222", fg="#E8E8E8").pack(pady=20)
    
    # Manage Restaurant button
    manage_restaurant_but = tk.Button(
        dashboard_frame, text="Manage Restaurant", width=20, height=2, cursor="hand2",
        bg="#4CAF50", fg="white", font=("Consolas", 12, "bold"),
        command=lambda: manage_restaurant(), activebackground="black", activeforeground="#E8E8E8"
    )
    manage_restaurant_but.pack(pady=10)

    # Purchase Log button
    purchase_log_but = tk.Button(
        dashboard_frame, text="Purchase Log", width=20, height=2, cursor="hand2",
        bg="#2196F3", fg="white", font=("Consolas", 12, "bold"),
        command=lambda: view_purchase_log(), activebackground="black", activeforeground="#E8E8E8"
    )
    purchase_log_but.pack(pady=10)
    
    # Add any admin-specific functionality here (e.g., viewing orders, managing menu items)
    # Example: Log out button
    logout_but = tk.Button(
        dashboard_frame, text="Log Out", width=12, height=2, cursor="hand2",
        bg="#f44336", fg="white", font=("Consolas", 12, "bold"),
        command=lambda: welcome_page(), activebackground="black", activeforeground="#E8E8E8"
    )
    logout_but.pack(pady=20)

def manage_restaurant():
    """Function to manage the restaurant items with filters and editable fields."""
    # Clear the current frame
    for widget in window.winfo_children():
        widget.destroy()

    tk.Label(window, text="Manage Restaurant", font=("Consolas", 16), bg="#222222", fg="#E8E8E8").pack(pady=10)

    # Filter Frame
    filter_frame = tk.Frame(window, bg="#222222")
    filter_frame.pack(pady=10)

    # Category Filter
    tk.Label(filter_frame, text="Category:", font=("Consolas", 12), bg="#222222", fg="#E8E8E8").grid(row=0, column=0, padx=5)
    category_var = tk.StringVar()
    category_dropdown = tk.OptionMenu(filter_frame, category_var, *get_unique_values("Category"))
    category_dropdown.config(bg="#222222", fg="#E8E8E8", activebackground="black", activeforeground="#E8E8E8", font=("Consolas", 10))
    category_dropdown["menu"].config(bg="#222222", fg="#e8e8e8", font=("Consolas", 10))
    category_dropdown.grid(row=0, column=1, padx=5)

    # Type Filter
    tk.Label(filter_frame, text="Type:", font=("Consolas", 12), bg="#222222", fg="#E8E8E8").grid(row=0, column=2, padx=5)
    type_var = tk.StringVar()
    type_dropdown = tk.OptionMenu(filter_frame, type_var, *get_unique_values("Type"))
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
        command=lambda: filter_items(category_var.get(), type_var.get(), name_var.get()), activebackground="black", activeforeground="#E8E8E8"
    )
    search_but.grid(row=0, column=6, padx=10)

    # Cancel Button (Clear Filters)
    cancel_but = tk.Button(
        filter_frame, text="Clear", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 12),
        command=lambda: manage_restaurant(), activebackground="black", activeforeground="#E8E8E8"  # Reset the entire page
    )
    cancel_but.grid(row=0, column=7, padx=10)

    # Editable fields frame
    global item_fields_frame
    item_fields_frame = ctk.CTkScrollableFrame(window, width=window_width-200, height=400)
    item_fields_frame.pack(pady=20)

    # New Item Button
    create_item_but = tk.Button(
        window, text="Create New Item", cursor="hand2", bg="#4CAF50", fg="white", font=("Consolas", 12),
        command=lambda: create_new_item(), activebackground="black", activeforeground="#E8E8E8"
    )
    create_item_but.pack(pady=10)

    # Back Button
    back_but = tk.Button(
        window, text="Back to Dashboard", cursor="hand2", bg="#3eb7c1", fg="white", font=("Consolas", 12),
        command=lambda: open_admin_dashboard(), activebackground="black", activeforeground="#E8E8E8"
    )
    back_but.place(x=window_width-200,y=window_height-50)

def get_unique_values(column_name):
    mycursor.execute(f"SELECT DISTINCT {column_name} FROM food")
    return [row[0] for row in mycursor.fetchall()]

def filter_items(category, type_, name):
    """Filter items based on the selected category, type, and name."""
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

    mycursor.execute(query, params)
    items = mycursor.fetchall()

    # Clear previous results
    for widget in item_fields_frame.winfo_children():
        widget.destroy()

    if items:
        for item in items:
            create_editable_item_fields(item)
    else:
        tk.Label(item_fields_frame, text="No items found", font=("Consolas", 12), bg="#2b2b2b", fg="#e8e8e8").pack()

def create_editable_item_fields(item, is_new=False):
    """Create editable fields for an item."""
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
            command=lambda: [save_item(item_id, category_var.get(), type_var.get(), name_var.get(), price_var.get())]
        )
        save_but.grid(row=0, column=4, padx=4)
    else :
        tk.Button(
            frame, text="Create", cursor="hand2", bg="#4CAF50", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
            command=lambda: [create_item(category_var.get(), type_var.get(), name_var.get(), price_var.get())]
        ).grid(row=0, column=4, padx=4)

    # Delete Button
    delete_but = tk.Button(
        frame, text="Delete", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
        command=lambda: delete_item(item_id)
    )
    delete_but.grid(row=0, column=5, padx=5)

def create_new_item():
    """Create editable fields for adding a new item."""
    # Add new item with empty fields and reset view
    manage_restaurant()
    create_editable_item_fields((None, "", "", "", ""), is_new=True)
    mydb.commit()

def save_item(item_id, category, type_, name, price):
    """Save the changes made to an existing item or create a new item."""
 
    if not category or not type_ or not name or not price:
        messagebox.showerror('Error', "All fields must be filled out.")
        return 
    else:
        messagebox.showinfo("Success!", "Item has been successfully modified")   
    
    mycursor.execute(
        "UPDATE food SET Name=%s, Category=%s, Type=%s, Price=%s WHERE ID=%s",
        (name, category, type_, price, item_id)
    )

    mydb.commit()
    manage_restaurant()  # Reload the page after saving

def create_item(category, type_, name, price) :
    try :
        if round(float(price), 0) <= 0 :
            messagebox.showerror('Error', "Price must be greater than 0.")
            return
    except :
        messagebox.showerror('Error', "Price must be a number.")
        return
    
    mycursor.execute("select category, type, name from food")
    for i in mycursor.fetchall() :
        if category.lower() == i[0].lower() and type_.lower() == i[1].lower() and name.lower() == i[2].lower() :
            messagebox.showerror("Error", "Item already exists!")
            break
    else :
        mycursor.execute("insert into food (name, category, type, price) values('{}', '{}', '{}', {})".format(name.title(), category.title(), type_.title(), price))
        messagebox.showinfo("Success!", "Item has been successfully added")   
        mydb.commit()
        manage_restaurant()

def delete_item(item_id):
    """Delete an item from the database."""

    res = messagebox.askquestion("Confirmation", "Do you want to delete this item?")

    if res == "yes" :
        mycursor.execute("DELETE FROM food WHERE ID = %s", (item_id,))
        mydb.commit()
        manage_restaurant()  # Reload the page after deleting

def view_purchase_log():
    """Function to display the purchase log."""
    # Clear the current frame
    for widget in window.winfo_children():
        widget.destroy()

    tk.Label(window, text="Purchase Log", font=("Consolas", 16), bg="#222222", fg="#e8e8e8").pack(pady=20)

    log_frame = ctk.CTkScrollableFrame(window, width=window_width-200, height=400)
    log_frame.pack(pady=10)

    # Define the column headers
    headers = ["Name", "Quantity", "Total Amount", "Date"] 

    # Add headers to the log frame
    for col in range(len(headers)):
        tk.Label(log_frame, text=headers[col], width=18, font=("Consolas", 12, "bold"), 
                 fg="#e8e8e8", bg="#333333", borderwidth=1, relief='ridge').grid(row=0, column=col, pady=5, padx=2)

    # Fetch and display the log details from the database
    log_records = []
    mycursor.execute("SELECT * FROM logtable")
    log_records = mycursor.fetchall()

    if log_records:
        row = 1  # Start from row 1 to leave space for headers
        for record in log_records:
            for col in range(len(record)):
                tk.Label(log_frame, text=record[col], width=20, font=("Consolas", 10), 
                         fg="#e8e8e8", bg="#2b2b2b", borderwidth=1, relief='ridge').grid(row=row, column=col, pady=5, padx=2)
            row += 1

    # Example: Add button to go back to the dashboard
    back_but = tk.Button(
        window, text="Back to Dashboard", cursor="hand2", bg="#3eb7c1", fg="white", font=("Consolas", 12),
        command=lambda: open_admin_dashboard(), activebackground="black", activeforeground="#E8E8E8"
    )
    back_but.place(x=window_width-200, y=window_height-50)

    def clear_items():
        if log_records == [] :
            messagebox.showinfo("Empty", "No records to clear")
        else :
            res = messagebox.askquestion("Confirmation", "Do you want to clear all records?")
            if res == "yes" :
                mycursor.execute('DELETE FROM logtable')
                mydb.commit()
                view_purchase_log()
                messagebox.showinfo("Success", "All records have been cleared")

    clear_but = tk.Button(
        window, text="Clear", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 12),
        command=lambda: clear_items(), activebackground="black", activeforeground="#E8E8E8"
    )
    clear_but.pack(pady=10)
            
#Create a new database, if it does not exist
def createdb():
    """Create the database if it does not exist."""
    mycursor.execute("CREATE DATABASE IF NOT EXISTS restaurant")
    mycursor.execute("USE restaurant")

#Create a new table, if it does not exist
def createtable():
    """Create the food table if it does not exist."""
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS food (ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, Name VARCHAR(50) NOT NULL, "
        "Category VARCHAR(50), Type VARCHAR(50), Price INT)"
    )
    mycursor.execute("DELETE FROM food")  # Clear existing items

#Create a table to store items in order
def create_order_table():
    """Create the order table if it does not exist."""
    mycursor.execute("create table if not exists orders(Name varchar(50) primary key, qty int check(qty > 0), Price int, Total_Price int)")
    mycursor.execute("DELETE FROM orders")  # Clear existing items

#Create a table to log all purchases
def create_log_table():
    """Create the log table if it does not exist."""
    mycursor.execute("create table if not exists logtable(Name varchar(50) not null, qty int, Total_Price int, Log_Time datetime)")

#Add food items to the table to make it accessible
def insert_food_items(file_path):
    """Insert food items into the database from a CSV file."""
    with open(file_path, 'r') as food_items: #Read items from CSV file
        item_details = csv.reader(food_items)
        for row in item_details:
            try:
                mycursor.execute(
                    'INSERT INTO food VALUES (%s, %s, %s, %s, %s)',
                    (int(row[0]), row[1], row[2], row[3], int(row[4]))
                )
            except ValueError: #Ignore text based values
                continue

# Connect to MySQL
mydb = conn.connect(host="localhost", user="root", passwd="root")
if mydb.is_connected():
    print("Connection has been established!")
else:
    exit(-1)

mycursor = mydb.cursor()

# Create database and table
createdb()
createtable()
create_log_table()
create_order_table()

# Define the path for food items CSV
path = r"D:\Annamalai\Programming\Project 12\Restaurant Menu - Food Items.csv"

# Insert food items into the database
insert_food_items(path)
mycursor.execute("SET GLOBAL sql_mode=''")
mydb.commit()  # Make changes in MySQL

# Initialize main window
cat_but = {}  # Categories
item_but = {}  # Food items

money = 0

show_passwd = False

# Create main window
window_width = 900
window_height = 600
window = tk.Tk()
window.title("Restaurant Menu")
window.geometry(f"{window_width}x{window_height}")
window.configure(bg="#222222")
window.resizable(0,0)

# Load the welcome page initially
welcome_page()

# Run the application
window.mainloop()

# Close MySQL connection
mydb.close()