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

![Number of flow in function of their packets number](sub-project-1/plot/myplot.png)
![Number of flow in function of their packets number with log](sub-project-1/plot/myplot2.png)

As you can see, the first plot is not really readable because of the huge number of flows that have a low number of
packets. To avoid this, we have plotted the same data, but with a logarithmic scale. This plot is way more readable, and
we can see that the majority of the flows have a low number of packets.

To interpret this, it is important to know that the flows are related to different protocols. Some protocols are
sending a lot of packets, and some others are sending only a few packets. This is why we have a lot of flows with a low
number of packets. But the huge spike at the beginning of the plot is not normal. Indeed, we can see that we have a lot
of flows with only one packet. This is not normal, and is probably due to a problem with the data.

## Subproject 2: IA models and attack detection

# Evaluation

# Conclusion

# Appendix 1: User's Manual

# Appendix 2: Licensed code
