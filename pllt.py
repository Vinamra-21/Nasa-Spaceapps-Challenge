import pandas as pd

# Load the datasets
df1 = pd.read_csv('DATA.csv')  # CO2 emissions dataset
df2 = pd.read_csv('POPULATION.csv')  # Population dataset
df3=pd.read_csv('imperfect-data.csv')


print(df1)
print(df2)
print(df3)