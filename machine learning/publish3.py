import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Load the cleaned standardized dataset
df = pd.read_csv('cleaned_standardized_land_use_emission_data.csv')

# Select numeric columns excluding 'year'
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.drop('year', errors='ignore')

# Prepare the features (X) and target variable (y)
target_variable = 'Population'  # Change this to your target variable
X = df[numeric_cols].drop(target_variable, axis=1)
y = df[target_variable]

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a list of models to train
models = {
    'Linear Regression': LinearRegression(),
    'Lasso Regression': Lasso(),
    'Ridge Regression': Ridge(),
    'Decision Tree Regressor': DecisionTreeRegressor(),
    'Random Forest Regressor': RandomForestRegressor(),
    'Gradient Boosting Regressor': GradientBoostingRegressor(),
    'K-Neighbors Regressor': KNeighborsRegressor(),
    'Support Vector Regressor': SVR(),
}

# Dictionary to hold model performance
results = {}

# Train each model and evaluate its performance
for name, model in models.items():
    # Using Standard Scaler for models that might benefit from feature scaling
    pipeline = make_pipeline(StandardScaler(), model) if name != 'Decision Tree Regressor' else model
    
    # Train the model
    pipeline.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = pipeline.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Store the results
    results[name] = {'MSE': mse, 'R^2': r2}

# Print the performance of each model
for model_name, metrics in results.items():
    print(f'{model_name}:')
    print(f'  Mean Squared Error: {metrics["MSE"]:.4f}')
    print(f'  R^2 Score: {metrics["R^2"]:.4f}\n')
