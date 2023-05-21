import sqlite3

class DatabaseManager:

    def __init__(self, db_filename):
        self.connection = sqlite3.connect(db_filename) # create a connection to the database 


    def __del__(self):
        self.connection.close() #closing the database later         

    def _execute(self, statement, values=None):

        with self.connection: #create transaction context

            cursor = self.connection.cursor() #cursor is used to execute statement 
            cursor.execute(statement, values or [])
            return cursor # returns the cursor, which has stored the result
        
        
    def create_table(self, table_name, columns):

        columns_with_types = [
            f"{column_name} {data_type}" for column_name, data_type in columns.items()
        ] # construct the column definitions with their datatypes and definitions 

        statement = f'''CREATE TABLE IF NOT EXISTS {table_name}
        ({", ".join(columns_with_types)});'''

        self._execute(statement)

    
    def add(self, table_name, data):

        placeholders = ", ".join("?" * len(data))
        column_names = ", ".join(data.keys())  #The keys of the data are the names of the columns
        column_values = tuple(data.values()) # .values() returns a dict_values object, but execute needs a list or a tuple

        self._execute(
            f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders}); 
            ''',
            column_values
        )


    def delete(self, table_name, criteria): # if no criteria argument, all records would be deleted
                
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
   
        self._execute(
            f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria}; 
            ''',
            tuple(criteria.values()) #use the values argument of self._execute as teh values to match against
        )

    def select(self, table_name, criteria=None, order_by=None):

        criteria = criteria or {} # criteria can be empty 

        query = f"SELECT * FROM {table_name}"

        if criteria: # WHERE will limit the results 
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"

        if order_by: #ORDER BY will sort results 
            query += f" ORDER BY {order_by}"

        return self._execute(query, tuple(criteria.values()))




