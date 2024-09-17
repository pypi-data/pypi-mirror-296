from pydantic.dataclasses import dataclass


@dataclass
class Node:
    name: str
    config: dict
    type: str


@dataclass
class Relationship:
    src_node_name: str
    dest_node_name: str
    type: str
