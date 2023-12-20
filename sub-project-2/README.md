# Sub-project 2

## Installation

Clone project:

```
git clone git@github.com:Enailis/IA-Detection-Intrusion.git
```

Install dependencies:

```
cd IA-Detection-Intrusion/sub-project-2
pip install -r requirements.txt
```

Create a folder called `TRAIN_ENSIBS` and put every `.xml` files required for the training.

You can now execute every python while by using the command `python3 <file.py>`.

## Disclaimer

This project is supposed to get the data pushed to ELK in [sub-project-1](../sub-project-1/README.md) but to gain some
time *(because of the horrible bandwidth of our school)* we decided to serialize the data in a pickle file.

## First data loading

You can use the file `split_data.py` to load the data from the `.xml` files and split them depending on appName.
For each appName category, the data is split into five sub dictionaries.

The data is then saved on `dictionnariesByAppNameSplitted.pickle` to avoid having to load the data every time.
So you only need to create the pickle file once.

This file will be used in the following function to load the data.

## Models training

### KNN

You can use the file `knn.py` to train the KNN model on the data.
The model is trained on one of the five sub dictionaries of the data.
The four others are used to test the model.

The model is using three neighbors.
That means that the model will look at the three closest neighbors to determine the category of the data.

### Naive Bayes

You can use the file `NaiveBayes.py` to train the Naive Bayes model on the data.
The model is trained on one of the five sub dictionaries of the data.
The four others are used to test the model.

### Random Forest

You can use the file `RandomForest.py` to train the Random Forest model on the data.
The model is trained on one of the five sub dictionaries of the data.
The four others are used to test the model.

The model is using 100 trees.

### Multilayer Perceptron classification

You can use the file `MultilayerPerceptron.py` to train the Multilayer Perceptron classification model on the data.
The model is trained on one of the five sub dictionaries of the data.
The four others are used to test the model.

## Data processing

### KNN

```plaintext
Results :
[+] HTTPWeb
 ╰─ Mean Accuracy: 99.83410889052463
 ╰─ Median Accuracy : 99.83191588486238
 ╰─ Mean Precision : 0.9323719879324288
 ╰─ Mean ROC AUC : 0.922938276369142
[+] SSH
 ╰─ Mean Accuracy: 99.98968540484786
 ╰─ Median Accuracy : 100.0
 ╰─ Mean Precision : 0.9998087954110899
 ╰─ Mean ROC AUC : 0.9999294283697953
[+] SMTP
 ╰─ Mean Accuracy: 99.91680147019953
 ╰─ Median Accuracy : 99.93069993069993
 ╰─ Mean Precision : 0.9854343185616259
 ╰─ Mean ROC AUC : 0.9695434652892482
[+] FTP
 ╰─ Mean Accuracy: 99.77809144660078
 ╰─ Median Accuracy : 99.82935153583618
 ╰─ Mean Precision : 0.9692681411015588
 ╰─ Mean ROC AUC : 0.9723742178026145
```

### Naive Bayes

```plaintext
Results :
[+] HTTPWeb
 ╰─ Mean Accuracy: 98.39389110563346
 ╰─ Median Accuracy : 98.67907809516849
 ╰─ Mean Precision : 0.5404557374966396
 ╰─ Mean ROC AUC : 0.5533703016315652
[+] SSH
 ╰─ Mean Accuracy: 75.16756432000766
 ╰─ Median Accuracy : 75.0
 ╰─ Mean Precision : 0.8736756701734437
 ╰─ Mean ROC AUC : 0.5322518895493253
[+] SMTP
 ╰─ Mean Accuracy: 97.69866099963187
 ╰─ Median Accuracy : 97.57449757449757
 ╰─ Mean Precision : 0.656003301540719
 ╰─ Mean ROC AUC : 0.9807490057894134
[+] FTP
 ╰─ Mean Accuracy: 85.35459265053554
 ╰─ Median Accuracy : 85.31796841655996
 ╰─ Mean Precision : 0.5586705979412233
 ╰─ Mean ROC AUC : 0.9253365791167967
```

### Random Forest

```plaintext
Results :
[+] HTTPWeb
 ╰─ Mean Accuracy: 99.99744221326846
 ╰─ Median Accuracy : 99.9981729987485
 ╰─ Mean Precision : 0.9995135659942382
 ╰─ Mean ROC AUC : 0.9982904236198072
[+] SSH
 ╰─ Mean Accuracy: 99.98968540484786
 ╰─ Median Accuracy : 100.0
 ╰─ Mean Precision : 0.9999301675977653
 ╰─ Mean ROC AUC : 0.9998031496062992
[+] SMTP
 ╰─ Mean Accuracy: 99.97226074895977
 ╰─ Median Accuracy : 100.0
 ╰─ Mean Precision : 0.9998598452109688
 ╰─ Mean ROC AUC : 0.9870445344129555
[+] FTP
 ╰─ Mean Accuracy: 100.0
 ╰─ Median Accuracy : 100.0
 ╰─ Mean Precision : 1.0
 ╰─ Mean ROC AUC : 1.0
```

### Multilayer Perceptron classification

```plaintext
Results :
[+] HTTPWeb
 ╰─ Mean Accuracy: 99.41664066669647
 ╰─ Median Accuracy : 99.41262446332328
 ╰─ Mean Precision : 0.4970832033334823
 ╰─ Mean ROC AUC : 0.5
[+] SSH
 ╰─ Mean Accuracy: 92.39975968056656
 ╰─ Median Accuracy : 92.37113402061856
 ╰─ Mean Precision : 0.9496766445957265
 ╰─ Mean ROC AUC : 0.8588010369325156
[+] SMTP
 ╰─ Mean Accuracy: 98.96019138737587
 ╰─ Median Accuracy : 98.8911988911989
 ╰─ Mean Precision : 0.4948009569368793
 ╰─ Mean ROC AUC : 0.5
[+] FTP
 ╰─ Mean Accuracy: 98.1394728907107
 ╰─ Median Accuracy : 98.12286689419795
 ╰─ Mean Precision : 0.6722472823958696
 ╰─ Mean ROC AUC : 0.5427075049301581
```

## Model comparison

Overall, the results seem diverse.
The performances are higher for Random Forest models, indicating a good generalization on the test data.
Naive Bayes models appear to be less effective.
However, it's important to consider other aspects such as class imbalance, sample size, and possibly adjust
hyperparameters to enhance performance

![AUC scores](images/AUC_scores.png)

**Conclusion**:

- Random Forest appears to be the most stable and effective choice among the tested models, with high performance across
  most categories.
- Naive Bayes seems less effective in this configuration.
- KNN exhibits variable performance across
  categories.
- Multilayer Perceptron shows competitive performance but with some variability
