import sqlite3
import random
import time
from datetime import datetime
from tkinter import messagebox


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
        self.root = root  # Для графического интерфейса

    def check_for_anomalies(self, temp, humidity):
        anomalies = []
        if temp < self.thresholds["temp_min"] or temp > self.thresholds["temp_max"]:
            anomalies.append(f"Температура вне нормы: {temp}C")
        if humidity < self.thresholds["humidity_min"] or humidity > self.thresholds["humidity_max"]:
            anomalies.append(f"Влажность вне нормы: {humidity}%")
        return anomalies

    def emulate_sensors(self):
        """Эмуляция показаний датчиков и их запись в БД."""
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
        messagebox.showinfo("Уведомление системному администратору", "\n".join(issues))

    def notify_security_admin(self, message):
        messagebox.showerror("Уведомление администратору безопасности", message)


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
