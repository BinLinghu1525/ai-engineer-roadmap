# Transformers

## Learning Goals

- Understand how Transformer components transform token representations.
- Trace information flow through attention and feed-forward blocks.
- Connect architecture concepts to efficient autoregressive inference.

## Key Topics

- Tokenization, embeddings, and positional information
- Queries, keys, values, and self-attention
- Multi-head attention and causal masking
- Feed-forward networks, residual connections, and normalization
- KV cache, RoPE, and inference

## Practice Tasks

- Calculate a small attention example by hand and verify tensor shapes.
- Visualize causal masks and compare positional approaches conceptually.
- Trace one token through a Transformer block.
- Benchmark cached and uncached inference on a small controlled example.

## Completion Criteria

- Explain every major Transformer block and its input/output shapes.
- Describe causal masking, KV caching, and RoPE without relying on slogans.
- Implement and test selected components only when the module begins.
- Document architecture and inference trade-offs accurately.
