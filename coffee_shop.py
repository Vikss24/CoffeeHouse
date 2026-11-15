import customtkinter as ctk
import sqlite3

# Налаштування теми інтерфейсу
ctk.set_appearance_mode("Світло")
ctk.set_default_color_theme("blue")

class CoffeeShopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Кав'ярня — Система управління")
        self.geometry("1100x700")
        self.minsize(1050, 650)
        self.configure(fg_color="#F5F7FA")

        # --- БІЧНА ПАНЕЛЬ ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="☕ Кав'ярня", 
            font=ctk.CTkFont(size=22, weight="bold"), text_color="white"
        )
        self.logo_label.pack(pady=(30, 20), padx=20)

        # Кнопки навігації на панелі
        self.btn_menu = ctk.CTkButton(
            self.sidebar, text="📋 Меню", command=self.show_menu_frame,
            fg_color="transparent", text_color="white", hover_color="#333333", anchor="w"
        )
        self.btn_menu.pack(pady=10, padx=20, fill="x")

        self.btn_stock = ctk.CTkButton(
            self.sidebar, text="📦 Склад інгредієнтів", command=self.show_stock_frame,
            fg_color="transparent", text_color="white", hover_color="#333333", anchor="w"
        )
        self.btn_stock.pack(pady=10, padx=20, fill="x")

        self.btn_orders = ctk.CTkButton(
            self.sidebar, text="🛒 Замовлення", command=self.show_orders_frame,
            fg_color="transparent", text_color="white", hover_color="#333333", anchor="w"
        )
        self.btn_orders.pack(pady=10, padx=20, fill="x")

        # --- ОСНОВНА ОБЛАСЬ КОНТЕНТУ ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Завантажуємо стартову сторінку (Меню)
        self.show_menu_frame()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_menu_frame(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="Меню кав'ярні", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 15))

        # Фрейм для виведення даних із бази
        box = ctk.CTkTextbox(self.content_frame, width=800, height=500, corner_radius=10)
        box.pack(fill="both", expand=True)

        # Читаємо дані з бази даних coffee_shop.db
        try:
            conn = sqlite3.connect('coffee_shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, price, category FROM menu")
            items = cursor.fetchall()
            conn.close()

            box.insert("end", f"{'Назва позиції':<30} | {'Ціна (грн)':<15} | {'Категорія':<20}\n")
            box.insert("end", "-" * 70 + "\n")
            for item in items:
                box.insert("end", f"{item[0]:<32} | {item[1]:<15} | {item[2]:<20}\n")
        except Exception as e:
            box.insert("end", f"Помилка завантаження бази даних: спочатку запустіть database.py!\nДеталі: {e}")

        box.configure(state="disabled")

    def show_stock_frame(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="Склад інгредієнтів", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 15))

        box = ctk.CTkTextbox(self.content_frame, width=800, height=500, corner_radius=10)
        box.pack(fill="both", expand=True)

        try:
            conn = sqlite3.connect('coffee_shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, quantity, unit FROM ingredients")
            items = cursor.fetchall()
            conn.close()

            box.insert("end", f"{'Інгредієнт':<30} | {'Кількість':<15} | {'Одиниця':<10}\n")
            box.insert("end", "-" * 60 + "\n")
            for item in items:
                box.insert("end", f"{item[0]:<32} | {item[1]:<15} | {item[2]:<10}\n")
        except Exception as e:
            box.insert("end", f"Помилка: {e}")

        box.configure(state="disabled")

    def show_orders_frame(self):
        self.clear_content()
        
        title = ctk.CTkLabel(self.content_frame, text="Управління замовленнями", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 15))

        info = ctk.CTkLabel(self.content_frame, text="Тут з'являтимуться нові замовлення покупців кав'ярні.", font=ctk.CTkFont(size=14))
        info.pack(anchor="w", pady=10)

if __name__ == "__main__":
    app = CoffeeShopApp()
    app.mainloop()
