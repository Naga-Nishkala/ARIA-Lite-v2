# ARIA-Lite v2

### A Biomedical GraphRAG System for Explainable Scientific Question Answering

---

## Overview

ARIA-Lite v2 is an explainable GraphRAG system designed for biomedical literature retrieval and question answering.

Traditional Retrieval-Augmented Generation (RAG) systems retrieve chunks of text using semantic similarity and pass them directly to a Large Language Model (LLM). While effective, these systems often lack transparency, struggle with complex biomedical relationships, and provide limited explainability regarding why information was retrieved.

ARIA-Lite v2 addresses these limitations by:

* Constructing a biomedical knowledge graph from scientific literature
* Detecting latent research communities using graph clustering
* Routing user queries to either local graph traversal or global community retrieval
* Providing explainable retrieval paths
* Generating grounded answers using retrieved scientific evidence

The project combines ideas from GraphRAG, knowledge graphs, community detection, semantic retrieval, and biomedical NLP into a lightweight and interpretable research assistant.

---

# System Architecture

```text
User Query
     |
     v
Hybrid Query Router
     |
     +-----------------------+
     |                       |
     v                       v
LOCAL Retrieval         GLOBAL Retrieval
(Graph Traversal)      (Community Retrieval)
     |                       |
     +-----------+-----------+
                 |
                 v
         Context Builder
                 |
                 v
             LLM Layer
                 |
                 v
        Answer Generation
                 |
                 v
      Explainability Module
```

---

# Key Features

## 1. Biomedical Entity Extraction

Scientific entities are extracted using SciSpacy.

Examples:

* HER2
* Trastuzumab
* Breast Cancer
* PIK3CA
* PD-L1

These entities become nodes within the graph and serve as anchors for retrieval.

---

## 2. Knowledge Graph Construction

The graph contains multiple node types:

### Entity Nodes

Biomedical concepts identified from scientific literature.

Examples:

* HER2
* EGFR
* Trastuzumab
* PIK3CA

### Section Nodes

Scientific text sections extracted from PubMed articles.

Examples:

* Abstract sections
* Study findings
* Results sections

### Community Information

Each entity is assigned to a graph community discovered through clustering.

---

## 3. Community Detection

Biomedical concepts naturally form research communities.

Examples:

Community A:

* HER2
* Trastuzumab
* Breast Cancer

Community B:

* Immunotherapy
* PD-L1
* Checkpoint Inhibitors

Community C:

* Prognostic Modeling
* XGBoost
* Survival Prediction

Community detection enables high-level retrieval across scientific themes rather than isolated entities.

---

# Hybrid Query Routing

ARIA-Lite v2 uses a rule-based hybrid router.

The router decides whether a query requires:

## LOCAL Retrieval

Relationship-oriented questions.

Examples:

* How does trastuzumab target HER2?
* What is the role of PIK3CA mutations?
* Explain the interaction between EGFR and HER2.

These queries require graph traversal around specific entities.

---

## GLOBAL Retrieval

Overview and landscape questions.

Examples:

* What are recent trends in cancer AI?
* Compare supervised and unsupervised learning for cancer subtyping.
* Summarize breast cancer prognosis research.

These queries require retrieval at the community level.

---

# Local Retrieval Pipeline

Local retrieval focuses on mechanistic and entity-centric questions.

---

## Step 1: Entity Extraction

Example:

Query:

```text
How does trastuzumab target HER2 in breast cancer?
```

Extracted entities:

```text
trastuzumab
HER2
breast cancer
```

---

## Step 2: Seed Node Matching

Entities are matched against graph nodes.

```text
trastuzumab -> graph node
HER2 -> graph node
breast cancer -> graph node
```

---

## Step 3: Graph Traversal

Traversal expands through:

```text
Entity -> Section
Section -> Entity -> Section
```

Multi-hop traversal enables discovery of related scientific evidence.

---

## Step 4: Section Scoring

Sections are ranked using:

* Traversal path strength
* Hop distance
* Entity overlap
* Edge type weighting

Higher scores indicate stronger relevance to the query.

---

## Output

Top-ranked scientific sections are sent to the LLM.

---

# Global Retrieval Pipeline

Global retrieval focuses on research overviews and broad scientific questions.

---

