import os
import psycopg2


class DatabaseConnection:
    __slots__ = ("__connection", "__hostname")

    def __init__(self, hostname):
        self.__connection = None
        self.__hostname = hostname

    def __enter__(self):
        self.__connection = psycopg2.connect(host=self.__hostname, dbname=os.environ['DATABASE_NAME'],
                                             user=os.environ['DATABASE_USERNAME'],
                                             password=os.environ['DATABASE_PASSWORD'],
                                             port=os.environ['DATABASE_PORT'])
        return self.__connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.__connection.close()
        else:
            self.__connection.commit()
            self.__connection.close()
