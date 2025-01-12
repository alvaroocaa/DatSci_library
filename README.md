# DatSci

Personal project to create a Python library to automatize recurrent day-to-day tasks performed at work involving treatment of data. This library will be updated as new necessities are faced and recurrent tasks need to be performed. 

It has been though as a library that will execute functions from different data streams:
* Fetching data
* Processing it
* Analyzing
* Cleansing

If anyone wants to give it a try feel free, it is an open-source project and contact me any time or create a push-request if you would like to contribute.

As of day 11/12/2024 official release of version 0.1. Stable version but will be worked and updated very soon as this is just a test that the project is working but give it a few months until it really becomes useful.


**Functions:**

1. **extract_df(file, directory, filename, ext):**

Function to export dataframes into different file formats. The parameters to be inputed are as follows:

* **file:** dataframe to be exported
* **directory:** directory where the file will be exported, if not indicated it will be exported into the directory where the script is located
* **filename:** the name that the exported file will gave
* **ext:** the type of file to be created. Extensions supported are:
    * **excel**
    * **parquet**
    * **csv**
    * **txt**

2. **read_txt(directory, rows=):**

Function created to read txt files specially imported from the SAP spool request options. The parameters to be inputed are as follows:

* **directory:** directory where the txt file to be read is located
* **rows=:** rows to be skipped, **OPTIONAL** parameter, default is 0

3. **format_db(df, dupl=, dupl_subs=, blnk=, type=):**

Function to format/clean a dataframe. The parameters to be inputed are as follows:

* **df:** dataframe to format/clean
* **dupl=:** if duplicate rows should be dropped =True, default is =False
* **dupl_subs=:** if duplicate rows should be dropped by looking at one row specifically indicate ='name of row', default is =False
* **blnk=:** if blank rows should be dropped =True, default is =False
* **type=:** if rows data type should be detected automatically =True, default is =False

4. **table_count(df, column):**

Function to create a table summarizing the data in a dataframe. The parameters to be inputed are as follows:

* **df:** dataframe to summarize the data
* **column:** the column that should be taken as the backbone to summarize the data