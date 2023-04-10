import pandas as pd
from datetime import timedelta
import numpy as np 

class DataFormatHandler:

    def __init__(self):
        self.site_column_header = 'Site ID'
        self.output_file_path = '../resources/output_exc.xlsx'
        self.sheet_name = 'input_refresh_template'
        self.data_frame_headers = [0,1,2]

    def format_site_data(self, xl_file_path: str):
        
        xls = pd.ExcelFile(xl_file_path)
        # Read xlsx file as a dataframe
        df = pd.read_excel(xls, sheet_name=self.sheet_name, header=self.data_frame_headers)
        
        # the existing data has a lot od duplicate header values
        # for example (Page Views, 2021/01/01) is repeated 100 times for each site
        
        # Assumption:
        # Site IDS in the data are always distinct and unique. With this assuption we can
        # safely remove dupicate header data.

        df.drop_duplicates(keep=False, inplace=True)

        #df.columns=pd.MultiIndex.from_tuples(df.columns)

        result = self.transform_data_frame(df)

        # add a column for day of the month
        result['Day of Month'] = result['Date'].dt.day

        result['Date'] = result['Date'].dt.date
        result = result.sort_values(['Site ID', 'Date'])

        # write to output file
        result.to_excel(self.output_file_path)  

    
    def transform_data_frame(self, df):
        start_date = df.columns.values.tolist()[0][0]
        end_date = df.columns.values.tolist()[0][1]

        # Assumption:
        # Site ID column header is always 'Site ID'. Based on this assumption we can
        # safely assume we consider all the site IDS dynamically from this column

        sites = df[(start_date, end_date, self.site_column_header)].tolist()

        # level 1 headers have the metrices
        columns_headers_level_1 = list(df.columns.levels[1])

        # getting all the metrices
        metrices = [col for col in columns_headers_level_1 if not col==end_date]

        result = pd.DataFrame()

        # for each metric convert date columns to rows 
        # this will make results as expected in output
        for metric in metrices:
            metric_df = df[ (start_date, metric)]
            metric_df['Site ID'] = sites

            # keep the Site ID constant and convert other columns to rows
            melted_metric = pd.melt(metric_df, id_vars=['Site ID'], var_name='Date', value_name=metric)
            if result.empty:
                result = melted_metric
            else:
                result = pd.merge(result, melted_metric)

        return result
