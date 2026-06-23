from User import Manager, Customer, Restaurant, Menu_item
from database import Database


def initialize():
    db = Database()

    # ── ساخت مدیر و رستوران ──
    manager = Manager("m1", "Romina", "Poorgholami", "romi12", "1234")
    restaurant = Restaurant("رستوران سنتی دیبیجا", manager)
    manager.restaurant = restaurant
    restaurant.add_category("پیش‌غذا")
    restaurant.add_category("دسر")
    restaurant.add_category("خورشت")
    restaurant.add_category("کباب")

    # ── آیتم‌های منو ──
    items = [
        # پیش‌غذا
        Menu_item("ماست و خیار", 18000, is_available=True,  category="پیش‌غذا"),
        Menu_item("سالاد فصل", 22000, is_available=True,  category="پیش‌غذا"),
        Menu_item("سینی مخلفات", 35000, is_available=True,  category="پیش‌غذا"),
        Menu_item("دیبیجا", 450000, is_available=True,  category="پیش‌غذا"),
        # غذا
        Menu_item("چلوکباب کوبیده",  95000, is_available=True,  category="کباب"),
        Menu_item("چلوکباب برگ",    145000, is_available=True,  category="کباب"),
        Menu_item("قرمه سبزی",       85000, is_available=True,  category="خورشت"),
        Menu_item("خورشت فسنجان",    90000, is_available=True,  category="خورشت"),
        Menu_item("جوجه کباب",      105000, is_available=True,  category="کباب"),
        Menu_item("ماهی قزل‌آلا کبابی",   130000, is_available=False, category="کباب"),

        # دسر
        Menu_item("زولبیا بامیه",    25000, is_available=True,  category="دسر"),
        Menu_item("فالوده شیرازی",   30000, is_available=True,  category="دسر"),

        # نوشیدنی
        Menu_item("دوغ محلی",        15000, is_available=True,  category="نوشیدنی"),
        Menu_item("نوشابه",           12000, is_available=True,  category="نوشیدنی"),
        Menu_item("دلستر",            18000, is_available=True,  category="نوشیدنی"),
        Menu_item("چای",               8000, is_available=True,  category="نوشیدنی"),
    ]

    for item in items:
        restaurant.menu.append(item)

    # ── ساخت مشتری ──
    customer = Customer("c1", "Sara", "Mohammadi", "sara99", "abcd")

    # ── ذخیره توی دیتابیس ──
    db.save_user(manager, "manager")
    db.save_restaurant(restaurant)
    for cat in ["پیش‌غذا", "دسر","خورشت","کباب"]:
        db.save_category(cat, restaurant.name)

    for item in items:
        db.save_menu_item(item, restaurant.name)

    db.save_user(customer, "customer")
    db.close()

   


if __name__ == "__main__":
    initialize()