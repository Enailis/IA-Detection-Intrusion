# Abstract

**TODO !**

# Introduction

This project as in main objectif the comprehension of how IA detection works, in case of attack detection.
More precisely, the project has been split in two parts :

1. How the source data is stored and processed
2. How IA models are trained and used to detect attacks with the processed data

The first part about data processing presents how important it is to have a good data set, and how to process it to
be able to use it in the second part. As challenges showed up, the data processing can be a huge part of the project,
and always impact how good the IA models will be.
Subproject 1 lets us learn about ElasticSearch and how to use it to store and process data. It also lets us learn
about the requests we can do on ElasticSearch, and how to use them to get the data we want.

The second part about the IA models presents how to train and use them to detect attacks. By proposing several models,
we
will see how important is the choice of the model, and how to use it to get the best results.

# Project structure

Our project is split in two subprojects, each one having its own directory. The first one is about the data processing,
and the second one is about the IA models and attack detection.

Each subproject can be used independently.

## Subproject 1: Data processing

This subproject is plotted in multiple files, each one having its own purpose and corresponding to a step of the
project.

### Load data

The first step that we have to do is to load the data into our ElasticSearch database. To do so, we have to use the file
`import_data.py`. For a more practical use, we have chosen to place our ElasticSearch database on a private server.
This alloys us to only have one database for both of us. It also allowed us to avoid some problems with the RAM, as we
don't have to load the database on our own computer.

In the file, we start by defining the ElasticSearch object, with providing some information about the database.

```python
es = Elasticsearch("https://tdelastic:9200", verify_certs=False, request_timeout=1000000,
                   basic_auth=(LOGIN, PASSWORD))
```

After that, we are able to discuss with the database.

To talk a bit about the data them self, we use multiple `.xml` file that have been generated (from the packet files (
pcap)) using IBM QRadar appliance. These files are composed of multiple flows, each one corresponding to a network
connection. These flows are related to different protocols, and have different attributes. To give an example, a flow
looks like this :

```xml

<TestbedMonJun14Flows>
    <appName>Unknown_UDP</appName>
    <totalSourceBytes>16076</totalSourceBytes>
    <totalDestinationBytes>0</totalDestinationBytes>
    <totalDestinationPackets>0</totalDestinationPackets>
    <totalSourcePackets>178</totalSourcePackets>
    <sourcePayloadAsBase64></sourcePayloadAsBase64>
    <destinationPayloadAsBase64></destinationPayloadAsBase64>
    <destinationPayloadAsUTF></destinationPayloadAsUTF>
    <direction>L2R</direction>
    <sourceTCPFlagsDescription>N/A</sourceTCPFlagsDescription>
    <destinationTCPFlagsDescription>N/A</destinationTCPFlagsDescription>
    <source>192.168.5.122</source>
    <protocolName>udp_ip</protocolName>
    <sourcePort>5353</sourcePort>
    <destination>224.0.0.251</destination>
    <destinationPort>5353</destinationPort>
    <startDateTime>2010-06-13T23:57:19</startDateTime>
    <stopDateTime>2010-06-14T00:11:23</stopDateTime>
    <Tag>Normal</Tag>
</TestbedMonJun14Flows>
```

One of the most important attributes is the `Tag` one. It is used to know if the flow is an attack or not. If it is an
attack, the value will be `Attack`, otherwise it will be `Normal`.

So our second step is to load the data into the database. To do so, we have parsed one by one each `.xml` file, and
inserted the flows into the database. To do so, we have used the `bulk` function of ElasticSearch. This function allows
us to insert multiple data at once, and is way faster than inserting one by one the data.

```python
success, failed = bulk(es, dictionnaries, index="ia-detection-intrusion")
```

To clarify, we have stored the data in the `ia-detection-intrusion` index. So all the data are stored in the same index.
This is not a problem, as we can use filters to get the data we want.

### Design an API

One of the parts of the project is to design an API to get the data we want from the ElasticSearch database.

To do so, we have chosen to place all the API functions into the `functions.py` file. This file contains, also like
the `import_data.py` file, an ElasticSearch object, to be able to discuss with the database, and more precisely with
the `ia-detection-intrusion` index.

All the functions are using the `search` function of ElasticSearch. This function allows us to get the data we want
using filters. For example, if we want to get all the data that have the `Tag` attribute equal to `Attack`, we can use
the following filter :

```python
body = {
    "query": {
        "match": {
            "Tag": "Attack"
        }
    }
}
```

This filter will be used in the `search` function, and will return all the data that have the `Tag` attribute equal to
`Attack`.

One of the biggest challenges of this part was to find the right filters to get the data we want and this without the
limitation of size of the data. Indeed, ElasticSearch has a limitation of 10 000 data returned by request. To avoid this
limitation, we have used the `scroll` function of ElasticSearch. This function allows us to get all the data we want,
without any limitation.

