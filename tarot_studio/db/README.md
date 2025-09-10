# Database Module - Tarot Studio

## Overview

The Database Module provides data persistence for the Tarot Studio application. It includes both a comprehensive SQLAlchemy-based implementation (`models.py`) and a lightweight JSON-based fallback implementation (`simple_db.py`) for environments where external dependencies are not available.

## Features

### Core Functionality
- **Card Management**: Store and retrieve tarot cards with full metadata
- **Spread Management**: Manage tarot spread layouts and custom spreads
- **Reading Persistence**: Save and retrieve tarot readings with interpretations
- **Memory System**: Semantic memory storage for AI context
- **Conversation Management**: Store AI conversations and chat history
- **Settings Management**: User preferences and application settings

### Data Models

#### Card
- Complete tarot card information (Major and Minor Arcana)
- Keywords, meanings, polarity, intensity scores
- Influence rules for card interactions
- Element and astrology associations

#### Spread
- Tarot spread layouts (Single Card, Three Card, Celtic Cross, etc.)
- Custom spread creation and management
- Position definitions and descriptions

#### Reading
- Complete tarot reading records
- Question, interpretation, summary, advice
- Tags and people involved
- Privacy settings

#### Memory
- Semantic memory for AI context
- Entity extraction and importance scoring
- Search and retrieval capabilities

#### Conversation
- AI conversation threads
- Message history and context
- Reading associations

## Implementation

### SQLAlchemy Implementation (`models.py`)

Full-featured database implementation using SQLAlchemy ORM:

```python
from tarot_studio.db.models import create_database, get_session, load_cards_from_json

# Create database
engine = create_database("tarot_studio.db")
session = get_session(engine)

# Load cards from JSON
load_cards_from_json("card_data.json", session)

# Create default spreads
create_default_spreads(session)
```

### SimpleDB Implementation (`simple_db.py`)

Lightweight JSON-based implementation for environments without SQLAlchemy:

```python
from tarot_studio.db.simple_db import SimpleDB

# Create database
db = SimpleDB("tarot_studio_data")

# Get all cards
cards = db.get_all_cards()

# Create a reading
reading_id = db.create_reading({
    'title': 'My Reading',
    'spread_id': 'three_card',
    'question': 'What do I need to know?',
    'interpretation': 'The cards suggest...'
})

# Store memory
memory_id = db.store_memory(
    entity_type="person",
    entity_name="John Doe",
    description="A friend who loves tarot",
    importance_score=0.8
)
```

## API Reference

### SimpleDB Class

#### Card Operations
- `get_all_cards()`: Get all cards
- `get_card(card_id)`: Get card by ID
- `get_cards_by_arcana(arcana)`: Get cards by arcana type
- `get_cards_by_suit(suit)`: Get cards by suit

#### Spread Operations
- `get_all_spreads()`: Get all spreads
- `get_spread(spread_id)`: Get spread by ID
- `create_spread(spread_data)`: Create new spread

#### Reading Operations
- `create_reading(reading_data)`: Create new reading
- `get_reading(reading_id)`: Get reading by ID
- `get_all_readings()`: Get all readings
- `update_reading(reading_id, updates)`: Update reading
- `delete_reading(reading_id)`: Delete reading

#### Memory Operations
- `store_memory(entity_type, entity_name, ...)`: Store memory
- `search_memories(query, limit)`: Search memories
- `get_recent_memories(days, limit)`: Get recent memories

#### Conversation Operations
- `create_conversation(title, reading_id, context)`: Create conversation
- `add_message(conversation_id, role, content)`: Add message
- `get_conversation(conversation_id)`: Get conversation
- `get_all_conversations()`: Get all conversations

#### Settings Operations
- `get_setting(key, default_value)`: Get setting
- `set_setting(key, value)`: Set setting

## Data Structure

### Card Data Format
```json
{
  "id": "fool",
  "name": "The Fool",
  "arcana": "major",
  "suit": null,
  "number": 0,
  "element": "air",
  "keywords": ["new beginnings", "innocence", "spontaneity"],
  "polarity": 0.5,
  "intensity": 0.6,
  "upright_meaning": "New beginnings, innocence, spontaneity",
  "reversed_meaning": "Recklessness, lack of direction",
  "influence_rules": []
}
```

