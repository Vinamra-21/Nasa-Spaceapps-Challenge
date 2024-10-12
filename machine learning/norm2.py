import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import json

# Load the data
df = pd.read_csv('merged_land_use_emission_data.csv')

# Select features and target
features = ['year', 'Population', 'cropLand', 'grazingLand', 'forestLand', 'fishingGround', 'builtupLand', 'carbon']
target = 'SolidWasteDisposal'

# Select the columns we want to use
df_selected = df[features + [target]]

# Replace NaN values with mean for each column
imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df_selected), columns=df_selected.columns)

# Standardize relevant columns (exclude 'year')
scaler = StandardScaler()
columns_to_standardize = [col for col in features+[target] if col != 'year']
df_imputed[columns_to_standardize] = scaler.fit_transform(df_imputed[columns_to_standardize])

# Save preprocessing stats
preprocessing_stats = {
    "imputer_statistics": dict(zip(df_selected.columns, imputer.statistics_)),
    "scaler_mean": dict(zip(columns_to_standardize, scaler.mean_)),
    "scaler_scale": dict(zip(columns_to_standardize, scaler.scale_))
}

with open('preprocessing_stats.json', 'w') as f:
    json.dump(preprocessing_stats, f, indent=4)

# Save updated CSV
df_imputed.to_csv('preprocessed_data.csv', index=False)

# Prepare data for modeling
X = df_imputed[features]
y = df_imputed[target]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models
models = {
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(random_state=42),
    "Lasso Regression": Lasso(random_state=42),
    "SVR": SVR(),
    "KNN Regressor": KNeighborsRegressor(),
    "Decision Tree": DecisionTreeRegressor(random_state=42)
}

# Train and evaluate models
results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results[name] = {"MSE": mse, "R2": r2}

    print(f"\n{name}:")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared Score: {r2}")

    if hasattr(model, 'feature_importances_'):
        feature_importance = pd.DataFrame({'feature': features, 'importance': model.feature_importances_})
        print("\nFeature Importance:")
        print(feature_importance.sort_values('importance', ascending=False))

# Save results
with open('model_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("\nResults saved to 'model_results.json'")
print("Preprocessing stats saved to 'preprocessing_stats.json'")
print("Updated data saved to 'preprocessed_data.csv'")