### Data visualization

In the subject, we have been asked to visualize the data we have in the database. We have stored the code into the
`flows_packets_draw.py` files.

To do that, we have request our database with the following filter :

```python
query = {
    "size": 0,
    "aggs": {
        "packet_number": {
            "terms": {
                "script": {
                    "source": "doc['totalDestinationPackets'].value + doc['totalSourcePackets'].value",
                    "lang": "painless"
                },
                "size": 10000
            }
        }
    }
}
```

This filter will return all the data we have in the database, but only the `totalDestinationPackets` and
`totalSourcePackets` attributes. These attributes are the number of packets that have been sent and received by the
source and the destination of the flow. We have chosen to sum these two attributes to get the total number of packets
that have been sent and received by the source and the destination of the flow.

After this, we had simply to plot the data we have got.

![Number of flow in function of their packets number](../sub-project-1/plot/myplot.png)
![Number of flow in function of their packets number with log](../sub-project-1/plot/myplot2.png)

As you can see, the first plot is not really readable because of the huge number of flows that have a low number of
packets. To avoid this, we have plotted the same data, but with a logarithmic scale. This plot is way more readable, and
we can see that the majority of the flows have a low number of packets.

To interpret this, it is important to know that the flows are related to different protocols. Some protocols are
sending a lot of packets, and some others are sending only a few packets. This is why we have a lot of flows with a low
number of packets. But the huge spike at the beginning of the plot is not normal. Indeed, we can see that we have a lot
of flows with only one packet. This is not normal, and is probably due to a problem with the data.

## Subproject 2: IA models and attack detection

As announced in the introduction, this subproject is about the IA models and attack detection. All the file related to
this subproject are in the `sub-project-2` directory.

### Preparing the classification tasks

The first task that we have to do is to prepare the data for the classification tasks. To do so, we have used two
different
files.

**The first one** is the `import_data.py` file, that we have already used in the first subproject.
But we still made some changes to it.
To gain some time, we have chosen to directly used `.xml` files instead of using our ElasticSearch database.
So now, this file only provides us the function `get_dictionnaries()` that returns the content of the `.xml`.

**The second file** is the `split_data.py` file. This file provides us three functions :

- `split_data()` that split the data into 4 `appName` categories (HTTPWeb, SSH, SMTP and FTP). This function also split
  each category into five parts (talked about this later).
- `serialize()` that serialize the data into a `dictionnariesByAppNameSplitted.pickle` file. This file is used to
  load more quickly the data and prevent us to have to load and split the data each time we want to use them.
- `get_pickle_file()`that returns the content of the `dictionnariesByAppNameSplitted.pickle` file.

To speak a bit more about the `split_data()` function, we are splitting the data into five parts to be able to use the
cross-validation method.
This method is used to train and test our models.
To do so, we are using four parts to train the models, and the last one to test them.
We are doing this five times, and each time we are using a different part to test the models.
This allows us to have a better idea of how good our models are.

