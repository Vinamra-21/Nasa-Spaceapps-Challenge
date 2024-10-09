import pandas as pd

# Load the data
url = 'https://ceos.org/gst/files/pilot_topdown_CO2_Budget_countries_v1.csv'
df_all = pd.read_csv(url, skiprows=52)

# Replace missing values with the median of each column
df_all = df_all.apply(lambda col: col.fillna(col.median()) if col.dtype != 'O' else col)

# Save the updated data to a new CSV file
df_all.to_csv('data_with_median.csv', index=False)

print("Missing values replaced with medians and saved to 'data_with_median.csv'")
