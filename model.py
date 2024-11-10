from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
prices_df = pd.read_csv('prices_testing.csv')
interest_df = pd.read_csv('interest.csv')
inflation_df = pd.read_csv('inflation.csv')

# Ensure Date column is in datetime format and set as index

# Ensure 'Date' is in datetime format and set as index
prices_df['Date'] = pd.to_datetime(prices_df['Date'])
prices_df.set_index('Date', inplace=True)

# Replace 'NaN' or 'inf' in the relevant columns
prices_df['Detached_Average_Price'] = pd.to_numeric(prices_df['Detached_Average_Price'], errors='coerce') # replace house type here
prices_df['Inflation'] = pd.to_numeric(prices_df['Inflation'], errors='coerce')
prices_df['Interest'] = pd.to_numeric(prices_df['Interest'], errors='coerce')

# Replace inf with NaN and then handle NaN
prices_df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Drop rows with NaN in relevant columns
prices_df.dropna(subset=['Detached_Average_Price', 'Inflation', 'Interest'], inplace=True)

# Split the data into training and testing sets
train_df, test_df = train_test_split(prices_df, test_size=0.2, shuffle=False)
# Check for inf values
print(np.isinf(train_df[['Detached_Average_Price', 'Inflation', 'Interest']]).sum())
input('<<')
# Initialize the SARIMAX model
model = SARIMAX(
    endog=train_df['Detached_Average_Price'],
    exog=train_df[['Inflation', 'Interest']],
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12)
)
results = model.fit()

# Forecast on the test set
forecast = results.forecast(steps=len(test_df), exog=test_df[['Inflation', 'Interest']])

# Evaluate the performance
mae = mean_absolute_error(test_df['Detached_Average_Price'], forecast)
rmse = np.sqrt(mean_squared_error(test_df['Detached_Average_Price'], forecast))

print("Mean Absolute Error (MAE):", mae)
print("Root Mean Squared Error (RMSE):", rmse)

# Plot the actual vs. predicted values
plt.figure(figsize=(14, 7))
plt.plot(test_df.index, test_df['Detached_Average_Price'], label='Actual Prices', color='blue')
plt.plot(test_df.index, forecast, label='Predicted Prices', color='red')
plt.title('Actual vs. Predicted Prices')
plt.xlabel('Date')
plt.ylabel('Average Price')
plt.legend()
plt.show()
