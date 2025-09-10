# Tarot Spreads Module

The Tarot Spreads Module provides comprehensive functionality for creating, managing, and executing tarot spreads. It includes predefined layouts, custom spread creation, position management, and integration with the deck and influence engine modules.

## Features

- **Predefined Spreads**: Single Card, Three Card, Celtic Cross, Relationship Cross, Year Ahead
- **Custom Spread Creation**: Build your own spreads with custom positions and layouts
- **Position Management**: Define positions with types, coordinates, and importance levels
- **Spread Validation**: Ensure spreads are valid and well-formed
- **File Operations**: Save and load spread configurations
- **Integration**: Seamless integration with Deck and Influence Engine modules
- **Spread Manager**: Centralized management of all spreads and templates

## Quick Start

```python
from tarot_studio.spreads import TarotSpread, SpreadManager
from tarot_studio.deck import Deck

# Load deck and create spread
deck = Deck.load_from_file('card_data.json')
deck.shuffle()

# Create a three-card reading
spread = TarotSpread.create_three_card_reading(
    deck, 
    "What does my future hold?"
)

# Draw cards
reading = spread.draw_cards()

# Get meanings
for spread_card in reading.cards:
    print(f"{spread_card.position.name}: {spread_card.card.name}")
    print(f"Meaning: {spread_card.card.get_meaning()}")
```

## Core Classes

### SpreadLayout

Defines the structure and positions of a tarot spread.

```python
from tarot_studio.spreads import SpreadLayout

# Create a custom layout
layout = SpreadLayout(
    id="my_spread",
    name="My Custom Spread",
    description="A spread for personal guidance",
    positions=[
        SpreadPosition(
            id="situation",
            name="Current Situation",
            description="What is happening now",
            position_type=PositionType.SITUATION,
            coordinates=(0.3, 0.5),
            importance=1.0
        )
    ]
)

# Validate layout
errors = layout.validate()
if not errors:
    print("Layout is valid!")
```

### TarotSpread

Manages a complete tarot spread with cards and meanings.

```python
from tarot_studio.spreads import TarotSpread

# Create spread from layout
spread = TarotSpread(layout, deck, "What guidance do I need?")

# Draw cards
reading = spread.draw_cards()

# Get reading summary
summary = spread.get_reading_summary()
print(f"Layout: {summary['layout_name']}")
print(f"Cards: {summary['card_count']}")

# Get position meanings
meanings = spread.get_all_meanings()
for position_id, meaning in meanings.items():
    print(f"{position_id}: {meaning}")
```

### SpreadManager

Centralized management of spreads and templates.

```python
from tarot_studio.spreads import SpreadManager

# Create manager
manager = SpreadManager()

# Get available spreads
spreads = manager.get_available_spreads()
print(f"Available spreads: {len(spreads)}")

# Create custom spread
positions = [
    {
        'id': 'situation',
        'name': 'Situation',
        'description': 'Current situation',
        'position_type': 'situation',
        'coordinates': (0.3, 0.5),
        'importance': 1.0
    }
]

layout = manager.create_custom_spread(
    'my_custom',
    'My Custom Spread',
    'A custom spread',
    positions
)

# Create spread from template
spread = manager.create_spread_from_template(
    'three_card',
    deck,
    'What does my future hold?'
)
```

## Predefined Spreads

### Single Card
- **ID**: `single_card`
- **Cards**: 1
- **Purpose**: Daily guidance and quick insights
- **Difficulty**: Beginner
- **Time**: 5 minutes

### Three Card
- **ID**: `three_card`
- **Cards**: 3
- **Purpose**: Past, Present, Future readings
- **Difficulty**: Beginner
- **Time**: 15 minutes

### Celtic Cross
- **ID**: `celtic_cross`
- **Cards**: 10
- **Purpose**: Comprehensive life analysis
- **Difficulty**: Intermediate
- **Time**: 45 minutes

### Relationship Cross
- **ID**: `relationship_cross`
- **Cards**: 7
- **Purpose**: Relationship insights
- **Difficulty**: Intermediate
- **Time**: 30 minutes

### Year Ahead
- **ID**: `year_ahead`
- **Cards**: 12
- **Purpose**: Yearly guidance
- **Difficulty**: Advanced
- **Time**: 60 minutes

## Position Types

The module supports various position types for semantic meaning:

