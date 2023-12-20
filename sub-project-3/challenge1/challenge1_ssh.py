# Imports

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from result_file import create_result_file
from split_datas import get_pickle_file

print("[+] Please wait, this may take a while...")

train = get_pickle_file("train")
test = get_pickle_file("test_ssh")

# Switch to dataframe
train = pd.DataFrame(train["SSH"])
test = pd.DataFrame(test["SSH"])

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

# Plot the pie chart of Attack vs Normal
print("[+] Plotting the pie chart of Attack vs Normal")

labels = 'Normal', 'Attack'
sizes = [list(y_train).count(0), list(y_train).count(1)]
print(f'Normal : {list(y_train).count(0)}')
print(f'Attack : {list(y_train).count(1)}')
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
plt.title("Attack vs Normal SSH prediction with Random Forest classifier")
plt.savefig("plot_images/RandomForest_SSH_Pie.png")

# Create result file
print("[+] Creating result file")

create_result_file(predictions, random_forest_classifier.predict_proba(X_test)[:, 1], "RandomForest", "SSH", "1")
