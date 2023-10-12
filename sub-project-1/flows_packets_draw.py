import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from matplotlib import pyplot as plt


def get_all_packet_data(es, index_name):
    """
    Récupère toutes les données du nombre de paquets de destination et de source pour chaque entrée.

    :param es: Instance de connexion Elasticsearch.
    :param index_name: Nom de l'index Elasticsearch contenant les données de logs.
    :return: Une liste de tuples, chaque tuple contenant le nombre de paquets de destination et de source.
    """
    packet_data = []
    page_size = 10000  # Taille de chaque page
    scroll_time = "1m"  # Durée de conservation de la recherche de défilement (1 minute)

    query = {
        "size": page_size,
    }

    result = es.search(index=index_name, body=query, scroll=scroll_time)
    scroll_id = result.get("_scroll_id")
    total_hits = result.get("hits", {}).get("total", {}).get("value", 0)
    hits = result.get("hits", {}).get("hits", [])

    packet_data.extend(hits)

    while len(packet_data) < total_hits:
        result = es.scroll(scroll_id=scroll_id, scroll=scroll_time)
        hits = result.get("hits", {}).get("hits", [])
        packet_data.extend(hits)

    return packet_data


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
    packet_data = get_all_packet_data(es, index_name)

    # Extraire les données de paquets de destination et source
    packet_number = []
    for element in packet_data:
        source_packets = element.get("_source", {}).get("totalSourcePackets")
        destination_packets = element.get("_source", {}).get("totalDestinationPackets")
        # average number of packets
        avg_packets = (source_packets + destination_packets) / 2
        packet_number.append(avg_packets)

    # Get the highest number of packets
    max_packets = max(packet_number)

    # Create a dictionary with the number of packets as key and the number of occurences as value
    packet_number_dict = {}
    for i in range(0, int(max_packets)):
        packet_number_dict[i] = 0

    for packet in packet_number:
        packet_number_dict[int(packet)] += 1

    # create an histogram with the number of packets as x-axis and the number of occurences as y-axis
    plt.figure(figsize=(10, 6))
    plt.bar(packet_number_dict.keys(), packet_number_dict.values(), color='g')
    plt.title("Histogramme du Nombre de Paquets")
    plt.xlabel("Nombre de Paquets")
    plt.ylabel("Nombre d'Occurences")
    plt.grid(True)
    plt.show()
