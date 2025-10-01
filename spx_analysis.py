import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error


def read_file_fn(filename: str):
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
jls_extract_var = read_file_fn
df = jls_extract_var(filename)
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
# Linear regression model

lr = LinearRegression()
y = df['SPX']
x = df[['GLD', 'SLV']]
lr.fit(x, y)

LinearRegression()

predict = lr.predict(x)

sns.lineplot(data=df, y='SPX', x=df.index)
sns.lineplot(y=predict, x=df.index)

mean_absolute_error(y, predict)
mean_absolute_percentage_error(y, predict)
# Rolling correlation between SPX and GLD
rolling_corr = df['SPX'].rolling(90).corr(df['GLD'])
# Rolling correlation (SPX vs GLD)
plt.figure(figsize=(10, 6))
plt.plot(df.index, rolling_corr, label='90-day Rolling Corr (SPX vs GLD)')
plt.axvline(pd.Timestamp('2020-03-01'),
            color='r', linestyle='--', label='COVID Crash')
plt.axvline(pd.Timestamp('2022-06-01'),
            color='g', linestyle='--', label='2022 Inflation Peak')
plt.legend()
plt.title("Time-varying SPX/GLD Correlation\n(Key macro events annotated)")
plt.show()
# Rolling correlation (SPX vs GLD)
window = 60
df["SPX_vol_z"] = (
    df["SPX"].pct_change().rolling(window).std()
    .transform(lambda x: (x - x.mean()) / x.std())
)
plt.figure(figsize=(10, 5))
plt.plot(df.index, df["SPX_vol_z"], label="SPX Volatility Z-Score")
plt.axhline(2, color="red", linestyle="--", label="High Vol regime")
plt.axhline(-2, color="blue", linestyle="--", label="Low Vol regime")
plt.legend()
plt.title("SPX Rolling Volatility Z-score (Regime Detection)")
plt.xlabel("Date")
plt.tight_layout()
plt.show()


def compute_drawdown(series):
    peak = series.cummax()
    dd = (series - peak) / peak
    return dd


dd_spx = compute_drawdown(df["SPX"])
dd_gld = compute_drawdown(df["GLD"])
dd_slv = compute_drawdown(df["SLV"])
# Rolling correlation (SPX vs GLD)
plt.figure(figsize=(12, 6))
plt.plot(df.index, dd_spx, label="SPX Drawdown", color="darkred")
plt.plot(df.index, dd_gld, label="Gold Drawdown", color="gold")
plt.plot(df.index, dd_slv, label="Silver Drawdown", color="silver")
plt.title("Maximum Drawdowns: SPX vs Gold & Silver (2015–2025)")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")
plt.legend()
plt.tight_layout()
plt.show()