![Image from https://medium.com/@gulcanogundur/model-se%C3%A7imi-k-fold-cross-validation-4635b61f143c](images/1_dldTNMhgjNNeu7d0OmNPCA.png)

### Classification Models

In this second task, we have to train and test different classification models. More precisely, 4 models :

- K-Nearest Neighbors classifier
- Naive Bayes classifier
- Random Forest classifier
- Multi-layer Perceptron classifier

To do so, we have choosen to use a file for each model. Each file contains the code to train and test the model. The
results are then printed in the console.

For each model, we globally have the same code.
We start by loading the data using the `get_pickle_file()` function from the `split_data.py` file.
After that, we are making a loop to train and test on each `appName` category.
And for each category, we are making a loop to train and test on each part of the data.

For each part, we are selecting the data we want to use to train and test the model.
Training data are pop() from the data, and testing data are the remaining data.
After that, we are applying some transformations to the data.
For example, we are using the `LabelEncoder()` function to transform all non `int` attribute into a number.
This is necessary to be able to use the data in the models.
Next, we are using the `SimpleImputer()` function to replace all `NaN` values by the mean of the column.
This is also necessary to be able to use the data in the models.
Finally, we are creating the model, and training it with the training data (with the function `fit()` of the model).

The model is now trained, and we can use it to predict the testing data.
To do so, we are using the `predict()` function of the model.
This function returns a list of predictions.
We are then comparing these predictions with the real values of the testing data, and calculating the accuracy of the
model.

Because we are using the cross-validation method, we are doing this five times per appName category.
And after that, we make the means of the accuracy of the five tests.
This allows us to have a better idea of how good our models are.

### Model evaluation and comparison

Now that we have trained and tested our models, we have to evaluate and compare them.

#### KNN

```plaintext
Accuracy scores :
[+] HTTPWeb
 ╰─ Mean : 98.93600399415638
 ╰─ Median : 98.9570130424754
 ╰─ Mean Precision : 0.497512398499892
 ╰─ Mean ROC AUC : 0.497932444876514
[+] SSH
 ╰─ Mean : 64.09715573286715
 ╰─ Median : 64.62549954879464
 ╰─ Mean Precision : 0.5722680190618965
 ╰─ Mean ROC AUC : 0.5829875879836963
[+] SMTP
 ╰─ Mean : 98.86316420445621
 ╰─ Median : 98.83902269970542
 ╰─ Mean Precision : 0.494796009010065
 ╰─ Mean ROC AUC : 0.4995096749777563
[+] FTP
 ╰─ Mean : 97.13023992874685
 ╰─ Median : 97.11938546890003
 ╰─ Mean Precision : 0.579660677009638
 ╰─ Mean ROC AUC : 0.6693818115293796
```

#### Naive Bayes

```plaintext
Results :
[+] HTTPWeb
 ╰─ Mean Accuracy: 99.41664063165945
 ╰─ Median Accuracy : 99.416047392196
 ╰─ Mean Precision : 0.49708320315829724
 ╰─ Mean ROC AUC : 0.5
[+] SSH
 ╰─ Mean Accuracy: 26.544304651042758
 ╰─ Median Accuracy : 26.4535258476215
 ╰─ Mean Precision : 0.13272152325521383
 ╰─ Mean ROC AUC : 0.5
[+] SMTP
 ╰─ Mean Accuracy: 98.96021072313098
 ╰─ Median Accuracy : 98.9428076256499
 ╰─ Mean Precision : 0.49480105361565496
 ╰─ Mean ROC AUC : 0.5
[+] FTP
 ╰─ Mean Accuracy: 98.07117853302196
 ╰─ Median Accuracy : 98.06892136989225
 ╰─ Mean Precision : 0.4903558926651098
 ╰─ Mean ROC AUC : 0.5
```

#### Random Forest

```plaintext
Results :
[+] HTTPWeb
 ╰─ Mean Accuracy: 99.3865865862443
 ╰─ Median Accuracy : 99.40211520586831
 ╰─ Mean Precision : 0.49982340311876444
 ╰─ Mean ROC AUC : 0.5000794844564099
[+] SSH
 ╰─ Mean Accuracy: 98.46333541413235
 ╰─ Median Accuracy : 99.81954111884507
 ╰─ Mean Precision : 0.989730836268744
 ╰─ Mean ROC AUC : 0.9722444199826665
[+] SMTP
 ╰─ Mean Accuracy: 99.67073760003026
 ╰─ Median Accuracy : 99.63604852686309
 ╰─ Mean Precision : 0.9873358805098771
 ╰─ Mean ROC AUC : 0.8554693348473735
[+] FTP
 ╰─ Mean Accuracy: 99.89331990568627
 ╰─ Median Accuracy : 99.91465756347344
 ╰─ Mean Precision : 0.9895174575111664
 ╰─ Mean ROC AUC : 0.9820131190167954
```

#### MLP

```plaintext
Results :
[+] HTTPWeb
 ╰─ Mean Accuracy: 99.4155901107381
 ╰─ Median Accuracy : 99.416047392196
 ╰─ Mean Precision : 0.49708317296381316
 ╰─ Mean ROC AUC : 0.4999947170279377
[+] SSH
 ╰─ Mean Accuracy: 94.11406135243028
 ╰─ Median Accuracy : 96.0041247744264
 ╰─ Mean Precision : 0.9456602456887089
 ╰─ Mean ROC AUC : 0.9065492485365457
[+] SMTP
 ╰─ Mean Accuracy: 95.03301483212392
 ╰─ Median Accuracy : 97.157712305026
 ╰─ Mean Precision : 0.5654041466829387
 ╰─ Mean ROC AUC : 0.612705936370572
[+] FTP
 ╰─ Mean Accuracy: 98.22906135771093
 ╰─ Median Accuracy : 98.14360396884668
 ╰─ Mean Precision : 0.7148723512698955
 ╰─ Mean ROC AUC : 0.6099666125328862
```

#### Global

How we can see, only the Random Forest classifier is able to detect attacks with a good accuracy.
The other models are at random because they have a ROC AUC very close to 0.5.
That means theses models are randomly classifying the data.

![Graph of the average AUC per model](../sub-project-2/images/AUC_scores.png)

# Evaluation

# Conclusion

# Appendix 1: User's Manual

# Appendix 2: Licensed code
