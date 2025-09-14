import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Read csv file downloaded from kaggle
df = pd.read_csv('gold_data_2015_25.csv')
# Display first few rows to understand the data structure
print(df.head())
# Display info about column types and non-null counts
print(df.info())
# Display descriptive statistics for numeric columns
print(df.describe())
# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])
print(df.info())
# Set 'Date' column as the index for time series analysis
print(df.loc[df['Date'].dt.year == 2025])
print(df.groupby(df['Date'].dt.year)[['SPX','GLD']].mean())
print(df.groupby(df['Date'].dt.year)[['SPX','GLD']].count())
df = df.set_index('Date')
print(df.head())
# Compute and print correlation matrix between variables
print(df.corr())
print(sns.heatmap(df.corr(), cmap="coolwarm"))
print(df['SPX'].plot())
from sklearn.linear_model import LinearRegression
#Looking into the regression of the data
lr=LinearRegression()
# Define target variable (y) and features (x)
y = df['SPX']
x = df[['GLD', 'SLV']]
# Train the regression model
lr.fit(x,y)
# Predict SPX values using trained model
predict = lr.predict(x)
sns.lineplot(data=df,y='SPX',x=df.index)
# Plot predicted SPX values over time
sns.lineplot(y=predict,x=df.index)
from sklearn.metrics import mean_absolute_error,mean_absolute_percentage_error
# Evaluate model performance with error metrics
print(mean_absolute_error(y,predict))
print(mean_absolute_percentage_error(y,predict))
