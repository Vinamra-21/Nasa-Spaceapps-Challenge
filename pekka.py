import pandas as pd

# Load the two datasets
df1 = pd.read_csv('data_with_median.csv')
df2 = pd.read_csv('cleaned-data-mean-replaced.csv')

# Preview the data to identify key columns
print(df1.head())  # Contains 'Alpha 3 Code', 'Year', etc.
print(df2.head())  # Contains 'countryCode', 'isoa2', 'year', etc.

# Perform the merge based on 'year' and country identifier
# Assuming 'Alpha 3 Code' in df1 corresponds to 'isoa2' in df2
merged_df = pd.merge(df1, df2, how='inner', left_on=['Alpha 3 Code', 'Year'], right_on=['isoa2', 'year'])

# Drop any unnecessary duplicate columns
merged_df = merged_df.drop(columns=['isoa2', 'year'])

# Display the merged dataframe
print(merged_df.head())

# Optional: Save the merged DataFrame to a CSV file
# merged_df.to_csv('merged_data.csv', index=False)
