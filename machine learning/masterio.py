import pandas as pd
import numpy as np

# Load the datasets
df_emissions = pd.read_csv('DATA.csv')
df_population = pd.read_csv('POPULATION.csv')

# Melt the emissions dataframe to convert years to a single column
year_columns = [col for col in df_emissions.columns if col.startswith('Y_')]
df_emissions_melted = df_emissions.melt(
    id_vars=['Country_code_A3', 'Name', 'ipcc_code_2006_for_standard_report_name'],
    value_vars=year_columns,
    var_name='Year',
    value_name='Emission'
)

# Clean up the Year column
df_emissions_melted['Year'] = df_emissions_melted['Year'].str.replace('Y_', '').astype(int)

# Rename columns for clarity
df_emissions_melted = df_emissions_melted.rename(columns={
    'Name': 'Country',
    'ipcc_code_2006_for_standard_report_name': 'Emission_Type'
})

# Melt the population dataframe
df_population_melted = df_population.melt(
    id_vars=['Country Code', 'Country Name'],
    value_vars=[str(year) for year in range(1960, 2024)],
    var_name='Year',
    value_name='Population'
)

# Clean up the Year column and rename columns
df_population_melted['Year'] = df_population_melted['Year'].astype(int)
df_population_melted = df_population_melted.rename(columns={
    'Country Code': 'Country_code_A3',
    'Country Name': 'Country'
})

# Merge the reshaped dataframes
merged_df = pd.merge(
    df_emissions_melted,
    df_population_melted[['Country_code_A3', 'Year', 'Population']],
    on=['Country_code_A3', 'Year'],
    how='left'
)

# Set the index
merged_df.set_index(['Year', 'Country', 'Emission_Type'], inplace=True)

# Sort the index
merged_df.sort_index(inplace=True)

# Display the first few rows of the merged dataset
print(merged_df.head(10))

# Display info about the merged dataset
print(merged_df.info())
merged_df.to_csv('need_imperfect_data.csv')