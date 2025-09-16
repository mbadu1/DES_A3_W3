# DES_A3_W3
# Gold Data 2015
# SPX Financial Data Analysis

A Python-based financial analysis tool for analyzing S&P 500 (SPX) performance in correlation with precious metals (Gold and Silver) from 2015-2025.

##  Overview

This project provides tools to analyze the relationship between the S&P 500 index and precious metals prices, offering insights into market correlations and trends over a 10-year period.

##  Features

- **Data Loading & Processing**: Automated CSV data ingestion with date parsing
- **Time Series Analysis**: Date-indexed data processing for temporal analysis
- **Correlation Analysis**: Statistical correlation between SPX, Gold (GLD), and Silver (SLV)
- **Data Visualization**: Heatmaps and time series plots using Seaborn and Matplotlib
- **Robust Testing**: Comprehensive test suite covering edge cases and data validation

## 📁 Project Structure

```
spx-analysis/
│
├── spx_analysis.py          # Main analysis script
├── test_spx_analysis.py     # Comprehensive test suite
├── gold_data_2015_25.csv    # Main dataset (2015-2025)
├── test_gold_data.csv       # Test dataset for unit tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

##  Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/spx-analysis.git
   cd spx-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download dataset**
   - Place your `gold_data_2015_25.csv` file in the project root
   - Ensure the CSV contains columns: `Date`, `SPX`, `GLD`, `SLV`

## 📊 Data Format

Your CSV file should have the following structure:

| Date       | SPX    | GLD   | SLV  |
|------------|--------|-------|------|
| 2015-01-01 | 2058.2 | 117.8 | 15.7 |
| 2015-01-02 | 2049.2 | 118.1 | 15.9 |
| ...        | ...    | ...   | ...  |

- **Date**: Date in YYYY-MM-DD format
- **SPX**: S&P 500 index value
- **GLD**: SPDR Gold Trust ETF price
- **SLV**: iShares Silver Trust ETF price

## 🔧 Usage

### Basic Analysis

```python
from spx_analysis import read_fn, process_date_fn

# Load and process data
df = read_fn('gold_data_2015_25.csv')
df_processed = process_date_fn(df)

# View basic statistics
print(df_processed.describe())

# Calculate correlations
correlations = df_processed.corr()
print(correlations)
```

### Running the Complete Analysis

```bash
python spx_analysis.py
```

This will generate:
- Descriptive statistics
- Correlation matrix
- Correlation heatmap visualization
- SPX time series plot

### Advanced Features (Commented Out)

The script includes optional machine learning analysis:
- Linear regression modeling
- SPX prediction based on precious metals prices
- Model evaluation metrics (MAE, MAPE)

To enable these features, uncomment the relevant sections in `spx_analysis.py`.

## 🧪 Testing

Run the comprehensive test suite:

```bash
python -m unittest test_spx_analysis.py -v
```

### Test Coverage

The test suite includes:

- **Data Loading Tests**
  - File reading validation
  - Column existence verification
  - Data type validation
  - Error handling for missing files

- **Data Processing Tests**
  - Date conversion accuracy
  - Index setting validation
  - Data integrity preservation
  - Invalid date handling

- **Data Quality Tests**
  - Value range validation
  - Missing data detection
  - Duplicate handling
  - Data continuity checks

- **Analysis Tests**
  - Correlation matrix properties
  - Statistical computation accuracy
  - Edge case handling

## 📈 Sample Outputs

### Correlation Matrix
```
        SPX       GLD       SLV
SPX    1.000000  0.234567  0.123456
GLD    0.234567  1.000000  0.789012
SLV    0.123456  0.789012  1.000000
```

### Key Insights
- Correlation between SPX and Gold: Moderate positive correlation
- Gold-Silver correlation: Strong positive correlation
- Time series trends reveal market behavior during major events

## 🔍 Key Functions

### `read_fn(filename: str) -> pd.DataFrame`
Loads CSV data from the specified file path.

### `process_date_fn(df: pd.DataFrame) -> pd.DataFrame`
Processes the DataFrame by:
- Converting Date column to datetime format
- Setting Date as index for time series analysis
- Performing basic data exploration

## 📊 Visualization Features

- **Correlation Heatmap**: Visual representation of asset correlations
- **Time Series Plots**: SPX performance over time
- **Statistical Summaries**: Descriptive statistics for all assets

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Add tests for new functionality
4. Ensure all tests pass (`python -m unittest`)
5. Commit changes (`git commit -am 'Add new feature'`)
6. Push to branch (`git push origin feature/new-feature`)
7. Create Pull Request

## 📋 Requirements

```txt
pandas>=1.3.0
seaborn>=0.11.0
matplotlib>=3.3.0
numpy>=1.20.0
scikit-learn>=1.0.0  # Optional, for ML features
```

##  Known Issues

- Large datasets may require increased memory allocation
- Date parsing assumes YYYY-MM-DD format
- Missing data points are not automatically interpolated

## Future Enhancements

- [ ] Add support for multiple date formats
- [ ] Implement data interpolation for missing values
- [ ] Add more sophisticated ML models
- [ ] Create interactive dashboard with Plotly
- [ ] Add support for additional financial indicators
- [ ] Implement automated data fetching from financial APIs

## Contact

- **Author**: Michael Badu
- **Email**: michael.badu@duke.edu
- **GitHub**: [@mbadu1](https://github.com/mbadu1)

## Disclosure
This project was developed with partial assistance from ChatGPT an AI language model by OpenAI.
ChatGPT was helpful for test scenerio's generation and this readme file