import psycopg2
from psycopg2 import Error
from todoapp.backend.setting import psql_host, psql_port, psql_password, psql_username, database_name
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import os

import sqlalchemy


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

    # def getCursor(self):
    #     try:
    #         # Connect to an existing database
    #         # self.connection = psycopg2.connect(user="yzq",
    #         #                                    password="zuqiangyyy",
    #         #                                    host="127.0.0.1",
    #         #                                    port="5432",
    #         #                                    database="flask_db")
    #
    #         self.connection = psycopg2.connect(user="postgres",
    #                                            password="jchk@cSjP&#:}&#$",
    #                                            host="35.239.10.136",
    #                                            database="todoapp_flask_db")
    #
    #         # Create a cursor to perform database operations
    #         self.cursor = self.connection.cursor()
    #         # Print PostgreSQL details
    #         print("PostgreSQL server information")
    #         print(self.connection.get_dsn_parameters(), "\n")
    #     except (Exception, Error) as error:
    #         print("Error while connecting to PostgreSQL", error)
    #
    #     return self.cursor
    #
    # def close(self):
    #     if (self.connection):
    #         self.connection.close()
    #         self.cursor.close()
    #         print("PostgreSQL connection is closed")

    def connect_with_connector(self) -> sqlalchemy.engine.base.Engine:
      """
      Initializes a connection pool for a Cloud SQL instance of Postgres.

      Uses the Cloud SQL Python Connector package.
      """
      # Note: Saving credentials in environment variables is convenient, but not
      # secure - consider a more secure solution such as
      # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
      # keep secrets safe.

      instance_connection_name = "to-do-app-378206:us-central1:todoappdb"  # e.g. 'project:region:instance'
      db_user = "postgres"  # e.g. 'my-db-user'
      db_pass = "zuqiangyu123"  # e.g. 'my-db-password'
      db_name = "postgres"  # e.g. 'my-database'

      ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

      # initialize Cloud SQL Python Connector object
      connector = Connector()

      def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
          instance_connection_name,
          "pg8000",
          user=db_user,
          password=db_pass,
          db=db_name,
          ip_type=ip_type,
        )
        return conn

      # The Cloud SQL Python Connector can be used with SQLAlchemy
      # using the 'creator' argument to 'create_engine'
      pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
      )
      return pool
