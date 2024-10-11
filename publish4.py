import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load the cleaned standardized dataset
df = pd.read_csv('cleaned_standardized_land_use_emission_data.csv')

# Select all numeric columns except 'year'
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
numeric_columns.remove('year')  # Remove year from the features

# Define the target variable (e.g., carbon emissions or total emissions)
target_variable = 'carbon'  # Example: using 'carbon' as the emission target
X = df[numeric_columns].drop(columns=[target_variable])
y = df[target_variable]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Get predictions for the test set
y_pred = model.predict(X_test)
error = mean_absolute_error(y_test, y_pred)
print(f'Model Test Error (Mean Absolute Error): {error:.4f}')

# Step 1: Predict the effect of a 5% increase in population and each land type on emissions
def predict_with_changes(df, feature, percentage_change):
    """ Function to predict emission changes with percentage changes in specific feature. """
    # Create a copy of the test set
    df_copy = df.copy()
    
    # Increase the specific feature by the given percentage
    df_copy[feature] *= (1 + percentage_change / 100.0)
    
    # Predict emissions with the modified feature
    return model.predict(df_copy)

# Step 2: Apply a 5% change to each numeric feature and calculate percentage change in emissions
percentage_change = 5  # 5% change
results = {}

for feature in X.columns:
    # Predict emissions before the change
    initial_predictions = model.predict(X_test)
    
    # Predict emissions after a 5% increase in the feature
    new_predictions = predict_with_changes(X_test, feature, percentage_change)
    
    # Calculate the percentage change in emissions
    percentage_change_in_emission = ((new_predictions - initial_predictions) / initial_predictions) * 100
    
    # Store the mean percentage change for each feature
    results[feature] = percentage_change_in_emission.mean()

# Step 3: Present the results as percentage changes for each feature
print("Percentage Change in Emissions Due to 5% Change in Each Feature:")
for feature, change in results.items():
    print(f"{feature}: {change:.2f}% change in emissions")

# Step 4: Predict the effect of population changes while considering other features
# We'll add a small tweak to ensure population alone doesn't lead to unrealistic results.
X_test_population_only = X_test.copy()
X_test_population_only['Population'] *= 1.05  # 5% increase in population

# Predict emissions with a 5% increase in population and all other factors constant
new_predictions_population = model.predict(X_test_population_only)

# Calculate the percentage change in emissions due to population increase
population_emission_change = ((new_predictions_population - y_pred) / y_pred) * 100
mean_population_emission_change = population_emission_change.mean()

print(f"\nMean Percentage Change in Emission Due to 5% Population Increase: {mean_population_emission_change:.2f}%")
