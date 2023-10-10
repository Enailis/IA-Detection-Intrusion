def get_dictionnaries():
    import os
    import xmltodict as xtd

    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk
    es = Elasticsearch("https://tdelastic:9200", verify_certs=False, request_timeout=1000000)

    directory = "TRAIN_ENSIBS"
    dictionnaries = []

    print("Indexing files...")

    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            print("╰─ " + file)
            with open(file, 'r') as f:
                dictionnaries.append(xtd.parse(f.read()))
                file_name = file.replace(directory + "/", "")
                es.index(index=file_name, id=len(dictionnaries), document=dictionnaries[-1])
    
    return dictionnaries



def get_dictionnaries2():
    import os
    from dotenv import load_dotenv
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk
    from lxml import etree as ET

    # Create ElasticSearch object
    load_dotenv()
    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")
    es = Elasticsearch("https://tdelastic:9200", verify_certs=False, request_timeout=1000000, http_auth=(LOGIN, PASSWORD))

    directory = "TRAIN_ENSIBS"
    dictionnaries = []

    # Pour chaque fichier XML du dossier
    print("[+] Indexing file")
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if filename.endswith(".xml"):
            print(" ╰─ " + filename)
            file_path = os.path.join(directory, filename)

            # Parse the XML file using lxml
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Initialize a list to store flow dictionaries
            flow_data = []
            flow_elements = root.xpath("//TestbedMonJun14Flows | //TestbedSatJun12 | //TestbedSunJun13Flows | //TestbedThuJun17-1Flows | //TestbedThuJun17-2Flows | //TestbedTueJun15-1Flows | //TestbedTueJun15-2Flows | //TestbedWedJun16-1Flows | //TestbedWedJun16-2Flows")
            filename = filename.replace('.xml','').replace('Flows','').replace('bis','')
            # Loop through the flow elements and convert each flow to a dictionary
            for flow_elem in flow_elements:
                flow_dict = {}
                for child_elem in flow_elem.getchildren():
                    if child_elem.tag == "Tag":
                        flow_dict[child_elem.tag] = child_elem.text
                    else:
                        flow_dict[child_elem.tag] = int(child_elem.text) if child_elem.tag.endswith(("Bytes", "Packets", "Port")) else child_elem.text
                flow_data.append(flow_dict)

            # Index the flow data in Elasticsearch with the origin file information
            for flow in flow_data:
                flow["origin_file"] = filename

                dictionnaries.append({
                    '_op_type': 'index',
                    '_index': "ia-detection-intrusion",
                    '_source': flow
                })

    success, failed = bulk(es, dictionnaries, index="ia-detection-intrusion")
    print("[+] Success: " + str(success))
    print("[-] Failed: " + str(failed))
    return dictionnaries


if __name__ == "__main__":
    dictionnaries = get_dictionnaries2()

    # Understand data's structure
    # The files are stored in a list called 'dictionnaries'
    # Each file is then stored in a dictionnary
    # The datas we want to access are all stored in the last key of dictionnaries[n]['dataroot'] 
    # This last key contains a list of dictionnaries of every flows
    # If you want to access 'appName', 'totalSourceBytes', etc. you'll have to do something like this:
    # dictionnaries[0]['dataroot']['TestbedMonJun14Flows'][0]['appName']

