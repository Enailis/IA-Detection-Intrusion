import pickle
import pandas as pd
import numpy as np
from import_datas import get_dictionnaries


def split_datas(dictionnaries):

    print("[+] Splitting datas")
    # Subdivided the dictionaries according to the appName
    appNames = ["HTTPWeb", "SSH", "SMTP", "FTP"]

    # Create a new dictionnary for each appName and fill it with the corresponding data
    dictionnariesByAppName = {}
    for appName in appNames:
        dictionnariesByAppName[appName] = []
        for dictionnary in dictionnaries:
            source = dictionnary["_source"]
            if source["appName"] == appName:
                dictionnariesByAppName[appName].append(source)

    return dictionnariesByAppName


# Serialize the dictionnaries using pickle to save some time
def serialize(dictionnaries):
    with open('dictionnariesByAppNameSplitted.pickle', 'wb') as handle:
        pickle.dump(dictionnaries, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\n[+] Success")
    print(" ╰─ " + "The dictionnaries has been serialized")


def get_pickle_file():
    with open('dictionnariesByAppNameSplitted.pickle', 'rb') as handle:
        return pickle.load(handle)


if __name__ == "__main__":
    dictionnaries = get_dictionnaries()
    dictionnariesByAppNameSplitted = split_datas(dictionnaries)
    serialize(dictionnariesByAppNameSplitted)