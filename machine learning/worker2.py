import pandas as pd
import requests

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

import pandas as pd
import requests

# Step 1: Fetch data from the API
api_data = []

for i in range(100, 101):
    url = "https://api.footprintnetwork.org/v1/data/100/all/EFCtot"

    # Your API credentials
    user_name = 'any-user-name'  # Replace with your actual username
    api_key = '1Veijtr0qGNr1j1Rl7M7Vs3roa6V420H1Fcv9b43tD0E0G74u9dc'  # Your provided API key

    # Set up headers for the request
    headers = {
        "Accept": "application/json"  # This specifies that we want a JSON response
    }

    # Fetch data from the API
    try:
        response = requests.get(url, auth=(user_name, api_key), headers=headers)

        # Debugging the response
        if response.status_code == 200:
            api_data = response.json()  # Use extend to add all records directly
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            api_data = []  # Set api_data to empty list if fetch fails

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        api_data = []  # Set api_data to empty list if an exception occurs

# Create DataFrame from API data
df_api = pd.DataFrame(api_data)
print("API DataFrame created successfully:")
print(df_api)

# Step 2: Load the CSV file
df_csv = pd.read_csv('data_with_median.csv')  # Replace with the path to your CSV file

# Step 3: Filter the API DataFrame for the years 2015 to 2019
df_api_filtered = df_api[df_api['Year'].between(2015, 2019)]

# Step 4: Merge the two DataFrames on the 'Country' and 'Year' columns
combined_df = pd.merge(
    df_api_filtered,
    df_csv,
    left_on=['Country', 'Year'],
    right_on=['country_code', 'Year'],
    how='inner'
)

# Step 5: Save the combined DataFrame to a CSV file
combined_df.to_csv('combined_data.csv', index=False)
print("Combined DataFrame saved to 'combined_data.csv'")
