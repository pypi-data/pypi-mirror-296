import pyodbc


class DbConnection:
    def __init__(self, connection_string):
        self.Driver = None
        self.Server = None
        self.Database = None
        self.UID = None
        self.PWD = None
        self.parse_connection_string(connection_string)

    def parse_connection_string(self, connection_string):
        parameters = connection_string.split(';')
        for param in parameters:
            if param.startswith('Driver'):
                self.Driver = param.split('=')[1].strip('{}')
            elif param.startswith('Server'):
                self.Server = param.split('=')[1]
            elif param.startswith('Database'):
                self.Database = param.split('=')[1]
            elif param.startswith('UID'):
                self.UID = param.split('=')[1]
            elif param.startswith('PWD'):
                self.PWD = param.split('=')[1]

    def get_connection(self):
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
