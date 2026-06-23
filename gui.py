import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from User import Platform, Manager, Customer, User, Restaurant


# ──────────────────────────────────────────
# صفحه ورود
# ──────────────────────────────────────────
class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f5f5")
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="🍕 Snapp Food",
                 font=("Arial", 28, "bold"),
                 bg="#f5f5f5", fg="#e74c3c").pack(pady=30)

        center = tk.Frame(self, bg="white", relief="ridge", bd=2)
        center.pack(padx=100, pady=10, fill="x")

        tk.Label(center, text="نام کاربری",
                 font=("Arial", 12), bg="white").grid(
                 row=0, column=0, padx=20, pady=10, sticky="e")
        self.username_entry = tk.Entry(center, font=("Arial", 12), width=25)
        self.username_entry.grid(row=0, column=1, padx=20, pady=10)

        tk.Label(center, text="رمز عبور",
                 font=("Arial", 12), bg="white").grid(
                 row=1, column=0, padx=20, pady=10, sticky="e")
        self.password_entry = tk.Entry(center, font=("Arial", 12),
                                       width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=20, pady=10)

        tk.Button(self, text="ورود",
                  font=("Arial", 12, "bold"),
                  bg="#e74c3c", fg="white",
                  width=20, cursor="hand2",
                  command=self._login).pack(pady=20)

        signup_frame = tk.Frame(self, bg="#f5f5f5")
        signup_frame.pack()
        
        tk.Button(signup_frame, text="ثبت‌ نام کنید",
                  font=("Arial", 15, "underline"),
                  bg="#f5f5f5", fg="#096d33",
                  bd=0, cursor="hand2",
                  command=self.app.show_signup).pack(side="left")
        
        tk.Label(signup_frame, text="حساب ندارید؟",
                 font=("Arial", 15), bg="#f5f5f5", fg="#222323").pack(side="left", padx=5)
        

    def _login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("خطا", "لطفاً همه فیلدها را پر کنید.")
            return

        for user in self.app.platform.users:
            if user.username == username and user.password == password:
                self.app.platform.current_user = user
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                if isinstance(user, Manager):
                    self.app.show_manager()
                else:
                    self.app.show_customer()
                return

        messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است.")
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

