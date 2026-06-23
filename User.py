from datetime import datetime
from database import Database


# ──────────────────────────────────────────
# کلاس آیتم منو
# ──────────────────────────────────────────
class Menu_item:
    def __init__(self, name, price, is_available=True, category="غذا"):
        self.name = name
        self.price = price
        self.is_available = is_available
        self.category = category

    def __str__(self):
        return f"{self.name} ({self.price:,} تومان)"


# ──────────────────────────────────────────
# کلاس سفارش
# ──────────────────────────────────────────
class Order:
    def __init__(self, order_id, customer, restaurant):
        self.order_id = order_id
        self.customer = customer
        self.restaurant = restaurant
        self.items = []
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                return True
        return False

    def total_price(self):
        return sum(item.price for item in self.items)

    def __str__(self):
        return f"Order#{self.order_id} - {self.restaurant.name} - {self.total_price():,} تومان"


# ──────────────────────────────────────────
# کلاس رستوران
# ──────────────────────────────────────────
class Restaurant:
    # رنگ‌های پیش‌فرض برای تخصیص خودکار به رستوران‌های جدید
    DEFAULT_COLORS = [
        "#e74c3c", "#3498db", "#2ecc71", "#f39c12",
        "#9b59b6", "#1abc9c", "#e67e22", "#34495e"
    ]
    _color_index = 0

    def __init__(self, name, manager, color=None):
        self.name = name
        self.manager = manager
        self.menu = []
        self.orders = []
        self.categories = ["غذا", "نوشیدنی"]
        if color:
            self.color = color
        else:
            # تخصیص خودکار رنگ از لیست پیش‌فرض 
            self.color = Restaurant.DEFAULT_COLORS[
                Restaurant._color_index % len(Restaurant.DEFAULT_COLORS)
            ]
            Restaurant._color_index += 1

    def add_order(self, order):
        self.orders.append(order)

    def get_item_by_name(self, name):
        for item in self.menu:
            if item.name == name:
                return item
        return None

    def add_category(self, category_name):
        """افزودن دسته‌بندی جدید - اگه تکراری باشه False برمیگردونه"""
        if category_name in self.categories:
            return False
        self.categories.append(category_name)
        return True

    def delete_category(self, category_name):
        """ غذا و نوشیدنی قابل حذف نیستند"""
        if category_name in ["غذا", "نوشیدنی"]:
            return False
        if category_name not in self.categories:
            return False
        # آیتم‌های این دسته به 'غذا' منتقل میشن
        for item in self.menu:
            if item.category == category_name:
                item.category = "غذا"
        self.categories.remove(category_name)
        return True

    def rename_category(self, old_name, new_name):
        """ غذا و نوشیدنی قابل تغییر نام نیستند"""
        if old_name in ["غذا", "نوشیدنی"]:
            return False
        if old_name not in self.categories:
            return False
        if new_name in self.categories:
            return False
        for item in self.menu:
            if item.category == old_name:
                item.category = new_name
        idx = self.categories.index(old_name)
        self.categories[idx] = new_name
        return True

    def __str__(self):
        return f"{self.name} (مدیر: {self.manager.username})"


# ──────────────────────────────────────────
# کلاس پایه کاربر
# ──────────────────────────────────────────
class User:
    def __init__(self, user_id, first_name, last_name, username, password):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    @staticmethod
    def validate_name(name):
        return name.isalpha() and len(name) > 0

    @staticmethod
    def validate_username(username):
        return username.isalnum() and len(username) >= 3

    @staticmethod
    def validate_password(password):
        return len(password) >= 4

    @staticmethod
    def generate_id(role, existing_ids):
        prefix = "m" if role == "manager" else "c"
        number = 1
        while f"{prefix}{number}" in existing_ids:
            number += 1
        return f"{prefix}{number}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"


# ──────────────────────────────────────────
# کلاس مدیر
# ──────────────────────────────────────────
class Manager(User):
    def __init__(self, user_id, first_name, last_name, username, password):
        super().__init__(user_id, first_name, last_name, username, password)
        self.restaurant = None

    def add_menu_item(self, name, price, category="غذا"):
        """افزودن آیتم جدید به منو"""
        if self.restaurant.get_item_by_name(name):
            return False
        if category not in self.restaurant.categories:
            category = "غذا"
        new_item = Menu_item(name, price, category=category)
        self.restaurant.menu.append(new_item)
        return True

    def edit_menu_item(self, name, new_price=None, new_available=None, new_category=None):
        """ویرایش آیتم منو"""
        item = self.restaurant.get_item_by_name(name)
        if not item:
            return False
        if new_price is not None:
            item.price = new_price
        if new_available is not None:
            item.is_available = new_available
        if new_category is not None and new_category in self.restaurant.categories:
            item.category = new_category
        return True

    def delete_menu_item(self, name):
        """حذف آیتم از منو"""
        item = self.restaurant.get_item_by_name(name)
        if not item:
            return False
        self.restaurant.menu.remove(item)
        return True

    def add_category(self, category_name):
        return self.restaurant.add_category(category_name)

    def delete_category(self, category_name):
        return self.restaurant.delete_category(category_name)

    def rename_category(self, old_name, new_name):
        return self.restaurant.rename_category(old_name, new_name)

    def set_color(self, color):
        """تنظیم رنگ رستوران"""
        self.restaurant.color = color


