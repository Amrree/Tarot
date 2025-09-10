"""
Memory system for Tarot Studio AI.

This module handles semantic memory storage and retrieval for AI conversations,
allowing the AI to remember past readings, people, and contexts.
"""

import json
import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import hashlib
import logging

logger = logging.getLogger(__name__)

@dataclass
class MemoryEntry:
    """A memory entry for AI context."""
    id: str
    entity_type: str  # 'person', 'place', 'concept', 'reading', 'card'
    entity_name: str
    description: str
    context: str
    importance_score: float
    last_mentioned: datetime
    created_at: datetime

@dataclass
class MemorySearchResult:
    """Result from memory search."""
    memory: MemoryEntry
    relevance_score: float
    context_snippet: str

class MemoryStore:
    """Manages semantic memory for AI conversations."""
    
    def __init__(self, db_path: str = "tarot_studio.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize memory database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create memories table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL,
                entity_name TEXT NOT NULL,
                description TEXT,
                context TEXT,
                importance_score REAL DEFAULT 1.0,
                last_mentioned TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for efficient searching
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memory_entity 
            ON memories(entity_type, entity_name)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memory_importance 
            ON memories(importance_score)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memory_last_mentioned 
            ON memories(last_mentioned)
        """)
        
        conn.commit()
        conn.close()
    
    def store_memory(
        self, 
        entity_type: str, 
        entity_name: str, 
        description: str = "", 
        context: str = "",
        importance_score: float = 1.0
    ) -> str:
        """Store a new memory entry."""
        memory_id = self._generate_memory_id(entity_type, entity_name, context)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if memory already exists
        cursor.execute("""
            SELECT id, importance_score FROM memories 
            WHERE entity_type = ? AND entity_name = ? AND context = ?
        """, (entity_type, entity_name, context))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing memory
            new_importance = max(existing[1], importance_score)
            cursor.execute("""
                UPDATE memories 
                SET importance_score = ?, last_mentioned = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_importance, existing[0]))
            memory_id = existing[0]
        else:
            # Insert new memory
            cursor.execute("""
                INSERT INTO memories 
                (id, entity_type, entity_name, description, context, importance_score)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (memory_id, entity_type, entity_name, description, context, importance_score))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Stored memory: {entity_type}:{entity_name}")
        return memory_id
    
    def search_memories(
        self, 
        query: str, 
        entity_types: Optional[List[str]] = None,
        limit: int = 10,
        min_importance: float = 0.1
    ) -> List[MemorySearchResult]:
        """Search memories by query."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build search query
        where_conditions = ["importance_score >= ?"]
        params = [min_importance]
        
        if entity_types:
            placeholders = ",".join(["?" for _ in entity_types])
            where_conditions.append(f"entity_type IN ({placeholders})")
            params.extend(entity_types)
        
        # Add text search
        where_conditions.append("""
            (entity_name LIKE ? OR description LIKE ? OR context LIKE ?)
        """)
        search_term = f"%{query}%"
        params.extend([search_term, search_term, search_term])
        
        sql = f"""
            SELECT id, entity_type, entity_name, description, context, 
                   importance_score, last_mentioned, created_at
            FROM memories 
            WHERE {' AND '.join(where_conditions)}
            ORDER BY importance_score DESC, last_mentioned DESC
            LIMIT ?
        """
        params.append(limit)
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        conn.close()
        
        # Convert to MemorySearchResult objects
        memory_results = []
        for row in results:
            memory = MemoryEntry(
                id=row[0],
                entity_type=row[1],
                entity_name=row[2],
                description=row[3],
                context=row[4],
                importance_score=row[5],
                last_mentioned=datetime.fromisoformat(row[6]),
                created_at=datetime.fromisoformat(row[7])
            )
            
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(query, memory)
            
            memory_results.append(MemorySearchResult(
                memory=memory,
                relevance_score=relevance_score,
                context_snippet=self._extract_context_snippet(memory.context, query)
            ))
        
        # Sort by relevance score
        memory_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return memory_results
    
    def get_recent_memories(self, days: int = 30, limit: int = 20) -> List[MemoryEntry]:
        """Get recently mentioned memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cursor.execute("""
            SELECT id, entity_type, entity_name, description, context, 
                   importance_score, last_mentioned, created_at
            FROM memories 
            WHERE last_mentioned >= ?
            ORDER BY last_mentioned DESC, importance_score DESC
            LIMIT ?
        """, (cutoff_date.isoformat(), limit))
        
        results = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in results:
            memories.append(MemoryEntry(
                id=row[0],
                entity_type=row[1],
                entity_name=row[2],
                description=row[3],
                context=row[4],
                importance_score=row[5],
                last_mentioned=datetime.fromisoformat(row[6]),
                created_at=datetime.fromisoformat(row[7])
            ))
        
        return memories
    
    def extract_entities_from_text(self, text: str) -> List[Tuple[str, str, str]]:
        """Extract potential entities from text."""
        entities = []
        
        # Simple entity extraction (in a real implementation, you'd use NLP)
        words = text.lower().split()
        
        # Look for potential person names (capitalized words)
        capitalized_words = [word for word in text.split() if word[0].isupper() and len(word) > 2]
        for word in capitalized_words:
            if word not in ['The', 'This', 'That', 'These', 'Those', 'Tarot', 'Card', 'Reading']:
                entities.append(('person', word, f"Mentioned in: {text[:100]}..."))
        
        # Look for card names
        card_keywords = ['card', 'tarot', 'reading', 'spread']
        for keyword in card_keywords:
            if keyword in text.lower():
                # Extract surrounding context
                start = max(0, text.lower().find(keyword) - 50)
                end = min(len(text), text.lower().find(keyword) + 100)
                context = text[start:end]
                entities.append(('concept', keyword, context))
        
        # Look for emotional states
        emotions = ['happy', 'sad', 'angry', 'excited', 'worried', 'confident', 'anxious']
        for emotion in emotions:
            if emotion in text.lower():
                entities.append(('emotion', emotion, f"Emotional state mentioned: {text[:100]}..."))
        
        return entities
    
    def store_reading_context(self, reading_data: Dict[str, Any]) -> List[str]:
        """Store context from a reading."""
        memory_ids = []
        
        # Store reading as entity
        reading_id = reading_data.get('id', 'unknown')
        reading_title = reading_data.get('title', 'Untitled Reading')
        
        memory_ids.append(self.store_memory(
            entity_type='reading',
            entity_name=reading_title,
            description=f"Reading from {reading_data.get('created_at', 'unknown date')}",
            context=json.dumps(reading_data),
            importance_score=2.0
        ))
        
        # Store cards as entities
        for card in reading_data.get('cards', []):
            card_name = card.get('name', 'Unknown Card')
            memory_ids.append(self.store_memory(
                entity_type='card',
                entity_name=card_name,
                description=f"Card in {card.get('position', 'unknown position')}",
                context=f"Reading: {reading_title}",
                importance_score=1.5
            ))
        
        # Extract entities from question/interpretation
        question = reading_data.get('question', '')
        interpretation = reading_data.get('interpretation', '')
        
        for text in [question, interpretation]:
            if text:
                entities = self.extract_entities_from_text(text)
                for entity_type, entity_name, context in entities:
                    memory_ids.append(self.store_memory(
                        entity_type=entity_type,
                        entity_name=entity_name,
                        description=f"Extracted from reading context",
                        context=context,
                        importance_score=1.0
                    ))
        
        return memory_ids
    
    def get_conversation_context(self, query: str, max_memories: int = 5) -> List[Dict[str, Any]]:
        """Get relevant memories for conversation context."""
        # Search for relevant memories
        search_results = self.search_memories(query, limit=max_memories)
        
        # Also get recent memories
        recent_memories = self.get_recent_memories(days=7, limit=max_memories)
        
        # Combine and deduplicate
        all_memories = {}
        
        for result in search_results:
            memory = result.memory
            all_memories[memory.id] = {
                'entity_type': memory.entity_type,
                'entity_name': memory.entity_name,
                'description': memory.description,
                'context': memory.context,
                'importance_score': memory.importance_score,
                'relevance_score': result.relevance_score
            }
        
        for memory in recent_memories:
            if memory.id not in all_memories:
                all_memories[memory.id] = {
                    'entity_type': memory.entity_type,
                    'entity_name': memory.entity_name,
                    'description': memory.description,
                    'context': memory.context,
                    'importance_score': memory.importance_score,
                    'relevance_score': 0.5  # Default relevance for recent memories
                }
        
        # Convert to list and sort by relevance
        context_memories = list(all_memories.values())
        context_memories.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return context_memories[:max_memories]
    
    def _generate_memory_id(self, entity_type: str, entity_name: str, context: str) -> str:
        """Generate unique memory ID."""
        content = f"{entity_type}:{entity_name}:{context}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _calculate_relevance_score(self, query: str, memory: MemoryEntry) -> float:
        """Calculate relevance score for memory search."""
        query_lower = query.lower()
        score = 0.0
        
        # Exact name match
        if query_lower in memory.entity_name.lower():
            score += 2.0
        
        # Partial name match
        if any(word in memory.entity_name.lower() for word in query_lower.split()):
            score += 1.0
        
        # Description match
        if query_lower in memory.description.lower():
            score += 1.5
        
        # Context match
        if query_lower in memory.context.lower():
            score += 1.0
        
        # Boost by importance score
        score += memory.importance_score * 0.5
        
        # Boost recent memories
        days_ago = (datetime.now() - memory.last_mentioned).days
        if days_ago < 7:
            score += 0.5
        elif days_ago < 30:
            score += 0.2
        
        return score
    
    def _extract_context_snippet(self, context: str, query: str, max_length: int = 100) -> str:
        """Extract relevant snippet from context."""
        if len(context) <= max_length:
            return context
        
        query_lower = query.lower()
        context_lower = context.lower()
        
        # Find query position in context
        query_pos = context_lower.find(query_lower)
        
        if query_pos != -1:
            # Center snippet around query
            start = max(0, query_pos - max_length // 2)
            end = min(len(context), start + max_length)
            snippet = context[start:end]
            
            if start > 0:
                snippet = "..." + snippet
            if end < len(context):
                snippet = snippet + "..."
            
            return snippet
        else:
            # Return beginning of context
            return context[:max_length] + "..."
    
    def cleanup_old_memories(self, days_threshold: int = 365, min_importance: float = 0.5):
        """Clean up old, low-importance memories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        
        cursor.execute("""
            DELETE FROM memories 
            WHERE last_mentioned < ? AND importance_score < ?
        """, (cutoff_date.isoformat(), min_importance))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Cleaned up {deleted_count} old memories")
        return deleted_count

# Example usage and testing
def test_memory_store():
    """Test the memory store functionality."""
    store = MemoryStore("test_memory.db")
    
    # Store some test memories
    store.store_memory(
        entity_type='person',
        entity_name='Sarah',
        description='Friend who asked about career reading',
        context='Sarah asked about her career prospects in a three-card reading',
        importance_score=2.0
    )
    
    store.store_memory(
        entity_type='card',
        entity_name='The Sun',
        description='Card that appeared in Sarah\'s reading',
        context='The Sun appeared in the future position, indicating success',
        importance_score=1.5
    )
    
    store.store_memory(
        entity_type='concept',
        entity_name='career',
        description='Career-related reading topic',
        context='Multiple readings have focused on career guidance',
        importance_score=1.0
    )
    
    # Search memories
    print("Searching for 'Sarah':")
    results = store.search_memories('Sarah')
    for result in results:
        print(f"  {result.memory.entity_type}: {result.memory.entity_name} (score: {result.relevance_score:.2f})")
    
    print("\nSearching for 'career':")
    results = store.search_memories('career')
    for result in results:
        print(f"  {result.memory.entity_type}: {result.memory.entity_name} (score: {result.relevance_score:.2f})")
    
    # Get conversation context
    print("\nGetting conversation context for 'Sarah career':")
    context = store.get_conversation_context('Sarah career')
    for memory in context:
        print(f"  {memory['entity_type']}: {memory['entity_name']}")

if __name__ == "__main__":
    test_memory_store()