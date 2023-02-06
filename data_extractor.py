import pandas as pd
from sqlalchemy import inspect

class DataExtractor:
    def __init__(self):
        pass

# Class data Extractor 
class DataExtractor:
    def __init__(self):
        self.engine = self.init_db_engine()

    def extract_data(self, table_name):
        # create a session using the engine
        inspector = inspect(self.engine)
        return inspector.get_table_names(f'SELECT * FROM {table_name}').fetchall()
        # execute a simple query to retrieve the data from the table

    def read_rds_table(self, table_name):
        # extract the data from the table
        data = self.extract_data(table_name)

        # convert the data to a pandas DataFrame
        df = pd.DataFrame(data)

        return df