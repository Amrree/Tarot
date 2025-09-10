"""
Unit tests for the Tarot Spreads Module.

This module contains comprehensive tests for all spread-related functionality,
including layouts, spreads, and the spread manager.
"""

import pytest
import json
import tempfile
import os
from typing import Dict, Any, List
from datetime import datetime
from tarot_studio.spreads import (
    SpreadLayout, SpreadPosition, TarotSpread, SpreadManager,
    PositionType, SpreadCard, SpreadReading
)
from tarot_studio.deck import Deck, Orientation


class TestSpreadPosition:
    """Test suite for SpreadPosition class."""
    
    def test_position_creation(self):
        """Test creating a spread position."""
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
        assert position.description == "A test position"
        assert position.position_type == PositionType.PRESENT
        assert position.coordinates == (0.5, 0.5)
        assert position.importance == 1.0
    
    def test_position_to_dict(self):
        """Test converting position to dictionary."""
        position = SpreadPosition(
            id="test_position",
            name="Test Position",
            description="A test position",
            position_type=PositionType.PRESENT,
            coordinates=(0.5, 0.5),
            importance=1.0
        )
        
        position_dict = position.to_dict()
        
        assert position_dict['id'] == "test_position"
        assert position_dict['name'] == "Test Position"
        assert position_dict['description'] == "A test position"
        assert position_dict['position_type'] == "present"
        assert position_dict['coordinates'] == (0.5, 0.5)
        assert position_dict['importance'] == 1.0
    
    def test_position_from_dict(self):
        """Test creating position from dictionary."""
        position_data = {
            'id': 'test_position',
            'name': 'Test Position',
            'description': 'A test position',
            'position_type': 'present',
            'coordinates': (0.5, 0.5),
            'importance': 1.0
        }
        
        position = SpreadPosition.from_dict(position_data)
        
        assert position.id == "test_position"
        assert position.name == "Test Position"
        assert position.description == "A test position"
        assert position.position_type == PositionType.PRESENT
        assert position.coordinates == (0.5, 0.5)
        assert position.importance == 1.0


