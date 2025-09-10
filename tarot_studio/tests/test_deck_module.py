"""
Unit tests for the Tarot Deck Module.

This module contains comprehensive tests for the Card and Deck classes,
including all functionality and edge cases.
"""

import pytest
import json
import tempfile
import os
from typing import Dict, Any, List
from tarot_studio.deck.card import Card, CardMetadata, Orientation, Arcana, Suit, Element
from tarot_studio.deck.deck import Deck


class TestCard:
    """Test suite for the Card class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.major_card_data = {
            'id': 'the_sun',
            'name': 'The Sun',
            'arcana': 'major',
            'element': 'fire',
            'keywords': ['joy', 'success', 'vitality'],
            'upright_meaning': 'The Sun represents joy, success, and vitality.',
            'reversed_meaning': 'Reversed, The Sun suggests temporary setbacks.'
        }
        
        self.minor_card_data = {
            'id': 'ace_of_wands',
            'name': 'Ace of Wands',
            'arcana': 'minor',
            'suit': 'wands',
            'number': 1,
            'element': 'fire',
            'keywords': ['inspiration', 'creativity'],
            'upright_meaning': 'The Ace of Wands represents new inspiration.',
            'reversed_meaning': 'Reversed, the Ace of Wands suggests blocked creativity.'
        }
    
    def test_card_creation_from_data(self):
        """Test creating a card from dictionary data."""
        # Test Major Arcana card
        card = Card.from_data(self.major_card_data)
        assert card.id == 'the_sun'
        assert card.name == 'The Sun'
        assert card.arcana == Arcana.MAJOR
        assert card.element == Element.FIRE
        assert card.keywords == ['joy', 'success', 'vitality']
        assert card.suit is None
        assert card.number is None
        
        # Test Minor Arcana card
        card = Card.from_data(self.minor_card_data)
        assert card.id == 'ace_of_wands'
        assert card.name == 'Ace of Wands'
        assert card.arcana == Arcana.MINOR
        assert card.suit == Suit.WANDS
        assert card.number == 1
        assert card.element == Element.FIRE
    
    def test_card_creation_missing_fields(self):
        """Test card creation with missing required fields."""
        # Missing id
        data = self.major_card_data.copy()
        del data['id']
        with pytest.raises(ValueError, match="Missing required field: id"):
            Card.from_data(data)
        
        # Missing name
        data = self.major_card_data.copy()
        del data['name']
        with pytest.raises(ValueError, match="Missing required field: name"):
            Card.from_data(data)
        
        # Missing upright_meaning
        data = self.major_card_data.copy()
        del data['upright_meaning']
        with pytest.raises(ValueError, match="Missing required field: upright_meaning"):
            Card.from_data(data)
        
        # Missing reversed_meaning
        data = self.major_card_data.copy()
        del data['reversed_meaning']
        with pytest.raises(ValueError, match="Missing required field: reversed_meaning"):
            Card.from_data(data)
    
    def test_card_creation_invalid_suit(self):
        """Test card creation with invalid suit."""
        data = self.minor_card_data.copy()
        data['suit'] = 'invalid_suit'
        with pytest.raises(ValueError, match="Invalid suit: invalid_suit"):
            Card.from_data(data)
    
    def test_card_creation_invalid_element(self):
        """Test card creation with invalid element."""
        data = self.major_card_data.copy()
        data['element'] = 'invalid_element'
        with pytest.raises(ValueError, match="Invalid element: invalid_element"):
            Card.from_data(data)
    
    def test_card_orientation(self):
        """Test card orientation functionality."""
        card = Card.from_data(self.major_card_data)
        
        # Default orientation should be upright
        assert card.orientation == Orientation.UPRIGHT
        assert card.is_upright()
        assert not card.is_reversed()
        
        # Test flipping
        card.flip()
        assert card.orientation == Orientation.REVERSED
        assert not card.is_upright()
        assert card.is_reversed()
        
        # Test setting orientation
        card.set_orientation(Orientation.UPRIGHT)
        assert card.orientation == Orientation.UPRIGHT
        assert card.is_upright()
    
    def test_card_meaning(self):
        """Test getting card meanings."""
        card = Card.from_data(self.major_card_data)
        
        # Test upright meaning
        assert card.get_meaning() == self.major_card_data['upright_meaning']
        
        # Test reversed meaning
        card.flip()
        assert card.get_meaning() == self.major_card_data['reversed_meaning']
    
    def test_card_arcana_checks(self):
        """Test Major/Minor Arcana checks."""
        major_card = Card.from_data(self.major_card_data)
        minor_card = Card.from_data(self.minor_card_data)
        
        assert major_card.is_major_arcana()
        assert not major_card.is_minor_arcana()
        
        assert minor_card.is_minor_arcana()
        assert not minor_card.is_major_arcana()
    
    def test_card_keyword_functionality(self):
        """Test keyword-related functionality."""
        card = Card.from_data(self.major_card_data)
        
        # Test has_keyword
        assert card.has_keyword('joy')
        assert card.has_keyword('JOY')  # Case insensitive
        assert not card.has_keyword('love')
        
        # Test keywords property
        assert card.keywords == ['joy', 'success', 'vitality']
        # Ensure it returns a copy
        keywords = card.keywords
        keywords.append('test')
        assert card.keywords == ['joy', 'success', 'vitality']
    
    def test_card_display_name(self):
        """Test card display name functionality."""
        card = Card.from_data(self.major_card_data)
        
        # Test upright display name
        assert card.get_display_name() == 'The Sun'
        
        # Test reversed display name
        card.flip()
        assert card.get_display_name() == 'The Sun (Reversed)'
    
    def test_card_to_dict(self):
        """Test converting card to dictionary."""
        card = Card.from_data(self.major_card_data)
        card_dict = card.to_dict()
        
        assert card_dict['id'] == 'the_sun'
        assert card_dict['name'] == 'The Sun'
        assert card_dict['arcana'] == 'major'
        assert card_dict['element'] == 'fire'
        assert card_dict['keywords'] == ['joy', 'success', 'vitality']
        assert card_dict['orientation'] == 'upright'
        assert card_dict['current_meaning'] == self.major_card_data['upright_meaning']
    
    def test_card_equality(self):
        """Test card equality."""
        card1 = Card.from_data(self.major_card_data)
        card2 = Card.from_data(self.major_card_data)
        card3 = Card.from_data(self.minor_card_data)
        
        # Same card, same orientation
        assert card1 == card2
        
        # Same card, different orientation
        card2.flip()
        assert card1 != card2
        
        # Different cards
        assert card1 != card3
    
    def test_card_hash(self):
        """Test card hashing."""
        card1 = Card.from_data(self.major_card_data)
        card2 = Card.from_data(self.major_card_data)
        card3 = Card.from_data(self.major_card_data)
        card3.flip()
        
        # Same card, same orientation should have same hash
        assert hash(card1) == hash(card2)
        
        # Same card, different orientation should have different hash
        assert hash(card1) != hash(card3)
    
    def test_card_string_representations(self):
        """Test card string representations."""
        card = Card.from_data(self.major_card_data)
        
        # Test __str__
        assert str(card) == 'The Sun'
        
        # Test __repr__
        repr_str = repr(card)
        assert 'Card' in repr_str
        assert 'the_sun' in repr_str
        assert 'upright' in repr_str


class TestDeck:
    """Test suite for the Deck class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a minimal test deck data
        self.test_deck_data = {
            'deck_info': {
                'name': 'Test Deck',
                'total_cards': 4
            },
            'major_arcana': [
                {
                    'id': 'the_sun',
                    'name': 'The Sun',
                    'element': 'fire',
                    'keywords': ['joy', 'success'],
                    'upright_meaning': 'The Sun represents joy and success.',
                    'reversed_meaning': 'Reversed, The Sun suggests setbacks.'
                },
                {
                    'id': 'the_moon',
                    'name': 'The Moon',
                    'element': 'water',
                    'keywords': ['intuition', 'mystery'],
                    'upright_meaning': 'The Moon represents intuition and mystery.',
                    'reversed_meaning': 'Reversed, The Moon suggests confusion.'
                }
            ],
            'minor_arcana': {
                'wands': {
                    'element': 'fire',
                    'ace': {
                        'keywords': ['inspiration'],
                        'upright_meaning': 'The Ace of Wands represents inspiration.',
                        'reversed_meaning': 'Reversed, the Ace of Wands suggests blocked creativity.'
                    },
                    'two': {
                        'keywords': ['planning'],
                        'upright_meaning': 'The Two of Wands represents planning.',
                        'reversed_meaning': 'Reversed, the Two of Wands suggests lack of planning.'
                    }
                }
            }
        }
    
    def test_deck_creation_from_data(self):
        """Test creating a deck from dictionary data."""
        deck = Deck.from_data(self.test_deck_data)
        
        assert len(deck) == 4
        assert deck.count_remaining() == 4
        assert deck.count_drawn() == 0
        assert not deck.is_empty()
        assert not deck.is_shuffled
    
    def test_deck_creation_from_file(self):
        """Test creating a deck from a JSON file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_deck_data, f)
            temp_file = f.name
        
        try:
            deck = Deck.load_from_file(temp_file)
            assert len(deck) == 4
            assert deck.count_remaining() == 4
        finally:
            os.unlink(temp_file)
    
    def test_deck_creation_file_not_found(self):
        """Test creating a deck from non-existent file."""
        with pytest.raises(FileNotFoundError):
            Deck.load_from_file('non_existent_file.json')
    
    def test_deck_creation_invalid_json(self):
        """Test creating a deck from invalid JSON file."""
        # Create a temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('invalid json content')
            temp_file = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                Deck.load_from_file(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_deck_shuffling(self):
        """Test deck shuffling functionality."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Test shuffling with seed
        deck.shuffle(seed=42)
        assert deck.is_shuffled
        
        # Test shuffling without seed
        deck.reset()
        deck.shuffle()
        assert deck.is_shuffled
    
    def test_deck_drawing_single_card(self):
        """Test drawing a single card."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Draw card with random orientation
        card = deck.draw_card()
        assert isinstance(card, Card)
        assert len(deck) == 3
        assert deck.count_drawn() == 1
        
        # Draw card with specific orientation
        card = deck.draw_card(Orientation.REVERSED)
        assert card.orientation == Orientation.REVERSED
        assert len(deck) == 2
        assert deck.count_drawn() == 2
    
    def test_deck_drawing_multiple_cards(self):
        """Test drawing multiple cards."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Draw multiple cards
        cards = deck.draw_cards(2)
        assert len(cards) == 2
        assert len(deck) == 2
        assert deck.count_drawn() == 2
        
        # Draw cards with specific orientations
        deck.reset()
        orientations = [Orientation.UPRIGHT, Orientation.REVERSED]
        cards = deck.draw_cards(2, orientations)
        assert cards[0].orientation == Orientation.UPRIGHT
        assert cards[1].orientation == Orientation.REVERSED
    
    def test_deck_drawing_errors(self):
        """Test drawing errors."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Draw all cards
        deck.draw_cards(4)
        
        # Try to draw from empty deck
        with pytest.raises(ValueError, match="Cannot draw from an empty deck"):
            deck.draw_card()
        
        # Try to draw more cards than available
        deck.reset()
        with pytest.raises(ValueError, match="Cannot draw 5 cards from deck with 4 cards"):
            deck.draw_cards(5)
        
        # Try to draw with invalid orientations list
        with pytest.raises(ValueError, match="Orientations list must have 2 elements"):
            deck.draw_cards(2, [Orientation.UPRIGHT])
    
    def test_deck_reset(self):
        """Test deck reset functionality."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Draw some cards
        deck.draw_cards(2)
        assert len(deck) == 2
        assert deck.count_drawn() == 2
        
        # Reset deck
        deck.reset()
        assert len(deck) == 4
        assert deck.count_drawn() == 0
        assert not deck.is_shuffled
    
    def test_deck_card_search(self):
        """Test card search functionality."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Test get_card_by_id
        card = deck.get_card_by_id('the_sun')
        assert card is not None
        assert card.name == 'The Sun'
        
        # Test get_card_by_name
        card = deck.get_card_by_name('The Sun')
        assert card is not None
        assert card.id == 'the_sun'
        
        # Test case insensitive search
        card = deck.get_card_by_name('the sun')
        assert card is not None
        assert card.id == 'the_sun'
        
        # Test non-existent card
        card = deck.get_card_by_id('non_existent')
        assert card is None
        
        card = deck.get_card_by_name('Non Existent')
        assert card is None
    
    def test_deck_filtering(self):
        """Test deck filtering functionality."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Test get_major_arcana
        major_cards = deck.get_major_arcana()
        assert len(major_cards) == 2
        assert all(card.is_major_arcana() for card in major_cards)
        
        # Test get_minor_arcana
        minor_cards = deck.get_minor_arcana()
        assert len(minor_cards) == 2
        assert all(card.is_minor_arcana() for card in minor_cards)
        
        # Test get_cards_by_suit
        wands_cards = deck.get_cards_by_suit(Suit.WANDS)
        assert len(wands_cards) == 2
        assert all(card.suit == Suit.WANDS for card in wands_cards)
        
        # Test get_cards_by_element
        fire_cards = deck.get_cards_by_element(Element.FIRE)
        assert len(fire_cards) == 3  # The Sun + 2 Wands cards
        
        water_cards = deck.get_cards_by_element(Element.WATER)
        assert len(water_cards) == 1  # The Moon
        
        # Test get_cards_with_keyword
        joy_cards = deck.get_cards_with_keyword('joy')
        assert len(joy_cards) == 1
        assert joy_cards[0].id == 'the_sun'
    
    def test_deck_info(self):
        """Test deck information functionality."""
        deck = Deck.from_data(self.test_deck_data)
        
        info = deck.get_deck_info()
        assert info['total_cards'] == 4
        assert info['drawn_cards'] == 0
        assert info['major_arcana'] == 2
        assert info['minor_arcana'] == 2
        assert info['suit_counts']['wands'] == 2
        assert info['element_counts']['fire'] == 3
        assert info['element_counts']['water'] == 1
        assert not info['is_shuffled']
        assert not info['is_empty']
    
    def test_deck_to_dict(self):
        """Test converting deck to dictionary."""
        deck = Deck.from_data(self.test_deck_data)
        
        deck_dict = deck.to_dict()
        assert 'remaining_cards' in deck_dict
        assert 'drawn_cards' in deck_dict
        assert 'deck_info' in deck_dict
        
        assert len(deck_dict['remaining_cards']) == 4
        assert len(deck_dict['drawn_cards']) == 0
    
    def test_deck_string_representations(self):
        """Test deck string representations."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Test __str__
        str_repr = str(deck)
        assert 'Deck' in str_repr
        assert '4 cards remaining' in str_repr
        assert '0 drawn' in str_repr
        
        # Test __repr__
        repr_str = repr(deck)
        assert 'Deck' in repr_str
        assert 'cards=4' in repr_str
        assert 'drawn=0' in repr_str
        assert 'shuffled=False' in repr_str
    
    def test_deck_length(self):
        """Test deck length functionality."""
        deck = Deck.from_data(self.test_deck_data)
        
        assert len(deck) == 4
        
        deck.draw_card()
        assert len(deck) == 3
        
        deck.reset()
        assert len(deck) == 4


class TestDeckIntegration:
    """Integration tests for the deck module."""
    
    def test_full_deck_loading(self):
        """Test loading a full 78-card deck."""
        # This would test with the actual card_data.json file
        # For now, we'll create a minimal test
        deck = Deck.from_data({
            'major_arcana': [],
            'minor_arcana': {}
        })
        
        # Should create empty deck
        assert len(deck) == 0
    
    def test_deck_workflow(self):
        """Test complete deck workflow."""
        deck = Deck.from_data(self.test_deck_data)
        
        # Shuffle deck
        deck.shuffle(seed=123)
        assert deck.is_shuffled
        
        # Draw cards for a reading
        cards = deck.draw_cards(3, [
            Orientation.UPRIGHT,
            Orientation.REVERSED,
            Orientation.UPRIGHT
        ])
        
        assert len(cards) == 3
        assert cards[0].is_upright()
        assert cards[1].is_reversed()
        assert cards[2].is_upright()
        
        # Check deck state
        assert len(deck) == 1
        assert deck.count_drawn() == 3
        
        # Reset for next reading
        deck.reset()
        assert len(deck) == 4
        assert deck.count_drawn() == 0
        assert not deck.is_shuffled


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])