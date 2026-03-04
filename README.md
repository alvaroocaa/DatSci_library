# DatSci

**DatSci** is a personal Python project aimed at automating recurring day-to-day data tasks performed at work.

The library is designed to support common data workflows, including:

- fetching data
- processing data
- analyzing data
- cleansing data
- exporting data

This project will continue to evolve as new use cases appear and additional recurring tasks are identified.

## Contributing

Contributions are welcome.

If you would like to contribute:

1. Create a new branch from `develop`
2. Make your changes in your own branch
3. Open a pull request into `develop`

Please avoid pushing directly to `main`.

Suggested branch naming:

- `feature/issue-id-short-description`
- `fix/issue-id-short-description`
- `docs/issue-id-short-description`

Examples:

- `feature/42-add-read-txt-options`
- `fix/15-handle-empty-files`
- `docs/8-update-readme`

## Branching Strategy

This repository follows a simple branching model:

- `main` → stable, release-ready code
- `develop` → active development branch
- `feature/*` → short-lived branches for each feature, fix, or documentation update (created from `develop`)

Recommended flow:

1. Create a feature branch from `develop`
2. Open a pull request into `develop`
3. Merge into `develop` after review
4. Merge `develop` into `main` once the code is stable

## Documentation

Documentation for the available functions can also be displayed by running:

**`read_me()`**

## Functions

### 1. `extract_df(file, directory, filename, ext)`

Exports a DataFrame into different file formats.

**Parameters:**

- **`file`**: DataFrame to export
- **`directory`**: destination directory. If not provided, the file is exported to the same directory where the script is located
- **`filename`**: name of the exported file
- **`ext`**: output file format. Supported values:
  - `excel`
  - `parquet`
  - `csv`
  - `txt`

---

### 2. `read_txt(directory, rows=0)`

Reads `.txt` files, especially files imported from SAP spool request outputs.

**Parameters:**

- **`directory`**: path to the `.txt` file
- **`rows`**: number of rows to skip. Optional. Default is `0`

---

### 3. `format_db(df, dupl=False, dupl_subs=False, blnk=False, type=False)`

Formats and cleans a DataFrame.

**Parameters:**

- **`df`**: DataFrame to clean
- **`dupl`**: remove duplicate rows if `True`. Default is `False`
- **`dupl_subs`**: remove duplicates based on a specific column name. Default is `False`
- **`blnk`**: remove blank rows if `True`. Default is `False`
- **`type`**: automatically detect data types if `True`. Default is `False`

---

### 4. `table_count(df, column)`

Creates a summary table based on a selected column in a DataFrame.

**Parameters:**

- **`df`**: DataFrame to summarize
- **`column`**: column used as the basis for the summary

---

### 5. `sh_excel(dfs, sheet_names, file_name, directory=False)`

Exports multiple DataFrames into a single Excel file, with each DataFrame stored in a different sheet.

**Parameters:**

- **`dfs`**: list or tuple of DataFrames to save
- **`sheet_names`**: list of sheet names
- **`file_name`**: name of the output Excel file, with or without the `.xlsx` extension
- **`directory`**: optional destination directory. Default is `False`

## Notes

This is an open-source project. Feel free to try it, suggest improvements, or open a pull request.