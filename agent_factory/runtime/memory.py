"""
Memory and session management for agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import sqlite3
import json
from datetime import datetime


@dataclass
class Interaction:
    """Represents a single interaction in a session."""
    session_id: str
    input_text: str
    output_text: str
    timestamp: datetime
    metadata: Dict[str, Any]


class MemoryStore(ABC):
    """Abstract base class for memory stores."""
    
    @abstractmethod
    def save_interaction(
        self,
        session_id: str,
        input_text: str,
        output_text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Save an interaction to memory."""
        pass
    
    @abstractmethod
    def get_context(self, session_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get conversation context for a session."""
        pass
    
    @abstractmethod
    def get_history(self, session_id: str, limit: int = 50) -> List[Interaction]:
        """Get interaction history for a session."""
        pass
    
    @abstractmethod
    def clear_session(self, session_id: str) -> None:
        """Clear all interactions for a session."""
        pass


class SQLiteMemoryStore(MemoryStore):
    """SQLite implementation of memory store."""
    
    def __init__(self, db_path: str = "./agent_factory/memory.db"):
        """
        Initialize SQLite memory store.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                input_text TEXT NOT NULL,
                output_text TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT,
                INDEX idx_session_id (session_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_interaction(
        self,
        session_id: str,
        input_text: str,
        output_text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Save an interaction to memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO interactions (session_id, input_text, output_text, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            input_text,
            output_text,
            datetime.now().isoformat(),
            json.dumps(metadata or {}),
        ))
        
        conn.commit()
        conn.close()
    
    def get_context(self, session_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get conversation context for a session."""
        history = self.get_history(session_id, limit)
        
        context = {
            "recent_interactions": [
                {
                    "input": interaction.input_text,
                    "output": interaction.output_text,
                }
                for interaction in history
            ],
        }
        
        return context
    
    def get_history(self, session_id: str, limit: int = 50) -> List[Interaction]:
        """Get interaction history for a session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT input_text, output_text, timestamp, metadata
            FROM interactions
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        interactions = []
        for row in rows:
            interactions.append(Interaction(
                session_id=session_id,
                input_text=row[0],
                output_text=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                metadata=json.loads(row[3]) if row[3] else {},
            ))
        
        return list(reversed(interactions))  # Return in chronological order
    
    def clear_session(self, session_id: str) -> None:
        """Clear all interactions for a session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM interactions WHERE session_id = ?", (session_id,))
        
        conn.commit()
        conn.close()
