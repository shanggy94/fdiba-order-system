import sqlite3

def create_database():
    # Създаване на връзка
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Активиране на поддръжка за външни ключове
    cursor.execute("PRAGMA foreign_keys = ON")

    # Таблица за потребители
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      username TEXT NOT NULL, 
                      email TEXT NOT NULL)''')

    # Таблица за продукти
    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                     (product_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      name TEXT NOT NULL, 
                      price REAL NOT NULL)''')

    # Таблица за поръчки
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                     (order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      user_id INTEGER, 
                      product_id INTEGER, 
                      quantity INTEGER NOT NULL, 
                      order_date TEXT NOT NULL, 
                      FOREIGN KEY(user_id) REFERENCES users(user_id), 
                      FOREIGN KEY(product_id) REFERENCES products(product_id))''')

    # Добавяне на примерни данни
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("pepi", "pepi@example.com"))
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("ivan", "ivan@example.com"))
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", ("Учебник по математика", 20.0))
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", ("Учебник по физика", 25.0))
    cursor.execute("INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)", (1, 1, 2, "2025-08-15"))
    cursor.execute("INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)", (2, 2, 1, "2025-08-16"))

    # Запазване на промените
    conn.commit()
    # Затваряне на връзката
    conn.close()

# Извикване на функцията
create_database()