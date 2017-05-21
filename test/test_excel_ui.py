"""
Unit tests for the excel_ui module.

"""

import os
import collections
import unittest

import numpy as np
import pandas as pd
import pandas.util.testing as tm

import FlowCal

class TestReadTable(unittest.TestCase):
    """
    Class to test excel_ui.read_table()

    """
    def setUp(self):
        # Name of the file to read
        self.filename = 'test/test_excel_ui.xlsx'

    def test_read_table(self):
        """
        Test for proper loading of a table from an Excel sheet.

        """
        # Sheet to read
        sheetname = "Instruments"
        # Column to use as index labels
        index_col = "ID"

        # Expected output
        expected_output_list = []
        row = {}
        row['Description'] = 'Moake\'s Flow Cytometer'
        row['Forward Scatter Channel'] = 'FSC-H'
        row['Side Scatter Channel'] = 'SSC-H'
        row['Fluorescence Channels'] = 'FL1-H, FL2-H, FL3-H'
        row['Time Channel'] = 'Time'
        expected_output_list.append(row)
        row = {}
        row['Description'] = 'Moake\'s Flow Cytometer (new acquisition card)'
        row['Forward Scatter Channel'] = 'FSC'
        row['Side Scatter Channel'] = 'SSC'
        row['Fluorescence Channels'] = 'FL1, FL2, FL3'
        row['Time Channel'] = 'TIME'
        expected_output_list.append(row)
        expected_index = pd.Series(['FC001', 'FC002'], name='ID')
        expected_columns = ['Description',
                            'Forward Scatter Channel',
                            'Side Scatter Channel',
                            'Fluorescence Channels',
                            'Time Channel']

        expected_output = pd.DataFrame(expected_output_list,
                                       index=expected_index,
                                       columns=expected_columns)

        # Read table
        table = FlowCal.excel_ui.read_table(self.filename,
                                            sheetname=sheetname,
                                            index_col=index_col)

        # Compare
        tm.assert_frame_equal(table, expected_output)

    def test_read_table_no_index_col(self):
        """
        Test proper loading of a table when no index column is specified.

        """
        # Sheet to read
        sheetname = "Instruments"

        # Expected output
        expected_output_list = []
        row = {}
        row['ID'] = 'FC001'
        row['Description'] = 'Moake\'s Flow Cytometer'
        row['Forward Scatter Channel'] = 'FSC-H'
        row['Side Scatter Channel'] = 'SSC-H'
        row['Fluorescence Channels'] = 'FL1-H, FL2-H, FL3-H'
        row['Time Channel'] = 'Time'
        expected_output_list.append(row)
        row = {}
        row['ID'] = 'FC002'
        row['Description'] = 'Moake\'s Flow Cytometer (new acquisition card)'
        row['Forward Scatter Channel'] = 'FSC'
        row['Side Scatter Channel'] = 'SSC'
        row['Fluorescence Channels'] = 'FL1, FL2, FL3'
        row['Time Channel'] = 'TIME'
        expected_output_list.append(row)
        expected_columns = ['ID',
                            'Description',
                            'Forward Scatter Channel',
                            'Side Scatter Channel',
                            'Fluorescence Channels',
                            'Time Channel']

        expected_output = pd.DataFrame(expected_output_list,
                                       columns=expected_columns)

        # Read table
        table = FlowCal.excel_ui.read_table(self.filename,
                                            sheetname=sheetname)

        # Compare
        tm.assert_frame_equal(table, expected_output)

    def test_read_table_with_empty_row(self):
        """
        Test for proper loading of a table that includes an empty row.

        """
        # Sheet to read
        sheetname = "Instruments (empty row)"
        # Column to use as index labels
        index_col = "ID"

        # Expected output
        expected_output_list = []
        row = {}
        row['Description'] = 'Moake\'s Flow Cytometer'
        row['Forward Scatter Channel'] = 'FSC-H'
        row['Side Scatter Channel'] = 'SSC-H'
        row['Fluorescence Channels'] = 'FL1-H, FL2-H, FL3-H'
        row['Time Channel'] = 'Time'
        expected_output_list.append(row)
        row = {}
        row['Description'] = 'Moake\'s Flow Cytometer (new acquisition card)'
        row['Forward Scatter Channel'] = 'FSC'
        row['Side Scatter Channel'] = 'SSC'
        row['Fluorescence Channels'] = 'FL1, FL2, FL3'
        row['Time Channel'] = 'TIME'
        expected_output_list.append(row)
        row = {}
        row['Description'] = 'Some other flow cytometer'
        row['Forward Scatter Channel'] = 'FSC-A'
        row['Side Scatter Channel'] = 'SSC-A'
        row['Fluorescence Channels'] = 'FL1-A, FL2-A, FL3-A'
        row['Time Channel'] = 'Time'
        expected_output_list.append(row)
        expected_index = pd.Series(['FC001', 'FC002', 'FC003'], name='ID')
        expected_columns = ['Description',
                            'Forward Scatter Channel',
                            'Side Scatter Channel',
                            'Fluorescence Channels',
                            'Time Channel']

        expected_output = pd.DataFrame(expected_output_list,
                                       index=expected_index,
                                       columns=expected_columns)

        # Read table
        table = FlowCal.excel_ui.read_table(self.filename,
                                            sheetname=sheetname,
                                            index_col=index_col)

        # Compare
        tm.assert_frame_equal(table, expected_output)

    def test_read_table_duplicated_id_error(self):
        """
        Test for error when table contains duplicated index values.

        """
        # Sheet to read
        sheetname = "Instruments (duplicated)"
        # Column to use as index labels
        index_col = "ID"

        # Call function
        self.assertRaises(ValueError,
                          FlowCal.excel_ui.read_table,
                          self.filename,
                          sheetname,
                          index_col)

    def test_read_table_list_argument_error(self):
        """
        Test for error when `sheetname` is a list.

        """
        # Sheet to read
        sheetname = ["Instruments", "Instruments (duplicated)"]
        # Column to use as index labels
        index_col = "ID"

        # Call function
        self.assertRaises(TypeError,
                          FlowCal.excel_ui.read_table,
                          self.filename,
                          sheetname,
                          index_col)

    def test_read_table_none_argument_error(self):
        """
        Test for error when `sheetname` is None.

        """
        # Sheet to read
        sheetname = None
        # Column to use as index labels
        index_col = "ID"

        # Call function
        self.assertRaises(TypeError,
                          FlowCal.excel_ui.read_table,
                          self.filename,
                          sheetname,
                          index_col)

if __name__ == '__main__':
    unittest.main()
