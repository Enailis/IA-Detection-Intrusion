import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from tabulate import tabulate


def get_distinct_protocols(es, index_name, ):
    # Requête Elasticsearch pour récupérer la liste distincte des protocoles
    query = {
        "size": 0,
        "aggs": {
            "distinct_protocols": {
                "terms": {
                    "field": "protocolName.keyword",
                    # Assurez-vous d'utiliser le champ keyword pour des termes non analysés
                    "size": 10000  # Le nombre maximum de protocoles distincts à récupérer
                }
            }
        }
    }

    # Exécutez la requête
    result = es.search(index=index_name, body=query)

    # Récupérez les protocoles distincts à partir des résultats
    distinct_protocols = [(bucket["key"], bucket["doc_count"]) for bucket in
                          result["aggregations"]["distinct_protocols"]["buckets"]]

    return distinct_protocols


def get_element_from_protocol(es, index_name, protocol):
    query = {
        "size": 10000,
        "query": {
            "term": {
                "protocolName.keyword": protocol,
            }
        }
    }

    result = es.search(index=index_name, body=query)
    hits = result.get("hits", {}).get("hits", [])

    # return the list of elements
    hits = [hit["_source"] for hit in hits]

    return hits


def get_element_count_from_protocol(es, index_name, protocol):
    hits = get_element_from_protocol(es, index_name, protocol)

    return len(hits)


def get_avg_payload_from_protocol(es, index_name, protocol):
    # Récupérer la liste des éléments
    hits = get_element_from_protocol(es, index_name, protocol)

    # Initialiser les compteurs et les totaux
    source_payload_size_total = 0
    destination_payload_size_total = 0
    source_payload_count = 0
    destination_payload_count = 0

    for hit in hits:
        source_payload = hit.get("sourcePayloadAsBase64", "")
        destination_payload = hit.get("destinationPayloadAsBase64", "")

        # Vérifier si le payload source n'est pas vide
        if source_payload:
            source_payload_size_total += len(source_payload)
            source_payload_count += 1

        # Vérifier si le payload destination n'est pas vide
        if destination_payload:
            destination_payload_size_total += len(destination_payload)
            destination_payload_count += 1

    # Calculer les moyennes
    avr_source_payload_size = source_payload_size_total / max(source_payload_count, 1)
    avr_destination_payload_size = destination_payload_size_total / max(destination_payload_count, 1)

    return avr_source_payload_size, avr_destination_payload_size


