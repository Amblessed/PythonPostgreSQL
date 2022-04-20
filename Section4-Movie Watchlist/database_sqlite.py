import sqlite3
from datetime import datetime
from sqlite3 import Cursor

# title, release_date, watched
# SELECT * FROM users WHERE surname LIKE 'Do%'
#    '%th' matches anything ending with `th`
#    'Do__s' matches anything starting with 'Do', ending with 's', and with two characters in between
#    'Bo%b' matches anything starting with 'Bo', ending with 'b', and any number of characters in between
#    '%sens%' matches anything containing 'sens', like 'sensibility' or 'insensible'
CREATE_MOVIES_TABLE = "CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, release_timestamp REAL);"
CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY);"
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
user_username TEXT, 
movie_id INTEGER, 
FOREIGN KEY(user_username) REFERENCES users(username)
FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES(?, ?);"
INSERT_USER = "INSERT INTO users (username) VALUES(?);"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies
JOIN watched ON movies.id = watched.movie_id
JOIN users ON users.username = watched.user_username
WHERE users.username= ?;"""
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = ?;"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES(?, ?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE ?;"
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"

connection = sqlite3.connect("movies.db")
connection.row_factory = sqlite3.Row


def create_tables() -> None:
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHED_TABLE)
        connection.execute(CREATE_RELEASE_INDEX)


def search_movies(search_term: str):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
        return cursor


def add_movie(title: str, release_timestamp) -> None:
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def add_user(username: str) -> None:
    with connection:
        connection.execute(INSERT_USER, (username,))


def get_movies(upcoming=False) -> Cursor:
    with connection:
        if upcoming:
            today_timestamp = datetime.today().timestamp()
            cursor = connection.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor = connection.execute(SELECT_ALL_MOVIES)
        return cursor


def watch_movie(username: str, movie_id: int) -> None:
    with connection:
        connection.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username: str) -> Cursor:
    with connection:
        cursor = connection.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor
