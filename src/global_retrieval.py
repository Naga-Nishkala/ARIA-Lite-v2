import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def load_embedder():
    model = SentenceTransformer("allenai-specter")
    print("SPECTER loaded")
    return model

global embedder
embedder = load_embedder()

def load_graph(graph_path):
    with open(graph_path, "rb") as f:
        G = pickle.load(f)

    print("Graph loaded")
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    return G


def load_communities(G):
    community_summaries = G.graph["community_summaries"]
    print("Communities found:", len(community_summaries))
    return community_summaries

def retrieve_communities(
    query,
    community_summaries,
    embedder,
    top_k=3
):
    """
    Query embedding → Community embedding similarity → Top-k communities
    """

    query_embedding = embedder.encode(
        query,
        normalize_embeddings=True
    )

    results = []

    for cid, info in community_summaries.items():

        community_embedding = info["embedding"]

        sim = cosine_similarity(
            [query_embedding],
            [community_embedding]
        )[0][0]

        results.append({
            "community_id": cid,
            "score": float(sim),
            "summary": info["summary"],
            "top_entities": info["top_entities"],
            "num_entities": info["num_entities"],
            "num_sections": info["num_sections"]
        })

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    print("Communities used:", len(results[:top_k]))

    return results[:top_k]
    

def get_community_sections(
    graph,
    community_id,
    max_sections=3
):
    sections = []

    for node, data in graph.nodes(data=True):

        if data.get("type") != "entity":
            continue

        if data.get("community_id") != community_id:
            continue

        for nbr in graph.neighbors(node):

            nbr_data = graph.nodes[nbr]

            if nbr_data.get("type") == "section":
                sections.append(nbr)

    sections = list(set(sections))

    return sections[:max_sections]


def build_global_context(graph, retrieved_communities):

    context = []

    for community in retrieved_communities:

        cid = community["community_id"]

        community_sections = get_community_sections(
            graph,
            cid
        )

        section_texts = []

        for sid in community_sections:

            text = graph.nodes[sid].get("text", "")

            if len(text) > 0:
                section_texts.append({
                    "section_id": sid,
                    "text": text[:1500]
                })

        context.append({
            "community_id": cid,
            "score": community["score"],
            "summary": community["summary"],
            "top_entities": community["top_entities"],
            "sections": section_texts
        })

    return context


def visualize_retrieved_communities(results):

    labels = [f"C{r['community_id']}" for r in results]
    scores = [r["score"] for r in results]

    plt.figure(figsize=(8,4))
    plt.bar(labels, scores)
    plt.title("Retrieved Communities")
    plt.ylabel("Cosine Similarity")
    plt.show()


def run_global_query(graph, query, top_k=3):

    community_summaries = load_communities(graph)

    retrieved = retrieve_communities(
        query,
        community_summaries,
        embedder,
        top_k=top_k
    )

    context = build_global_context(graph, retrieved)

    return retrieved, context