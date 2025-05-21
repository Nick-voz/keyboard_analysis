import sqlite3

from env import (
    DB_PATH,
)  # Предполагается, что DB_PATH указывает путь к вашей базе данных


def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS keypress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL,
        key TEXT NOT NULL
    );
    """
    with sqlite3.connect(DB_PATH) as db:
        db.execute(create_table_query)
        db.commit()
        print("Таблица 'keypress' успешно создана (если её не существовало).")


if __name__ == "__main__":
    create_table()
