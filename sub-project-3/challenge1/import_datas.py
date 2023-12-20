def get_train_datas():
    # Imports
    import os
    from lxml import etree as ET

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
            flow_elements = root.xpath(
                "//TestbedMonJun14Flows | //TestbedSatJun12 | //TestbedSunJun13Flows | //TestbedThuJun17-1Flows | //TestbedThuJun17-2Flows | //TestbedTueJun15-1Flows | //TestbedTueJun15-2Flows | //TestbedWedJun16-1Flows | //TestbedWedJun16-2Flows")
            filename = filename.replace('.xml', '').replace('Flows', '').replace('bis', '')
            # Loop through the flow elements and convert each flow to a dictionary
            for flow_elem in flow_elements:
                flow_dict = {}
                for child_elem in flow_elem.getchildren():
                    if child_elem.tag == "Tag":
                        flow_dict[child_elem.tag] = child_elem.text
                    else:
                        flow_dict[child_elem.tag] = int(child_elem.text) if child_elem.tag.endswith(
                            ("Bytes", "Packets", "Port")) else child_elem.text
                dictionnaries.append(flow_dict)

    return dictionnaries


def get_test_datas(file: str) -> list:
    # Imports
    from lxml import etree as ET

    dictionnaries = []

    print(" ╰─ " + file)
    # Parse the XML file using lxml
    tree = ET.parse(file)
    root = tree.getroot()

    # Initialize a list to store flow dictionaries
    flow_data = []
    flow_elements = root.xpath("item")

    # Loop through the flow elements and convert each flow to a dictionary
    for flow_elem in flow_elements:
        flow_dict = {}
        for child_elem in flow_elem.getchildren():
            if child_elem.tag == "Tag":
                flow_dict[child_elem.tag] = child_elem.text
            else:
                flow_dict[child_elem.tag] = int(child_elem.text) if child_elem.tag.endswith(
                    ("Bytes", "Packets", "Port")) else child_elem.text
        dictionnaries.append(flow_dict)

    return dictionnaries


if __name__ == "__main__":
    dictionnaries = get_train_datas()
    print("\n\033[32m[+] Success")
    print(" ╰─ Dictionnaries has been generated\033[37m")

    data = get_test_datas("challenge1_data/benchmark_SSH_test.xml")
    print("\n\033[32m[+] Success")
    print(" ╰─ Dictionnaries has been generated\033[37m")
