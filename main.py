import tkinter as tk
from tkinter import messagebox, simpledialog
from Base import SecuritySystem

class SecuritySystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система безопасности")
        self.root.configure(bg="#1c1c1c")
        self.security_system = SecuritySystem(self.root)

        self.main_frame = tk.Frame(self.root, bg="#1c1c1c")
        self.main_frame.pack(padx=20, pady=20)

        self.create_login_interface()

    def create_login_interface(self):
        """Создание интерфейса авторизации."""
        # Установка размеров и центровка окна
        window_width = 500
        window_height = 240
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Увеличенные шрифты
        label_font = ("Arial", 14)
        entry_font = ("Arial", 12)
        button_font = ("Arial", 14)
        label_fg = "#ffffff"
        entry_bg = "#333333"
        entry_fg = "#ffffff"
        button_bg = "#444444"
        button_fg = "#ffffff"

        # Поле ввода имени пользователя
        tk.Label(self.main_frame, text="Имя пользователя:", font=label_font, fg=label_fg, bg="#1c1c1c").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.username_entry = tk.Entry(self.main_frame, font=entry_font, bg=entry_bg, fg=entry_fg, insertbackground="#ffffff", width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        # Поле ввода пароля
        tk.Label(self.main_frame, text="Пароль:", font=label_font, fg=label_fg, bg="#1c1c1c").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.password_entry = tk.Entry(self.main_frame, show="*", font=entry_font, bg=entry_bg, fg=entry_fg, insertbackground="#ffffff", width=25)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Кнопка входа
        tk.Button(
            self.main_frame, text="Войти", font=button_font, bg=button_bg, fg=button_fg, width=20, command=self.authenticate_user
        ).grid(row=2, columnspan=2, pady=20)

    def authenticate_user(self):
        """Аутентификация пользователя."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.security_system.db.authenticate_user(username, password)

        if role:
            messagebox.showinfo("Успешный вход", f"Добро пожаловать, {username} ({role[0]})")
            self.show_dashboard(username, role[0])
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def show_dashboard(self, username, role):
        """Отображение панели управления."""
        # Очистка текущих виджетов
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Увеличенные шрифты
        label_font = ("Arial", 16, "bold")
        button_font = ("Arial", 14)
        label_fg = "#ffffff"
        button_bg = "#444444"
        button_fg = "#ffffff"

        # Информация о пользователе
        tk.Label(
            self.main_frame,
            text=f"Пользователь: {username} ({role})", font=label_font, fg=label_fg, bg="#1c1c1c"
        ).pack(pady=10)

        # Создание кнопок в зависимости от роли пользователя
        def create_button(text, command):
            tk.Button(
                self.main_frame,
                text=text,
                font=button_font,
                bg=button_bg,
                fg=button_fg,
                width=30,
                height=1,
                command=command
            ).pack(pady=10)

        match role:
            case "personal manager":
                create_button("Удалить пользователя", self.delete_user)
                create_button("Добавить пользователя", self.add_user)
                create_button("Выйти", self.create_login_interface)

            case "admin":
                create_button("Изменить пороговые значения", self.change_thresholds)
                create_button("Просмотреть значения датчиков", self.view_sensor_data)
                create_button("Эмулировать показания датчиков", self.emulate_sensors)
                create_button("Выйти", self.create_login_interface)

            case _:
                create_button("Просмотреть значения датчиков", self.view_sensor_data)
                create_button("Эмулировать показания датчиков", self.emulate_sensors)
                create_button("Выйти", self.create_login_interface)

        # Автоматическая настройка размеров окна
        self.root.update_idletasks()  # Обновление содержимого
        self.root.geometry("")  # Окно автоматически подстраивается под содержимое

    def add_user(self):
        """Добавление нового пользователя."""
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Добавить пользователя")

        add_user_window.configure(bg="#1c1c1c")

        # Устанавливаем положение окна
        window_width = 400
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        add_user_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Увеличенные шрифты
        label_font = ("Arial", 14)
        entry_font = ("Arial", 12)
        button_font = ("Arial", 14)
        label_fg = "#ffffff"
        entry_bg = "#333333"
        entry_fg = "#ffffff"
        button_bg = "#444444"
        button_fg = "#ffffff"

        # Поле ввода имени пользователя
        tk.Label(add_user_window, text="Имя пользователя:", font=label_font, fg=label_fg, bg="#1c1c1c").grid(row=0, column=0, pady=10,
                                                                                               padx=10, sticky="w")
        username_entry = tk.Entry(add_user_window, font=entry_font, bg=entry_bg, fg=entry_fg,
                                  insertbackground="#ffffff", width=25)
        username_entry.grid(row=0, column=1, pady=10, padx=10)

        # Поле ввода пароля
        tk.Label(add_user_window, text="Пароль:", font=label_font, fg=label_fg, bg="#1c1c1c").grid(row=1, column=0, pady=10, padx=10,
                                                                                     sticky="w")
        password_entry = tk.Entry(add_user_window, show="*", font=entry_font, bg=entry_bg, fg=entry_fg,
                                  insertbackground="#ffffff", width=25)
        password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Поле ввода роли
        tk.Label(add_user_window, text="Роль (admin, user, personal manager):", font=label_font, fg=label_fg, bg="#1c1c1c").grid(
            row=2, column=0, pady=10, padx=10, sticky="w")
        role_entry = tk.Entry(add_user_window, font=entry_font, bg=entry_bg, fg=entry_fg, insertbackground="#ffffff",
                              width=25)
        role_entry.grid(row=2, column=1, pady=10, padx=10)

        def submit_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_entry.get()
            if role in ["admin", "user", "personal manager"]:
                self.security_system.db.add_user(username, password, role)
                messagebox.showinfo("Успех", f"Пользователь '{username}' добавлен как '{role}'.")
                add_user_window.destroy()  # Закрыть окно после успешного добавления
            else:
                messagebox.showerror("Ошибка", "Некорректная роль.")

        # Кнопка для подтверждения
        tk.Button(add_user_window, text="Добавить пользователя", font=button_font, bg=button_bg, fg=button_fg, width=20,
                  command=submit_user).grid(row=3, columnspan=2, pady=20)

        # Обновляем размер окна под содержимое
        add_user_window.update_idletasks()
        add_user_window.geometry('')  # Окно будет адаптироваться к размеру содержимого

    def delete_user(self):
        """Удаление пользователя."""
        delete_user_window = tk.Toplevel(self.root)
        delete_user_window.title("Удалить пользователя")

        delete_user_window.configure(bg="#1c1c1c")  # Темный фон

        # Устанавливаем положение окна
        window_width = 400
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        delete_user_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Увеличенные шрифты
        label_font = ("Arial", 14)
        entry_font = ("Arial", 12)
        button_font = ("Arial", 14)
        label_fg = "#ffffff"
        entry_bg = "#333333"
        entry_fg = "#ffffff"
        button_bg = "#444444"
        button_fg = "#ffffff"

        # Поле ввода имени пользователя
        tk.Label(delete_user_window, text="Имя пользователя:", font=label_font, fg=label_fg, bg="#1c1c1c").grid(row=0, column=0,
                                                                                                  pady=10, padx=10,
                                                                                                  sticky="w")
        username_entry = tk.Entry(delete_user_window, font=entry_font, bg=entry_bg, fg=entry_fg,
                                  insertbackground="#000000", width=25)
        username_entry.grid(row=0, column=1, pady=10, padx=10)

        # Поле ввода роли (опционально)
        tk.Label(delete_user_window, text="Роль (опционально):", font=label_font, fg=label_fg, bg="#1c1c1c").grid(row=1, column=0,
                                                                                                    pady=10, padx=10,
                                                                                                    sticky="w")
        role_entry = tk.Entry(delete_user_window, font=entry_font, bg=entry_bg, fg=entry_fg, insertbackground="#000000",
                              width=25)
        role_entry.grid(row=1, column=1, pady=10, padx=10)

        def submit_delete_user():
            username = username_entry.get()
            role = role_entry.get() if role_entry.get() else None
            if username:
                self.security_system.db.delete_user(username, role)
                messagebox.showinfo("Успех", f"Пользователь '{username}' с ролью '{role or 'все роли'}' удалён.")
                delete_user_window.destroy()  # Закрыть окно после успешного удаления
            else:
                messagebox.showerror("Ошибка", "Имя пользователя не указано.")

        # Кнопка для подтверждения
        tk.Button(delete_user_window, text="Удалить пользователя", font=button_font, bg=button_bg, fg=button_fg,
                  width=20, command=submit_delete_user).grid(row=2, columnspan=2, pady=20)

        # Обновляем размер окна под содержимое
        delete_user_window.update_idletasks()
        delete_user_window.geometry('')  # Окно будет адаптироваться к размеру содержимого

    def change_thresholds(self):
        """Изменение пороговых значений датчиков."""
        change_thresholds_window = tk.Toplevel(self.root)
        change_thresholds_window.title("Изменить пороговые значения")

        # Устанавливаем фон окна
        change_thresholds_window.configure(bg="#1c1c1c")  # Темный фон

        # Устанавливаем положение окна
        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        change_thresholds_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Увеличенные шрифты
        label_font = ("Arial", 14)
        entry_font = ("Arial", 12)
        button_font = ("Arial", 14)
        label_fg = "#ffffff"  # Белый цвет для текста
        entry_bg = "#333333"  # Темный фон для полей ввода
        entry_fg = "#ffffff"  # Белый текст в полях ввода
        button_bg = "#444444"  # Темный фон для кнопок
        button_fg = "#ffffff"  # Белый текст на кнопках

        # Поле ввода минимальной температуры
        tk.Label(
            change_thresholds_window,
            text="Минимальная температура:",
            font=label_font,
            fg=label_fg,
            bg="#1c1c1c"  # Черный фон для метки
        ).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        temp_min_entry = tk.Entry(change_thresholds_window, font=entry_font, bg=entry_bg, fg=entry_fg,
                                  insertbackground="#ffffff", width=25)
        temp_min_entry.grid(row=0, column=1, pady=10, padx=10)

        # Поле ввода максимальной температуры
        tk.Label(
            change_thresholds_window,
            text="Максимальная температура:",
            font=label_font,
            fg=label_fg,
            bg="#1c1c1c"  # Черный фон для метки
        ).grid(row=1, column=0, pady=10, padx=10, sticky="w")
        temp_max_entry = tk.Entry(change_thresholds_window, font=entry_font, bg=entry_bg, fg=entry_fg,
                                  insertbackground="#ffffff", width=25)
        temp_max_entry.grid(row=1, column=1, pady=10, padx=10)

        # Поле ввода минимальной влажности
        tk.Label(
            change_thresholds_window,
            text="Минимальная влажность:",
            font=label_font,
            fg=label_fg,
            bg="#1c1c1c"  # Черный фон для метки
        ).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        humidity_min_entry = tk.Entry(change_thresholds_window, font=entry_font, bg=entry_bg, fg=entry_fg,
                                      insertbackground="#ffffff", width=25)
        humidity_min_entry.grid(row=2, column=1, pady=10, padx=10)

        # Поле ввода максимальной влажности
        tk.Label(
            change_thresholds_window,
            text="Максимальная влажность:",
            font=label_font,
            fg=label_fg,
            bg="#1c1c1c"  # Черный фон для метки
        ).grid(row=3, column=0, pady=10, padx=10, sticky="w")
        humidity_max_entry = tk.Entry(change_thresholds_window, font=entry_font, bg=entry_bg, fg=entry_fg,
                                      insertbackground="#ffffff", width=25)
        humidity_max_entry.grid(row=3, column=1, pady=10, padx=10)

        # Кнопка сохранения значений
        def save_thresholds():
            """Сохранение пороговых значений."""
            try:
                temp_min = float(temp_min_entry.get())
                temp_max = float(temp_max_entry.get())
                humidity_min = float(humidity_min_entry.get())
                humidity_max = float(humidity_max_entry.get())

                # Обновление пороговых значений в системе
                self.security_system.thresholds["temp_min"] = temp_min
                self.security_system.thresholds["temp_max"] = temp_max
                self.security_system.thresholds["humidity_min"] = humidity_min
                self.security_system.thresholds["humidity_max"] = humidity_max

                messagebox.showinfo("Успех", "Пороговые значения обновлены.")
                change_thresholds_window.destroy()  # Закрыть окно после сохранения
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные числовые значения.")

        save_button = tk.Button(
            change_thresholds_window,
            text="Сохранить",
            font=button_font,
            bg=button_bg,
            fg=button_fg,
            command=save_thresholds
        )
        save_button.grid(row=4, columnspan=2, pady=20)

        change_thresholds_window.update_idletasks()
        change_thresholds_window.geometry('')

    def view_sensor_data(self):
        """Просмотр последних значений датчиков."""
        data = self.security_system.db.get_recent_sensor_data()
        if data:
            sensor_window = tk.Toplevel(self.root)
            sensor_window.title("Данные с датчиков")

            sensor_window.geometry("800x350+200+200")  # Задание размеров и положения окна

            canvas = tk.Canvas(sensor_window)
            scrollbar_y = tk.Scrollbar(sensor_window, orient="vertical", command=canvas.yview)
            scrollbar_x = tk.Scrollbar(sensor_window, orient="horizontal", command=canvas.xview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")

            for row in data:
                timestamp, temperature, humidity, motion, door = row
                tk.Label(
                    scrollable_frame,
                    text=f"{timestamp} - Температура={temperature}C, Влажность={humidity}%, Движение={bool(motion)}, Дверь={bool(door)}"
                ).pack(anchor="w")
        else:
            messagebox.showinfo("Данные с датчиков", "Нет данных для отображения.")

    def emulate_sensors(self):
        """Эмуляция показаний датчиков."""
        self.security_system.emulate_sensors()
        messagebox.showinfo("Эмуляция", "Показания датчиков обновлены.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecuritySystemApp(root)
    root.mainloop()