import os
import pickle
import networkx as nx
from collections import defaultdict
import spacy
import matplotlib.pyplot as plt
from collections import defaultdict

nlp = spacy.load("en_core_sci_md")

def extract_query_entities(query):
    """
    Extract biomedical entities from query using SciSpacy.
    """
    doc = nlp(query)
    entities = set()

    for ent in doc.ents:
        entities.add(ent.text.lower())

    return list(entities)

def get_seed_nodes(query_entities, entity_to_nodes):
    """
    Map extracted entities → graph nodes.
    """
    seeds = []

    for ent in query_entities:
        if ent in entity_to_nodes:
            seeds.extend(entity_to_nodes[ent])

    return list(set(seeds))


def local_traversal(
    graph,
    seed_nodes,
    max_hops=2,
    max_section_expansion=25
):

    """
    Local Graph Traversal

    Input:
        graph
        seed_nodes = matched query entities

    Output:
        retrieved_sections
        traversal_records
    """

    retrieved_sections = set()

    traversal_records = []

    # --------------------------------------------------------
    # HOP 1
    # ENTITY <-> SECTION
    # --------------------------------------------------------

    first_sections = set()

    for entity in seed_nodes:

        if entity not in graph:
            continue

        for nbr in graph.neighbors(entity):

            nbr_type = graph.nodes[nbr].get("type")

            # ----------------------------------------
            # ENTITY -> SECTION
            # ----------------------------------------
            if nbr_type == "section":

                edge_type = graph.edges[entity, nbr].get(
                    "type",
                    "MENTIONS"
                )

                first_sections.add(nbr)
                retrieved_sections.add(nbr)

                traversal_records.append({
                    "source": entity,
                    "edge": edge_type,
                    "target": nbr,
                    "hop": 1,
                    "score": 3
                })

    # --------------------------------------------------------
    # HOP 2
    # SECTION -> ENTITY -> SECTION
    # --------------------------------------------------------

    if max_hops >= 2:

        second_sections = set()

        for section in first_sections:

            for nbr in graph.neighbors(section):

                nbr_type = graph.nodes[nbr].get("type")

                # ------------------------------------
                # SECTION -> ENTITY
                # ------------------------------------
                if nbr_type == "entity":

                    edge_type = graph.edges[section, nbr].get(
                        "type",
                        "UNKNOWN"
                    )

                    traversal_records.append({
                        "source": section,
                        "edge": edge_type,
                        "target": nbr,
                        "hop": 2,
                        "score": 2
                    })

                    # ------------------------------------------------
                    # LIMIT SECTION EXPANSION
                    # Prevent graph explosion from supernodes
                    # ------------------------------------------------

                    connected_sections = []

                    for sec2 in graph.neighbors(nbr):

                        if graph.nodes[sec2].get("type") == "section":
                            connected_sections.append(sec2)

                    # limit expansion
                    connected_sections = connected_sections[
                        :max_section_expansion
                    ]

                    # ------------------------------------------------
                    # ENTITY -> SECTION
                    # ------------------------------------------------

                    for sec2 in connected_sections:

                        edge2 = graph.edges[nbr, sec2].get(
                            "type",
                            "MENTIONS"
                        )

                        second_sections.add(sec2)
                        retrieved_sections.add(sec2)

                        traversal_records.append({
                            "source": nbr,
                            "edge": edge2,
                            "target": sec2,
                            "hop": 2,
                            "score": 2
                        })

    return list(retrieved_sections), traversal_records


