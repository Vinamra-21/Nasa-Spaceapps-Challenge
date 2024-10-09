import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('data_with_median.csv')

# Columns related to the different experiments (IS, LNLG, LNLGIS, LNLGOGIS)
experiments = ['IS', 'LNLG', 'LNLGIS', 'LNLGOGIS']

# Columns to apply the mean transformation on (ignoring uncertainties)
columns_to_mean = ['dC_loss (TgCO2)', 'NBE (TgCO2)', 'NCE (TgCO2)', 'FUR']

# Apply the mean across the 4 experiments for each set of columns
for col in columns_to_mean:
    # Create the column names for each experiment
    experiment_columns = [f'FUR {exp}' if col == 'FUR' else f'{exp} {col}' for exp in experiments]
    
    # Calculate the mean for these columns
    df[f'Mean {col}'] = df[experiment_columns].mean(axis=1)

# Keep the original columns that are not part of the experiment columns
final_columns = ['Alpha 3 Code', 'Year', 'Rivers (TgCO2)', 'River unc (TgCO2)', 
                 'Wood+Crop (TgCO2)', 'Wood+Crop unc (TgCO2)', 
                 'FF (TgCO2)', 'FF unc (TgCO2)', 'Z-statistic'] + \
                [f'Mean {col}' for col in columns_to_mean]

# Display the final dataframe with the original non-experiment columns and the new mean columns
print(df[final_columns])

df[final_columns].to_csv('output.csv', index=False)
