import pickle
from lxml import etree as ET


def load_file(file):
    flows = []
    context = ET.iterparse(file, events=("end",), tag=("FFlow"))
    
    for _, elem in context:
        flow_dict = {}
        for child_elem in elem.getchildren():
            if child_elem.tag in ["Timestamp", "Duration", "Src_Pt", "Dst_Pt", "Packets", "Flows", "Tos"]:
                flow_dict[child_elem.tag] = int(float(child_elem.text.replace(' ', '')))
            elif child_elem.tag == "Bytes":
                value = child_elem.text.replace(' ', '')
                convertion = {("M", '000000'), ("K", '000'), ("G", '000000000')}
                for k, v in convertion:
                    if k in value:
                        value = value.replace(k, v).replace('.', '')
                flow_dict[child_elem.tag] = int(float(value))
            else:
                flow_dict[child_elem.tag] = child_elem.text
        flows.append(flow_dict)

    # Transform flow list into pandas dataframe
    import pandas as pd
    df = pd.DataFrame(flows)

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