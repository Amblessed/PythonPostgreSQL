import os
from typing import Tuple, List

from database_connection import DatabaseConnection
from dotenv import load_dotenv

load_dotenv()

Poll = Tuple[int, str, str]
Option = Tuple[int, str, int]
Vote = Tuple[str, int]
PollWithOption = Tuple[int, str, str, int, str, int]

CREATE_POLLS = "CREATE TABLE IF NOT EXISTS polls (id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"
CREATE_OPTIONS = "CREATE TABLE IF NOT EXISTS options (id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER, FOREIGN KEY(poll_id) REFERENCES polls (id));"
CREATE_VOTES = "CREATE TABLE IF NOT EXISTS votes (username TEXT, option_id INTEGER, FOREIGN KEY(option_id) REFERENCES options (id));"

INSERT_POLL_RETURN_ID = "INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"
SELECT_ALL_POLLS = "SELECT * FROM polls;"
SELECT_POLL = "SELECT * FROM polls WHERE id = %s;"
SELECT_POLL_OPTIONS = "SELECT * FROM options WHERE poll_id = %s;"
INSERT_OPTION_RETURN_ID = "INSERT INTO options (option_text, poll_id) VALUES (%s, %s) RETURNING id;"
SELECT_OPTION = "SELECT * FROM options WHERE id = %s;"
SELECT_VOTES_FOR_OPTION = "SELECT * FROM votes WHERE option_id = %s;"

INSERT_VOTE = "INSERT INTO votes (username, option_id) VALUES (%s, %s);"
SELECT_LATEST_POLL = """SELECT * FROM polls WHERE polls.id = (SELECT id FROM polls ORDER BY DESC LIMIT 1);"""

hostname: str = os.environ['DATABASE_HOSTNAME']


def create_tables() -> None:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(CREATE_POLLS)
        cursor.execute(CREATE_OPTIONS)
        cursor.execute(CREATE_VOTES)


# ----polls-----

def create_poll(title: str, owner: str) -> int:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))
        return cursor.fetchone()[0]


def get_polls() -> List[Poll]:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_ALL_POLLS)
        return cursor.fetchall()


def get_poll(poll_id: int) -> Poll:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_POLL, (poll_id,))
        return cursor.fetchone()


def get_latest_poll() -> Poll:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_LATEST_POLL)
        return cursor.fetchone()


def get_option(option_id: int) -> Option:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_OPTION, (option_id,))
        return cursor.fetchone()


def add_option(option_text, poll_id: int) -> int:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_OPTION_RETURN_ID, (option_text, poll_id))
        return cursor.fetchone()


def get_votes_for_option(option_id: int) -> List[Vote]:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_VOTES_FOR_OPTION, (option_id,))
        return cursor.fetchall()


def add_poll_vote(username: str, option_id: int):
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_VOTE, (username, option_id))


def get_poll_options(poll_id: int) -> List[Option]:
    with DatabaseConnection(hostname) as connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_POLL_OPTIONS, (poll_id,))
        return cursor.fetchall()
