import os
import pandas as pd # type: ignore
import numpy as np # type: ignore
import openpyxl # type: ignore
import tempfile
import xlsxwriter # type: ignore
import chardet # type:ignore
from rapidfuzz import fuzz #type: ignore

def extract_df(file, directory, filename, ext):
    try:
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

    except Exception as e:
        raise ValueError(f"Directory creation failed: {ext}")

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

    # Open the file in binary as reading mode to detect the file's encoding using chardet library
    with open(directory, 'rb') as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    encode =  detector.result['encoding'] # Return file's encoding

    # Read file with the correct encoding detected as before
    with open(directory, 'r', encoding=encode) as file:
        text = file.read()

    # Clean the text by removing unwanted characters (" and ')
    cleaned_text = text.replace('"', '').replace("'", '')

    # Create a temporary file and write the cleaned text to it
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', newline='') as tmp_file:
        tmp_file.write(cleaned_text)
        tmp_file_path = tmp_file.name  # Get the path to the temporary file

    # Read Dataframe from cleaned file
    rows = kwargs.get('rows', 0)
    df = pd.read_csv(tmp_file_path, skiprows=rows, encoding='utf-8', sep='\t') # Read the cleaned text with UTF-8 encoding (as rewritten above)
    os.remove(tmp_file_path) # Remove temporary file

    for col in df.columns:
        if 'Unna' not in col and not df[col].isna().all():
            df = df[df[col] != col]
            print(f"Filtered using column: {col}")
            break
    else:
        print("No valid column found.")

    i = 0
    while i < len(df.columns):
        col = df.columns[i]

        # Case 1: Column contains 'Unna' and is completely empty — drop it
        if 'Unna' in col and df[col].isna().all():
            df = df.drop(columns=[col])
            # Don't increment i because columns shifted left
            continue

        # Case 2: Column contains 'Unna' and is NOT empty
        if 'Unna' in col and not df[col].isna().all():
            if i + 1 < len(df.columns):
                next_col = df.columns[i + 1]

                # Next column does NOT contain 'Unna' and IS empty
                if 'Unna' not in next_col and df[next_col].isna().all():
                    # Rename current col to a temp unique name
                    temp_name = col + "_temp_rename"

                    df = df.rename(columns={col: temp_name})

                    # Drop the next (empty) column
                    df = df.drop(columns=[next_col])

                    # Rename temp column to the next_col's original name
                    df = df.rename(columns={temp_name: next_col})

                    # Don't increment i because columns shifted
                    continue

        i += 1


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

    # Check if df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The 'df' parameter must be a pandas DataFrame.")
    
    # Ensure 'column' is a string (the name of the column to filter by)
    if not isinstance(column, str):
        raise ValueError("The 'column' parameter must be a string representing the column name.")
    
    # Check if the specified column exists in the dataframe
    if column not in df.columns:
        raise ValueError(f"The specified column '{column}' does not exist in the dataframe.")
    
    categories = pd.unique(df[column])

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

def sh_excel(dfs, sheet_names, file_name, **kwargs):

    directory = kwargs.get('directory', False)

    if not all(isinstance(arg, (tuple, list)) for arg in (dfs, sheet_names)):
        raise ValueError("'dfs' and 'sheet_names' input parameters must be of type tuple or list")
        
    if not all(isinstance(df, pd.DataFrame) for df in dfs):
        raise ValueError("Each element in 'dfs' must be a pandas DataFrame.")

    if len(dfs) != len(sheet_names):
        raise ValueError("'dfs' and 'sheet_names' must have the same length")

    if not all(isinstance(name, str) for name in sheet_names):
        raise ValueError("Each element in 'sheet_names' must be a string.")
    
    if not file_name.lower().endswith(".xlsx"):
        file_name += ".xlsx"

    if directory and isinstance(directory, str):
        file_name = os.path.join(directory, file_name)

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        for df, sheet_name in zip(dfs, sheet_names):
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Each element in 'dfs' must be a pandas DataFrame")
            writer.book.use_zip64()  
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Excel file '{file_name}' saved successfully!")
    
def read_me():
    try:
        with open("README.md", "r", encoding="utf-8") as file:
            content = file.read()
        fixed_content = content.replace('\u00A0', ' ').replace('*','')
        print(fixed_content)
    except FileNotFoundError:
        print("README.md file not found.")
    except Exception as e:
        print(f"Error reading README.md: {e}")

def similarity(a, b):

    if len(a) != len(b):
        raise ValueError(f"Length of both lists are not the same: {len(a)} != {len(b)}")
    
    else:
        return_list = []

        for x, y in zip(a,b):

            ratio = fuzz.ratio(x, y)
            partial_ratio = fuzz.partial_ratio(x, y)
            sort_ratio = fuzz.token_sort_ratio(x, y)
            set_ratio = fuzz.token_set_ratio(x, y)

            return_list.append((ratio + partial_ratio + sort_ratio + set_ratio) / 4)

    return return_list