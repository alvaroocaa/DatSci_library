import os
import pandas as pd
import numpy as np
    
def extract_df(file, directory, filename, ext):

    try:
        os.makedirs(directory, exist_ok=True)

    except:
        print('Directory does not exist')
        return
    
    try:

        if ext == 'excel':
            path = os.path.join(directory, filename)
            file.to_excel(path)

        elif ext == 'parquet':
            path = os.path.join(directory, filename)
            file.to_parquet(path)
        
        elif ext == 'csv':
            path = os.path.join(directory, filename)
            file.to_csv(path)

        if ext == 'txt':
            path = os.path.join(directory, filename)
            file.to_txt(path)

    except:
        print("Couldn't save successfully!")
        return
    

def format_db(df, **kwargs):

    dupl = kwargs.get('dupl', False)
    blnk = kwargs.get('blnk', False)
    
    if dupl and not blnk:
        return df.drop_duplicates()
    elif not dupl and blnk:
        return df.dropna()
    elif dupl and blnk:
        return df.drop_duplicates().dropna()
    else:
        return df  
    

def table_count(df, categories, column):

    Count_list = []
    Count_list_xcent = []

    for cat in categories:

        df_filtered = df[df[column] == cat]
        Count_list.append(len(df_filtered))
        Count_list_xcent.append(len(df_filtered) / len(df))

    categories = categories.append('Total')
    Count_list = Count_list.append(len(df))
    Count_list_xcent = Count_list_xcent.append(len(df) / len(df))

    return pd.DataFrame({
        'Categories': categories,
        'Count': Count_list,
        'Count (%)': Count_list_xcent
    })

