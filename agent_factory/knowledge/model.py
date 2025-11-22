"""
Knowledge Pack data models.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod


@dataclass
class DataSource:
    """Data source for knowledge pack."""
    type: str  # "directory", "url", "database", "api"
    path: Optional[str] = None
    url: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingConfig:
    """Embedding model configuration."""
    model: str = "text-embedding-3-small"
    provider: str = "openai"  # "openai", "anthropic", "local"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrieverConfig:
    """Retriever configuration."""
    type: str = "vector_store"  # "vector_store", "bm25", "hybrid"
    vector_store: str = "chroma"  # "chroma", "pinecone", "weaviate"
    top_k: int = 5
    similarity_threshold: float = 0.7
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgePack:
    """
    Knowledge Pack - Pluggable RAG module for agents.
    
    Example:
        >>> pack = KnowledgePack(
        ...     id="academic-research",
        ...     name="Academic Research Pack",
        ...     domain="academic",
        ...     data_sources=[DataSource(type="directory", path="./data/papers")],
        ... )
    """
    id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    domain: str = "general"
    tags: List[str] = field(default_factory=list)
    data_sources: List[DataSource] = field(default_factory=list)
    embedding_config: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    retriever_config: RetrieverConfig = field(default_factory=RetrieverConfig)
    metadata: Dict[str, Any] = field(default_factory=dict)


class KnowledgeRetriever(ABC):
    """
    Abstract base class for knowledge retrievers.
    
    Implementations:
    - VectorStoreRetriever: Vector similarity search
    - BM25Retriever: Keyword-based retrieval
    - HybridRetriever: Combines vector + keyword
    """
    
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of retrieved documents with content and metadata
        """
        pass
    
    @abstractmethod
    def load(self, knowledge_pack: KnowledgePack) -> None:
        """
        Load knowledge pack data.
        
        Args:
            knowledge_pack: Knowledge pack to load
        """
        pass
