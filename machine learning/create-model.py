import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('cleaned_standardized_land_use_emission_data.csv')

# Prepare features (X) and target variable (y)
X = df[['cropLand', 'grazingLand', 'forestLand', 'fishingGround', 'builtupLand', 'Population']]
y = df['carbon']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'model2.joblib')

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

# Select top 5 important features
top_5_features = feature_importance.head(5)['feature'].tolist()
print(f"Top 5 important features: {top_5_features}")

plt.figure(figsize=(10, 6))
plt.bar(feature_importance['feature'], feature_importance['importance'])
plt.title('Feature Importance in Predicting Methane Emissions')
plt.xlabel('Land Use Type')
plt.ylabel('Importance')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Update the model to train on top 5 features
X_top5 = X[top_5_features]
X_train_top5, X_test_top5, y_train_top5, y_test_top5 = train_test_split(X_top5, y, test_size=0.2, random_state=42)

# Train model on top 5 features
model_top5 = RandomForestRegressor(n_estimators=100, random_state=42)
model_top5.fit(X_train_top5, y_train_top5)

# Save the top 5 model
joblib.dump(model_top5, 'model_top5.joblib')

# Make predictions with top 5 model
y_pred_top5 = model_top5.predict(X_test_top5)

# Evaluate the top 5 model
mse_top5 = mean_squared_error(y_test_top5, y_pred_top5)
r2_top5 = r2_score(y_test_top5, y_pred_top5)

print(f"Top 5 Features Model - Mean Squared Error: {mse_top5}")
print(f"Top 5 Features Model - R-squared Score: {r2_top5}")
