import networkx as nx
import matplotlib.pyplot as plt

def visualize_local_traversal(traversal_records, top_k=3):
    """
    Visualize LOCAL retrieval paths.
    """

    G_viz = nx.DiGraph()

    # Build graph from traversal records
    for r in traversal_records:
        src = r["source"]
        tgt = r["target"]
        edge = r["edge"]
        hop = r["hop"]

        G_viz.add_node(src)
        G_viz.add_node(tgt)
        G_viz.add_edge(src, tgt, label=f"{edge}(H{hop})")

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G_viz, seed=42)

    nx.draw(
        G_viz,
        pos,
        with_labels=True,
        node_size=1800,
        font_size=8,
        arrows=True
    )

    edge_labels = nx.get_edge_attributes(G_viz, "label")
    nx.draw_networkx_edge_labels(
        G_viz,
        pos,
        edge_labels=edge_labels,
        font_size=7
    )

    plt.title("LOCAL TRAVERSAL EXPLAINABILITY GRAPH")
    plt.show()

import pandas as pd

def visualize_section_scores(ranked_sections, top_k=10):
    """
    Bar chart of top retrieved sections.
    """

    top = ranked_sections[:top_k]

    labels = [s["section_id"][:12] for s in top]
    scores = [s["score"] for s in top]

    plt.figure(figsize=(10, 4))
    plt.bar(labels, scores)

    plt.title("Top Retrieved Sections (Scoring Breakdown)")
    plt.ylabel("Score")
    plt.xticks(rotation=45)
    plt.show()


def visualize_global_communities(retrieved_communities):
    """
    Visualize GLOBAL retrieval results.
    """

    labels = [f"C{c['community_id']}" for c in retrieved_communities]
    scores = [c["score"] for c in retrieved_communities]

    plt.figure(figsize=(8, 4))
    plt.bar(labels, scores)

    plt.title("GLOBAL COMMUNITY RETRIEVAL")
    plt.ylabel("Cosine Similarity")
    plt.show()


def visualize_hybrid_flow(local_results, global_results):
    """
    Shows LOCAL vs GLOBAL contribution.
    """

    plt.figure(figsize=(6, 4))

    plt.bar(
        ["LOCAL", "GLOBAL"],
        [
            len(local_results),
            len(global_results)
        ]
    )

    plt.title("Hybrid Retrieval Split")
    plt.ylabel("Number of Retrieved Units")
    plt.show()


def print_top_paths(traversal_records, top_n=10):
    """
    Print most important reasoning paths.
    """

    print("\n============================")
    print("TOP TRAVERSAL PATHS")
    print("============================")

    for i, r in enumerate(traversal_records[:top_n]):
        print(
            f"{i+1}. {r['source']} → {r['edge']} → {r['target']} (H{r['hop']})"
        )