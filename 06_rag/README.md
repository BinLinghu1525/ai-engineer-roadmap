# Retrieval-Augmented Generation

## Learning Goals

- Design RAG pipelines as measurable retrieval and generation systems.
- Understand trade-offs across ingestion, retrieval, reranking, and evaluation.
- Diagnose bad cases using evidence from intermediate pipeline stages.

## Key Topics

- Document parsing and chunking
- Embeddings and vector databases
- Dense retrieval, sparse retrieval, and BM25
- Hybrid retrieval, query rewriting, reranking, and metadata filtering
- Retrieval evaluation and answer evaluation
- Bad-case analysis

## Practice Tasks

- Compare chunking strategies on a small documented corpus.
- Design dense, sparse, and hybrid retrieval experiments.
- Define retrieval and answer-quality evaluation datasets and metrics.
- Categorize failure cases and propose targeted improvements.

## Completion Criteria

- Build a reproducible RAG baseline when this module begins.
- Measure retrieval separately from generation quality.
- Explain component choices, trade-offs, and observed failure modes.
- Document evaluation data, configuration, results, and limitations.

## Current evidence

- [`explainable_rag`](explainable_rag/) — zero-dependency hybrid retrieval baseline with visible BM25/TF-IDF/RRF scores, cited evidence, a labeled evaluation set, and automated tests.
