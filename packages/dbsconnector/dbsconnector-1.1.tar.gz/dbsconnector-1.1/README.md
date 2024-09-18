# Database Connector Package

# Overview
**dbsconnector** is a Python package designed to simplify data integration from various sources, including CSV, Excel, Google Sheets, and MongoDB. The package provides a unified interface to connect, load, and process data with minimal setup, making it easier for Developers and Data Scientists to work across multiple data formats.

# Current Features:
- Connect to CSV files and load them into a Pandas DataFrame
- Handle Excel files with multiple sheets
- Fetch data from Google Sheets using an API key
- Interact with MongoDB collections

# Future Features (Upcoming):
- Support for more databases (SQL, NoSQL)
- Cloud storage integration (AWS S3, Google Cloud, etc.)
- API-based data sources

# Installation
To install the package, use pip:
```bash
pip install dbsconnector==1.1
```

# How to use this package?

## Connecting to csv
```py
# import the module:
from dbsconnector import databases
# load the data:
df = databases.load_csv(filepath='sample.csv', delimiter=',')
# display the data:
df
```

## Connecting to Excel
```py
# import the module:
from dbsconnector import databases
# load the data:
df = databases.load_excelsheet(filepath='sample.xlsx', sheet_name='sample_sheet')
# display the data:
df
```

## Connecting to gsheet
```py
# import the module:
from dbsconnector import databases
# load the data:
df = databases.load_gsheet(gsheet_id='17r9f4BL7sjmdLBnt92OdQP3CHK5bdT3hozg6DUJXGqU',sheet_name='sample_sheet')
# display the data:
df
```

## Connecting to MongoDB
```py
# import the module:
from dbsconnector import databases
# load the data:
df = databases.load_mongodbdata(host='localhost', database='sample_database', collection='sample_collection')
# display the data:
df
```

# Contributions
* Contributions are welcome! Please open an issue or submit a pull request on GitHub for adding new features, fixing bugs, or improving documentation. Open-source collaboration is highly encouraged!

# License
This project is licensed under the MIT License.

# Contact
For any questions or suggestions, please contact [yuvaneshkm05@gmail.com](yuvaneshkm05@gmail.com)

# Connect
Connect with me on [LinkedIn](https://www.linkedin.com/in/yuvaneshkm)
