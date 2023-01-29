import pyodbc

class DatabaseConnector:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
    
    def create_connection(self):
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        return connection
    
    def close_connection(self, connection):
        connection.close()
    
    def execute_query(self, connection, query):
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        return cursor
    
    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor

connector = DatabaseConnector(server='your_server_name', database='your_database_name', username='your_username', password='your_password')

# create a connection to the database
connection = connector.create_connection()

# execute a query
cursor = connector.execute_query(connection, "INSERT INTO table_name (column1, column2) VALUES (value1, value2)")

# close the connection
connector.close_connection(connection)
