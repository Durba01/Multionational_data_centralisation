#%%
import pandas as pd
import numpy as np
# Step 6
class DataCleaning:
    def __init__(self):
        pass
    def clean_user_data(self, user_df):
        for col in user_df.select_dtypes(include=['object']):
            try:
                user_df[col] = pd.to_numeric(user_df[col])
            except ValueError:
                user_df[col] = np.nan
        if user_df.select_dtypes(include=['object']).nunique().sum() > 0:
            return user_df.select_dtypes(include=['object'])
        else:
            return "All incorrectly typed values have been corrected."


# MILESTONE 4 STEP 3
    # return card data 
    def clean_card_data(self, data):
        clean_data = []
        for value in data:
            if value is None:
                continue
            try:
                float(value)
                clean_data.append(value)
            except ValueError:
                continue
        return clean_data

cleaning = DataCleaning()

