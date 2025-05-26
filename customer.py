import tkinter as tk 
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector as conn

class UI:
    def __init__(self, window, window_dim):
        self.window = window
        self.window_width, self.window_height = window_dim
        self.__money = 0
    
    def connect_db(self):
        self.mydb = conn.connect(host="localhost", user="root", passwd="root", database="restaurant")
        if self.mydb.is_connected():
            print(f"Connection with {__name__} has been established!")
        else:
            exit(-1)

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT order_id FROM logtable")
        self.order_id = max([row[0] for row in self.mycursor.fetchall()] or [0]) + 1

    def list_category(self):
        # Clear any existing widgets on the window
        for widget in self.window.winfo_children():
            widget.destroy()
            
        #Order button
        order_but = tk.Button(
            self.window, text="Show Order", cursor="hand2", foreground="black", bg="#ffef00",
            font=("Consolas", 12), command=lambda: self.open_order(), activebackground="black", activeforeground="#E8E8E8"
        )
        order_but.place(x=self.window_width-220, y=self.window_height-50)
        
        # Quit button
        quit_but = tk.Button(
            self.window, text="Quit", cursor="hand2", foreground="white", bg="#f44336",
            font=("Consolas", 12), command=lambda: self.window.destroy(), activebackground="black", activeforeground="#E8E8E8"
        )
        quit_but.place(x=self.window_width-100, y=self.window_height-50)
        
        # Create a new frame for categories on the left side of the window
        cat_frame = ctk.CTkScrollableFrame(self.window, width=150, height=500, fg_color="transparent", scrollbar_fg_color="#272727")
        cat_frame.place(relx=0, rely=0)

        # Query categories from the database
        self.mycursor.execute("SELECT DISTINCT category FROM food")
        categories = self.mycursor.fetchall()

        cat_but = {}  # Dictionary to hold buttons

        # Create a button for each category
        for category in categories:
            cat = category[0]
            cat_but[cat] = tk.Button(
                cat_frame, text=cat, width=12, height=3, cursor="hand2",
                bg="#3eb7c1", fg="white", font=("Consolas", 12, "bold"),
                command=lambda m=cat: self.list_items(m), activebackground="black", activeforeground="#E8E8E8"
            )
            cat_but[cat].pack(pady=10)  # Arrange buttons vertically with padding

    def list_items(self, category):
        # Create a new frame for items on the right side of the window
        items_frame = ctk.CTkScrollableFrame(self.window, width=500, height=400)
        items_frame.place(relx=0.6, rely=0.4, anchor="center")

        # Fetch items from the database for the selected category
        items = []
        self.mycursor.execute("SELECT Name, Price FROM food WHERE category = %s", (category,))
        items = self.mycursor.fetchall()

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
                    command=lambda m=item_name: self.open_popup(m), activebackground="black", activeforeground="#E8E8E8"
                )
                item_but[item_name].pack(pady=5)
        else:
            # If no items found, display a message
            tk.Label(items_frame, text="No items available", font=("Consolas", 12), fg="#E8E8E8", bg="#2b2b2b").pack(pady=20)

    def open_popup(self, item_name):
        def submit() :
            i = quantity_entry.get()
            try :
                z = int(i)
                self.mycursor.execute("select name from orders where name = '%s'" %(item_name))
                r = self.mycursor.fetchone()
                #Statements to add to order
                if r :
                    self.mycursor.execute("update orders set qty=qty+%s where name = '%s'" %(z, item_name))
                    self.mycursor.execute("update orders set total_price=total_price+%s where name = '%s'" %(price*z, item_name))
                else :
                    self.mycursor.execute("insert into orders values('%s', %s, %s, %s)" %(item_name, z, price, price*z))
                self.__money += price*z
                self.mydb.commit()
                top.destroy()
            except ValueError:
                messagebox.showerror('Error', "Please provide an integer value")
            except conn.errors.DatabaseError :
                messagebox.showerror('Error', "Please provide a value greater than 0")
        
        self.mycursor.execute("SELECT Price FROM food WHERE Name = '%s'" %(item_name,))
        price = self.mycursor.fetchall()[0][0]

        top = tk.Toplevel(self.window)
        top.geometry("300x300")
        top.config(bg="#222222")
        top.grab_set()
        top.resizable(0,0)
        top.title("Quantity")

        tk.Label(top, text="Please enter the quantity", font=("Consolas", 12), fg="#E8E8E8", bg="#222222").pack(pady=20)
        tk.Message(top, width=300, text=f"Food item: {item_name}", font=("Consolas", 10), fg="#E8E8E8", bg="#222222").pack()
        tk.Message(top, width=200, text=f"Price per item: ₹{price}", font=("Consolas", 10), fg="#E8E8E8", bg="#222222").pack()

        quantity_entry = tk.Entry(top, bg="#414141", fg="#E8E8E8", insertbackground="#E8E8E8", font=("Consolas", 12))
        quantity_entry.pack(pady=10)

        tk.Button(top, cursor="hand2", text="Add to order", command=lambda : submit(), bg="#4CAF50", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8").place(x=70,y=150)
        tk.Button(top, cursor="hand2", text="Cancel", command=lambda : top.destroy(), bg="#f44336", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8").place(x=170,y=150)

    def open_order(self):
        # Check if order is empty and show a message
        self.mycursor.execute("select * from orders")
        rows = self.mycursor.fetchall()

        if not rows:
            empty_order_message = tk.Toplevel(self.window)
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
            payPage = tk.Toplevel(order_window)
            payPage.resizable(0,0)
            payPage.geometry("300x200")
            payPage.config(bg="#222222")
            payPage.grab_set()

            # Display amount to be paid
            tk.Message(payPage, width=200, text=f"Amount to pay: ₹{self.__money}", fg="#E8E8E8", bg="#222222").place(x=70, y=50)
            
            # Pay button
            tk.Button(
                payPage, cursor="hand2", text="Pay", command=lambda: complete_payment(payPage),
                bg="#4CAF50", fg="white", font=("Consolas", 10), activebackground="black", activeforeground="#E8E8E8"
            ).place(x=110, y=100)

        def complete_payment(payPage):
            for i in rows:
                self.mycursor.execute("Insert into logtable values({}, '{}', {}, {},NOW())".format(self.order_id, i[0], i[1], i[3]))
            self.mycursor.execute("delete from orders")
            self.__money = 0     # Reset the self.__money variable
            self.order_id += 1
            payPage.destroy()  # Close the payment page
            order_window.destroy()  # Close the order window
            self.list_category() # Goes back to menu for the next user
            self.mydb.commit()
        
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
            res = messagebox.askquestion("Confirmation", "Do you want to delete this item?")

            if res == "yes" :
                print(item)
                self.mycursor.execute(f"select total_price from orders where name = '{item}'")
                self.__money -= self.mycursor.fetchone()[0]
                self.mycursor.execute("delete from orders where name = '{}'".format(item))
                self.mydb.commit()
                self.list_category()

                self.mycursor.execute("select * from orders")
                if self.mycursor.fetchall() :
                    self.open_order()

        # Create a new window for the order
        for widget in self.window.winfo_children() :
            widget.destroy()
            
        tk.Label(self.window, text="Your Order", font=("Consolas", 16), bg="#222222", fg="#e8e8e8").pack(pady=20)

        order_window = ctk.CTkScrollableFrame(self.window, width=self.window_width-100, height=400)
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
        tk.Label(self.window, text=f"Total Amount: ₹{self.__money}", font=("Consolas", 14), fg="#E8E8E8", bg="#222222").place(x=100,y=self.window_height-50)

        # Hide Cart button
        tk.Button(
            self.window, cursor="hand2", text="Hide Order", command=lambda: self.list_category(),
            bg="#ffef00", fg="black", font=("Consolas", 12), activebackground="black", activeforeground="#E8E8E8"
        ).place(x=self.window_width-220, y=self.window_height-50)

        # Purchase button
        tk.Button(
            self.window, cursor="hand2", text="Purchase", command=lambda: pay_money(),
            bg="green", fg="white", font=("Consolas", 12), activebackground="black", activeforeground="#E8E8E8"
        ).place(x=self.window_width-320, y=self.window_height-50)
    
    def establish(self):
        self.connect_db()
        self.list_category()