### Spread Data Format
```json
{
  "id": "three_card",
  "name": "Three Card Spread",
  "description": "Past, Present, Future reading",
  "positions": [
    {"name": "Past", "description": "What has influenced your current situation"},
    {"name": "Present", "description": "Your current circumstances and mindset"},
    {"name": "Future", "description": "What is likely to unfold"}
  ],
  "is_custom": false,
  "created_by": null
}
```

### Reading Data Format
```json
{
  "id": "reading_123",
  "title": "My Reading",
  "spread_id": "three_card",
  "question": "What do I need to know?",
  "interpretation": "The cards suggest...",
  "summary": "Brief summary",
  "advice": ["Advice item 1", "Advice item 2"],
  "tags": ["tag1", "tag2"],
  "people_involved": ["Person 1"],
  "is_private": false,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

## Testing

The module includes comprehensive tests:

```bash
# Test SimpleDB implementation
python3 test_db_module.py

# Test individual components
python3 test_simple_db.py
```

## File Structure

```
db/
├── models.py          # SQLAlchemy models and functions
├── simple_db.py       # JSON-based SimpleDB implementation
├── generate_deck.py   # Deck generation utilities
├── migrations/        # Database migration scripts
├── schemas/           # Data schemas
│   └── card_schema.json
└── README.md          # This documentation
```

## Dependencies

### SQLAlchemy Implementation
- `sqlalchemy`: ORM and database toolkit
- `sqlite3`: Database engine (built-in)

### SimpleDB Implementation
- `json`: JSON handling (built-in)
- `pathlib`: Path utilities (built-in)
- `uuid`: UUID generation (built-in)
- `datetime`: Date/time handling (built-in)

## Usage Examples

### Basic Usage
```python
from tarot_studio.db.simple_db import SimpleDB

# Initialize database
db = SimpleDB("my_tarot_data")

# Get all cards
cards = db.get_all_cards()
print(f"Loaded {len(cards)} cards")

# Create a reading
reading_id = db.create_reading({
    'title': 'Daily Guidance',
    'spread_id': 'single_card',
    'question': 'What do I need to focus on today?',
    'interpretation': 'The cards suggest focusing on new opportunities.'
})

# Store a memory
db.store_memory(
    entity_type="concept",
    entity_name="new opportunities",
    description="Focus on emerging possibilities",
    importance_score=0.7
)

# Close database
db.close()
```

### Advanced Usage
```python
# Search memories
memories = db.search_memories("opportunities", limit=5)
for memory in memories:
    print(f"Found: {memory['entity_name']} - {memory['description']}")

# Create custom spread
custom_spread_id = db.create_spread({
    'name': 'My Custom Spread',
    'description': 'A personalized spread',
    'positions': [
        {'name': 'Challenge', 'description': 'Current challenge'},
        {'name': 'Solution', 'description': 'Potential solution'}
    ],
    'is_custom': True,
    'created_by': 'user123'
})

# Create conversation
conversation_id = db.create_conversation(
    title="Reading Discussion",
    reading_id=reading_id,
    context="Discussing the reading interpretation"
)

# Add messages
db.add_message(conversation_id, "user", "What does this card mean?")
db.add_message(conversation_id, "assistant", "This card represents...")
```

## Error Handling

The module includes comprehensive error handling:

- **File I/O Errors**: Graceful handling of file read/write operations
- **Data Validation**: Validation of data structures and required fields
- **Import Errors**: Fallback behavior when dependencies are missing
- **JSON Errors**: Proper handling of malformed JSON data

## Performance Considerations

### SimpleDB Performance
- **Memory Usage**: All data loaded into memory for fast access
- **File I/O**: Data saved to JSON files for persistence
- **Search Performance**: Linear search through memory (suitable for small datasets)

### Optimization Tips
- Use specific queries instead of loading all data
- Implement data pagination for large datasets
- Consider caching frequently accessed data
- Regular cleanup of old conversations and memories

## Future Enhancements

- **Indexing**: Add search indexes for better performance
- **Caching**: Implement intelligent caching strategies
- **Compression**: Add data compression for large datasets
- **Backup**: Automated backup and restore functionality
- **Migration**: Tools for upgrading data formats
- **Analytics**: Usage statistics and insights

## Contributing

When contributing to the Database Module:

1. Maintain backward compatibility
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Follow the existing code style
5. Consider both SQLAlchemy and SimpleDB implementations

## License

This module is part of the Tarot Studio project and follows the same license terms.