# 从零上手指南

这份指南按数据在系统中的真实流动顺序学习。每一步先运行、再观察、最后阅读对应代码。

## 第 0 步：跑通基线

```powershell
cd D:\AI\ai-engineer-roadmap\06_rag\explainable_rag
python -m ragx.cli query "RRF 为什么不直接融合原始分数？"
python -m ragx.cli evaluate
python -m pytest -q
```

先确认三个事实：查询能返回编号证据、检索 Trace 有双路分数、测试全部通过。

## 第 1 步：替换知识库

把自己的 UTF-8 `.md` 或 `.txt` 文件放进：

```text
fixtures/corpus/
```

学习时先用可公开的小文档，不要放论文版权全文、个人数据或公司机密。`text.py` 会递归读取文件，并生成：

```text
Document(document_id, source, text)
```

检查点：你能否说出 `document_id`、`source` 和 `text` 分别解决什么问题？

## 第 2 步：观察 Chunk

`chunking.py` 按空行识别段落，再把相邻段落组合到 `max_tokens` 限制内。每个 Chunk 保存：

```text
chunk_id
document_id
source
position
token_count
text
```

修改 `max_chunk_tokens` 后重新运行评测，观察召回是否变化。不要先假定更大或更小一定更好。

## 第 3 步：理解词元化

`text.py::tokenize()` 将英文和数字按单词处理，将中文按单字处理。这保证零依赖和可解释性，但无法很好表达中文词语边界。

这是一个有意保留的基线限制。后续可以比较：

```text
单字 tokenizer
vs 中文分词
vs 神经语义 embedding
```

## 第 4 步：分别理解两个检索器

`BM25Retriever` 使用词频、逆文档频率和长度归一化。它擅长精确术语。

`TfidfCosineRetriever` 生成可检查的词项权重向量，再计算余弦相似度。它仍然主要依赖词面重合，不等同于 Sentence Transformer 语义向量。

查询输出同时保留：

```text
bm25_score + bm25_rank
vector_score + vector_rank
matched_terms
```

检查点：如果 BM25 排名高而 TF-IDF 排名低，可能是哪类查询或文档？

## 第 5 步：理解 RRF 融合

两个检索器的原始分数不在同一量纲，不能随意相加。RRF 对每个检索器中的排名计算：

```text
1 / (k + rank)
```

然后求和。`retrieval.py::hybrid_search()` 保留所有原始分数和排名，因此最终排名可以追溯。

## 第 6 步：区分检索与回答

`pipeline.py::retrieve()` 只负责找证据；`answer()` 才负责组织回答。

当前回答器选择与查询词重合最多的句子，并加入 `[1]`、`[2]` 引用。这样不够流畅，但非常适合验证：

```text
检索是否找到正确证据？
回答是否使用了已检索证据？
```

如果完全没有词项命中，系统返回 `Insufficient evidence`，而不是编造答案。

## 第 7 步：运行检索评测

`fixtures/eval_cases.json` 中每条数据包含：

```json
{
  "id": "rrf",
  "query": "RRF 为什么不直接融合原始分数？",
  "relevant_documents": ["retrieval"]
}
```

`evaluation.py` 计算：

- Hit Rate@k：前 k 个结果中是否至少有一个相关文档；
- MRR：第一个相关文档排名倒数的平均值。

新增文档时，应同步增加人工标注查询。不要只用系统自己生成的答案作为真值。

## 第 8 步：分析 Bad Case

查询失败时按以下顺序检查：

```text
1. 相关事实是否存在于语料？
2. 解析后文本是否正确？
3. 事实是否完整落入某个 Chunk？
4. 查询与 Chunk 使用了哪些词元？
5. BM25 和 TF-IDF 各排第几？
6. RRF 是否改善或破坏了排名？
7. 正确 Chunk 已召回时，回答器是否忠实使用？
```

这能区分摄取、切分、检索、融合和生成五种失败层级。

## 第 9 步：升级为专业语义 RAG

不要同时替换所有组件。推荐一次只做一个实验：

1. 保留 BM25，把 TF-IDF 替换为 Sentence Transformers；
2. 使用同一评测集比较 Hit@k、MRR、延迟和内存；
3. 增加 cross-encoder reranker，并再次比较；
4. 指标明确改善后，再迁移到 Qdrant；
5. 最后接入 LLM 生成，并单独评测忠实度和引用正确性。

每次升级都应保留配置、指标、Bad Case 和结论，而不只是保存最终代码。
