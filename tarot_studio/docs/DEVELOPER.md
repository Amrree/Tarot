# Developer Documentation

This document provides detailed information for developers working on Tarot Studio.

## Architecture Overview

Tarot Studio is built using a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  Business Logic │    │   Data Layer    │
│   (PyObjC)      │    │   (Core)        │    │  (SQLAlchemy)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Layer      │    │ Influence Engine │    │  Memory System   │
│   (Ollama)      │    │   (Rules)        │    │  (Semantic)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Core Components

### 1. Influence Engine (`core/influence_engine.py`)

The influence engine computes how neighboring cards modify meanings in tarot spreads.

**Key Classes:**
- `InfluenceEngine`: Main engine class
- `CardPosition`: Represents a card in a specific position
- `InfluenceFactor`: Describes how one card influences another
- `InfluencedCard`: A card with computed influence modifications

**Algorithm:**
1. Load base attributes for every card
2. Compute adjacency map (neighbors per layout)
3. For each card, accumulate influence from neighbors
4. Calculate final polarity score
5. Generate influenced meaning text

**Example Usage:**
```python
engine = InfluenceEngine()
spread_positions = [CardPosition('the_sun', 'present', 'upright', card_data)]
influenced_cards = engine.compute_influenced_meanings(spread_positions, spread_layout)
```

### 2. AI Integration (`ai/ollama_client.py`)

Provides integration with local Ollama LLM for generating tarot interpretations.

**Key Classes:**
- `OllamaClient`: Main client for Ollama communication
- `AIResponse`: Structured response from AI
- `ConversationContext`: Context for AI conversations

**Features:**
- Structured JSON responses
- Streaming support for real-time UI updates
- Conversation memory integration
- Error handling and fallbacks

**Example Usage:**
```python
client = OllamaClient(model_name="llama3.2")
response = await client.generate_reading_interpretation(spread_data)
```

### 3. Memory System (`ai/memory.py`)

Manages semantic memory for AI conversations and context.

**Key Classes:**
- `MemoryStore`: Main memory management class
- `MemoryEntry`: Individual memory entry
- `MemorySearchResult`: Search result with relevance scoring

**Features:**
- Entity extraction from text
- Semantic search and retrieval
- Importance scoring and decay
- Context-aware memory recall

**Example Usage:**
```python
store = MemoryStore()
store.store_memory('person', 'Sarah', 'Friend who asked about career')
results = store.search_memories('Sarah')
```

### 4. Database Models (`db/models.py`)

SQLAlchemy models for data persistence.

**Key Models:**
- `Card`: Tarot card with all attributes
- `Reading`: Complete tarot reading
- `ReadingCard`: Association between reading and card
- `Conversation`: AI conversation session
- `Memory`: Semantic memory entry

**Relationships:**
- Reading → ReadingCard → Card (many-to-many)
- Reading → Conversation (one-to-many)
- Memory (standalone with indexes)

## UI Framework

### PyObjC Integration

The UI is built using PyObjC for native macOS integration:

```python
from Foundation import *
from AppKit import *
from Cocoa import *

class MainWindow(NSWindow):
    def init(self):
        # Create window with dark theme
        self = super(MainWindow, self).initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 1200, 800),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
            NSBackingStoreBuffered,
            False
        )
```

### Component Structure

- `MainWindow`: Main application window
- `SidebarView`: Navigation sidebar
- `ReadingsView`: Card drawing and interpretation
- `ChatView`: AI conversation interface
- `HistoryView`: Past readings browser
- `SettingsView`: App configuration

### Dark Theme Implementation

```python
# Set dark appearance
self.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameDarkAqua))

# Use system colors
NSColor.controlBackgroundColor()  # Dark background
NSColor.labelColor()              # Light text
NSColor.secondaryLabelColor()     # Muted text
NSColor.controlAccentColor()      # Accent color
```

## Data Flow

### 1. Card Drawing Flow

```
User clicks "Draw Cards"
    ↓
ReadingsView.drawCards_()
    ↓
getRandomCards() → Database query
    ↓
displayCardInSlot() → UI update
    ↓
generateInterpretation() → AI call
    ↓
displayInterpretation() → UI update
```

### 2. AI Interpretation Flow

```
generateInterpretation()
    ↓
Create spread_data dictionary
    ↓
ollama_client.generate_reading_interpretation()
    ↓
Build structured prompt
    ↓
Send to Ollama LLM
    ↓
Parse JSON response
    ↓
Update UI with interpretation
```

### 3. Memory Integration Flow

```
AI generates response
    ↓
Extract entities from conversation
    ↓
Store in MemoryStore
    ↓
Search relevant memories for context
    ↓
Include in AI prompt
    ↓
Generate context-aware response
```

## Testing

### Test Structure

