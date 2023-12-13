from lxml import etree as ET


def load_test():
    file = "data/traffic_os_TEST.xml"

    flows = []
    tree = ET.parse(file)
    root = tree.getroot()

    flow_elements = root.xpath("FFlow")

    for flow_elem in flow_elements:
        flow_dict = {}
        for child_elem in flow_elem.getchildren():
            if child_elem.tag in ["Timestamp", "Duration", "Src_Pt", "Dst_Pt", "Packets", "Bytes", "Flows", "Tos"]:
                flow_dict[child_elem.tag] = int(child_elem.text)
            else:
                flow_dict[child_elem.tag] = child_elem.text
        flows.append(flow_dict)

    # Transform flow list into pandas dataframe
    import pandas as pd
    df = pd.DataFrame(flows)

    return df


def load_train():
    file = "data/traffic_os_TRAIN.xml"

    flows = []
    tree = ET.parse(file)
    root = tree.getroot()

    flow_elements = root.xpath("FFlow")

    for flow_elem in flow_elements:
        flow_dict = {}
        for child_elem in flow_elem.getchildren():
            if child_elem.tag in ["Timestamp", "Duration", "Src_Pt", "Dst_Pt", "Packets", "Bytes", "Flows", "Tos"]:
                flow_dict[child_elem.tag] = int(child_elem.text)
            else:
                flow_dict[child_elem.tag] = child_elem.text
        flows.append(flow_dict)

    # Transform flow list into pandas dataframe
    import pandas as pd
    df = pd.DataFrame(flows)

    return df
