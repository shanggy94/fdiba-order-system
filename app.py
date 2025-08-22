from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Функция за свързване с базата данни
def get_db_connection():
    conn = sqlite3.connect('orders.db')
    conn.row_factory = sqlite3.Row
    return conn

# Главна страница - показва списък с поръчки
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT orders.order_id, users.username, products.name, orders.quantity, orders.order_date
        FROM orders
        JOIN users ON orders.user_id = users.user_id
        JOIN products ON orders.product_id = products.product_id
    ''')
    orders = cursor.fetchall()
    conn.close()
    return render_template('index.html', orders=orders)

# Страница за добавяне на нова поръчка
@app.route('/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        order_date = request.form['order_date']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)',
                       (user_id, product_id, quantity, order_date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username FROM users')
    users = cursor.fetchall()
    cursor.execute('SELECT product_id, name FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('add_order.html', users=users, products=products)

# Страница за редактиране на поръчка
@app.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        order_date = request.form['order_date']
        
        cursor.execute('UPDATE orders SET user_id = ?, product_id = ?, quantity = ?, order_date = ? WHERE order_id = ?',
                       (user_id, product_id, quantity, order_date, order_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
    order = cursor.fetchone()
    cursor.execute('SELECT user_id, username FROM users')
    users = cursor.fetchall()
    cursor.execute('SELECT product_id, name FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('edit_order.html', order=order, users=users, products=products)

# Изтриване на поръчка
@app.route('/delete/<int:order_id>')
def delete_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)