```
tests/
├── test_influence_engine.py    # Influence engine tests
├── test_ollama_client.py       # AI client tests
├── test_memory.py             # Memory system tests
├── test_database.py           # Database tests
└── test_ui.py                 # UI tests (limited)
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_influence_engine.py -v

# Run with coverage
pytest tests/ --cov=tarot_studio --cov-report=html
```

### Test Examples

**Influence Engine Test:**
```python
def test_major_arcana_influence(self):
    """Test that Major Arcana cards have stronger influence."""
    spread_positions = create_test_spread()
    influenced_cards = self.engine.compute_influenced_meanings(spread_positions, spread_layout)
    
    # Verify influence factors
    assert len(influenced_cards[0].influence_factors) > 0
    assert any(factor.influence_type == 'major_arcana' for factor in influenced_cards[0].influence_factors)
```

**AI Client Test:**
```python
@pytest.mark.asyncio
async def test_generate_reading_interpretation_success(self):
    """Test successful reading interpretation generation."""
    spread_data = {'reading_id': 'test_001', 'cards': [...]}
    
    with patch.object(self.client.client, 'generate', return_value=mock_response):
        response = await self.client.generate_reading_interpretation(spread_data)
        
        assert response.reading_id == 'test_001'
        assert response.summary is not None
```

## Packaging

### py2app Configuration

The app is packaged using py2app with the following configuration:

```python
OPTIONS = {
    'plist': {
        'CFBundleName': 'Tarot Studio',
        'CFBundleIdentifier': 'com.tarotstudio.app',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'NSAppearanceName': 'NSAppearanceNameDarkAqua',
    },
    'packages': ['tarot_studio', 'tarot_studio.app', ...],
    'includes': ['objc', 'Foundation', 'AppKit', 'sqlalchemy', 'ollama'],
    'excludes': ['tkinter', 'matplotlib', 'numpy', ...],
}
```

### Build Process

1. **Setup Environment**: Create virtual environment
2. **Install Dependencies**: Install all required packages
3. **Build App**: Run py2app to create .app bundle
4. **Code Sign**: Sign the app for distribution
5. **Create DMG**: Package for distribution

### Build Script

```bash
#!/bin/bash
# Build script for macOS app

# Check macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script must be run on macOS"
    exit 1
fi

# Setup environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install py2app

# Build app
cd tarot_studio/packaging
python3 setup_app.py py2app

# Code sign
codesign --force --deep --sign - "dist/Tarot Studio.app"
```

## Performance Considerations

### Database Optimization

- **Indexes**: Proper indexing on frequently queried fields
- **Connection Pooling**: Reuse database connections
- **Lazy Loading**: Load related data only when needed

### AI Performance

- **Streaming**: Stream AI responses for better UX
- **Caching**: Cache common interpretations
- **Timeout Handling**: Prevent hanging on slow AI responses

### UI Performance

- **Lazy Loading**: Load UI components on demand
- **Background Processing**: Run heavy operations in background
- **Memory Management**: Proper cleanup of resources

## Security

### Data Encryption

Sensitive data is encrypted using the `cryptography` library:

```python
from cryptography.fernet import Fernet

def encrypt_data(data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode()).decode()
```

### Key Management

- **macOS Keychain**: Store encryption keys securely
- **User Passphrase**: Derive keys from user input
- **Key Rotation**: Support for changing encryption keys

## Debugging

### Logging

The application uses Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Application started")
logger.error(f"Failed to connect: {e}")
```

### Common Issues

**PyObjC Import Errors:**
```python
# Ensure proper imports
from Foundation import *
from AppKit import *
from Cocoa import *
```

**Database Connection Issues:**
```python
# Check database path and permissions
engine = create_engine(f"sqlite:///{db_path}")
```

**Ollama Connection Issues:**
```python
# Verify Ollama is running
client = OllamaClient()
connected = await client.check_connection()
```

## Contributing

### Code Style

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations
- **Docstrings**: Document all public methods
- **Error Handling**: Proper exception handling

### Pull Request Process

1. **Fork Repository**: Create your own fork
2. **Create Branch**: Use descriptive branch names
3. **Write Tests**: Add tests for new functionality
4. **Update Documentation**: Update relevant docs
5. **Submit PR**: Include detailed description

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass and cover new functionality
- [ ] Documentation is updated
- [ ] No breaking changes without migration
- [ ] Performance impact considered
- [ ] Security implications reviewed

## Future Enhancements

### Planned Features

- **Custom Decks**: Support for user-created decks
- **Advanced Spreads**: More complex spread layouts
- **Card Images**: Integration with card artwork
- **Export Features**: PDF and image export
- **Voice Input**: Speech-to-text for questions
- **Accessibility**: VoiceOver and keyboard navigation

### Technical Improvements

- **Performance**: Optimize database queries and AI responses
- **Testing**: Increase test coverage
- **Documentation**: More comprehensive API docs
- **Internationalization**: Multi-language support
- **Plugin System**: Extensible architecture