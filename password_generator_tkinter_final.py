import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import pyperclip
import json
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x600")

        # Установка иконки для окна
        icon_path = "C:/Users/lozov/OneDrive/Рабочий стол/PasswordGenerator/password_icon.ico"
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"Не удалось загрузить иконку: {e}")
        else:
            print(f"Файл иконки не найден по пути: {icon_path}")

        # Загрузка сохранённой темы
        self.current_theme = self.load_settings()

        # Устанавливаем фон
        self.root.configure(bg="#121212" if self.current_theme == "dark" else "#F5F5F5")

        # Основной контейнер для страниц
        self.main_frame = tk.Frame(root, bg="#121212" if self.current_theme == "dark" else "#F5F5F5")
        self.main_frame.pack(fill="both", expand=True)

        # Контейнеры для страниц
        self.home_page = tk.Frame(self.main_frame, bg="#121212" if self.current_theme == "dark" else "#F5F5F5")
        self.settings_page = tk.Frame(self.main_frame, bg="#121212" if self.current_theme == "dark" else "#F5F5F5")

        # Разрешенные символы
        self.allowed_letters = ''.join([c for c in string.ascii_letters if c not in 'Oo'])
        self.allowed_digits = '123456789'
        self.allowed_chars = self.allowed_letters + self.allowed_digits

        # Текущий формат и список шаблонов
        self.current_format = tk.StringVar(value="XXX-XXX-XXX")
        self.current_password = ""

        # Настройка стилей
        self.style = ttk.Style()
        self.configure_styles()

        # Инициализация страниц
        self.create_home_page()
        self.create_settings_page()

        # Показываем главную страницу
        self.show_home_page()

    def configure_styles(self):
        # Стиль для кнопок на главной странице
        self.style.configure("Custom.TButton", font=("Roboto", 14), padding=10)
        self.style.map("Custom.TButton", background=[("active", "#1565C0" if self.current_theme == "dark" else "#0277BD")])

        # Стиль для кнопки "Done"
        self.style.configure("DoneButton.TButton", font=("Roboto", 14), padding=10)
        self.style.map("DoneButton.TButton", background=[("active", "#1565C0" if self.current_theme == "dark" else "#0277BD")])

        # Стиль для кнопок "Dark" и "Light"
        self.style.configure("ThemeButton.TButton", font=("Roboto", 14), padding=10)
        self.style.map("ThemeButton.TButton", background=[("active", "#90CAF9" if self.current_theme == "dark" else "#64B5F6")])

        # Стиль для OptionMenu
        self.style.configure("Custom.TMenubutton", font=("Roboto", 12), padding=5)
        self.style.configure("Custom.TMenu", font=("Roboto", 12), padding=5)

    def load_settings(self):
        config_dir = os.path.join(os.getcwd(), "Config")
        config_file = os.path.join(config_dir, "settings.json")
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                settings = json.load(f)
                return settings.get("theme", "dark")
        return "dark"  # По умолчанию тёмная тема

    def save_settings(self):
        config_dir = os.path.join(os.getcwd(), "Config")
        config_file = os.path.join(config_dir, "settings.json")
        try:
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            with open(config_file, "w") as f:
                json.dump({"theme": self.current_theme}, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def apply_theme(self):
        text_color = "#E0E0E0" if self.current_theme == "dark" else "#212121"
        bg_color = "#121212" if self.current_theme == "dark" else "#F5F5F5"
        button_color = "#1976D2" if self.current_theme == "dark" else "#0288D1"
        button_active = "#1565C0" if self.current_theme == "dark" else "#0277BD"
        settings_button_color = "#BBDEFB" if self.current_theme == "dark" else "#90CAF9"
        settings_button_active = "#90CAF9" if self.current_theme == "dark" else "#64B5F6"
        menu_bg = "#666666" if self.current_theme == "dark" else "#E0E0E0"
        menu_fg = "white" if self.current_theme == "dark" else "black"

        # Обновляем фон
        self.root.configure(bg=bg_color)
        self.main_frame.configure(bg=bg_color)
        self.home_page.configure(bg=bg_color)
        self.settings_page.configure(bg=bg_color)

        # Обновляем цвета на главной странице
        self.title_label.config(fg=text_color, bg=bg_color)
        self.style.configure("Custom.TButton", background=button_color)
        self.style.map("Custom.TButton", background=[("active", button_active)])
        self.style.configure("Custom.TMenubutton", background=menu_bg, foreground=menu_fg)
        self.style.configure("Custom.TMenu", background=menu_bg, foreground=menu_fg)
        self.password_entry.config(fg=text_color, bg=bg_color, insertbackground=text_color)
        self.password_frame.config(bg=bg_color)

        # Обновляем цвета на странице настроек
        self.theme_label.config(fg=text_color, bg=bg_color)
        self.theme_frame.config(bg=bg_color)
        self.style.configure("ThemeButton.TButton", background=settings_button_color, foreground=text_color)
        self.style.map("ThemeButton.TButton", background=[("active", settings_button_active)])
        self.style.configure("DoneButton.TButton", background=button_color)
        self.style.map("DoneButton.TButton", background=[("active", button_active)])

    def create_home_page(self):
        # Заголовок
        self.title_label = tk.Label(self.home_page, text="Password Generator", font=("Roboto", 32, "bold"), bg="#121212" if self.current_theme == "dark" else "#F5F5F5")
        self.title_label.pack(pady=50)

        # Кнопка настроек (иконка)
        self.settings_icon = ttk.Button(self.home_page, text=" ⚙️ ", command=self.show_settings_page, style="Custom.TButton")
        self.settings_icon.pack(anchor="ne", padx=10, pady=10)

        # Кнопка генерации
        self.generate_button = ttk.Button(self.home_page, text="  Generate Password  ", command=self.generate_password, style="Custom.TButton")
        self.generate_button.pack(pady=40, padx=20)

        # Поле для пароля и выпадающий список шаблонов
        self.password_frame = tk.Frame(self.home_page, bg="#121212" if self.current_theme == "dark" else "#F5F5F5")
        self.password_frame.pack(pady=40)
        self.password_entry = tk.Entry(self.password_frame, width=20, font=("Roboto", 16), justify="center")
        self.password_entry.pack(side="left")
        self.template_menu = ttk.OptionMenu(self.password_frame, self.current_format, "XXX-XXX-XXX", "XXX-XXX-XXX", "XXXX-XXXX", command=self.select_template, style="Custom.TMenubutton")
        self.template_menu.pack(side="left", padx=10)

        # Кнопка копирования
        self.copy_button = ttk.Button(self.home_page, text="  Copy Password  ", command=self.copy_password, style="Custom.TButton")
        self.copy_button.pack(pady=40, padx=20)

    def create_settings_page(self):
        # Заголовок настроек
        self.theme_label = tk.Label(self.settings_page, text="Choose Theme", font=("Roboto", 24, "bold"), bg="#121212" if self.current_theme == "dark" else "#F5F5F5")
        self.theme_label.pack(pady=80)

        # Кнопки выбора темы
        self.theme_frame = tk.Frame(self.settings_page, bg="#121212" if self.current_theme == "dark" else "#F5F5F5")
        self.theme_frame.pack(pady=50)
        self.dark_button = ttk.Button(self.theme_frame, text="  Dark  ", command=lambda: self.set_theme("dark"), style="ThemeButton.TButton")
        self.dark_button.pack(side="left", padx=20, pady=10)
        self.light_button = ttk.Button(self.theme_frame, text="  Light  ", command=lambda: self.set_theme("light"), style="ThemeButton.TButton")
        self.light_button.pack(side="left", padx=20, pady=10)

        # Кнопка "Готово"
        self.done_button = ttk.Button(self.settings_page, text="  Done  ", command=self.show_home_page, style="DoneButton.TButton")
        self.done_button.pack(pady=50, padx=20)

    def show_home_page(self):
        self.settings_page.pack_forget()
        self.home_page.pack(fill="both", expand=True)
        self.apply_theme()

    def show_settings_page(self):
        self.home_page.pack_forget()
        self.settings_page.pack(fill="both", expand=True)
        self.apply_theme()

    def generate_password(self):
        format_value = self.current_format.get()
        if format_value == "XXX-XXX-XXX":
            parts = [''.join(random.choice(self.allowed_chars) for _ in range(3)) for _ in range(3)]
            password = '-'.join(parts)
        else:  # XXXX-XXXX
            parts = [''.join(random.choice(self.allowed_chars) for _ in range(4)) for _ in range(2)]
            password = '-'.join(parts)

        self.current_password = password
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_password(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

    def select_template(self, value):
        self.current_format.set(value)
        self.generate_password()

    def set_theme(self, theme):
        self.current_theme = theme
        self.apply_theme()
        self.save_settings()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()