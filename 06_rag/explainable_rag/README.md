# Explainable Hybrid RAG Baseline

一个可以立即运行、逐层检查的 RAG 学习项目。它不依赖 LangChain、向量数据库或外部 API，目的是先把 RAG 的数据流、评分和评测真正看懂，再替换为生产组件。

## 为什么不直接复制大型项目

大型框架适合交付，但第一天容易隐藏 Chunk、词元、分数、排名融合和失败层级。本项目保留生产系统应有的模块边界，同时让每个中间结果可见。

## 架构

```text
Markdown/TXT
→ Document
→ paragraph-aware Chunk
→ BM25 sparse retrieval ──┐
→ TF-IDF cosine vector ───┤
                         RRF
                          ↓
                 ranked evidence
                          ↓
            extractive cited answer
                          ↓
                  Hit@k / MRR eval
```

## 立即运行

```powershell
cd D:\AI\ai-engineer-roadmap\06_rag\explainable_rag
python -m ragx.cli query "RRF 为什么适合融合不同检索器？"
python -m ragx.cli evaluate
python -m pytest -q
```

不需要 API Key，也不需要安装第三方包。

完整学习顺序见 [`LEARNING_GUIDE.md`](LEARNING_GUIDE.md)。

当前 6 条人工标注样例在 `top_k=3` 下得到 `Hit Rate@3 = 1.0`、
`MRR = 1.0`。这只是用于确认评测闭环能运行的合成小样本，不代表真实业务质量；扩大语料和评测集后指标通常会下降。

## 你会看到什么

每个检索结果都会展示：

- `chunk_id`、来源文件与原始文本；
- BM25 原始分数及排名；
- TF-IDF 余弦分数及排名；
- RRF 融合分数及最终排名；
- 查询与 Chunk 实际匹配的词项；
- 回答使用的编号证据。

## 项目结构

```text
explainable_rag/
├── ragx/
│   ├── models.py       # 数据契约
│   ├── text.py         # 文档加载与词元化
│   ├── chunking.py     # 段落感知切分
│   ├── retrieval.py    # BM25、TF-IDF、RRF
│   ├── pipeline.py     # 检索与证据式回答
│   ├── evaluation.py   # Hit@k 与 MRR
│   └── cli.py          # 命令行入口
├── fixtures/
│   ├── corpus/         # 可公开的示例知识库
│   └── eval_cases.json # 人工标注评测集
└── tests/
```

## 关键设计选择

1. **Chunk 保留来源**：每个 Chunk 有稳定 ID、文件名、位置和词元数。
2. **双路检索分开评分**：先保留 BM25 与 TF-IDF 原始结果，再融合。
3. **RRF 使用排名融合**：避免错误地直接相加不同量纲的原始分数。
4. **检索和生成分开评测**：先证明证据能被找到，再评价回答是否忠实。
5. **确定性基线**：相同输入产生相同结果，适合测试和回归比较。

## 当前限制

- TF-IDF 是透明的向量基线，不理解深层语义；下一版可替换为 Sentence Transformers。
- 目前支持 UTF-8 Markdown/TXT；PDF 解析应作为独立、可测试的摄取层加入。
- 回答器是抽取式证据汇总，不调用 LLM，因此不会产生流畅综合回答。
- 示例评测集很小，只能验证工程闭环，不能代表真实业务质量。

## 专业化升级顺序

```text
V1 当前透明基线
→ V2 Sentence Transformers 稠密向量 + reranker
→ V3 Qdrant 持久化、过滤与批量索引
→ V4 OpenAI-compatible 生成器 + 引用约束
→ V5 50+ 条人工评测集、bad-case taxonomy、回归报告
→ V6 FastAPI、日志、缓存、Docker 和 CI
```

参考项目：[Sentence Transformers](https://github.com/UKPLab/sentence-transformers)、[Qdrant](https://github.com/qdrant/qdrant)、[Haystack](https://github.com/deepset-ai/haystack)。
