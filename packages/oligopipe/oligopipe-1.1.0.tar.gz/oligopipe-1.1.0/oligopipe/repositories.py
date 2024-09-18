import logging

import psycopg2

logger = logging.getLogger(__name__)


class AnnotationRepository:

    def __init__(self, db_credentials):
        """
        :param db_credentials: dictionary containing connection parameters for the database
        """
        self.host = db_credentials["HOST"]
        self.user = db_credentials["USER"]
        self.password = db_credentials["PASSWORD"]
        self.db = db_credentials["DB"]
        self.port = db_credentials["PORT"]
        self.db_connection = None
        self.cursor = None

    def connect(self):
        logger.debug("Connect to: "+self.host)#+":"+self.db)
        self.db_connection = psycopg2.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.db, port=self.port)
        self.cursor = self.db_connection.cursor()

    def execute(self, query, args=None):
        """
        Executes a query and return an iterable cursor to access the result
        :param query: an SQL query
        :param args: extra args
        :return: the iterable cursor
        """
        self.cursor.execute(query, args)
        return self.cursor

    def disconnect(self):
        self.db_connection.close()
