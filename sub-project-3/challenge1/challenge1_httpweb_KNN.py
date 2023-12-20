# Imports

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

from result_file import create_result_file
from split_datas import get_pickle_file
from plot_result import plot_result

print("[+] Please wait, this may take a while...")

train = get_pickle_file("train")
test = get_pickle_file("test_http")

# Switch to dataframe
train = pd.DataFrame(train["HTTPWeb"])
test = pd.DataFrame(test["HTTPWeb"])

# Split train dataframe into X_train and y_train with y_train being the "Tag"
X_train = train.drop(
    columns=["Tag", "appName", "sourcePayloadAsBase64", "destinationPayloadAsBase64", "sensorInterfaceId", "startTime"],
    axis=1)
y_train = train["Tag"]

# Split concatenated_df into X_train (drop the Tag column)
X_test = test.drop(columns=["Tag", "appName", "sourcePayloadAsBase64", "destinationPayloadAsBase64"], axis=1)

# Init KNN
knn_model = KNeighborsClassifier(n_neighbors=3)

# Train model
print("[+] Training model")
knn_model.fit(X_train, y_train)

# Predict using test datas
print("[+] Predicting using test datas")
predictions = knn_model.predict(X_test)

# Plot the pie chart of Attack vs Normal
plot_result(predictions, "plot_images/KNN_HTTPWeb_Pie.png",
            "Attack vs Normal HTTPWeb prediction with Random Forest classifier")

# Create result file
print("[+] Creating result file")

create_result_file(predictions, knn_model.predict_proba(X_test)[:, 1], "KNN", "HTTPWeb", "1")
