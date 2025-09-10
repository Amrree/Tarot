"""
Simple JSON-based database implementation for Tarot Studio.
Fallback implementation when SQLAlchemy is not available.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import uuid

class SimpleDB:
    """Simple JSON-based database for Tarot Studio."""
    
    def __init__(self, db_path: str = "tarot_studio_data"):
        """Initialize the simple database."""
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        # File paths for different data types
        self.cards_file = self.db_path / "cards.json"
        self.spreads_file = self.db_path / "spreads.json"
        self.readings_file = self.db_path / "readings.json"
        self.conversations_file = self.db_path / "conversations.json"
        self.memories_file = self.db_path / "memories.json"
        self.settings_file = self.db_path / "settings.json"
        
        # Initialize data structures
        self.cards = self._load_data(self.cards_file, [])
        self.spreads = self._load_data(self.spreads_file, [])
        self.readings = self._load_data(self.readings_file, [])
        self.conversations = self._load_data(self.conversations_file, [])
        self.memories = self._load_data(self.memories_file, [])
        self.settings = self._load_data(self.settings_file, {})
        
        # Initialize with default data if empty
        self._initialize_defaults()
    
    def _load_data(self, file_path: Path, default_value):
        """Load data from JSON file."""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return default_value
        return default_value
    
    def _save_data(self, file_path: Path, data):
        """Save data to JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving data to {file_path}: {e}")
    
    def _initialize_defaults(self):
        """Initialize with default data if empty."""
        if not self.cards:
            self._load_default_cards()
        if not self.spreads:
            self._load_default_spreads()
    
    def _load_default_cards(self):
        """Load default cards from the deck module."""
        try:
            from tarot_studio.deck.deck import Deck
            # Load deck from the JSON file
            deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
            
            for card in deck._original_order:
                card_data = {
                    'id': card.id,
                    'name': card.name,
                    'arcana': card.arcana.value,
                    'suit': card.suit.value if card.suit else None,
                    'number': card.number,
                    'element': card.element.value if card.element else None,
                    'keywords': card.keywords,
                    'polarity': getattr(card, 'polarity', 0.0),
                    'intensity': getattr(card, 'intensity', 0.5),
                    'upright_meaning': card.upright_meaning,
                    'reversed_meaning': card.reversed_meaning,
                    'influence_rules': getattr(card, 'influence_rules', []),
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
                self.cards.append(card_data)
            
            self._save_data(self.cards_file, self.cards)
            print(f"Loaded {len(self.cards)} cards into simple database")
            
        except ImportError as e:
            print(f"Warning: Could not import Deck module for default cards: {e}")
            # Fallback: create a minimal card set
            self._create_minimal_cards()
    
    def _create_minimal_cards(self):
        """Create a minimal set of cards as fallback."""
        minimal_cards = [
            {
                'id': 'fool',
                'name': 'The Fool',
                'arcana': 'major',
                'suit': None,
                'number': 0,
                'element': 'air',
                'keywords': ['new beginnings', 'innocence', 'spontaneity'],
                'polarity': 0.5,
                'intensity': 0.6,
                'upright_meaning': 'New beginnings, innocence, spontaneity',
                'reversed_meaning': 'Recklessness, lack of direction',
                'influence_rules': [],
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'id': 'magician',
                'name': 'The Magician',
                'arcana': 'major',
                'suit': None,
                'number': 1,
                'element': 'air',
                'keywords': ['manifestation', 'willpower', 'skill'],
                'polarity': 0.7,
                'intensity': 0.8,
                'upright_meaning': 'Manifestation, willpower, skill',
                'reversed_meaning': 'Manipulation, lack of skill',
                'influence_rules': [],
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'id': 'ace_wands',
                'name': 'Ace of Wands',
                'arcana': 'minor',
                'suit': 'wands',
                'number': 1,
                'element': 'fire',
                'keywords': ['inspiration', 'creativity', 'new beginnings'],
                'polarity': 0.8,
                'intensity': 0.7,
                'upright_meaning': 'New inspiration, creative energy',
                'reversed_meaning': 'Blocked creativity, lack of inspiration',
                'influence_rules': [],
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
        ]
        
        self.cards = minimal_cards
        self._save_data(self.cards_file, self.cards)
        print(f"Created {len(self.cards)} minimal cards as fallback")
    
    def _load_default_spreads(self):
        """Load default spreads."""
        default_spreads = [
            {
                'id': 'single_card',
                'name': 'Single Card',
                'description': 'A simple one-card reading for daily guidance or quick insights.',
                'positions': [
                    {'name': 'Guidance', 'description': 'What you need to know right now'}
                ],
                'is_custom': False,
                'created_by': None,
                'created_at': datetime.utcnow().isoformat()
            },
            {
                'id': 'three_card',
                'name': 'Three Card Spread',
                'description': 'Past, Present, Future reading for understanding life flow.',
                'positions': [
                    {'name': 'Past', 'description': 'What has influenced your current situation'},
                    {'name': 'Present', 'description': 'Your current circumstances and mindset'},
                    {'name': 'Future', 'description': 'What is likely to unfold'}
                ],
                'is_custom': False,
                'created_by': None,
                'created_at': datetime.utcnow().isoformat()
            },
            {
                'id': 'celtic_cross',
                'name': 'Celtic Cross',
                'description': 'A comprehensive 10-card spread for deep insight.',
                'positions': [
                    {'name': 'Present Situation', 'description': 'What is happening now'},
                    {'name': 'Challenge', 'description': 'What is blocking or helping you'},
                    {'name': 'Past', 'description': 'What has led to this situation'},
                    {'name': 'Future', 'description': 'What is likely to happen'},
                    {'name': 'Above', 'description': 'Your conscious goals and aspirations'},
                    {'name': 'Below', 'description': 'Your subconscious influences'},
                    {'name': 'Advice', 'description': 'How to approach the situation'},
                    {'name': 'External Influences', 'description': 'People or events affecting you'},
                    {'name': 'Hopes and Fears', 'description': 'Your inner hopes and concerns'},
                    {'name': 'Outcome', 'description': 'The likely resolution'}
                ],
                'is_custom': False,
                'created_by': None,
                'created_at': datetime.utcnow().isoformat()
            }
        ]
        
        self.spreads = default_spreads
        self._save_data(self.spreads_file, self.spreads)
        print(f"Loaded {len(self.spreads)} default spreads")
    
    # Card operations
    def get_card(self, card_id: str) -> Optional[Dict[str, Any]]:
        """Get a card by ID."""
        for card in self.cards:
            if card['id'] == card_id:
                return card
        return None
    
    def get_all_cards(self) -> List[Dict[str, Any]]:
        """Get all cards."""
        return self.cards.copy()
    
    def get_cards_by_arcana(self, arcana: str) -> List[Dict[str, Any]]:
        """Get cards by arcana type."""
        return [card for card in self.cards if card['arcana'] == arcana]
    
    def get_cards_by_suit(self, suit: str) -> List[Dict[str, Any]]:
        """Get cards by suit."""
        return [card for card in self.cards if card.get('suit') == suit]
    
    # Spread operations
    def get_spread(self, spread_id: str) -> Optional[Dict[str, Any]]:
        """Get a spread by ID."""
        for spread in self.spreads:
            if spread['id'] == spread_id:
                return spread
        return None
    
    def get_all_spreads(self) -> List[Dict[str, Any]]:
        """Get all spreads."""
        return self.spreads.copy()
    
    def create_spread(self, spread_data: Dict[str, Any]) -> str:
        """Create a new spread."""
        spread_id = str(uuid.uuid4())
        spread_data['id'] = spread_id
        spread_data['created_at'] = datetime.utcnow().isoformat()
        self.spreads.append(spread_data)
        self._save_data(self.spreads_file, self.spreads)
        return spread_id
    
    # Reading operations
    def create_reading(self, reading_data: Dict[str, Any]) -> str:
        """Create a new reading."""
        reading_id = str(uuid.uuid4())
        reading_data['id'] = reading_id
        reading_data['created_at'] = datetime.utcnow().isoformat()
        reading_data['updated_at'] = datetime.utcnow().isoformat()
        self.readings.append(reading_data)
        self._save_data(self.readings_file, self.readings)
        return reading_id
    
    def get_reading(self, reading_id: str) -> Optional[Dict[str, Any]]:
        """Get a reading by ID."""
        for reading in self.readings:
            if reading['id'] == reading_id:
                return reading
        return None
    
    def get_all_readings(self) -> List[Dict[str, Any]]:
        """Get all readings."""
        return self.readings.copy()
    
    def update_reading(self, reading_id: str, updates: Dict[str, Any]) -> bool:
        """Update a reading."""
        for i, reading in enumerate(self.readings):
            if reading['id'] == reading_id:
                reading.update(updates)
                reading['updated_at'] = datetime.utcnow().isoformat()
                self.readings[i] = reading
                self._save_data(self.readings_file, self.readings)
                return True
        return False
    
    def delete_reading(self, reading_id: str) -> bool:
        """Delete a reading."""
        for i, reading in enumerate(self.readings):
            if reading['id'] == reading_id:
                del self.readings[i]
                self._save_data(self.readings_file, self.readings)
                return True
        return False
    
    # Memory operations
    def store_memory(self, entity_type: str, entity_name: str, description: str = None, 
                    context: str = None, importance_score: float = 1.0) -> str:
        """Store a memory."""
        memory_id = str(uuid.uuid4())
        memory_data = {
            'id': memory_id,
            'entity_type': entity_type,
            'entity_name': entity_name,
            'description': description,
            'context': context,
            'importance_score': importance_score,
            'last_mentioned': datetime.utcnow().isoformat(),
            'created_at': datetime.utcnow().isoformat()
        }
        self.memories.append(memory_data)
        self._save_data(self.memories_file, self.memories)
        return memory_id
    
    def search_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories by query."""
        query_lower = query.lower()
        results = []
        
        for memory in self.memories:
            score = 0
            if query_lower in memory['entity_name'].lower():
                score += 2
            if memory['description'] and query_lower in memory['description'].lower():
                score += 1
            if memory['context'] and query_lower in memory['context'].lower():
                score += 1
            
            if score > 0:
                results.append((score, memory))
        
        # Sort by relevance score and importance
        results.sort(key=lambda x: (x[0], x[1]['importance_score']), reverse=True)
        return [memory for _, memory in results[:limit]]
    
    def get_recent_memories(self, days: int = 7, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent memories."""
        cutoff_date = datetime.utcnow().timestamp() - (days * 24 * 60 * 60)
        recent_memories = []
        
        for memory in self.memories:
            memory_date = datetime.fromisoformat(memory['last_mentioned']).timestamp()
            if memory_date >= cutoff_date:
                recent_memories.append(memory)
        
        recent_memories.sort(key=lambda x: x['last_mentioned'], reverse=True)
        return recent_memories[:limit]
    
    # Settings operations
    def get_setting(self, key: str, default_value=None):
        """Get a setting value."""
        return self.settings.get(key, default_value)
    
    def set_setting(self, key: str, value: Any):
        """Set a setting value."""
        self.settings[key] = value
        self._save_data(self.settings_file, self.settings)
    
    # Conversation operations
    def create_conversation(self, title: str, reading_id: str = None, 
                          context: str = None) -> str:
        """Create a new conversation."""
        conversation_id = str(uuid.uuid4())
        conversation_data = {
            'id': conversation_id,
            'reading_id': reading_id,
            'title': title,
            'context': context,
            'is_memory_enabled': True,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'messages': []
        }
        self.conversations.append(conversation_data)
        self._save_data(self.conversations_file, self.conversations)
        return conversation_id
    
    def add_message(self, conversation_id: str, role: str, content: str) -> bool:
        """Add a message to a conversation."""
        for conversation in self.conversations:
            if conversation['id'] == conversation_id:
                message = {
                    'id': len(conversation['messages']) + 1,
                    'role': role,
                    'content': content,
                    'timestamp': datetime.utcnow().isoformat()
                }
                conversation['messages'].append(message)
                conversation['updated_at'] = datetime.utcnow().isoformat()
                self._save_data(self.conversations_file, self.conversations)
                return True
        return False
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get a conversation by ID."""
        for conversation in self.conversations:
            if conversation['id'] == conversation_id:
                return conversation
        return None
    
    def get_all_conversations(self) -> List[Dict[str, Any]]:
        """Get all conversations."""
        return self.conversations.copy()
    
    def close(self):
        """Close the database connection."""
        # Save all data
        self._save_data(self.cards_file, self.cards)
        self._save_data(self.spreads_file, self.spreads)
        self._save_data(self.readings_file, self.readings)
        self._save_data(self.conversations_file, self.conversations)
        self._save_data(self.memories_file, self.memories)
        self._save_data(self.settings_file, self.settings)
        print("Simple database closed and data saved")

# Convenience functions for compatibility
def create_database(db_path: str = "tarot_studio_data"):
    """Create a simple database instance."""
    return SimpleDB(db_path)

def get_session(db_instance):
    """Get a session (same as the db instance for simple DB)."""
    return db_instance