## Step 1: Query Embedding

The user query is encoded using SPECTER embeddings.

---

## Step 2: Community Retrieval

Community summaries are embedded and compared using cosine similarity.

```text
Query
   |
   v
Community Embeddings
   |
   v
Top-k Communities
```

---

## Step 3: Context Construction

For each retrieved community:

* Community summary
* Representative sections
* Key entities

are collected into a context package.

---

## Output

Retrieved communities provide high-level scientific context for the LLM.

---

# Explainability Layer

A major goal of ARIA-Lite v2 is transparency.

---

## Local Explainability

For local retrieval, ARIA displays:

### Retrieved Sections

Top-ranked scientific sections.

### Traversal Paths

Example:

```text
HER2
  |
  +--MENTIONS-->
        Section A

trastuzumab
  |
  +--MENTIONS-->
        Section A
```

This reveals exactly why evidence was retrieved.

---

## Global Explainability

For global retrieval, ARIA displays:

### Retrieved Communities

Example:

```text
Community 2
Score: 0.78

Community 9
Score: 0.77

Community 3
Score: 0.74
```

### Community Summaries

Each retrieved community includes:

* Scientific theme
* Key biomedical concepts
* Supporting evidence

---

# Notebook Structure

## Notebook 1

PubMed Data Collection

```text
1_pubmed_data_downloader.ipynb
```

Downloads and stores biomedical literature.

---

## Notebook 2A

Data Cleaning & Preprocessing

```text
2A_data_cleaning_and_preprocessing.ipynb
```

Cleans article metadata and text.

---

## Notebook 2B

Dataset Creation

```text
2B_dataset_creator.ipynb
```

Creates processed datasets for graph construction.

---

## Notebook 3A

Entity Extraction

```text
3A_entity_extraction.ipynb
```

Extracts biomedical entities using SciSpacy.

---

## Notebook 3B

Entity Linking

```text
3B_entity_linking.ipynb
```

Links entities to graph nodes.

---

## Notebook 4

Graph Construction

```text
4_graph_builder.ipynb
```

Builds the biomedical knowledge graph.

---

## Notebook 5

Community Detection

```text
5_graph_clustering.ipynb
```

Discovers graph communities and generates summaries.

---

## Notebook 6

Hybrid Query Routing

```text
6_query_routing_experiments.ipynb
```

Routes queries to Local or Global retrieval.

---

## Notebook 7

Local Graph Traversal

```text
7_local_traversal.ipynb
```

Performs explainable graph-based retrieval.

---

## Notebook 8

Global Community Retrieval

```text
8_global_retrieval.ipynb
```

Performs community-level semantic retrieval.

---

## Notebook 9

End-to-End Question Answering

```text
9_answer_generation.ipynb
```

Combines:

* Query Routing
* Local Retrieval
* Global Retrieval
* Context Building
* LLM Generation
* Explainability

into a complete GraphRAG pipeline.

---

# Technologies Used

### NLP

* SciSpacy
* Sentence Transformers
* SPECTER

### Graph Analytics

* NetworkX

### Machine Learning

* Scikit-learn

### LLMs

Current:

* Phi-3 Mini

Planned:

* GPT
* Claude
* Gemini

---

# Current Capabilities

* Biomedical entity extraction
* Knowledge graph construction
* Community detection
* Local graph retrieval
* Global community retrieval
* Hybrid query routing
* Explainable retrieval
* LLM-based answer generation

---

# Future Work

## Hybrid Retrieval

Combine local and global retrieval for complex queries.

Example:

```text
How does trastuzumab target HER2 and what are recent advances?
```

Requires both mechanistic and landscape-level retrieval.

---

## Improved Explainability

Interactive graph visualization of retrieval paths.

---

## Better LLM Integration

Replace lightweight local models with stronger API-based models.

Potential options:

* GPT
* Claude
* Gemini

---

## Benchmark Evaluation

Develop evaluation datasets for:

* Retrieval quality
* Routing accuracy
* Answer correctness
* Explainability effectiveness

---

# Project Goal

ARIA-Lite v2 aims to demonstrate how graph-based retrieval, community-aware reasoning, and explainable AI can be integrated into a biomedical question-answering system that is transparent, interpretable, and grounded in scientific evidence.
