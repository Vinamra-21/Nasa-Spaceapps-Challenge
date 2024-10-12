import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib

# Load the data
df = pd.read_csv('cleaned_standardized_land_use_emission_data.csv')

# Prepare features (X) and target variable (y)
X = df[['cropLand', 'grazingLand', 'forestLand', 'fishingGround', 'builtupLand', 'Population',
        'BiologicalTreatmentofSolidWaste', 'ChemicalIndustry', 'CivilAviation', 
        'Emissionsfrombiomassburning', 'EntericFermentation', 'Fossilfuelfires', 
        'IncinerationandOpenBurningofWaste', 'MainActivityElectricityandHeatProduction', 
        'ManufacturingIndustriesandConstruction', 'ManureManagement', 'MetalIndustry', 
        'NonSpecified', 'OilandNaturalGas', 'OtherTransportation', 
        'PetroleumRefiningManufactureofSolidFuelsandOtherEnergyIndustries', 'Railways', 
        'Residentialandothersectors', 'Ricecultivations', 'RoadTransportationnoresuspension', 
        'SolidFuels', 'SolidWasteDisposal', 'WastewaterTreatmentandDischarge', 'WaterborneNavigation']]
y = df['carbon']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'methane_model.joblib')

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared Score: {r2}")

# Feature importance
feature_importance = pd.DataFrame({'feature': X.columns, 'importance': model.feature_importances_})
feature_importance = feature_importance.sort_values('importance', ascending=False)

# Plot feature importance
plt.figure(figsize=(12, 8))
plt.bar(feature_importance['feature'], feature_importance['importance'])
plt.title('Feature Importance in Predicting Methane Emissions')
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
