"""
Example Usage of the Tarot Spreads Module

This file demonstrates how to use the spreads module for creating and managing
tarot spreads, including layouts, positions, and complete readings.
"""

import json
from pathlib import Path
from tarot_studio.spreads import (
    SpreadLayout, SpreadPosition, TarotSpread, SpreadManager,
    PositionType
)
from tarot_studio.deck import Deck, Orientation


def example_single_card_reading():
    """Example of a single card reading."""
    print("=== Single Card Reading Example ===")
    
    # Load deck and shuffle
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=42)
    
    # Create single card spread
    spread = TarotSpread.create_single_card_reading(
        deck, 
        "What guidance do I need today?"
    )
    
    # Draw card
    reading = spread.draw_cards()
    
    # Display results
    print(f"Reading ID: {reading.spread_id}")
    print(f"Question: {spread.user_context}")
    print(f"Card: {reading.cards[0].card.name} ({reading.cards[0].card.orientation.value})")
    print(f"Meaning: {reading.cards[0].card.get_meaning()[:100]}...")
    
    return spread, reading


def example_three_card_reading():
    """Example of a three-card reading."""
    print("\n=== Three Card Reading Example ===")
    
    # Load deck and shuffle
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=123)
    
    # Create three card spread
    spread = TarotSpread.create_three_card_reading(
        deck,
        "What does my future hold?"
    )
    
    # Draw cards
    reading = spread.draw_cards()
    
    # Display results
    print(f"Reading ID: {reading.spread_id}")
    print(f"Question: {spread.user_context}")
    print(f"Layout: {spread.layout.name}")
    
    for spread_card in reading.cards:
        print(f"\n{spread_card.position.name}:")
        print(f"  Card: {spread_card.card.name} ({spread_card.card.orientation.value})")
        print(f"  Meaning: {spread_card.card.get_meaning()[:100]}...")
    
    return spread, reading


def example_celtic_cross_reading():
    """Example of a Celtic Cross reading."""
    print("\n=== Celtic Cross Reading Example ===")
    
    # Load deck and shuffle
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=456)
    
    # Create Celtic Cross spread
    spread = TarotSpread.create_celtic_cross_reading(
        deck,
        "I need deep insight into my current situation"
    )
    
    # Draw cards
    reading = spread.draw_cards()
    
    # Display results
    print(f"Reading ID: {reading.spread_id}")
    print(f"Question: {spread.user_context}")
    print(f"Layout: {spread.layout.name}")
    print(f"Cards: {len(reading.cards)}")
    
    # Show first few cards
    for i, spread_card in enumerate(reading.cards[:5]):
        print(f"\n{spread_card.position.name}:")
        print(f"  Card: {spread_card.card.name} ({spread_card.card.orientation.value})")
        print(f"  Description: {spread_card.position.description}")
    
    print(f"\n... and {len(reading.cards) - 5} more cards")
    
    return spread, reading


def example_custom_spread():
    """Example of creating and using a custom spread."""
    print("\n=== Custom Spread Example ===")
    
    # Create spread manager
    manager = SpreadManager()
    
    # Define custom positions
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
            'id': 'obstacle',
            'name': 'Main Obstacle',
            'description': 'What is blocking progress',
            'position_type': 'challenge',
            'coordinates': (0.7, 0.5),
            'importance': 0.9
        },
        {
            'id': 'guidance',
            'name': 'Guidance',
            'description': 'What you need to know',
            'position_type': 'advice',
            'coordinates': (0.5, 0.3),
            'importance': 0.8
        },
        {
            'id': 'outcome',
            'name': 'Likely Outcome',
            'description': 'Where this is heading',
            'position_type': 'outcome',
            'coordinates': (0.5, 0.7),
            'importance': 0.9
        }
    ]
    
    # Create custom spread
    layout = manager.create_custom_spread(
        'situation_analysis',
        'Situation Analysis',
        'A 4-card spread for analyzing current situations',
        positions,
        category='analysis',
        difficulty='intermediate',
        estimated_time=20
    )
    
    print(f"Created custom spread: {layout.name}")
    print(f"Positions: {len(layout.positions)}")
    print(f"Category: {layout.category}")
    print(f"Difficulty: {layout.difficulty}")
    
    # Use the custom spread
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=789)
    
    spread = TarotSpread(layout, deck, "I need to understand my current situation")
    reading = spread.draw_cards()
    
    print(f"\nReading Results:")
    print(f"Question: {spread.user_context}")
    
    for spread_card in reading.cards:
        print(f"\n{spread_card.position.name}:")
        print(f"  Card: {spread_card.card.name} ({spread_card.card.orientation.value})")
        print(f"  Description: {spread_card.position.description}")
        print(f"  Meaning: {spread_card.card.get_meaning()[:100]}...")
    
    return spread, reading


def example_spread_manager():
    """Example of using the spread manager."""
    print("\n=== Spread Manager Example ===")
    
    # Create manager
    manager = SpreadManager()
    
    # Get available spreads
    spreads = manager.get_available_spreads()
    print(f"Available spreads: {len(spreads)}")
    
    # Show spreads by category
    categories = {}
    for spread in spreads:
        category = spread['category']
        categories[category] = categories.get(category, 0) + 1
    
    print(f"Categories: {categories}")
    
    # Show spreads by difficulty
    difficulties = {}
    for spread in spreads:
        difficulty = spread['difficulty']
        difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
    
    print(f"Difficulties: {difficulties}")
    
    # Get statistics
    stats = manager.get_spread_statistics()
    print(f"\nStatistics:")
    print(f"  Total spreads: {stats['total_spreads']}")
    print(f"  Template spreads: {stats['template_spreads']}")
    print(f"  Custom spreads: {stats['custom_spreads']}")
    print(f"  Average card count: {stats['average_card_count']}")
    
    # Search spreads
    search_results = manager.search_spreads("three")
    print(f"\nSearch results for 'three': {len(search_results)}")
    for result in search_results:
        print(f"  - {result['name']}: {result['card_count']} cards")
    
    return manager