- `PAST`: Past influences and events
- `PRESENT`: Current circumstances
- `FUTURE`: Future possibilities
- `SITUATION`: Current situation
- `CHALLENGE`: Obstacles and difficulties
- `ADVICE`: Guidance and recommendations
- `OUTCOME`: Likely results
- `HOPES_FEARS`: Inner hopes and concerns
- `EXTERNAL`: External influences
- `ABOVE`: Conscious goals
- `BELOW`: Subconscious influences
- `LESSON`: Learning opportunities
- `CONNECTION`: Relationships and bonds
- `PARTNER`: Partner's perspective
- `YOU`: Your perspective
- `CUSTOM`: Custom position type

## Custom Spread Creation

Create your own spreads with custom positions and layouts:

```python
# Define positions
positions = [
    {
        'id': 'situation',
        'name': 'Current Situation',
        'description': 'What is happening now',
        'position_type': 'situation',
        'coordinates': (0.3, 0.5),
        'importance': 1.0
    },
    {
        'id': 'advice',
        'name': 'Advice',
        'description': 'What you need to know',
        'position_type': 'advice',
        'coordinates': (0.7, 0.5),
        'importance': 0.9
    }
]

# Create custom spread
layout = manager.create_custom_spread(
    'my_spread',
    'My Custom Spread',
    'A spread for personal guidance',
    positions,
    category='personal',
    difficulty='beginner',
    estimated_time=15
)
```

## Spread Validation

All spreads are validated to ensure they are well-formed:

```python
# Validate layout
errors = layout.validate()
if errors:
    print(f"Validation errors: {errors}")
else:
    print("Layout is valid!")
```

Common validation checks:
- No duplicate position IDs
- At least one position
- Reasonable card count (max 21 recommended)
- Valid importance values (0.0 to 2.0)

## File Operations

Save and load spread configurations:

```python
# Save spread to file
layout.save_to_file('my_spread.json')

# Load spread from file
loaded_layout = SpreadLayout.load_from_file('my_spread.json')

# Export all spreads
manager.export_all_spreads('all_spreads.json')

# Import spreads
stats = manager.import_spreads('all_spreads.json')
print(f"Imported: {stats['imported_templates']} templates, {stats['imported_custom']} custom")
```

## Integration with Other Modules

### Deck Integration

```python
from tarot_studio.deck import Deck

# Load deck
deck = Deck.load_from_file('card_data.json')
deck.shuffle()

# Create spread
spread = TarotSpread.create_three_card_reading(deck, "What does my future hold?")

# Draw cards
reading = spread.draw_cards()

# Reset deck if needed
spread.reset_deck()
```

### Influence Engine Integration

```python
from tarot_studio.core.enhanced_influence_engine import EnhancedInfluenceEngine

# Apply influence engine
card_database = load_card_database()  # Your card database
influenced_meanings = spread.apply_influence_engine(card_database)

# Get enhanced meanings
for card_data in influenced_meanings['cards']:
    print(f"Position: {card_data['position']}")
    print(f"Enhanced meaning: {card_data['influenced_text']}")
```

## Advanced Features

### Position Importance

Control the relative importance of positions:

```python
position = SpreadPosition(
    id="important",
    name="Important Position",
    description="Most important position",
    position_type=PositionType.PRESENT,
    importance=1.5  # Higher importance
)

# Get most important positions
important_positions = layout.get_most_important_positions(3)
```

### Coordinate System

Use coordinates for visual layout:

```python
position = SpreadPosition(
    id="center",
    name="Center Position",
    description="Center of the spread",
    position_type=PositionType.PRESENT,
    coordinates=(0.5, 0.5)  # Center coordinates
)
```

### Notes and Context

Add notes to positions and readings:

```python
# Add notes to position
spread.add_notes('present', 'This feels very relevant')

# Add notes to entire reading
spread.add_reading_notes('A very insightful reading')

# Get notes
present_card = reading.get_card_by_position('present')
print(f"Notes: {present_card.notes}")
```

## Error Handling

The module provides comprehensive error handling:

```python
try:
    # Create spread with invalid layout
    spread = TarotSpread(invalid_layout, deck)
except ValueError as e:
    print(f"Error: {e}")

try:
    # Draw cards when deck is empty
    reading = spread.draw_cards()
except ValueError as e:
    print(f"Error: {e}")
```

## Testing

Run the test suite:

```bash
python -m pytest tarot_studio/tests/test_spreads_module.py -v
```

## Examples

See `example_usage.py` for comprehensive examples of all module features.

## Dependencies

- `tarot_studio.deck`: Deck module for card management
- `tarot_studio.core.enhanced_influence_engine`: Influence engine for enhanced meanings
- Standard library: `json`, `pathlib`, `datetime`, `uuid`, `dataclasses`, `enum`

## Version

Current version: 1.0.0

## License

Part of the Tarot Studio project.