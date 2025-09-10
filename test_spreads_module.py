#!/usr/bin/env python3
"""
Simple test script for the Tarot Spreads Module.

This script tests the core functionality of the spreads module without pytest.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tarot_studio'))

from tarot_studio.spreads import (
    SpreadLayout, SpreadPosition, TarotSpread, SpreadManager,
    PositionType
)
from tarot_studio.deck import Deck, Orientation


def test_spread_position():
    """Test SpreadPosition functionality."""
    print("Testing SpreadPosition...")
    
    # Create position
    position = SpreadPosition(
        id="test_position",
        name="Test Position",
        description="A test position",
        position_type=PositionType.PRESENT,
        coordinates=(0.5, 0.5),
        importance=1.0
    )
    
    assert position.id == "test_position"
    assert position.name == "Test Position"
    assert position.position_type == PositionType.PRESENT
    
    # Test to_dict
    position_dict = position.to_dict()
    assert position_dict['id'] == "test_position"
    assert position_dict['position_type'] == "present"
    
    # Test from_dict
    restored_position = SpreadPosition.from_dict(position_dict)
    assert restored_position.id == position.id
    assert restored_position.name == position.name
    
    print("✅ SpreadPosition tests passed")


def test_spread_layout():
    """Test SpreadLayout functionality."""
    print("Testing SpreadLayout...")
    
    # Create positions
    positions = [
        SpreadPosition(
            id="position1",
            name="Position 1",
            description="First position",
            position_type=PositionType.PAST,
            coordinates=(0.2, 0.5),
            importance=0.8
        ),
        SpreadPosition(
            id="position2",
            name="Position 2",
            description="Second position",
            position_type=PositionType.PRESENT,
            coordinates=(0.5, 0.5),
            importance=1.0
        )
    ]
    
    # Create layout
    layout = SpreadLayout(
        id="test_layout",
        name="Test Layout",
        description="A test layout",
        positions=positions,
        category="test",
        difficulty="beginner",
        estimated_time=15
    )
    
    assert layout.id == "test_layout"
    assert len(layout.positions) == 2
    assert layout.card_count == 2
    
    # Test validation
    errors = layout.validate()
    assert len(errors) == 0
    
    # Test position retrieval
    position = layout.get_position_by_id("position1")
    assert position is not None
    assert position.name == "Position 1"
    
    # Test positions by type
    present_positions = layout.get_positions_by_type(PositionType.PRESENT)
    assert len(present_positions) == 1
    assert present_positions[0].id == "position2"
    
    # Test to_dict
    layout_dict = layout.to_dict()
    assert layout_dict['id'] == "test_layout"
    assert len(layout_dict['positions']) == 2
    
    # Test from_dict
    restored_layout = SpreadLayout.from_dict(layout_dict)
    assert restored_layout.id == layout.id
    assert len(restored_layout.positions) == len(layout.positions)
    
    print("✅ SpreadLayout tests passed")


def test_predefined_layouts():
    """Test predefined layout creation."""
    print("Testing predefined layouts...")
    
    # Test single card
    single_layout = SpreadLayout.create_single_card()
    assert single_layout.id == "single_card"
    assert len(single_layout.positions) == 1
    assert single_layout.positions[0].id == "guidance"
    
    # Test three card
    three_layout = SpreadLayout.create_three_card()
    assert three_layout.id == "three_card"
    assert len(three_layout.positions) == 3
    position_ids = [pos.id for pos in three_layout.positions]
    assert "past" in position_ids
    assert "present" in position_ids
    assert "future" in position_ids
    
    # Test Celtic Cross
    celtic_layout = SpreadLayout.create_celtic_cross()
    assert celtic_layout.id == "celtic_cross"
    assert len(celtic_layout.positions) == 10
    assert celtic_layout.difficulty == "intermediate"
    
    print("✅ Predefined layouts tests passed")


def test_tarot_spread():
    """Test TarotSpread functionality."""
    print("Testing TarotSpread...")
    
    # Load deck
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=42)
    
    # Create spread
    layout = SpreadLayout.create_three_card()
    spread = TarotSpread(layout, deck, "What does my future hold?")
    
    assert spread.layout == layout
    assert spread.deck == deck
    assert spread.user_context == "What does my future hold?"
    assert spread.reading is None
    
    # Draw cards
    reading = spread.draw_cards()
    
    assert reading is not None
    assert reading.spread_id is not None
    assert len(reading.cards) == 3
    assert reading.user_context == "What does my future hold?"
    
    # Check that cards were drawn from deck
    assert len(deck) == 75  # 78 - 3 = 75
    
    # Test reading summary
    summary = spread.get_reading_summary()
    assert summary['spread_id'] == reading.spread_id
    assert summary['card_count'] == 3
    assert summary['layout_name'] == "Three Card"
    
    # Test position meanings
    meanings = spread.get_all_meanings()
    assert len(meanings) == 3
    assert 'past' in meanings
    assert 'present' in meanings
    assert 'future' in meanings
    
    # Test adding notes
    spread.add_notes('present', 'This feels very relevant')
    spread.add_reading_notes('A very insightful reading')
    
    present_card = reading.get_card_by_position('present')
    assert present_card.notes == 'This feels very relevant'
    assert reading.notes == 'A very insightful reading'
    
    print("✅ TarotSpread tests passed")


def test_spread_manager():
    """Test SpreadManager functionality."""
    print("Testing SpreadManager...")
    
    # Create manager
    manager = SpreadManager()
    
    assert len(manager.spread_templates) > 0
    assert len(manager.custom_spreads) == 0
    
    # Test available spreads
    spreads = manager.get_available_spreads()
    assert len(spreads) > 0
    
    # Check that default templates are loaded
    assert 'single_card' in manager.spread_templates
    assert 'three_card' in manager.spread_templates
    assert 'celtic_cross' in manager.spread_templates
    
    # Test getting spread layout
    layout = manager.get_spread_layout('three_card')
    assert layout is not None
    assert layout.id == 'three_card'
    
    # Test creating custom spread
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
    
    custom_layout = manager.create_custom_spread(
        'custom_test',
        'Custom Test Spread',
        'A test custom spread',
        positions,
        category='test',
        difficulty='beginner',
        estimated_time=10
    )
    
    assert custom_layout.id == 'custom_test'
    assert len(custom_layout.positions) == 2
    assert 'custom_test' in manager.custom_spreads
    
    # Test creating spread from template
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=123)
    
    spread = manager.create_spread_from_template(
        'three_card',
        deck,
        'Test reading'
    )
    
    assert spread.layout.id == 'three_card'
    assert spread.deck == deck
    assert spread.user_context == 'Test reading'
    
    # Test statistics
    stats = manager.get_spread_statistics()
    assert 'total_spreads' in stats
    assert 'template_spreads' in stats
    assert 'custom_spreads' in stats
    assert stats['template_spreads'] > 0
    assert stats['custom_spreads'] == 1  # We created one custom spread
    
    print("✅ SpreadManager tests passed")


def test_integration():
    """Test integration between components."""
    print("Testing integration...")
    
    # Create manager and deck
    manager = SpreadManager()
    deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
    deck.shuffle(seed=456)
    
    # Create spread from template
    spread = manager.create_spread_from_template(
        'three_card',
        deck,
        'What does my future hold?'
    )
    
    # Draw cards
    reading = spread.draw_cards()
    
    # Verify reading
    assert reading is not None
    assert len(reading.cards) == 3
    assert reading.user_context == 'What does my future hold?'
    
    # Get summary
    summary = spread.get_reading_summary()
    assert summary['card_count'] == 3
    assert summary['layout_name'] == 'Three Card'
    
    # Add to recent readings
    manager.add_recent_reading(reading)
    assert len(manager.recent_readings) == 1
    
    # Test position meanings
    meanings = spread.get_all_meanings()
    assert len(meanings) == 3
    
    # Add notes
    spread.add_notes('present', 'This feels very relevant')
    spread.add_reading_notes('A very insightful reading')
    
    assert reading.get_card_by_position('present').notes == 'This feels very relevant'
    assert reading.notes == 'A very insightful reading'
    
    print("✅ Integration tests passed")


def main():
    """Run all tests."""
    print("Tarot Spreads Module - Test Suite")
    print("=" * 50)
    
    try:
        test_spread_position()
        test_spread_layout()
        test_predefined_layouts()
        test_tarot_spread()
        test_spread_manager()
        test_integration()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! The spreads module is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)