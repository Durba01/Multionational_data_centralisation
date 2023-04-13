#%%
import yaml
from sqlalchemy import create_engine
import psycopg2
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd 
from sqlalchemy import inspect

class DatabaseConnector:
    def __init__(self):
        self.creds = self.read_db_creds("db_creds.yaml")
        self.engine = self.init_db_engine()
    # STEP 2
    def read_db_creds(self, file_path):
        with open(file_path, 'r') as file:
            creds = yaml.safe_load(file)
        return creds

    #creds = read_db_creds('db_creds.yaml')
    #print(creds)

    # STEP 3
    def init_db_engine(self):
        creds = self.creds
        # format the connection string using the credentials
        conn_string = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
            user=creds['RDS_USER'],
            password=creds['RDS_PASSWORD'],
            host=creds['RDS_HOST'],
            port=creds['RDS_PORT'],
            database=creds['RDS_DATABASE']
        )
        # create the engine using the connection string
        engine = create_engine(conn_string)
        return engine
        
#def __init__(self):
    #creds = self.read_db_creds("db_creds.yaml")
    #engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
    #engine.connect() # connect the database with the 

# %%
