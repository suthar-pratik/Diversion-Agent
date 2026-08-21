import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from app.config import settings


class RAGEngine:
    """
    RAG engine backed by ChromaDB and orchestrated by LangChain.

    Public API (unchanged from the SQLite-based version):
        - add_resolved_incident(number, short_description, resolution, resolved_by)
        - search_similar_incidents(query, top_k=2) -> list of dicts
        - get_all_resolved_incidents() -> list of dicts (used by /api/history)
        - seed_historical_incidents(seed_list) -> bulk-loads historical KB

    Storage: ChromaDB collection at settings.CHROMA_PERSIST_DIR / settings.CHROMA_COLLECTION_NAME.
    Embeddings: settings.OLLAMA_EMBED_MODEL via langchain_community.embeddings.OllamaEmbeddings.
    """

    def __init__(self):
        # 1. LangChain embedding function wrapping the local Ollama model
        self.embeddings = OllamaEmbeddings(
            model=settings.OLLAMA_EMBED_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
        )

        # 2. Persistent ChromaDB client on disk
        self.chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )

        # 3. LangChain Chroma vector store bound to the named collection
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=self.embeddings,
        )

    # ---------- write paths ----------

    def add_resolved_incident(
        self,
        number: str,
        short_description: str,
        resolution: str,
        resolved_by: str,
    ) -> None:
        """
        Indexes a freshly resolved incident into ChromaDB so future similar
        incidents can match against it.
        """
        text = f"{short_description} {resolution}"
        metadata = {
            "number": number,
            "description": description,
            "root_cause": root_cause,
            "assignment_group": resolved_by,
        }
        # Use the incident number as the doc id so re-resolving the same
        # ticket doesn't create duplicate embeddings.
        doc = Document(page_content=text, metadata=metadata, id=number)
        self.vectorstore.add_documents([doc])
        print(f"Added resolved incident {number} to RAG (ChromaDB).")

    def seed_historical_incidents(self, historical_tickets: list) -> None:
        """
        Bulk-loads the historical seed list into ChromaDB on first startup.
        Skips if the collection already has documents (idempotent across restarts).
        """
        existing = self.chroma_client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )
        if existing.count() > 0:
            print(
                f"ChromaDB collection already has {existing.count()} docs; "
                "skipping seed."
            )
            return

        print(
            f"Seeding {len(historical_tickets)} historical resolved incidents "
            "into ChromaDB..."
        )
        documents = []
        for ticket in historical_tickets:
            text = f"{ticket['short_description']} {ticket['resolution']}"
            metadata = {
                "number": ticket["number"],
                "short_description": ticket["short_description"],
                "resolution": ticket["resolution"],
                "resolved_by": ticket["resolved_by"],
            }
            documents.append(
                Document(page_content=text, metadata=metadata, id=ticket["number"])
            )
        self.vectorstore.add_documents(documents)
        print("Historical incidents seeded into ChromaDB successfully.")


rag_engine = RAGEngine()
