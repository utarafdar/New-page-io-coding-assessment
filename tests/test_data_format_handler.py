import pytest
import pandas as pd
import sys
import os
sys.path.insert(1, '../src')

from data_format_handler import DataFormatHandler


@pytest.fixture()
def resource_df():
    xls = pd.ExcelFile('../tests/resources/test_file.xlsx')
    df = pd.read_excel(xls, sheet_name='input_refresh_template', header=[0,1,2])
    df.drop_duplicates(keep=False, inplace=True)
    yield df

    # tear down
    if os.path.exists("../tests/resources/output_exc.xlsx"):
        os.remove('../tests/resources/output_exc.xlsx')


class TestDataFormatHandler:

    # test if output files is created
    def test_format_site_data(self, monkeypatch):
        self.data_format_handler = DataFormatHandler()
        self.data_format_handler.output_file_path = '../tests/resources/output_exc.xlsx'
        self.data_format_handler.format_site_data('../tests/resources/test_file.xlsx')
        assert os.path.exists("../tests/resources/output_exc.xlsx") == True
    
    
    # test if results of tranformation are accurate
    def test_transform_data_frame(self, resource_df):
        self.data_format_handler = DataFormatHandler()
        result = self.data_format_handler.transform_data_frame(resource_df)
        print(list(result.columns))
        assert list(result.columns) == ['Site ID', 'Date', 'Page Views', 'Total Time Spent', 'Unique Visitors']
        assert result.shape == (300, 5)

