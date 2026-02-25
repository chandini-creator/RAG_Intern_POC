# Internship Curriculum vs RAG Plan — Mapping & Gaps

This document maps **your internship phases (2–7)** and their concepts/deliverables to the **current RAG plan** (local-only: ingest → Chroma → query → Ollama). It shows what is **covered**, **partially covered**, or **missing**, and how to extend the plan so the full curriculum is included.

---

## Legend

| Symbol | Meaning |
|--------|--------|
| ✅ | **In plan** — Current RAG design + code will touch this |
| ⚠️ | **Partial** — Implicit or easy to add; needs explicit doc or small feature |
| ❌ | **Not in plan** — Need to add deliverable, doc, or module |

---

## Phase 2 (Week 2): LLM Fundamentals + Embeddings & Vector DBs

### 2️⃣ LLM Fundamentals

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| What is an LLM? | ⚠️ | Add **LLM_FUNDAMENTALS.md**: definition, how Ollama fits in |
| Tokens | ⚠️ | Doc: tokenization, cost/latency; optional: log token count in `/ask` |
| Context window | ⚠️ | Doc + in code: chunk retrieval respects context limit when building prompt |
| Temperature | ✅ | We use Ollama; expose `temperature` (and top_p) in `/ask` or config |
| Top_p | ✅ | Same: expose in API/config for Ollama |
| Hallucination | ⚠️ | **Deliverable**: doc “What causes hallucinations?” — link to RAG |
| Prompt engineering basics | ✅ | RAG prompt = system + context + user question |
| System vs User vs Assistant roles | ✅ | Use proper role structure in Ollama/LangChain messages |
| Streaming responses | ❌ | **Add**: optional streaming endpoint (e.g. `/ask/stream`) |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| Doc: What causes hallucinations? | ❌ | **Add** `docs/HALLUCINATIONS_AND_RAG.md` |
| Doc: Why RAG reduces hallucinations? | ⚠️ | Include in same doc (grounding in retrieved context) |
| Doc: What is context window limitation? | ❌ | **Add** to LLM fundamentals doc or separate |

---

### 3️⃣ Embeddings

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| What is an embedding? | ✅ | In ingest + query flow; add short doc |
| Semantic similarity | ✅ | Vector search in Chroma is semantic similarity |
| Cosine similarity | ⚠️ | Doc: explain; Chroma uses it by default — mention in embeddings doc |
| Chunking strategies | ✅ | Use at least one (e.g. recursive); **deliverable** compares 3 |
| Why chunk size matters | ✅ | Doc + configurable chunk size in code |
| Metadata importance | ✅ | Store source/filename in Chroma; use for filtering later |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| Compare 3 chunking strategies (fixed, recursive, semantic) | ⚠️ | **Add** code or script that runs all 3 + **Add** `docs/CHUNKING_STRATEGIES.md` |
| Explain which is better and why | ❌ | Same doc |

---

### 4️⃣ Vector Databases

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| Pinecone | ❌ | **Doc only** (comparison): when cloud vs local |
| Chroma | ✅ | In plan as primary vector DB |
| FAISS | ⚠️ | **Doc**: “When to use FAISS vs Pinecone?” — add FAISS as optional in-memory option |
| Qdrant | ❌ | **Doc only** in comparison |
| HNSW indexing | ⚠️ | **Doc**: Chroma/FAISS use approximate NN; explain HNSW briefly |
| Similarity search vs hybrid search | ⚠️ | **Doc**; optional: add BM25 later for hybrid |
| Metadata filtering | ✅ | Chroma supports it; use in retrieval (e.g. by source) |
| Multi-tenant indexing | ❌ | **Doc**: “How multi-tenant memory works?” — not in initial code |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| When to use FAISS vs Pinecone? | ❌ | **Add** `docs/VECTOR_DB_COMPARISON.md` |
| How multi-tenant memory works? | ❌ | Same doc or separate |

---

## Phase 3 (Week 3): RAG Architecture

### 5️⃣ RAG Architecture

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| Ingestion pipeline | ✅ | Load → Chunk → Embed → Index (Chroma) |
| Document loaders | ✅ | LangChain loaders (PDF, TXT) |
| Text splitters | ✅ | Recursive/semantic chunking |
| Embedding pipeline | ✅ | sentence-transformers → vectors |
| Indexing | ✅ | Chroma persist |
| Retrieval | ✅ | Vector search top-k |
| Reranking | ❌ | **Add** optional reranker step (e.g. cross-encoder) for “advanced RAG” |
| Response synthesis | ✅ | LLM (Ollama) with context |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| Diagram: User → Query → Embedding → Vector Search → Context → LLM → Response | ✅ | **Add** `docs/RAG_FLOW_DIAGRAM.md` (already described; formalize as diagram) |
| Explain retrieval failure scenarios | ❌ | **Add** to RAG doc |
| How to improve recall | ❌ | Same |
| How to improve precision | ❌ | Same |

---

### 6️⃣ Advanced RAG Concepts

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| Query rewriting | ❌ | **Doc**; optional: add step before retrieval |
| Self-query retriever | ❌ | **Doc**; optional: metadata + natural language |
| Parent-child document retrieval | ❌ | **Doc**; optional: small chunks for retrieval, larger for context |
| Reranking models | ❌ | **Doc**; optional: add reranker in pipeline |
| Multi-vector retrieval | ❌ | **Doc** |
| Hybrid search (BM25 + embeddings) | ❌ | **Doc**; optional: add later |
| RAG evaluation metrics | ❌ | **Doc**; Phase 7 ties in (Ragas, etc.) |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| Compare Basic RAG vs Advanced RAG vs Agentic RAG | ❌ | **Add** `docs/RAG_COMPARISON.md` |

