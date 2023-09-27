import psycopg2 as ps
from psycopg2 import extensions


class connect:
    """Provides the database connection"""
    def __init__(self):
        self.db_hostname = "localhost"
        self.db_database = "Database_Job_Offers"
        self.db_username = "eraysen"
        self.db_pwd = "****"
        self.db_port_id = 5432

        global connection
        global cursor

        try:
            connection = ps.connect(

                host=self.db_hostname,
                dbname=self.db_database,
                user=self.db_username,
                password=self.db_pwd,
                port=self.db_port_id)

            self.cursor = connection.cursor()

            autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
            connection.set_isolation_level(autocommit)
            self.cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
            print("Successful Connecting")
            print("")

        except Exception as error:
            print("Connection Failed", error)
            cursor.close()
            connection.close()

