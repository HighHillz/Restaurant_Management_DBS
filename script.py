import mysql.connector as conn
import csv

class Database:
    def __init__(self, database = ""):
        self.connect_to_mysql(database)
    
    def connect_to_mysql(self, db):
        # Connect to MySQL
        if db:
            self.mydb = conn.connect(host="localhost", user="root", passwd="root", database = db)
        else:
            self.mydb = conn.connect(host="localhost", user="root", passwd="root")
        if not self.mydb.is_connected():
            exit(-1)
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SET SESSION sql_mode=''")
        self.mydb.commit()

    def create_db(self, database):
        self.mycursor.execute("create database if not exists {}".format(database))
        self.mycursor.execute("use {}".format(database))
        
    def createtable(self):
        self.mycursor.execute(
            "CREATE TABLE IF NOT EXISTS food (ID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(50) NOT NULL, "
            "Category VARCHAR(50), Type VARCHAR(50), Price INT)"
        )

    def create_log_table(self):
        self.mycursor.execute("create table if not exists logtable(username varchar(30), Name varchar(50) not null, qty int, Total_Price int, Log_Time datetime)")

    def create_account_table(self):
        self.mycursor.execute("create table if not exists accounts(username varchar(30), password varchar(30), type varchar(20), phone char(10), email varchar(30), created datetime)")
            
    def create_tables(self):
        self.createtable()
        self.create_log_table()
        self.create_account_table()
    
    def close_database(self):
        self.mydb.close()
        
    #Add food items to the table to make it accessible
    def insert_food_items(self, file_path):
        """Insert food items into the database from a CSV file."""
        self.mycursor.execute("select * from food")
        if self.mycursor.fetchall():
            return
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
        
    def create_menu(self):
        path = r"Restaurant Menu - Food Items.csv"
        self.insert_food_items(path)

class Account(Database):
    def __init__(self, Type):
        super().__init__('Restaurant')
        self.Type = Type

    def username_exists(self, username):
        self.mycursor.execute("SELECT username FROM accounts WHERE username = %s AND type = %s", (username, self.Type))
        return bool(self.mycursor.fetchall())

    def create_account(self, username, password, phone, email):
        self.mycursor.execute("INSERT INTO accounts VALUES(%s, %s, %s, %s, %s, NOW())", (username, password, self.Type, phone, email))
        self.mydb.commit()

    def verify_login(self, username, password):
        self.mycursor.execute("SELECT password FROM accounts WHERE type = %s AND username = %s", (self.Type, username))
        result = self.mycursor.fetchone()
        return result and result[0] == password
    
    def get_customer_details(self):
        self.mycursor.execute("select username, phone, email, created from accounts where type = 'Customer'")
        return self.mycursor.fetchall()
    
    def get_account_detail(self, username, Type):
        self.mycursor.execute("select * from accounts where type = %s and username = %s", (Type, username))
        return self.mycursor.fetchone()
    
    def edit_account_detail(self, username, Type, password, phone, email):
        self.mycursor.execute("update accounts set password = %s where username = %s and type = %s", (password, username, Type))
        self.mycursor.execute("update accounts set phone = %s where username = %s and type = %s", (phone, username, Type))
        self.mycursor.execute("update accounts set email = %s where username = %s and type = %s", (email, username, Type))
        self.mydb.commit()
    
    def delete_account(self, username, Type):
        self.mycursor.execute("delete from accounts where username = %s and type = %s", (username, Type))
        self.mydb.commit()
    
    @staticmethod
    def is_phone_valid(phone):
        if len(phone) == 10 and phone.isdigit():
            return True
        return False
    
    @staticmethod
    def is_email_valid(email):
        if email.count('@') == 1:
            for i in email:
                if i == '@':
                    continue
                if not (i.isalnum() or i == "."):
                    return False
            return True
        return False

class Order(Database):
    def __init__(self, username):
        super().__init__('Restaurant')
        self.username = username
        self.order_list = {}
    
    def get_categories(self):
        # Query categories from the database
        self.mycursor.execute("SELECT DISTINCT category FROM food")
        return self.mycursor.fetchall()
    
    def get_items(self, category):
        self.mycursor.execute("SELECT Name, Price FROM food WHERE category = %s", (category,))
        return self.mycursor.fetchall()
    
    def add_to_order(self, item, qty):
        if item in self.get_order_list().keys():
            self.get_order_list()[item] += qty
        else:
            self.get_order_list()[item] = qty
    
    def get_order_list(self):
        return self.order_list
    
    def delete_item(self, item):
        del self.get_order_list()[item]
    
    def get_item_price(self, item):
        self.mycursor.execute("select price from food where name = %s", (item,))
        return self.mycursor.fetchone()[0]
    
    def get_total_amount(self):
        amount = 0
        self.mycursor.execute("select name, price from food")
        r = self.mycursor.fetchall()
        for key in self.order_list:
            for row in r:
                if row[0] == key:
                    amount += row[1] * self.order_list[key]
        return amount
    
    def update_purchase(self):
        for key in self.order_list:
            self.mycursor.execute("insert into logtable values('{}', '{}', {}, {}, NOW())".format(self.username, key, self.order_list[key],  self.order_list[key] * self.get_item_price(key)))
        self.mydb.commit()
    
class History(Database):
    def __init__(self, Type):
        super().__init__('Restaurant')
        self.Type = Type

    def fetch_records(self, username):
        # Fetch and display the log details from the database
        self.username = username

        if self.Type == 'Customer':
            self.mycursor.execute("SELECT name, qty, total_price, log_time FROM logtable where username = %s", (self.username,))
        else:
            if self.username:
                self.mycursor.execute("SELECT * FROM logtable where username = %s", (self.username,))
            else:
                self.mycursor.execute("SELECT * FROM logtable")

        return self.mycursor.fetchall()

class Menu(Database):
    def __init__(self):
        super().__init__('Restaurant')

    def get_unique_values(self, column_name):
        self.mycursor.execute(f"SELECT DISTINCT {column_name} FROM food")
        return [row[0] for row in self.mycursor.fetchall()]
    
    def get_filtered_items(self, category, type_, name):
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
        return self.mycursor.fetchall()
    
    def save_item_sql(self, item_id, category, type_, name, price):
        self.mycursor.execute("UPDATE food SET Name=%s, Category=%s, Type=%s, Price=%s WHERE ID=%s", (name, category, type_, price, item_id))
        self.mydb.commit()
    
    def create_item_sql(self, category, type_, name, price):
        self.mycursor.execute("select category, type, name from food")
        for i in self.mycursor.fetchall() :
            print(category.lower() == i[0].lower() and type_.lower() == i[1].lower() and name.lower() == i[2].lower())
            if category.lower() == i[0].lower() and type_.lower() == i[1].lower() and name.lower() == i[2].lower() :
                return False
        else :
            self.mycursor.execute("insert into food (name, category, type, price) values('{}', '{}', '{}', {})".format(name.title(), category.title(), type_.title(), price))
            self.mydb.commit()
            return True  
    
    def delete_item_sql(self, id):
        self.mycursor.execute("DELETE FROM food WHERE ID = %s", (id,))
        self.mydb.commit()