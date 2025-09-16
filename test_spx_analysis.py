import pandas as pd
import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from spx_analysis import read_fn, process_date_fn

class TestDataCleaning(unittest.TestCase): 
    def setUp(self):
        # Create a temporary test CSV file
        self.test_data = {
            'Date': ['2020-01-01', '2020-01-02', '2020-01-03', '2021-01-01', '2025-01-01'],
            'SPX': [3200.0, 3250.5, 3180.2, 3756.1, 4800.0],
            'GLD': [150.5, 152.1, 149.8, 178.2, 190.5],
            'SLV': [18.2, 18.5, 17.9, 25.1, 22.8]
        }
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        test_df = pd.DataFrame(self.test_data)
        test_df.to_csv(self.temp_file.name, index=False)
        self.temp_file.close()
        
        self.df = read_fn(self.temp_file.name)

    def tearDown(self):
        # Clean up temporary file
        os.unlink(self.temp_file.name)

    # Existing tests
    def test_read_fn(self): 
        self.assertEqual(type(self.df), pd.DataFrame)
        
    def test_process_date_fn(self): 
        df_processed = process_date_fn(self.df.copy())
        self.assertEqual(type(df_processed), pd.DataFrame)
        self.assertGreaterEqual(df_processed.shape[0], 0)

    # Additional comprehensive test cases
    
    def test_read_fn_columns_exist(self):
        """Test that required columns exist in the loaded data"""
        expected_columns = ['Date', 'SPX', 'GLD', 'SLV']
        for col in expected_columns:
            self.assertIn(col, self.df.columns, f"Column '{col}' missing from DataFrame")

    def test_read_fn_data_types(self):
        """Test that data types are as expected after reading"""
        self.assertTrue(pd.api.types.is_object_dtype(self.df['Date']), "Date should be object type initially")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['SPX']), "SPX should be numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['GLD']), "GLD should be numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df['SLV']), "SLV should be numeric")

    def test_read_fn_file_not_found(self):
        """Test handling of non-existent file"""
        with self.assertRaises(FileNotFoundError):
            read_fn('non_existent_file.csv')

    def test_process_date_fn_datetime_conversion(self):
        """Test that Date column is properly converted to datetime and set as index"""
        df_processed = process_date_fn(self.df.copy())
        
        # Check that Date is now the index and is datetime type
        self.assertIsInstance(df_processed.index, pd.DatetimeIndex, "Index should be DatetimeIndex")
        self.assertNotIn('Date', df_processed.columns, "Date column should be removed after setting as index")

    def test_process_date_fn_preserves_data(self):
        """Test that processing preserves original data values"""
        original_spx_sum = self.df['SPX'].sum()
        df_processed = process_date_fn(self.df.copy())
        processed_spx_sum = df_processed['SPX'].sum()
        
        self.assertAlmostEqual(original_spx_sum, processed_spx_sum, places=2, 
                              msg="SPX values should be preserved during processing")

    def test_process_date_fn_handles_invalid_dates(self):
        """Test handling of invalid date formats"""
        invalid_data = self.df.copy()
        invalid_data.loc[0, 'Date'] = 'invalid-date'
        
        # This should either raise an error or handle gracefully
        # Depending on your requirements, adjust this test
        with self.assertRaises((ValueError, pd.errors.ParserError)):
            process_date_fn(invalid_data)

    def test_dataframe_not_empty(self):
        """Test that the loaded DataFrame is not empty"""
        self.assertGreater(len(self.df), 0, "DataFrame should not be empty")
        self.assertGreater(self.df.shape[1], 0, "DataFrame should have columns")

    def test_no_all_null_columns(self):
        """Test that no columns are entirely null"""
        for column in self.df.columns:
            self.assertFalse(self.df[column].isnull().all(), f"Column '{column}' should not be entirely null")

    def test_numeric_columns_have_valid_ranges(self):
        """Test that numeric columns have reasonable value ranges"""
        df_processed = process_date_fn(self.df.copy())
        
        # SPX should be positive and within reasonable range
        self.assertTrue((df_processed['SPX'] > 0).all(), "SPX values should be positive")
        self.assertTrue((df_processed['SPX'] < 10000).all(), "SPX values should be reasonable (< 10000)")
        
        # GLD should be positive
        self.assertTrue((df_processed['GLD'] > 0).all(), "GLD values should be positive")
        
        # SLV should be positive
        self.assertTrue((df_processed['SLV'] > 0).all(), "SLV values should be positive")

    def test_date_range_validity(self):
        """Test that dates fall within expected range"""
        df_processed = process_date_fn(self.df.copy())
        
        min_date = df_processed.index.min()
        max_date = df_processed.index.max()
        
        # Assuming data should be between 2015 and 2025 based on filename
        self.assertGreaterEqual(min_date.year, 2015, "Minimum date should be 2015 or later")
        self.assertLessEqual(max_date.year, 2025, "Maximum date should be 2025 or earlier")

    def test_correlation_calculation(self):
        """Test that correlation matrix can be calculated"""
        df_processed = process_date_fn(self.df.copy())
        
        # Should be able to calculate correlation without errors
        corr_matrix = df_processed.corr()
        
        self.assertIsInstance(corr_matrix, pd.DataFrame, "Correlation should return DataFrame")
        self.assertEqual(corr_matrix.shape[0], corr_matrix.shape[1], "Correlation matrix should be square")
        
        # Diagonal should be 1.0
        for i in range(len(corr_matrix)):
            self.assertAlmostEqual(corr_matrix.iloc[i, i], 1.0, places=2, 
                                 msg="Diagonal elements should be 1.0")

    def test_data_continuity(self):
        """Test for reasonable data continuity (no extreme jumps)"""
        df_processed = process_date_fn(self.df.copy())
        df_sorted = df_processed.sort_index()
        
        # Calculate percentage changes
        spx_pct_change = df_sorted['SPX'].pct_change().dropna()
        
        # Check that no single day change is more than 50% (reasonable for most cases)
        extreme_changes = spx_pct_change.abs() > 0.5
        self.assertFalse(extreme_changes.any(), 
                        "SPX should not have extreme single-day changes (>50%)")

    def test_missing_data_handling(self):
        """Test behavior with missing data"""
        df_with_na = self.df.copy()
        df_with_na.loc[0, 'SPX'] = None
        
        df_processed = process_date_fn(df_with_na)
        
        # Check that the function handles NaN values appropriately
        self.assertIsInstance(df_processed, pd.DataFrame, "Should return DataFrame even with NaN values")

    def test_duplicate_dates_handling(self):
        """Test handling of duplicate dates"""
        df_with_duplicates = self.df.copy()
        df_with_duplicates = pd.concat([df_with_duplicates, df_with_duplicates.iloc[:1]], ignore_index=True)
        
        # This test depends on how you want to handle duplicates
        # You might want to modify process_date_fn to handle this case
        try:
            df_processed = process_date_fn(df_with_duplicates)
            # If it succeeds, check that duplicates are handled somehow
            self.assertIsInstance(df_processed, pd.DataFrame)
        except ValueError:
            # If it raises an error, that's also acceptable behavior
            pass

    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrame"""
        empty_df = pd.DataFrame(columns=['Date', 'SPX', 'GLD', 'SLV'])
        
        # Save empty DataFrame to temp file
        empty_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        empty_df.to_csv(empty_temp.name, index=False)
        empty_temp.close()
        
        try:
            empty_loaded = read_fn(empty_temp.name)
            # Depending on your requirements, this might raise an error or return empty DF
            self.assertEqual(len(empty_loaded), 0, "Empty file should result in empty DataFrame")
        finally:
            os.unlink(empty_temp.name)


class TestDataAnalysis(unittest.TestCase):
    """Additional tests for analysis functions that could be extracted from main script"""
    
    def setUp(self):
        # Create sample data for analysis tests
        dates = pd.date_range('2020-01-01', periods=100, freq='D')
        self.sample_df = pd.DataFrame({
            'SPX': range(3000, 3100),
            'GLD': range(150, 250),
            'SLV': range(20, 120)
        }, index=dates)

    def test_correlation_matrix_properties(self):
        """Test properties of correlation matrix"""
        corr = self.sample_df.corr()
        
        # Should be symmetric
        pd.testing.assert_frame_equal(corr, corr.T, check_names=False)
        
        # All values should be between -1 and 1
        self.assertTrue((corr.values >= -1).all() and (corr.values <= 1).all())

    def test_descriptive_statistics(self):
        """Test that descriptive statistics are reasonable"""
        desc_stats = self.sample_df.describe()
        
        # Should have standard statistical measures
        expected_stats = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
        for stat in expected_stats:
            self.assertIn(stat, desc_stats.index)
        
        # Count should equal dataframe length
        for col in self.sample_df.columns:
            self.assertEqual(desc_stats.loc['count', col], len(self.sample_df))


if __name__ == "__main__": 
    unittest.main(verbosity=2)