from bigxml import XMLElement


def transform_IP(ip: str):
    # Transform an IP address into a 32-bit integer
    ip = ip.split('.')

    # Prevent bad IP addresses
    if len(ip) != 4:
        return 0

    ip = [int(i) for i in ip]
    ip = ip[0] * 256 ** 3 + ip[1] * 256 ** 2 + ip[2] * 256 + ip[3]
    return ip


def transform_protocolName(protocolName: str):
    protocol_dict = {
        "TCP": 0,
        "UDP": 1,
        "IGMP": 2,
        "ICMP": 3
    }
    if protocolName in protocol_dict:
        return protocol_dict[protocolName]
    else:
        return 4  # Other


def trandform_flags(flags: str):
    new_flags = []

    # Create a list of 1 and 0 (1 if a char is present, 0 otherwise) pattern '?APRSF'
    for char in flags:
        if char != '.':
            new_flags.append("1")
        else:
            new_flags.append("0")

    # Transform the list into a string
    new_flags = "".join(new_flags)

    return int(new_flags)


def transform_tag(tag: str):
    tag_dict = {
        "normal": 0,
        "attacker": 1,
        "victim": 2,
    }
    if tag in tag_dict:
        return tag_dict[tag]
    else:
        return 3  # Other


def transform_flow(flow: XMLElement) -> dict:
    # Convert to dictionary
    flow = flow.__dict__

    # Transform IP addresses
    flow["src_ip"] = transform_IP(flow["src_ip"])
    flow["dst_ip"] = transform_IP(flow["dst_ip"])

    # Transform flags
    flow["flags"] = trandform_flags(flow["flags"])

    # Transform protocol
    flow["protocol"] = transform_protocolName(flow["protocol"])

    # Transform lavel
    flow["label"] = transform_tag(flow["label"])

    return flow
