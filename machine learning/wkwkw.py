import Levenshtein as lev

country_data = [
    ("AFG", "Afghanistan"),
    ("AGO", "Angola"),
    ("ALB", "Albania"),
    ("ARE", "United Arab Emirates"),
    ("ARG", "Argentina"),
    ("ARM", "Armenia"),
    ("ATG", "Antigua and Barbuda"),
    ("AUS", "Australia"),
    ("AUT", "Austria"),
    ("AZE", "Azerbaijan"),
    ("BDI", "Burundi"),
    ("BEL", "Belgium"),
    ("BEN", "Benin"),
    ("BFA", "Burkina Faso"),
    ("BGD", "Bangladesh"),
    ("BGR", "Bulgaria"),
    ("BHS", "Bahamas"),
    ("BIH", "Bosnia and Herzegovina"),
    ("BLR", "Belarus"),
    ("BLZ", "Belize"),
    ("BOL", "Bolivia"),
    ("BRA", "Brazil"),
    ("BRB", "Barbados"),
    ("BRN", "Brunei"),
    ("BTN", "Bhutan"),
    ("BWA", "Botswana"),
    ("CAF", "Central African Republic"),
    ("CAN", "Canada"),
    ("CHE", "Switzerland"),
    ("CHL", "Chile"),
    ("CHN", "China"),
    ("CIV", "Ivory Coast"),
    ("CMR", "Cameroon"),
    ("COD", "Democratic Republic of the Congo"),
    ("COG", "Republic of the Congo"),
    ("COK", "Cook Islands"),
    ("COL", "Colombia"),
    ("COM", "Comoros"),
    ("CPV", "Cape Verde"),
    ("CRI", "Costa Rica"),
    ("CUB", "Cuba"),
    ("CYP", "Cyprus"),
    ("CZE", "Czech Republic"),
    ("DEU", "Germany"),
    ("DJI", "Djibouti"),
    ("DMA", "Dominica"),
    ("DNK", "Denmark"),
    ("DOM", "Dominican Republic"),
    ("DZA", "Algeria"),
    ("ECU", "Ecuador"),
    ("EGY", "Egypt"),
    ("ERI", "Eritrea"),
    ("ESP", "Spain"),
    ("EST", "Estonia"),
    ("ETH", "Ethiopia"),
    ("FIN", "Finland"),
    ("FJI", "Fiji"),
    ("FRA", "France"),
    ("FSM", "Micronesia"),
    ("GAB", "Gabon"),
    ("GBR", "United Kingdom"),
    ("GEO", "Georgia"),
    ("GHA", "Ghana"),
    ("GIN", "Guinea"),
    ("GNB", "Guinea-Bissau"),
    ("GNQ", "Equatorial Guinea"),
    ("GRC", "Greece"),
    ("GRD", "Grenada"),
    ("GTM", "Guatemala"),
    ("GUY", "Guyana"),
    ("HND", "Honduras"),
    ("HRV", "Croatia"),
    ("HTI", "Haiti"),
    ("HUN", "Hungary"),
    ("IDN", "Indonesia"),
    ("IND", "India"),
    ("IRL", "Ireland"),
    ("IRN", "Iran"),
    ("IRQ", "Iraq"),
    ("ISL", "Iceland"),
    ("ISR", "Israel"),
    ("ITA", "Italy"),
    ("JAM", "Jamaica"),
    ("JOR", "Jordan"),
    ("JPN", "Japan"),
    ("KAZ", "Kazakhstan"),
    ("KEN", "Kenya"),
    ("KGZ", "Kyrgyzstan"),
    ("KHM", "Cambodia"),
    ("KIR", "Kiribati"),
    ("KNA", "Saint Kitts and Nevis"),
    ("KOR", "South Korea"),
    ("KWT", "Kuwait"),
    ("LAO", "Laos"),
    ("LBN", "Lebanon"),
    ("LBR", "Liberia"),
    ("LBY", "Libya"),
    ("LCA", "Saint Lucia"),
    ("LKA", "Sri Lanka"),
    ("LSO", "Lesotho"),
    ("LTU", "Lithuania"),
    ("LVA", "Latvia"),
    ("MAR", "Morocco"),
    ("MDA", "Moldova"),
    ("MDG", "Madagascar"),
    ("MDV", "Maldives"),
    ("MEX", "Mexico"),
    ("MHL", "Marshall Islands"),
    ("MKD", "North Macedonia"),
    ("MLI", "Mali"),
    ("MLT", "Malta"),
    ("MMR", "Myanmar"),
    ("MNE", "Montenegro"),
    ("MNG", "Mongolia"),
    ("MOZ", "Mozambique"),
    ("MRT", "Mauritania"),
    ("MUS", "Mauritius"),
    ("MWI", "Malawi"),
    ("MYS", "Malaysia"),
    ("NAM", "Namibia"),
    ("NER", "Niger"),
    ("NGA", "Nigeria"),
    ("NIC", "Nicaragua"),
    ("NIU", "Niue"),
    ("NLD", "Netherlands"),
    ("NOR", "Norway"),
    ("NPL", "Nepal"),
    ("NRU", "Nauru"),
    ("NZL", "New Zealand"),
    ("OMN", "Oman"),
    ("PAK", "Pakistan"),
    ("PAN", "Panama"),
    ("PER", "Peru"),
    ("PHL", "Philippines"),
    ("PLW", "Palau"),
    ("PNG", "Papua New Guinea"),
    ("POL", "Poland"),
    ("PRK", "North Korea"),
    ("PRT", "Portugal"),
    ("PRY", "Paraguay"),
    ("QAT", "Qatar"),
    ("ROU", "Romania"),
    ("RUS", "Russia"),
    ("RWA", "Rwanda"),
    ("SAU", "Saudi Arabia"),
    ("SDN", "Sudan"),
    ("SEN", "Senegal"),
    ("SLB", "Solomon Islands"),
    ("SLE", "Sierra Leone"),
    ("SLV", "El Salvador"),
    ("SOM", "Somalia"),
    ("SRB", "Serbia"),
    ("SSD", "South Sudan"),
    ("STP", "Sao Tome and Principe"),
    ("SUR", "Suriname"),
    ("SVK", "Slovakia"),
    ("SVN", "Slovenia"),
    ("SWE", "Sweden"),
    ("SWZ", "Eswatini"),
    ("SYC", "Seychelles"),
    ("SYR", "Syria"),
    ("TCD", "Chad"),
    ("TGO", "Togo"),
    ("THA", "Thailand"),
    ("TJK", "Tajikistan"),
    ("TKM", "Turkmenistan"),
    ("TLS", "Timor-Leste"),
    ("TON", "Tonga"),
    ("TTO", "Trinidad and Tobago"),
    ("TUN", "Tunisia"),
    ("TUR", "Turkey"),
    ("TUV", "Tuvalu"),
    ("TZA", "Tanzania"),
    ("UGA", "Uganda"),
    ("UKR", "Ukraine"),
    ("URY", "Uruguay"),
    ("USA", "United States"),
    ("UZB", "Uzbekistan"),
    ("VCT", "Saint Vincent and the Grenadines"),
    ("VEN", "Venezuela"),
    ("VNM", "Vietnam"),
    ("VUT", "Vanuatu"),
    ("WSM", "Samoa"),
    ("YEM", "Yemen"),
    ("ZAF", "South Africa"),
    ("ZMB", "Zambia"),
    ("ZWE", "Zimbabwe"),
    ("Region_ASEAN", "ASEAN"),
    ("Region_AU", "Australia"),
    ("Region_AU_North", "Northern Australia"),
    ("Region_AU_South", "Southern Australia"),
    ("Region_AU_West", "Western Australia"),
    ("Region_AU_East", "Eastern Australia"),
    ("Region_AU_Central", "Central Australia"),
    ("Region_CELAC_wBrazil", "CELAC with Brazil"),
    ("Region_ECO", "Economic Community"),
    ("Region_Europe", "Europe"),
    ("Region_EU", "European Union"),
    ("Region_SAARC", "SAARC"),
    ("Region_Middle_East", "Middle East"),
    ("Region_North_America", "North America")
]

