import matplotlib.pyplot as plt
import numpy as np

data = {
    "KNN": {
        "httpweb": [99.83410889052463, 99.83191588486238, 0.9323719879324288, 0.922938276369142],
        "ssh": [99.98968540484786, 100.0, 0.9998087954110899, 0.9999294283697953],
        "SMTP": [99.91680147019953, 99.93069993069993, 0.9854343185616259, 0.9695434652892482],
        "FTP": [99.77809144660078, 99.82935153583618, 0.9692681411015588, 0.9723742178026145],
    },
    "Naive Bayes": {
        "httpweb": [98.39389110563346, 98.67907809516849, 0.5404557374966396, 0.5533703016315652],
        "ssh": [75.16756432000766, 75.0, 0.8736756701734437, 0.5322518895493253],
        "SMTP": [97.69866099963187, 97.57449757449757, 0.656003301540719, 0.9807490057894134],
        "FTP": [85.35459265053554, 85.31796841655996, 0.5586705979412233, 0.9253365791167967],
    },
    "Random Forest": {
        "httpweb": [99.99744221326846, 99.9981729987485, 0.9995135659942382, 0.9982904236198072],
        "ssh": [99.98968540484786, 100.0, 0.9999301675977653, 0.9998031496062992],
        "SMTP": [99.97226074895977, 100.0, 0.9998598452109688, 0.9870445344129555],
        "FTP": [100.0, 100.0, 1.0, 1.0],
    },
    "MLPC": {
        "httpweb": [99.41664066669647, 99.41262446332328, 0.4970832033334823, 0.5],
        "ssh": [92.39975968056656, 92.37113402061856, 0.9496766445957265, 0.8588010369325156],
        "SMTP": [98.96019138737587, 98.8911988911989, 0.4948009569368793, 0.5],
        "FTP": [98.1394728907107, 98.12286689419795, 0.6722472823958696, 0.5427075049301581],
    }
}

columns = ["Mean Accuracy", "Median Accuracy", "Mean Precision", "Mean ROC AUC"]

# Make a graph of the AUC scores for each classifier (We take the mean of each AUC score per classifier)

# Get the mean AUC scores for each classifier
AUC_scores = {}
for classifier in data.keys():
    AUC_scores[classifier] = 0
    temp_scores = []
    for type in data[classifier].keys():
        temp_scores.append(np.mean(data[classifier][type][3]))
    AUC_scores[classifier] = np.mean(temp_scores)
print(AUC_scores)

plt.figure(figsize=(10, 11))
plt.title("Mean AUC scores for each classifier")
plt.xlabel("Classifier")
plt.ylabel("Mean AUC score")
plt.ylim(0, 1.0)
plt.xticks(rotation=45)
plt.grid(True)
# sort the AUC scores from highest to lowest
sorted_AUC_scores = sorted(AUC_scores.items(), key=lambda x: x[1], reverse=True)
# plot the AUC scores
plt.bar(range(len(AUC_scores)), [val[1] for val in sorted_AUC_scores], align='center')
# add classifier names as x labels
plt.xticks(range(len(AUC_scores)), [val[0] for val in sorted_AUC_scores])

# Save the plot in `images/AUC_scores.png`
plt.savefig("images/AUC_scores.png")

# Plot the graph
plt.show()