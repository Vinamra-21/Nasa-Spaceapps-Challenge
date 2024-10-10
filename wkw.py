import pandas as pd # for manipulating csv dataset
import numpy as np
import matplotlib.pyplot as plt # make plots
from scipy.stats import norm # We will use this for understanding significance
url ='https://ceos.org/gst/files/pilot_topdown_CO2_Budget_countries_v1.csv'
df_all = pd.read_csv(url, skiprows=52)
# Choose one experiment from the list ['IS', 'LNLG', 'LNLGIS', 'LNLGOGIS']
experiment = 'LNLGIS'

# Subset of columns for a given experiment
if experiment == 'IS':
    df = df_all.drop(df_all.columns[[4,5,6,7,8,9,12,13,14,15,16,17,20,21,22,23,24,25,34,35,36]], axis=1)
if experiment == 'LNLG':
    df = df_all.drop(df_all.columns[[2,3,6,7,8,9,10,11,14,15,16,17,18,19,22,23,24,25,33,35,36]], axis=1)
if experiment == 'LNLGIS':
    df = df_all.drop(df_all.columns[[2,3,4,5,8,9,10,11,12,13,16,17,18,19,20,21,24,25,33,34,36]], axis=1)
if experiment == 'LNLGOGIS':
    df = df_all.drop(df_all.columns[[2,3,4,5,6,7,10,11,12,13,14,15,18,19,20,21,22,23,33,34,35]], axis=1)

# We can now look at the colums of data
df.head()
# Choose a country
country_name = 'USA' 

# We can sub-select the data for the country
country_data = df[df['Alpha 3 Code'] == country_name]

# Now we can look at the data for a specific experiment and country
country_data.head()
# Make plot
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.errorbar(country_data['Year'],country_data[experiment+' dC_loss (TgCO2)'],
                    yerr=country_data[experiment+' dC_loss unc (TgCO2)'],label=experiment,capsize=10)
ax1.legend(loc='upper right')
ax1.set_ylabel('$\Delta$C$_\mathrm{loss}$ (TgCO$_2$ year$^{-1}$)')
ax1.set_xlabel('Year')
ax1.set_title('$\Delta$C$_\mathrm{loss}$ for '+country_name)
ymin, ymax = ax1.get_ylim()
max_abs_y = max(abs(ymin), abs(ymax))
ax1.set_ylim([-max_abs_y, max_abs_y])
xmin, xmax = ax1.get_xlim()
ax1.plot([xmin,xmax],[0,0],'k',linewidth=0.5)
ax1.set_xlim([xmin, xmax])
plt.show()
# Pick a specifc year (or mean year)
year=str(2015)

# Make plot
country_data_mean = country_data[country_data['Year'] == year]
a=country_data_mean['Wood+Crop (TgCO2)']
b=country_data_mean['Wood+Crop unc (TgCO2)']
print(b)
#
plt.bar(1, country_data_mean['FF (TgCO2)'], yerr=country_data_mean['FF unc (TgCO2)'], label='FF', alpha=0.5)
plt.bar(2, country_data_mean['Rivers (TgCO2)'], yerr=country_data_mean['River unc (TgCO2)'], label='Rivers', alpha=0.5)
plt.bar(3, country_data_mean['Wood+Crop (TgCO2)'], yerr=abs(country_data_mean['Wood+Crop unc (TgCO2)']), label='WoodCrop', alpha=0.5)
plt.bar(4, country_data_mean[experiment+' dC_loss (TgCO2)'], yerr=country_data_mean['LNLGIS dC_loss unc (TgCO2)'], label='dC', alpha=0.5)
plt.bar(6, country_data_mean[experiment+' NCE (TgCO2)'], yerr=country_data_mean['LNLGIS NCE unc (TgCO2)'], label='NCE', alpha=0.5)
ax = plt.gca()
ymin, ymax = ax.get_ylim()
plt.plot([5,5],[ymin,ymax],'k:')
xmin, xmax = ax.get_xlim()
plt.plot([xmin,xmax],[0,0],'k',linewidth=0.5)
plt.xlim([xmin,xmax])
plt.ylim([ymin,ymax])
#
plt.xticks([1,2,3,4,6], ['Fossil\nFuels','Rivers','Wood+\nCrops','$\mathrm{\Delta C _{loss}}$','NCE'])
plt.title(country_name+' '+year)
plt.ylabel('CO$_2$ Flux (TgCO$_2$ year$^{-1}$)')
plt.show()
# Select NCE, NBE or dC_loss
quantity = 'dC_loss'

