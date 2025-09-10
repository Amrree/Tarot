# Tarot Deck Module

The Deck Module provides a complete implementation of a tarot deck system for the Tarot Studio application. This module serves as the foundation for all tarot-related functionality, providing clean, extensible classes for representing individual cards and complete decks.

## Overview

The Deck Module consists of two main classes:

- **Card**: Represents a single tarot card with metadata, meanings, and orientation support
- **Deck**: Represents a complete 78-card tarot deck with shuffling, drawing, and reset functionality

## Features

### Card Class Features
- Complete metadata support (name, arcana type, suit, number, element, keywords)
- Upright and reversed meanings
- Orientation management (flip, set orientation)
- Keyword searching and filtering
- Dictionary serialization
- Equality and hashing support

### Deck Class Features
- Full 78-card deck (22 Major Arcana + 56 Minor Arcana)
- Shuffling with optional seed for reproducibility
- Single and multiple card drawing
- Orientation support at draw time
- Card filtering by various criteria (suit, element, keywords, arcana type)
- Deck reset functionality
- Comprehensive deck information and statistics

## File Structure

```
tarot_studio/deck/
├── __init__.py          # Module initialization
├── card.py              # Card class implementation
├── deck.py              # Deck class implementation
├── card_data.json       # Complete card data (78 cards)
└── README.md            # This documentation
```

## Usage Examples

### Basic Card Usage

```python
from tarot_studio.deck.card import Card, Orientation

# Create a card from data
card_data = {
    'id': 'the_sun',
    'name': 'The Sun',
    'arcana': 'major',
    'element': 'fire',
    'keywords': ['joy', 'success', 'vitality'],
    'upright_meaning': 'The Sun represents joy, success, and vitality.',
    'reversed_meaning': 'Reversed, The Sun suggests temporary setbacks.'
}

card = Card.from_data(card_data)

# Get card information
print(card.name)  # "The Sun"
print(card.arcana)  # Arcana.MAJOR
print(card.element)  # Element.FIRE
print(card.keywords)  # ['joy', 'success', 'vitality']

# Work with orientation
print(card.get_meaning())  # Upright meaning
card.flip()
print(card.get_meaning())  # Reversed meaning

# Check for keywords
if card.has_keyword('joy'):
    print("This card is about joy!")
```

### Basic Deck Usage

```python
from tarot_studio.deck.deck import Deck, Orientation

# Load deck from file
deck = Deck.load_from_file('card_data.json')

# Shuffle the deck
deck.shuffle(seed=42)  # Optional seed for reproducible shuffling

# Draw a single card
card = deck.draw_card()
print(f"Drew: {card}")

# Draw a card with specific orientation
reversed_card = deck.draw_card(Orientation.REVERSED)
print(f"Drew reversed: {reversed_card}")

# Draw multiple cards
cards = deck.draw_cards(3, [
    Orientation.UPRIGHT,
    Orientation.REVERSED,
    Orientation.UPRIGHT
])

# Check deck state
print(f"Remaining cards: {len(deck)}")
print(f"Drawn cards: {deck.count_drawn()}")

# Reset deck for next reading
deck.reset()
```

### Advanced Deck Usage

```python
# Filter cards by various criteria
major_cards = deck.get_major_arcana()
minor_cards = deck.get_minor_arcana()
wands_cards = deck.get_cards_by_suit(Suit.WANDS)
fire_cards = deck.get_cards_by_element(Element.FIRE)
joy_cards = deck.get_cards_with_keyword('joy')

# Search for specific cards
card = deck.get_card_by_id('the_sun')
card = deck.get_card_by_name('The Sun')

# Get deck information
info = deck.get_deck_info()
print(f"Total cards: {info['total_cards']}")
print(f"Major Arcana: {info['major_arcana']}")
print(f"Minor Arcana: {info['minor_arcana']}")
print(f"Suit counts: {info['suit_counts']}")
print(f"Element counts: {info['element_counts']}")
```

## Integration with Other Modules

### Spreads Module Integration

The Deck Module is designed to work seamlessly with the Spreads Module:

```python
# Example of how spreads module would use deck
def draw_spread(deck, spread_type):
    """Draw cards for a specific spread type."""
    if spread_type == 'three_card':
        positions = ['past', 'present', 'future']
        cards = deck.draw_cards(3)
        return {pos: card for pos, card in zip(positions, cards)}
    elif spread_type == 'celtic_cross':
        positions = ['situation', 'challenge', 'past', 'future', 
                    'above', 'below', 'advice', 'external', 
                    'hopes_fears', 'outcome']
        cards = deck.draw_cards(10)
        return {pos: card for pos, card in zip(positions, cards)}
```

