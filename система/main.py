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
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Имя пользователя:").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.main_frame, text="Пароль:").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.main_frame, text="Войти", command=self.authenticate_user).grid(row=2, columnspan=2, pady=10)

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
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text=f"Пользователь: {username} ({role})").pack(pady=5)

        if role == "admin":
            tk.Button(self.main_frame, text="Добавить пользователя", command=self.add_user).pack(pady=5)
            tk.Button(self.main_frame, text="Удалить пользователя", command=self.delete_user).pack(pady=5)
            tk.Button(self.main_frame, text="Изменить пороговые значения", command=self.change_thresholds).pack(pady=5)

        tk.Button(self.main_frame, text="Просмотреть значения датчиков", command=self.view_sensor_data).pack(pady=5)

        tk.Button(self.main_frame, text="Эмулировать показания датчиков", command=self.emulate_sensors).pack(pady=5)
        tk.Button(self.main_frame, text="Выйти", command=self.create_login_interface).pack(pady=10)

    def add_user(self):
        """Добавление нового пользователя."""
        username = simpledialog.askstring("Добавить пользователя", "Введите имя пользователя:")
        if username:
            password = simpledialog.askstring("Добавить пользователя", "Введите пароль:")
            role = simpledialog.askstring("Добавить пользователя", "Введите роль (admin или user):")
            if role in ["admin", "user"]:
                self.security_system.db.add_user(username, password, role)
                messagebox.showinfo("Успех", f"Пользователь '{username}' добавлен как '{role}'.")
            else:
                messagebox.showerror("Ошибка", "Некорректная роль.")

    def delete_user(self):
        """Удаление пользователя."""
        username = simpledialog.askstring("Удалить пользователя", "Введите имя пользователя для удаления:")
        if username:
            self.security_system.db.delete_user(username)
            messagebox.showinfo("Успех", f"Пользователь '{username}' удалён.")

    def change_thresholds(self):
        """Изменение пороговых значений датчиков."""
        thresholds = simpledialog.askstring(
            "Пороговые значения",
            "Введите значения (temp_min, temp_max, humidity_min, humidity_max) через запятую:"
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

            canvas = tk.Canvas(sensor_window)
            scrollbar_y = tk.Scrollbar(sensor_window, orient="vertical", command=canvas.yview)
            scrollbar_x = tk.Scrollbar(sensor_window, orient="horizontal", command=canvas.xview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")

            for row in data:
                timestamp, temperature, humidity, motion, door = row
                tk.Label(scrollable_frame, text=f"{timestamp} - Температура={temperature}C, Влажность={humidity}%, Движение={bool(motion)}, Дверь={bool(door)}").pack(anchor="w")
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