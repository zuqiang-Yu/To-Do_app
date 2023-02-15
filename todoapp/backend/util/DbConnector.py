import psycopg2
from psycopg2 import Error
from setting import psql_host, psql_port, psql_password, psql_username, database_name


class DbConnector:
    """
    connect to the database
    """

    def __init__(self):
        self.user = psql_username
        self.host = psql_host
        self.port = psql_port
        self.password = psql_password
        self.database_name = database_name
        self.connection = None
        self.cursor = None

    def getCursor(self):
        try:
            # Connect to an existing database
            self.connection = psycopg2.connect(user="yzq",
                                               password="zuqiangyyy",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="flask_db")

            # Create a cursor to perform database operations
            self.cursor = self.connection.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(self.connection.get_dsn_parameters(), "\n")
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

        return self.cursor

    def close(self):
        if (self.connection):
            self.connection.close()
            self.cursor.close()
            print("PostgreSQL connection is closed")
