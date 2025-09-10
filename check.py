# # train_model.py

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
# import joblib

# # Load the dataset
# data = pd.read_csv("upi_fraud_dataset.csv")

# # Split the dataset into features and target
# X = data.drop(['Id', 'upi_number', 'fraud_risk'], axis=1)
# y = data['fraud_risk']

# # Split the dataset into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(
# X, y, test_size=0.3, random_state=42)

# # Train Random Forest model
# rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
# rf_model.fit(X_train, y_train)

# # Train Logistic Regression model
# lr_model = LogisticRegression(max_iter=1000, random_state=42)
# lr_model.fit(X_train, y_train)

# # Save both models
# joblib.dump(rf_model, "rf_model.pkl")
# joblib.dump(lr_model, "lr_model.pkl")

# train_model.py


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import sqlite3

# Load the data from transactions.db
conn = sqlite3.connect("transactions.db")
data = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()

# Convert prediction column to binary: 'Fraud' -> 1, 'Not Fraud' -> 0
data['prediction'] = data['prediction'].apply(lambda x: 1 if x == "Fraud" else 0)

# Debug: Confirm conversion
print("\nAfter converting to binary:")
print(data['prediction'].value_counts())

# Split the dataset into features and target
X = data[
    ['trans_hour', 'trans_day', 'trans_month', 'trans_year',
     'trans_amount',]]
y = data['prediction']

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)

# Train Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42,
                                  class_weight='balanced')
rf_model.fit(X_train, y_train)

# Debug: Evaluate model
y_pred = rf_model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(rf_model, "rf_model.pkl")
