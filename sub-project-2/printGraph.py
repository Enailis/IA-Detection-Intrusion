import matplotlib.pyplot as plt
import numpy as np

data = {
    "KNN": {
        "httpweb": [98.936, 98.957, 0.498, 0.498],
        "ssh": [64.097, 64.625, 0.572, 0.583],
        "SMTP": [98.863, 98.839, 0.495, 0.500],
        "FTP": [97.130, 97.119, 0.580, 0.670],
    },
    "Naive Bayes": {
        "httpweb": [99.416, 99.416, 0.497, 0.500],
        "ssh": [26.544, 26.454, 0.133, 0.500],
        "SMTP": [98.960, 98.943, 0.495, 0.500],
        "FTP": [98.071, 98.069, 0.490, 0.500],
    },
    "Random Forest": {
        "httpweb": [99.386, 99.402, 0.500, 0.500],
        "ssh": [98.463, 99.820, 0.990, 0.972],
        "SMTP": [99.671, 99.636, 0.987, 0.855],
        "FTP": [99.893, 99.915, 0.990, 0.982],
    },
    "MLPC": {
        "httpweb": [99.416, 99.416, 0.497, 0.500],
        "ssh": [94.114, 96.004, 0.946, 0.907],
        "SMTP": [95.033, 97.158, 0.565, 0.613],
        "FTP": [98.229, 98.144, 0.715, 0.610],
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