import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from unittest.mock import patch
import tempfile
pd.set_option('future.no_silent_downcasting', True)

# Importing functions to test
from datsci.datsci import extract_df, format_db, table_count, read_txt, sh_excel, read_me, similarity

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
        
def test_extract_df_txt(sample_dataframe, temp_directory):
    file_name = "test_file.txt"
    extract_df(sample_dataframe, temp_directory, file_name, "txt")
    assert os.path.exists(os.path.join(temp_directory, file_name))

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

def test_read_txt_non_utf8(temp_directory):
    """Test reading a non-utf-8 (latin-1) encoded text file with several lines."""
    text_file_path = os.path.join(temp_directory, "latin1_file.txt")
    lines = [
        "Col1\tCol2\n",
        "áéíóú\tñÑ\n",
        "foo\tbar\n"
    ]
    with open(text_file_path, "w", encoding="latin-1") as f:
        f.writelines(lines)

    df = read_txt(text_file_path)
    assert not df.empty
    assert list(df.columns) == ["Col1", "Col2"]
    assert "foo" in df["Col1"].values

def test_read_txt_complex_unnamed_and_empty_columns(temp_directory):
    """
    Test that:
    - Empty 'Unnam' columns are dropped,
    - Non-empty 'Unnam' columns are renamed to the following column,
    - Rows where column value == column name are filtered out,
    - Only the correct columns and values remain.
    """
    text_file_path = os.path.join(temp_directory, "complex_unnamed.txt")
    # Creating tab-separated content that fits your use case
    content = (
        "Test 1\tUnnam 1\tValidCol\tUnnam 2\n"
        "a1\t\t\tb1\n"
        "a2\t\t\tb2\n"
        "Test 1\tdata\tdata\t\n"  # To test filtering out rows where value == col name
    )
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    df = read_txt(text_file_path)

    # 'Unnam 1' is empty, should be dropped
    assert 'Unnam 1' not in df.columns

    # 'Unnam 2' is non-empty and next col 'ValidCol' is empty,
    # so 'Unnam 2' should be renamed to 'ValidCol' and 'ValidCol' dropped,
    # resulting in no 'ValidCol' column but renamed 'Unnam 2' column named 'ValidCol'
    assert 'ValidCol' in df.columns
    assert 'Unnam 2' not in df.columns

    # Filtered out rows where column value equals column name (e.g., "Test 1" in "Test 1" col)
    assert not (df['Test 1'] == 'Test 1').any()

    # Validate some values remain
    assert 'a1' in df['Test 1'].values
    assert 'b1' in df['ValidCol'].values

def test_read_txt_drop_unnamed_columns_with_whitespace_only(temp_directory):
    text_file_path = os.path.join(temp_directory, "whitespace_unnamed.txt")
    content = (
        "A\tUnnam 1\tB\n"
        "x\t   \ty\n"
        "z\t\tw\n"
    )
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    df = read_txt(text_file_path)
    assert "Unnam 1" not in df.columns
    
def test_read_txt_drop_multiple_empty_unnamed_columns(temp_directory):
    text_file_path = os.path.join(temp_directory, "multi_unnamed.txt")
    content = (
        "A\tUnnam 1\tUnnam 2\tB\n"
        "x\t\t\ty\n"
        "z\t\t\tw\n"
    )
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    df = read_txt(text_file_path)
    assert "Unnam 1" not in df.columns
    assert "Unnam 2" not in df.columns
    assert list(df.columns) == ["A", "B"]
    
def test_read_txt_unnamed_column_mixed_blank_types(temp_directory):
    text_file_path = os.path.join(temp_directory, "mixed_blank_unnamed.txt")
    content = (
        "A\tUnnam 1\tB\n"
        "x\t \ty\n"
        "z\t\tw\n"
    )
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    df = read_txt(text_file_path)
    assert "Unnam 1" not in df.columns
    
