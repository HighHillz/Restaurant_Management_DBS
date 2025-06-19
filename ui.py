import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

import script

class BaseWindow:
    def __init__(self, width, height, window_title="", is_popup=False, base_window=None):
        self.width = width
        self.height = height
        self.title = window_title
        if is_popup:
            self.window = tk.Toplevel(base_window)
            self.window.grab_set()
        else:
            self.window = tk.Tk()
        self.window.title(self.title)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.configure(bg="#1e1e1e")
        self.window.resizable(False, False)

    def create_window(self):
        return self.window

    def rename_window_title(self, new_title):
        self.window.title(new_title)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def destroy_objects(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def destroy_self(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()

class Window(BaseWindow):
    def __init__(self, width, height, window_title=""):
        super().__init__(width, height, window_title, is_popup=False)

class PopupWindow(BaseWindow):
    def __init__(self, width, height, base_window, window_title=""):
        super().__init__(width, height, window_title, is_popup=True, base_window=base_window)

class HomePage:
    def __init__(self):
        main_window.rename_window_title("Restaurant")
        self.setup_ui()
    
    def setup_ui(self):
        """Display the welcome page with a Quit button."""
        # Clear the current frame
        main_window.destroy_objects()
        
        #Quit button
        tk.Button(
            main_window.window, text="Quit", cursor="hand2", foreground="white", bg="#f44336",
            font=("Consolas", 10), command=main_window.destroy_self,
            activebackground="black", activeforeground="#E8E8E8"
        ).place(x=10, y=10)

        welcome_frame = tk.Frame(main_window.window, bg="#1e1e1e")
        welcome_frame.place(relx=0.5, rely=0.4, anchor="center")

        #Title label    
        tk.Label(
            welcome_frame, text="Welcome to A2N Cafe",
            font=("Consolas", 24), bg="#1e1e1e", fg="#E8E8E8"
        ).pack(pady=50)

        # Admin button
        admin_but = tk.Button(
            welcome_frame, text="Admin", width=15, height=2, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 12, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda: LoginPage('Admin')
        )
        admin_but.pack(pady=10)

        # Customer button
        customer_but = tk.Button(
            welcome_frame, text="Customer", width=15, height=2, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 12, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda: LoginPage('Customer')
        )
        customer_but.pack(pady=10)
    
class LoginPage:
    def __init__(self, Type):
        self.Type = Type
        self.show_passwd = False
        self.accounts = script.Account(self.Type)
        main_window.rename_window_title(f"{self.Type}: Login")
        self.setup_login_ui()
    
    def setup_login_ui(self):
        # Clear the current frame
        main_window.destroy_objects()

        # Home button
        tk.Button(main_window.window, cursor="hand2", text="Home", bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=HomePage).place(x=10, y=10)

        login_frame = tk.Frame(main_window.window, bg="#1e1e1e")
        login_frame.place(relx=0.5, rely=0.4, anchor="center")

        #Username field
        tk.Label(login_frame, text="Username:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8").grid(row=0, column=0, pady=10)
        self.username_var = tk.StringVar()
        tk.Entry(login_frame, textvariable=self.username_var, font=("Consolas", 12), bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8").grid(row=0, column=1, columnspan=2, pady=10)
        
        #Phone field
        self.phone_label = tk.Label(login_frame, text="Phone:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8")
        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(login_frame, textvariable=self.phone_var, font=("Consolas", 12), bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8")
        
        #Email field
        self.email_label = tk.Label(login_frame, text="Email:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8")
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(login_frame, textvariable=self.email_var, font=("Consolas", 12), bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8")

        #Password field
        tk.Label(login_frame, text="Password:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8").grid(row=3, column=0, pady=10)
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(login_frame, textvariable=self.password_var, font=("Consolas", 12), show="*", bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8")
        password_entry.grid(row=3, column=1, columnspan=2, padx=10)

        #Show password button
        self.show_passwd_btn = tk.Button(
            login_frame, text="Show", width=5, height=1, cursor="hand2",
            bg="#393939", fg="white", font=("Consolas", 8),
            activebackground="black", activeforeground="#E8E8E8", command=lambda:self.toggle_passwd(password_entry)
        )
        self.show_passwd_btn.grid(row=3, column=3, padx=10)

        #Login button
        self.login_but = tk.Button(
            login_frame, text="Login", width=6, height=1, cursor="hand2",
            bg="green", fg="white", font=("Consolas", 11, "bold"),
            activebackground="black", activeforeground="#E8E8E8", command=lambda: self.verify_login(self.username_var.get(), self.password_var.get())
        )
        self.login_but.grid(row=4, column=1, pady=10)

        #Create Account button
        self.create_but = tk.Button(
            login_frame, text="New Account", width=12, height=1, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 11, "bold"), activebackground="black", activeforeground="#E8E8E8", command=self.setup_create_account_ui
        )
        self.create_but.grid(row=4, column=2, pady=10)

        #Error Message label
        self.message_label = tk.Label(login_frame, text="", font=("Consolas", 10), bg="#1e1e1e", anchor="center")
        self.message_label.grid(row=5, column=0, columnspan=4, pady=10)
        
    
    def verify_login(self, username, password):
        if self.accounts.username_exists(username):
            if self.accounts.verify_login(username, password):
                Dashboard(self.Type, username)
            else:
                self.message_label.config(text="Incorrect password. Please try again", fg="#ff7b6f")
        else:
            self.message_label.config(text=f"An account for {username} does not exist!", fg="#ff7b6f")
    
    def toggle_passwd(self, field):
        self.show_passwd = not self.show_passwd
        if self.show_passwd:
            field.config(show="")
            self.show_passwd_btn.config(text="Hide")
        else:
            field.config(show="*")
            self.show_passwd_btn.config(text="Show")
            
    def setup_create_account_ui(self):
        self.login_but.config(text="Create", command=lambda: self.create_account(self.username_var.get(), self.password_var.get(), self.phone_var.get(), self.email_var.get()))
        self.create_but.config(text="Back", command=lambda: self.setup_login_ui())
        self.username_var.set("")
        self.password_var.set("")
        self.message_label.config(text="")
        self.phone_label.grid(row=1, column=0, pady=10)
        self.phone_entry.grid(row=1, column=1, columnspan=2, pady=10)
        self.email_label.grid(row=2, column=0, pady=10)
        self.email_entry.grid(row=2, column=1, columnspan=2, pady=10)
    
    def create_account(self, username, password, phone, email):
        if not self.accounts.username_exists(username):
            if self.accounts.is_phone_valid(phone):
                if self.accounts.is_email_valid(email):
                    self.accounts.create_account(username, password, phone, email)
                    self.message_label.config(text=f"An account for {username} has been created!", fg="green")
                else:
                    self.message_label.config(text=f"Invalid email address!", fg="#ff7b6f")
            else:
                self.message_label.config(text=f"Invalid phone number!", fg="#ff7b6f")
        else:
            self.message_label.config(text=f"An account for {username} already exists!", fg="#ff7b6f")

class Dashboard:
    def __init__(self, Type, username):
        self.Type = Type
        self.username = script.Account(self.Type).get_account_detail(username, self.Type)[0]
        main_window.rename_window_title(f"{self.Type}: Dashboard")
        self.setup_ui()
    
    def setup_ui(self):
        main_window.destroy_objects()

        tk.Button(main_window.window, text="Profile", cursor="hand2",
            bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: ProfilePopup(self.Type, self.username)).place(x=main_window.get_width()-70, y=10)
        
        self.dashboard_frame = tk.Frame(main_window.window, bg="#1e1e1e")
        self.dashboard_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.dashboard_frame, text=f"Welcome {self.username}!", font=("Consolas", 16), bg="#1e1e1e", fg="#E8E8E8").pack(pady=20)

        self.customer_functions() if self.Type == 'Customer' else self.admin_functions()
    
    def customer_functions(self):
        order_page_but = tk.Button(
            self.dashboard_frame, text="Order Food", width=20, height=2, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 12, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda: OrderPage(self.username)
        )
        order_page_but.pack(pady=10)

        # Previous Orders button
        order_hist_but = tk.Button(
            self.dashboard_frame, text="Previous Orders", width=20, height=2, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 12, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda: HistoryPage(self.Type, self.username)
        )
        order_hist_but.pack(pady=10)
    
    def admin_functions(self):
        # Manage Restaurant button
        manage_restaurant_but = tk.Button(
            self.dashboard_frame, text="Menu Management", width=20, height=2, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 12, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda: MenuManagementPage(self.username)
        )
        manage_restaurant_but.pack(pady=10)

        # Previous Orders button
        order_hist_but = tk.Button(
            self.dashboard_frame, text="Previous Orders", width=20, height=2, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 12, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda: HistoryPage(self.Type, self.username)
        )
        order_hist_but.pack(pady=10)
        
        # Customers Book button
        customers_book_but = tk.Button(
            self.dashboard_frame, text="View Customers", width=20, height=2, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 12, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda: CustomerBookPage(self.Type, self.username)
        )
        customers_book_but.pack(pady=10)

        """ # Reports Generator button
        reports_but = tk.Button(
            self.dashboard_frame, text="Generate Report", width=20, height=2, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 12, "bold"),
            activebackground="black", activeforeground="#E8E8E8"
        )
        reports_but.pack(pady=10) """

class ProfilePopup:
    def __init__(self, Type, username):
        self.Type = Type
        self.username = username
        self.account = script.Account(self.Type)
        self.top = PopupWindow(300, 300, main_window.window, "")
        self.top.create_window()
        self.setup_ui()

    def setup_ui(self):
        self.top.destroy_objects()
        self.top.rename_window_title(f"Profile: {self.username}")

        # Add button to go back to the dashboard
        tk.Button(
            self.top.window, text="Close", cursor="hand2", bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: self.top.destroy_self()
        ).place(x=10, y=10)
        
        self.details_frame = tk.Frame(self.top.window, bg="#1e1e1e")
        self.details_frame.pack(anchor="w", pady=(50, 20), padx=5)
        
        self.panel_frame = tk.Frame(self.top.window, bg="#1e1e1e")
        self.panel_frame.pack()

        self.write_details()
        self.setup_settings_panel()
        #self.setup_function_frames()
    
    def write_details(self):
        details = self.account.get_account_detail(self.username, self.Type)

        tk.Label(self.details_frame, text=f"Username: {details[0]}", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8", anchor="w", justify="left").pack(anchor="w", fill="x")
        
        tk.Label(self.details_frame, text=f"Role: {self.Type}", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8", anchor="w", justify="left").pack(anchor="w", fill="x")
        
        tk.Label(self.details_frame, text=f"Phone: {details[3]}", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8", anchor="w", justify="left").pack(anchor="w", fill="x")
        
        tk.Label(self.details_frame, text=f"Email: {details[4]}", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8", anchor="w", justify="left").pack(anchor="w", fill="x")
    
    def setup_settings_panel(self):
        # Settings button
        tk.Button(
            self.panel_frame, text="Settings", width=10, height=1, cursor="hand2",
            bg="#393939", fg="white", font=("Consolas", 10, "bold"), activebackground="black", activeforeground="#E8E8E8", command=self.setup_function_frames
        ).grid(column=0, row=0, padx=(0, 5))

        # Log out button
        tk.Button(
            self.panel_frame, text="Logout", width=7, height=1, cursor="hand2",
            bg="#f44336", fg="white", font=("Consolas", 10, "bold"),
            command=lambda: LoginPage(self.Type), activebackground="black", activeforeground="#E8E8E8"
        ).grid(column=1, row=0, padx=(5, 0))
        
    def setup_function_frames(self):
        self.top.rename_window_title('Settings')
        self.top.destroy_objects()
        
        # Add button to go back to the dashboard
        tk.Button(
            self.top.window, text="Back", cursor="hand2", bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: self.setup_ui()
        ).place(x=10, y=10)
        
        self.account_frame = tk.Frame(self.top.window, bg="#1e1e1e")
        self.account_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Edit Account button
        tk.Button(
            self.account_frame, text="Edit Account", width=15, height=1, cursor="hand2",
            bg="teal", fg="white", font=("Consolas", 10, "bold"), activebackground="black", activeforeground="#E8E8E8", command=self.edit_ui
        ).pack(pady=5)
        
        # Delete Account button
        tk.Button(
            self.account_frame, text="Delete Account", width=15, height=1, cursor="hand2",
            bg="#f44336", fg="white", font=("Consolas", 10, "bold"), activebackground="black", activeforeground="#E8E8E8", command=self.delete_account
        ).pack(pady=5)
    
    def edit_ui(self):
        self.top.rename_window_title('Edit Account')
        self.top.destroy_objects()

        details = self.account.get_account_detail(self.username, self.Type)
        
        self.details_frame = tk.Frame(self.top.window, bg="#1e1e1e")
        self.details_frame.pack(anchor="w", pady=(50, 20), padx=5)
        
        self.panel_frame = tk.Frame(self.top.window, bg="#1e1e1e")
        self.panel_frame.pack()

        #Phone field
        tk.Label(self.details_frame, text="Phone:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8").grid(row=1, column=0, pady=10)
        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(self.details_frame, textvariable=self.phone_var, font=("Consolas", 12), bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8")
        self.phone_entry.grid(row=1, column=1, columnspan=2, pady=10)
        self.phone_var.set(details[3])
        
        #Email field
        tk.Label(self.details_frame, text="Email:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8").grid(row=2, column=0, pady=10)
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self.details_frame, textvariable=self.email_var, font=("Consolas", 12), bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8")
        self.email_entry.grid(row=2, column=1, columnspan=2, pady=10)
        self.email_var.set(details[4])

        #Password field
        tk.Label(self.details_frame, text="Password:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8").grid(row=3, column=0, pady=10)
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(self.details_frame, textvariable=self.password_var, font=("Consolas", 12), bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8")
        password_entry.grid(row=3, column=1, columnspan=2, padx=10)
        self.password_var.set(details[1])
    
        # Save button
        tk.Button(
            self.panel_frame, text="Save", width=7, height=1, cursor="hand2",
            bg="green", fg="white", font=("Consolas", 10, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda: self.edit_account_detail()
        ).grid(column=0, row=0, padx=(0, 5))

        # Cancel button
        tk.Button(
            self.panel_frame, text="Cancel", width=7, height=1, cursor="hand2",
            bg="#f44336", fg="white", font=("Consolas", 10, "bold"),
            command=self.setup_function_frames, activebackground="black", activeforeground="#E8E8E8"
        ).grid(column=1, row=0, padx=(5, 0))
    
    def edit_account_detail(self):
        res = messagebox.askquestion("Edit Account", "Do you want to change your account details?")

        if res == "yes":
            self.account.edit_account_detail(self.username, self.Type, self.password_var.get(), self.phone_var.get(), self.email_var.get())
            res = messagebox.showinfo("Success!", "Account has been successfully edited!")
            self.setup_ui()
    
    def delete_account(self):
        res = messagebox.askquestion("WARNING!", "Deleting this account will permenantly erase all information related to the account, and is an irreversible process. Do you want to continue?")

        if res == "yes":
            self.account.delete_account(self.username, self.Type)
            res = messagebox.showinfo("Success!", "Account has been successfully deleted!")
            HomePage()

class OrderPage:
    def __init__(self, username, order_class = ""):
        self.username = username
        self.order = script.Order(self.username) if not order_class else order_class
        main_window.rename_window_title('Menu')
        self.setup_ui()

    def setup_ui(self):
        main_window.destroy_objects()

        #Order button
        tk.Button(
            main_window.window, text="Show Order", cursor="hand2", foreground="white", bg="#393939",
            font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: OrderListPage(self.username, self.order)
        ).place(x=main_window.get_width()-120, y=main_window.get_height()-50)
        
        # Add button to go back to the dashboard
        tk.Button(
            main_window.window, text="Back to Dashboard", cursor="hand2", bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: Dashboard('Customer', self.username)
        ).place(x=10, y=10)

        self.list_categories()
    
    def list_categories(self):
        # Create a new frame for categories on the left side of the window
        cat_frame = ctk.CTkScrollableFrame(main_window.window, width=150, height=475, fg_color="transparent", scrollbar_fg_color="#272727")
        cat_frame.place(x=0, y=50)

        categories = self.order.get_categories()

        # Create a button for each category
        for category in categories:
            tk.Button(
                cat_frame, text=category[0], width=12, height=3, cursor="hand2",
                bg="teal", fg="white", font=("Consolas", 12, "bold"), activebackground="black", activeforeground="#E8E8E8", command=lambda i=category[0]: self.list_items(i)
            ).pack(pady=10)
    
    def list_items(self, category):
        # Create a new frame for items on the right side of the window
        items_frame = ctk.CTkScrollableFrame(main_window.window, width=500, height=400)
        items_frame.place(relx=0.6, rely=0.5, anchor="center")

        # Create a title label in the items frame
        tk.Label(items_frame, text=category, font=("Consolas", 14, "bold"), fg="#E8E8E8", bg="#2b2b2b").pack(pady=10)

        items = self.order.get_items(category)

        # Create a button for each item in the selected category
        for item in items:
            item_name, item_price = item
            tk.Button(
                items_frame, text=f"{item_name} - ₹{item_price}", width=30, height=2, cursor="hand2",
                bg="#216f75", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda name=item_name, price=item_price: QuantityPopup(name, price, self.order)
            ).pack(pady=5)

class QuantityPopup:
    def __init__(self, item, price, order_class):
        self.item_name = item
        self.price = price
        self.order = order_class
        self.setup_ui()
    
    def setup_ui(self):
        self.top = PopupWindow(300, 300, main_window.window, 'Quantity')
        self.top.create_window()
        
        tk.Label(self.top.window, text="Please enter the quantity", font=("Consolas", 12), fg="#E8E8E8", bg="#1e1e1e").pack(pady=20)
        tk.Message(self.top.window, width=300, text=f"Food item: {self.item_name}", font=("Consolas", 10), fg="#E8E8E8", bg="#1e1e1e").pack()
        tk.Message(self.top.window, width=200, text=f"Price per item: ₹{self.price}", font=("Consolas", 10), fg="#E8E8E8", bg="#1e1e1e").pack()

        #Input field to enter quantity
        quantity_entry = tk.Entry(self.top.window, bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12))
        quantity_entry.pack(pady=10)

        #Button to add item to order
        tk.Button(self.top.window, cursor="hand2", text="Add to order", bg="green", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: self.submit(quantity_entry.get())).place(x=70,y=150)

        #Button to close the quantity popup
        tk.Button(self.top.window, cursor="hand2", text="Cancel", command=lambda : self.top.destroy_self(), bg="#f44336", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8").place(x=170,y=150)

        self.top.run()

    def submit(self, qty) :
        try :
            qty = int(qty)
            if qty > 0:
                self.order.add_to_order(self.item_name, qty)
                self.top.destroy_self()
            else:
                messagebox.showerror('Error', "Please provide a value greater than 0")
        except ValueError:
            messagebox.showerror('Error', "Please provide an integer value")

class OrderListPage:
    def __init__(self, username, order_class):
        self.username = username
        self.order = order_class
        main_window.rename_window_title('Your Order')
        self.setup_ui()
    
    def setup_ui(self):
        main_window.destroy_objects()

        tk.Label(main_window.window, text="Your Order", font=("Consolas", 16), bg="#1e1e1e", fg="#e8e8e8").pack(pady=(50, 20))

        order_window = ctk.CTkScrollableFrame(main_window.window, width=main_window.get_width()-100, height=400)
        order_window.pack()
        
        self.order_frame = tk.Frame(order_window, bg="#2b2b2b")
        self.order_frame.pack(pady=10)
        
        self.populate_order()

        # Display total amount to be paid
        tk.Label(main_window.window, text=f"Total Amount: ₹{self.order.get_total_amount()}", font=("Consolas", 14), fg="#E8E8E8", bg="#1e1e1e").place(x=40,y=main_window.get_height()-50)

        # Hide Cart button
        tk.Button(
            main_window.window, cursor="hand2", text="Hide Order", command=lambda: OrderPage(self.username, self.order),
            bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8"
        ).place(x=main_window.get_width()-120, y=main_window.get_height()-50)

        # Purchase button
        tk.Button(
            main_window.window, cursor="hand2", text="Purchase", command=lambda: PaymentPopup(self.username, self.order),
            bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8"
        ).place(x=main_window.get_width()-200, y=main_window.get_height()-50)
    
    def populate_order(self):
        for widget in self.order_frame.winfo_children():
            widget.destroy()

        # Define the column headers
        headers = ["Name", "Quantity", "Price", "Total Price"] 

        # Add headers to the log frame
        for col in range(len(headers)):
            tk.Label(self.order_frame, text=headers[col], width=18, font=("Consolas", 12, "bold"), 
                    fg="#e8e8e8", bg="#333333", borderwidth=1, relief='ridge').grid(row=0, column=col, pady=5, padx=2)
        
        if self.order.get_order_list():
            row = 1  # Start from row 1 to leave space for headers
            for record in self.order.get_order_list().items():
                for col in range(len(headers)):
                    curr_price = self.order.get_item_price(record[0])
                    l = [record[0], record[1], curr_price, curr_price * record[1]]
                    tk.Label(self.order_frame, text=l[col], width=20, font=("Consolas", 10), fg="#e8e8e8", bg="#2b2b2b", borderwidth=1, relief='ridge').grid(row=row, column=col, pady=5, padx=2)

                    # Delete Button
                    tk.Button(
                        self.order_frame, text="Delete", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 8), activebackground="black", activeforeground="#E8E8E8", command=lambda i=record[0]: self.delete_item(i)
                    ).grid(row=row, column=4, padx=5)
                row += 1

    def delete_item(self, item):
        res = messagebox.askquestion("Confirmation", "Do you want to delete this item?")
        if res == "yes" :
            self.order.delete_item(item)
            self.populate_order()

class PaymentPopup:
    def __init__(self, username, order_class):
        self.username = username
        self.order = order_class
        self.setup_ui()
    
    def setup_ui(self):
        if self.order.get_order_list():
            self.payPage = PopupWindow(300, 200, main_window.window, 'Confirm Payment')
            self.payPage.create_window()

            # Display amount to be paid
            tk.Message(self.payPage.window, width=200, text=f"Amount to pay: ₹{self.order.get_total_amount()}", font=('Consolas', 10), fg="#E8E8E8", bg="#1e1e1e").pack(pady=10)
            
            # Pay button
            tk.Button(
                self.payPage.window, cursor="hand2", text="Pay", command=lambda: self.complete_payment(),
                bg="green", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8"
            ).pack(pady=10)

            self.payPage.run()
        else:
            messagebox.showerror('Error', 'Your order list is empty!')
    
    def complete_payment(self):
        self.payPage.destroy_objects()
        self.order.update_purchase()

        tk.Label(self.payPage.window, text="Payment successful!", fg="#E8E8E8", bg="#1e1e1e", font=("Consolas", 12)).pack(pady=50)

        tk.Button(
            self.payPage.window, text="Okay", command=self.go_back,
            font=("Consolas", 10), bg="green", fg="white", cursor="hand2", activebackground="black", activeforeground="#E8E8E8"
        ).pack(pady=10)
    
    def go_back(self):
        OrderPage(self.username)
        self.payPage.destroy_self()

class HistoryPage:
    def __init__(self, Type, username):
        self.username = username
        self.Type = Type
        self.history = script.History(self.Type)
        main_window.rename_window_title(f'Previous Orders')
        self.setup_ui()
    
    def setup_ui(self):
        main_window.destroy_objects()

        # Add button to go back to the dashboard
        tk.Button(
            main_window.window, text="Back to Dashboard", cursor="hand2", bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: Dashboard(self.Type, self.username)
        ).place(x=10, y=10)

        # Title label below the button
        tk.Label(main_window.window, text="Previous Orders", font=("Consolas", 16), bg="#1e1e1e", fg="#e8e8e8").pack(pady=(50, 20))

        log_window = ctk.CTkScrollableFrame(main_window.window, width=main_window.get_width()-150, height=400)
        log_window.pack()

        self.log_frame = tk.Frame(log_window, bg="#2b2b2b")
        self.log_frame.pack(pady=10)

        # Define the column headers
        headers = ["Item", "Quantity", "Total Amount", "Date"] 

        headers.insert(0, "Username") if self.Type == 'Admin' else 0

        # Add headers to the log frame
        for col in range(len(headers)):
            tk.Label(self.log_frame, text=headers[col], width=18, font=("Consolas", 12, "bold"), 
                    fg="#e8e8e8", bg="#333333", borderwidth=1, relief='ridge').grid(row=0, column=col, pady=5, padx=2)
        
        self.create_hist_table(self.username if self.Type == 'Customer' else "")
        
    def create_hist_table(self, username):
        log_records = self.history.fetch_records(username)

        row = 1  # Start from row 1 to leave space for headers
        for record in log_records:
            for col in range(len(record)):
                tk.Label(self.log_frame, text=record[col], width=20, font=("Consolas", 10), 
                        fg="#e8e8e8", bg="#2b2b2b", borderwidth=1, relief='ridge').grid(row=row, column=col, pady=5, padx=2)
            row += 1

class MenuManagementPage:
    def __init__(self, username):
        self.menu = script.Menu()
        self.username = username
        main_window.rename_window_title('Menu Management')
        self.setup_ui()
    
    def setup_ui(self):
        main_window.destroy_objects()
        
        # Add button to go back to the dashboard
        tk.Button(
            main_window.window, text="Back to Dashboard", cursor="hand2", bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: Dashboard('Admin', self.username)
        ).place(x=10, y=10)

        tk.Label(main_window.window, text="Menu Management", font=("Consolas", 16), bg="#1e1e1e", fg="#E8E8E8").pack(pady=(50, 20))

        # Filter Frame
        self.filter_frame = tk.Frame(main_window.window, bg="#1e1e1e")
        self.filter_frame.pack(pady=10)

        self.create_filters_panel()
        self.create_menu_screen()
        
        # New Item Button
        create_item_but = tk.Button(
            main_window.window, text="Create New Item", cursor="hand2", bg="green", fg="white", font=("Consolas", 10),
            command=lambda: self.new_item_fields(), activebackground="black", activeforeground="#E8E8E8"
        )
        create_item_but.place(x=main_window.get_width()-155, y=main_window.get_height()-50)
    
    def create_filters_panel(self):
        for widget in self.filter_frame.winfo_children():
            widget.destroy()
            
        # Category Filter
        tk.Label(self.filter_frame, text="Category:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8").grid(row=0, column=0, padx=5)
        self.category_var = tk.StringVar()
        category_dropdown = tk.OptionMenu(self.filter_frame, self.category_var, *self.menu.get_unique_values("Category"))
        category_dropdown.config(bg="#1e1e1e", fg="#E8E8E8", activebackground="black", activeforeground="#E8E8E8", font=("Consolas", 10))
        category_dropdown["menu"].config(bg="#1e1e1e", fg="#e8e8e8", font=("Consolas", 10))
        category_dropdown.grid(row=0, column=1, padx=5)
        
        # Type Filter
        tk.Label(self.filter_frame, text="Type:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8").grid(row=0, column=2, padx=5)
        self.type_var = tk.StringVar()
        type_dropdown = tk.OptionMenu(self.filter_frame, self.type_var, *self.menu.get_unique_values("Type"))
        type_dropdown.config(cursor="hand2", bg="#222222", fg="#E8E8E8", activebackground="black", activeforeground="#E8E8E8", font=("Consolas", 10))
        type_dropdown["menu"].config(bg="#222222", fg="#e8e8e8", font=("Consolas", 10))
        type_dropdown.grid(row=0, column=3, padx=5)
        
        # Name Filter
        tk.Label(self.filter_frame, text="Name:", font=("Consolas", 12), bg="#1e1e1e", fg="#E8E8E8").grid(row=0, column=4, padx=5)
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(self.filter_frame, textvariable=self.name_var, bg="#222222", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12))
        name_entry.grid(row=0, column=5, padx=5)

        # Search by filter Button
        search_but = tk.Button(
            self.filter_frame, text="Search", cursor="hand2", bg="green", fg="white", font=("Consolas", 12),
            command=lambda: self.filter_items(self.category_var.get(), self.type_var.get(), self.name_var.get()), activebackground="black", activeforeground="#E8E8E8"
        )
        search_but.grid(row=0, column=6, padx=10)

        # Cancel Button (Clear Filters)
        cancel_but = tk.Button(
            self.filter_frame, text="Clear", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 12),
            command=lambda: self.reset_filters(), activebackground="black", activeforeground="#E8E8E8"  # Reset the entire page
        )
        cancel_but.grid(row=0, column=7, padx=10)
    
    def reset_filters(self):
        self.category_var.set("")
        self.type_var.set("")
        self.name_var.set("")
    
    def create_menu_screen(self):
        # Editable fields frame
        self.item_fields_frame = ctk.CTkScrollableFrame(main_window.window, width=main_window.get_width()-100, height=350)
        self.item_fields_frame.pack(pady=20)
    
    def new_item_fields(self):
        # Add new item with empty fields and reset view
        self.reset_filters()
        for widget in self.item_fields_frame.winfo_children():
            widget.destroy()
        self.create_editable_item_fields((None, "", "", "", ""), is_new=True)
    
    def filter_items(self, category, type_, name):
        items = self.menu.get_filtered_items(category, type_, name)

        # Clear previous results
        for widget in self.item_fields_frame.winfo_children():
            widget.destroy()
            
        if items:
            for item in items:
                self.create_editable_item_fields(item)
        else:
            tk.Label(self.item_fields_frame, text="No items found", font=("Consolas", 12), bg="#2b2b2b", fg="#e8e8e8").pack()
    
    def create_editable_item_fields(self, item, is_new=False):
        item_id, item_name, item_category, item_type, item_price = item

        # Check if the header already exists before creating
        if not self.item_fields_frame.winfo_children():
            header_frame = tk.Frame(self.item_fields_frame, bg="#2b2b2b")
            header_frame.pack(pady=5, anchor="n")

            # Add column headers
            headers = ["Category", "Type", "Name", "Price"]
            for col, text in enumerate(headers):
                tk.Label(header_frame, text=text, bg="#2b2b2b", fg="#E8E8E8", font=("Consolas", 10), width=10).grid(row=0, column=col, padx=10)

            tk.Label(header_frame, bg="#2b2b2b", width=8).grid(row=0, column=4)
            tk.Label(header_frame, bg="#2b2b2b", width=8).grid(row=0, column=5)

        # Frame for editable fields
        frame = tk.Frame(self.item_fields_frame, bg="#2b2b2b")
        frame.pack(pady=5)

        # Editable fields for category, type, name, and price
        category_var = tk.StringVar(value=item_category)
        tk.Entry(frame, textvariable=category_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 10), width=12).grid(row=0, column=0, padx=5)

        type_var = tk.StringVar(value=item_type)
        tk.Entry(frame, textvariable=type_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 10), width=12).grid(row=0, column=1, padx=5)

        name_var = tk.StringVar(value=item_name)
        tk.Entry(frame, textvariable=name_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 10), width=12).grid(row=0, column=2, padx=5)

        price_var = tk.StringVar(value=item_price)
        tk.Entry(frame, textvariable=price_var, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 10), width=12).grid(row=0, column=3, padx=5)

        # Save Button
        if not is_new :
            tk.Button(
                frame, text="Save", cursor="hand2", bg="green", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
                command=lambda: self.save_item(item_id, category_var.get(), type_var.get(), name_var.get(), price_var.get())
            ).grid(row=0, column=4, padx=4)

            # Delete Button
            tk.Button(
                frame, text="Delete", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
                command=lambda: self.delete_item(item_id)
            ).grid(row=0, column=5, padx=5)
        else :
            tk.Button(
                frame, text="Create", cursor="hand2", bg="green", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
                command=lambda: self.create_item(category_var.get(), type_var.get(), name_var.get(), price_var.get())
            ).grid(row=0, column=4, padx=4)
            
            tk.Button(
                frame, text="Cancel", cursor="hand2", bg="#f44336", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8",
                command=self.cancel_creation
            ).grid(row=0, column=5, padx=5)
        
    def cancel_creation(self):
        res = messagebox.askquestion("Confirmation", "Do you want to cancel creation?")
        if res == "yes" :
            for widget in self.item_fields_frame.winfo_children():
                widget.destroy()

    def save_item(self, item_id, category, type_, name, price):
        if not category or not type_ or not name or not price:
            messagebox.showerror('Error', "All fields must be filled out.")
        else:
            try :
                if round(float(price), 0) <= 0 :
                    messagebox.showerror('Error', "Price must be greater than 0.")
                    return
            except :
                messagebox.showerror('Error', "Price must be a number.")
                return
            self.menu.save_item_sql(item_id, category, type_, name, price)
            messagebox.showinfo("Success!", "Item has been successfully modified")
    
    def create_item(self, category, type_, name, price) :
        if not category or not type_ or not name or not price:
            messagebox.showerror('Error', "All fields must be filled out.")
            return
        
        try :
            if round(float(price), 0) <= 0 :
                messagebox.showerror('Error', "Price must be greater than 0.")
                return
        except :
            messagebox.showerror('Error', "Price must be a number.")
            return
        
        if not self.menu.create_item_sql(category, type_, name, price):
            messagebox.showerror("Error", "Item already exists!")
        else:
            messagebox.showinfo("Success!", "Item has been successfully added") 
            for widget in self.item_fields_frame.winfo_children():
                widget.destroy()
            self.create_filters_panel()
            
    def delete_item(self, item_id):
        res = messagebox.askquestion("Confirmation", "Do you want to delete this item?")
        if res == "yes" :
            self.menu.delete_item_sql(item_id)
            self.filter_items(self.category_var.get(), self.type_var.get(), self.name_var.get())

class CustomerBookPage:
    def __init__(self, Type, username):
        self.Type = Type
        self.username = username
        self.accounts = script.Account(self.Type)
        main_window.rename_window_title('Customer Book')
        self.setup_ui()
    
    def setup_ui(self):
        main_window.destroy_objects()

        # Add button to go back to the dashboard
        tk.Button(
            main_window.window, text="Back to Dashboard", cursor="hand2", bg="#393939", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8", command=lambda: Dashboard(self.Type, self.username)
        ).place(x=10, y=10)

        # Title label below the button
        tk.Label(main_window.window, text="Customer Book", font=("Consolas", 16), bg="#1e1e1e", fg="#e8e8e8").pack(pady=(50, 20))

        log_window = ctk.CTkScrollableFrame(main_window.window, width=main_window.get_width()-150, height=400)
        log_window.pack()

        self.log_frame = tk.Frame(log_window, bg="#2b2b2b")
        self.log_frame.pack(pady=10)

        # Define the column headers
        headers = ["Username", "Phone", "Email", "Created"] 

        # Add headers to the log frame
        for col in range(len(headers)):
            tk.Label(self.log_frame, text=headers[col], width=18, font=("Consolas", 12, "bold"), 
                    fg="#e8e8e8", bg="#333333", borderwidth=1, relief='ridge').grid(row=0, column=col, pady=5, padx=2)
        
        self.create_view_table(self.username if self.Type == 'Customer' else "")
        
    def create_view_table(self, username):
        log_records = self.accounts.get_customer_details()

        row = 1  # Start from row 1 to leave space for headers
        for record in log_records:
            for col in range(len(record)):
                tk.Label(self.log_frame, text=record[col], width=20, font=("Consolas", 10), 
                        fg="#e8e8e8", bg="#2b2b2b", borderwidth=1, relief='ridge').grid(row=row, column=col, pady=5, padx=2)
            row += 1

if __name__ == "__main__":
    script.Database().create_db('Restaurant')
    db = script.Database('Restaurant')
    db.create_tables()
    db.create_menu()
    main_window = Window(1000, 600)
    main_window.create_window()
    HomePage()
    main_window.run()
    db.close_database()
