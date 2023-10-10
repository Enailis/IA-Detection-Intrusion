def get_dictionnaries():
    import os
    import xmltodict as xtd

    #from elasticsearch import Elasticsearch
    #es = Elasticsearch("http://localhost:9200")

    directory = "TRAIN_ENSIBS"
    dictionnaries = []

    print("Indexing files...")

    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            print("╰─ " + file)
            with open(file, 'r') as f:
                dictionnaries.append(xtd.parse(f.read()))
                #file_name = file.replace(directory + "/", "")
                #es.index(index=file_name, id=len(dictionnaries), document=dictionnaries[-1])
    
    return dictionnaries


if __name__ == "__main__":
    dictionnaries = get_dictionnaries()

    # Understand data's structure
    # The files are stored in a list called 'dictionnaries'
    # Each file is then stored in a dictionnary
    # The datas we want to access are all stored in the last key of dictionnaries[n]['dataroot'] 
    # This last key contains a list of dictionnaries of every flows
    # If you want to access 'appName', 'totalSourceBytes', etc. you'll have to do something like this:
    # dictionnaries[0]['dataroot']['TestbedMonJun14Flows'][0]['appName']

    print(dictionnaries[0]['dataroot']['TestbedMonJun14Flows'][0].keys())