class TestSpreadLayout:
    """Test suite for SpreadLayout class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_positions = [
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
            ),
            SpreadPosition(
                id="position3",
                name="Position 3",
                description="Third position",
                position_type=PositionType.FUTURE,
                coordinates=(0.8, 0.5),
                importance=0.8
            )
        ]
    
    def test_layout_creation(self):
        """Test creating a spread layout."""
        layout = SpreadLayout(
            id="test_layout",
            name="Test Layout",
            description="A test layout",
            positions=self.test_positions,
            category="test",
            difficulty="beginner",
            estimated_time=15
        )
        
        assert layout.id == "test_layout"
        assert layout.name == "Test Layout"
        assert layout.description == "A test layout"
        assert len(layout.positions) == 3
        assert layout.category == "test"
        assert layout.difficulty == "beginner"
        assert layout.estimated_time == 15
        assert layout.card_count == 3
    
    def test_layout_add_position(self):
        """Test adding a position to a layout."""
        layout = SpreadLayout(
            id="test_layout",
            name="Test Layout",
            description="A test layout",
            positions=self.test_positions[:2]
        )
        
        assert layout.card_count == 2
        
        new_position = SpreadPosition(
            id="position4",
            name="Position 4",
            description="Fourth position",
            position_type=PositionType.ADVICE,
            coordinates=(0.5, 0.8),
            importance=0.9
        )
        
        layout.add_position(new_position)
        
        assert len(layout.positions) == 3
        assert layout.card_count == 3
    
    def test_layout_get_position_by_id(self):
        """Test getting a position by ID."""
        layout = SpreadLayout(
            id="test_layout",
            name="Test Layout",
            description="A test layout",
            positions=self.test_positions
        )
        
        position = layout.get_position_by_id("position2")
        assert position is not None
        assert position.name == "Position 2"
        
        position = layout.get_position_by_id("nonexistent")
        assert position is None
    
    def test_layout_get_positions_by_type(self):
        """Test getting positions by type."""
        layout = SpreadLayout(
            id="test_layout",
            name="Test Layout",
            description="A test layout",
            positions=self.test_positions
        )
        
        present_positions = layout.get_positions_by_type(PositionType.PRESENT)
        assert len(present_positions) == 1
        assert present_positions[0].id == "position2"
        
        past_positions = layout.get_positions_by_type(PositionType.PAST)
        assert len(past_positions) == 1
        assert past_positions[0].id == "position1"
    
    def test_layout_get_most_important_positions(self):
        """Test getting most important positions."""
        layout = SpreadLayout(
            id="test_layout",
            name="Test Layout",
            description="A test layout",
            positions=self.test_positions
        )
        
        important_positions = layout.get_most_important_positions(2)
        assert len(important_positions) == 2
        assert important_positions[0].id == "position2"  # importance 1.0
        assert important_positions[1].id in ["position1", "position3"]  # importance 0.8
    
    def test_layout_validation(self):
        """Test layout validation."""
        # Valid layout
        layout = SpreadLayout(
            id="test_layout",
            name="Test Layout",
            description="A test layout",
            positions=self.test_positions
        )
        
        errors = layout.validate()
        assert len(errors) == 0
        
        # Layout with duplicate IDs
        duplicate_positions = self.test_positions + [
            SpreadPosition(
                id="position1",  # Duplicate ID
                name="Duplicate Position",
                description="Duplicate position",
                position_type=PositionType.ADVICE,
                coordinates=(0.5, 0.8),
                importance=0.9
            )
        ]
        
        layout_with_duplicates = SpreadLayout(
            id="test_layout",
            name="Test Layout",
            description="A test layout",
            positions=duplicate_positions
        )
        
        errors = layout_with_duplicates.validate()
        assert len(errors) > 0
        assert "Duplicate position IDs" in errors[0]
        
        # Empty layout
        empty_layout = SpreadLayout(
            id="empty_layout",
            name="Empty Layout",
            description="An empty layout",
            positions=[]
        )
        
        errors = empty_layout.validate()
        assert len(errors) > 0
        assert "Spread must have at least one position" in errors[0]
    
    def test_layout_to_dict(self):
        """Test converting layout to dictionary."""
        layout = SpreadLayout(
            id="test_layout",
            name="Test Layout",
            description="A test layout",
            positions=self.test_positions,
            category="test",
            difficulty="beginner",
            estimated_time=15
        )
        
        layout_dict = layout.to_dict()
        
        assert layout_dict['id'] == "test_layout"
        assert layout_dict['name'] == "Test Layout"
        assert layout_dict['description'] == "A test layout"
        assert len(layout_dict['positions']) == 3
        assert layout_dict['category'] == "test"
        assert layout_dict['difficulty'] == "beginner"
        assert layout_dict['estimated_time'] == 15
        assert layout_dict['card_count'] == 3
    
    def test_layout_from_dict(self):
        """Test creating layout from dictionary."""
        layout_data = {
            'id': 'test_layout',
            'name': 'Test Layout',
            'description': 'A test layout',
            'positions': [
                {
                    'id': 'position1',
                    'name': 'Position 1',
                    'description': 'First position',
                    'position_type': 'past',
                    'coordinates': (0.2, 0.5),
                    'importance': 0.8
                },
                {
                    'id': 'position2',
                    'name': 'Position 2',
                    'description': 'Second position',
                    'position_type': 'present',
                    'coordinates': (0.5, 0.5),
                    'importance': 1.0
                }
            ],
            'category': 'test',
            'difficulty': 'beginner',
            'estimated_time': 15,
            'card_count': 2
        }
        
        layout = SpreadLayout.from_dict(layout_data)
        
        assert layout.id == "test_layout"
        assert layout.name == "Test Layout"
        assert layout.description == "A test layout"
        assert len(layout.positions) == 2
        assert layout.category == "test"
        assert layout.difficulty == "beginner"
        assert layout.estimated_time == 15
        assert layout.card_count == 2
    
    def test_create_single_card_layout(self):
        """Test creating single card layout."""
        layout = SpreadLayout.create_single_card()
        
        assert layout.id == "single_card"
        assert layout.name == "Single Card"
        assert len(layout.positions) == 1
        assert layout.positions[0].id == "guidance"
        assert layout.card_count == 1
        assert layout.category == "daily"
        assert layout.difficulty == "beginner"
    
    def test_create_three_card_layout(self):
        """Test creating three card layout."""
        layout = SpreadLayout.create_three_card()
        
        assert layout.id == "three_card"
        assert layout.name == "Three Card"
        assert len(layout.positions) == 3
        assert layout.card_count == 3
        assert layout.category == "general"
        assert layout.difficulty == "beginner"
        
        # Check position IDs
        position_ids = [pos.id for pos in layout.positions]
        assert "past" in position_ids
        assert "present" in position_ids
        assert "future" in position_ids
    
    def test_create_celtic_cross_layout(self):
        """Test creating Celtic Cross layout."""
        layout = SpreadLayout.create_celtic_cross()
        
        assert layout.id == "celtic_cross"
        assert layout.name == "Celtic Cross"
        assert len(layout.positions) == 10
        assert layout.card_count == 10
        assert layout.category == "comprehensive"
        assert layout.difficulty == "intermediate"
        assert layout.estimated_time == 45
        
        # Check position IDs
        position_ids = [pos.id for pos in layout.positions]
        assert "situation" in position_ids
        assert "challenge" in position_ids
        assert "past" in position_ids
        assert "future" in position_ids
        assert "outcome" in position_ids
    
    def test_layout_file_operations(self):
        """Test saving and loading layouts to/from files."""
        layout = SpreadLayout.create_three_card()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save layout
            layout.save_to_file(temp_file)
            
            # Load layout
            loaded_layout = SpreadLayout.load_from_file(temp_file)
            
            assert loaded_layout.id == layout.id
            assert loaded_layout.name == layout.name
            assert len(loaded_layout.positions) == len(layout.positions)
            assert loaded_layout.card_count == layout.card_count
            
        finally:
            os.unlink(temp_file)


class TestTarotSpread:
    """Test suite for TarotSpread class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.layout = SpreadLayout.create_three_card()
        self.deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
        self.deck.shuffle(seed=42)
        self.user_context = "What does my future hold?"
    
    def test_spread_creation(self):
        """Test creating a tarot spread."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        
        assert spread.layout == self.layout
        assert spread.deck == self.deck
        assert spread.user_context == self.user_context
        assert spread.reading is None
    
    def test_spread_creation_invalid_layout(self):
        """Test creating spread with invalid layout."""
        # Create invalid layout (empty positions)
        invalid_layout = SpreadLayout(
            id="invalid",
            name="Invalid Layout",
            description="Invalid layout",
            positions=[]
        )
        
        with pytest.raises(ValueError, match="Invalid spread layout"):
            TarotSpread(invalid_layout, self.deck, self.user_context)
    
    def test_draw_cards(self):
        """Test drawing cards for the spread."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        
        reading = spread.draw_cards()
        
        assert reading is not None
        assert reading.spread_id is not None
        assert reading.layout == self.layout
        assert len(reading.cards) == 3
        assert reading.user_context == self.user_context
        
        # Check that cards were drawn from deck
        assert len(self.deck) == 75  # 78 - 3 = 75
        
        # Check card positions
        position_ids = [card.position.id for card in reading.cards]
        assert "past" in position_ids
        assert "present" in position_ids
        assert "future" in position_ids
    
    def test_draw_cards_with_orientations(self):
        """Test drawing cards with specific orientations."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        
        orientations = [Orientation.UPRIGHT, Orientation.REVERSED, Orientation.UPRIGHT]
        reading = spread.draw_cards(orientations)
        
        assert reading.cards[0].card.orientation == Orientation.UPRIGHT
        assert reading.cards[1].card.orientation == Orientation.REVERSED
        assert reading.cards[2].card.orientation == Orientation.UPRIGHT
    
    def test_draw_cards_insufficient_cards(self):
        """Test drawing cards when deck doesn't have enough cards."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        
        # Draw most cards from deck
        self.deck.draw_cards(76)  # Leave only 2 cards
        
        with pytest.raises(ValueError, match="Deck has 2 cards, but spread requires 3"):
            spread.draw_cards()
    
    def test_draw_cards_invalid_orientations(self):
        """Test drawing cards with invalid orientations list."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        
        orientations = [Orientation.UPRIGHT, Orientation.REVERSED]  # Only 2 orientations for 3 cards
        
        with pytest.raises(ValueError, match="Orientations list must have 3 elements"):
            spread.draw_cards(orientations)
    
    def test_get_reading_summary(self):
        """Test getting reading summary."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        reading = spread.draw_cards()
        
        summary = spread.get_reading_summary()
        
        assert summary['spread_id'] == reading.spread_id
        assert summary['layout_name'] == self.layout.name
        assert summary['card_count'] == 3
        assert summary['user_context'] == self.user_context
        assert summary['has_influenced_meanings'] == False
        assert len(summary['cards']) == 3
        
        # Check card information
        for card_info in summary['cards']:
            assert 'position' in card_info
            assert 'card_name' in card_info
            assert 'orientation' in card_info
            assert 'importance' in card_info
    
    def test_get_reading_summary_no_reading(self):
        """Test getting summary when no reading drawn."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        
        with pytest.raises(ValueError, match="No reading drawn yet"):
            spread.get_reading_summary()
    
    def test_get_position_meaning(self):
        """Test getting position meaning."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        reading = spread.draw_cards()
        
        # Get meaning for a position
        meaning = spread.get_position_meaning('past')
        assert meaning is not None
        assert len(meaning) > 0
        
        # Get meaning for non-existent position
        meaning = spread.get_position_meaning('nonexistent')
        assert meaning is None
    
    def test_get_all_meanings(self):
        """Test getting all position meanings."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        reading = spread.draw_cards()
        
        meanings = spread.get_all_meanings()
        
        assert len(meanings) == 3
        assert 'past' in meanings
        assert 'present' in meanings
        assert 'future' in meanings
        
        for position_id, meaning in meanings.items():
            assert meaning is not None
            assert len(meaning) > 0
    
    def test_add_notes(self):
        """Test adding notes to positions and reading."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        reading = spread.draw_cards()
        
        # Add notes to a position
        spread.add_notes('present', 'This feels very relevant')
        
        present_card = reading.get_card_by_position('present')
        assert present_card.notes == 'This feels very relevant'
        
        # Add notes to entire reading
        spread.add_reading_notes('A very insightful reading')
        assert reading.notes == 'A very insightful reading'
    
    def test_add_notes_no_reading(self):
        """Test adding notes when no reading drawn."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        
        with pytest.raises(ValueError, match="No reading drawn yet"):
            spread.add_notes('present', 'Test notes')
        
        with pytest.raises(ValueError, match="No reading drawn yet"):
            spread.add_reading_notes('Test reading notes')
    
    def test_reset_deck(self):
        """Test resetting the deck."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        reading = spread.draw_cards()
        
        # Deck should have fewer cards after drawing
        assert len(self.deck) == 75
        
        # Reset deck
        spread.reset_deck()
        
        # Deck should be back to full size
        assert len(self.deck) == 78
    
    def test_to_dict(self):
        """Test converting spread to dictionary."""
        spread = TarotSpread(self.layout, self.deck, self.user_context)
        reading = spread.draw_cards()
        
        spread_dict = spread.to_dict()
        
        assert 'layout' in spread_dict
        assert 'user_context' in spread_dict
        assert 'reading' in spread_dict
        
        assert spread_dict['user_context'] == self.user_context
        assert spread_dict['reading']['spread_id'] == reading.spread_id
        assert len(spread_dict['reading']['cards']) == 3
    
    def test_create_from_layout(self):
        """Test creating spread from layout."""
        spread = TarotSpread.create_from_layout(self.layout, self.deck, self.user_context)
        
        assert spread.layout == self.layout
        assert spread.deck == self.deck
        assert spread.user_context == self.user_context
    
    def test_create_three_card_reading(self):
        """Test creating three card reading."""
        spread = TarotSpread.create_three_card_reading(self.deck, self.user_context)
        
        assert spread.layout.id == "three_card"
        assert spread.deck == self.deck
        assert spread.user_context == self.user_context
    
    def test_create_celtic_cross_reading(self):
        """Test creating Celtic Cross reading."""
        spread = TarotSpread.create_celtic_cross_reading(self.deck, self.user_context)
        
        assert spread.layout.id == "celtic_cross"
        assert spread.deck == self.deck
        assert spread.user_context == self.user_context
    
    def test_create_single_card_reading(self):
        """Test creating single card reading."""
        spread = TarotSpread.create_single_card_reading(self.deck, self.user_context)
        
        assert spread.layout.id == "single_card"
        assert spread.deck == self.deck
        assert spread.user_context == self.user_context


