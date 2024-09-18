from pydantic.dataclasses import dataclass


@dataclass
class Node:
    name: str
    config: dict
    type: str


@dataclass
class Relationship:
    src_node_name: str
    src_node_type: str
    dest_node_name: str
    dest_node_type: str
    type: str
