User Input
 ├─ Native OS execution (unchanged)
 └─ NLP pipeline
      ├─ Tool classifier (same as Stage 7)
      ├─ RAG Retriever
      │     ├─ Vector DB 1 (local dataset)
      │     └─ Vector DB 2 (public docs)
      ├─ Context assembly
      ├─ Local LLM (command synthesis)
      └─ Safety + confirmation

Dataset → Embeddings → FAISS index → Disk

1️⃣ Technology Choice (EXPLICIT & JUSTIFIED)
✅ FAISS (CPU)

Why this is the correct choice:

Offline

Fast

Deterministic

Widely accepted in research

Easy to serialize

You can explicitly justify this in your paper.