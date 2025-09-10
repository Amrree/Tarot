"""
Integration tests for tarot spreads using the Enhanced Influence Engine.

This module tests complete spread processing with realistic card combinations.
"""

import pytest
import json
from typing import Dict, Any
from tarot_studio.core.enhanced_influence_engine import EnhancedInfluenceEngine, EngineConfig

class TestSpreadIntegration:
    """Integration tests for tarot spreads."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = EngineConfig()
        self.engine = EnhancedInfluenceEngine(self.config)
        
        # Create comprehensive card database
        self.card_database = self._create_comprehensive_card_database()
    
    def _create_comprehensive_card_database(self) -> Dict[str, Dict[str, Any]]:
        """Create a comprehensive card database for testing."""
        return {
            # Major Arcana
            "the_fool": {
                "card_id": "the_fool", "name": "The Fool", "arcana": "major", "element": "air",
                "polarity": 0.2, "intensity": 0.7, "keywords": ["new_beginnings", "innocence", "free_spirit"],
                "themes": {"new_beginnings": 0.9, "innocence": 0.8, "freedom": 0.7},
                "upright_meaning": "The Fool represents new beginnings, innocence, and a free spirit.",
                "reversed_meaning": "Reversed, The Fool suggests recklessness or being held back."
            },
            "the_magician": {
                "card_id": "the_magician", "name": "The Magician", "arcana": "major", "element": "fire",
                "polarity": 0.8, "intensity": 0.8, "keywords": ["manifestation", "power", "skill"],
                "themes": {"manifestation": 0.9, "power": 0.8, "skill": 0.7},
                "upright_meaning": "The Magician represents the power of manifestation and skill.",
                "reversed_meaning": "Reversed, The Magician suggests manipulation or lack of skill."
            },
            "the_sun": {
                "card_id": "the_sun", "name": "The Sun", "arcana": "major", "element": "fire",
                "polarity": 1.0, "intensity": 0.9, "keywords": ["joy", "success", "vitality"],
                "themes": {"joy": 0.9, "success": 0.8, "vitality": 0.7},
                "upright_meaning": "The Sun represents joy, success, and vitality.",
                "reversed_meaning": "Reversed, The Sun suggests temporary setbacks."
            },
            "the_tower": {
                "card_id": "the_tower", "name": "The Tower", "arcana": "major", "element": "fire",
                "polarity": -0.8, "intensity": 0.9, "keywords": ["sudden_change", "disruption", "awakening"],
                "themes": {"sudden_change": 0.9, "disruption": 0.8, "awakening": 0.7},
                "upright_meaning": "The Tower represents sudden change and disruption.",
                "reversed_meaning": "Reversed, The Tower suggests avoiding necessary change."
            },
            "the_star": {
                "card_id": "the_star", "name": "The Star", "arcana": "major", "element": "air",
                "polarity": 0.7, "intensity": 0.8, "keywords": ["hope", "inspiration", "guidance"],
                "themes": {"hope": 0.9, "inspiration": 0.8, "guidance": 0.7},
                "upright_meaning": "The Star represents hope, inspiration, and guidance.",
                "reversed_meaning": "Reversed, The Star suggests despair or lack of hope."
            },
            "the_moon": {
                "card_id": "the_moon", "name": "The Moon", "arcana": "major", "element": "water",
                "polarity": -0.3, "intensity": 0.7, "keywords": ["illusion", "intuition", "mystery"],
                "themes": {"illusion": 0.8, "intuition": 0.7, "mystery": 0.6},
                "upright_meaning": "The Moon represents intuition and mystery.",
                "reversed_meaning": "Reversed, The Moon suggests confusion."
            },
            "temperance": {
                "card_id": "temperance", "name": "Temperance", "arcana": "major", "element": "earth",
                "polarity": 0.6, "intensity": 0.7, "keywords": ["balance", "moderation", "patience"],
                "themes": {"balance": 0.9, "moderation": 0.8, "patience": 0.7},
                "upright_meaning": "Temperance represents balance, moderation, and patience.",
                "reversed_meaning": "Reversed, Temperance suggests imbalance or impatience."
            },
            "the_world": {
                "card_id": "the_world", "name": "The World", "arcana": "major", "element": "earth",
                "polarity": 0.9, "intensity": 0.8, "keywords": ["completion", "achievement", "fulfillment"],
                "themes": {"completion": 0.9, "achievement": 0.8, "fulfillment": 0.7},
                "upright_meaning": "The World represents completion, achievement, and fulfillment.",
                "reversed_meaning": "Reversed, The World suggests incomplete projects."
            },
            
            # Minor Arcana - Wands
            "ace_of_wands": {
                "card_id": "ace_of_wands", "name": "Ace of Wands", "arcana": "minor", "suit": "wands", "number": 1, "element": "fire",
                "polarity": 0.8, "intensity": 0.7, "keywords": ["inspiration", "creativity", "new_beginnings"],
                "themes": {"inspiration": 0.9, "creativity": 0.8, "new_beginnings": 0.7},
                "upright_meaning": "The Ace of Wands represents new inspiration and creative energy.",
                "reversed_meaning": "Reversed, the Ace of Wands suggests blocked creativity."
            },
            "two_of_wands": {
                "card_id": "two_of_wands", "name": "Two of Wands", "arcana": "minor", "suit": "wands", "number": 2, "element": "fire",
                "polarity": 0.6, "intensity": 0.6, "keywords": ["planning", "future", "personal_power"],
                "themes": {"planning": 0.8, "future": 0.7, "personal_power": 0.6},
                "upright_meaning": "The Two of Wands represents planning and future vision.",
                "reversed_meaning": "Reversed, the Two of Wands suggests lack of planning."
            },
            "three_of_wands": {
                "card_id": "three_of_wands", "name": "Three of Wands", "arcana": "minor", "suit": "wands", "number": 3, "element": "fire",
                "polarity": 0.7, "intensity": 0.6, "keywords": ["expansion", "foresight", "leadership"],
                "themes": {"expansion": 0.8, "foresight": 0.7, "leadership": 0.6},
                "upright_meaning": "The Three of Wands represents expansion and foresight.",
                "reversed_meaning": "Reversed, the Three of Wands suggests lack of expansion."
            },
            "five_of_wands": {
                "card_id": "five_of_wands", "name": "Five of Wands", "arcana": "minor", "suit": "wands", "number": 5, "element": "fire",
                "polarity": -0.4, "intensity": 0.7, "keywords": ["conflict", "competition", "struggle"],
                "themes": {"conflict": 0.8, "competition": 0.7, "struggle": 0.6},
                "upright_meaning": "The Five of Wands represents conflict and competition.",
                "reversed_meaning": "Reversed, the Five of Wands suggests avoiding conflict."
            },
            
            # Minor Arcana - Cups
            "ace_of_cups": {
                "card_id": "ace_of_cups", "name": "Ace of Cups", "arcana": "minor", "suit": "cups", "number": 1, "element": "water",
                "polarity": 0.8, "intensity": 0.6, "keywords": ["love", "emotions", "spirituality"],
                "themes": {"love": 0.9, "emotions": 0.8, "spirituality": 0.7},
                "upright_meaning": "The Ace of Cups represents new love and emotions.",
                "reversed_meaning": "Reversed, the Ace of Cups suggests blocked emotions."
            },
            "three_of_cups": {
                "card_id": "three_of_cups", "name": "Three of Cups", "arcana": "minor", "suit": "cups", "number": 3, "element": "water",
                "polarity": 0.8, "intensity": 0.6, "keywords": ["celebration", "friendship", "joy"],
                "themes": {"celebration": 0.9, "friendship": 0.8, "joy": 0.7},
                "upright_meaning": "The Three of Cups represents celebration and friendship.",
                "reversed_meaning": "Reversed, the Three of Cups suggests isolation."
            },
            "five_of_cups": {
                "card_id": "five_of_cups", "name": "Five of Cups", "arcana": "minor", "suit": "cups", "number": 5, "element": "water",
                "polarity": -0.6, "intensity": 0.7, "keywords": ["loss", "disappointment", "grief"],
                "themes": {"loss": 0.8, "disappointment": 0.7, "grief": 0.6},
                "upright_meaning": "The Five of Cups represents loss and disappointment.",
                "reversed_meaning": "Reversed, the Five of Cups suggests moving past loss."
            },
            
            # Minor Arcana - Swords
            "ace_of_swords": {
                "card_id": "ace_of_swords", "name": "Ace of Swords", "arcana": "minor", "suit": "swords", "number": 1, "element": "air",
                "polarity": 0.7, "intensity": 0.8, "keywords": ["clarity", "truth", "justice"],
                "themes": {"clarity": 0.9, "truth": 0.8, "justice": 0.7},
                "upright_meaning": "The Ace of Swords represents clarity and truth.",
                "reversed_meaning": "Reversed, the Ace of Swords suggests confusion."
            },
            "five_of_swords": {
                "card_id": "five_of_swords", "name": "Five of Swords", "arcana": "minor", "suit": "swords", "number": 5, "element": "air",
                "polarity": -0.6, "intensity": 0.7, "keywords": ["conflict", "defeat", "betrayal"],
                "themes": {"conflict": 0.8, "defeat": 0.7, "betrayal": 0.6},
                "upright_meaning": "The Five of Swords represents conflict and defeat.",
                "reversed_meaning": "Reversed, the Five of Swords suggests avoiding conflict."
            },
            
            # Minor Arcana - Pentacles
            "ace_of_pentacles": {
                "card_id": "ace_of_pentacles", "name": "Ace of Pentacles", "arcana": "minor", "suit": "pentacles", "number": 1, "element": "earth",
                "polarity": 0.7, "intensity": 0.6, "keywords": ["opportunity", "prosperity", "new_beginning"],
                "themes": {"opportunity": 0.9, "prosperity": 0.8, "new_beginning": 0.7},
                "upright_meaning": "The Ace of Pentacles represents new opportunities and prosperity.",
                "reversed_meaning": "Reversed, the Ace of Pentacles suggests missed opportunities."
            },
            "ten_of_pentacles": {
                "card_id": "ten_of_pentacles", "name": "Ten of Pentacles", "arcana": "minor", "suit": "pentacles", "number": 10, "element": "earth",
                "polarity": 0.8, "intensity": 0.7, "keywords": ["wealth", "family", "legacy"],
                "themes": {"wealth": 0.9, "family": 0.8, "legacy": 0.7},
                "upright_meaning": "The Ten of Pentacles represents wealth, family, and legacy.",
                "reversed_meaning": "Reversed, the Ten of Pentacles suggests financial instability."
            }
        }
    
    def test_three_card_triad_positive_flow(self):
        """Test three-card triad with positive flow."""
        spread_data = {
            "reading_id": "triad_positive_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "present", "card_id": "two_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "three_of_wands", "orientation": "upright"}
            ],
            "user_context": "What is my creative journey?"
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Validate result structure
        assert result["reading_id"] == "triad_positive_001"
        assert len(result["cards"]) == 3
        
        # Check that the center card (present) is influenced by both neighbors
        present_card = next(card for card in result["cards"] if card["position"] == "present")
        assert len(present_card["influence_factors"]) >= 2  # Should be influenced by past and future
        
        # Check for numerical sequence detection
        assert "continuity" in present_card["themes"] or any("continuity" in card["themes"] for card in result["cards"])
        
        # Validate influence factors
        for card in result["cards"]:
            for factor in card["influence_factors"]:
                assert factor["source_position"] in ["past", "present", "future"]
                assert factor["source_card_id"] in self.card_database
                assert factor["effect"] != ""
                assert factor["explain"] != ""
    
    def test_three_card_triad_major_dominance(self):
        """Test three-card triad with Major Arcana dominance."""
        spread_data = {
            "reading_id": "triad_major_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "present", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "two_of_wands", "orientation": "upright"}
            ],
            "user_context": "What does my future hold?"
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Check that Major Arcana (The Sun) dominates the reading
        sun_card = next(card for card in result["cards"] if card["position"] == "past")
        assert sun_card["polarity_score"] > 0.8  # Should maintain high polarity
        
        # Check that Minor Arcana cards are influenced by Major Arcana
        ace_card = next(card for card in result["cards"] if card["position"] == "present")
        two_card = next(card for card in result["cards"] if card["position"] == "future")
        
        # Both should have influence factors from The Sun
        ace_influences = [f for f in ace_card["influence_factors"] if f["source_card_id"] == "the_sun"]
        two_influences = [f for f in two_card["influence_factors"] if f["source_card_id"] == "the_sun"]
        
        assert len(ace_influences) > 0
        assert len(two_influences) > 0
    
    def test_three_card_triad_elemental_conflict(self):
        """Test three-card triad with elemental conflict."""
        spread_data = {
            "reading_id": "triad_elemental_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "ace_of_wands", "orientation": "upright"},  # Fire
                {"position_id": "present", "card_id": "ace_of_cups", "orientation": "upright"},  # Water
                {"position_id": "future", "card_id": "ace_of_swords", "orientation": "upright"}  # Air
            ],
            "user_context": "What is my emotional journey?"
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Check that elemental conflicts are handled
        cups_card = next(card for card in result["cards"] if card["position"] == "present")
        
        # Should have elemental influence factors
        elemental_factors = [f for f in cups_card["influence_factors"] if "Elemental affinity" in f["explain"]]
        assert len(elemental_factors) >= 2  # Should be influenced by both Fire and Air elements
    
    def test_three_card_triad_reversal_propagation(self):
        """Test three-card triad with reversal propagation."""
        spread_data = {
            "reading_id": "triad_reversal_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "present", "card_id": "the_moon", "orientation": "reversed"},
                {"position_id": "future", "card_id": "the_star", "orientation": "upright"}
            ],
            "user_context": "What is my spiritual journey?"
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Check that reversal propagation affects neighboring cards
        sun_card = next(card for card in result["cards"] if card["position"] == "past")
        star_card = next(card for card in result["cards"] if card["position"] == "future")
        
        # Both should have influence factors from the reversed Moon
        sun_influences = [f for f in sun_card["influence_factors"] if f["source_card_id"] == "the_moon"]
        star_influences = [f for f in star_card["influence_factors"] if f["source_card_id"] == "the_moon"]
        
        assert len(sun_influences) > 0
        assert len(star_influences) > 0
        
        # Check that reversal propagation reduces intensity
        moon_card = next(card for card in result["cards"] if card["position"] == "present")
        assert moon_card["intensity_score"] < 0.7  # Should be reduced from baseline
    
    def test_celtic_cross_complex_influence(self):
        """Test Celtic Cross with complex influence patterns."""
        spread_data = {
            "reading_id": "celtic_complex_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "celtic_cross",
            "positions": [
                {"position_id": "situation", "card_id": "the_magician", "orientation": "upright"},
                {"position_id": "challenge", "card_id": "five_of_wands", "orientation": "upright"},
                {"position_id": "past", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "the_star", "orientation": "upright"},
                {"position_id": "above", "card_id": "temperance", "orientation": "upright"},
                {"position_id": "below", "card_id": "ace_of_cups", "orientation": "upright"},
                {"position_id": "advice", "card_id": "the_world", "orientation": "upright"},
                {"position_id": "external", "card_id": "ten_of_pentacles", "orientation": "upright"},
                {"position_id": "hopes_fears", "card_id": "the_tower", "orientation": "upright"},
                {"position_id": "outcome", "card_id": "three_of_cups", "orientation": "upright"}
            ],
            "user_context": "What does my future hold in my career?"
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Validate result structure
        assert result["reading_id"] == "celtic_complex_001"
        assert len(result["cards"]) == 10
        
        # Check that the situation card (center of cross) is heavily influenced
        situation_card = next(card for card in result["cards"] if card["position"] == "situation")
        assert len(situation_card["influence_factors"]) >= 4  # Should be influenced by challenge, past, future, above, below
        
        # Check that Major Arcana cards maintain dominance
        major_cards = [card for card in result["cards"] if card["card_id"] in ["the_magician", "the_star", "temperance", "the_world", "the_tower"]]
        for card in major_cards:
            assert card["polarity_score"] >= -1.0  # Should maintain reasonable polarity
            assert card["intensity_score"] >= 0.5  # Should maintain reasonable intensity
        
        # Check that the outcome card is influenced by multiple factors
        outcome_card = next(card for card in result["cards"] if card["position"] == "outcome")
        assert len(outcome_card["influence_factors"]) >= 2  # Should be influenced by advice and hopes_fears
    
    def test_celtic_cross_conflict_resolution(self):
        """Test Celtic Cross with conflict resolution."""
        spread_data = {
            "reading_id": "celtic_conflict_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "celtic_cross",
            "positions": [
                {"position_id": "situation", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "challenge", "card_id": "five_of_swords", "orientation": "upright"},
                {"position_id": "past", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "the_star", "orientation": "upright"},
                {"position_id": "above", "card_id": "temperance", "orientation": "upright"},
                {"position_id": "below", "card_id": "ace_of_cups", "orientation": "upright"},
                {"position_id": "advice", "card_id": "the_world", "orientation": "upright"},
                {"position_id": "external", "card_id": "ten_of_pentacles", "orientation": "upright"},
                {"position_id": "hopes_fears", "card_id": "five_of_cups", "orientation": "upright"},
                {"position_id": "outcome", "card_id": "three_of_cups", "orientation": "upright"}
            ],
            "user_context": "What does my future hold in my relationships?"
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Check that conflict resolution is applied
        # The Sun (positive) vs Five of Swords (negative) should trigger conflict resolution
        sun_card = next(card for card in result["cards"] if card["position"] == "situation")
        swords_card = next(card for card in result["cards"] if card["position"] == "challenge")
        
        # Both should have conflict resolution factors
        sun_conflicts = [f for f in sun_card["influence_factors"] if "Conflict resolution" in f["explain"]]
        swords_conflicts = [f for f in swords_card["influence_factors"] if "Conflict resolution" in f["explain"]]
        
        assert len(sun_conflicts) > 0 or len(swords_conflicts) > 0  # At least one should have conflict resolution
    
    def test_celtic_cross_narrative_boost(self):
        """Test Celtic Cross with narrative boost."""
        spread_data = {
            "reading_id": "celtic_narrative_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "celtic_cross",
            "positions": [
                {"position_id": "situation", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "challenge", "card_id": "two_of_wands", "orientation": "upright"},
                {"position_id": "past", "card_id": "three_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "five_of_wands", "orientation": "upright"},
                {"position_id": "above", "card_id": "ace_of_cups", "orientation": "upright"},
                {"position_id": "below", "card_id": "three_of_cups", "orientation": "upright"},
                {"position_id": "advice", "card_id": "five_of_cups", "orientation": "upright"},
                {"position_id": "external", "card_id": "ace_of_swords", "orientation": "upright"},
                {"position_id": "hopes_fears", "card_id": "five_of_swords", "orientation": "upright"},
                {"position_id": "outcome", "card_id": "ace_of_pentacles", "orientation": "upright"}
            ],
            "user_context": "What does my future hold in my creative projects?"
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Check that narrative boost is applied for shared themes
        # Multiple Wands cards should boost "creativity" theme
        wands_cards = [card for card in result["cards"] if card["card_id"].endswith("_wands")]
        
        for card in wands_cards:
            # Should have narrative boost factors
            narrative_factors = [f for f in card["influence_factors"] if "Narrative boost" in f["explain"]]
            assert len(narrative_factors) > 0  # Should have narrative boost
    
    def test_spread_performance_benchmarks(self):
        """Test that spreads meet performance benchmarks."""
        import time
        
        # Test three-card spread performance
        spread_data = {
            "reading_id": "perf_test_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "present", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "two_of_wands", "orientation": "upright"}
            ]
        }
        
        start_time = time.time()
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        end_time = time.time()
        
        processing_time = end_time - start_time
        assert processing_time < 0.1  # Should be under 100ms
        
        # Test Celtic Cross performance
        celtic_spread = {
            "reading_id": "perf_celtic_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "celtic_cross",
            "positions": [
                {"position_id": "situation", "card_id": "the_magician", "orientation": "upright"},
                {"position_id": "challenge", "card_id": "five_of_wands", "orientation": "upright"},
                {"position_id": "past", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "the_star", "orientation": "upright"},
                {"position_id": "above", "card_id": "temperance", "orientation": "upright"},
                {"position_id": "below", "card_id": "ace_of_cups", "orientation": "upright"},
                {"position_id": "advice", "card_id": "the_world", "orientation": "upright"},
                {"position_id": "external", "card_id": "ten_of_pentacles", "orientation": "upright"},
                {"position_id": "hopes_fears", "card_id": "the_tower", "orientation": "upright"},
                {"position_id": "outcome", "card_id": "three_of_cups", "orientation": "upright"}
            ]
        }
        
        start_time = time.time()
        result = self.engine.compute_influenced_meanings(celtic_spread, self.card_database)
        end_time = time.time()
        
        processing_time = end_time - start_time
        assert processing_time < 0.2  # Should be under 200ms
    
    def test_spread_deterministic_output(self):
        """Test that spreads produce deterministic output."""
        spread_data = {
            "reading_id": "deterministic_test_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "present", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "two_of_wands", "orientation": "upright"}
            ]
        }
        
        # Run the same input multiple times
        result1 = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        result2 = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Results should be identical
        assert result1["reading_id"] == result2["reading_id"]
        assert result1["summary"] == result2["summary"]
        assert len(result1["cards"]) == len(result2["cards"])
        
        for card1, card2 in zip(result1["cards"], result2["cards"]):
            assert card1["polarity_score"] == card2["polarity_score"]
            assert card1["intensity_score"] == card2["intensity_score"]
            assert card1["influenced_text"] == card2["influenced_text"]
            assert len(card1["influence_factors"]) == len(card2["influence_factors"])
    
    def test_spread_schema_validation(self):
        """Test that spread outputs validate against schema."""
        spread_data = {
            "reading_id": "schema_test_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "present", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "two_of_wands", "orientation": "upright"}
            ]
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Validate required fields
        assert "reading_id" in result
        assert "summary" in result
        assert "cards" in result
        assert "advice" in result
        assert "follow_up_questions" in result
        
        # Validate card structure
        for card in result["cards"]:
            required_fields = ["position", "card_id", "card_name", "orientation", "base_text", "influenced_text", "polarity_score", "intensity_score", "themes", "influence_factors", "journal_prompt"]
            for field in required_fields:
                assert field in card
            
            # Validate numeric ranges
            assert -2.0 <= card["polarity_score"] <= 2.0
            assert 0.0 <= card["intensity_score"] <= 1.0
            
            # Validate influence factors
            for factor in card["influence_factors"]:
                assert "source_position" in factor
                assert "source_card_id" in factor
                assert "effect" in factor
                assert "explain" in factor

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])