def get_total_bytes_by_protocol(es, index_name):
    """
    Récupère le total de "totalDestinationBytes" et "totalSourceBytes" par protocole.

    :param es: Instance de connexion Elasticsearch.
    :param index_name: Nom de l'index Elasticsearch contenant les données de logs.
    :return: Un dictionnaire où les clés sont les protocoles et les valeurs sont les totaux de "totalDestinationBytes" et "totalSourceBytes".
    """
    query = {
        "size": 0,
        "aggs": {
            "protocols": {
                "terms": {
                    "field": "protocolName.keyword",
                    "size": 10000  # Le nombre maximum de protocoles distincts
                },
                "aggs": {
                    "total_destination_bytes": {
                        "sum": {
                            "field": "totalDestinationBytes"
                        }
                    },
                    "total_source_bytes": {
                        "sum": {
                            "field": "totalSourceBytes"
                        }
                    }
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    total_bytes_by_protocol = {}
    protocol_buckets = result.get("aggregations", {}).get("protocols", {}).get("buckets", [])

    for bucket in protocol_buckets:
        protocol_name = bucket.get("key", "N/A")
        total_destination_bytes = bucket.get("total_destination_bytes", {}).get("value", 0)
        total_source_bytes = bucket.get("total_source_bytes", {}).get("value", 0)
        total_bytes_by_protocol[protocol_name] = {
            "totalDestinationBytes": total_destination_bytes,
            "totalSourceBytes": total_source_bytes
        }

    return total_bytes_by_protocol


def get_total_packets_by_protocol(es, index_name):
    """
    Récupère le total de "totalDestinationPackets" et "totalSourcePackets" par protocole.

    :param es: Instance de connexion Elasticsearch.
    :param index_name: Nom de l'index Elasticsearch contenant les données de logs.
    :return: Un dictionnaire où les clés sont les protocoles et les valeurs sont les totaux de "totalDestinationPackets" et "totalSourcePackets".
    """
    query = {
        "size": 0,
        "aggs": {
            "protocols": {
                "terms": {
                    "field": "protocolName.keyword",
                    "size": 10000  # Le nombre maximum de protocoles distincts
                },
                "aggs": {
                    "total_destination_packets": {
                        "sum": {
                            "field": "totalDestinationPackets"
                        }
                    },
                    "total_source_packets": {
                        "sum": {
                            "field": "totalSourcePackets"
                        }
                    }
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    total_packets_by_protocol = {}
    protocol_buckets = result.get("aggregations", {}).get("protocols", {}).get("buckets", [])

    for bucket in protocol_buckets:
        protocol_name = bucket.get("key", "N/A")
        total_destination_packets = bucket.get("total_destination_packets", {}).get("value", 0)
        total_source_packets = bucket.get("total_source_packets", {}).get("value", 0)
        total_packets_by_protocol[protocol_name] = {
            "totalDestinationPackets": total_destination_packets,
            "totalSourcePackets": total_source_packets
        }

    return total_packets_by_protocol


def get_distinct_app_names(es, index_name):
    """
    Récupère la liste des "appName" distincts.

    :param es: Instance de connexion Elasticsearch.
    :param index_name: Nom de l'index Elasticsearch contenant les données de logs.
    :return: Liste des "appName" distincts.
    """
    query = {
        "size": 0,
        "aggs": {
            "distinct_app_names": {
                "terms": {
                    "field": "appName.keyword",  # Assurez-vous d'utiliser le champ keyword pour des termes non analysés
                    "size": 10000  # Le nombre maximum d'appNames distincts à récupérer
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    distinct_app_names = [bucket["key"] for bucket in result["aggregations"]["distinct_app_names"]["buckets"]]

    return distinct_app_names


def get_entries_by_app_name(es, index_name, app_name):
    """
    Récupère la liste de toutes les entrées pour un "appName" donné en utilisant la pagination.

    :param es: Instance de connexion Elasticsearch.
    :param index_name: Nom de l'index Elasticsearch contenant les données de logs.
    :param app_name: Nom de l'application à rechercher.
    :return: Liste de toutes les entrées correspondant à l'application donnée.
    """
    page_size = 1000  # Taille de chaque page
    scroll_time = "1m"  # Durée de conservation de la recherche de défilement (1 minute)
    entries = []

    # Requête de recherche initiale avec pagination
    query = {
        "size": page_size,
        "query": {
            "term": {
                "appName.keyword": app_name
            }
        }
    }

    result = es.search(index=index_name, body=query, scroll=scroll_time)
    scroll_id = result.get("_scroll_id")
    total_hits = result.get("hits", {}).get("total", {}).get("value", 0)
    hits = result.get("hits", {}).get("hits", [])

    entries.extend(hits)

    while len(entries) < total_hits:
        # Récupération des résultats de la page suivante
        result = es.scroll(scroll_id=scroll_id, scroll=scroll_time)
        hits = result.get("hits", {}).get("hits", [])
        entries.extend(hits)

    return entries


def get_entries_count_by_app_name(es, index_name, app_name):
    hits = get_entries_by_app_name(es, index_name, app_name)

    return len(hits)


def get_avg_payload_by_app_name(es, index_name, appName):
    # Récupérer la liste des éléments
    hits = get_entries_by_app_name(es, index_name, appName)

    # Initialiser les compteurs et les totaux
    source_payload_size_total = 0
    destination_payload_size_total = 0
    source_payload_count = 0
    destination_payload_count = 0

    for hit in hits:
        source_payload = hit.get("sourcePayloadAsBase64", "")
        destination_payload = hit.get("destinationPayloadAsBase64", "")

        # Vérifier si le payload source n'est pas vide
        if source_payload:
            source_payload_size_total += len(source_payload)
            source_payload_count += 1

        # Vérifier si le payload destination n'est pas vide
        if destination_payload:
            destination_payload_size_total += len(destination_payload)
            destination_payload_count += 1

    # Calculer les moyennes
    avr_source_payload_size = source_payload_size_total / max(source_payload_count, 1)
    avr_destination_payload_size = destination_payload_size_total / max(destination_payload_count, 1)

    return avr_source_payload_size, avr_destination_payload_size


def get_total_bytes_by_app_name(es, index_name):
    """
    Récupère le total de "totalDestinationBytes" et "totalSourceBytes" par appName.

    :param es: Instance de connexion Elasticsearch.
    :param index_name: Nom de l'index Elasticsearch contenant les données de logs.
    :return: Un dictionnaire où les clés sont les applications et les valeurs sont les totaux de "totalDestinationBytes" et "totalSourceBytes".
    """
    query = {
        "size": 0,
        "aggs": {
            "protocols": {
                "terms": {
                    "field": "appName.keyword",
                    "size": 10000  # Le nombre maximum de appName distincts
                },
                "aggs": {
                    "total_destination_bytes": {
                        "sum": {
                            "field": "totalDestinationBytes"
                        }
                    },
                    "total_source_bytes": {
                        "sum": {
                            "field": "totalSourceBytes"
                        }
                    }
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    total_bytes_by_protocol = {}
    protocol_buckets = result.get("aggregations", {}).get("protocols", {}).get("buckets", [])

    for bucket in protocol_buckets:
        protocol_name = bucket.get("key", "N/A")
        total_destination_bytes = bucket.get("total_destination_bytes", {}).get("value", 0)
        total_source_bytes = bucket.get("total_source_bytes", {}).get("value", 0)
        total_bytes_by_protocol[protocol_name] = {
            "totalDestinationBytes": total_destination_bytes,
            "totalSourceBytes": total_source_bytes
        }

    return total_bytes_by_protocol


def get_total_packets_by_app_name(es, index_name):
    """
    Récupère le total de "totalDestinationPackets" et "totalSourcePackets" par appName.

    :param es: Instance de connexion Elasticsearch.
    :param index_name: Nom de l'index Elasticsearch contenant les données de logs.
    :return: Un dictionnaire où les clés sont les applications et les valeurs sont les totaux de "totalDestinationPackets" et "totalSourcePackets".
    """
    query = {
        "size": 0,
        "aggs": {
            "protocols": {
                "terms": {
                    "field": "appName.keyword",
                    "size": 10000  # Le nombre maximum d'applications distinct
                },
                "aggs": {
                    "total_destination_packets": {
                        "sum": {
                            "field": "totalDestinationPackets"
                        }
                    },
                    "total_source_packets": {
                        "sum": {
                            "field": "totalSourcePackets"
                        }
                    }
                }
            }
        }
    }

    result = es.search(index=index_name, body=query)

    total_packets_by_protocol = {}
    protocol_buckets = result.get("aggregations", {}).get("protocols", {}).get("buckets", [])

    for bucket in protocol_buckets:
        protocol_name = bucket.get("key", "N/A")
        total_destination_packets = bucket.get("total_destination_packets", {}).get("value", 0)
        total_source_packets = bucket.get("total_source_packets", {}).get("value", 0)
        total_packets_by_protocol[protocol_name] = {
            "totalDestinationPackets": total_destination_packets,
            "totalSourcePackets": total_source_packets
        }

    return total_packets_by_protocol


if __name__ == '__main__':
    # Load environment variables
    load_dotenv()
    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")

    es = Elasticsearch("https://tdelastic:9200", verify_certs=False, request_timeout=1000000,
                       basic_auth=(LOGIN, PASSWORD))

    # Spécifiez l'index Elasticsearch contenant vos données de logs
    index_name = os.getenv("INDEX_NAME")

    # 1 - Récupérez la liste distincte des protocoles ##################################################################
    print(" 1 - Récupérez la liste distincte des protocoles")
    distinct_protocols = get_distinct_protocols(es, index_name)

    # Affichez la liste distincte des protocoles dans un tableau
    table_headers = ["Protocole", "Nombre"]
    table_data = distinct_protocols

    # Utilisez tabulate pour afficher le tableau
    table = tabulate(table_data, headers=table_headers, tablefmt="pretty")
    print(table)

    # 2 - Récupérez la liste distincte des éléments d'un protocole #####################################################
    print(" 2 - Récupérez la liste distincte des éléments d'un protocole")
    protocol_to_search = "ip"

    # Récupérez les éléments du protocole
    elements = get_element_from_protocol(es, index_name, protocol_to_search)
    print(elements)

    # 3 - Récupérez le nombre d'éléments d'un protocole ################################################################
    print(" 3 - Récupérez le nombre d'éléments d'un protocole")
    protocol_to_search = "ip"
    elements = get_element_count_from_protocol(es, index_name, protocol_to_search)
    print(elements)

    # 4 - Récupérez le moyen de payload source et destination pour un protocole #######################################
    print(" 4 - Récupérez le moyen de payload source et destination pour un protocole")
    protocol_to_search = "ip"
    avr_source_payload_size, avr_destination_payload_size = get_avg_payload_from_protocol(es, index_name,
                                                                                          protocol_to_search)
    print("Average source payload size: {}".format(avr_source_payload_size))
    print("Average destination payload size: {}".format(avr_destination_payload_size))

    # 5 - Récupérez le total de "totalDestinationBytes" et "totalSourceBytes" par protocole ############################
    print(" 5 - Récupérez le total de \"totalDestinationBytes\" et \"totalSourceBytes\" par protocole")
    total_bytes_by_protocol = get_total_bytes_by_protocol(es, index_name)
    if total_bytes_by_protocol:
        for protocol, data in total_bytes_by_protocol.items():
            print(f"Protocole: {protocol}")
            print(f"Total de Destination Bytes: {data['totalDestinationBytes']}")
            print(f"Total de Source Bytes: {data['totalSourceBytes']}")
            print()
    else:
        print("Aucune donnée trouvée.")

    # 6 - Récupérez le total de "totalDestinationPackets" et "totalSourcePackets" par protocole ########################
    print(" 6 - Récupérez le total de \"totalDestinationPackets\" et \"totalSourcePackets\" par protocole")
    total_packets = get_total_packets_by_protocol(es, index_name)

    if total_packets:
        for protocol, data in total_packets.items():
            print(f"Protocole: {protocol}")
            print(f"Total de Destination Packets: {data['totalDestinationPackets']}")
            print(f"Total de Source Packets: {data['totalSourcePackets']}")
            print()
    else:
        print("Aucune donnée trouvée.")

    # 7 - Récupérez la liste distincte des "appName" ###################################################################
    print(" 7 - Récupérez la liste distincte des \"appName\"")
    app_names = get_distinct_app_names(es, index_name)

    if app_names:
        print("Liste des appName distincts:")
        for app_name in app_names:
            print(app_name)
    else:
        print("Aucun appName distinct trouvé.")

    # 8 - Récupérez les entrées pour un "appName" donné ################################################################
    print(" 8 - Récupérez les entrées pour un \"appName\" donné")
    # app_name_to_search = "NetBIOS-IP"  # Remplacez par le nom de l'application spécifique que vous recherchez

    # entries = get_entries_by_app_name(es, index_name, app_name_to_search)
    #
    # if entries:
    #     print(f"Entrées pour l'application '{app_name_to_search}':")
    #     for entry in entries:
    #         print(entry["_source"])
    # else:
    #     print(f"Aucune entrée trouvée pour l'application '{app_name_to_search}'.")

    # 9 - Récupérez le nombre d'entrées pour un "appName" donné #######################################################
    # print(" 9 - Récupérez le nombre d'entrées pour un \"appName\" donné")
    # app_name_to_search = "NetBIOS-IP"  # Remplacez par le nom de l'application spécifique que vous recherchez
    #
    # entries_count = get_entries_count_by_app_name(es, index_name, app_name_to_search)
    # print(f"Nombre d'entrées pour l'application '{app_name_to_search}': {entries_count}")

    # 10 - Récupérez la taille moyenne des "destinationPayloadAsBase64" et "sourcePayloadAsBase64" pour chaque "appName"
    # print(
    #     "10 - Récupérez la taille moyenne des \"destinationPayloadAsBase64\" et \"sourcePayloadAsBase64\" pour chaque "
    #     "\"appName\"")
    # avr_source_payload_size, avr_destination_payload_size = get_avg_payload_by_app_name(es, index_name,
    #                                                                                     "WindowsFileSharing")
    # print("Average source payload size: {}".format(avr_source_payload_size))
    # print("Average destination payload size: {}".format(avr_destination_payload_size))

    # 11 - Récupérez le total de "totalDestinationBytes" et "totalSourceBytes" par appName ##############################
    print("11 - Récupérez le total de \"totalDestinationBytes\" et \"totalSourceBytes\" par appName")
    total_bytes_by_app_name = get_total_bytes_by_app_name(es, index_name)

    if total_bytes_by_app_name:
        for app_name, data in total_bytes_by_app_name.items():
            print(f"Application: {app_name}")
            print(f"Total de Destination Bytes: {data['totalDestinationBytes']}")
            print(f"Total de Source Bytes: {data['totalSourceBytes']}")
            print()
    else:
        print("Aucune donnée trouvée.")

    # 12 - Récupérez le total de "totalDestinationPackets" et "totalSourcePackets" par appName ##########################
    print("12 - Récupérez le total de \"totalDestinationPackets\" et \"totalSourcePackets\" par appName")
    total_packets_by_app_name = get_total_packets_by_app_name(es, index_name)

    if total_packets_by_app_name:
        for app_name, data in total_packets_by_app_name.items():
            print(f"Application: {app_name}")
            print(f"Total de Destination Packets: {data['totalDestinationPackets']}")
            print(f"Total de Source Packets: {data['totalSourcePackets']}")
            print()
    else:
        print("Aucune donnée trouvée.")
