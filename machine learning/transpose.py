import pandas as pd

# Update the path to your final population dataset
final_population_path = 'C:/Users/Lenovo/Desktop/SPACEAPPS/final_population.csv'  # Adjust the path accordingly
output_transposed_path = 'C:/Users/Lenovo/Desktop/SPACEAPPS/transposed_final_population.csv'  # Adjust output path as needed

# Load the final population dataset
final_population = pd.read_csv(final_population_path)

# Print the columns in final_population for debugging
print(final_population.columns)

# Transpose the DataFrame
transposed_population = final_population.set_index('Country Code').T  # Adjust the index if necessary

# Save the transposed DataFrame to a new CSV file
transposed_population.to_csv(output_transposed_path)

print(f'Transposed population data saved to {output_transposed_path}')
