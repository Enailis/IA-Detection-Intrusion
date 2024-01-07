import pickle

import pandas as pd
from bigxml import Parser

from Flow import Flow
from transformation import transform_flow


def load_file(file):
    flow_list = []

    with open(file, 'rb') as f:
        print("Parsing file")
        for item in Parser(f).iter_from(Flow):
            # Process item
            transformed_item = transform_flow(item)

            # Add item to list
            flow_list.append(transformed_item)
    f.close()

    # Convert list to dataframe
    df = pd.DataFrame(flow_list)

    return df


def export_pickle(train, test):
    with open('train.pickle', 'wb') as handle:
        pickle.dump(train, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\n[+] Success")
    print(" ╰─ " + "The train datas has been serialized")

    with open('test.pickle', 'wb') as handle:
        pickle.dump(test, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\n[+] Success")
    print(" ╰─ " + "The train datas has been serialized")


def load_pickle():
    print("\n[~] Loading pickle files...")
    with open('train.pickle', 'rb') as handle:
        train = pickle.load(handle)

    with open('test.pickle', 'rb') as handle:
        test = pickle.load(handle)

    print("\n[+] Success")
    print(" ╰─ " + "The files has been loaded successfully")

    return train, test


if __name__ == "__main__":
    print("\n[~] Loading training datas...")
    train = load_file("data/traffic_os_TRAIN.xml")
    print("[+] Training datas:")
    print(train.head())

    print("\n[~] Loading training datas...")
    test = load_file("data/traffic_os_TEST.xml")
    print("[+] Testing datas:")
    print(test.head())

    print("\n[~] Exporting datas to pickle files...")
    export_pickle(train, test)
    train_pickle, test_pickle = load_pickle()

    print("\n[+] Training datas from pickle file:")
    print(train_pickle.head())

    print("\n[+] Testing datas from pickle file:")
    print(test_pickle.head())
