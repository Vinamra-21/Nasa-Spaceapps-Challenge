import pandas as pd

def load_land_use_data(file_path):
    # Load land use data
    df = pd.read_csv(file_path)
    # Select relevant columns
    columns_to_keep = ['year', 'countryName', 'cropLand', 'grazingLand', 'forestLand', 
                       'fishingGround', 'builtupLand', 'carbon']
    df = df[columns_to_keep]
    return df

def load_emission_data(file_path):
    # Load emission data
    df = pd.read_csv(file_path)
    # Rename columns for consistency
    df = df.rename(columns={'Year': 'year', 'Country': 'countryName'})
    return df

def merge_datasets(land_use_df, emission_df):
    # Merge datasets on year and country name
    merged_df = pd.merge(land_use_df, emission_df, on=['year', 'countryName'], how='inner')
    
    # Pivot the emission data
    pivoted_df = merged_df.pivot_table(
        values='Emission', 
        index=['year', 'countryName', 'Population', 'cropLand', 'grazingLand', 
               'forestLand', 'fishingGround', 'builtupLand', 'carbon'],
        columns='Emission_Type', 
        aggfunc='first'
    ).reset_index()
    
    # Rename columns to remove spaces and special characters
    pivoted_df.columns = pivoted_df.columns.str.replace(' ', '').str.replace('-', '')
    
    return pivoted_df

def main():
    land_use_file = 'imperfect-data.csv'  # Replace with your actual file path
    emission_file = 'need_imperfect_data.csv'  # Replace with your actual file path
    
    land_use_df = load_land_use_data(land_use_file)
    emission_df = load_emission_data(emission_file)
    
    merged_df = merge_datasets(land_use_df, emission_df)
    
    # Save the merged dataset
    merged_df.to_csv('merged_land_use_emission_data.csv', index=False)
    
    print("Data merged successfully. Output saved to 'merged_land_use_emission_data.csv'")
    print(f"Shape of the merged dataset: {merged_df.shape}")
    print("\nFirst few rows of the merged dataset:")
    print(merged_df.head())
    
    # Print the column names
    print("\nColumns in the merged dataset:")
    print(merged_df.columns.tolist())

if __name__ == "__main__":
    main()
