# Tarot AI Module

The Tarot AI Module provides comprehensive AI functionality for the Tarot Studio application, including Ollama integration, memory management, conversation handling, and prompt templates for tarot interpretations.

## Features

- **Ollama Integration**: Local LLM integration with model management and error handling
- **Memory System**: Semantic memory storage and retrieval for AI conversations
- **Conversation Manager**: Chat with cards, readings, and general tarot discussions
- **Prompt Templates**: Comprehensive templates for various AI interactions
- **Configuration Management**: AI settings, model selection, and preferences
- **Fallback Support**: Graceful degradation when AI services are unavailable

## Quick Start

```python
from tarot_studio.ai import OllamaClient, MemoryStore, ConversationManager
from tarot_studio.ai.prompt_templates import PromptTemplateManager
from tarot_studio.ai.ai_config import AIConfigManager

# Initialize AI components
config_manager = AIConfigManager()
ollama_client = OllamaClient()
memory_store = MemoryStore()
conversation_manager = ConversationManager(ollama_client, memory_store)
template_manager = PromptTemplateManager()

# Check AI availability
is_available = await ollama_client.check_connection()
if is_available:
    print("AI is ready!")
else:
    print("AI fallback mode - using template-based responses")
```

## Core Components

### OllamaClient

Manages integration with local Ollama LLM service.

```python
from tarot_studio.ai.ollama_client import OllamaClient

# Create client
client = OllamaClient("llama3.2", "http://localhost:11434")

# Check connection
is_connected = await client.check_connection()

# Get available models
models = client.get_available_models()
for model in models:
    print(f"Model: {model.name} ({model.size})")

# Set active model
client.set_model("llama3.2")

# Generate response
response = await client.generate_response("Tell me about The Fool card")
```

### MemoryStore

Manages semantic memory for AI conversations.

```python
from tarot_studio.ai.memory import MemoryStore

# Create memory store
memory_store = MemoryStore("tarot_memories.db")

# Store memory
memory_id = memory_store.store_memory(
    entity_type="card",
    entity_name="The Fool",
    description="The Fool represents new beginnings and taking risks",
    context="Card interpretation discussion",
    importance_score=0.8
)

# Search memories
results = memory_store.search_memories("fool", limit=5)
for result in results:
    print(f"Found: {result.memory.entity_name} - {result.memory.description}")

# Get recent memories
recent = memory_store.get_recent_memories(days=7, limit=10)
```

### ConversationManager

Handles AI conversations and chat functionality.

```python
from tarot_studio.ai.conversation_manager import ConversationManager

# Create conversation manager
conversation_manager = ConversationManager(ollama_client, memory_store)

# Create session
session = conversation_manager.create_session("card_chat", "user123")

# Chat with a card
card_data = {
    "name": "The Fool",
    "meaning": "New beginnings and taking a leap of faith",
    "keywords": ["new beginnings", "innocence", "free spirit"]
}

response = await conversation_manager.chat_with_card(
    session.session_id,
    card_data,
    "What does The Fool mean for my career change?"
)

print(f"AI Response: {response.summary}")

# Chat about a reading
reading_data = {
    "spread_id": "reading123",
    "layout_name": "Three Card",
    "cards": [
        {"position": "Past", "card_name": "The Fool", "orientation": "upright"},
        {"position": "Present", "card_name": "The Magician", "orientation": "upright"},
        {"position": "Future", "card_name": "The World", "orientation": "upright"}
    ]
}

response = await conversation_manager.chat_with_reading(
    session.session_id,
    reading_data,
    "What does this reading tell me about my future?"
)

# End session
conversation_manager.end_session(session.session_id)
```

### PromptTemplateManager

Manages prompt templates for AI interactions.

