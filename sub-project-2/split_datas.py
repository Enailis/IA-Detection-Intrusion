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

    # Slipt each dictionnary into 5 parts S1, S2, S3, S4, S5
    dictionnariesByAppNameSplitted = {}
    for appName in appNames:
        dictionnariesByAppNameSplitted[appName] = []
        for i in range(5):
            dictionnariesByAppNameSplitted[appName].append([])
        for i in range(len(dictionnariesByAppName[appName])):
            dictionnariesByAppNameSplitted[appName][i % 5].append(dictionnariesByAppName[appName][i])

    print("[+] Success")
    print(" ╰─ " + "Dicts splitted into 5 parts")