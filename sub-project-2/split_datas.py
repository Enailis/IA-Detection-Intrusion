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
                dictionnariesByAppName[appName].append(dictionnary)

    # Split each dictionary into 5 parts S1, S2, S3, S4, S5 using pandas
    dictionnariesByAppNameSplitted = {}
    for appName in appNames:
        df = pd.DataFrame(dictionnariesByAppName[appName])
        df_split = np.array_split(df, 5)
        dictionnariesByAppNameSplitted[appName] = df_split
    
    print("\n[+] Success")
    print(" ╰─ " + "Dicts splitted into 5 parts")


# Serialize the dictionnaries using pickle to save some time
def serialize(dictionnaries):
    import pickle
    
    with open('dictionnariesByAppNameSplitted.pickle', 'wb') as handle:
        pickle.dump(dictionnaries, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("\n[+] Success")
    print(" ╰─ " + "The dictionnaries has been serialized")


if __name__ == "__main__":
    dictionnaries = get_dictionnaries()
    split_datas(dictionnaries)
    serialize(dictionnaries)