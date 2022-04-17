import sqlite3
from datetime import datetime
from sqlite3 import Cursor

connection = sqlite3.connect("data.db")
connection.row_factory = sqlite3.Row


# A cursor is a structure that allows us to traverse a result set
# Database cursors allow the database to only results when requested
# SQLite cursors load all results, but help us go over them more easily

def create_table():
    with connection:
        connection.execute("CREATE TABLE IF NOT EXISTS entries (content TEXT, date TEXT);")


def add_entry(entry_content: str, entry_date: str):
    with connection:
        if not entry_date:
            entry_date = datetime.today().strftime('%d-%m-%Y')
        connection.execute("INSERT INTO entries VALUES(?, ?);", (entry_content, entry_date))


def get_entries() -> Cursor:
    cursor = connection.execute("SELECT * FROM entries;")
    return cursor


