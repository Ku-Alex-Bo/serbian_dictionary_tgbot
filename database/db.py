import sqlite3
from config import DB_PATH
from typing import List, Tuple

class WordsManager:
    def __init__(self, db_path=DB_PATH) -> None:
        self.db_path = db_path
        self._create_table()

    def _connect(self) -> None:
        """Подключение к базе данных"""
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        """Создание таблицы, если ее еще нет."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY,
                    serbian TEXT NOT NULL,
                    russian TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            ''')
            conn.commit()

    def insert_word(self, serbian, russian, category) -> None:
        """Добавить слово в базу данных."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO words (serbian, russian, category)
                VALUES (?, ?, ?)
            ''', (serbian, russian, category))
            conn.commit()

    def get_words_by_category(self, category: str) -> List[Tuple[str, str, str]]:
        """Получить все слова по категории."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT serbian, russian, image FROM words WHERE category=?
            ''', (category,))
            return cursor.fetchall()

    def get_all_words(self) -> List[Tuple[str, str, str, str]]:
        """Получить все слова из базы данных."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT serbian, russian, image, category FROM words')
            return cursor.fetchall()

    def get_categories(self) -> List[str]:
        """Получить все категории"""
        all_words = self.get_all_words()
        return [*set([elem[-1] for elem in all_words])]

    def delete_word(self, word_id) -> None:
        """Удалить слово по ID."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM words WHERE id=?', (word_id,))
            conn.commit()

    def update_word(self, word_id, new_serbian, new_russian, new_category) -> None:
        """Обновить слово в базе данных."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE words
                SET serbian=?, russian=?, category=?
                WHERE id=?
            ''', (new_serbian, new_russian, new_category, word_id))
            conn.commit()


class UsersManager():
    def __init__(self, db_path=DB_PATH) -> None:
        self.db_path = db_path
        self._create_table()

    def _connect(self) -> None:
        """Подключение к базе данных"""
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        """Создание таблицы, если ее еще нет."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    tg_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    language TEXT DEFAULT 'serbian' NOT NULL,
                    repeat_words TEXT DEFAULT ''
                )
            ''')
            conn.commit()

    def insert_user(self, tg_id, name) -> None:
        """Добавить пользователя в базу данных."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (tg_id, name)
                VALUES (?, ?)
            ''', (tg_id, name))
            conn.commit()

    def get_user_by_tg_id(self, tg_id: int) -> dict:
        """Получить данные пользователя по telegram id"""
        with self._connect() as conn:
            cursor = conn.cursor()
            keys = ["tg_id", "name", "language", "repeat_words"]
            query = f"SELECT {', '.join(keys)} FROM users WHERE tg_id=?"
            cursor.execute(query, (tg_id,))
            data = cursor.fetchone()
            if data:
                user_dict = {key: value for key, value in zip(keys, data)}
                return user_dict
            return None

    def update_user_language(self, tg_id: int, new_language: str) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            query = f"UPDATE users SET language = ? WHERE tg_id = ?"
            cursor.execute(query, (new_language,tg_id))
            conn.commit()

    def update_user_repeat_words(self, tg_id: int, words: str) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            query = "SELECT repeat_words FROM users WHERE tg_id=?"
            cursor.execute(query, (tg_id))
            data = cursor.fetchone()
            print(data)

wm = WordsManager()
um = UsersManager()
