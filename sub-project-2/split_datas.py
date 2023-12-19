import base64
import hashlib
import pickle
from datetime import datetime

import numpy as np
import pandas
import pandas as pd

from import_datas import get_dictionnaries


def split_datas(main_dataframe: pandas.DataFrame):
    print("[+] Splitting datas")
    # Subdivided the dictionaries according to the appName
    appNames = ["HTTPWeb", "SSH", "SMTP", "FTP"]

    # Split the main dataframe into appNames dataframes
    dictionnariesByAppName = {}
    for appName in appNames:
        df = main_dataframe[main_dataframe["appName"] == appName]
        dictionnariesByAppName[appName] = df.to_dict(orient="records")

    # Split each dataframe into 5 parts S1, S2, S3, S4, S5 using pandas
    dictionnariesByAppNameSplitted = {}
    for appName in appNames:
        df = pandas.DataFrame(dictionnariesByAppName[appName])

        # Shuffle the dataframe
        df = df.sample(frac=1, random_state=42)

        df = np.array_split(df, 5)
        dictionnariesByAppNameSplitted[appName] = df

    print("\n[+] Success")
    print(" ╰─ " + "Dicts splitted into 5 parts")

    return dictionnariesByAppNameSplitted


def transform_IP(ip: str):
    # Transform an IP address into a 32 bits integer
    ip = ip.split('.')
    ip = [int(i) for i in ip]
    ip = ip[0] * 256 ** 3 + ip[1] * 256 ** 2 + ip[2] * 256 + ip[3]
    return ip


def transform_date(date: str):
    # Transform date like yyyy-mm-ddThh:mm:ss into a timestamp
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    timestamp = int(dt.timestamp())
    return timestamp


def transform_protocolName(protocolName: str):
    protocol_dict = {
        "tcp_ip": 0,
        "udp_ip": 1,
        "icmp_ip": 2,
        "igmp": 3,
        "ip": 4,
        "ipv6igmp": 5
    }
    if protocolName in protocol_dict:
        return protocol_dict[protocolName]
    else:
        return 6  # Other


def transform_payload(payload: str):
    # Test if the payload is a base64 string
    try:
        decoded_bytes = base64.b64decode(payload)
    except Exception:
        return 0
    # Compute hash of the decoded bytes
    hash_object = hashlib.sha256(decoded_bytes)
    # Convert hash to int
    integer_representation = int(hash_object.hexdigest(), 16)
    return integer_representation


def transform_direction(direction: str):
    direction_dict = {
        "L2R": 0,
        "R2L": 1,
        "L2L": 2,
        "R2R": 3
    }
    if direction in direction_dict:
        return direction_dict[direction]
    else:
        return 4  # Other


def transform_TCPFlagsDescription(TCPFlagsDescription: str):
    TCPFlagsDescription_dict = {
        "N/A": 0,
        "F,S,P,A": 1,
        "F,A": 2,
        "R": 3,
        "F,P,A": 4,
        "S, P, A": 5,
        "S,A": 6,
        "P,A": 7,
        "A": 8,
        "S": 9,
        "R,A": 10,
    }
    if TCPFlagsDescription in TCPFlagsDescription_dict:
        return TCPFlagsDescription_dict[TCPFlagsDescription]
    else:
        return 11  # Other


def transform_tag(tag: str):
    tag_dict = {
        "Normal": 0,
        "Attack": 1
    }
    if tag in tag_dict:
        return tag_dict[tag]
    else:
        return 2  # Other


def process_datas(datas: list):
    # TTransform datas list into a dataframe
    df = pd.DataFrame(datas)

    # Transform IP addresses into 32-bit integers
    print("[+] Transforming IP addresses into 32-bit integers")
    df["source"] = df["source"].apply(transform_IP)
    df["destination"] = df["destination"].apply(transform_IP)

    # Transform dates into timestamps
    print("[+] Transforming dates into timestamps")
    df["startDateTime"] = df["startDateTime"].apply(transform_date)
    df["stopDateTime"] = df["stopDateTime"].apply(transform_date)

    # Transform protocolName into integers
    print("[+] Transforming protocolName into integers")
    df["protocolName"] = df["protocolName"].apply(transform_protocolName)

    # Transform payload into integers
    print("[+] Transforming payload into integers")
    df["sourcePayloadAsBase64"] = df["sourcePayloadAsBase64"].apply(transform_payload)
    df["destinationPayloadAsBase64"] = df["destinationPayloadAsBase64"].apply(transform_payload)

    # Transform a direction into integers
    print("[+] Transforming a direction into integers")
    df["direction"] = df["direction"].apply(transform_direction)

    # Transform TCPFlagsDescription into integers
    print("[+] Transforming TCPFlagsDescription into integers")
    df["sourceTCPFlagsDescription"] = df["sourceTCPFlagsDescription"].apply(transform_TCPFlagsDescription)
    df["destinationTCPFlagsDescription"] = df["destinationTCPFlagsDescription"].apply(transform_TCPFlagsDescription)

    # Transform tag into integers
    print("[+] Transforming tag into integers")
    df["Tag"] = df["Tag"].apply(transform_tag)

    # Drop other payload columns
    print("[+] Dropping useless columns")
    df = df.drop(columns=["sourcePayloadAsUTF", "destinationPayloadAsUTF", "sensorInterfaceId", "startTime"])

    return df


# Serialize the dictionnaries using pickle to save some time
def serialize(dictionnaries: dict):
    with open('dictionnariesByAppNameSplitted.pickle', 'wb') as handle:
        pickle.dump(dictionnaries, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\n[+] Success")
    print(" ╰─ " + "The dictionnaries has been serialized")


def get_pickle_file() -> dict:
    with open('dictionnariesByAppNameSplitted.pickle', 'rb') as handle:
        return pickle.load(handle)


if __name__ == "__main__":
    # Start timer
    start = datetime.now()

    dictionnaries = get_dictionnaries()
    transform_dats = process_datas(dictionnaries)
    dictionnariesByAppNameSplitted = split_datas(transform_dats)
    serialize(dictionnariesByAppNameSplitted)

    # End timer
    end = datetime.now()
    print("\n[+] Execution time: " + str(end - start))
