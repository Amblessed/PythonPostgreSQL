import os
from datetime import datetime
from typing import List

from database_connection import DatabaseConnection
from dotenv import load_dotenv

load_dotenv()

# title, release_date, watched
# SELECT * FROM users WHERE surname LIKE 'Do%'
#    '%th' matches anything ending with `th`
#    'Do__s' matches anything starting with 'Do', ending with 's', and with two characters in between
#    'Bo%b' matches anything starting with 'Bo', ending with 'b', and any number of characters in between
#    '%sens%' matches anything containing 'sens', like 'sensibility' or 'insensible'
CREATE_MOVIES_TABLE = "CREATE TABLE IF NOT EXISTS movies (id SERIAL PRIMARY KEY, title TEXT, release_timestamp REAL);"
CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY);"
CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (user_username TEXT, movie_id INTEGER, FOREIGN KEY(user_username) REFERENCES users(username),
FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES(%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES(%s);"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """SELECT movies.* FROM movies
JOIN watched ON movies.id = watched.movie_id
JOIN users ON users.username = watched.user_username
WHERE users.username= %s;"""
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = %s;"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES(%s, %s);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE %s;"
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"

hostname: str = os.environ['DATABASE_HOSTNAME']


def create_tables() -> None:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_MOVIES_TABLE)
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(CREATE_WATCHED_TABLE)


def search_movies(search_term: str) -> List:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
        return cursor.fetchall()


def add_movie(title: str, release_timestamp) -> None:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def add_user(username: str) -> None:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_USER, (username,))


def get_movies(upcoming=False) -> List:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def watch_movie(username: str, movie_id: int) -> None:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username: str) -> List:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()
