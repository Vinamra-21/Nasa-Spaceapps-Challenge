import pandas as pd

# Load the dataset
df = pd.read_csv('merged_land_use_emission_data.csv')

# Select numeric columns excluding 'year'
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.drop('year', errors='ignore')

# Calculate mean and standard deviation for the numeric columns
means = df[numeric_cols].mean()
std_devs = df[numeric_cols].std()

# Create a formatted string with "column - value"
stats_str = "Mean Values:\n"
for col in numeric_cols:
    stats_str += f"{col} - {means[col]:.4f}\n"  # Mean values with 4 decimal places

stats_str += "\nStandard Deviation Values:\n"
for col in numeric_cols:
    stats_str += f"{col} - {std_devs[col]:.4f}\n"  # Std deviation values with 4 decimal places

# Write the statistics to a text file
with open('numeric_stats.txt', 'w') as f:
    f.write(stats_str)

print("Means and standard deviations have been saved to 'numeric_stats.txt'.")
