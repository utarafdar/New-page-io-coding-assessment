# New-page-io-coding-assessment

## Description

This is a python project that cleans site metrics data. The site metrics data is in the format as shown in **/resources/test_exc.xlsx** file. This application reads the xl file using python pandas library. The data from the metrics file is converted to a dataframe. Cleans it and transforms it in a cleaner format as shown in **resources/output_exc.xlsx file**

# Transformations 
1. Remove duplicates
2. Convert the metric dates from column to rows using pandas melt function
3. Add day of the month column
4. clean Date values to format yyyy/mm/dd from pandas date time format

## Installation steps
# Go to the root project folder and activate virtual env
```
python3 -m venv .venv

source .venv/bin/activate
```

# Install dependencies
```
pip3 install -r requirements.txt

```

# Go to src folder and run the project

```
cd src

python3 main.py
```

## Run tests
go to tests folder from root folder
```
cd tests

pytest test_data_format_handler.py 

```


## Edge cases and limitations

1. The number of sites can be dynamic
2. The metrics can also be dynamic. Once can add more metrics or remove some, the code will still work
3. The format of data input should be same as the input file
4. One short coming is the data is not accurately sorted based on Site IDs. The site 10 comes next to site 1 instead of site 2. thi is becase site id is a string. This can be handle in a better way.
5. Exception handling is not done due to time constraints