# ──────────────────────────────────────────
# صفحه ثبت‌نام
# ──────────────────────────────────────────
class SignupFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f5f5")
        self.app = app
        self._build()

    def _build(self):
        tk.Label(self, text="ثبت‌نام",
                 font=("Arial", 24, "bold"),
                 bg="#f5f5f5", fg="#2ecc71").pack(pady=20)

        center = tk.Frame(self, bg="white", relief="ridge", bd=2)
        center.pack(padx=100, pady=10, fill="x")

        fields = [
            ("نام", "first_name"),
            ("نام خانوادگی", "last_name"),
            ("نام کاربری", "username"),
            ("رمز عبور", "password"),
        ]
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(center, text=label,
                     font=("Arial", 12), bg="white").grid(
                     row=i, column=0, padx=20, pady=8, sticky="e")
            entry = tk.Entry(center, font=("Arial", 12), width=25,
                             show="*" if key == "password" else "")
            entry.grid(row=i, column=1, padx=20, pady=8)
            self.entries[key] = entry

        tk.Label(center, text="نوع حساب",
                 font=("Arial", 12), bg="white").grid(
                 row=4, column=0, padx=20, pady=8, sticky="e")
        self.role_var = tk.StringVar(value="customer")
        role_frame = tk.Frame(center, bg="white")
        role_frame.grid(row=4, column=1, padx=20, pady=8, sticky="w")
        tk.Radiobutton(role_frame, text="مشتری", variable=self.role_var,
                       value="customer", bg="white",
                       command=self._toggle_restaurant).pack(side="left")
        tk.Radiobutton(role_frame, text="مدیر", variable=self.role_var,
                       value="manager", bg="white",
                       command=self._toggle_restaurant).pack(side="left")

        self.restaurant_label = tk.Label(center, text="نام رستوران",
                                          font=("Arial", 12), bg="white")
        self.restaurant_entry = tk.Entry(center, font=("Arial", 12), width=25)
        self.restaurant_label.grid(row=5, column=0, padx=20, pady=8, sticky="e")
        self.restaurant_entry.grid(row=5, column=1, padx=20, pady=8)
        self.restaurant_label.grid_remove()
        self.restaurant_entry.grid_remove()

        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="ثبت‌ نام",
                  font=("Arial", 12, "bold"),
                  bg="#2ecc71", fg="white",
                  width=12, cursor="hand2",
                  command=self._signup).pack(side="left", padx=10)
        tk.Button(btn_frame, text="بازگشت",
                  font=("Arial", 12, "bold"),
                  bg="#95a5a6", fg="white",
                  width=12, cursor="hand2",
                  command=self.app.show_login).pack(side="left", padx=10)

    def _toggle_restaurant(self):
        "تشخیص و نمایش اینتری برای رستوران"
        if self.role_var.get() == "manager":
            self.restaurant_label.grid()
            self.restaurant_entry.grid()
        else:
            self.restaurant_label.grid_remove()
            self.restaurant_entry.grid_remove()

    def _signup(self):
        first_name = self.entries["first_name"].get().strip()
        last_name  = self.entries["last_name"].get().strip()
        username   = self.entries["username"].get().strip()
        password   = self.entries["password"].get().strip()
        role       = self.role_var.get()

        if not User.validate_name(first_name):
            messagebox.showerror("خطا", "نام نامعتبر است.")
            return
        if not User.validate_name(last_name):
            messagebox.showerror("خطا", "نام خانوادگی نامعتبر است.")
            return
        if not User.validate_username(username):
            messagebox.showerror("خطا", "نام کاربری باید حداقل ۳ کاراکتر و فقط حرف/عدد باشد.")
            return
        if any(u.username == username for u in self.app.platform.users):
            messagebox.showerror("خطا", "این نام کاربری قبلاً استفاده شده.")
            return
        if not User.validate_password(password):
            messagebox.showerror("خطا", "رمز عبور باید حداقل ۴ کاراکتر باشد.")
            return

        existing_ids = [u.user_id for u in self.app.platform.users]

        if role == "manager":
            restaurant_name = self.restaurant_entry.get().strip()
            if not restaurant_name:
                messagebox.showerror("خطا", "نام رستوران نمی‌تواند خالی باشد.")
                return
            if any(r.name == restaurant_name for r in self.app.platform.restaurants):
                messagebox.showerror("خطا", "رستورانی با این نام قبلاً وجود دارد.")
                return
            user_id  = User.generate_id("manager", existing_ids)
            new_user = Manager(user_id, first_name, last_name, username, password)
            new_restaurant = Restaurant(restaurant_name, new_user)
            new_user.restaurant = new_restaurant
            self.app.platform.restaurants.append(new_restaurant)
            self.app.platform.db.save_restaurant(new_restaurant)
        else:
            user_id  = User.generate_id("customer", existing_ids)
            new_user = Customer(user_id, first_name, last_name, username, password)

        self.app.platform.users.append(new_user)
        self.app.platform.db.save_user(new_user, role)
        messagebox.showinfo("موفقیت", f"ثبت‌نام موفق! ID شما: {user_id}")
        self._clear_form()
        self.app.show_login()

    def _clear_form(self):
        """پاک کردن فرم بعد از ثبت‌نام"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.restaurant_entry.delete(0, tk.END)
        self.role_var.set("customer")
        self.restaurant_label.grid_remove()
        self.restaurant_entry.grid_remove()


# ──────────────────────────────────────────
# پنجره مدیریت دسته‌بندی‌ها
# ──────────────────────────────────────────
class CategoryManagerWindow(tk.Toplevel):
    def __init__(self, parent, app, on_close_callback):
        super().__init__(parent)
        self.app = app
        self.on_close_callback = on_close_callback
        self.title("مدیریت دسته‌بندی‌ها")
        self.geometry("420x500")
        self.configure(bg="#f5f5f5")
        self.resizable(False, False)
        self.grab_set()
        self._build()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build(self):
        manager = self.app.platform.current_user

        tk.Label(self, text="📂 مدیریت دسته‌بندی‌ها",
                 font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)
        tk.Label(self, text=f"رستوران: {manager.restaurant.name}",
                 font=("Arial", 11), bg="#f5f5f5", fg="#7f8c8d").pack()

        list_frame = tk.Frame(self, bg="white", relief="ridge", bd=2)
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(list_frame, text="دسته‌بندی‌های فعلی:",
                 font=("Arial", 11, "bold"), bg="white").pack(pady=(8, 0))

        self.cat_listbox = tk.Listbox(list_frame, font=("Arial", 11),
                                       height=8, selectbackground="#3498db",
                                       cursor="hand2")
        self.cat_listbox.pack(padx=10, pady=5, fill="both", expand=True)

        input_frame = tk.Frame(self, bg="#f5f5f5")
        input_frame.pack(padx=20, pady=5, fill="x")
        tk.Label(input_frame, text="نام دسته‌بندی:",
                 font=("Arial", 11), bg="#f5f5f5").grid(row=0, column=0, sticky="e", padx=5)
        self.cat_entry = tk.Entry(input_frame, font=("Arial", 11), width=22)
        self.cat_entry.grid(row=0, column=1, padx=5)

        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="➕ افزودن",
                  font=("Arial", 10, "bold"),
                  bg="#2ecc71", fg="white", width=10,
                  cursor="hand2",
                  command=self._add_category).grid(row=0, column=0, padx=5, pady=4)
        tk.Button(btn_frame, text="✏️ تغییر نام",
                  font=("Arial", 10, "bold"),
                  bg="#3498db", fg="white", width=10,
                  cursor="hand2",
                  command=self._rename_category).grid(row=0, column=1, padx=5, pady=4)
        tk.Button(btn_frame, text="🗑️ حذف",
                  font=("Arial", 10, "bold"),
                  bg="#e74c3c", fg="white", width=10,
                  cursor="hand2",
                  command=self._delete_category).grid(row=0, column=2, padx=5, pady=4)

        tk.Label(self, text="⚠️ دسته‌های 'غذا' و 'نوشیدنی' قابل حذف یا تغییر نام نیستند",
                 font=("Arial", 9), bg="#f5f5f5", fg="#e67e22").pack()

        tk.Button(self, text="بستن",
                  font=("Arial", 11),
                  bg="#95a5a6", fg="white", width=12,
                  cursor="hand2",
                  command=self._on_close).pack(pady=8)

        self._refresh_list()

    def _refresh_list(self):
        self.cat_listbox.delete(0, tk.END)
        manager = self.app.platform.current_user
        for cat in manager.restaurant.categories:
            self.cat_listbox.insert(tk.END, cat)

    def _get_selected(self):
        selected = self.cat_listbox.curselection()
        if not selected:
            return None
        return self.cat_listbox.get(selected[0])

    def _add_category(self):
        name = self.cat_entry.get().strip()
        if not name:
            messagebox.showerror("خطا", "نام دسته‌بندی را وارد کنید.", parent=self)
            return
        manager = self.app.platform.current_user
        if manager.add_category(name):
            self.app.platform.db.save_category(name, manager.restaurant.name)
            self._refresh_list()
            self.cat_entry.delete(0, tk.END)
            messagebox.showinfo("موفقیت", f"دسته '{name}' اضافه شد.", parent=self)
        else:
            messagebox.showerror("خطا", "این دسته‌بندی قبلاً وجود دارد.", parent=self)

    def _rename_category(self):
        old_name = self._get_selected()
        if not old_name:
            messagebox.showerror("خطا", "ابتدا یک دسته از لیست انتخاب کنید.", parent=self)
            return
        if old_name in ["غذا", "نوشیدنی"]:
            messagebox.showerror("خطا", f"دسته '{old_name}' قابل تغییر نام نیست.", parent=self)
            return
        new_name = self.cat_entry.get().strip()
        if not new_name:
            messagebox.showerror("خطا", "نام جدید را در فیلد ورودی وارد کنید.", parent=self)
            return
        manager = self.app.platform.current_user
        if manager.rename_category(old_name, new_name):
            self.app.platform.db.rename_category(old_name, new_name, manager.restaurant.name)
            for item in manager.restaurant.menu:
                self.app.platform.db.update_menu_item(item, manager.restaurant.name)
            self._refresh_list()
            self.cat_entry.delete(0, tk.END)
            messagebox.showinfo("موفقیت", f"'{old_name}' به '{new_name}' تغییر یافت.", parent=self)
        else:
            messagebox.showerror("خطا", "عملیات ناموفق. شاید نام جدید تکراری باشد.", parent=self)

    def _delete_category(self):
        cat_name = self._get_selected()
        if not cat_name:
            messagebox.showerror("خطا", "ابتدا یک دسته از لیست انتخاب کنید.", parent=self)
            return
        if cat_name in ["غذا", "نوشیدنی"]:
            messagebox.showerror("خطا", f"دسته '{cat_name}' قابل حذف نیست.", parent=self)
            return
        if not messagebox.askyesno("تأیید",
                                    f"دسته '{cat_name}' حذف شود?\nآیتم‌هایش به 'غذا' منتقل می‌شوند.",
                                    parent=self):
            return
        manager = self.app.platform.current_user
        if manager.delete_category(cat_name):
            self.app.platform.db.delete_category(cat_name, manager.restaurant.name)
            for item in manager.restaurant.menu:
                self.app.platform.db.update_menu_item(item, manager.restaurant.name)
            self._refresh_list()
            messagebox.showinfo("موفقیت", f"دسته '{cat_name}' حذف شد.", parent=self)

    def _on_close(self):
        self.on_close_callback()
        self.destroy()


# ──────────────────────────────────────────
# پنل مدیر
# ──────────────────────────────────────────
class ManagerFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f5f5")
        self.app = app

    def build(self):
        for widget in self.winfo_children():
            widget.destroy()

        manager = self.app.platform.current_user
        rest_color = manager.restaurant.color

        # هدر با رنگ رستوران
        header = tk.Frame(self, bg=rest_color)
        header.pack(fill="x")
        tk.Label(header, text=f"🍕 {manager.restaurant.name}",
                 font=("Arial", 16, "bold"),
                 bg=rest_color, fg="white").pack(side="left", padx=20, pady=10)

        # دکمه انتخاب رنگ رستوران
        tk.Button(header, text="🎨 رنگ رستوران",
                  font=("Arial", 10), bg="white", fg=rest_color,
                  cursor="hand2",
                  command=self._pick_color).pack(side="right", padx=10)

        tk.Button(header, text="خروج",
                  font=("Arial", 10), fg="white",
                  bg=self._darken(rest_color),
                  bd=0, cursor="hand2",
                  command=self.app.logout).pack(side="right", padx=10)

        # محتوای اصلی
        main = tk.Frame(self, bg="#f5f5f5")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ── ستون چپ: فرم ──
        left = tk.Frame(main, bg="white", relief="ridge", bd=2)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="مدیریت منو",
                 font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        form = tk.Frame(left, bg="white")
        form.pack(padx=20, pady=5, fill="x")

        tk.Label(form, text="نام آیتم:", bg="white",
                 font=("Arial", 11)).grid(row=0, column=0, sticky="e", pady=5)
        self.name_entry = tk.Entry(form, font=("Arial", 11), width=20)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="قیمت (تومان):", bg="white",
                 font=("Arial", 11)).grid(row=1, column=0, sticky="e", pady=5)
        self.price_entry = tk.Entry(form, font=("Arial", 11), width=20)
        self.price_entry.grid(row=1, column=1, padx=10, pady=5)

        # دسته‌بندی - Combobox (جایگزین radio button نوع)
        tk.Label(form, text="دسته‌بندی:", bg="white",
                 font=("Arial", 11)).grid(row=2, column=0, sticky="e", pady=5)
        self.category_var = tk.StringVar(value="غذا")
        self.category_combo = ttk.Combobox(form, textvariable=self.category_var,
                                            width=18, state="readonly",
                                            font=("Arial", 11))
        self.category_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self._refresh_category_combo()

        tk.Label(form, text="وضعیت:", bg="white",
                 font=("Arial", 11)).grid(row=3, column=0, sticky="e", pady=5)
        self.available_var = tk.BooleanVar(value=True)
        avail_frame = tk.Frame(form, bg="white")
        avail_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        tk.Radiobutton(avail_frame, text="موجود", variable=self.available_var,
                       value=True, bg="white").pack(side="left")
        tk.Radiobutton(avail_frame, text="ناموجود", variable=self.available_var,
                       value=False, bg="white").pack(side="left")

        # دکمه‌های عملیات
        btn_frame = tk.Frame(left, bg="white")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="➕ افزودن",
                  font=("Arial", 10, "bold"),
                  bg="#2ecc71", fg="white", width=10,
                  cursor="hand2",
                  command=self._add_item).pack(side="left", padx=4)
        tk.Button(btn_frame, text="✏️ ویرایش",
                  font=("Arial", 10, "bold"),
                  bg="#3498db", fg="white", width=10,
                  cursor="hand2",
                  command=self._edit_item).pack(side="left", padx=4)
        tk.Button(btn_frame, text="🗑️ حذف",
                  font=("Arial", 10, "bold"),
                  bg="#e74c3c", fg="white", width=10,
                  cursor="hand2",
                  command=self._delete_item).pack(side="left", padx=4)

        tk.Button(left, text="📂 مدیریت دسته‌بندی‌ها",
                  font=("Arial", 10, "bold"),
                  bg="#9b59b6", fg="white", width=22,
                  cursor="hand2",
                  command=self._open_category_manager).pack(pady=(0, 10))

        # ── ستون راست: جداول ──
        right = tk.Frame(main, bg="white", relief="ridge", bd=2)
        right.pack(side="right", fill="both", expand=True)

        tab = ttk.Notebook(right)
        tab.pack(fill="both", expand=True, padx=10, pady=10)

        # تب منو
        menu_tab = tk.Frame(tab, bg="white")
        tab.add(menu_tab, text="📋 منو")

        self.menu_tree = ttk.Treeview(menu_tab,
                                       columns=("name", "price", "status"),
                                       show="headings", height=12)
        self.menu_tree.heading("name",   text="نام")
        self.menu_tree.heading("price",  text="قیمت")
        self.menu_tree.heading("status", text="وضعیت")
        self.menu_tree.column("name",   width=140)
        self.menu_tree.column("price",  width=100)
        self.menu_tree.column("status", width=90)

        scrollbar = ttk.Scrollbar(menu_tab, orient="vertical",
                                   command=self.menu_tree.yview)
        self.menu_tree.configure(yscrollcommand=scrollbar.set)
        self.menu_tree.pack(side="left", fill="both", expand=True, padx=(5,0), pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        self.menu_tree.bind("<<TreeviewSelect>>", self._on_select)

        # تب سفارش‌ها
        orders_tab = tk.Frame(tab, bg="white")
        tab.add(orders_tab, text="📦 سفارش‌ها")

        self.orders_tree = ttk.Treeview(orders_tab,
                                         columns=("id", "customer", "total", "time"),
                                         show="headings", height=12)
        self.orders_tree.heading("id",       text="شماره")
        self.orders_tree.heading("customer", text="مشتری")
        self.orders_tree.heading("total",    text="مبلغ")
        self.orders_tree.heading("time",     text="زمان")
        self.orders_tree.column("id",       width=80)
        self.orders_tree.column("customer", width=100)
        self.orders_tree.column("total",    width=100)
        self.orders_tree.column("time",     width=120)
        self.orders_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.orders_tree.bind("<Double-1>", self._show_order_detail)

        self._refresh_menu()
        self._refresh_orders()

    def _darken(self, hex_color):
        """تیره‌تر کردن رنگ برای دکمه خروج"""
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            r = max(0, int(r * 0.8))
            g = max(0, int(g * 0.8))
            b = max(0, int(b * 0.8))
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return "#c0392b"

    def _pick_color(self):
        """باز کردن color picker برای انتخاب رنگ رستوران"""
        manager = self.app.platform.current_user
        # colorchooser پنجره انتخاب رنگ سیستم‌عامل رو باز می‌کنه
        result = colorchooser.askcolor(
            color=manager.restaurant.color,
            title="رنگ رستوران را انتخاب کنید"
        )
        # result یه tuple هست: ((r,g,b), '#rrggbb') یا (None, None)
        if result and result[1]:
            new_color = result[1]
            manager.set_color(new_color)
            self.app.platform.db.update_restaurant_color(
                manager.restaurant.name, new_color
            )
            # rebuild برای اعمال رنگ جدید به هدر
            self.build()

    def _refresh_category_combo(self):
        """آپدیت Combobox دسته‌بندی‌ها"""
        manager = self.app.platform.current_user
        if manager and manager.restaurant:
            self.category_combo["values"] = manager.restaurant.categories
            if self.category_var.get() not in manager.restaurant.categories:
                self.category_var.set("غذا")

    def _refresh_menu(self):
        """نمایش منو گروه‌بندی‌شده"""
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)

        manager = self.app.platform.current_user

        for category in manager.restaurant.categories:
            items_in_cat = [item for item in manager.restaurant.menu
                            if item.category == category]
            if not items_in_cat:
                continue
            # سطر عنوان دسته‌بندی
            self.menu_tree.insert("", "end",
                                   values=(f"── {category} ──", "", ""),
                                   tags=("category_header",))
            for item in items_in_cat:
                self.menu_tree.insert("", "end", values=(
                    item.name,
                    f"{item.price:,}",
                    "✅ موجود" if item.is_available else "❌ ناموجود"
                ))

        self.menu_tree.tag_configure("category_header",
                                      background="#ecf0f1",
                                      font=("Arial", 10, "bold"))

    def _refresh_orders(self):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)
        manager = self.app.platform.current_user
        for order in manager.restaurant.orders:
            self.orders_tree.insert("", "end", values=(
                order.order_id,
                order.customer.username,
                f"{order.total_price():,}",
                order.created_at
            ))

    def _on_select(self, event):
        """پر کردن فرم با آیتم انتخاب‌شده"""
        selected = self.menu_tree.selection()
        if not selected:
            return
        values = self.menu_tree.item(selected[0])["values"]
        if str(values[0]).startswith("──"):
            return

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[0])
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, str(values[1]).replace(",", ""))
        self.available_var.set(True if "✅" in str(values[2]) else False)

        manager = self.app.platform.current_user
        item = manager.restaurant.get_item_by_name(str(values[0]))
        if item:
            self.category_var.set(item.category)

    def _add_item(self):
        name      = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        category  = self.category_var.get()

        if not name:
            messagebox.showerror("خطا", "نام آیتم را وارد کنید.")
            return
        if not price_str.isdigit() or int(price_str) <= 0:
            messagebox.showerror("خطا", "قیمت باید عدد مثبت باشد.")
            return

        manager = self.app.platform.current_user
        success = manager.add_menu_item(name, int(price_str), category)

        if success:
            item = manager.restaurant.get_item_by_name(name)
            item.is_available = self.available_var.get()
            self.app.platform.db.save_menu_item(item, manager.restaurant.name)
            self._refresh_menu()
            self._clear_form()
            messagebox.showinfo("موفقیت", f"آیتم '{name}' در دسته '{category}' اضافه شد.")
        else:
            messagebox.showerror("خطا", f"آیتم '{name}' از قبل وجود دارد.")

    def _edit_item(self):
        name      = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        category  = self.category_var.get()

        if not name:
            messagebox.showerror("خطا", "ابتدا یک آیتم از جدول انتخاب کنید.")
            return
        if not price_str.isdigit() or int(price_str) <= 0:
            messagebox.showerror("خطا", "قیمت باید عدد مثبت باشد.")
            return

        manager = self.app.platform.current_user
        success = manager.edit_menu_item(name, int(price_str),
                                          self.available_var.get(), category)
        if success:
            item = manager.restaurant.get_item_by_name(name)
            self.app.platform.db.update_menu_item(item, manager.restaurant.name)
            self._refresh_menu()
            messagebox.showinfo("موفقیت", f"آیتم '{name}' ویرایش شد.")
        else:
            messagebox.showerror("خطا", f"آیتم '{name}' پیدا نشد.")

    def _delete_item(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("خطا", "ابتدا یک آیتم از جدول انتخاب کنید.")
            return
        if not messagebox.askyesno("تأیید", f"آیتم '{name}' حذف شود؟"):
            return
        manager = self.app.platform.current_user
        if manager.delete_menu_item(name):
            self.app.platform.db.delete_menu_item(name, manager.restaurant.name)
            self._refresh_menu()
            self._clear_form()

    def _open_category_manager(self):
        CategoryManagerWindow(self, self.app,
                               on_close_callback=self._after_category_manager)

    def _after_category_manager(self):
        self._refresh_category_combo()
        self._refresh_menu()

    def _clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.category_var.set("غذا")
        self.available_var.set(True)

    def _show_order_detail(self, event):
        selected = self.orders_tree.selection()
        if not selected:
            return
        order_id = self.orders_tree.item(selected[0])["values"][0]
        manager = self.app.platform.current_user
        order = next((o for o in manager.restaurant.orders
                      if o.order_id == order_id), None)
        if order:
            self._open_detail_window(order)

    def _open_detail_window(self, order):
        win = tk.Toplevel(self)
        win.title(f"جزئیات سفارش {order.order_id}")
        win.geometry("400x450")
        win.configure(bg="#f5f5f5")
        win.grab_set()

        tk.Label(win, text=f"📋 سفارش {order.order_id}",
                 font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

        info = tk.Frame(win, bg="white", relief="ridge", bd=2)
        info.pack(padx=20, fill="x")
        tk.Label(info, text=f"🏪 رستوران: {order.restaurant.name}",
                 font=("Arial", 11), bg="white").pack(anchor="w", padx=10, pady=3)
        tk.Label(info, text=f"👤 مشتری: {order.customer.username}",
                 font=("Arial", 11), bg="white").pack(anchor="w", padx=10, pady=3)
        tk.Label(info, text=f"🕐 زمان: {order.created_at}",
                 font=("Arial", 11), bg="white").pack(anchor="w", padx=10, pady=3)

        tk.Label(win, text="آیتم‌های سفارش:",
                 font=("Arial", 11, "bold"), bg="#f5f5f5").pack(pady=(10, 0))

        tree_frame = tk.Frame(win)
        tree_frame.pack(padx=20, pady=5, fill="both", expand=True)
        item_tree = ttk.Treeview(tree_frame,
                                  columns=("category", "name", "price"),
                                  show="headings", height=6)
        item_tree.heading("category", text="دسته‌بندی")
        item_tree.heading("name",     text="نام آیتم")
        item_tree.heading("price",    text="قیمت")
        item_tree.column("category", width=90)
        item_tree.column("name",     width=150)
        item_tree.column("price",    width=100)
        item_tree.pack(fill="both", expand=True)

        # گروه‌بندی آیتم‌ها بر اساس دسته‌بندی در فاکتور
        from collections import defaultdict
        grouped = defaultdict(list)
        for item in order.items:
            grouped[item.category].append(item)

        for category, items in grouped.items():
            for item in items:
                item_tree.insert("", "end", values=(
                    category,
                    item.name,
                    f"{item.price:,} تومان"
                ))

        tk.Label(win, text=f"💰 مبلغ کل: {order.total_price():,} تومان",
                 font=("Arial", 13, "bold"),
                 bg="#f5f5f5", fg="#e74c3c").pack(pady=10)
        tk.Button(win, text="بستن", font=("Arial", 11),
                  bg="#95a5a6", fg="white", cursor="hand2",
                  command=win.destroy).pack(pady=5)


# ──────────────────────────────────────────
# پنل مشتری
# ──────────────────────────────────────────
class CustomerFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f5f5")
        self.app = app
        self.selected_restaurant = None

    def build(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.selected_restaurant = None
        customer = self.app.platform.current_user

        # هدر
        header = tk.Frame(self, bg="#2ecc71")
        header.pack(fill="x")
        tk.Label(header, text=f"👤 {customer.first_name} {customer.last_name}",
                 font=("Arial", 14, "bold"),
                 bg="#2ecc71", fg="white").pack(side="left", padx=20, pady=10)
        tk.Button(header, text="خروج",
                  font=("Arial", 10), bg="#27ae60", fg="white",
                  bd=0, cursor="hand2",
                  command=self.app.logout).pack(side="right", padx=20)

        main = tk.Frame(self, bg="#f5f5f5")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ── ستون چپ: لیست رستوران‌ها با رنگ هر رستوران ──
        left = tk.Frame(main, bg="white", relief="ridge", bd=2)
        left.pack(side="left", fill="y", padx=(0, 10), ipadx=10)

        tk.Label(left, text="🏪 رستوران‌ها",
                 font=("Arial", 13, "bold"), bg="white").pack(pady=10)

        self.restaurant_buttons_frame = tk.Frame(left, bg="white")
        self.restaurant_buttons_frame.pack(padx=5, pady=5, fill="both", expand=True)

        self._build_restaurant_list()

        # ── ستون راست: تب‌ها ──
        right = tk.Frame(main, bg="white", relief="ridge", bd=2)
        right.pack(side="right", fill="both", expand=True)

        tab = ttk.Notebook(right)
        tab.pack(fill="both", expand=True, padx=10, pady=10)

        # تب منو
        menu_tab = tk.Frame(tab, bg="white")
        tab.add(menu_tab, text="📋 منو")

        self.menu_tree = ttk.Treeview(menu_tab,
                                       columns=("name", "price", "status"),
                                       show="headings", height=10)
        self.menu_tree.heading("name",   text="نام")
        self.menu_tree.heading("price",  text="قیمت")
        self.menu_tree.heading("status", text="وضعیت")
        self.menu_tree.column("name",   width=140)
        self.menu_tree.column("price",  width=90)
        self.menu_tree.column("status", width=100)

        menu_scroll = ttk.Scrollbar(menu_tab, orient="vertical",
                                     command=self.menu_tree.yview)
        self.menu_tree.configure(yscrollcommand=menu_scroll.set)
        self.menu_tree.pack(side="left", fill="both", expand=True, padx=(5,0), pady=5)
        menu_scroll.pack(side="right", fill="y", pady=5)

        tk.Button(menu_tab, text="➕ افزودن به سبد خرید",
                  font=("Arial", 11, "bold"),
                  bg="#2ecc71", fg="white",
                  cursor="hand2",
                  command=self._add_to_cart).pack(pady=8)

        # تب سبد خرید
        cart_tab = tk.Frame(tab, bg="white")
        tab.add(cart_tab, text="🛒 سبد خرید")

        self.cart_tree = ttk.Treeview(cart_tab,
                                       columns=("name", "restaurant", "qty", "price"),
                                       show="headings", height=9)
        self.cart_tree.heading("name",       text="نام")
        self.cart_tree.heading("restaurant", text="رستوران")
        self.cart_tree.heading("qty",        text="تعداد")
        self.cart_tree.heading("price",      text="جمع")
        self.cart_tree.column("name",       width=130)
        self.cart_tree.column("restaurant", width=100)
        self.cart_tree.column("qty",        width=55, anchor="center")
        self.cart_tree.column("price",      width=90)
        self.cart_tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.total_label = tk.Label(cart_tab, text="جمع کل: ۰ تومان",
                                    font=("Arial", 12, "bold"),
                                    bg="white", fg="#e74c3c")
        self.total_label.pack(pady=3)

        btn_cart = tk.Frame(cart_tab, bg="white")
        btn_cart.pack(pady=5)
        tk.Button(btn_cart, text="➕ یکی بیشتر",
                  font=("Arial", 10, "bold"),
                  bg="#2ecc71", fg="white", width=11,
                  cursor="hand2",
                  command=self._increase_qty).pack(side="left", padx=5)
        tk.Button(btn_cart, text="➖ یکی کمتر",
                  font=("Arial", 10, "bold"),
                  bg="#e67e22", fg="white", width=11,
                  cursor="hand2",
                  command=self._decrease_qty).pack(side="left", padx=5)
        tk.Button(btn_cart, text="🗑️ حذف کامل",
                  font=("Arial", 10, "bold"),
                  bg="#e74c3c", fg="white", width=11,
                  cursor="hand2",
                  command=self._remove_from_cart).pack(side="left", padx=5)

        btn_cart2 = tk.Frame(cart_tab, bg="white")
        btn_cart2.pack(pady=3)
        tk.Button(btn_cart2, text="✅ نهایی کردن سفارش",font=("Arial", 11, "bold"),
                  bg="#3498db", fg="white", width=22,
                  cursor="hand2",
                  command=self._checkout).pack()

        # تب تاریخچه
        history_tab = tk.Frame(tab, bg="white")
        tab.add(history_tab, text="📦 تاریخچه سفارش‌ها")

        self.history_tree = ttk.Treeview(history_tab,
                                          columns=("id", "restaurant", "total", "time"),
                                          show="headings", height=10)
        self.history_tree.heading("id",         text="شماره")
        self.history_tree.heading("restaurant", text="رستوران")
        self.history_tree.heading("total",      text="مبلغ")
        self.history_tree.heading("time",       text="زمان")
        self.history_tree.column("id",         width=80)
        self.history_tree.column("restaurant", width=110)
        self.history_tree.column("total",      width=90)
        self.history_tree.column("time",       width=120)
        self.history_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.history_tree.bind("<Double-1>", self._show_order_detail)

        self._refresh_history()

    def _build_restaurant_list(self):
        """ساخت دکمه‌های رستوران با رنگ هر رستوران"""
        for widget in self.restaurant_buttons_frame.winfo_children():
            widget.destroy()

        for restaurant in self.app.platform.restaurants:
            btn = tk.Button(
                self.restaurant_buttons_frame,
                text=f"🏪 {restaurant.name}",
                font=("Arial", 10, "bold"),
                bg=restaurant.color,      # رنگ خود رستوران
                fg="white",
                width=16,
                cursor="hand2",
                relief="flat",
                pady=6,
                command=lambda r=restaurant: self._select_restaurant(r)
            )
            btn.pack(pady=3, padx=5, fill="x")

    def _select_restaurant(self, restaurant):
        """انتخاب رستوران با کلیک روی دکمه‌اش"""
        self.selected_restaurant = restaurant
        self._refresh_menu()

    def _get_cart_item_names(self):
        """برگرداندن نام آیتم‌هایی که توی سبد خرید هستن"""
        customer = self.app.platform.current_user
        return {key[0] for key in customer.cart.keys()}

    def _get_selected_cart_entry(self):
        """گرفتن آیتم انتخاب‌شده از جدول سبد خرید"""
        selected = self.cart_tree.selection()
        if not selected:
            return None, None
        values = self.cart_tree.item(selected[0])["values"]
        item_name = str(values[0])
        restaurant_name = str(values[1])
        return item_name, restaurant_name

    def _increase_qty(self):
        """افزودن یک عدد به تعداد آیتم انتخاب‌شده در سبد"""
        item_name, restaurant_name = self._get_selected_cart_entry()
        if not item_name:
            messagebox.showerror("خطا", "ابتدا یک آیتم از سبد انتخاب کنید.")
            return
        customer = self.app.platform.current_user
        key = (item_name, restaurant_name)
        if key in customer.cart:
            customer.cart[key]["quantity"] += 1
            self._refresh_cart()

    def _decrease_qty(self):
        item_name, restaurant_name = self._get_selected_cart_entry()
        if not item_name:
            messagebox.showerror("خطا", "ابتدا یک آیتم از سبد انتخاب کنید.")
            return
        customer = self.app.platform.current_user
        customer.remove_from_cart(item_name, restaurant_name)
        self._refresh_cart()

    def _refresh_menu(self):
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)
        if not self.selected_restaurant:
            return

        # آیتم‌هایی که الان توی سبد خرید هستن
        cart_items = self._get_cart_item_names()
        rest_color = self.selected_restaurant.color

        for category in self.selected_restaurant.categories:
            items_in_cat = [item for item in self.selected_restaurant.menu
                            if item.category == category]
            if not items_in_cat:
                continue

            # سطر عنوان دسته با رنگ رستوران
            self.menu_tree.insert("", "end",
                                   values=(f"── {category} ──", "", ""),
                                   tags=("category_header",))

            for item in items_in_cat:
                if item.name in cart_items:
                    # آیتم توی سبده - با رنگ رستوران و علامت سبد
                    status = "🛒 در سبد خرید"
                    tag = "in_cart"
                else:
                    status = "✅ موجود" if item.is_available else "❌ ناموجود"
                    tag = "normal"

                self.menu_tree.insert("", "end", values=(
                    item.name,
                    f"{item.price:,}",
                    status
                ), tags=(tag,))

        # استایل‌ها
        self.menu_tree.tag_configure("category_header",
                                      background="#ecf0f1",
                                      font=("Arial", 10, "bold"))
        # آیتم‌های توی سبد با رنگ رستوران هایلایت میشن
        self.menu_tree.tag_configure("in_cart",
                                      background=rest_color,
                                      foreground="white",
                                      font=("Arial", 10, "bold"))
        self.menu_tree.tag_configure("normal", background="white")

    def _refresh_cart(self):
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)
        customer = self.app.platform.current_user
        total = 0
        for entry in customer.cart.values():
            item = entry["item"]
            restaurant = entry["restaurant"]
            qty = entry["quantity"]
            subtotal = item.price * qty
            total += subtotal
            # برای هر رستوران تگ جداگانه با رنگ خودش
            tag_name = f"rest_{restaurant.name}"
            self.cart_tree.insert("", "end", values=(
                item.name,
                restaurant.name,
                f"x{qty}",
                f"{subtotal:,}"
            ), tags=(tag_name,))
            self.cart_tree.tag_configure(tag_name,
                                          background=restaurant.color,
                                          foreground="white",
                                          font=("Arial", 10, "bold"))

        self.total_label.config(text=f"جمع کل: {total:,} تومان")
        self._refresh_menu()

    def _refresh_history(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        customer = self.app.platform.current_user
        for order in customer.order_history:
            self.history_tree.insert("", "end", values=(
                order.order_id,
                order.restaurant.name,
                f"{order.total_price():,}",
                order.created_at
            ))

    def _add_to_cart(self):
        if not self.selected_restaurant:
            messagebox.showerror("خطا", "ابتدا یک رستوران انتخاب کنید.")
            return

        selected = self.menu_tree.selection()
        if not selected:
            messagebox.showerror("خطا", "ابتدا یک آیتم از منو انتخاب کنید.")
            return

        values = self.menu_tree.item(selected[0])["values"]
        if str(values[0]).startswith("──"):
            messagebox.showerror("خطا", "لطفاً یک آیتم انتخاب کنید، نه عنوان دسته‌بندی.")
            return

        if "❌" in str(values[2]):
            messagebox.showerror("خطا", "این آیتم در دسترس نیست.")
            return

        item = self.selected_restaurant.get_item_by_name(str(values[0]))
        customer = self.app.platform.current_user
        customer.add_to_cart(item, self.selected_restaurant)
        self._refresh_cart()
        messagebox.showinfo("موفقیت", f"'{values[0]}' به سبد خرید اضافه شد.")

    def _remove_from_cart(self):
        """حذف کامل آیتم از سبد صرف نظر از تعداد"""
        item_name, restaurant_name = self._get_selected_cart_entry()
        if not item_name:
            messagebox.showerror("خطا", "ابتدا یک آیتم از سبد انتخاب کنید.")
            return
        customer = self.app.platform.current_user
        customer.remove_all_from_cart(item_name, restaurant_name)
        self._refresh_cart()

    def _checkout(self):
        customer = self.app.platform.current_user
        if not customer.cart:
            messagebox.showerror("خطا", "سبد خرید خالی است.")
            return

        total = sum(e["item"].price * e["quantity"] for e in customer.cart.values())
        if not messagebox.askyesno("تأیید",
                                    f"مبلغ کل: {total:,} تومان\nسفارش نهایی شود؟"):
            return

        orders = customer.checkout(self.app.platform._generate_order_id)
        for order in orders:
            self.app.platform.db.save_order(order)

        self._refresh_cart()
        self._refresh_history()
        messagebox.showinfo("موفقیت",
                            f"{len(orders)} سفارش با موفقیت ثبت شد!\nمبلغ: {total:,} تومان")

    def _show_order_detail(self, event):
        selected = self.history_tree.selection()
        if not selected:
            return
        order_id = self.history_tree.item(selected[0])["values"][0]
        customer = self.app.platform.current_user
        order = next((o for o in customer.order_history
                      if o.order_id == order_id), None)
        if not order:
            return

        win = tk.Toplevel(self)
        win.title(f"جزئیات سفارش {order_id}")
        win.geometry("400x450")
        win.configure(bg="#f5f5f5")
        win.grab_set()

        tk.Label(win, text=f"📋 سفارش {order_id}",
                 font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

        info = tk.Frame(win, bg="white", relief="ridge", bd=2)
        info.pack(padx=20, fill="x")
        tk.Label(info, text=f"🏪 رستوران: {order.restaurant.name}",
                 font=("Arial", 11), bg="white").pack(anchor="w", padx=10, pady=3)
        tk.Label(info, text=f"👤 مشتری: {order.customer.username}",
                 font=("Arial", 11), bg="white").pack(anchor="w", padx=10, pady=3)
        tk.Label(info, text=f"🕐 زمان: {order.created_at}",
                 font=("Arial", 11), bg="white").pack(anchor="w", padx=10, pady=3)

        tk.Label(win, text="آیتم‌های سفارش:",
                 font=("Arial", 11, "bold"), bg="#f5f5f5").pack(pady=(10, 0))

        tree_frame = tk.Frame(win)
        tree_frame.pack(padx=20, pady=5, fill="both", expand=True)
        item_tree = ttk.Treeview(tree_frame,
                                  columns=("category", "name", "price"),
                                  show="headings", height=6)
        item_tree.heading("category", text="دسته‌بندی")
        item_tree.heading("name",     text="نام آیتم")
        item_tree.heading("price",    text="قیمت")
        item_tree.column("category", width=90)
        item_tree.column("name",     width=150)
        item_tree.column("price",    width=100)
        item_tree.pack(fill="both", expand=True)

        # گروه‌بندی آیتم‌ها بر اساس دسته‌بندی در فاکتور
        from collections import defaultdict
        grouped = defaultdict(list)
        for item in order.items:
            grouped[item.category].append(item)

        for category, items in grouped.items():
            for item in items:
                item_tree.insert("", "end", values=(
                    category,
                    item.name,
                    f"{item.price:,} تومان"
                ))

        tk.Label(win, text=f"💰 مبلغ کل: {order.total_price():,} تومان",
                 font=("Arial", 13, "bold"),
                 bg="#f5f5f5", fg="#e74c3c").pack(pady=10)
        tk.Button(win, text="بستن", font=("Arial", 11),
                  bg="#95a5a6", fg="white", cursor="hand2",
                  command=win.destroy).pack(pady=5)


# ──────────────────────────────────────────
# کلاس اصلی برنامه
# ──────────────────────────────────────────
class SnappApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Snapp Food")
        self.root.geometry("860x580")
        self.root.configure(bg="#f5f5f5")

        self.platform = Platform()
        self.platform.load_all()

        self.login_frame    = LoginFrame(root, self)
        self.signup_frame   = SignupFrame(root, self)
        self.manager_frame  = ManagerFrame(root, self)
        self.customer_frame = CustomerFrame(root, self)

        self.show_login()

    def show_login(self):
        self.signup_frame.pack_forget()
        self.manager_frame.pack_forget()
        self.customer_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_signup(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack(fill="both", expand=True)

    def show_manager(self):
        self.login_frame.pack_forget()
        self.manager_frame.build()
        self.manager_frame.pack(fill="both", expand=True)

    def show_customer(self):
        self.login_frame.pack_forget()
        self.customer_frame.build()
        self.customer_frame.pack(fill="both", expand=True)

    def logout(self):
        self.platform.current_user = None
        self.show_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = SnappApp(root)
    root.mainloop()