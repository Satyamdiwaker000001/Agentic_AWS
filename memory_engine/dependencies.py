from functools import lru_cache
import logging

from config import settings
from chunker import TextChunker
from embedding_engine import EmbeddingEngine
from memory_store import MemoryStore
from search_engine import SearchEngine
from agent_layer import AgentLayer

logger = logging.getLogger(__name__)

@lru_cache()
def get_chunker() -> TextChunker:
    logger.info("Initializing TextChunker singleton")
    return TextChunker(
        chunk_size=settings.chunk_size, 
        chunk_overlap=settings.chunk_overlap
    )

@lru_cache()
def get_embedding_engine() -> EmbeddingEngine:
    logger.info("Initializing EmbeddingEngine singleton")
    return EmbeddingEngine(model_name=settings.embedding_model_name)

@lru_cache()
def get_memory_store() -> MemoryStore:
    logger.info("Initializing MemoryStore singleton")
    return MemoryStore(db_dir=settings.chroma_db_dir)

@lru_cache()
def _get_search_engine() -> SearchEngine:
    logger.info("Initializing SearchEngine singleton")
    return SearchEngine(
        embedding_engine=get_embedding_engine(),
        memory_store=get_memory_store()
    )

def get_search_engine() -> SearchEngine:
    """Dependency injector for SearchEngine"""
    return _get_search_engine()

@lru_cache()
def _get_agent_layer() -> AgentLayer:
    logger.info("Initializing AgentLayer singleton")
    return AgentLayer()

def get_agent_layer() -> AgentLayer:
    """Dependency injector for AgentLayer"""
    return _get_agent_layer()
