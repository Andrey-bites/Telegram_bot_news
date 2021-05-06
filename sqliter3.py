import sqlite3


class Sqlighter:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subscription(self, status=True):
        with self.connection:
            return self.cursor.execute("SELECT FROM subscription WHERE status = ?", (status)).fetchall()

    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT FROM subscription WHERE user_id = ?", (user_id)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        with self.connection:
            return self.cursor.execute("INSERT INTO subscription (user_id, status) VALUES (?/?)", (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки"""
        return self.cursor.execute("UPDATE subscrition SET status = ? WHERE user_id = ?", (status, user_id))

    def close(self):
        self.connection.close()
