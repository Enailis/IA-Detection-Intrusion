from dataclasses import dataclass

from bigxml import xml_handle_element, XMLElement


@xml_handle_element("dataroot", "FFlow")
@dataclass
class Flow:
    duration: float = 0.0
    src_ip: str = ""
    src_port: float = 0.0
    dst_ip: str = ""
    dst_port: float = 0.0
    protocol: str = ""
    flags: str = ""
    tos: int = 0
    packets: int = 0
    bytes: int = 0
    flows: int = 0
    label: str = ""

    @xml_handle_element("Duration")
    def handle_duration(self, node: XMLElement):
        self.duration = float(node.text)

    @xml_handle_element("Protocol")
    def handle_protocol(self, node: XMLElement):
        self.protocol = node.text

    @xml_handle_element("Src_IP_Add")
    def handle_src_ip(self, node: XMLElement):
        self.src_ip = node.text

    @xml_handle_element("Src_Pt")
    def handle_src_pt(self, node: XMLElement):
        self.src_port = float(node.text)

    @xml_handle_element("Dst_IP_Add")
    def handle_dst_ip(self, node: XMLElement):
        self.dst_ip = node.text

    @xml_handle_element("Dst_Pt")
    def handle_dst_pt(self, node: XMLElement):
        self.dst_port = float(node.text)

    @xml_handle_element("Packets")
    def handle_packets(self, node: XMLElement):
        self.packets = int(node.text)

    @xml_handle_element("Bytes")
    def handle_bytes(self, node: XMLElement):
        try:
            self.bytes = int(node.text)
        except:
            self.bytes = 0

    @xml_handle_element("Flows")
    def handle_flows(self, node: XMLElement):
        self.flows = int(node.text)

    @xml_handle_element("Flags")
    def handle_flags(self, node: XMLElement):
        self.flags = node.text

    @xml_handle_element("Tos")
    def handle_tos(self, node: XMLElement):
        self.tos = int(node.text)

    @xml_handle_element("Tag")
    def handle_tag(self, node: XMLElement):
        self.label = node.text
