# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the standardized data
df = pd.read_csv('cleaned_standardized_land_use_emission_data.csv')

# Drop non-numeric columns (keeping 'year' as required for analysis)
df_numeric = df.select_dtypes(include=['float64', 'int64']).drop('year', axis=1)
# Check column names to verify if 'methane' exists
print(df_numeric.columns)

# If the column name is correct, the following will work
X = df_numeric.drop('Population', axis=1)
y = df_numeric['Population']


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 1: Model 1 - Linear Regression for population impact on methane
model_lr_pop = LinearRegression()
model_lr_pop.fit(X_train[['Population']], y_train)
y_pred_pop_lr = model_lr_pop.predict(X_test[['Population']])

# Step 2: Model 2 - Random Forest for population impact on methane
model_rf_pop = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf_pop.fit(X_train[['Population']], y_train)
y_pred_pop_rf = model_rf_pop.predict(X_test[['Population']])

# Calculate R2 and MSE for both population models
r2_lr_pop = r2_score(y_test, y_pred_pop_lr)
mse_lr_pop = mean_squared_error(y_test, y_pred_pop_lr)

r2_rf_pop = r2_score(y_test, y_pred_pop_rf)
mse_rf_pop = mean_squared_error(y_test, y_pred_pop_rf)

# Step 3: Model 3 - Linear Regression for 5% change in land types impact on methane
model_lr_land = LinearRegression()
land_columns = ['cropLand', 'grazingLand', 'forestLand', 'fishingGround', 'builtupLand']
X_land = X_train[land_columns]
model_lr_land.fit(X_land, y_train)
y_pred_land_lr = model_lr_land.predict(X_test[land_columns])

# Calculate R2 and MSE for land types model
r2_lr_land = r2_score(y_test, y_pred_land_lr)
mse_lr_land = mean_squared_error(y_test, y_pred_land_lr)

# Organize results
results = {
    'Linear Regression Population': {'R2': r2_lr_pop, 'MSE': mse_lr_pop},
    'Random Forest Population': {'R2': r2_rf_pop, 'MSE': mse_rf_pop},
    'Linear Regression Land Types': {'R2': r2_lr_land, 'MSE': mse_lr_land},
}

results
