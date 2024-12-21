import tkinter as tk
from tkinter import messagebox, simpledialog
from Base import SecuritySystem

class SecuritySystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система безопасности")
        self.security_system = SecuritySystem()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.create_login_interface()

    def create_login_interface(self):
        """Создание интерфейса авторизации."""
        # Установка размеров и центровка окна
        window_width = 500
        window_height = 300
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

        # Поле ввода имени пользователя
        tk.Label(self.main_frame, text="Имя пользователя:", font=label_font).grid(row=0, column=0, pady=10, padx=10,
                                                                                  sticky="w")
        self.username_entry = tk.Entry(self.main_frame, font=entry_font, width=25)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        # Поле ввода пароля
        tk.Label(self.main_frame, text="Пароль:", font=label_font).grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.password_entry = tk.Entry(self.main_frame, show="*", font=entry_font, width=25)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Кнопка входа
        tk.Button(
            self.main_frame, text="Войти", font=button_font, width=20, command=self.authenticate_user
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

        # Информация о пользователе
        tk.Label(
            self.main_frame,
            text=f"Пользователь: {username} ({role})",
            font=label_font
        ).pack(pady=10)

        # Создание кнопок в зависимости от роли пользователя
        def create_button(text, command):
            tk.Button(
                self.main_frame,
                text=text,
                font=button_font,
                width=30,  # Увеличенная ширина кнопки
                height=1,  # Увеличенная высота кнопки
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
        username = simpledialog.askstring("Добавить пользователя", "Введите имя пользователя:")
        if username:
            password = simpledialog.askstring("Добавить пользователя", "Введите пароль:")
            role = simpledialog.askstring("Добавить пользователя", "Введите роль:\nadmin \nuser \npersonal manager")
            if role in ["admin", "user", "personal manager"]:
                self.security_system.db.add_user(username, password, role)
                messagebox.showinfo("Успех", f"Пользователь '{username}' добавлен как '{role}'.")
            else:
                messagebox.showerror("Ошибка", "Некорректная роль.")

    def delete_user(self):
        """Удаление пользователя."""
        username = simpledialog.askstring("Удалить пользователя", "Введите имя пользователя для удаления:")
        role = simpledialog.askstring("Удалить пользователя", "Введите роль (опционально):")
        if username:
            self.security_system.db.delete_user(username, role)
            messagebox.showinfo("Успех", f"Пользователь '{username}' с ролью '{role or 'все роли'}' удалён.")

    def change_thresholds(self):
        """Изменение пороговых значений датчиков."""
        thresholds = simpledialog.askstring(
            "Пороговые значения",
            "Введите значения через запятую:\n1.минимальная температура\n2.максимальная температура\n3.минимальная влажность\n4.максимальная влажность"
        )
        if thresholds:
            try:
                temp_min, temp_max, humidity_min, humidity_max = map(float, thresholds.split(","))
                self.security_system.thresholds["temp_min"] = temp_min
                self.security_system.thresholds["temp_max"] = temp_max
                self.security_system.thresholds["humidity_min"] = humidity_min
                self.security_system.thresholds["humidity_max"] = humidity_max
                messagebox.showinfo("Успех", "Пороговые значения обновлены.")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите 4 числовых значения через запятую.")

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