import pytest
from pkg_resources import resource_filename

import pytest
import pandas as pd
import pandas.util.testing as pdtest

from swmmreport import ReportFile


def data_path(filename):
    path = resource_filename("swmmreport.tests._data", filename)
    return path

class base_ReportFileMixin(object):
    known_surcharge_columns = ['Type', 'Hours',
        'Max_Above_Crown_Feet', 'Min_Below_Rim_Feet'
    ]
    known_depth_columns = ['Type', 'Avg_Depth_Feet', 'Max_Depth_Feet',
        'Max_HGL_Feet', 'Day_of_max', 'Time_of_max', 'Reported_Max'
    ]
    def teardown(self):
        None

    def test_attributes(self):
        assert hasattr(self.rpt, 'path')
        assert isinstance(self.rpt.path, str)

        assert hasattr(self.rpt, 'orig_file')
        assert isinstance(self.rpt.orig_file, list)

        assert hasattr(self.rpt, 'surcharge_results')
        assert isinstance(self.rpt.surcharge_results, pd.DataFrame)
        for col in self.known_surcharge_columns:
            assert col in self.rpt.surcharge_results.columns.tolist()

        assert hasattr(self.rpt, 'depth_results')
        assert isinstance(self.rpt.depth_results, pd.DataFrame)
        for col in self.known_depth_columns:
            assert col in self.rpt.depth_results.columns.tolist()


class Test_ReportFile(base_ReportFileMixin):
    def setup(self):
        self.known_path = data_path('test_rpt.rpt')
        self.surcharge_file = data_path('test_surcharge_data.csv')
        self.depth_file = data_path('test_depth_data.csv')

        self.known_surcharge_results = pd.read_csv(
            self.surcharge_file, index_col=[0])

        self.known_depth_results = pd.read_csv(
            self.depth_file, index_col=[0])

        self.rpt = ReportFile(self.known_path)


    def test_depth_results(self):
        pdtest.assert_frame_equal(self.rpt.depth_results, self.known_depth_results)

    def test_surcharge_results(self):
        pdtest.assert_frame_equal(self.rpt.surcharge_results, self.known_surcharge_results)
