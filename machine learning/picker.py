import pandas as pd

# Update these paths to the actual locations of your CSV files
final_dataset_path = 'C:/Users/Lenovo/Desktop/SPACEAPPS/final_dataset.csv'  # Adjust the path accordingly
final_population_path = 'C:/Users/Lenovo/Desktop/SPACEAPPS/final_population.csv'  # Adjust the path accordingly

# Load the datasets
final_dataset = pd.read_csv(final_dataset_path)
final_population = pd.read_csv(final_population_path)

# Print the columns in final_dataset
print(final_dataset.columns)  # Debugging step to see actual column names

# Transpose the final_population DataFrame
transposed_population = final_population.set_index('Country Code').T

# Merge the transposed population data with the final_dataset using 'isoa2'
final_dataset = final_dataset.merge(transposed_population, left_on='isoa2', right_index=True, how='left')

# Save the updated final_dataset
final_dataset.to_csv('C:/Users/Lenovo/Desktop/SPACEAPPS/updated_final_dataset.csv', index=False)  # Adjust the output path as needed
