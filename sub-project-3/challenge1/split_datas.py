import base64
import hashlib
import pickle
from datetime import datetime

import pandas
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from import_datas import get_test_datas
from import_datas import get_train_datas


def split_datas(main_dataframe: pandas.DataFrame):
    print("[+] Splitting datas")
    # Subdivided the dictionaries according to the appName
    appNames = ["HTTPWeb", "SSH", "SMTP", "FTP"]

    # Split the main dataframe into appNames dataframes
    dictionnariesByAppName = {}
    for appName in appNames:
        df = main_dataframe[main_dataframe["appName"] == appName]
        dictionnariesByAppName[appName] = df.to_dict(orient="records")

    return dictionnariesByAppName


def transform_IP(ip: str):
    # Transform an IP address into a 32-bit integer
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

    # Normalize the integer representation
    scaler = MinMaxScaler()
    normalized_representation = scaler.fit_transform([[integer_representation]])[0][0]

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
    # print("[+] Transforming payload into integers")
    # df["sourcePayloadAsBase64"] = df["sourcePayloadAsBase64"].apply(transform_payload)
    # df["destinationPayloadAsBase64"] = df["destinationPayloadAsBase64"].apply(transform_payload)

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
    df = df.drop(columns=["sourcePayloadAsUTF", "destinationPayloadAsUTF"])

    return df


# Serialize the dictionnaries using pickle to save some time
def serialize(dictionnaries: dict, name: str):
    with open(f'{name}.pickle', 'wb') as handle:
        pickle.dump(dictionnaries, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\n[+] Success")
    print(" ╰─ " + "The dictionnaries has been serialized")


def get_pickle_file(name: str) -> dict:
    with open(f'{name}.pickle', 'rb') as handle:
        return pickle.load(handle)


if __name__ == "__main__":
    # Start timer
    start = datetime.now()

    # Get datas
    train = get_train_datas()
    test_ssh = get_test_datas("challenge1_data/benchmark_SSH_test.xml")
    test_http = get_test_datas("challenge1_data/benchmark_HTTPWeb_test.xml")

    # Process datas
    print("\n[+] --- Processing datas")
    print(" ╰─ " + "train")
    train_process = process_datas(train)
    print(" ╰─ " + "test_ssh")
    test_ssh_process = process_datas(test_ssh)
    print(" ╰─ " + "test_http")
    test_http_process = process_datas(test_http)

    # Split datas
    print("\n[+] --- Splitting datas")
    train_splitted = split_datas(train_process)

    # Split the main dataframe into appNames dataframes
    test_ssh = {"SSH": test_ssh_process.to_dict(orient="records")}
    test_http = {"HTTPWeb": test_http_process.to_dict(orient="records")}

    # Serialize datas
    print("\n[+] --- Serializing datas")
    print(" ╰─ " + "train")
    serialize(train_splitted, "train")
    print(" ╰─ " + "test_ssh")
    serialize(test_ssh, "test_ssh")
    print(" ╰─ " + "test_http")
    serialize(test_http, "test_http")
    print("\n[+] Success")

    # End timer
    end = datetime.now()
    print("\n[+] Execution time: " + str(end - start))
