import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd
import numpy as np
import os
from io import StringIO
from unittest.mock import patch
from datsci.datsci import extract_df, format_db, table_count

# Sample DataFrame for testing
@pytest.fixture
def sample_df():
    data = {
        'Category': ['A', 'B', 'A', 'B', 'C', 'A', np.nan, np.nan],
        'Value': [1, 2, 1, 4, 5, np.nan, 7, np.nan]
    }
    return pd.DataFrame(data)

# Test extract_df function
@patch('os.makedirs')
@patch.object(pd.DataFrame, 'to_excel')
@patch.object(pd.DataFrame, 'to_parquet')
@patch.object(pd.DataFrame, 'to_csv')
def test_extract_df(mock_to_csv, mock_to_parquet, mock_to_excel, mock_makedirs, sample_df):
    # Test Excel export
    extract_df(sample_df, 'test_dir', 'test_file.xlsx', 'excel')
    mock_makedirs.assert_called_once_with('test_dir', exist_ok=True)
    mock_to_excel.assert_called_once_with('test_dir/test_file.xlsx')

    # Test Parquet export
    extract_df(sample_df, 'test_dir', 'test_file.parquet', 'parquet')
    mock_to_parquet.assert_called_once_with('test_dir/test_file.parquet')

    # Test CSV export
    extract_df(sample_df, 'test_dir', 'test_file.csv', 'csv')
    mock_to_csv.assert_called_once_with('test_dir/test_file.csv')

    # Test invalid format (should not raise an error)
    extract_df(sample_df, 'test_dir', 'test_file.txt', 'txt')
    # Mock for txt export is missing, test should pass without any calls here

# Test format_db function
def test_format_db(sample_df):
    # Test dropping duplicates (dupl=True)
    df_no_duplicates = format_db(sample_df, dupl=True, blnk=False)
    assert len(df_no_duplicates) == 7  # Should drop the duplicate entries

    # Test dropping NaN (blnk=True)
    df_no_blank = format_db(sample_df, dupl=False, blnk=True)
    assert df_no_blank.isnull().sum().sum() == 0  # Should drop the row with NaN in both columns

    # Test dropping both duplicates and NaN
    df_no_dupl_no_blank = format_db(sample_df, dupl=True, blnk=True)
    assert len(df_no_dupl_no_blank) == 4  # Should drop duplicate 'A' and NaN

    # Test without dropping anything
    df_no_changes = format_db(sample_df, dupl=False, blnk=False)
    assert len(df_no_changes) == 8  # Should return the original DataFrame without changes

# Test table_count function
def test_table_count(sample_df):
    categories = pd.Series(['A', 'B', 'C'])
    result_df = table_count(sample_df, categories, 'Category') #PETA EN EL .APPEND('TOTAL) DE A LIBRERIA PQ SE LE PASA UNA PD.SERIES I NO UN ARRAY, TENER EN CUENTA VARIOS TIPOS DE INPUTS

    # Check if 'Total' row is added
    assert 'Total' in result_df['Categories'].values

    # Check that count and percentage for 'Total' is correct
    total_count = len(sample_df)
    total_percent = total_count / total_count
    assert result_df[result_df['Categories'] == 'Total']['Count'].values[0] == total_count
    assert result_df[result_df['Categories'] == 'Total']['Count (%)'].values[0] == total_percent

    # Check if the count and percentages for the categories are correct
    for cat in categories:
        cat_count = len(sample_df[sample_df['Category'] == cat])
        cat_percent = cat_count / len(sample_df)
        assert result_df[result_df['Categories'] == cat]['Count'].values[0] == cat_count
        assert result_df[result_df['Categories'] == cat]['Count (%)'].values[0] == cat_percent

# Test edge cases for table_count (e.g., missing categories)
def test_table_count_empty_categories(sample_df):
    categories = pd.Series([])
    result_df = table_count(sample_df, categories, 'Category')
    assert result_df.empty  # Should return an empty DataFrame when no categories are provided

# Test edge cases for extract_df (nonexistent directory, wrong file format)
@patch('os.makedirs')
@patch.object(pd.DataFrame, 'to_excel')
@patch.object(pd.DataFrame, 'to_parquet')
@patch.object(pd.DataFrame, 'to_csv')
def test_extract_df_invalid_format(mock_to_csv, mock_to_parquet, mock_to_excel, mock_makedirs, sample_df):
    # Test invalid file format
    with pytest.raises(ValueError):
        extract_df(sample_df, 'test_dir', 'test_file.xyz', 'xyz')

    # Test directory creation failure (e.g., permission issues or path length issues)
    mock_makedirs.side_effect = OSError('Permission Denied')
    extract_df(sample_df, 'test_dir', 'test_file.csv', 'csv')  # Should print error message

if __name__ == '__main__':
    pytest.main()