class TestSpreadManager:
    """Test suite for SpreadManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = SpreadManager()
        self.deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
        self.deck.shuffle(seed=42)
    
    def test_manager_initialization(self):
        """Test spread manager initialization."""
        assert len(self.manager.spread_templates) > 0
        assert len(self.manager.custom_spreads) == 0
        assert len(self.manager.recent_readings) == 0
        
        # Check that default templates are loaded
        assert 'single_card' in self.manager.spread_templates
        assert 'three_card' in self.manager.spread_templates
        assert 'celtic_cross' in self.manager.spread_templates
    
    def test_get_available_spreads(self):
        """Test getting available spreads."""
        spreads = self.manager.get_available_spreads()
        
        assert len(spreads) > 0
        
        # Check that all spreads have required fields
        for spread in spreads:
            assert 'id' in spread
            assert 'name' in spread
            assert 'description' in spread
            assert 'category' in spread
            assert 'difficulty' in spread
            assert 'card_count' in spread
            assert 'type' in spread
    
    def test_get_spreads_by_category(self):
        """Test getting spreads by category."""
        daily_spreads = self.manager.get_spreads_by_category('daily')
        general_spreads = self.manager.get_spreads_by_category('general')
        
        assert len(daily_spreads) > 0
        assert len(general_spreads) > 0
        
        for spread in daily_spreads:
            assert spread['category'] == 'daily'
        
        for spread in general_spreads:
            assert spread['category'] == 'general'
    
    def test_get_spreads_by_difficulty(self):
        """Test getting spreads by difficulty."""
        beginner_spreads = self.manager.get_spreads_by_difficulty('beginner')
        intermediate_spreads = self.manager.get_spreads_by_difficulty('intermediate')
        
        assert len(beginner_spreads) > 0
        assert len(intermediate_spreads) > 0
        
        for spread in beginner_spreads:
            assert spread['difficulty'] == 'beginner'
        
        for spread in intermediate_spreads:
            assert spread['difficulty'] == 'intermediate'
    
    def test_get_spread_layout(self):
        """Test getting spread layout by ID."""
        # Test getting template
        layout = self.manager.get_spread_layout('three_card')
        assert layout is not None
        assert layout.id == 'three_card'
        
        # Test getting non-existent spread
        layout = self.manager.get_spread_layout('nonexistent')
        assert layout is None
    
    def test_create_custom_spread(self):
        """Test creating custom spread."""
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
        
        layout = self.manager.create_custom_spread(
            'custom_test',
            'Custom Test Spread',
            'A test custom spread',
            positions,
            category='test',
            difficulty='beginner',
            estimated_time=10
        )
        
        assert layout.id == 'custom_test'
        assert layout.name == 'Custom Test Spread'
        assert len(layout.positions) == 2
        assert 'custom_test' in self.manager.custom_spreads
    
    def test_create_custom_spread_duplicate_id(self):
        """Test creating custom spread with duplicate ID."""
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
        
        # Create first spread
        self.manager.create_custom_spread(
            'duplicate_test',
            'First Spread',
            'First spread',
            positions
        )
        
        # Try to create second spread with same ID
        with pytest.raises(ValueError, match="Spread ID 'duplicate_test' already exists"):
            self.manager.create_custom_spread(
                'duplicate_test',
                'Second Spread',
                'Second spread',
                positions
            )
    
    def test_create_spread_from_template(self):
        """Test creating spread from template."""
        spread = self.manager.create_spread_from_template(
            'three_card',
            self.deck,
            'Test reading'
        )
        
        assert spread.layout.id == 'three_card'
        assert spread.deck == self.deck
        assert spread.user_context == 'Test reading'
    
    def test_create_spread_from_template_not_found(self):
        """Test creating spread from non-existent template."""
        with pytest.raises(ValueError, match="Template 'nonexistent' not found"):
            self.manager.create_spread_from_template(
                'nonexistent',
                self.deck,
                'Test reading'
            )
    
    def test_save_and_load_custom_spread(self):
        """Test saving and loading custom spread."""
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
        
        # Create custom spread
        layout = self.manager.create_custom_spread(
            'save_test',
            'Save Test Spread',
            'A spread for testing save/load',
            positions
        )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save spread
            self.manager.save_custom_spread('save_test', temp_file)
            
            # Create new manager and load spread
            new_manager = SpreadManager()
            loaded_layout = new_manager.load_custom_spread(temp_file)
            
            assert loaded_layout.id == 'save_test'
            assert loaded_layout.name == 'Save Test Spread'
            assert len(loaded_layout.positions) == 1
            
        finally:
            os.unlink(temp_file)
    
    def test_delete_custom_spread(self):
        """Test deleting custom spread."""
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
        
        # Create custom spread
        self.manager.create_custom_spread(
            'delete_test',
            'Delete Test Spread',
            'A spread for testing deletion',
            positions
        )
        
        assert 'delete_test' in self.manager.custom_spreads
        
        # Delete spread
        result = self.manager.delete_custom_spread('delete_test')
        assert result == True
        assert 'delete_test' not in self.manager.custom_spreads
        
        # Try to delete non-existent spread
        result = self.manager.delete_custom_spread('nonexistent')
        assert result == False
    
    def test_recent_readings(self):
        """Test recent readings functionality."""
        # Create a reading
        spread = self.manager.create_spread_from_template('three_card', self.deck)
        reading = spread.draw_cards()
        
        # Add to recent readings
        self.manager.add_recent_reading(reading)
        
        assert len(self.manager.recent_readings) == 1
        
        # Get recent readings
        recent = self.manager.get_recent_readings(5)
        assert len(recent) == 1
        assert recent[0].spread_id == reading.spread_id
    
    def test_get_spread_statistics(self):
        """Test getting spread statistics."""
        stats = self.manager.get_spread_statistics()
        
        assert 'total_spreads' in stats
        assert 'template_spreads' in stats
        assert 'custom_spreads' in stats
        assert 'categories' in stats
        assert 'difficulties' in stats
        assert 'average_card_count' in stats
        assert 'recent_readings_count' in stats
        
        assert stats['template_spreads'] > 0
        assert stats['custom_spreads'] == 0
        assert stats['total_spreads'] > 0
    
    def test_search_spreads(self):
        """Test searching spreads."""
        # Search for "three"
        results = self.manager.search_spreads("three")
        assert len(results) > 0
        
        # Check that results contain "three" in name or description
        for result in results:
            assert ("three" in result['name'].lower() or 
                   "three" in result['description'].lower())
        
        # Search for non-existent term
        results = self.manager.search_spreads("nonexistent")
        assert len(results) == 0


class TestSpreadIntegration:
    """Integration tests for the spreads module."""
    
    def test_complete_spread_workflow(self):
        """Test complete spread workflow."""
        # Create manager and deck
        manager = SpreadManager()
        deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
        deck.shuffle(seed=123)
        
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
    
    def test_custom_spread_workflow(self):
        """Test custom spread workflow."""
        manager = SpreadManager()
        deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
        deck.shuffle(seed=456)
        
        # Create custom spread
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
            'custom_workflow',
            'Custom Workflow Spread',
            'A spread for testing workflow',
            positions,
            category='test',
            difficulty='beginner'
        )
        
        # Create spread from custom layout
        spread = TarotSpread(layout, deck, 'Test custom spread')
        
        # Draw cards
        reading = spread.draw_cards()
        
        # Verify
        assert len(reading.cards) == 2
        assert reading.layout.id == 'custom_workflow'
        
        # Get meanings
        meanings = spread.get_all_meanings()
        assert len(meanings) == 2
        assert 'situation' in meanings
        assert 'advice' in meanings


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])