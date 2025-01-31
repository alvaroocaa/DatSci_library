import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from io import StringIO
from unittest.mock import patch
import tempfile

# Importing functions to test
from datsci.datsci import extract_df, format_db, table_count, read_txt, sh_excel

# ===========================
# FIXTURES
# ===========================

@pytest.fixture
def sample_dataframe():
    """Fixture providing a sample DataFrame for testing."""
    return pd.DataFrame({
        "Category": ["A", "B", "A", "C", "B", "A"],
        "Value": [10, 20, 10, 30, 20, 10]
    })

@pytest.fixture
def sample_dataframes():
    """Fixture providing multiple DataFrames and corresponding sheet names for testing sh_excel."""
    dfs = (
        pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}),
        pd.DataFrame({"X": ["a", "b", "c"], "Y": [True, False, True]})
    )
    sheet_names = ("Sheet1", "Sheet2")
    return dfs, sheet_names

@pytest.fixture
def temp_directory():
    """Fixture creating a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def temp_excel_file():
    """Fixture creating a temporary file path for Excel output."""
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmpfile:
        yield tmpfile.name
    os.remove(tmpfile.name)  # Cleanup after test

# ===========================
# TESTS FOR extract_df
# ===========================

def test_extract_df(sample_dataframe, temp_directory):
    """Test extract_df function with different formats."""
    file_name = "test_file.xlsx"
    extract_df(sample_dataframe, temp_directory, file_name, "excel")
    assert os.path.exists(os.path.join(temp_directory, file_name))

    file_name = "test_file.csv"
    extract_df(sample_dataframe, temp_directory, file_name, "csv")
    assert os.path.exists(os.path.join(temp_directory, file_name))

    with pytest.raises(ValueError):
        extract_df(sample_dataframe, temp_directory, "test_file.xyz", "xyz")

# ===========================
# TESTS FOR read_txt
# ===========================

def test_read_txt(temp_directory):
    """Test reading a text file with tab-separated values."""
    text_file_path = os.path.join(temp_directory, "test_file.txt")
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write("Column1\tColumn2\nValue1\tValue2\n")

    df = read_txt(text_file_path)
    assert not df.empty
    assert list(df.columns) == ["Column1", "Column2"]

# ===========================
# TESTS FOR format_db
# ===========================

def test_format_db(sample_dataframe):
    """Test format_db function for duplicate removal and blank handling."""
    formatted_df = format_db(sample_dataframe, dupl=True)
    assert len(formatted_df) < len(sample_dataframe)  # Duplicates removed

    formatted_df = format_db(sample_dataframe, blnk=True)
    assert not formatted_df.isnull().any().any()  # No blanks should remain

# ===========================
# TESTS FOR table_count
# ===========================

def test_table_count(sample_dataframe):
    """Test table_count function for valid category counting."""
    count_df = table_count(sample_dataframe, "Category")
    assert "Categories" in count_df.columns
    assert "Count" in count_df.columns
    assert "Count (%)" in count_df.columns

    assert len(count_df) == len(sample_dataframe["Category"].unique()) + 1  # Unique categories + total

    with pytest.raises(ValueError):
        table_count(sample_dataframe, "NonExistentColumn")  # Column doesn't exist

    with pytest.raises(ValueError):
        table_count(sample_dataframe, 123)  # Column name is not a string

# ===========================
# TESTS FOR sh_excel
# ===========================

def test_sh_excel_default_path(sample_dataframes, temp_excel_file):
    """Test saving an Excel file with a default file path (no directory)."""
    dfs, sheet_names = sample_dataframes
    sh_excel(dfs, sheet_names, temp_excel_file)

    assert os.path.exists(temp_excel_file)

    with pd.ExcelFile(temp_excel_file) as xls:
        assert set(xls.sheet_names) == set(sheet_names)

def test_sh_excel_with_directory(sample_dataframes, temp_directory):
    """Test saving an Excel file inside a specified directory."""
    dfs, sheet_names = sample_dataframes
    file_name = "test_output.xlsx"

    sh_excel(dfs, sheet_names, file_name, directory=temp_directory)

    expected_path = os.path.join(temp_directory, file_name)
    assert os.path.exists(expected_path)

    with pd.ExcelFile(expected_path) as xls:
        assert set(xls.sheet_names) == set(sheet_names)

def test_sh_excel_missing_extension(sample_dataframes, temp_directory):
    """Test that file_name without .xlsx gets corrected."""
    dfs, sheet_names = sample_dataframes
    file_name = "test_output"  # No .xlsx

    sh_excel(dfs, sheet_names, file_name, directory=temp_directory)

    expected_path = os.path.join(temp_directory, "test_output.xlsx")
    assert os.path.exists(expected_path)

def test_sh_excel_invalid_inputs(sample_dataframes, temp_excel_file):
    """Test error handling for invalid inputs in sh_excel."""
    dfs, sheet_names = sample_dataframes

    # Mismatched dfs and sheet_names lengths
    with pytest.raises(ValueError, match="must have the same length"):
        sh_excel(dfs, ("Sheet1",), temp_excel_file)

    # Non-list/tuple inputs
    with pytest.raises(ValueError, match="must be of type tuple or list"):
        sh_excel("not_a_list", sheet_names, temp_excel_file)

    with pytest.raises(ValueError, match="must be of type tuple or list"):
        sh_excel(dfs, "not_a_list", temp_excel_file)

    # Non-DataFrame elements in dfs
    with pytest.raises(ValueError, match="Each element in 'dfs' must be a pandas DataFrame"):
        sh_excel([1, 2, 3], sheet_names, temp_excel_file)

# ===========================
# RUN TESTS
# ===========================

if __name__ == "__main__":
    pytest.main()