```python
from tarot_studio.ai.prompt_templates import PromptTemplateManager

# Create template manager
template_manager = PromptTemplateManager()

# Get available templates
templates = template_manager.get_all_templates()
for template in templates:
    print(f"Template: {template.name} - {template.description}")

# Render template
variables = {
    "card_name": "The Fool",
    "arcana_type": "Major Arcana",
    "suit": "None",
    "number": "0",
    "element": "Air",
    "keywords": "new beginnings, innocence",
    "upright_meaning": "New beginnings and taking a leap of faith",
    "reversed_meaning": "Recklessness or being held back",
    "orientation": "upright",
    "user_question": "What should I do about my career?",
    "context": "User is considering a career change"
}

prompt = template_manager.render_template("card_interpretation", variables)
print(f"Generated prompt: {prompt}")

# Create custom template
custom_template = template_manager.create_custom_template(
    name="career_advice",
    description="Template for career advice",
    template="Based on {card_name}, here's my advice for your career: {advice}",
    variables=["card_name", "advice"],
    category="custom"
)
```

### AIConfigManager

Manages AI configuration and settings.

```python
from tarot_studio.ai.ai_config import AIConfigManager

# Create config manager
config_manager = AIConfigManager("ai_config.json")

# Get current settings
settings = config_manager.get_settings()
print(f"Default model: {settings.default_model}")
print(f"Temperature: {settings.temperature}")
print(f"Max tokens: {settings.max_tokens}")

# Update settings
config_manager.update_settings(
    temperature=0.8,
    max_tokens=1024,
    enable_memory=True
)

# Get available models
models = config_manager.get_models()
for model in models:
    print(f"Model: {model.display_name} ({model.size}) - Enabled: {model.enabled}")

# Get recommended models
recommended = config_manager.get_recommended_models()
for model in recommended:
    print(f"Recommended: {model.display_name}")

# Set default model
config_manager.set_default_model("llama3.2")

# Enable/disable models
config_manager.enable_model("mistral")
config_manager.disable_model("codellama")

# Validate configuration
errors = config_manager.validate_config()
if errors:
    print(f"Configuration errors: {errors}")
else:
    print("Configuration is valid")

# Save configuration
config_manager.save_config()
```

## Available Templates

### Card Interpretation
- **Name**: `card_interpretation`
- **Purpose**: Interpret a single tarot card
- **Variables**: `card_name`, `arcana_type`, `suit`, `number`, `element`, `keywords`, `upright_meaning`, `reversed_meaning`, `orientation`, `user_question`, `context`

### Reading Interpretation
- **Name**: `reading_interpretation`
- **Purpose**: Interpret a complete tarot reading
- **Variables**: `spread_name`, `user_question`, `reading_date`, `cards_info`, `context`

### Card Chat
- **Name**: `card_chat`
- **Purpose**: Chat with a specific tarot card
- **Variables**: `card_name`, `card_meaning`, `keywords`, `orientation`, `user_message`, `previous_context`

### Reading Chat
- **Name**: `reading_chat`
- **Purpose**: Chat about a tarot reading
- **Variables**: `spread_name`, `cards_summary`, `original_question`, `user_message`, `previous_context`

### General Tarot Chat
- **Name**: `general_tarot_chat`
- **Purpose**: General tarot conversation
- **Variables**: `user_message`, `context`

### Influence Interpretation
- **Name**: `influence_interpretation`
- **Purpose**: Interpret influenced card meanings
- **Variables**: `card_name`, `position`, `base_meaning`, `influenced_meaning`, `influence_score`, `influence_factors`, `spread_name`, `user_question`, `other_cards`

### Journal Prompts
- **Name**: `journal_prompt`
- **Purpose**: Generate journal prompts for readings
- **Variables**: `spread_name`, `user_question`, `cards_summary`

### Advice Generation
- **Name**: `advice_generation`
- **Purpose**: Generate practical advice from readings
- **Variables**: `spread_name`, `user_question`, `cards_summary`, `key_themes`

### Follow-up Questions
- **Name**: `follow_up_questions`
- **Purpose**: Generate follow-up questions for readings
- **Variables**: `spread_name`, `user_question`, `cards_summary`

## Configuration

### Default Settings

```python
AISettings(
    default_model="llama3.2",
    ollama_base_url="http://localhost:11434",
    max_tokens=2048,
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.1,
    context_length=4096,
    enable_memory=True,
    memory_retention_days=30,
    enable_conversation_history=True,
    max_conversation_history=50,
    enable_streaming=True,
    response_timeout=30,
    retry_attempts=3,
    enable_fallback=True,
    fallback_model="llama3.2"
)
```

