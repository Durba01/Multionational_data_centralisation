import pandas as pd

# Step 6
class DataClean:
    def __init__(self):
        pass
    
    def clean_user_data(df):
        # Replace NULL values with a default value or method of your choice
        df.fillna(0, inplace=True)

        # Convert age column to integer if possible, otherwise replace with default value
        def to_int(x):
            try:
                return int(x)
            except:
                return 0

        df['age'] = df['age'].apply(to_int)

        # Remove rows with incorrect or inconsistent information
        df = df[df['age'] >= 0]

        return df
    #This method takes a pandas DataFrame as an argument and returns a cleaned version of the DataFrame. It first replaces any NULL values with a default value of 0, then converts the age column to integer if possible, otherwise replaces with default value. Finally, it removes any rows with incorrect or inconsistent information by keeping only those rows where the age column is greater than or equal to 0.

    




    
