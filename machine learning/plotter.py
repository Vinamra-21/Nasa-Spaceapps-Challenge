import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Load dataset
url = 'https://ceos.org/gst/files/pilot_topdown_CO2_Budget_countries_v1.csv'
df_all = pd.read_csv(url, skiprows=52)

# List all available countries
countries = df_all['Alpha 3 Code'].unique()
print(f"Number of countries with data available: {len(countries)}")
print("List of available countries:")
for i, country in enumerate(countries, 1):
    print(f"{i}. {country}")

# Choose country
country_choice = int(input("Enter the number corresponding to the country you want to choose: "))
chosen_country = countries[country_choice - 1]
print(f"You have selected: {chosen_country}")

# Choose experiment
experiment = input("Choose an experiment from ['IS', 'LNLG', 'LNLGIS', 'LNLGOGIS']: ")

# Subset of columns for the chosen experiment
if experiment == 'IS':
    df = df_all.drop(df_all.columns[[4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 34, 35, 36]], axis=1)
elif experiment == 'LNLG':
    df = df_all.drop(df_all.columns[[2, 3, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 33, 35, 36]], axis=1)
elif experiment == 'LNLGIS':
    df = df_all.drop(df_all.columns[[2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 24, 25, 33, 34, 36]], axis=1)
elif experiment == 'LNLGOGIS':
    df = df_all.drop(df_all.columns[[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 33, 34, 35]], axis=1)

# Filter data for the chosen country
country_data = df[df['Alpha 3 Code'] == chosen_country]

# Ask the user for a specific year or 'mean'
year_choice = input("Enter a specific year (or type 'mean' for the average): ")

if year_choice.lower() == 'mean':
    # Calculate the mean values over all available years
    country_data_mean = country_data.mean(numeric_only=True)
else:
    # Filter data for the chosen year
    year_choice = int(year_choice)
    country_data_mean = country_data[country_data['Year'] == year_choice]

# Plot 2: CO2 fluxes comparison for the specific year or mean
plt.bar(1, country_data_mean['FF (TgCO2)'], yerr=country_data_mean['FF unc (TgCO2)'], label='FF', alpha=0.5)
plt.bar(2, country_data_mean['Rivers (TgCO2)'], yerr=country_data_mean['River unc (TgCO2)'], label='Rivers', alpha=0.5)
plt.bar(3, country_data_mean['Wood+Crop (TgCO2)'], yerr=abs(country_data_mean['Wood+Crop unc (TgCO2)']), label='WoodCrop', alpha=0.5)
plt.bar(4, country_data_mean[experiment + ' dC_loss (TgCO2)'], yerr=country_data_mean[experiment + ' dC_loss unc (TgCO2)'], label='dC', alpha=0.5)
plt.bar(6, country_data_mean[experiment + ' NCE (TgCO2)'], yerr=country_data_mean[experiment + ' NCE unc (TgCO2)'], label='NCE', alpha=0.5)

ax = plt.gca()
ymin, ymax = ax.get_ylim()
plt.plot([5, 5], [ymin, ymax], 'k:')
xmin, xmax = ax.get_xlim()
plt.plot([xmin, xmax], [0, 0], 'k', linewidth=0.5)
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])

plt.xticks([1, 2, 3, 4, 6], ['Fossil\nFuels', 'Rivers', 'Wood+\nCrops', '$\mathrm{\Delta C _{loss}}$', 'NCE'])
plt.title(f"{chosen_country} {year_choice if year_choice != 'mean' else 'Mean'}")
plt.ylabel('CO$_2$ Flux (TgCO$_2$ year$^{-1}$)')
plt.show()
