import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from src.io_tools import clean_data_strip, clean_data_lower

class TestIOTools(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({'col1': ['  stripwhitespace '], 
            'col2': ['MakeThisLowerCase'], 
            'col3': ['test_trial_description'],
            'col4': [1]})
        self.stripped_df = pd.DataFrame({'col1': ['stripwhitespace'], 
            'col2': ['MakeThisLowerCase'], 
            'col3': ['test_trial_description'],
            'col4': [1]})
        self.lowered_df = pd.DataFrame({'col1': ['  stripwhitespace '], 
            'col2': ['makethislowercase'], 
            'col3': ['test_trial_description'],
            'col4': [1]})
    
    def test_clean_data_strip(self):
        cleaned = clean_data_strip(self.df)
        assert_frame_equal(cleaned, self.stripped_df)
    
    def test_clean_data_lower(self):
        cleaned = clean_data_lower(self.df)
        assert_frame_equal(cleaned, self.lowered_df)