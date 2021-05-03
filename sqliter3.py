import sqlite3


class SQLighter:

    def __init__(self, database_file):
        """подключаемся к БД и сохроняем курсор соединения"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subscription(self, status=True):
        """получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscription` WHERE `status` = ?", (status)).fetchall()

    def subscriber_exists(self, user_id):
        """проверяем есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `subscription` WHERE `user_id` = ?", (user_id)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        """ добавляем подписчика в БД """
        with self.connection:
            return self.cursor.execute("INSERT into `subscription` (`user_id`, `status`) VALUES (?, ?)", (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки"""
        return self.cursor.execute("UPDATE `subscription` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        """ Закрываем соединение с БД """
        self.connection.close()
