import pandas as pd
import seaborn as sns


def read_fn(filename: str):
    # Read csv file downloaded from kaggle
    df = pd.read_csv(filename)
    return df


def process_date_fn(df: pd.DataFrame) -> pd.DataFrame:
    # Convert the 'Date' column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])
    df.info()
    # Set 'Date' column as the index for time series analysis
    df.loc[df["Date"].dt.year == 2025]
    df.groupby(df["Date"].dt.year)[["SPX", "GLD"]].mean()
    df.groupby(df["Date"].dt.year)[["SPX", "GLD"]].count()
    df = df.set_index("Date")

    return df


filename = "gold_data_2015_25.csv"
df = read_fn(filename)
df = process_date_fn(df)


# Display first few rows to understand the data structure
df.head()
# Display info about column types and non-null counts
df.info()
# Display descriptive statistics for numeric columns
df.describe()

# Compute and print correlation matrix between variables
df.corr()
sns.heatmap(df.corr(), cmap="coolwarm")
df["SPX"].plot()