# Value for comparison
comparison_value = 1000 # TgCO2/year


MIP_mean = country_data_mean[experiment+' '+quantity+' (TgCO2)'].item()
MIP_std = country_data_mean[experiment+' '+quantity+' unc (TgCO2)'].item()

# Perform t-test
t_value = abs(MIP_mean - comparison_value)/(MIP_std / np.sqrt(11))
crtical_value = 2.23 # use p=0.05 significance
if t_value > crtical_value:
    ttest = 'statistically different'
if t_value < crtical_value:
    ttest = 'not statistically\ndifferent'

# Make plot
xbounds = abs(MIP_mean)+MIP_std*4
if abs(crtical_value) > xbounds:
    xbounds = abs(crtical_value)
x_axis = np.arange(-1.*xbounds, xbounds, 1) 
plt.plot(x_axis, norm.pdf(x_axis, MIP_mean, MIP_std)) 
ax = plt.gca()
ymin, ymax = ax.get_ylim()
xmin, xmax = ax.get_xlim()
plt.plot([0,0],[ymin,ymax*1.2],'k:',linewidth=0.5)
plt.plot([xmin,xmax],[0,0],'k:',linewidth=0.5)
plt.plot([comparison_value,comparison_value],[ymin,ymax*1.2],'k')
plt.text(comparison_value+(xmax-xmin)*0.01,ymax*0.96,'value = '+str(comparison_value),ha='left',va='top')
plt.text(comparison_value+(xmax-xmin)*0.01,ymax*0.9,ttest,ha='left',va='top')
plt.ylim([ymin,ymax*1.2])
plt.xlim([xmin,xmax])
plt.plot(MIP_mean,ymax*1.03,'ko')
plt.plot([MIP_mean-MIP_std,
         MIP_mean+MIP_std],
         [ymax*1.03,ymax*1.03],'k')
plt.plot([MIP_mean-MIP_std,
         MIP_mean-MIP_std],
         [ymax*1.005,ymax*1.055],'k')
plt.plot([MIP_mean+MIP_std,
         MIP_mean+MIP_std],
         [ymax*1.005,ymax*1.055],'k')
plt.text(MIP_mean,ymax*1.115,
         str(round(MIP_mean))+' $\pm$ '+
         str(round(MIP_std))+' TgCO$_2$',ha='center')
plt.title(country_name+' '+year+' '+quantity+'')
plt.yticks([])
plt.ylabel('Probability')
plt.xlabel(quantity+' (TgCO$_2$ year$^{-1}$)')
plt.show()
# Make plot
fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
ax1.plot(country_data['Year'],country_data['Z-statistic'],label=experiment)
ax1.legend(loc='upper right')
ax1.set_ylabel('Z-statistic')
ax1.set_xlabel('Year')
ax1.set_title(country_name)
ymin, ymax = ax1.get_ylim()
max_abs_y = max(abs(ymin), abs(ymax))
ax1.set_ylim([-3, 3])
xmin, xmax = ax1.get_xlim()
ax1.plot([xmin,xmax],[0,0],'k',linewidth=0.5)
ax1.plot([xmin,xmax],[-1.96,-1.96],'k--',linewidth=0.5)
ax1.plot([xmin,xmax],[1.96,1.96],'k--',linewidth=0.5)
ax1.set_xlim([xmin, xmax])
ax1.text(xmin+0.12,2.6,'Fractional error reduction: '+str(country_data['FUR '+experiment].iloc[1]))
plt.show()