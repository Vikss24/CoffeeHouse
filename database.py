import sqlite3

def init_db():
    conn = sqlite3.connect('coffee_shop.db')
    cursor = conn.cursor()

    # 1. Таблиця співробітників та користувачів
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')

    # 2. Таблиця інгредієнтів на складі
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL
        )
    ''')

    # 3. Таблиця меню кав'ярні
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')

    # 4. Таблиця замовлень / покупок
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Додаємо тестових користувачів (як у прикладі README)
    cursor.executemany('''
        INSERT OR IGNORE INTO users (login, password, role, full_name)
        VALUES (?, ?, ?, ?)
    ''', [
        ('admin', 'admin123', 'Адміністратор', 'Вікторія (Власниця)'),
        ('barista', '1234', 'Бариста', 'Олена Коваленко'),
        ('client', '1234', 'Клієнт', 'Гість кав\'ярні')
    ])

    # Додаємо базові інгредієнти
    cursor.executemany('''
        INSERT OR IGNORE INTO ingredients (name, quantity, unit)
        VALUES (?, ?, ?)
    ''', [
        ('Кава в зернах (Арабіка)', 5000, 'г'),
        ('Молоко 2.5%', 10000, 'мл'),
        ('Цукор білий', 3000, 'г'),
        ('Сироп Карамель', 1000, 'мл')
    ])

    # Додаємо базове меню
    cursor.executemany('''
        INSERT OR IGNORE INTO menu (name, price, category)
        VALUES (?, ?, ?)
    ''', [
        ('Еспресо', 45.0, 'Кава'),
        ('Американо', 50.0, 'Кава'),
        ('Капучино', 65.0, 'Кава з молоком'),
        ('Лате', 70.0, 'Кава з молоком'),
        ('Круасан з шоколадом', 55.0, 'Випічка')
    ])

    conn.commit()
    conn.close()
    print("Базу даних кав'ярні успішно створено та заповнено!")

if __name__ == '__main__':
    init_db()
