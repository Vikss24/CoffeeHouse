import sqlite3
import customtkinter as ctk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")


# --- ВІКНО АВТОРИЗАЦІЇ З ВИБОРОМ РОЛІ ---
class LoginWindow(ctk.CTk):

  def __init__(self):
    super().__init__()

    self.title("Coffee House — Вхід у систему")
    self.geometry("400x480")
    self.configure(fg_color="#2D1B12")

    self.grid_columnconfigure(0, weight=1)

    self.logo_label = ctk.CTkLabel(
        self,
        text="☕ Coffee House",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#FFFFFF",
    )
    self.logo_label.grid(row=0, column=0, pady=(35, 10))

    self.subtitle_label = ctk.CTkLabel(
        self,
        text="Система управління кав'ярнею",
        font=ctk.CTkFont(size=12, slant="italic"),
        text_color="#D7CCC8",
    )
    self.subtitle_label.grid(row=1, column=0, pady=(0, 25))

    self.login_entry = ctk.CTkEntry(
        self,
        placeholder_text="Логін",
        width=260,
        height=40,
        fg_color="#F5ECE1",
        text_color="#3D2314",
        border_color="#6F4E37",
    )
    self.login_entry.grid(row=2, column=0, pady=10)

    self.pass_entry = ctk.CTkEntry(
        self,
        placeholder_text="Пароль",
        show="*",
        width=260,
        height=40,
        fg_color="#F5ECE1",
        text_color="#3D2314",
        border_color="#6F4E37",
    )
    self.pass_entry.grid(row=3, column=0, pady=10)

    self.error_label = ctk.CTkLabel(
        self, text="", font=ctk.CTkFont(size=12), text_color="#FF6B6B"
    )
    self.error_label.grid(row=4, column=0, pady=5)

    self.login_btn = ctk.CTkButton(
        self,
        text="Увійти",
        command=self.check_login,
        width=260,
        height=40,
        fg_color="#6F4E37",
        hover_color="#5A3D28",
        font=ctk.CTkFont(size=14, weight="bold"),
    )
    self.login_btn.grid(row=5, column=0, pady=(10, 15))

    self.hint_label = ctk.CTkLabel(
        self,
        text="Працівник: admin / 123\nКористувач: user / 111",
        font=ctk.CTkFont(size=11),
        text_color="#BCAAA4",
    )
    self.hint_label.grid(row=6, column=0, pady=(0, 20))

  def check_login(self):
    login = self.login_entry.get().strip()
    password = self.pass_entry.get().strip()

    if login == "admin" and password == "123":
      self.destroy()
      app = CoffeeShopApp(role="worker")
      app.mainloop()
    elif login == "user" and password == "111":
      self.destroy()
      app = CoffeeShopApp(role="client")
      app.mainloop()
    else:
      self.error_label.configure(text="Неправильний логін або пароль!")


