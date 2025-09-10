"""
Tests for the card influence engine.
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tarot_studio.core.influence_engine import InfluenceEngine, CardPosition, create_test_spread

class TestInfluenceEngine:
    """Test cases for the influence engine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = InfluenceEngine()
    
    def test_engine_initialization(self):
        """Test that the engine initializes correctly."""
        assert self.engine.major_arcana_multiplier == 1.5
        assert self.engine.max_polarity_range == 2.0
        assert self.engine.min_polarity_range == -2.0
    
    def test_compute_influenced_meanings(self):
        """Test computing influenced meanings for a spread."""
        spread_positions, spread_layout = create_test_spread()
        
        influenced_cards = self.engine.compute_influenced_meanings(spread_positions, spread_layout)
        
        assert len(influenced_cards) == 3
        assert all(card.card_id for card in influenced_cards)
        assert all(card.polarity_score is not None for card in influenced_cards)
        assert all(card.influence_factors is not None for card in influenced_cards)
    
    def test_major_arcana_influence(self):
        """Test that Major Arcana cards have stronger influence."""
        # Create a spread with The Sun (Major Arcana) and minor cards
        the_sun_data = {
            'id': 'the_sun',
            'arcana': 'major',
            'polarity': 1.0,
            'intensity': 0.9,
            'upright_meaning': 'Joy, success, and vitality',
            'reversed_meaning': 'Temporary setbacks',
            'influence_rules': {
                'adjacency_bonus': 0.6,
                'major_arcana_multiplier': 1.5,
                'themes': ['joy', 'success', 'vitality']
            }
        }
        
        three_cups_data = {
            'id': 'three_of_cups',
            'arcana': 'minor',
            'suit': 'cups',
            'polarity': 0.8,
            'intensity': 0.6,
            'upright_meaning': 'Celebration, friendship, and joy',
            'reversed_meaning': 'Isolation, exclusion',
            'influence_rules': {
                'adjacency_bonus': 0.3,
                'suit_interaction': {'cups': 0.2, 'swords': -0.1, 'pentacles': 0.3, 'wands': 0.0},
                'themes': ['celebration', 'friendship', 'joy']
            }
        }
        
        spread_positions = [
            CardPosition('the_sun', 'present', 'upright', the_sun_data),
            CardPosition('three_of_cups', 'past', 'upright', three_cups_data)
        ]
        
        spread_layout = {
            'positions': [
                {'name': 'past', 'description': 'What has influenced your current situation'},
                {'name': 'present', 'description': 'Your current circumstances'}
            ]
        }
        
        influenced_cards = self.engine.compute_influenced_meanings(spread_positions, spread_layout)
        
        # The Sun should influence the Three of Cups
        three_cups_card = next(card for card in influenced_cards if card.card_id == 'three_of_cups')
        assert len(three_cups_card.influence_factors) > 0
        
        # Check that The Sun is listed as an influence factor
        sun_influence = next(
            (factor for factor in three_cups_card.influence_factors if factor.source_card == 'the_sun'),
            None
        )
        assert sun_influence is not None
        assert sun_influence.influence_type == 'major_arcana'
    
    def test_suit_interaction(self):
        """Test suit interaction between cards."""
        # Create cards of different suits
        ace_wands_data = {
            'id': 'ace_of_wands',
            'arcana': 'minor',
            'suit': 'wands',
            'polarity': 0.8,
            'intensity': 0.7,
            'upright_meaning': 'New inspiration and creative energy',
            'reversed_meaning': 'Blocked creativity',
            'influence_rules': {
                'adjacency_bonus': 0.2,
                'suit_interaction': {'cups': 0.1, 'swords': -0.1, 'pentacles': 0.0, 'wands': 0.0},
                'themes': ['inspiration', 'creativity', 'new_beginnings']
            }
        }
        
        three_cups_data = {
            'id': 'three_of_cups',
            'arcana': 'minor',
            'suit': 'cups',
            'polarity': 0.8,
            'intensity': 0.6,
            'upright_meaning': 'Celebration, friendship, and joy',
            'reversed_meaning': 'Isolation, exclusion',
            'influence_rules': {
                'adjacency_bonus': 0.3,
                'suit_interaction': {'cups': 0.2, 'swords': -0.1, 'pentacles': 0.3, 'wands': 0.0},
                'themes': ['celebration', 'friendship', 'joy']
            }
        }
        
        spread_positions = [
            CardPosition('ace_of_wands', 'present', 'upright', ace_wands_data),
            CardPosition('three_of_cups', 'past', 'upright', three_cups_data)
        ]
        
        spread_layout = {
            'positions': [
                {'name': 'past', 'description': 'What has influenced your current situation'},
                {'name': 'present', 'description': 'Your current circumstances'}
            ]
        }
        
        influenced_cards = self.engine.compute_influenced_meanings(spread_positions, spread_layout)
        
        # Check for suit interaction
        ace_wands_card = next(card for card in influenced_cards if card.card_id == 'ace_of_wands')
        suit_influence = next(
            (factor for factor in ace_wands_card.influence_factors if factor.influence_type == 'suit_interaction'),
            None
        )
        assert suit_influence is not None
    
    def test_reversed_card_polarity(self):
        """Test that reversed cards have reduced polarity."""
        card_data = {
            'id': 'the_sun',
            'arcana': 'major',
            'polarity': 1.0,
            'intensity': 0.9,
            'upright_meaning': 'Joy, success, and vitality',
            'reversed_meaning': 'Temporary setbacks',
            'influence_rules': {
                'adjacency_bonus': 0.6,
                'major_arcana_multiplier': 1.5,
                'themes': ['joy', 'success', 'vitality']
            }
        }
        
        # Test upright card
        upright_position = CardPosition('the_sun', 'present', 'upright', card_data)
        upright_polarity = self.engine._calculate_polarity_score(upright_position, [])
        
        # Test reversed card
        reversed_position = CardPosition('the_sun', 'present', 'reversed', card_data)
        reversed_polarity = self.engine._calculate_polarity_score(reversed_position, [])
        
        # Reversed card should have lower polarity
        assert reversed_polarity < upright_polarity
        assert reversed_polarity < 0  # Should be negative for reversed Sun
    
    def test_polarity_clamping(self):
        """Test that polarity scores are clamped to valid range."""
        # Create a card with extreme polarity
        extreme_card_data = {
            'id': 'extreme_card',
            'arcana': 'major',
            'polarity': 5.0,  # Very high polarity
            'intensity': 1.0,
            'upright_meaning': 'Extreme positive energy',
            'reversed_meaning': 'Extreme negative energy',
            'influence_rules': {
                'adjacency_bonus': 0.0,
                'major_arcana_multiplier': 1.5,
                'themes': ['extreme']
            }
        }
        
        position = CardPosition('extreme_card', 'present', 'upright', extreme_card_data)
        polarity = self.engine._calculate_polarity_score(position, [])
        
        # Polarity should be clamped to max range
        assert polarity <= self.engine.max_polarity_range
        assert polarity >= self.engine.min_polarity_range
    
    def test_influence_factor_explanation(self):
        """Test that influence factors have meaningful explanations."""
        spread_positions, spread_layout = create_test_spread()
        
        influenced_cards = self.engine.compute_influenced_meanings(spread_positions, spread_layout)
        
        for card in influenced_cards:
            for factor in card.influence_factors:
                assert factor.explanation is not None
                assert len(factor.explanation) > 0
                assert factor.source_card is not None
                assert factor.influence_type is not None
    
    def test_journal_prompt_generation(self):
        """Test that journal prompts are generated for each card."""
        spread_positions, spread_layout = create_test_spread()
        
        influenced_cards = self.engine.compute_influenced_meanings(spread_positions, spread_layout)
        
        for card in influenced_cards:
            assert card.journal_prompt is not None
            assert len(card.journal_prompt) > 0
            assert card.card_id in card.journal_prompt.lower()

if __name__ == "__main__":
    pytest.main([__file__])