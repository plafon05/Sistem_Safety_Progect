import sqlite3
import time
import tkinter as tk
from datetime import datetime
import random

class NotificationManager:
    def __init__(self, root):
        self.root = root
        self.notifications = []
        self.hide_all_button = None

    def show_notification(self, message, recipient):
        notification_window = tk.Toplevel(self.root)
        notification_window.overrideredirect(True)
        notification_window.attributes('-topmost', True)

        notification_window.configure(bg="lightgray")

        # Calculate position for the notification
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        notification_height = 80
        notification_y = screen_height - (len(self.notifications) + 1) * (notification_height + 10)
        notification_window.geometry(f"320x{notification_height}+{screen_width - 330}+{notification_y}")

        # Add recipient label
        recipient_label = tk.Label(notification_window, text=recipient, bg="red", font=("Arial",9, "bold"), anchor="w")
        recipient_label.pack(fill="x", padx=5, pady=2)

        # Add message label
        message_label = tk.Label(notification_window, text=message, bg="lightgray", font=("Arial", 10), anchor="w", justify="left", wraplength=300)
        message_label.pack(fill="x", padx=5, pady=5)

        # Add close button
        close_button = tk.Button(notification_window, text="x", command=lambda: self.close_notification(notification_window), bg="lightgray")
        close_button.place(x=300, y=0, width=20, height=20)

        self.notifications.append(notification_window)
        self.animate_notification(notification_window)
        self.update_positions()

        # Show "Hide All" button if there are multiple notifications
        if len(self.notifications) > 1 and not self.hide_all_button:
            self.show_hide_all_button()

    def animate_notification(self, notification_window):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        target_y = int(notification_window.geometry().split('+')[2])

        for step in range(screen_height, target_y, -10):
            notification_window.geometry(f"320x80+{screen_width - 330}+{step}")
            notification_window.update()
            self.root.after(5)

    def close_notification(self, notification_window):
        notification_window.destroy()
        self.notifications.remove(notification_window)
        self.update_positions()

        # Remove "Hide All" button if no notifications remain
        if len(self.notifications) <= 1 and self.hide_all_button:
            self.hide_all_button.destroy()
            self.hide_all_button = None

    def update_positions(self):
        # Обновляем позиции уведомлений и кнопку "Скрыть все"
        screen_height = self.root.winfo_screenheight()
        notification_height = 80
        for index, notification in enumerate(self.notifications):
            notification_y = screen_height - (index + 1) * (notification_height + 10)
            notification.geometry(f"320x{notification_height}+{self.root.winfo_screenwidth() - 330}+{notification_y}")

        # Если нужно, отображаем кнопку "Скрыть все"
        if len(self.notifications) > 1:
            self.show_hide_all_button()
        elif self.hide_all_button:
            self.hide_all_button.place_forget()
            self.hide_all_button = None

    def show_hide_all_button(self):
        if not self.hide_all_button:
            # Создание кнопки, если она не существует
            self.hide_all_button = tk.Button(
                self.root,
                text="Скрыть все",
                command=self.hide_all,
                bg="lightgray",
                font=("Arial", 10)
            )
        # Позиционируем кнопку внизу экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.hide_all_button.place(
            x=screen_width - 330,
            y=screen_height - 50,  # Немного выше нижнего края
            width=100,  # Ширина кнопки
            height=30  # Высота кнопки
        )
        self.hide_all_button.lift()  # Перемещаем кнопку поверх других элементов

    def hide_all(self):
        # Удаление всех уведомлений
        for notification in self.notifications:
            notification.destroy()
        self.notifications.clear()

        # Удаление кнопки
        if self.hide_all_button:
            self.hide_all_button.place_forget()
            self.hide_all_button = None


class SecuritySystem:
    def __init__(self, root):
        self.db = Database()
        self.thresholds = {
            "temp_min": 18.0,
            "temp_max": 26.0,
            "humidity_min": 30.0,
            "humidity_max": 60.0
        }
        self.motion_sensor_active = False
        self.door_sensor_active = False
        self.root = root
        self.notifications = NotificationManager(root)

    def check_for_anomalies(self, temp, humidity):
        anomalies = []
        if temp < self.thresholds["temp_min"] or temp > self.thresholds["temp_max"]:
            anomalies.append(f"Температура вне нормы: {temp}C")
        if humidity < self.thresholds["humidity_min"] or humidity > self.thresholds["humidity_max"]:
            anomalies.append(f"Влажность вне нормы: {humidity}%")
        return anomalies

    def emulate_sensors(self):
        temp = random.uniform(15, 30)
        humidity = random.uniform(20, 70)
        motion_detected = random.choice([True, False])
        door_opened = random.choice([True, False])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.save_sensor_data(temp, humidity, motion_detected, door_opened, timestamp)

        anomalies = self.check_for_anomalies(temp, humidity)
        if anomalies:
            self.notify_system_admin(anomalies)

        if motion_detected and not self.is_working_hours():
            self.activate_alarm("Движение в нерабочее время")

        if door_opened:
            self.activate_alarm("Дверь сервера открыта без разрешения")

    def is_working_hours(self):
        current_hour = datetime.now().hour
        return 8 <= current_hour <= 20

    def activate_alarm(self, reason):
        self.notify_security_admin(reason)

    def notify_system_admin(self, issues):
        for issue in issues:
            self.notifications.show_notification(issue, "Уведомление системному администратору")

    def notify_security_admin(self, message):
        self.notifications.show_notification(message, "Уведомление администратору безопасности")



class Database:
    def __init__(self):
        self.connection = sqlite3.connect("security_system.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
           CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL,
               password TEXT NOT NULL,
               role TEXT NOT NULL,
               UNIQUE(username, role)
           )""")
        self.cursor.execute("""
           CREATE TABLE IF NOT EXISTS sensor_data (
               timestamp TEXT,
               temperature REAL,
               humidity REAL,
               motion_detected INTEGER,
               door_opened INTEGER
           )""")
        self.connection.commit()
        self.ensure_admin_exists()

    def ensure_admin_exists(self):
        """Создаёт учётную запись админа, если она не существует."""
        self.cursor.execute("SELECT * FROM users WHERE username = ?", ("danila.zheltov",))
        if not self.cursor.fetchone():
            self.add_user("danila.zheltov", "123", "admin")

    def ensure_personal_manager_exists(self):
        """Создаёт учётную запись менеджера по персоналу, если она не существует."""
        self.cursor.execute("SELECT * FROM users WHERE username = ?", ("danila.zheltov",))
        if not self.cursor.fetchone():
            self.add_user("danila.zheltov", "1234", "personal manager")

    def add_user(self, username, password, role):
        try:
            self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                (username, password, role))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Пользователь с именем '{username}' и ролью '{role}' уже существует.")

    def delete_user(self, username, role=None):
        if role:
            self.cursor.execute("DELETE FROM users WHERE username = ? AND role = ?", (username, role))
        else:
            self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.connection.commit()

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone()

    def save_sensor_data(self, temp, humidity, motion, door, timestamp):
        self.cursor.execute("""
            INSERT INTO sensor_data (timestamp, temperature, humidity, motion_detected, door_opened)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, temp, humidity, int(motion), int(door)))
        self.connection.commit()

    def get_recent_sensor_data(self):
        self.cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
        return self.cursor.fetchall()

    def update_thresholds(self, temp_min, temp_max, humidity_min, humidity_max):
        """Обновление пороговых значений."""
        self.thresholds = {
            "temp_min": temp_min,
            "temp_max": temp_max,
            "humidity_min": humidity_min,
            "humidity_max": humidity_max
        }
