#%%
import yaml
from sqlalchemy import create_engine
import psycopg2
import pandas as pd 
from sqlalchemy import inspect

class DatabaseConnector:
    def __init__(self):
        self.creds = self.read_db_creds("db_creds.yaml")
        #self.engine = self.init_db_engine()
    # STEP 2
    def read_db_creds(self, file_path):
        with open(file_path, 'r') as file:
            creds = yaml.safe_load(file)
        return creds

    #creds = read_db_creds('db_creds.yaml')
    #print(creds)

    # STEP 3
    def init_db_engine(self, creds):
        '''take data from read_db_creds, return sqlalchemy database engine'''
        engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
        engine.connect()
        return engine

       #STEP 4
    def list_db_tables(self, engine):
        # retrieve the table names 
        inspector = inspect(engine)
        return inspector.get_table_names()
    
    # STEP 7 
    def upload_to_db(self, df, table_name):
        self.creds = self.read_db_creds("local_db_creds.yaml")
        self.engine = self.init_db_engine(creds=self.creds) # I added the cred argument in
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)

    
connector = DatabaseConnector()
creds = connector.read_db_creds("db_creds.yaml")
engine = connector.init_db_engine(creds)

# TASK 7 
table_list = connector.list_db_tables(engine)
table_list

