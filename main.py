import tkinter as tk 
import mysql.connector as conn
import csv

import customer
import admin


class Restaurant:

    ## Small Methods

    def conntect_to_sql(self):
        # Connect to MySQL
        self.mydb = conn.connect(host="localhost", user="root", passwd="root")
        if self.mydb.is_connected():
            print(f"Connection with {__name__} has been established!")
        else:
            exit(-1)
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SET SESSION sql_mode=''")
        self.mydb.commit()

    def createdb(self):
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS restaurant")
        self.mycursor.execute("USE restaurant")

    def createtable(self):
        self.mycursor.execute(
            "CREATE TABLE IF NOT EXISTS food (ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL, Name VARCHAR(50) NOT NULL, "
            "Category VARCHAR(50), Type VARCHAR(50), Price INT)"
        )
        self.mycursor.execute("DELETE FROM food")  # Clear existing items

    def create_order_table(self):
        self.mycursor.execute("create table if not exists orders(Name varchar(50) primary key, qty int check(qty > 0), Price int, Total_Price int)")
        self.mycursor.execute("DELETE FROM orders")  # Clear existing items

    def create_log_table(self):
        self.mycursor.execute("create table if not exists logtable(order_id int, Name varchar(50) not null, qty int, Total_Price int, Log_Time datetime)")

    #Add food items to the table to make it accessible
    def insert_food_items(self, file_path):
        """Insert food items into the database from a CSV file."""
        with open(file_path, 'r') as food_items: #Read items from CSV file
            item_details = csv.reader(food_items)
            for row in item_details:
                try:
                    self.mycursor.execute(
                        'INSERT INTO food VALUES (%s, %s, %s, %s, %s)',
                        (int(row[0]), row[1], row[2], row[3], int(row[4]))
                    )
                except ValueError: #Ignore text based values
                    continue
            self.mydb.commit()
    
    ## Sub Methods

    def setup_sql_database(self):
        self.conntect_to_sql()
        self.createdb()
        self.createtable()
        self.create_log_table()
        self.create_order_table()
    
    def create_menu(self):
        path = r"Restaurant Menu - Food Items.csv"
        self.insert_food_items(path)
    
    def create_ui(self):
        # Create main window
        self.window_dim = [1000, 600]
        self.window = tk.Tk()
        self.window.title("Restaurant Menu")
        self.window.geometry(f"{self.window_dim[0]}x{self.window_dim[1]}")
        self.window.configure(bg="#222222")
        self.window.resizable(0,0)
        self.welcome_page()
        self.window.mainloop()
        self.mydb.close()

    def welcome_page(self):
        """Display the welcome page with two buttons: Admin and Customer."""

        for widget in self.window.winfo_children() :
            widget.destroy()
        
        # Quit button
        quit_but = tk.Button(
            self.window, text="Quit", cursor="hand2", foreground="white", bg="#f44336",
            font=("Consolas", 12), command=lambda: self.window.destroy(), activebackground="black", activeforeground="#E8E8E8"
        )
        quit_but.place(x=self.window_dim[0]-100, y=self.window_dim[1]-50)

        welcome_frame = tk.Frame(self.window, bg="#222222")
        welcome_frame.place(relx=0.5, rely=0.4, anchor="center")
            
        # Window Title
        tk.Label(welcome_frame, text="Welcome to A2N Cafe", font=("Consolas", 24), bg="#222222", fg="#E8E8E8").pack(pady=50)

        # Admin button
        admin_but = tk.Button(
            welcome_frame, text="Admin", width=15, height=2, cursor="hand2",
            bg="#3eb7c1", fg="white", font=("Consolas", 12, "bold"),
            command=lambda: admin.UI(self.window, self.window_dim).establish(), activebackground="black", activeforeground="#E8E8E8"
        )
        admin_but.pack(pady=10)

        # Customer button
        customer_but = tk.Button(
            welcome_frame, text="Customer", width=15, height=2, cursor="hand2",
            bg="#3eb7c1", fg="white", font=("Consolas", 12, "bold"),
            command=lambda: customer.UI(self.window, self.window_dim).establish(), activebackground="black", activeforeground="#E8E8E8"
        )
        customer_but.pack(pady=10)

    ## Main Methods

    def open(self):
        self.setup_sql_database()
        self.create_menu()
        self.create_ui()

if __name__ == "__main__":
    Restaurant().open()