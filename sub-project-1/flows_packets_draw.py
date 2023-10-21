import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from matplotlib import pyplot as plt


def get_flow_par_packet_table(es, index_name):
    # Get the number of occurence of each packet number (the packet number is the sum of the "totalDestinationPackets"
    # and "totalSourcePackets" fields)

    # Create a query to get the number of occurence of each packet number
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

    # Execute the query
    res = es.search(index=index_name, body=query)
    return res


# Exemple d'utilisation
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")

    # Create ElasticSearch object
    print("[+] Connecting to ElasticSearch")
    es = Elasticsearch("https://tdelastic:9200", verify_certs=False, request_timeout=1000000,
                       basic_auth=(LOGIN, PASSWORD))
    index_name = os.getenv("INDEX_NAME")

    print("[+] Getting all packet data")
    packet_data = get_flow_par_packet_table(es, index_name).get("aggregations", {}).get("packet_number", {}).get(
        "buckets", {})
    print("[+] Done")

    # Create a list of packet number and a list of occurence
    packet_number = []
    occurence = []
    for packet in packet_data:
        packet_number.append(packet.get("key"))
        occurence.append(packet.get("doc_count"))

    # Plot histogram of the number of occurence of each packet number
    # limit the y axis to the highest number of occurence
    plt.bar(packet_number, occurence)
    plt.ylim(0, max(occurence))
    plt.xlabel("Packet number")
    plt.ylabel("Occurence")
    plt.title("Number of occurence of each packet number")
    plt.show()

    # Plot histogram of the number of occurence of each packet number (log scale)
    plt.bar(packet_number, occurence)
    plt.xlabel("Packet number")
    plt.ylabel("Occurence")
    plt.title("Number of occurence of each packet number (log scale)")
    plt.yscale("log")
    plt.show()

    # Statistics
    print("Statistics:")
    print("Number of packet number: {}".format(len(packet_number)))
    print("Max number of occurence: {}".format(max(occurence)))
    print("Min number of occurence: {}".format(min(occurence)))