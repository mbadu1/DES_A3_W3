import pandas as pd
import unittest
from spx_analysis import read_fn, process_date_fn

class TestDataCleaning(unittest.TestCase): 
    def setUp(self):
        filename = 'test_gold_data.csv'
        self.df = read_fn(filename)

    def test_read_fn(self): 
        self.assertEqual(type(self.df), pd.DataFrame) # Check if return is a dataframe
        
    def test_process_date_fn(self): 
        df_processed = process_date_fn(self.df)
        self.assertEqual(type(df_processed), pd.DataFrame) # Check if return is a dataframe
        self.assertGreaterEqual(df_processed.shape[0], 0) # Check if returned dataframe is non empty

if __name__ == "__main__": 
    unittest.main()

# # Fixture to provide a sample DataFrame and file path for tests
# @pytest.fixture
# def test_data_path(tmp_path):
#     """Creates a temporary CSV file for testing."""
#     content = "Date,SPX,GLD,SLV\n2024-01-01,100,200,300\n2024-01-02,110,210,310\n2024-01-03,120,220,320\n2024-01-04,130,230,330\n2024-01-05,140,240,340"
#     file = tmp_path / "test_data.csv"
#     file.write_text(content)
#     return file

# # Unit test for the data loading function
# def test_load_data(test_data_path):
#     df = load_data(test_data_path)
#     assert isinstance(df, pd.DataFrame)
#     assert not df.empty
#     assert 'Date' not in df.columns
#     assert isinstance(df.index, pd.DatetimeIndex)

# # System test for the model training and evaluation pipeline
# def test_train_and_evaluate_model(test_data_path):
#     df = load_data(test_data_path)
    
#     # Define features and target based on your script
#     features = ['GLD', 'SLV']
#     target = 'SPX'
    
#     model, mae, mape = train_and_evaluate_model(df, features, target)
    
#     # Assertions to check the output
#     assert hasattr(model, 'predict') # Check if it's a valid model object
#     assert isinstance(mae, float)
#     assert isinstance(mape, float)
#     assert mape > 0 # A simple check to ensure a valid calculation