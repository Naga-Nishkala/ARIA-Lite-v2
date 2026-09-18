# ARIA-Lite v2 — Local Retrieval Evaluation
## Benchmark
- Benchmark: `aria_local_benchmark_v2.json`
- Queries: 10
- Retrieval run: `local_retrieval_v1`

## Aggregate Performance
| Metric | Mean |
|---|---:|
| precision@1 | 0.2000 |
| precision@3 | 0.2667 |
| precision@5 | 0.2800 |
| precision@10 | 0.1900 |
| recall@1 | 0.0343 |
| recall@3 | 0.1151 |
| recall@5 | 0.1966 |
| recall@10 | 0.2716 |
| f1@5 | 0.2260 |
| f1@10 | 0.2177 |
| MRR | 0.3765 |
| average_precision | 0.2327 |

## Query-Level Results
| Query | Anchor | Precision@5 | Recall@5 | F1@5 | MRR |
|---|---|---:|---:|---:|---:|
| Q1 | tamoxifen | 0.400 | 0.222 | 0.286 | 0.500 |
| Q2 | tumor-infiltrating lymphocytes | 0.400 | 0.400 | 0.400 | 1.000 |
| Q3 | trastuzumab | 0.000 | 0.000 | 0.000 | 0.000 |
| Q4 | pik3ca | 0.200 | 0.143 | 0.167 | 0.333 |
| Q5 | pd-l1 | 0.600 | 0.429 | 0.500 | 1.000 |
| Q6 | explainable artificial intelligence | 0.000 | 0.000 | 0.000 | 0.012 |
| Q7 | olaparib | 0.200 | 0.250 | 0.222 | 0.200 |
| Q8 | spatial transcriptomics | 0.000 | 0.000 | 0.000 | 0.053 |
| Q9 | paclitaxel | 0.400 | 0.222 | 0.286 | 0.333 |
| Q10 | estrogen receptor | 0.600 | 0.300 | 0.400 | 0.333 |

## Notes
- Retrieval implementation was evaluated as-is.
- No retrieval logic was modified during evaluation.
- Gold evidence is taken from the benchmark's `gold_evidence` node IDs.
- Metrics are based on retrieved section/node IDs.
