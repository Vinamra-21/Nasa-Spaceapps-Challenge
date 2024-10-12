import pandas as pd

# Load the data
url = 'https://ceos.org/gst/files/pilot_topdown_CO2_Budget_countries_v1.csv'
df_all = pd.read_csv(url, skiprows=52)

# Define the experiment options and corresponding columns to drop
experiment_options = {
    'IS': [4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 34, 35, 36],
    'LNLG': [2, 3, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 33, 35, 36],
    'LNLGIS': [2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 24, 25, 33, 34, 36],
    'LNLGOGIS': [2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 33, 34, 35]
}

# Get the unique years and country codes from the dataset
years = df_all['Year'].unique()
country_codes = df_all['Alpha 3 Code'].unique()

# Initialize an empty DataFrame to store the results
all_combinations_data = pd.DataFrame()

# Loop through all combinations of country codes, years, and experiments
for country_code in country_codes:
    for year in years:
        for experiment, drop_columns in experiment_options.items():
            # Filter the dataframe for the current country and year
            country_data = df_all[df_all['Alpha 3 Code'] == country_code]
            country_data_year = country_data[country_data['Year'] == year]
            
            if country_data_year.empty:
                continue
            
            # Drop irrelevant columns based on the current experiment
            df_experiment = country_data_year.drop(df_all.columns[drop_columns], axis=1)
            
            # Add experiment type as a column
            df_experiment['Experiment'] = experiment

            # Append to the final DataFrame
            all_combinations_data = pd.concat([all_combinations_data, df_experiment])

# Reset the index for the final DataFrame
all_combinations_data.reset_index(drop=True, inplace=True)

# Save the combined data to a CSV file
all_combinations_data.to_csv('all_country_experiment_data.csv', index=False)

print("Data for all combinations saved to 'all_country_experiment_data.csv'")
