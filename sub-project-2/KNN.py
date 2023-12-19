# Imports
import statistics

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import KNeighborsClassifier

from split_datas import get_pickle_file

print("[+] Please wait, this may take a while...")

datas = get_pickle_file()

accuracy_scores = {}
precision_scores = {}
roc_auc_scores = {}

for appName in datas:
    print(" ╰─ Analyzing " + appName + "...")
    accuracy_scores[appName] = []
    precision_scores[appName] = []
    roc_auc_scores[appName] = []

    for i in range(0, len(datas[appName])):
        copy = datas[appName].copy()

        test = copy.pop(i)

        # Concatenate all dataframes in the list copy
        train = pd.concat(copy)

        # Split train dataframe into X_train and y_train with y_train being the "Tag"
        X_train = train.drop(columns=["Tag", "appName", "sourcePayloadAsBase64", "destinationPayloadAsBase64"], axis=1)
        y_train = train["Tag"]

        # Split concatenated_df into X_train (drop the Tag column)
        X_test = test.drop(columns=["Tag", "appName", "sourcePayloadAsBase64", "destinationPayloadAsBase64"], axis=1)
        y_test = test["Tag"]

        # Init KNN
        knn_model = KNeighborsClassifier(n_neighbors=3)

        # Train model
        print(f' ╰─ Training model...    {i + 1}/{len(datas[appName])}')
        knn_model.fit(X_train, y_train)

        # Predict using test datas
        predictions = knn_model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, predictions)
        accuracy = accuracy * 100
        accuracy_scores[appName].append(accuracy)

        precision = precision_score(y_test, predictions, average=None)
        precision_scores[appName].append(precision)

        roc_auc = roc_auc_score(y_test, predictions)
        roc_auc_scores[appName].append(roc_auc)

        from sklearn.metrics import roc_curve
        import matplotlib.pyplot as plt

        # Compute ROC curve
        fpr, tpr, thresholds = roc_curve(y_test, predictions)

        # Plot ROC curve
        plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC curve for ' + appName + ' (fold ' + str(i) + ')')
        plt.legend(loc="lower right")
        plt.savefig("ROC_images/KNN/ROC_" + appName + "_" + str(i) + ".png")

print("\nResults :")
for appName in accuracy_scores:
    print("[+] " + appName)
    print(" ╰─ Mean Accuracy: " + str(np.mean(accuracy_scores[appName])))
    print(" ╰─ Median Accuracy : " + str(statistics.median(accuracy_scores[appName])))
    print(" ╰─ Mean Precision : " + str(np.mean(precision_scores[appName])))
    print(" ╰─ Mean ROC AUC : " + str(np.mean(roc_auc_scores[appName])))