country_map = {code: name for code, name in country_data}

def find_closest_country(input_name):
    closest_countries = sorted(country_map.items(), key=lambda item: lev.distance(input_name.lower(), item[1].lower()))
    return closest_countries[:5]

# Example usage
input_country_name = input('Enter Country Name: ').capitalize()
closest_matches = find_closest_country(input_country_name)

print("Closest matches:")
for code, name in closest_matches:
    print(f"{name} ({code})")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

url = 'https://ceos.org/gst/files/pilot_topdown_CO2_Budget_countries_v1.csv'
df_all = pd.read_csv(url, skiprows=52)

year_input = input("Enter the year (e.g., 2015): ")
experiment_options = ['IS', 'LNLG', 'LNLGIS', 'LNLGOGIS']
print("Available experiments:", experiment_options)
experiment_input = input("Choose an experiment from the list: ")

# Convert country name to country code
country_code =input("Enter the country code (e.g., USA): ")
if not country_code:
    print("Invalid country name. Exiting.")
    exit()

# Subset of columns for the given experiment
if experiment_input == 'IS':
    df = df_all.drop(df_all.columns[[4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 34, 35, 36]], axis=1)
elif experiment_input == 'LNLG':
    df = df_all.drop(df_all.columns[[2, 3, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 33, 35, 36]], axis=1)