---

## Phase 4 (Week 4): LangChain

### 7️⃣ LangChain Core Concepts

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| Chains | ✅ | RAG = chain (retriever + prompt + LLM) |
| Prompt templates | ✅ | LangChain prompt with context + question |
| Output parsers | ⚠️ | **Add** for structured answer (e.g. answer + sources) |
| Memory | ❌ | **Doc**: “Memory vs Vector DB”; Phase 6 for full memory |
| Tools | ❌ | **Doc**; Phase 5 LangGraph uses tools |
| Agents | ❌ | **Doc**: “Chain vs Agent”; Phase 5 builds agent |
| Callbacks | ⚠️ | **Doc**; optional: LangSmith/local callback for tracing |
| LCEL | ✅ | Use `retriever \| prompt \| llm` style where possible |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| Explain: Chain vs Agent | ❌ | **Add** `docs/LANGCHAIN_CONCEPTS.md` |
| Explain: Memory vs Vector DB | ❌ | Same |
| Explain: Tool vs Retriever | ❌ | Same |

---

### 8️⃣ Structured Output & JSON Mode

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| JSON schema validation | ✅ | FastAPI + Pydantic already; extend for `/ask` response |
| Function calling / Tool calling | ❌ | **Doc**; LangGraph phase can use tools |
| Guardrails | ❌ | **Doc** |
| Response parsing | ✅ | Pydantic models for API |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| Why strict JSON mode matters in production? | ❌ | **Add** `docs/STRUCTURED_OUTPUT.md` |

---

## Phase 5 (Week 5): LangGraph (Agentic Systems)

### 9️⃣ LangGraph Concepts

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| Nodes, Edges, State | ❌ | **Add** LangGraph module: e.g. Retrieve → Validate → Generate |
| Conditional branching | ❌ | Same |
| Multi-step reasoning | ❌ | Same |
| Retry nodes, Tool execution nodes | ❌ | **Doc** + optional graph nodes |
| Memory persistence, Checkpointing | ❌ | **Doc**; Phase 6 memory |
| Why LangGraph > traditional agents | ❌ | **Doc** |
| Deterministic vs non-deterministic flows | ❌ | **Doc** |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| Diagram: Multi-step agent (Retrieve → Validate → Rewrite → Generate → Verify) | ❌ | **Add** `docs/LANGGRAPH_AGENT_DIAGRAM.md` + optional code |

---

## Phase 6: Agent Memory Systems

### Memory concepts

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| Short-term / Long-term / Semantic / Episodic memory | ❌ | **Doc** |
| Memory decay, Importance scoring, Retrieval scoring | ❌ | **Doc** |
| Zep, Mem0, Vector memory, Knowledge graph memory | ❌ | **Doc** (concept tools) |

**Deliverables:**

| Deliverable | In plan? | Action |
|-------------|----------|--------|
| How memory improves UX? When NOT to use memory? | ❌ | **Add** `docs/AGENT_MEMORY.md` |

---

## Phase 7: Evaluation & Monitoring

### 10️⃣ LLM Evaluation

| Concept | In plan? | Where / How to cover |
|--------|----------|----------------------|
| RAG evaluation, Groundedness, Faithfulness, Answer relevance | ❌ | **Doc**; optional: Ragas script |
| Retrieval recall | ❌ | **Doc** |
| Latency tracking | ⚠️ | Add middleware or logging for `/ask` latency |
| Token cost tracking | ❌ | **Doc** (Ollama local = no $ cost; still token count) |
| Hallucination detection | ❌ | **Doc** |
| LangSmith, TruLens, Ragas | ❌ | **Doc** (tools to explore) |

---

## Summary: What the current plan includes vs what to add

| Category | In current plan | To add |
|----------|------------------|--------|
| **Core RAG flow** | ✅ Ingest + Query (Chroma, Ollama, embeddings) | — |
| **LLM fundamentals** | ✅ Temperature, top_p, roles, prompt | Streaming, 3 docs (hallucinations, context window, RAG) |
| **Embeddings** | ✅ Embeddings, chunking, metadata | Doc on cosine similarity; 3-way chunking comparison + doc |
| **Vector DBs** | ✅ Chroma, metadata filtering | Docs: FAISS vs Pinecone, multi-tenant, HNSW |
| **RAG architecture** | ✅ Full pipeline, diagram | Doc: retrieval failures, recall/precision; optional reranking |
| **Advanced RAG** | — | Doc: query rewrite, rerank, hybrid; Basic vs Advanced vs Agentic |
| **LangChain** | ✅ Chains, prompts, LCEL, retrievers | Docs: Chain vs Agent, Memory vs Vector DB, Tool vs Retriever |
| **Structured output** | ✅ Pydantic/JSON in API | Doc: why strict JSON in production |
| **LangGraph** | — | Doc + diagram (Retrieve → Validate → Rewrite → Generate → Verify); optional code |
| **Agent memory** | — | Doc: when memory helps, when not; concept tools |
| **Evaluation** | — | Doc + optional: latency log, Ragas/TruLens/LangSmith |

---

## Recommended next steps (in order)

1. **Implement core RAG** (ingest + `/ask` with Chroma + Ollama) so the app demonstrates the flow.
2. **Add deliverable docs** under `docs/` for each phase (see “Action” in tables above).
3. **Add optional code** where useful: streaming `/ask`, 3 chunking strategies, FAISS option, reranker, then LangGraph agent and memory if time.

Using this mapping, the **same RAG plan** (local-only drug-doc RAG) **can cover all curriculum concepts** by adding the listed documents and optional features. The codebase stays one coherent project; the curriculum is covered by implementation + explicit deliverables in `docs/`.
