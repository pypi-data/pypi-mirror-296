import logging
from dataclasses import asdict
from .models import Node, Relationship
from neo4j import GraphDatabase


class Client:
    def __init__(
        self,
        neo4j_uri: str,
        neo4j_db_name: str,
        neo4j_username: str,
        neo4j_password: str,
    ):
        self.neo4j_uri = neo4j_uri
        self.neo4j_db_name = neo4j_db_name
        self.neo4j_username = neo4j_username
        self.neo4j_password = neo4j_password

    def create_or_update_nodes(self, nodes: list[Node]):
        """Create or update Node to graph database"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            driver.execute_query(
                """
                WITH $data AS batch
                UNWIND batch AS node
                CALL apoc.merge.node([node.type], {name: node.name, type: node.type}, apoc.map.merge({name: node.name, type: node.type}, node.config), node.config) YIELD node AS mergedNode
                RETURN mergedNode
                """,
                {"data": [asdict(node) for node in nodes]},
                database_=self.neo4j_db_name,
            )
        logging.info(f"Successfully created or updated {len(nodes)} nodes")

    def create_or_update_relationships(self, relationships: list[Relationship]):
        """Create or update Relationship to graph database"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            driver.execute_query(
                """
                WITH $data AS batch
                UNWIND batch AS relationship
                MATCH (k {name: relationship.src_node_name, type: relationship.src_node_type})
                with k, relationship
                MATCH (j {name: relationship.dest_node_name, type: relationship.dest_node_type})
                WITH k, j, relationship
                CALL apoc.merge.relationship(k, relationship.type, {}, {}, j)
                YIELD rel
                return rel
                """,
                {"data": [asdict(relationship) for relationship in relationships]},
                database_=self.neo4j_db_name,
            )
        logging.info(
            f"Successfully created or updated {len(relationships)} relationships"
        )

    def get_nodes_with_missing_relationship(
        self, node_type: str, relationship_type: str, limit: int
    ) -> list[Node]:
        """Return Nodes of type with missing relationship"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            result = driver.execute_query(
                f"""
                MATCH (node:{node_type})
                WHERE NOT EXISTS ((node)-[:{relationship_type}]->())
                RETURN node LIMIT {limit}
                """,
                database_=self.neo4j_db_name,
            )
            nodes = self._get_nodes_from_result(result)
            return nodes

    def get_nodes_of_type(self, node_type: str) -> list[Node]:
        """Get Nodes of a specific type"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            result = driver.execute_query(
                f"""
                MATCH (node {{type: '{node_type}'}})
                RETURN node
                """,
                database_=self.neo4j_db_name,
            )

            nodes = self._get_nodes_from_result(result)
            return nodes

    def get_nodes_of_type_with_fields(
        self, node_type: str, fields: dict[str, str]
    ) -> list[Node]:
        """Get Nodes of a specific type with fields"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            field_string = ", ".join(
                [f"{key}: '{value}'" for key, value in fields.items()]
            )
            result = driver.execute_query(
                f"""
                MATCH (node:{node_type} {{{field_string}}})
                RETURN node
                """,
                database_=self.neo4j_db_name,
            )

            nodes = self._get_nodes_from_result(result)
            return nodes

    def get_node(self, name: str, node_type: str) -> Node:
        """Get Node by name and type"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            result = driver.execute_query(
                f"""
                MATCH (node {{type: "{node_type}", name: "{name}"}})
                RETURN node
                """,
                database_=self.neo4j_db_name,
            )

            nodes = self._get_nodes_from_result(result)
            return nodes[0]

    def get_related_nodes(
        self, node_name: str, node_type: str, relationship_type: str
    ) -> list[Node]:
        """Get Nodes related to a specific Node"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            result = driver.execute_query(
                f"""
                MATCH (og_node {{type: '{node_type}', name: '{node_name}'}})-[r:{relationship_type}]->(node)
                RETURN node
                """,
                database_=self.neo4j_db_name,
            )

            nodes = self._get_nodes_from_result(result)
            return nodes

    def get_nodes_of_type_with_property_not_set(
        self, node_type: str, property: str
    ) -> list[Node]:
        """Get Nodes of a specific type with missing given property"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            result = driver.execute_query(
                f"""
                MATCH (node:{node_type})
                WHERE (node.{property}) IS NULL
                RETURN node
                """,
                database_=self.neo4j_db_name,
            )

            nodes = self._get_nodes_from_result(result)
            return nodes

    def create_vector_index(
        self,
        node_type: str,
        embedding_field: str,
        vector_dimensions: int,
        vector_similarity_function: str,
    ):
        """Create Vector Index"""
        try:
            with GraphDatabase.driver(
                self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
            ) as driver:
                driver.execute_query(
                    f"""
                    CREATE VECTOR INDEX
                    FOR (n:{node_type}) ON (n.{embedding_field})
                    OPTIONS {{indexConfig: {{
                        `vector.dimensions`: {vector_dimensions},
                        `vector.similarity_function`: '{vector_similarity_function}'
                      }}
                    }}
                    """,
                    database_=self.neo4j_db_name,
                )
            logging.info(f"Successfully created vector index for {node_type}")
        except Exception as e:
            if "An equivalent index already exists" in e.message:
                logging.info(f"Vector index for {node_type} already exists.")
            else:
                raise

    def set_nodes_vector_property(
        self, node_type: str, nodes: list[Node], embedding_field: str
    ):
        """Set parameters for nodes in graph database"""
        with GraphDatabase.driver(
            self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password)
        ) as driver:
            driver.execute_query(
                f"""
                WITH $data AS batch
                UNWIND batch AS node_data
                MATCH (node:{node_type} {{name: node_data.name}})
                CALL db.create.setNodeVectorProperty(node, '{embedding_field}', node_data.config['{embedding_field}'])
                """,
                {"data": [asdict(node_data) for node_data in nodes]},
                database_=self.neo4j_db_name,
            )
        logging.info(f"Successfully set parameters for {len(nodes)} {node_type} nodes")

    def _get_nodes_from_result(self, result):
        records, summary, keys = result
        raw_nodes = []
        for record in records:
            node = record["node"]
            node_data = {
                "id": node.element_id,
                "labels": list(node.labels),
                "properties": dict(node.items()),
            }
            raw_nodes.append(node_data)

        nodes = []
        for raw_node in raw_nodes:
            config = raw_node["properties"]
            name = raw_node["properties"]["name"]
            del config["name"]
            type = raw_node["properties"]["type"]
            del config["type"]

            node = Node(
                name=name,
                type=type,
                config=config,
            )
            nodes.append(node)
        return nodes
