#!/usr/bin/env python3
"""
Example usage of the Tarot Deck Module.

This script demonstrates how other modules (like spreads, influence engine, etc.)
would interact with the deck module to draw cards and perform readings.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import the deck module
sys.path.append(str(Path(__file__).parent.parent))

from tarot_studio.deck import Deck, Orientation, Suit, Element


def example_basic_deck_usage():
    """Demonstrate basic deck operations."""
    print("=== Basic Deck Usage ===")
    
    # Load the deck
    deck = Deck.load_from_file('card_data.json')
    print(f"Loaded deck with {len(deck)} cards")
    
    # Shuffle the deck
    deck.shuffle(seed=42)
    print("Deck shuffled")
    
    # Draw a single card
    card = deck.draw_card()
    print(f"Drew card: {card}")
    print(f"Meaning: {card.get_meaning()[:50]}...")
    
    # Draw a reversed card
    reversed_card = deck.draw_card(Orientation.REVERSED)
    print(f"Drew reversed card: {reversed_card}")
    
    # Draw multiple cards
    cards = deck.draw_cards(3, [
        Orientation.UPRIGHT,
        Orientation.REVERSED,
        Orientation.UPRIGHT
    ])
    print(f"Drew 3 cards: {[str(card) for card in cards]}")
    
    print(f"Remaining cards: {len(deck)}")
    print(f"Drawn cards: {deck.count_drawn()}")
    
    # Reset the deck
    deck.reset()
    print(f"After reset: {len(deck)} cards remaining")
    print()


def example_card_filtering():
    """Demonstrate card filtering and search functionality."""
    print("=== Card Filtering and Search ===")
    
    deck = Deck.load_from_file('card_data.json')
    
    # Get Major Arcana cards
    major_cards = deck.get_major_arcana()
    print(f"Major Arcana cards: {len(major_cards)}")
    print(f"First Major Arcana: {major_cards[0].name}")
    
    # Get Minor Arcana cards
    minor_cards = deck.get_minor_arcana()
    print(f"Minor Arcana cards: {len(minor_cards)}")
    
    # Get cards by suit
    wands_cards = deck.get_cards_by_suit(Suit.WANDS)
    print(f"Wands cards: {len(wands_cards)}")
    print(f"First Wands card: {wands_cards[0].name}")
    
    # Get cards by element
    fire_cards = deck.get_cards_by_element(Element.FIRE)
    print(f"Fire element cards: {len(fire_cards)}")
    
    # Search for specific cards
    sun_card = deck.get_card_by_id('the_sun')
    if sun_card:
        print(f"Found The Sun: {sun_card.name}")
        print(f"Keywords: {sun_card.keywords}")
    
    # Search by name
    moon_card = deck.get_card_by_name('The Moon')
    if moon_card:
        print(f"Found The Moon: {moon_card.name}")
    
    # Search by keyword
    joy_cards = deck.get_cards_with_keyword('joy')
    print(f"Cards with 'joy' keyword: {len(joy_cards)}")
    for card in joy_cards:
        print(f"  - {card.name}")
    print()


def example_spreads_integration():
    """Demonstrate how the spreads module would use the deck."""
    print("=== Spreads Module Integration Example ===")
    
    deck = Deck.load_from_file('card_data.json')
    deck.shuffle(seed=123)
    
    def draw_three_card_spread(deck):
        """Draw cards for a three-card spread."""
        positions = ['Past', 'Present', 'Future']
        cards = deck.draw_cards(3)
        
        spread = {}
        for position, card in zip(positions, cards):
            spread[position] = {
                'card': card,
                'name': card.name,
                'orientation': card.orientation.value,
                'meaning': card.get_meaning()
            }
        
        return spread
    
    def draw_celtic_cross_spread(deck):
        """Draw cards for a Celtic Cross spread."""
        positions = [
            'Situation', 'Challenge', 'Past', 'Future',
            'Above', 'Below', 'Advice', 'External',
            'Hopes & Fears', 'Outcome'
        ]
        
        # Draw 10 cards with random orientations
        cards = deck.draw_cards(10)
        
        spread = {}
        for position, card in zip(positions, cards):
            spread[position] = {
                'card': card,
                'name': card.name,
                'orientation': card.orientation.value,
                'meaning': card.get_meaning()
            }
        
        return spread
    
    # Draw a three-card spread
    print("Drawing Three-Card Spread:")
    three_card_spread = draw_three_card_spread(deck)
    for position, card_info in three_card_spread.items():
        print(f"{position}: {card_info['name']} ({card_info['orientation']})")
        print(f"  {card_info['meaning'][:60]}...")
    
    print(f"\nRemaining cards after three-card spread: {len(deck)}")
    
    # Reset and draw Celtic Cross
    deck.reset()
    deck.shuffle(seed=456)
    
    print("\nDrawing Celtic Cross Spread:")
    celtic_spread = draw_celtic_cross_spread(deck)
    for position, card_info in celtic_spread.items():
        print(f"{position}: {card_info['name']} ({card_info['orientation']})")
    
    print(f"\nRemaining cards after Celtic Cross: {len(deck)}")
    print()


def example_influence_engine_integration():
    """Demonstrate how the influence engine would use the deck."""
    print("=== Influence Engine Integration Example ===")
    
    deck = Deck.load_from_file('card_data.json')
    deck.shuffle(seed=789)
    
    def convert_card_for_influence_engine(card):
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
    
    # Draw cards for influence engine
    cards = deck.draw_cards(3)
    
    print("Cards for Influence Engine:")
    for i, card in enumerate(cards, 1):
        print(f"Card {i}: {card.name}")
        
        # Convert to influence engine format
        engine_data = convert_card_for_influence_engine(card)
        
        print(f"  ID: {engine_data['card_id']}")
        print(f"  Arcana: {engine_data['arcana']}")
        print(f"  Element: {engine_data['element']}")
        print(f"  Keywords: {engine_data['keywords']}")
        print(f"  Current meaning: {card.get_meaning()[:50]}...")
        print()
    
    print()


def example_deck_statistics():
    """Demonstrate deck statistics and information."""
    print("=== Deck Statistics ===")
    
    deck = Deck.load_from_file('card_data.json')
    
    # Get deck information
    info = deck.get_deck_info()
    
    print(f"Total cards: {info['total_cards']}")
    print(f"Major Arcana: {info['major_arcana']}")
    print(f"Minor Arcana: {info['minor_arcana']}")
    print(f"Suit distribution:")
    for suit, count in info['suit_counts'].items():
        print(f"  {suit.title()}: {count}")
    print(f"Element distribution:")
    for element, count in info['element_counts'].items():
        print(f"  {element.title()}: {count}")
    
    # Draw some cards and show updated stats
    deck.draw_cards(10)
    updated_info = deck.get_deck_info()
    
    print(f"\nAfter drawing 10 cards:")
    print(f"Remaining: {updated_info['total_cards']}")
    print(f"Drawn: {updated_info['drawn_cards']}")
    print()


def main():
    """Run all examples."""
    print("Tarot Deck Module - Example Usage")
    print("=" * 50)
    
    try:
        example_basic_deck_usage()
        example_card_filtering()
        example_spreads_integration()
        example_influence_engine_integration()
        example_deck_statistics()
        
        print("=" * 50)
        print("✅ All examples completed successfully!")
        print("\nThe Deck Module is ready for integration with other modules.")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())