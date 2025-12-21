Prompt
 → Embedding
 → Similarity (cosine)
 → Top-k tools
 → Predicted tool

 🎯 What we will do (high-level, structured)

1️⃣ Use your dataset
data/security_nlp_cli_10000.csv
2️⃣ Generate embeddings for dataset prompts
3️⃣ Store embeddings in memory (for now)
4️⃣ Compute cosine similarity with user prompt
5️⃣ Predict the best tool
6️⃣ Plug this into existing backend (no CLI change)