### Influence Engine Integration

The Deck Module provides the card data needed by the Influence Engine:

```python
# Example of how influence engine would use deck
def get_card_for_influence_engine(card):
    """Convert Card object to influence engine format."""
    return {
        'card_id': card.id,
        'name': card.name,
        'arcana': card.arcana.value,
        'suit': card.suit.value if card.suit else None,
        'number': card.number,
        'element': card.element.value if card.element else None,
        'keywords': card.keywords,
        'polarity': 0.0,  # Would be calculated by influence engine
        'intensity': 0.5,  # Would be calculated by influence engine
        'themes': {},      # Would be calculated by influence engine
        'upright_meaning': card.upright_meaning,
        'reversed_meaning': card.reversed_meaning
    }
```

## Data Format

### Card Data Structure

Cards are stored in JSON format with the following structure:

```json
{
  "id": "unique_card_identifier",
  "name": "Human Readable Name",
  "arcana": "major|minor",
  "suit": "wands|cups|swords|pentacles|null",
  "number": "integer|null",
  "element": "fire|water|air|earth|null",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "upright_meaning": "Full upright meaning text...",
  "reversed_meaning": "Full reversed meaning text..."
}
```

### Deck Data Structure

The complete deck is stored in a JSON file with this structure:

```json
{
  "deck_info": {
    "name": "Deck Name",
    "version": "1.0.0",
    "description": "Deck description",
    "total_cards": 78,
    "major_arcana_count": 22,
    "minor_arcana_count": 56
  },
  "major_arcana": [
    {
      "id": "the_fool",
      "name": "The Fool",
      "number": 0,
      "element": "air",
      "keywords": ["new_beginnings", "innocence"],
      "upright_meaning": "...",
      "reversed_meaning": "..."
    }
  ],
  "minor_arcana": {
    "wands": {
      "element": "fire",
      "theme": "creativity, passion, inspiration",
      "ace": {
        "keywords": ["inspiration", "creativity"],
        "upright_meaning": "...",
        "reversed_meaning": "..."
      }
    }
  }
}
```

## Testing

The module includes comprehensive unit tests covering:

- Card creation and validation
- Orientation management
- Keyword functionality
- Deck loading and creation
- Shuffling and drawing
- Card filtering and search
- Error handling
- Edge cases

Run tests with:
```bash
python -m pytest tarot_studio/tests/test_deck_module.py -v
```

## Error Handling

The module includes robust error handling for:

- **Invalid card data**: Missing required fields, invalid enums
- **File operations**: Missing files, invalid JSON
- **Deck operations**: Drawing from empty deck, invalid parameters
- **Card operations**: Invalid orientations, missing data

## Performance Considerations

- **Memory efficient**: Cards are loaded once and reused
- **Fast lookups**: Dictionary-based card searching
- **Optimized shuffling**: Uses Python's built-in random.shuffle
- **Lazy loading**: Cards are only created when needed

## Extensibility

The module is designed for easy extension:

- **Custom decks**: Add new card data files
- **Additional metadata**: Extend Card class with new fields
- **Custom drawing logic**: Override Deck methods
- **New card types**: Extend the Card class hierarchy

## Dependencies

- **Python 3.8+**: Uses modern Python features
- **Standard library only**: No external dependencies
- **JSON**: For card data storage
- **Random**: For shuffling functionality
- **Pathlib**: For file operations
- **Dataclasses**: For clean data structures
- **Enum**: For type safety

## Future Enhancements

Potential future enhancements include:

- **Multiple deck support**: Load different tarot decks
- **Custom card creation**: User-defined cards
- **Deck statistics**: Advanced analytics
- **Card relationships**: Predefined card interactions
- **Deck validation**: Ensure deck completeness
- **Performance optimization**: Caching and indexing
- **Internationalization**: Multi-language support

## Contributing

When contributing to the Deck Module:

1. **Follow the existing code style**
2. **Add comprehensive tests** for new functionality
3. **Update documentation** for any API changes
4. **Ensure backward compatibility** when possible
5. **Test with the full 78-card deck** for integration issues

## License

This module is part of the Tarot Studio application and follows the same license terms.