def example_spread_with_notes():
    """Example of adding notes to a spread."""
    print("\n=== Spread with Notes Example ===")
    
    # Create spread
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=999)
    
    spread = TarotSpread.create_three_card_reading(
        deck,
        "What should I focus on this week?"
    )
    
    # Draw cards
    reading = spread.draw_cards()
    
    # Add notes to individual positions
    spread.add_notes('past', 'This resonates with my recent job change')
    spread.add_notes('present', 'I can see this in my current relationships')
    spread.add_notes('future', 'This gives me hope for what\'s coming')
    
    # Add notes to entire reading
    spread.add_reading_notes('A very insightful reading that helped clarify my priorities')
    
    # Display results with notes
    print(f"Reading ID: {reading.spread_id}")
    print(f"Question: {spread.user_context}")
    print(f"Reading Notes: {reading.notes}")
    
    for spread_card in reading.cards:
        print(f"\n{spread_card.position.name}:")
        print(f"  Card: {spread_card.card.name} ({spread_card.card.orientation.value})")
        print(f"  Notes: {spread_card.notes}")
    
    return spread, reading


def example_spread_validation():
    """Example of spread validation."""
    print("\n=== Spread Validation Example ===")
    
    # Create valid layout
    valid_layout = SpreadLayout.create_three_card()
    errors = valid_layout.validate()
    print(f"Valid layout errors: {errors}")
    
    # Create invalid layout (empty positions)
    invalid_layout = SpreadLayout(
        id="invalid",
        name="Invalid Layout",
        description="Invalid layout",
        positions=[]
    )
    
    errors = invalid_layout.validate()
    print(f"Invalid layout errors: {errors}")
    
    # Create layout with duplicate IDs
    duplicate_positions = [
        SpreadPosition(
            id="position1",
            name="Position 1",
            description="First position",
            position_type=PositionType.PAST,
            coordinates=(0.2, 0.5),
            importance=0.8
        ),
        SpreadPosition(
            id="position1",  # Duplicate ID
            name="Position 2",
            description="Second position",
            position_type=PositionType.PRESENT,
            coordinates=(0.5, 0.5),
            importance=1.0
        )
    ]
    
    duplicate_layout = SpreadLayout(
        id="duplicate",
        name="Duplicate Layout",
        description="Layout with duplicate IDs",
        positions=duplicate_positions
    )
    
    errors = duplicate_layout.validate()
    print(f"Duplicate layout errors: {errors}")
    
    return valid_layout, invalid_layout, duplicate_layout


def example_spread_file_operations():
    """Example of saving and loading spreads."""
    print("\n=== Spread File Operations Example ===")
    
    # Create a custom spread
    manager = SpreadManager()
    
    positions = [
        {
            'id': 'situation',
            'name': 'Situation',
            'description': 'Current situation',
            'position_type': 'situation',
            'coordinates': (0.3, 0.5),
            'importance': 1.0
        },
        {
            'id': 'advice',
            'name': 'Advice',
            'description': 'Guidance',
            'position_type': 'advice',
            'coordinates': (0.7, 0.5),
            'importance': 0.9
        }
    ]
    
    layout = manager.create_custom_spread(
        'file_test',
        'File Test Spread',
        'A spread for testing file operations',
        positions
    )
    
    # Save to file
    file_path = Path('test_spread.json')
    layout.save_to_file(file_path)
    print(f"Saved spread to: {file_path}")
    
    # Load from file
    loaded_layout = SpreadLayout.load_from_file(file_path)
    print(f"Loaded spread: {loaded_layout.name}")
    print(f"Positions: {len(loaded_layout.positions)}")
    
    # Clean up
    file_path.unlink()
    print("Cleaned up test file")
    
    return layout, loaded_layout


def example_spread_with_orientations():
    """Example of controlling card orientations."""
    print("\n=== Spread with Orientations Example ===")
    
    # Load deck and shuffle
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=111)
    
    # Create spread
    spread = TarotSpread.create_three_card_reading(
        deck,
        "What do I need to know about my past, present, and future?"
    )
    
    # Draw cards with specific orientations
    orientations = [Orientation.UPRIGHT, Orientation.REVERSED, Orientation.UPRIGHT]
    reading = spread.draw_cards(orientations)
    
    print(f"Reading ID: {reading.spread_id}")
    print(f"Question: {spread.user_context}")
    
    for i, spread_card in enumerate(reading.cards):
        print(f"\n{spread_card.position.name}:")
        print(f"  Card: {spread_card.card.name}")
        print(f"  Orientation: {spread_card.card.orientation.value}")
        print(f"  Requested: {orientations[i].value}")
        print(f"  Meaning: {spread_card.card.get_meaning()[:100]}...")
    
    return spread, reading


def main():
    """Run all examples."""
    print("Tarot Spreads Module - Example Usage")
    print("=" * 50)
    
    try:
        # Run examples
        example_single_card_reading()
        example_three_card_reading()
        example_celtic_cross_reading()
        example_custom_spread()
        example_spread_manager()
        example_spread_with_notes()
        example_spread_validation()
        example_spread_file_operations()
        example_spread_with_orientations()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()