# ──────────────────────────────────────────
# کلاس مشتری
# ──────────────────────────────────────────
class Customer(User):
    def __init__(self, user_id, first_name, last_name, username, password):
        super().__init__(user_id, first_name, last_name, username, password)
        # سبد خرید به صورت دیکشنری: کلید = (نام آیتم, نام رستوران)
        # مقدار = {"item": ..., "restaurant": ..., "quantity": ...}
        self.cart = {}
        self.order_history = []

    def add_to_cart(self, item, restaurant):
        """افزودن آیتم به سبد - اگه از قبل باشه تعدادش زیاد میشه"""
        if not item.is_available:
            return False
        key = (item.name, restaurant.name)
        if key in self.cart:
            self.cart[key]["quantity"] += 1
        else:
            self.cart[key] = {
                "item": item,
                "restaurant": restaurant,
                "quantity": 1
            }
        return True

    def remove_from_cart(self, item_name, restaurant_name):
        """کم کردن یک عدد از تعداد - اگه صفر شد حذف میشه"""
        key = (item_name, restaurant_name)
        if key not in self.cart:
            return False
        self.cart[key]["quantity"] -= 1
        if self.cart[key]["quantity"] <= 0:
            del self.cart[key]
        return True

    def remove_all_from_cart(self, item_name, restaurant_name):
        key = (item_name, restaurant_name)
        if key not in self.cart:
            return False
        del self.cart[key]
        return True

    def checkout(self, order_id_generator):
        if not self.cart:
            return []

        restaurant_items = {}
        for key, entry in self.cart.items():
            item = entry["item"]
            restaurant = entry["restaurant"]
            quantity = entry["quantity"]
            if restaurant.name not in restaurant_items:
                restaurant_items[restaurant.name] = (restaurant, [])
            for q in range(quantity):
                restaurant_items[restaurant.name][1].append(item)

        orders = []
        for restaurant_name, (restaurant, items) in restaurant_items.items():
            order_id = order_id_generator()
            new_order = Order(order_id, self, restaurant)
            for item in items:
                new_order.add_item(item)
            restaurant.add_order(new_order)
            self.order_history.append(new_order)
            orders.append(new_order)

        self.cart = {}
        return orders


# ──────────────────────────────────────────
# کلاس پلتفرم (هسته اصلی برنامه)
# ──────────────────────────────────────────
class Platform:
    def __init__(self):
        self.restaurants = []
        self.users = []
        self.current_user = None
        self._order_counter = 1
        self.db = Database()

    def _get_existing_ids(self):
        return [user.user_id for user in self.users]

    def _generate_order_id(self):
        order_id = f"ORD{self._order_counter}"
        self._order_counter += 1
        return order_id

    def load_all(self):

        # بارگذاری کاربران
        for row in self.db.load_users():
            user_id, first_name, last_name, username, password, role = row
            if role == "manager":
                user = Manager(user_id, first_name, last_name, username, password)
            else:
                user = Customer(user_id, first_name, last_name, username, password)
            self.users.append(user)

        # بارگذاری رستوران‌ها
        for row in self.db.load_restaurants():
            restaurant_name, manager_username, color = row
            manager = next(
                (u for u in self.users if u.username == manager_username), None
            )
            if not manager:
                continue

            restaurant = Restaurant(restaurant_name, manager, color=color)
            manager.restaurant = restaurant
            self.restaurants.append(restaurant)

            # بارگذاری دسته‌بندی‌های اضافی (غذا و نوشیدنی از قبل هستن)
            for cat_name in self.db.load_categories(restaurant_name):
                if cat_name not in restaurant.categories:
                    restaurant.categories.append(cat_name)

            # بارگذاری آیتم‌های منو
            for item_row in self.db.load_menu_items(restaurant_name):
                item_name, price, is_available, category = item_row
                item = Menu_item(item_name, price, bool(is_available), category)
                restaurant.menu.append(item)

        # بارگذاری سفارش‌ها
        for customer in [u for u in self.users if isinstance(u, Customer)]:
            for order_row in self.db.load_orders(customer.username):
                order_id, customer_username, restaurant_name, created_at = order_row
                restaurant = next(
                    (r for r in self.restaurants if r.name == restaurant_name), None
                )
                if not restaurant:
                    continue
                order = Order(order_id, customer, restaurant)
                order.created_at = created_at
                for item_row in self.db.load_order_items(order_id):
                    item_name, price, category = item_row
                    item = Menu_item(item_name, price, category=category)
                    order.add_item(item)
                customer.order_history.append(order)
                restaurant.orders.append(order)
                # آپدیت شمارنده سفارش‌ها
                number = int(order_id.replace("ORD", ""))
                if number >= self._order_counter:
                    self._order_counter = number + 1