import sqlite3


class Database:
    def __init__(self, db_name="SnappFood.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # جدول کاربران
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id    TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name  TEXT NOT NULL,
                username   TEXT UNIQUE NOT NULL,
                password   TEXT NOT NULL,
                role       TEXT NOT NULL
            )
        """)

        # جدول رستوران‌ها - حالا شامل ستون color هم هست
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS restaurants (
                name             TEXT PRIMARY KEY,
                manager_username TEXT NOT NULL,
                color            TEXT NOT NULL DEFAULT '#e74c3c'
            )
        """)

        # جدول دسته‌بندی‌ها
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                restaurant_name TEXT NOT NULL,
                UNIQUE(name, restaurant_name)
            )
        """)

        # جدول آیتم‌های منو - بدون item_type، فقط category
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name       TEXT NOT NULL,
                price           INTEGER NOT NULL,
                is_available    INTEGER NOT NULL,
                restaurant_name TEXT NOT NULL,
                category        TEXT NOT NULL DEFAULT 'غذا'
            )
        """)

        # جدول سفارش‌ها
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id          TEXT PRIMARY KEY,
                customer_username TEXT NOT NULL,
                restaurant_name   TEXT NOT NULL,
                created_at        TEXT NOT NULL
            )
        """)

        # جدول آیتم‌های سفارش
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id  TEXT NOT NULL,
                item_name TEXT NOT NULL,
                price     INTEGER NOT NULL,
                category  TEXT NOT NULL DEFAULT 'عمومی'
            )
        """)

        # سازگاری با دیتابیس قدیمی - اضافه کردن ستون‌های جدید اگه وجود نداشتن
        for sql in [
            "ALTER TABLE restaurants ADD COLUMN color TEXT NOT NULL DEFAULT '#e74c3c'",
            "ALTER TABLE menu_items ADD COLUMN category TEXT NOT NULL DEFAULT 'غذا'",
            "ALTER TABLE order_items ADD COLUMN category TEXT NOT NULL DEFAULT 'عمومی'",
        ]:
            try:
                self.cursor.execute(sql)
            except sqlite3.OperationalError:
                pass  # ستون از قبل وجود دارد

        self.conn.commit()

    def close(self):
        self.conn.close()

    # ──────────────────────────────────────────
    # عملیات کاربران
    # ──────────────────────────────────────────

    def save_user(self, user, role):
        """ذخیره کاربر جدید"""
        try:
            self.cursor.execute("""
                INSERT INTO users (user_id, first_name, last_name, username, password, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user.user_id, user.first_name, user.last_name,
                  user.username, user.password, role))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def load_users(self):
        """خواندن همه کاربران"""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    # ──────────────────────────────────────────
    # عملیات رستوران‌ها
    # ──────────────────────────────────────────

    def save_restaurant(self, restaurant):
        """ذخیرهرستوران جدید با رنگش"""
        try:
            self.cursor.execute("""
                INSERT INTO restaurants (name, manager_username, color)
                VALUES (?, ?, ?)
            """, (restaurant.name, restaurant.manager.username, restaurant.color))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def update_restaurant_color(self, restaurant_name, color):
        """آپدیت رنگ رستوران"""
        self.cursor.execute("""
            UPDATE restaurants SET color = ?
            WHERE name = ?
        """, (color, restaurant_name))
        self.conn.commit()

    def load_restaurants(self):
        """خواندن همه رستوران‌ها - شامل رنگ"""
        self.cursor.execute("SELECT name, manager_username, color FROM restaurants")
        return self.cursor.fetchall()

    # ──────────────────────────────────────────
    # عملیات دسته‌بندی‌ها
    # ──────────────────────────────────────────

    def save_category(self, name, restaurant_name):
        """ذخیره دسته‌بندی جدید"""
        try:
            self.cursor.execute("""
                INSERT INTO categories (name, restaurant_name)
                VALUES (?, ?)
            """, (name, restaurant_name))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # از قبل وجود دارد

    def load_categories(self, restaurant_name):
        """خواندن دسته‌بندی‌های یک رستوران"""
        self.cursor.execute("""
            SELECT name FROM categories
            WHERE restaurant_name = ?
            ORDER BY id
        """, (restaurant_name,))
        return [row[0] for row in self.cursor.fetchall()]

    def delete_category(self, name, restaurant_name):
        """حذف دسته‌بندی"""
        self.cursor.execute("""
            DELETE FROM categories
            WHERE name = ? AND restaurant_name = ?
        """, (name, restaurant_name))
        self.conn.commit()

    def rename_category(self, old_name, new_name, restaurant_name):
        """تغییر نام دسته‌بندی"""
        self.cursor.execute("""
            UPDATE categories SET name = ?
            WHERE name = ? AND restaurant_name = ?
        """, (new_name, old_name, restaurant_name))
        self.conn.commit()

    # ──────────────────────────────────────────
    # عملیات آیتم‌های منو
    # ──────────────────────────────────────────

    def save_menu_item(self, item, restaurant_name):
        """ذخیره آیتم منو - بدون item_type"""
        self.cursor.execute("""
            INSERT INTO menu_items (item_name, price, is_available, restaurant_name, category)
            VALUES (?, ?, ?, ?, ?)
        """, (item.name, item.price,
              1 if item.is_available else 0,
              restaurant_name,
              item.category))
        self.conn.commit()

    def load_menu_items(self, restaurant_name):
        """خواندن آیتم‌های منو - بدون item_type"""
        self.cursor.execute("""
            SELECT item_name, price, is_available, category
            FROM menu_items
            WHERE restaurant_name = ?
        """, (restaurant_name,))
        return self.cursor.fetchall()

    def update_menu_item(self, item, restaurant_name):
        """آپدیت آیتم منو"""
        self.cursor.execute("""
            UPDATE menu_items
            SET price = ?, is_available = ?, category = ?
            WHERE item_name = ? AND restaurant_name = ?
        """, (item.price,
              1 if item.is_available else 0,
              item.category,
              item.name,
              restaurant_name))
        self.conn.commit()

    def delete_menu_item(self, item_name, restaurant_name):
        """حذف آیتم از منو"""
        self.cursor.execute("""
            DELETE FROM menu_items
            WHERE item_name = ? AND restaurant_name = ?
        """, (item_name, restaurant_name))
        self.conn.commit()

    # ──────────────────────────────────────────
    # عملیات سفارش‌ها
    # ──────────────────────────────────────────

    def save_order(self, order):
        """ذخیره سفارش و آیتم‌هایش"""
        self.cursor.execute("""
            INSERT INTO orders (order_id, customer_username, restaurant_name, created_at)
            VALUES (?, ?, ?, ?)
        """, (order.order_id, order.customer.username,
              order.restaurant.name, order.created_at))
        for item in order.items:
            self.cursor.execute("""
                INSERT INTO order_items (order_id, item_name, price, category)
                VALUES (?, ?, ?, ?)
            """, (order.order_id, item.name, item.price, item.category))
        self.conn.commit()

    def load_orders(self, customer_username):
        """خواندن سفارش‌های یک مشتری"""
        self.cursor.execute("""
            SELECT * FROM orders WHERE customer_username = ?
        """, (customer_username,))
        return self.cursor.fetchall()

    def load_order_items(self, order_id):
        """خواندن آیتم‌های یک سفارش - حالا category هم برگردانده میشه"""
        self.cursor.execute("""
            SELECT item_name, price, category FROM order_items WHERE order_id = ?
        """, (order_id,))
        return self.cursor.fetchall()

    def load_restaurant_orders(self, restaurant_name):
        """خواندن همه سفارش‌های یک رستوران"""
        self.cursor.execute("""
            SELECT * FROM orders WHERE restaurant_name = ?
        """, (restaurant_name,))
        return self.cursor.fetchall()
    

        