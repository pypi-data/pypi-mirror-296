# OracleDBHandler Library

## Overview

`OracleDBHandler` is a Python class designed to simplify interactions with an Oracle database. It provides functionality to connect to the database, insert and update data from a `pandas` DataFrame, execute arbitrary queries, delete data, check for duplicate records, and more. (Link: https://pypi.org/project/OracleDBHandler/)

## Features

- **Connect** to an Oracle database.
- **Insert** data from a `pandas` DataFrame.
- **Update** data in an Oracle table.
- **Execute arbitrary queries** with or without parameters and return the results.
- **Delete** data from tables with or without conditions.
- **Check for duplicates** in a table based on specified columns.
- **Close** the connection to the Oracle database.

## Requirements

Make sure you have the necessary libraries installed:

- Python 3.x
- `oracledb` and `pandas` libraries:
  ```bash
  pip install oracledb pandas

## Installation

Install via pip: 

```bash
pip install OracleDBHandler
```

## Usage

### 1. Initialize and Connect to Oracle Database

Instantiate the `OracleDBHandler` class with your Oracle database credentials and call the `connect` method.

```python
from OracleDBHandler import OracleDBHandler

db_handler = OracleDBHandler(
    user='your_user',
    password='your_password',
    host='your_host',
    port='your_port',
    serviceName='your_service'
)

db_handler.connect()
```

### 2. Insert Data into Oracle Table
```python
import pandas as pd

data = {'ID': [1, 2], 'Name': ['John', 'Alice'], 'Age': [25, 30]}
df = pd.DataFrame(data)
db_handler.insert_data(df, 'your_table')
```

### 3. Update Data in Oracle Table
```python
updated_data = {'ID': [1], 'Name': ['John Updated'], 'Age': [26]}
df_update = pd.DataFrame(updated_data)
db_handler.update_data(df_update, 'your_table', 'ID')
```

### 4. Execute Arbitrary Queries
```python
query = "SELECT * FROM your_table WHERE Age > :age"
params = {'age': 25}
result = db_handler.execute_query(query, params)
print(result)
```

### 5. Delete Data from a Table
```python
# Delete data with condition
db_handler.delete_data('your_table', 'Age > 30')

# Delete all data
db_handler.delete_data('your_table')
```

### 6. Check for Duplicate Records
```python
# Check for duplicates based on specific columns
duplicates = db_handler.check_duplicates('your_table', ['Name', 'Age'])
print(duplicates)

# Check for duplicates across all columns
duplicates_all = db_handler.check_duplicates('your_table')
print(duplicates_all)
```

### 7. Close the Database Connection
```python
db_handler.close()
```

## Error Handling
The library provides basic error handling for database-related issues. If a connection or query fails, the exception message is printed, and the transaction is rolled back if necessary.

## License
This project is licensed under the MIT License.