# --- ГОЛОВНЕ ВІКНО ДОДАТКУ ---
class CoffeeShopApp(ctk.CTk):

  def __init__(self, role="client"):
    super().__init__()

    self.role = role
    title_suffix = (
        "Панель працівника" if self.role == "worker" else "Меню користувача"
    )
    self.title(f"Coffee House — {title_suffix}")
    self.geometry("1150x700")
    self.configure(fg_color="#F5ECE1")

    self.cart = []
    self.current_category = "Усі"

    self.grid_columnconfigure(1, weight=1)
    self.grid_rowconfigure(0, weight=1)

    # --- 1. БІЧНА ПАНЕЛЬ НАВІГАЦІЇ ---
    self.sidebar_frame = ctk.CTkFrame(
        self, width=220, fg_color="#2D1B12", corner_radius=0
    )
    self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
    self.sidebar_frame.grid_rowconfigure(9, weight=1)

    self.logo_label = ctk.CTkLabel(
        self.sidebar_frame,
        text="☕ Coffee House",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color="#FFFFFF",
    )
    self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")

    role_text = (
        "👤 Режим: Працівник"
        if self.role == "worker"
        else "👤 Режим: Користувач"
    )
    self.role_label = ctk.CTkLabel(
        self.sidebar_frame,
        text=role_text,
        font=ctk.CTkFont(size=12, slant="italic"),
        text_color="#D7CCC8",
    )
    self.role_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

    if self.role == "worker":
      nav_buttons = [
          ("📦 Склад інгредієнтів", self.show_inventory),
          ("🛒 Закупівлі", self.show_purchases_view),
          ("👥 Список працівників", self.show_employees_view),
      ]
    else:
      nav_buttons = [
          ("🏠 Меню кав'ярні", self.show_menu),
          ("📋 Історія замовлень", self.show_orders_view),
      ]

    for idx, (text, command) in enumerate(nav_buttons, start=2):
      btn = ctk.CTkButton(
          self.sidebar_frame,
          text=text,
          fg_color="transparent",
          hover_color="#4A2E1B",
          anchor="w",
          font=ctk.CTkFont(size=14),
          text_color="#FFFFFF",
          command=command,
      )
      btn.grid(row=idx, column=0, padx=15, pady=8, sticky="ew")

    self.exit_btn = ctk.CTkButton(
        self.sidebar_frame,
        text="🚪 Змінити акаунт",
        fg_color="#8D4004",
        hover_color="#A04A05",
        text_color="#FFFFFF",
        command=self.logout,
    )
    self.exit_btn.grid(row=10, column=0, padx=20, pady=20, sticky="ew")

    # --- 2. ЦЕНТРАЛЬНА ЧАСТИНА ---
    self.main_area = ctk.CTkFrame(self, fg_color="#F9F6F0", corner_radius=0)
    self.main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    self.main_area.grid_columnconfigure(0, weight=1)
    self.main_area.grid_rowconfigure(2, weight=1)

    self.header_label = ctk.CTkLabel(
        self.main_area,
        text="",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#3D2314",
    )
    self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

    self.filter_frame = ctk.CTkFrame(
        self.main_area, fg_color="transparent", height=40
    )
    self.filter_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

    self.catalog_frame = ctk.CTkScrollableFrame(
        self.main_area, fg_color="transparent"
    )
    self.catalog_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    # --- 3. ПРАВА ПАНЕЛЬ (КОШИК) — Тільки для користувача ---
    if self.role == "client":
      self.cart_frame = ctk.CTkFrame(
          self, width=280, fg_color="#FFFFFF", corner_radius=10
      )
      self.cart_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
      self.cart_frame.grid_rowconfigure(1, weight=1)

      self.cart_title = ctk.CTkLabel(
          self.cart_frame,
          text="🛒 Ваше замовлення",
          font=ctk.CTkFont(size=18, weight="bold"),
          text_color="#3D2314",
      )
      self.cart_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

      self.cart_list_frame = ctk.CTkScrollableFrame(
          self.cart_frame, fg_color="#F9F6F0"
      )
      self.cart_list_frame.grid(
          row=1, column=0, sticky="nsew", padx=15, pady=5
      )

      self.total_label = ctk.CTkLabel(
          self.cart_frame,
          text="Разом: 0 грн",
          font=ctk.CTkFont(size=16, weight="bold"),
          text_color="#3D2314",
      )
      self.total_label.grid(row=2, column=0, padx=20, pady=15, sticky="w")

      self.checkout_btn = ctk.CTkButton(
          self.cart_frame,
          text="Оформити замовлення",
          fg_color="#6F4E37",
          hover_color="#5A3D28",
          height=40,
          font=ctk.CTkFont(size=14, weight="bold"),
          command=self.checkout,
      )
      self.checkout_btn.grid(
          row=3, column=0, padx=20, pady=(0, 20), sticky="ew"
      )

      self.show_menu()
    else:
      self.show_inventory()

  def logout(self):
    self.destroy()
    login_app = LoginWindow()
    login_app.mainloop()

  def clear_content(self):
    for widget in self.catalog_frame.winfo_children():
      widget.destroy()
    for widget in self.filter_frame.winfo_children():
      widget.destroy()

  def show_menu(self):
    self.header_label.configure(text="Меню кав'ярні")
    self.clear_content()

    categories = ["Усі", "coffee", "tea", "dessert", "bakery"]
    for cat in categories:
      btn = ctk.CTkButton(
          self.filter_frame,
          text=cat.capitalize(),
          fg_color="#D7CCC8" if cat != self.current_category else "#6F4E37",
          text_color="#3D2314" if cat != self.current_category else "#FFFFFF",
          hover_color="#BCAAA4",
          height=30,
          command=lambda c=cat: self.filter_menu(c),
      )
      btn.pack(side="left", padx=5)

    self.load_menu_cards()

  def filter_menu(self, category):
    self.current_category = category
    self.show_menu()

  def load_menu_cards(self):
    for widget in self.catalog_frame.winfo_children():
      widget.destroy()

    try:
      conn = sqlite3.connect("coffee_shop.db")
      cursor = conn.cursor()
      if self.current_category == "Усі":
        cursor.execute("SELECT name, price, type FROM menu")
      else:
        cursor.execute(
            "SELECT name, price, type FROM menu WHERE type = ?",
            (self.current_category,),
        )
      items = cursor.fetchall()
      conn.close()
    except Exception:
      items = []

    row, col = 0, 0
    for name, price, category in items:
      card = ctk.CTkFrame(
          self.catalog_frame,
          width=190,
          height=160,
          fg_color="#FFFFFF",
          corner_radius=12,
      )
      card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
      card.grid_propagate(False)

      lbl_name = ctk.CTkLabel(
          card,
          text=name,
          font=ctk.CTkFont(size=13, weight="bold"),
          text_color="#3D2314",
          wraplength=170,
      )
      lbl_name.pack(padx=5, pady=(15, 2))

      lbl_cat = ctk.CTkLabel(
          card, text=f"Тип: {category}", font=ctk.CTkFont(size=11), text_color="#8C7865"
      )
      lbl_cat.pack(padx=5, pady=2)

      lbl_price = ctk.CTkLabel(
          card,
          text=f"{price:.2f} грн",
          font=ctk.CTkFont(size=13, weight="bold"),
          text_color="#6F4E37",
      )
      lbl_price.pack(padx=5, pady=2)

      btn_add = ctk.CTkButton(
          card,
          text="+ Додати",
          fg_color="#6F4E37",
          hover_color="#5A3D28",
          height=26,
          font=ctk.CTkFont(size=12),
          command=lambda n=name, p=price: self.add_to_cart(n, p),
      )
      btn_add.pack(padx=15, pady=(5, 10), fill="x")

      col += 1
      if col > 2:
        col = 0
        row += 1

  def add_to_cart(self, name, price):
    self.cart.append({"name": name, "price": price})
    self.update_cart_display()

  def update_cart_display(self):
    for widget in self.cart_list_frame.winfo_children():
      widget.destroy()

    total = 0
    for item in self.cart:
      total += item["price"]
      lbl = ctk.CTkLabel(
          self.cart_list_frame,
          text=f"{item['name']} — {item['price']:.2f} грн",
          font=ctk.CTkFont(size=12),
          text_color="#3D2314",
      )
      lbl.pack(anchor="w", pady=2)

    self.total_label.configure(text=f"Разом: {total:.2f} грн")

  def checkout(self):
    if not self.cart:
      return
    try:
      conn = sqlite3.connect("coffee_shop.db")
      cursor = conn.cursor()
      total_sum = sum(item["price"] for item in self.cart)
      items_str = ", ".join([item["name"] for item in self.cart])
      cursor.execute(
          "INSERT INTO orders (menu_id, quantity, payment) VALUES (?, ?, ?)",
          (1, len(self.cart), "card"),
      )
      conn.commit()
      conn.close()
    except Exception:
      pass

    self.cart.clear()
    self.update_cart_display()
    self.show_orders_view()

  def show_inventory(self):
    self.header_label.configure(text="Склад інгредієнтів")
    self.clear_content()

    try:
      conn = sqlite3.connect("coffee_shop.db")
      cursor = conn.cursor()
      cursor.execute("SELECT ingredient_id, name, unit FROM ingredients")
      items = cursor.fetchall()
      conn.close()
    except Exception:
      items = []

    header_frame = ctk.CTkFrame(
        self.catalog_frame, fg_color="#6F4E37", corner_radius=6
    )
    header_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(
        header_frame,
        text="ID",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF",
        width=80,
        anchor="center",
    ).pack(side="left", padx=10, pady=8)
    ctk.CTkLabel(
        header_frame,
        text="Назва інгредієнта",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF",
        width=250,
        anchor="w",
    ).pack(side="left", padx=15, pady=8)
    ctk.CTkLabel(
        header_frame,
        text="Одиниця",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF",
        width=100,
        anchor="center",
    ).pack(side="left", padx=10, pady=8)

    for ing_id, name, unit in items:
      row_frame = ctk.CTkFrame(
          self.catalog_frame, fg_color="#FFFFFF", corner_radius=6
      )
      row_frame.pack(fill="x", padx=10, pady=4)

      ctk.CTkLabel(
          row_frame,
          text=str(ing_id),
          font=ctk.CTkFont(size=13),
          text_color="#3D2314",
          width=80,
          anchor="center",
      ).pack(side="left", padx=10, pady=8)
      ctk.CTkLabel(
          row_frame,
          text=name,
          font=ctk.CTkFont(size=13),
          text_color="#3D2314",
          width=250,
          anchor="w",
      ).pack(side="left", padx=15, pady=8)
      ctk.CTkLabel(
          row_frame,
          text=unit,
          font=ctk.CTkFont(size=13),
          text_color="#3D2314",
          width=100,
          anchor="center",
      ).pack(side="left", padx=10, pady=8)

  def show_purchases_view(self):
    self.header_label.configure(text="Облік закупівель")
    self.clear_content()

    try:
      conn = sqlite3.connect("coffee_shop.db")
      cursor = conn.cursor()
      cursor.execute(
          "SELECT id, date, ingredient_id, quantity, unit, price, total FROM purchases"
      )
      purchases = cursor.fetchall()
      conn.close()
    except Exception:
      purchases = []

    if not purchases:
      lbl = ctk.CTkLabel(
          self.catalog_frame,
          text="Закупівель поки немає.",
          font=ctk.CTkFont(size=14),
          text_color="#8C7865",
      )
      lbl.pack(pady=40)
      return

    for p_id, date, ing_id, qty, unit, price, total in purchases:
      card = ctk.CTkFrame(self.catalog_frame, fg_color="#FFFFFF", corner_radius=8)
      card.pack(fill="x", padx=10, pady=5)
      ctk.CTkLabel(
          card,
          text=f"📦 Закупівля #{p_id} | Інгредієнт ID: {ing_id} — {qty} {unit}",
          font=ctk.CTkFont(size=13, weight="bold"),
          text_color="#3D2314",
      ).pack(anchor="w", padx=15, pady=(10, 2))
      ctk.CTkLabel(
          card,
          text=f"💰 Ціна за од.: {price} грн | Всього: {total:.2f} грн | Дата: {date}",
          font=ctk.CTkFont(size=12),
          text_color="#6F4E37",
      ).pack(anchor="w", padx=15, pady=(2, 10))

  def show_orders_view(self):
    self.header_label.configure(text="Історія замовлень")
    self.clear_content()

    try:
      conn = sqlite3.connect("coffee_shop.db")
      cursor = conn.cursor()
      cursor.execute("SELECT id, menu_id, quantity, payment, date FROM orders")
      orders = cursor.fetchall()
      conn.close()
    except Exception:
      orders = []

    if not orders:
      lbl = ctk.CTkLabel(
          self.catalog_frame,
          text="Тут поки немає оформлених замовлень.",
        font=ctk.CTkFont(size=14),
          text_color="#8C7865",
      )
      lbl.pack(pady=40)
      return

    for o_id, m_id, qty, payment, date in orders:
      card = ctk.CTkFrame(self.catalog_frame, fg_color="#FFFFFF", corner_radius=8)
      card.pack(fill="x", padx=10, pady=5)

      ctk.CTkLabel(
          card,
          text=f"📋 Замовлення #{o_id} (Меню ID: {m_id}) — Кількість: {qty}",
          font=ctk.CTkFont(size=13, weight="bold"),
          text_color="#3D2314",
      ).pack(anchor="w", padx=15, pady=(10, 2))
      ctk.CTkLabel(
          card,
          text=f"💳 Оплата: {payment}  |  🕒 Дата: {date}",
          font=ctk.CTkFont(size=12),
          text_color="#6F4E37",
      ).pack(anchor="w", padx=15, pady=(2, 10))

  def show_employees_view(self):
    self.header_label.configure(text="Працівники кав'ярні")
    self.clear_content()

    try:
      conn = sqlite3.connect("coffee_shop.db")
      cursor = conn.cursor()
      cursor.execute("SELECT full_name, position, phone FROM employees")
      employees = cursor.fetchall()
      conn.close()
    except Exception:
      employees = []

    header_frame = ctk.CTkFrame(
        self.catalog_frame, fg_color="#6F4E37", corner_radius=6
    )
    header_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(
        header_frame,
        text="ПІБ працівника",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF",
        width=250,
        anchor="w",
    ).pack(side="left", padx=15, pady=8)
    ctk.CTkLabel(
        header_frame,
        text="Посада",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF",
        width=150,
        anchor="center",
    ).pack(side="left", padx=10, pady=8)
    ctk.CTkLabel(
        header_frame,
        text="Телефон",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color="#FFFFFF",
        width=150,
        anchor="center",
    ).pack(side="left", padx=10, pady=8)

    for full_name, position, phone in employees:
      row_frame = ctk.CTkFrame(
          self.catalog_frame, fg_color="#FFFFFF", corner_radius=6
      )
      row_frame.pack(fill="x", padx=10, pady=4)

      ctk.CTkLabel(
          row_frame,
          text=full_name,
          font=ctk.CTkFont(size=13),
          text_color="#3D2314",
          width=250,
          anchor="w",
      ).pack(side="left", padx=15, pady=8)
      ctk.CTkLabel(
          row_frame,
          text=position,
          font=ctk.CTkFont(size=13),
          text_color="#3D2314",
          width=150,
          anchor="center",
      ).pack(side="left", padx=10, pady=8)
      ctk.CTkLabel(
          row_frame,
          text=phone,
          font=ctk.CTkFont(size=13),
          text_color="#3D2314",
          width=150,
          anchor="center",
      ).pack(side="left", padx=10, pady=8)


if __name__ == "__main__":
  login_app = LoginWindow()
  login_app.mainloop()
