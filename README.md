# ARIA-Lite v2

### Explainable GraphRAG for Biomedical Literature

ARIA-Lite v2 is a biomedical GraphRAG system that combines knowledge graphs, community detection, graph traversal, semantic retrieval, and LLMs to answer scientific questions with explainable evidence retrieval.

---

## Pipeline

```text
PubMed Articles
      ↓
Entity Extraction (SciSpacy)
      ↓
Entity Linking
      ↓
Knowledge Graph Construction
      ↓
Community Detection
      ↓
Community Summarization
      ↓

                User Query
                      ↓
              Hybrid Router
               /         \
              /           \
         LOCAL           GLOBAL
    Graph Traversal   Community Retrieval
              \           /
               \         /
                Context Builder
                      ↓
                     LLM
                      ↓
             Generated Answer
                      ↓
              Explainability
```

---

## Key Features

* Biomedical entity extraction using SciSpacy
* Knowledge graph construction from scientific literature
* Community detection for scientific theme discovery
* Hybrid query routing (Local vs Global retrieval)
* Multi-hop graph traversal for mechanistic questions
* Community-level retrieval for overview questions
* Explainable retrieval paths and evidence tracking
* LLM-powered biomedical question answering
* Modular GraphRAG architecture

---

## Repository Structure

```text
notebook/
├── 1_pubmed_data_downloader.ipynb
├── 2A_data_cleaning_and_preprocessing.ipynb
├── 2B_dataset_creator.ipynb
├── 3A_entity_extraction.ipynb
├── 3B_entity_linking.ipynb
├── 4_graph_builder.ipynb
├── 5_graph_clustering.ipynb
├── 6_query_routing_experiments.ipynb
├── 7_local_traversal.ipynb
├── 8_global_retrieval.ipynb
├── 9_llm_orchestrator.ipynb

src/
├── router.py
├── local_traversal.py
├── global_retrieval.py
└── visualization.py
```

---

## Retrieval Modes

### Local Retrieval

Used for entity-specific and mechanistic questions.

**Example**

```text
How does trastuzumab target HER2?
```

Pipeline:

```text
Query
 ↓
Entity Extraction
 ↓
Graph Traversal
 ↓
Section Ranking
 ↓
LLM Answer
```

---

### Global Retrieval

Used for overview and comparison questions.

**Example**

```text
Compare supervised and unsupervised learning for cancer subtyping.
```

Pipeline:

```text
Query
 ↓
Community Retrieval
 ↓
Community Ranking
 ↓
Context Building
 ↓
LLM Answer
```

---

## Explainability

ARIA-Lite v2 exposes retrieval decisions through:

* Retrieved communities
* Retrieved scientific sections
* Traversal paths
* Community rankings
* Retrieval scores

This allows users to inspect why evidence was retrieved before trusting the generated answer.

---

## Current Stack

* Python
* SciSpacy
* NetworkX
* Sentence Transformers
* SPECTER
* Scikit-learn
* HuggingFace Transformers

---

## Future Work

* Hybrid Local + Global retrieval
* Interactive graph visualization
* Stronger LLM backends (GPT / Claude)
* Streamlit deployment
* Retrieval benchmarking

---

## Project Goal

Build an interpretable biomedical research assistant that combines graph-based reasoning, community-aware retrieval, and LLM generation while maintaining transparent evidence retrieval.
