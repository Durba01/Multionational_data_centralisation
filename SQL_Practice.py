#%%
from sqlalchemy import create_engine
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'aicoredb.cvs16hdtbk8f.eu-west-2.rds.amazonaws.com' # Change it to your AWS endpoint
USER = 'postgres'
PASSWORD = '62260928'
PORT = 5432
DATABASE = 'aicoredb'
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
engine.connect() # connect the database with the VSCode

from sklearn.datasets import load_iris
import pandas as pd
data = load_iris()
iris = pd.DataFrame(data['data'], columns=data['feature_names'])
iris.head()

df = pd.read_sql_table('iris_dataset', engine)
df.head()

# %%
