# Imports

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from result_file import create_result_file
from load_file import load_pickle
print("[+] Please wait, this may take a while...")

train, test = load_pickle()

# Split train dataframe into X_train and y_train with y_train being the "Tag"
X_train = train.drop(
    columns=["Tag", "appName", "sourcePayloadAsBase64", "destinationPayloadAsBase64", "sensorInterfaceId", "startTime"],
    axis=1)
y_train = train["Tag"]

# Split concatenated_df into X_train (drop the Tag column)
X_test = test.drop(columns=["Tag", "appName", "sourcePayloadAsBase64", "destinationPayloadAsBase64"], axis=1)

# Init Random Forest
random_forest_classifier = RandomForestClassifier(n_estimators=100)

# Train model
print("[+] Training model")
random_forest_classifier.fit(X_train, y_train)

# Predict using test datas
print("[+] Predicting using test datas")
predictions = random_forest_classifier.predict(X_test)

# Create result file
print("[+] Creating result file")

create_result_file(predictions, random_forest_classifier.predict_proba(X_test)[:, 1], "RandomForest", "1")
