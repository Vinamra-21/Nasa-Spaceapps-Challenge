import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import json
import google.generativeai as genai

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
columns_to_standardize = [col for col in features if col != 'year']
df_imputed[columns_to_standardize] = scaler.fit_transform(df_imputed[columns_to_standardize])

# Prepare data for modeling
X = df_imputed[features]
y = df_imputed[target]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Random Forest Model:")
print(f"Mean Squared Error: {mse}")
print(f"R-squared Score: {r2}")

# Feature importance
feature_importance = pd.DataFrame({'feature': features, 'importance': rf_model.feature_importances_})
print("\nFeature Importance:")
print(feature_importance.sort_values('importance', ascending=False))

# 1. Predict how change in population will affect emission
def predict_population_change(model, X, population_change):
    X_modified = X.copy()
    X_modified['Population'] += population_change
    return model.predict(X_modified)

population_increase = X['Population'].mean() * 0.1  # 10% increase
emissions_base = rf_model.predict(X)
emissions_increased_pop = predict_population_change(rf_model, X, population_increase)
population_effect = (emissions_increased_pop - emissions_base).mean()

print(f"\n1. Effect of 10% population increase on emissions: {population_effect}")

# 2. Predict how 5% change in each land type will affect emission
land_types = ['cropLand', 'grazingLand', 'forestLand', 'fishingGround', 'builtupLand']
land_type_effects = {}

for land_type in land_types:
    X_modified = X.copy()
    X_modified[land_type] *= 1.05  # 5% increase
    emissions_changed = rf_model.predict(X_modified)
    effect = (emissions_changed - emissions_base).mean()
    land_type_effects[land_type] = effect
    print(f"\n2. Effect of 5% increase in {land_type} on emissions: {effect}")

# 3. Use Gemini to analyze results
genai.configure(api_key="")  # No API key needed for basic usage

analysis_prompt = f"""
Analyze the following results from our environmental impact prediction model:

1. A 10% increase in population is predicted to change emissions by {population_effect:.4f} units.

2. The effects of a 5% increase in different land types on emissions are:
{json.dumps(land_type_effects, indent=2)}

3. The feature importance of our model is:
{feature_importance.to_string()}

Based on these results, what course of action would likely give the most benefit in terms of reducing emissions? 
Provide a concise analysis and recommendation.
"""

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(analysis_prompt)

print("\n3. Gemini Analysis:")
print(response.text)

# Save results
results = {
    "model_performance": {"MSE": mse, "R2": r2},
    "feature_importance": feature_importance.to_dict(),
    "population_effect": population_effect,
    "land_type_effects": land_type_effects,
    "gemini_analysis": response.text
}

with open('environmental_impact_analysis.json', 'w') as f:
    json.dump(results, f, indent=4)

print("\nResults saved to 'environmental_impact_analysis.json'")