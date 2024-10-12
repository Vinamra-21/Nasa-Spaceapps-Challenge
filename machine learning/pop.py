import pandas as pd

# Read the CSV file
df = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_31753.csv', skiprows=4)
df.to_csv('POPULATION.csv')