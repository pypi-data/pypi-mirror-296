# Copyright Jiaqi (Hutao of Emberfire)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import yaml
from neo4j import GraphDatabase

URI = os.environ["NEO4J_URI"]
AUTH = (os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])


def get_vocabulary(yaml_path: str) -> list[tuple[str, str]]:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    return [(vocabulary["term"], vocabulary["definition"]) for vocabulary in data["vocabulary"]]


def load_into_database(yaml_path: str, language: str):
    """
    Upload a vocabulary file to Neo4j Database.

    The YAML format has to be the following::

    vocabulary:
      - term: 你好
        definition: hello
      - term: 一
        definition: 1
      - term: 二
        definition: 2
      ...

    The function handles MANY-TO-MANY relationships. i.e. multiple terms with the same definition and multiple
    definitions with the same term. Each unique term and definition are separate nodes in graph. The MANY-TO-MANY
    relationships show up naturally as multi incident/outgoing edges of the nodes.

    :param yaml_path:  The absolute or relative path (to the invoking script) to the YAML file that containts the
                       vocabulary structure mentioned above.
    :param language:  The language of the vocabulary. This value will show up as the "language" property of the `Term`
                      node in the Graph database.
    """
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

    vocabulary = get_vocabulary(yaml_path)
    unique_terms = set(term for term, definition in vocabulary)
    unique_definitions = set(definition for term, definition in vocabulary)

    with driver.session() as session:
        session.write_transaction(
            lambda tx, terms: [
                tx.run(
                    "CREATE (term:Term {name: $term, language: $language})",
                    term=term,
                    language=language,
                ) for term in terms
            ],
            unique_terms
        )
        session.write_transaction(
            lambda tx, definitions: [
                tx.run(
                    "CREATE (definition:Definition {name: $definition})",
                    definition=definition,
                ) for definition in definitions
            ],
            unique_definitions
        )

        session.write_transaction(
            lambda tx, nodes: [
                tx.run(
                    """
                    MATCH
                        (term:Term WHERE term.name = $term AND term.language = $language),
                        (definition:Definition WHERE definition.name = $definition)
                    CREATE
                        (term)-[:DEFINITION]->(definition)
                    """,
                    term=node["name"],
                    language=language,
                    definition=node["definition"],
                ) for node in nodes
            ],
            [{"name": term, "definition": definition} for term, definition in vocabulary]
        )