### Supported Models

- **Llama 3.2** (3B, 8B, 70B) - Recommended for most use cases
- **Mistral** (7B) - Fast and efficient
- **Phi-3** (3.8B) - Compact and efficient
- **Code Llama** (7B) - Good for technical discussions

### Model Recommendations

- **Beginner**: Llama 3.2 3B or Phi-3 3.8B
- **Balanced**: Llama 3.2 8B or Mistral 7B
- **High Quality**: Llama 3.2 70B (requires more resources)

## Error Handling

The AI module includes comprehensive error handling:

```python
try:
    response = await ollama_client.generate_response(prompt)
except AIError as e:
    print(f"AI Error: {e.message}")
    # Fallback to template-based response
    response = generate_template_response(prompt)
except ConnectionError:
    print("Ollama service unavailable - using fallback mode")
    response = generate_fallback_response(prompt)
```

## Fallback Behavior

When Ollama is unavailable, the AI module gracefully falls back to:

1. **Template-based responses** using predefined templates
2. **Cached responses** from previous similar queries
3. **Basic interpretations** using card meanings and keywords
4. **Error messages** with helpful guidance

## Memory Management

The memory system automatically:

- **Stores conversations** for future reference
- **Searches relevant context** for each query
- **Cleans up old memories** based on importance and age
- **Extracts entities** from conversations for better context

## Integration with Other Modules

### Deck Module Integration

```python
from tarot_studio.deck import Deck
from tarot_studio.ai import ConversationManager

deck = Deck.load_from_file('card_data.json')
card = deck.draw_card()

# Chat with the drawn card
response = await conversation_manager.chat_with_card(
    session_id,
    card.to_dict(),
    "What does this card mean for me?"
)
```

### Spreads Module Integration

```python
from tarot_studio.spreads import TarotSpread
from tarot_studio.ai import ConversationManager

spread = TarotSpread.create_three_card_reading(deck, "What does my future hold?")
reading = spread.draw_cards()

# Chat about the reading
response = await conversation_manager.chat_with_reading(
    session_id,
    spread.to_dict(),
    "Can you help me understand this reading better?"
)
```

### Influence Engine Integration

```python
from tarot_studio.core.enhanced_influence_engine import EnhancedInfluenceEngine
from tarot_studio.ai.prompt_templates import PromptTemplateManager

# Apply influence engine
influenced_meanings = spread.apply_influence_engine(card_database)

# Use AI to interpret influenced meanings
template_manager = PromptTemplateManager()
for card_data in influenced_meanings['cards']:
    prompt = template_manager.render_template("influence_interpretation", card_data)
    ai_response = await ollama_client.generate_response(prompt)
```

## Testing

Run the AI module tests:

```bash
python3 test_ai_module.py
```

The test suite covers:
- OllamaClient functionality
- MemoryStore operations
- ConversationManager features
- PromptTemplateManager functionality
- AIConfigManager operations
- Integration between components

## Dependencies

- **ollama** (optional) - For local LLM integration
- **sqlite3** - For memory storage
- **Standard library** - json, datetime, logging, threading, etc.

## Performance Considerations

- **Memory Usage**: Large models (70B) require significant RAM
- **Response Time**: Smaller models are faster but less accurate
- **Storage**: Memory database grows over time, consider cleanup
- **Caching**: Connection and model info are cached for performance

## Security

- **Local Processing**: All AI processing happens locally
- **No External Calls**: No data sent to external services
- **Memory Encryption**: Sensitive data can be encrypted in memory
- **Access Control**: Memory access can be restricted by user

## Troubleshooting

### Common Issues

1. **Ollama Not Running**
   ```bash
   # Start Ollama service
   ollama serve
   ```

2. **Model Not Found**
   ```bash
   # Pull a model
   ollama pull llama3.2
   ```

3. **Memory Database Issues**
   ```python
   # Reset memory store
   memory_store = MemoryStore("new_memory.db")
   ```

4. **Configuration Errors**
   ```python
   # Reset to defaults
   config_manager.reset_to_defaults()
   ```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Version

Current version: 1.0.0

## License

Part of the Tarot Studio project.