def get_dictionnaries():
    # Imports
    from lxml import etree as ET

    file = "challenge1_data/benchmark_HTTPWeb_test.xml"
    dictionnaries = []
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
        flow_data.append(flow_dict)

    # Index the flow data in Elasticsearch with the origin file information
    for flow in flow_data:
        flow["origin_file"] = file

        dictionnaries.append({
            '_op_type': 'index',
            '_index': "ia-detection-intrusion",
            '_source': flow
        })

    return dictionnaries


if __name__ == '__main__':
    data = get_dictionnaries()
    print(data)
