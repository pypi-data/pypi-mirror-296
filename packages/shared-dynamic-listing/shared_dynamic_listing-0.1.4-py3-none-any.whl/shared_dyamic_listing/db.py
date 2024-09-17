import pyodbc


class DbConnection:
    def __init__(self, connection_dict):
        self.Driver = connection_dict.get('Driver')
        self.Server = connection_dict.get('Server')
        self.Database = connection_dict.get('Database')
        self.UID = connection_dict.get('UID')
        self.PWD = connection_dict.get('PWD')

    def get_connection(self):
        # Dynamically create the connection string from the dictionary values
        connection_str = (
            f"Driver={self.Driver};"
            f"Server={self.Server};"
            f"Database={self.Database};"
            f"UID={self.UID};"
            f"PWD={self.PWD};"
        )

        # Use pyodbc to create a connection
        try:
            conn = pyodbc.connect(connection_str)
            return conn
        except pyodbc.Error as e:
            print("Error connecting to the database:", e)
            return None