elif experiment_input == 'LNLGIS':
    df = df_all.drop(df_all.columns[[2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 24, 25, 33, 34, 36]], axis=1)
elif experiment_input == 'LNLGOGIS':
    df = df_all.drop(df_all.columns[[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 33, 34, 35]], axis=1)
else:
    print("Invalid experiment type. Exiting.")
    exit()

# We can now look at the columns of data
df.head()

# We can sub-select the data for the country
country_data = df[df['Alpha 3 Code'] == country_code]

# Now we can look at the data for a specific experiment and country
country_data.head()

# Make plot
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.errorbar(country_data['Year'], country_data[experiment_input + ' dC_loss (TgCO2)'],
              yerr=country_data[experiment_input + ' dC_loss unc (TgCO2)'], label=experiment_input, capsize=10)
ax1.legend(loc='upper right')
ax1.set_ylabel('$\Delta$C$_\mathrm{loss}$ (TgCO$_2$ year$^{-1}$)')
ax1.set_xlabel('Year')
ax1.set_title('$\Delta$C$_\mathrm{loss}$ for ' + country_code)
ymin, ymax = ax1.get_ylim()
max_abs_y = max(abs(ymin), abs(ymax))
ax1.set_ylim([-max_abs_y, max_abs_y])
xmin, xmax = ax1.get_xlim()
ax1.plot([xmin, xmax], [0, 0], 'k', linewidth=0.5)
ax1.set_xlim([xmin, xmax])
plt.show()

# Make plot for the specific year
country_data_mean = country_data[country_data['Year'] == year_input]
if country_data_mean.empty:
    print("No data for the specified year. Exiting.")
    exit()

plt.bar(1, country_data_mean['FF (TgCO2)'], yerr=country_data_mean['FF unc (TgCO2)'], label='FF', alpha=0.5)
plt.bar(2, country_data_mean['Rivers (TgCO2)'], yerr=country_data_mean['River unc (TgCO2)'], label='Rivers', alpha=0.5)
plt.bar(3, country_data_mean['Wood+Crop (TgCO2)'], yerr=abs(country_data_mean['Wood+Crop unc (TgCO2)']), label='WoodCrop', alpha=0.5)
plt.bar(4, country_data_mean[experiment_input + ' dC_loss (TgCO2)'], yerr=country_data_mean['LNLGIS dC_loss unc (TgCO2)'], label='dC', alpha=0.5)
plt.bar(6, country_data_mean[experiment_input + ' NCE (TgCO2)'], yerr=country_data_mean['LNLGIS NCE unc (TgCO2)'], label='NCE', alpha=0.5)