def test_read_txt_strips_header_spaces(temp_directory):
    text_file_path = os.path.join(temp_directory, "header_spaces.txt")
    content = (
        "  Col1  \t Unnam 1 \t Col2 \n"
        "a\t\tb\n"
    )
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    df = read_txt(text_file_path)
    assert "Col1" in df.columns
    assert "Col2" in df.columns
    
def test_read_txt_promotes_next_unnamed_into_empty_named_column(temp_directory):
    text_file_path = os.path.join(temp_directory, "promote_unnamed.txt")
    content = (
        "A\tValidCol\tUnnam 2\n"
        "x\t\tb1\n"
        "y\t\tb2\n"
    )
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    df = read_txt(text_file_path)
    assert "ValidCol" in df.columns
    assert "Unnam 2" not in df.columns
    assert "b1" in df["ValidCol"].values
    assert "b2" in df["ValidCol"].values
    assert len(df) == 2
        
def test_format_db_blnk_removes_all_nan_rows():
    df = pd.DataFrame({
        "A": [1, np.nan, 2],
        "B": [3, np.nan, np.nan]
    })
    formatted = format_db(df, blnk=True)
    assert len(formatted) == 2

# ===========================
# TEST FOR LEADING/TRAILING SPACES IN COLUMN NAMES
# ===========================

def test_column_names_no_leading_or_trailing_spaces(sample_dataframe):
    """Ensure no column names contain leading or trailing whitespace."""
    assert all(col == col.strip() for col in sample_dataframe.columns)


def test_column_names_stripped():
    """Ensure stripping logic correctly cleans column names."""
    df = pd.DataFrame({"  A  ": [1], " B": [2], "C ": [3]})
    cleaned = [col.strip() for col in df.columns]
    df.columns = cleaned
    assert all(col == col.strip() for col in df.columns)

# ===========================
# TESTS FOR format_db
# ===========================

def test_format_db(sample_dataframe):
    """Test format_db function for duplicate removal and blank handling."""
    formatted_df = format_db(sample_dataframe, dupl=True)
    assert len(formatted_df) < len(sample_dataframe)  # Duplicates removed

    formatted_df = format_db(sample_dataframe)
    assert not formatted_df.isnull().any().any()
    
def test_format_db_removes_duplicates(sample_dataframe):
    formatted_df = format_db(sample_dataframe, dupl=True)
    assert len(formatted_df) < len(sample_dataframe)
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
        
def test_table_count_values(sample_dataframe):
    count_df = table_count(sample_dataframe, "Category")
    a_count = count_df.loc[count_df["Categories"] == "A", "Count"].iloc[0]
    total_count = count_df.loc[count_df["Categories"] == "Total", "Count"].iloc[0]
    assert a_count == 3
    assert total_count == 6

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

def test_read_me_file_not_found():
    with patch("builtins.print") as mock_print:
        read_me()
        assert mock_print.called

# ===========================
# TESTS FOR similarity
# ===========================

def test_similarity_basic():
    a = ["hello world", "foo bar"]
    b = ["hello world", "bar foo"]
    result = similarity(a, b)
    assert len(result) == 2
    assert result[0] == 100  # Exact match
    assert result[1] > 75     # Partial and token ratios should yield high similarity

def test_similarity_empty_lists():
    assert similarity([], []) == []

def test_similarity_mismatched_lengths():
    with pytest.raises(ValueError, match="Length of both lists are not the same"):
        similarity(["a"], ["a", "b"])

def test_similarity_typo():
    a = ["hello world"]
    b = ["helloo world"]
    result = similarity(a, b)
    assert len(result) == 1
    assert 85 <= result[0] < 100  # Close match, not perfect
    
def test_similarity_case_difference():
    result = similarity(["Hello"], ["hello"])
    assert len(result) == 1
    assert result[0] < 100

# ===========================
# RUN TESTS
# ===========================

if __name__ == "__main__":
    pytest.main()
