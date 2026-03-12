import os
from typing import List, Tuple

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions

from utils.config import settings


class RagService:
    def __init__(self) -> None:
        self.client = chromadb.Client(
            ChromaSettings(
                persist_directory=settings.chroma_dir,
            )
        )
        self.collection = self.client.get_or_create_collection(
            name="company_knowledge",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            ),
        )

    def ingest_data_dir(self) -> None:
        """Простая индексация всех .txt файлов из каталога data."""
        doc_id = 0
        for filename in os.listdir(settings.data_dir):
            if not filename.endswith(".txt"):
                continue
            path = os.path.join(settings.data_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            if not text.strip():
                continue
            doc_id += 1
            self.collection.add(
                ids=[f"doc_{doc_id}"],
                documents=[text],
                metadatas=[{"filename": filename, "path": path}],
            )

    def query(self, question: str, top_k: int = 3) -> Tuple[str, List[dict]]:
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k,
        )
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        context_parts = []
        for doc, meta in zip(documents, metadatas):
            fname = meta.get("filename", "unknown")
            context_parts.append(f"[Источник: {fname}]\n{doc}")
        context = "\n\n".join(context_parts)
        return context, metadatas

    def stats(self) -> str:
        count = self.collection.count()
        return (
            f"RAG /stats\n"
            f"- Документов в коллекции: {count}\n"
            f"- Каталог данных: {settings.data_dir}\n"
            f"- Каталог ChromaDB: {settings.chroma_dir}\n"
            f"- Для работы с базой знаний используйте режим /mode rag"
        )


rag_service = RagService()