ax = plt.gca()
ymin, ymax = ax.get_ylim()
plt.plot([5, 5], [ymin, ymax], 'k:')
xmin, xmax = ax.get_xlim()
plt.plot([xmin, xmax], [0, 0], 'k', linewidth=0.5)
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])

plt.xticks([1, 2, 3, 4, 6], ['Fossil\nFuels', 'Rivers', 'Wood+\nCrops', '$\mathrm{\Delta C _{loss}}$', 'NCE'])
plt.title(country_code + ' ' + year_input)
plt.ylabel('CO$_2$ Flux (TgCO$_2$ year$^{-1}$)')
plt.show()

# Select NCE, NBE or dC_loss
quantity = 'dC_loss'
comparison_value = 1000  # TgCO2/year

MIP_mean = country_data_mean[experiment_input + ' ' + quantity + ' (TgCO2)'].item()
MIP_std = country_data_mean[experiment_input + ' ' + quantity + ' unc (TgCO2)'].item()

# Perform t-test
t_value = abs(MIP_mean - comparison_value) / (MIP_std / np.sqrt(11))
critical_value = 2.23  # use p=0.05 significance
if t_value > critical_value:
    ttest = 'statistically different'
else:
    ttest = 'not statistically\ndifferent'

# Make plot
xbounds = abs(MIP_mean) + MIP_std * 4
if abs(critical_value) > xbounds:
    xbounds = abs(critical_value)
x_axis = np.arange(-1. * xbounds, xbounds, 1)
plt.plot(x_axis, norm.pdf(x_axis, MIP_mean, MIP_std))
ax = plt.gca()
ymin, ymax = ax.get_ylim()
xmin, xmax = ax.get_xlim()
plt.plot([0, 0], [ymin, ymax * 1.2], 'k:', linewidth=0.5)
plt.plot([xmin, xmax], [0, 0], 'k:', linewidth=0.5)
plt.plot([comparison_value, comparison_value], [ymin, ymax * 1.2], 'k')
plt.text(comparison_value + (xmax - xmin) * 0.01, ymax * 0.96, 'value = ' + str(comparison_value), ha='left', va='top')
plt.text(comparison_value + (xmax - xmin) * 0.01, ymax * 0.9, ttest, ha='left', va='top')
plt.ylim([ymin, ymax * 1.2])
plt.xlim([xmin, xmax])
plt.plot(MIP_mean, ymax * 1.03, 'ko')
plt.plot([MIP_mean - MIP_std,
          MIP_mean + MIP_std],
         [ymax * 1.03, ymax * 1.03], 'k')
plt.plot([MIP_mean - MIP_std,
          MIP_mean - MIP_std],
         [ymax * 1.005, ymax * 1.055], 'k')
plt.plot([MIP_mean + MIP_std,
          MIP_mean + MIP_std],
         [ymax * 1.005, ymax * 1.055], 'k')
plt.text(MIP_mean, ymax * 1.115,
         str(round(MIP_mean)) + ' $\pm$ ' +
         str(round(MIP_std)) + ' TgCO$_2$', ha='center', va='bottom')
plt.title(f"{country_code} {year_input} {experiment_input} {quantity} t-test")
plt.show()
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(country_data['Year'],country_data['Z-statistic'],label=experiment_input)
ax1.legend(loc='upper right')
ax1.set_ylabel('Z-statistic')
ax1.set_xlabel('Year')
ax1.set_title(country_code)
ymin, ymax = ax1.get_ylim()
max_abs_y = max(abs(ymin), abs(ymax))
ax1.set_ylim([-3, 3])
xmin, xmax = ax1.get_xlim()
ax1.plot([xmin,xmax],[0,0],'k',linewidth=0.5)
ax1.plot([xmin,xmax],[-1.96,-1.96],'k--',linewidth=0.5)
ax1.plot([xmin,xmax],[1.96,1.96],'k--',linewidth=0.5)
ax1.set_xlim([xmin, xmax])
ax1.text(xmin+0.12,2.6,'Fractional error reduction: '+str(country_data['FUR '+experiment_input].iloc[1]))
plt.show()