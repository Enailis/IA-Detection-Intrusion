def get_dictionnaries():
    # Imports
    import os
    from dotenv import load_dotenv
    from elasticsearch import Elasticsearch
    from elasticsearch.helpers import bulk
    from lxml import etree as ET

    # Load environment variables
    load_dotenv()
    LOGIN = os.getenv("LOGIN")
    PASSWORD = os.getenv("PASSWORD")

    # Create ElasticSearch object
    es = Elasticsearch("https://tdelastic:9200", verify_certs=False, request_timeout=1000000, basic_auth=(LOGIN, PASSWORD))

    directory = "TRAIN_ENSIBS"
    dictionnaries = []

    print("[+] Indexing file")
    
    # Foreach files in "TRAIN_ENSIBS" directory
    for filename in os.listdir(directory):
        # Filter to check only XML files
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

    # Send datas to ElasticSearch
    success, failed = bulk(es, dictionnaries, index="ia-detection-intrusion")
    return success, failed, dictionnaries


if __name__ == "__main__":
    success, failed, dictionnaries = get_dictionnaries()
    print("[+] Success")
    print(" ╰─ " + str(success))
    print("[-] Failed")
    print(" ╰─ " + str(failed))