import statistics

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder

from split_datas import get_pickle_file

print("[+] Please wait, this may take a while...")

datas = get_pickle_file()

accuracy_scores = {}
for appName in datas:
    print(" ╰─ Analyzing " + appName + "...")
    accuracy_scores[appName] = []
    for i in range(0, len(datas[appName])):
        copy = datas[appName].copy()

        train = copy.pop(i)

        # Concatenate all dataframes in the list copy
        concatenated_df = pd.concat(copy)

        # Split train dataframe into X_train and y_train with y_train being the "Tag"
        X_train = train.drop(columns=["Tag"], axis=1)
        y_train = train["Tag"]

        # Split concatenated_df into X_train (just drop the Tag column)
        X_test = concatenated_df.drop(columns=["Tag"], axis=1)
        y_test = concatenated_df["Tag"]

        # Encode strings into numerical values
        label_encoder = LabelEncoder()
        X_train_encoded = X_train.apply(label_encoder.fit_transform)
        y_train_encoded = label_encoder.fit_transform(y_train)
        X_test_encoded = X_test.apply(label_encoder.fit_transform)
        y_test_encoded = label_encoder.fit_transform(y_test)

        # Utilise un imputeur pour remplacer les NaN par la moyenne des colonnes
        imputer = SimpleImputer(strategy='mean')
        X_train_imputed = imputer.fit_transform(X_train_encoded)
        X_test_imputed = imputer.transform(X_test_encoded)

        # Init KNN
        naive_bayes_model = GaussianNB()

        # Train model
        naive_bayes_model.fit(X_train_imputed, y_train_encoded)

        # Predict using test datas
        predictions = naive_bayes_model.predict(X_test_imputed)

        # Calculate accuracy
        accuracy = accuracy_score(y_test_encoded, predictions)
        accuracy = accuracy * 100
        accuracy_scores[appName].append(accuracy)

print("\nAccuracy scores :")
for appName in accuracy_scores:
    print("[+] " + appName)
    print(" ╰─ Mean : " + str(np.mean(accuracy_scores[appName])))
    print(" ╰─ Median : " + str(statistics.median(accuracy_scores[appName])))
