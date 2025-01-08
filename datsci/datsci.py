import os
import pandas as pd # type: ignore
import numpy as np # type: ignore

def extract_df(file, directory, filename, ext):
    try:
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

    except Exception as e:
        print(f'Directory creation failed: {e}')
        return

    try:
        # Check for supported file extensions
        if ext == 'excel':
            path = os.path.join(directory, filename)
            file.to_excel(path)

        elif ext == 'parquet':
            path = os.path.join(directory, filename)
            file.to_parquet(path)
        
        elif ext == 'csv':
            path = os.path.join(directory, filename)
            file.to_csv(path)

        elif ext == 'txt':
            path = os.path.join(directory, filename)
            # Assuming there is a `to_txt` method or alternative code for saving txt
            file.to_csv(path, sep='\t')  # Temporary workaround if `to_txt` is not implemented

        else:
            # Raise ValueError if the extension is unsupported
            raise ValueError(f"Unsupported file format: {ext}")

    except Exception as e:
        print(f"Couldn't save successfully! Error: {e}")
        raise  # Re-raise the exception to ensure it's handled properly


def read_txt(directory, **kwargs):

    with open(directory, 'r', encoding='utf-8') as file:
        text = file.read()

    cleaned_text = text.replace('"', '').replace("'", '')
    dir_name, base_name = os.path.split(directory)
    file_name, file_ext = os.path.splitext(base_name)
    cleaned_file_path = os.path.join(dir_name, f"{file_name}_cleaned{file_ext}")

    with open(cleaned_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    rows = kwargs.get('rows', 0)

    df = pd.read_csv(rf'{cleaned_file_path}', skip_rows = rows, encoding ='latin', sep = '\t')
    return df


def format_db(df, **kwargs):

    dupl = kwargs.get('dupl', False)
    dupl_subs = kwargs.get('dupl_subs', False)
    blnk = kwargs.get('blnk', False)
    type = kwargs.get('type', False)
    
    if dupl:
        df = df.drop_duplicates()

    if dupl_subs:
        df = df.drop_duplicates(subset=[dupl_subs])
    
    if blnk:
        df = df.dropna(how='all')

    if type:
        df = df.convert_dtypes()

    return df
    

def table_count(df, column):
    
    categories = pd.unique(df[column])

    # Check if df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The 'df' parameter must be a pandas DataFrame.")
    
    # Ensure 'column' is a string (the name of the column to filter by)
    if not isinstance(column, str):
        raise ValueError("The 'column' parameter must be a string representing the column name.")
    
    # Check if the specified column exists in the dataframe
    if column not in df.columns:
        raise ValueError(f"The specified column '{column}' does not exist in the dataframe.")

    # Check if categories is empty
    if len(categories.tolist()) == 0:
        raise ValueError("The 'categories' list cannot be empty.")
    
    categories = categories.tolist()
    
    # Initialize lists to store counts and percentages
    Count_list = []
    Count_list_xcent = []

    # Iterate through each category to count occurrences
    for cat in categories:
        if pd.isna(cat): 
            df_filtered = df[df[column].isna()]
        else:
            df_filtered = df[df[column] == cat]
        
        Count_list.append(len(df_filtered))
        Count_list_xcent.append(len(df_filtered) / len(df) * 100)  # Convert to percentage

    # Add the total category
    categories.append('Total')
    Count_list.append(len(df))  # Total count
    Count_list_xcent.append(100)  # Total percentage is always 100%

    # Create a new DataFrame with the results
    return_df = pd.DataFrame({
        'Categories': categories,
        'Count': Count_list,
        'Count (%)': Count_list_xcent
    })

    return return_df