def score_sections(
    query_entities,
    retrieved_sections,
    traversal_records,
    graph
):

    """
    Score retrieved sections based on:
    - edge type
    - hop distance
    - entity overlap
    - deduplicated traversal paths
    """

    query_entities = set([
        e.lower() for e in query_entities
    ])

    section_scores = defaultdict(float)

    section_paths = defaultdict(list)

    # --------------------------------------------------------
    # DEDUPLICATE PATHS ARE RECORDED
    # --------------------------------------------------------

    seen_paths = set()

    # --------------------------------------------------------
    # SCORE VIA TRAVERSAL RECORDS
    # --------------------------------------------------------

    for record in traversal_records:

        source = record["source"]
        edge = record["edge"]
        target = record["target"]
        hop = record["hop"]

        # ----------------------------------------------------
        # only score section targets
        # ----------------------------------------------------

        if target not in retrieved_sections:
            continue

        # ----------------------------------------------------
        # UNIQUE PATH KEY
        # ----------------------------------------------------

        path_key = (
            source,
            edge,
            target,
            hop
        )

        # skip duplicate paths
        if path_key in seen_paths:
            continue

        seen_paths.add(path_key)

        score = 0

        # ----------------------------------------------------
        # EDGE WEIGHTS
        # ----------------------------------------------------

        if edge == "MENTIONS":
            score += 3

        elif edge == "SIMILAR_SECTION":
            score += 2

        elif edge == "CO_OCCURS":
            score += 1

        # ----------------------------------------------------
        # STRONGER HOP PENALTIES
        # ----------------------------------------------------

        if hop == 1:

            # direct evidence
            score += 5

        elif hop == 2:

            # weaker contextual evidence
            score += 1

        elif hop >= 3:

            # penalize distant traversal
            score -= 2

        # ----------------------------------------------------
        # ENTITY OVERLAP BONUS
        # ----------------------------------------------------

        section_text = graph.nodes[target].get(
            "text",
            ""
        ).lower()

        overlap = 0

        for ent in query_entities:

            if ent in section_text:
                overlap += 1

        score += overlap * 2

        # ----------------------------------------------------
        # STORE SCORE
        # ----------------------------------------------------

        section_scores[target] += score

        section_paths[target].append(record)

    # --------------------------------------------------------
    # BUILD RANKED OUTPUT
    # --------------------------------------------------------

    ranked_sections = []

    for section, score in section_scores.items():

        ranked_sections.append({

            "section_id": section,

            "score": round(score, 2),

            "text": graph.nodes[section].get(
                "text",
                ""
            ),

            "paper_id": graph.nodes[section].get(
                "paper_id",
                ""
            ),

            "paths": section_paths[section]
        })

    ranked_sections = sorted(
        ranked_sections,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_sections


def run_local_query(graph, query):
    """
    Full local retrieval pipeline wrapper.
    """

    # Step 1 — entity extraction
    query_entities = extract_query_entities(query)

    # Step 2 — seed node mapping
    entity_to_nodes = {
        n: [n] for n, d in graph.nodes(data=True)
        if d.get("type") == "entity"
    }

    seed_nodes = get_seed_nodes(query_entities, entity_to_nodes)

    # Step 3 — traversal
    retrieved_sections, traversal_records = local_traversal(
        graph,
        seed_nodes
    )

    # Step 4 — scoring
    ranked_sections = score_sections(
        query_entities,
        retrieved_sections,
        traversal_records,
        graph
    )

    return ranked_sections


def visualize_traversal(graph, ranked_sections, top_k=3):

    """
    Visualize retrieval paths.
    """

    viz_graph = nx.Graph()

    # --------------------------------------------------------
    # ADD PATHS
    # --------------------------------------------------------

    for item in ranked_sections[:top_k]:

        for path in item["paths"]:

            src = path["source"]
            tgt = path["target"]
            edge = path["edge"]

            viz_graph.add_node(src)
            viz_graph.add_node(tgt)

            viz_graph.add_edge(src, tgt, label=edge)

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    plt.figure(figsize=(14, 10))

    pos = nx.spring_layout(viz_graph, seed=42)

    nx.draw(
        viz_graph,
        pos,
        with_labels=True,
        node_size=1800,
        font_size=8
    )

    edge_labels = nx.get_edge_attributes(
        viz_graph,
        "label"
    )

    nx.draw_networkx_edge_labels(
        viz_graph,
        pos,
        edge_labels=edge_labels,
        font_size=7
    )

    plt.title("ARIA Local Traversal Explainability")

    plt.show()