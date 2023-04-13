#%%
import pandas as pd
from sqlalchemy import inspect
from sqlalchemy import create_engine
from data_base_connector import DatabaseConnector
import sqlalchemy
import tabula 
import requests
import boto3
import pandas as pd
from io import StringIO
import json 

# Class data Extractor 
class DataExtractor:
    def __init__(self):
        pass

    # A method that read the RDS Tables 
    def read_rds_table(self, engine, table_name):
        with engine.begin() as conn:
            query = sqlalchemy.text(f"SELECT * FROM  {table_name}")
            df = pd.read_sql_query(query, conn)
        return df

     # A method that use tabula to extract all tables from the PDF
    def retrieve_pdf_data(self, link):
        self.link = link 
        tables = tabula.read_pdf(link, pages='all', multiple_tables=True)
        # Concatenate all tables into a single DataFrame
        df = pd.concat(tables)
        return df
    
    def list_number_of_stores(self, endpoint, headers):
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            return json_data#['number_of_stores']
        else:
            raise ValueError(f"Failed to get number of stores. Response code: {response.status_code}")
        
    def retrieve_stores_data(self, endpoint, headers, store_number):
        stores_data = []
        for store_index in range(store_number):
            store_endpoint = endpoint + str(store_index)
            response = requests.get(store_endpoint, headers=headers)
            if response.status_code == 200:
                current_data = list(response.json().values())
                column_headings=response.json().keys()
                stores_data.append(current_data)
            else:
                print("Error fetching stores data: ", response.status_code)
                return []
        return pd.DataFrame(data = stores_data, columns=column_headings)  

    def extract_from_s3(self, s3_address):
        s3 = boto3.resource('s3')
        bucket_name, object_key = s3_address.split('//')[1].split('/', 1)
        obj = s3.Object(bucket_name=bucket_name, key=object_key)
        file_content = obj.get()['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(file_content))
        return df
    
    def get_json_from_s3(self, bucket_name, key):
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)

connector = DatabaseConnector()
creds = connector.read_db_creds("db_creds.yaml")
engine = connector.init_db_engine(creds)
extractor = DataExtractor()

# Retrieve the tables in the central database
tables = connector.list_db_tables(engine)
tables

# Retreve the legacy_user table from the central database
user_df = extractor.read_rds_table(engine, 'legacy_users')
user_df

# Retrive data saved and load to db
data_df = pd.read_csv("cleaned_data.csv")
data_df.head()

# Upload to db
load = connector.upload_to_db(df=data_df,table_name='dim_users')
load

# Extracting pdf_data 
pdf_data = extractor.retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")
pdf_data.head()

# Uploading pdf_data to db
df_pdf = pd.read_csv("pdf_data.csv")
pdf_data_load = connector.upload_to_db(df = df_pdf, table_name='dim_card_details')
pdf_data_load

 #Retrieve a store 
headers = {
    'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'
}

endpoint = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
retrieve_store = extractor.list_number_of_stores(endpoint, headers)
retrieve_store

# Retrieve store data 
end_point_2 = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
store_data = extractor.retrieve_stores_data(endpoint = end_point_2, headers=headers, store_number=450)
print(store_data.head())

# TASK 6 
#s3_address = 's3://data-handling-public/products.csv'
#s3_data = extractor.extract_from_s3(s3_address)
#s3_data.head()

# Uploading cleaned s3_data to db
#s3_data_bot = pd.read_csv("s3_data.csv")
#s3_load = connector.upload_to_db(df = s3_data_bot, table_name='dim_products')
#s3_load

# TASK 7 
# Retreve the orders_table table from the central database
#orders_df = extractor.read_rds_table(engine, 'orders_table')
#orders_df.head()

# Uploading cleaned orders_data to db
#user_order = pd.read_csv("orders_df.csv")
#user_load = connector.upload_to_db(df = user_order, table_name='orders_table')
#user_load

# TASK 8 
# Extracting json data from AWS CLoud 
#bucket_name = 'data-handling-public'
#key = 'date_details.json'
#json_data = extractor.get_json_from_s3(bucket_name, key)
#json_data

# Uploading cleaned j_data to db
#j_data = pd.read_csv("j_data_csv")
#j_load = connector.upload_to_db(df = j_data, table_name='dim_date_times')
#j_load

# %%
