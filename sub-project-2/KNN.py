# Imports
from split_datas import get_pickle_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier


datas = get_pickle_file()

for appName in datas:
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
        y_train_encoded = X_train.apply(label_encoder.fit_transform)
        X_test_encoded  = X_test.apply(label_encoder.fit_transform)
        y_test_encoded  = label_encoder.fit_transform(y_test)

        # Init KNN
        knn_model = KNeighborsClassifier(n_neighbors=3)

        print("training...")
        # Train model
        knn_model.fit(X_train_encoded, y_train_encoded)

        print("predicting...")
        # Predict using test datas
        predictions = knn_model.predict(X_test_encoded)

        # Calculate accuracy
        accuracy = np.mean(predictions == y_test)
        print(f"Accuracy for {appName} number {i} : {accuracy}")
    print("---------------------------------")