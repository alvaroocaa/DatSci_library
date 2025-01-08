import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import os
from io import StringIO
from unittest.mock import patch
from datsci.datsci import extract_df, format_db, table_count, read_txt
import tempfile

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "Category": ["A", "B", "A", "C", "B", "A"],
        "Value": [10, 20, 10, 30, 20, 10]
    })

@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

# Test for extract_df
def test_extract_df(sample_dataframe, temp_directory):
    file_name = "test_file.xlsx"
    extract_df(sample_dataframe, temp_directory, file_name, "excel")
    assert os.path.exists(os.path.join(temp_directory, file_name))

    file_name = "test_file.csv"
    extract_df(sample_dataframe, temp_directory, file_name, "csv")
    assert os.path.exists(os.path.join(temp_directory, file_name))

    with pytest.raises(ValueError):
        extract_df(sample_dataframe, temp_directory, "test_file.xyz", "xyz")

# Test for read_txt
def test_read_txt(temp_directory):
    text_file_path = os.path.join(temp_directory, "test_file.txt")
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write("Column1\tColumn2\nValue1\tValue2\n")

    df = read_txt(text_file_path)
    assert not df.empty
    assert list(df.columns) == ["Column1", "Column2"]

# Test for format_db
def test_format_db(sample_dataframe):
    formatted_df = format_db(sample_dataframe, dupl=True)
    assert len(formatted_df) < len(sample_dataframe)  # Duplicates removed

    formatted_df = format_db(sample_dataframe, blnk=True)
    assert not formatted_df.isnull().any().any()  # No blanks should remain

# Test for table_count
def test_table_count(sample_dataframe):
    count_df = table_count(sample_dataframe, "Category")
    assert "Categories" in count_df.columns
    assert "Count" in count_df.columns
    assert "Count (%)" in count_df.columns

    assert len(count_df) == len(sample_dataframe["Category"].unique()) + 1  # Unique categories + total

    with pytest.raises(ValueError):
        table_count(sample_dataframe, "NonExistentColumn")  # Column doesn't exist

    with pytest.raises(ValueError):
        table_count(sample_dataframe, 123)  # Column name is not a string

# Run the tests if script is executed directly
if __name__ == "__main__":
    pytest.main()
