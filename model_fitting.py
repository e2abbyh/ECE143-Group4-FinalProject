import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb


df = pd.read_csv('cleaned_combined_data.csv')

info = pd.DataFrame({
    'Data Type': df.dtypes,
    'Unique Values': df.nunique()
})

categorical_columns = ['Senator', 'Symbol', 'Company', 'Sector', 'Industry', 'Party',
                       'State', 'composite_litigation_name', 'company_ticker_symbol',
                       'cld_fic_filing_dt', 'cld_fic_class_start_dt', 'cld_fic_class_end_dt',
                       'comp_classification_sector_luv', 'comp_classification_indust_luv',
                       'issuer_comp_citizen_hq', 'issuer_comp_citizen_jurisdict',
                       'cld_fic_court_usdc_luv', 'company_market', 'company_market_status',
                       'cld_case_status_gen_luv', 'cld_flag_case_ever_go_trial', 'case_last_stage_date']

label_encoder = LabelEncoder()

for column in categorical_columns:
    df[column] = label_encoder.fit_transform(df[column].astype(str))

df = df.drop(columns=['Unnamed: 0', 'index_number'])

unique_values = df.nunique()
for column, num_unique in unique_values.items():
    print(f"{column}: {num_unique} unique values")

"""
Train and evaluate multiple regression models on a dataset, compute Mean Absolute Error (MAE),
and extract feature importances for each model.

Parameters:
-----------
X : pd.DataFrame
    The input features (predictors) of the dataset.
    
y : pd.Series
    The target variable (Estimated Holdings), log-transformed.
    
test_size : float, optional (default=0.2)
    The proportion of the dataset to include in the test split.
    
random_state : int, optional (default=42)
    The seed used by the random number generator for reproducibility.
    
Returns:
--------
dict
    A dictionary with model names as keys and a tuple containing the MAE and a DataFrame
    of feature importances (if applicable) as values.
"""

X = df.drop(columns=['Estimated Holdings'])
y = df['Estimated Holdings']

y = np.log1p(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(),
    "Random Forest": RandomForestRegressor(),
    "SVR": SVR(),
    "XGBoost": xgb.XGBRegressor()
}

results = {}
feature_importances = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred_log = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred_log)
    results[name] = mae

    if hasattr(model, "feature_importances_"):  # Tree-based models
        feature_importances[name] = model.feature_importances_
    elif hasattr(model, "coef_"):  # Linear models
        feature_importances[name] = np.abs(model.coef_)

best_model_name = min(results, key=results.get)
best_model_mae = results[best_model_name]

print("Model performance (Mean Absolute Error) in log-space:")
for name, mae in results.items():
    print(f"{name}: {mae:.4f}")

print(f"\nBest model: {best_model_name} with MAE: {best_model_mae:.4f}")

for name, importance in feature_importances.items():
    feature_importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": importance
    }).sort_values(by="Importance", ascending=False)
    
    print(f"\n{name} Feature Importances:")
    print(feature_importance_df.to_string(index=False))
