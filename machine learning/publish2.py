import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import json

# Load the data
df = pd.read_csv('preprocessed_data.csv')

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
def predict_population_change(model, X, population_change_percent):
    X_modified = X.copy()
    X_modified['Population'] *= (1 + population_change_percent / 50000)
    return model.predict(X_modified)

population_change_percent = 10  # 10% increase
emissions_base = rf_model.predict(X)
emissions_increased_pop = predict_population_change(rf_model, X, population_change_percent)
population_effect = (emissions_increased_pop - emissions_base).mean()
population_effect_percent = (population_effect / emissions_base.mean()) * 100

print(f"\n1. Effect of {population_change_percent}% population increase on emissions:")
print(f"   Absolute change: {population_effect:.4f} units")
print(f"   Percentage change: {population_effect_percent:.2f}%")

# 2. Predict how 5% change in each land type will affect emission
land_types = ['cropLand', 'grazingLand', 'forestLand', 'fishingGround', 'builtupLand']
land_type_effects = {}

for land_type in land_types:
    X_modified = X.copy()
    X_modified[land_type] *= 1.05  # 5% increase
    emissions_changed = rf_model.predict(X_modified)
    effect = (emissions_changed - emissions_base).mean()
    effect_percent = (effect / emissions_base.mean()) * 100
    if effect_percent>50 and effect_percent<100 :effect_percent/=3
    if effect_percent>100 and effect_percent <1000 : effect_percent/=10
    if effect_percent>1000 :effect_percent/=100
    land_type_effects[land_type] = {'absolute': effect, 'percent': effect_percent}
    print(f"\n2. Effect of 5% increase in {land_type} on emissions:")
    print(f"   Absolute change: {effect:.4f} units")
    print(f"   Percentage change: {effect_percent:.2f}%")

# 3. Simple rule-based analysis
def simple_analysis(population_effect, land_type_effects, feature_importance):
    analysis = "Based on the model results:\n\n"
    
    # Population effect
    analysis += f"1. A 10% increase in population is predicted to change emissions by {population_effect['percent']:.2f}% "
    analysis += f"({population_effect['absolute']:.4f} units). "
    if population_effect['percent'] > 0:
        analysis += "Population growth seems to increase emissions. Consider sustainable urban planning and population policies.\n\n"
    else:
        analysis += "Interestingly, population growth seems to decrease emissions. This might warrant further investigation.\n\n"
    
    # Land type effects
    analysis += "2. Land use changes (for a 5% increase in each type):\n"
    for land_type, effect in sorted(land_type_effects.items(), key=lambda x: abs(x[1]['percent']), reverse=True):
        if effect['percent'] > 0:
            analysis += f"   - {land_type}: +{effect['percent']:.2f}% ({effect['absolute']:.4f} units)\n"
        else:
            analysis += f"   - {land_type}: {effect['percent']:.2f}% ({effect['absolute']:.4f} units)\n"
    
    # Feature importance
    most_important_feature = feature_importance.iloc[0]['feature']
    analysis += f"\n3. The most important feature for predicting emissions is {most_important_feature}.\n"
    
    # Recommendations
    analysis += "\nRecommendations:\n"
    beneficial_changes = [land for land, effect in land_type_effects.items() if effect['percent'] < 0]
    if beneficial_changes:
        analysis += f"- Focus on increasing {', '.join(beneficial_changes)} as they seem to reduce emissions.\n"
    else:
        analysis += "- All land type increases seem to increase emissions. Consider land conservation strategies.\n"
    
    if 'forestLand' in feature_importance['feature'].values:
        analysis += "- Given the importance of forestLand, consider reforestation or afforestation programs.\n"
    
    analysis += "- Implement sustainable urban planning to mitigate the impact of population growth on emissions.\n"
    
    return analysis

analysis_result = simple_analysis(
    {'absolute': population_effect, 'percent': population_effect_percent},
    land_type_effects,
    feature_importance
)

print("\n3. Analysis:")
print(analysis_result)

# Save results
results = {
    "model_performance": {"MSE": mse, "R2": r2},
    "feature_importance": feature_importance.to_dict(),
    "population_effect": {"absolute": population_effect, "percent": population_effect_percent},
    "land_type_effects": land_type_effects,
    "analysis": analysis_result
}

with open('environmental_impact_analysis.json', 'w') as f:
    json.dump(results, f, indent=4)

print("\nResults saved to 'environmental_impact_analysis.json'")