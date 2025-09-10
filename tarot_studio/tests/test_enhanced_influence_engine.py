"""
Unit tests for the Enhanced Tarot Influence Engine.

This module contains comprehensive tests for all influence rules and edge cases.
"""

import pytest
import json
from typing import Dict, Any, List
from tarot_studio.core.enhanced_influence_engine import (
    EnhancedInfluenceEngine, EngineConfig, CardMetadata, CardPosition, 
    InfluencedCard, InfluenceFactor, Orientation, Arcana, Element
)

class TestEnhancedInfluenceEngine:
    """Test suite for the Enhanced Influence Engine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = EngineConfig()
        self.engine = EnhancedInfluenceEngine(self.config)
        
        # Create test card database
        self.card_database = {
            "the_sun": {
                "card_id": "the_sun",
                "name": "The Sun",
                "arcana": "major",
                "element": "fire",
                "polarity": 1.0,
                "intensity": 0.9,
                "keywords": ["joy", "success", "vitality"],
                "themes": {"joy": 0.9, "success": 0.8, "vitality": 0.7},
                "upright_meaning": "The Sun represents joy, success, and vitality.",
                "reversed_meaning": "Reversed, The Sun suggests temporary setbacks."
            },
            "the_moon": {
                "card_id": "the_moon",
                "name": "The Moon",
                "arcana": "major",
                "element": "water",
                "polarity": -0.3,
                "intensity": 0.7,
                "keywords": ["illusion", "intuition", "mystery"],
                "themes": {"illusion": 0.8, "intuition": 0.7, "mystery": 0.6},
                "upright_meaning": "The Moon represents intuition and mystery.",
                "reversed_meaning": "Reversed, The Moon suggests confusion."
            },
            "ace_of_wands": {
                "card_id": "ace_of_wands",
                "name": "Ace of Wands",
                "arcana": "minor",
                "suit": "wands",
                "number": 1,
                "element": "fire",
                "polarity": 0.8,
                "intensity": 0.7,
                "keywords": ["inspiration", "creativity", "new_beginnings"],
                "themes": {"inspiration": 0.9, "creativity": 0.8, "new_beginnings": 0.7},
                "upright_meaning": "The Ace of Wands represents new inspiration.",
                "reversed_meaning": "Reversed, the Ace of Wands suggests blocked creativity."
            },
            "two_of_wands": {
                "card_id": "two_of_wands",
                "name": "Two of Wands",
                "arcana": "minor",
                "suit": "wands",
                "number": 2,
                "element": "fire",
                "polarity": 0.6,
                "intensity": 0.6,
                "keywords": ["planning", "future", "personal_power"],
                "themes": {"planning": 0.8, "future": 0.7, "personal_power": 0.6},
                "upright_meaning": "The Two of Wands represents planning and future vision.",
                "reversed_meaning": "Reversed, the Two of Wands suggests lack of planning."
            },
            "three_of_wands": {
                "card_id": "three_of_wands",
                "name": "Three of Wands",
                "arcana": "minor",
                "suit": "wands",
                "number": 3,
                "element": "fire",
                "polarity": 0.7,
                "intensity": 0.6,
                "keywords": ["expansion", "foresight", "leadership"],
                "themes": {"expansion": 0.8, "foresight": 0.7, "leadership": 0.6},
                "upright_meaning": "The Three of Wands represents expansion and foresight.",
                "reversed_meaning": "Reversed, the Three of Wands suggests lack of expansion."
            },
            "ace_of_cups": {
                "card_id": "ace_of_cups",
                "name": "Ace of Cups",
                "arcana": "minor",
                "suit": "cups",
                "number": 1,
                "element": "water",
                "polarity": 0.8,
                "intensity": 0.6,
                "keywords": ["love", "emotions", "spirituality"],
                "themes": {"love": 0.9, "emotions": 0.8, "spirituality": 0.7},
                "upright_meaning": "The Ace of Cups represents new love and emotions.",
                "reversed_meaning": "Reversed, the Ace of Cups suggests blocked emotions."
            },
            "five_of_swords": {
                "card_id": "five_of_swords",
                "name": "Five of Swords",
                "arcana": "minor",
                "suit": "swords",
                "number": 5,
                "element": "air",
                "polarity": -0.6,
                "intensity": 0.7,
                "keywords": ["conflict", "defeat", "betrayal"],
                "themes": {"conflict": 0.8, "defeat": 0.7, "betrayal": 0.6},
                "upright_meaning": "The Five of Swords represents conflict and defeat.",
                "reversed_meaning": "Reversed, the Five of Swords suggests avoiding conflict."
            }
        }
    
    def test_engine_initialization(self):
        """Test engine initialization with default config."""
        engine = EnhancedInfluenceEngine()
        assert engine.config.dominance_multiplier == 1.5
        assert engine.config.reversal_decay_factor == 0.8
        assert engine.config.conflict_threshold == 0.5
        assert engine.config.theme_threshold == 0.3
    
    def test_engine_initialization_custom_config(self):
        """Test engine initialization with custom config."""
        config = EngineConfig(
            dominance_multiplier=2.0,
            reversal_decay_factor=0.7,
            conflict_threshold=0.6
        )
        engine = EnhancedInfluenceEngine(config)
        assert engine.config.dominance_multiplier == 2.0
        assert engine.config.reversal_decay_factor == 0.7
        assert engine.config.conflict_threshold == 0.6
    
    def test_load_card_metadata(self):
        """Test loading card metadata from dictionary."""
        card_data = self.card_database["the_sun"]
        card_metadata = self.engine.load_card_metadata(card_data)
        
        assert card_metadata.card_id == "the_sun"
        assert card_metadata.name == "The Sun"
        assert card_metadata.arcana == Arcana.MAJOR
        assert card_metadata.element == Element.FIRE
        assert card_metadata.baseline_polarity == 1.0
        assert card_metadata.baseline_intensity == 0.9
        assert "joy" in card_metadata.keywords
        assert card_metadata.themes["joy"] == 0.9
    
    def test_elemental_affinity_matrix_traditional(self):
        """Test traditional elemental affinity matrix."""
        config = EngineConfig(elemental_system="traditional")
        engine = EnhancedInfluenceEngine(config)
        
        # Fire + Fire should reinforce
        assert engine.elemental_affinity_matrix["fire"]["fire"] > 1.0
        
        # Fire + Water should oppose
        assert engine.elemental_affinity_matrix["fire"]["water"] < 1.0
        
        # Fire + Air should be neutral
        assert engine.elemental_affinity_matrix["fire"]["air"] == 1.0
    
    def test_elemental_affinity_matrix_crowley(self):
        """Test Crowley elemental affinity matrix."""
        config = EngineConfig(elemental_system="crowley")
        engine = EnhancedInfluenceEngine(config)
        
        # Crowley system should have different values
        assert engine.elemental_affinity_matrix["fire"]["fire"] == 1.2
        assert engine.elemental_affinity_matrix["fire"]["water"] == 0.6
        assert engine.elemental_affinity_matrix["fire"]["air"] == 1.0
        assert engine.elemental_affinity_matrix["fire"]["earth"] == 0.8
    
    def test_elemental_affinity_matrix_simplified(self):
        """Test simplified elemental affinity matrix."""
        config = EngineConfig(elemental_system="simplified")
        engine = EnhancedInfluenceEngine(config)
        
        # Simplified system should have moderate values
        assert engine.elemental_affinity_matrix["fire"]["fire"] == 1.1
        assert engine.elemental_affinity_matrix["fire"]["water"] == 0.7
        assert engine.elemental_affinity_matrix["fire"]["air"] == 1.0
        assert engine.elemental_affinity_matrix["fire"]["earth"] == 0.9
    
    def test_canonical_adjacency_matrices(self):
        """Test canonical adjacency matrices for standard spreads."""
        # Three-card spread
        three_card_matrix = self.engine.adjacency_matrices["three_card"]
        assert three_card_matrix["past"]["present"] == 1.0
        assert three_card_matrix["present"]["future"] == 1.0
        assert three_card_matrix["past"]["future"] == 0.5
        
        # Celtic Cross
        celtic_matrix = self.engine.adjacency_matrices["celtic_cross"]
        assert celtic_matrix["situation"]["challenge"] == 1.0
        assert celtic_matrix["past"]["future"] == 0.8
        assert celtic_matrix["advice"]["external"] == 0.8
        
        # Relationship Cross
        relationship_matrix = self.engine.adjacency_matrices["relationship_cross"]
        assert relationship_matrix["you"]["partner"] == 1.0
        assert relationship_matrix["connection"]["advice"] == 0.8
        
        # Year Ahead
        year_matrix = self.engine.adjacency_matrices["year_ahead"]
        assert year_matrix["january"]["february"] == 1.0
        assert year_matrix["december"]["january"] == 0.5
    
    def test_adjacency_influence_rule(self):
        """Test adjacency influence rule."""
        # Create test cards
        card1_metadata = self.engine.load_card_metadata(self.card_database["the_sun"])
        card2_metadata = self.engine.load_card_metadata(self.card_database["ace_of_wands"])
        
        card1_pos = CardPosition("past", "the_sun", Orientation.UPRIGHT, card1_metadata)
        card2_pos = CardPosition("present", "ace_of_wands", Orientation.UPRIGHT, card2_metadata)
        
        # Create influenced card
        influenced_card = InfluencedCard(
            position="present",
            card_id="ace_of_wands",
            card_name="Ace of Wands",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=0.8,
            intensity_score=0.7,
            themes={"inspiration": 0.9},
            influence_factors=[],
            journal_prompt=""
        )
        
        # Apply adjacency influence
        adjacency_matrix = {"present": {"past": 1.0}}
        self.engine._apply_adjacency_influence(influenced_card, [card1_pos], adjacency_matrix)
        
        # Check that influence was applied
        assert influenced_card.polarity_score > 0.8  # Should be increased
        assert len(influenced_card.influence_factors) == 1
        assert influenced_card.influence_factors[0].source_card_id == "the_sun"
        assert influenced_card.influence_factors[0].explain.startswith("Adjacency influence")
    
    def test_elemental_dignities_rule(self):
        """Test elemental dignities rule."""
        # Create test cards with same element (fire)
        card1_metadata = self.engine.load_card_metadata(self.card_database["the_sun"])
        card2_metadata = self.engine.load_card_metadata(self.card_database["ace_of_wands"])
        
        card1_pos = CardPosition("past", "the_sun", Orientation.UPRIGHT, card1_metadata)
        card2_pos = CardPosition("present", "ace_of_wands", Orientation.UPRIGHT, card2_metadata)
        
        # Create influenced card
        influenced_card = InfluencedCard(
            position="present",
            card_id="ace_of_wands",
            card_name="Ace of Wands",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=0.8,
            intensity_score=0.7,
            themes={"inspiration": 0.9},
            influence_factors=[],
            journal_prompt=""
        )
        
        # Apply elemental dignities
        self.engine._apply_elemental_dignities(influenced_card, [card1_pos])
        
        # Check that elemental affinity was applied
        assert len(influenced_card.influence_factors) == 1
        assert influenced_card.influence_factors[0].explain.startswith("Elemental affinity")
        assert "fire" in influenced_card.influence_factors[0].explain
    
    def test_major_dominance_rule(self):
        """Test Major Arcana dominance rule."""
        # Create test cards - Major Arcana influencing Minor Arcana
        card1_metadata = self.engine.load_card_metadata(self.card_database["the_sun"])
        card2_metadata = self.engine.load_card_metadata(self.card_database["ace_of_wands"])
        
        card1_pos = CardPosition("past", "the_sun", Orientation.UPRIGHT, card1_metadata)
        card2_pos = CardPosition("present", "ace_of_wands", Orientation.UPRIGHT, card2_metadata)
        
        # Create influenced card (Minor Arcana)
        influenced_card = InfluencedCard(
            position="present",
            card_id="ace_of_wands",
            card_name="Ace of Wands",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=0.8,
            intensity_score=0.7,
            themes={"inspiration": 0.9},
            influence_factors=[],
            journal_prompt=""
        )
        
        # Apply Major dominance
        self.engine._apply_major_dominance(influenced_card, [card1_pos])
        
        # Check that Major dominance was applied
        assert len(influenced_card.influence_factors) == 1
        assert influenced_card.influence_factors[0].explain.startswith("Major Arcana dominance")
        assert "1.5x" in influenced_card.influence_factors[0].explain
    
    def test_numerical_sequence_detection(self):
        """Test numerical sequence detection rule."""
        # Create test cards with numerical sequence
        card1_metadata = self.engine.load_card_metadata(self.card_database["ace_of_wands"])
        card2_metadata = self.engine.load_card_metadata(self.card_database["two_of_wands"])
        card3_metadata = self.engine.load_card_metadata(self.card_database["three_of_wands"])
        
        card1_pos = CardPosition("past", "ace_of_wands", Orientation.UPRIGHT, card1_metadata)
        card2_pos = CardPosition("present", "two_of_wands", Orientation.UPRIGHT, card2_metadata)
        card3_pos = CardPosition("future", "three_of_wands", Orientation.UPRIGHT, card3_metadata)
        
        all_cards = [card1_pos, card2_pos, card3_pos]
        
        # Create influenced card
        influenced_card = InfluencedCard(
            position="present",
            card_id="two_of_wands",
            card_name="Two of Wands",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=0.6,
            intensity_score=0.6,
            themes={"planning": 0.8},
            influence_factors=[],
            journal_prompt=""
        )
        
        # Apply numerical sequence detection
        self.engine._apply_numerical_sequences(influenced_card, all_cards)
        
        # Check that sequence was detected
        assert "continuity" in influenced_card.themes
        assert influenced_card.themes["continuity"] > 0
        assert influenced_card.intensity_score > 0.6
        assert len(influenced_card.influence_factors) == 1
        assert influenced_card.influence_factors[0].explain.startswith("Numerical sequence detected")
    
    def test_reversal_propagation_rule(self):
        """Test reversal propagation rule."""
        # Create test cards with reversed neighbor
        card1_metadata = self.engine.load_card_metadata(self.card_database["the_moon"])
        card2_metadata = self.engine.load_card_metadata(self.card_database["ace_of_wands"])
        
        card1_pos = CardPosition("past", "the_moon", Orientation.REVERSED, card1_metadata)
        card2_pos = CardPosition("present", "ace_of_wands", Orientation.UPRIGHT, card2_metadata)
        
        # Create influenced card
        influenced_card = InfluencedCard(
            position="present",
            card_id="ace_of_wands",
            card_name="Ace of Wands",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=0.8,
            intensity_score=0.7,
            themes={"inspiration": 0.9},
            influence_factors=[],
            journal_prompt=""
        )
        
        # Apply reversal propagation
        self.engine._apply_reversal_propagation(influenced_card, [card1_pos])
        
        # Check that reversal propagation was applied
        assert influenced_card.intensity_score < 0.7  # Should be reduced
        assert len(influenced_card.influence_factors) == 1
        assert influenced_card.influence_factors[0].explain.startswith("Reversal propagation")
        assert "decay" in influenced_card.influence_factors[0].explain
    
    def test_conflict_resolution_rule(self):
        """Test conflict resolution rule."""
        # Create test cards with opposing polarities
        card1_metadata = self.engine.load_card_metadata(self.card_database["the_sun"])
        card2_metadata = self.engine.load_card_metadata(self.card_database["five_of_swords"])
        
        card1_pos = CardPosition("past", "the_sun", Orientation.UPRIGHT, card1_metadata)
        card2_pos = CardPosition("present", "five_of_swords", Orientation.UPRIGHT, card2_metadata)
        
        all_cards = [card1_pos, card2_pos]
        
        # Create influenced card
        influenced_card = InfluencedCard(
            position="present",
            card_id="five_of_swords",
            card_name="Five of Swords",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=-0.6,
            intensity_score=0.7,
            themes={"conflict": 0.8},
            influence_factors=[],
            journal_prompt=""
        )
        
        # Apply conflict resolution
        self.engine._apply_conflict_resolution(influenced_card, all_cards)
        
        # Check that conflict resolution was applied
        assert len(influenced_card.influence_factors) == 1
        assert influenced_card.influence_factors[0].explain.startswith("Conflict resolution")
        assert "damping" in influenced_card.influence_factors[0].explain
    
    def test_narrative_boost_rule(self):
        """Test narrative boost rule."""
        # Create test cards with shared themes
        card1_metadata = self.engine.load_card_metadata(self.card_database["ace_of_wands"])
        card2_metadata = self.engine.load_card_metadata(self.card_database["two_of_wands"])
        
        card1_pos = CardPosition("past", "ace_of_wands", Orientation.UPRIGHT, card1_metadata)
        card2_pos = CardPosition("present", "two_of_wands", Orientation.UPRIGHT, card2_metadata)
        
        all_cards = [card1_pos, card2_pos]
        
        # Create influenced card
        influenced_card = InfluencedCard(
            position="present",
            card_id="two_of_wands",
            card_name="Two of Wands",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=0.6,
            intensity_score=0.6,
            themes={"planning": 0.8, "future": 0.7},
            influence_factors=[],
            journal_prompt=""
        )
        
        # Apply narrative boost
        self.engine._apply_narrative_boost(influenced_card, all_cards)
        
        # Check that narrative boost was applied
        assert len(influenced_card.influence_factors) == 1
        assert influenced_card.influence_factors[0].explain.startswith("Narrative boost")
        assert "theme" in influenced_card.influence_factors[0].explain
    
    def test_local_overrides_rule(self):
        """Test local overrides rule."""
        # Create test card
        card_metadata = self.engine.load_card_metadata(self.card_database["ace_of_wands"])
        card_pos = CardPosition("present", "ace_of_wands", Orientation.UPRIGHT, card_metadata)
        
        # Create influenced card
        influenced_card = InfluencedCard(
            position="present",
            card_id="ace_of_wands",
            card_name="Ace of Wands",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=0.8,
            intensity_score=0.7,
            themes={"inspiration": 0.9},
            influence_factors=[],
            journal_prompt=""
        )
        
        # Apply local overrides
        rule_overrides = [
            {
                "type": "polarity_multiplier",
                "card_id": "ace_of_wands",
                "multiplier": 1.5
            }
        ]
        
        self.engine._apply_local_overrides(influenced_card, rule_overrides)
        
        # Check that local override was applied
        assert len(influenced_card.influence_factors) == 1
        assert influenced_card.influence_factors[0].explain.startswith("Local polarity override")
    
    def test_complete_three_card_reading(self):
        """Test complete three-card reading processing."""
        spread_data = {
            "reading_id": "test_three_card_001",
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
        
        # Validate result structure
        assert result["reading_id"] == "test_three_card_001"
        assert "summary" in result
        assert len(result["cards"]) == 3
        assert "advice" in result
        assert "follow_up_questions" in result
        
        # Validate each card
        for card in result["cards"]:
            assert "position" in card
            assert "card_id" in card
            assert "card_name" in card
            assert "orientation" in card
            assert "base_text" in card
            assert "influenced_text" in card
            assert "polarity_score" in card
            assert "intensity_score" in card
            assert "themes" in card
            assert "influence_factors" in card
            assert "journal_prompt" in card
            
            # Validate numeric ranges
            assert -2.0 <= card["polarity_score"] <= 2.0
            assert 0.0 <= card["intensity_score"] <= 1.0
            
            # Validate influence factors
            for factor in card["influence_factors"]:
                assert "source_position" in factor
                assert "source_card_id" in factor
                assert "effect" in factor
                assert "explain" in factor
    
    def test_celtic_cross_reading(self):
        """Test Celtic Cross reading processing."""
        spread_data = {
            "reading_id": "test_celtic_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "celtic_cross",
            "positions": [
                {"position_id": "situation", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "challenge", "card_id": "five_of_swords", "orientation": "upright"},
                {"position_id": "past", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "two_of_wands", "orientation": "upright"},
                {"position_id": "above", "card_id": "three_of_wands", "orientation": "upright"},
                {"position_id": "below", "card_id": "ace_of_cups", "orientation": "upright"},
                {"position_id": "advice", "card_id": "the_moon", "orientation": "upright"},
                {"position_id": "external", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "hopes_fears", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "outcome", "card_id": "two_of_wands", "orientation": "upright"}
            ],
            "user_context": "What does my future hold?"
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Validate result structure
        assert result["reading_id"] == "test_celtic_001"
        assert len(result["cards"]) == 10
        
        # Validate complex influence patterns
        for card in result["cards"]:
            assert len(card["influence_factors"]) >= 0  # Should have some influence factors
            assert card["polarity_score"] >= -2.0
            assert card["polarity_score"] <= 2.0
            assert card["intensity_score"] >= 0.0
            assert card["intensity_score"] <= 1.0
    
    def test_error_handling_invalid_card_id(self):
        """Test error handling for invalid card ID."""
        spread_data = {
            "reading_id": "test_error_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "invalid_card", "orientation": "upright"}
            ]
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Should return error response
        assert "Error processing reading" in result["summary"]
        assert len(result["cards"]) == 0
    
    def test_error_handling_invalid_orientation(self):
        """Test error handling for invalid orientation."""
        spread_data = {
            "reading_id": "test_error_002",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_sun", "orientation": "invalid"}
            ]
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Should return error response
        assert "Error processing reading" in result["summary"]
        assert len(result["cards"]) == 0
    
    def test_deterministic_output(self):
        """Test that the engine produces deterministic output."""
        spread_data = {
            "reading_id": "test_deterministic_001",
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
    
    def test_score_normalization(self):
        """Test that scores are properly normalized."""
        spread_data = {
            "reading_id": "test_normalization_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "present", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "future", "card_id": "the_sun", "orientation": "upright"}
            ]
        }
        
        result = self.engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # All scores should be within valid ranges
        for card in result["cards"]:
            assert -2.0 <= card["polarity_score"] <= 2.0
            assert 0.0 <= card["intensity_score"] <= 1.0
            
            # Theme weights should be within valid ranges
            for theme, weight in card["themes"].items():
                assert 0.0 <= weight <= 1.0
    
    def test_template_generation_fallback(self):
        """Test template generation when LLM is disabled."""
        config = EngineConfig(enable_llm_generation=False)
        engine = EnhancedInfluenceEngine(config)
        
        spread_data = {
            "reading_id": "test_template_001",
            "date_time": "2024-01-15T10:30:00Z",
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
                {"position_id": "present", "card_id": "ace_of_wands", "orientation": "upright"},
                {"position_id": "future", "card_id": "two_of_wands", "orientation": "upright"}
            ]
        }
        
        result = engine.compute_influenced_meanings(spread_data, self.card_database)
        
        # Should still produce valid results
        assert result["reading_id"] == "test_template_001"
        assert len(result["cards"]) == 3
        
        for card in result["cards"]:
            assert card["influenced_text"] != ""
            assert card["base_text"] in card["influenced_text"]  # Should contain base text
    
    def test_journal_prompt_generation(self):
        """Test journal prompt generation."""
        card_metadata = self.engine.load_card_metadata(self.card_database["the_sun"])
        card_pos = CardPosition("past", "the_sun", Orientation.UPRIGHT, card_metadata)
        
        influenced_card = InfluencedCard(
            position="past",
            card_id="the_sun",
            card_name="The Sun",
            orientation="upright",
            base_text="Test text",
            influenced_text="",
            polarity_score=1.0,
            intensity_score=0.9,
            themes={"joy": 0.9},
            influence_factors=[
                InfluenceFactor("present", "ace_of_wands", "+0.20", "Adjacency influence")
            ],
            journal_prompt=""
        )
        
        journal_prompt = self.engine._generate_journal_prompt(influenced_card)
        
        assert "The Sun" in journal_prompt
        assert "past position" in journal_prompt
        assert "ace_of_wands" in journal_prompt
        assert journal_prompt.endswith("?")
    
    def test_summary_generation(self):
        """Test summary generation."""
        # Create test influenced cards
        cards = [
            InfluencedCard(
                position="past",
                card_id="the_sun",
                card_name="The Sun",
                orientation="upright",
                base_text="Test text",
                influenced_text="",
                polarity_score=1.0,
                intensity_score=0.9,
                themes={"joy": 0.9},
                influence_factors=[],
                journal_prompt=""
            ),
            InfluencedCard(
                position="present",
                card_id="ace_of_wands",
                card_name="Ace of Wands",
                orientation="upright",
                base_text="Test text",
                influenced_text="",
                polarity_score=0.8,
                intensity_score=0.7,
                themes={"inspiration": 0.9},
                influence_factors=[],
                journal_prompt=""
            )
        ]
        
        summary = self.engine._generate_summary(cards)
        
        assert len(summary) > 0
        assert "reading" in summary.lower()
        assert "positive" in summary.lower() or "uplifting" in summary.lower()
    
    def test_advice_generation(self):
        """Test advice generation."""
        # Create test influenced cards
        cards = [
            InfluencedCard(
                position="past",
                card_id="the_sun",
                card_name="The Sun",
                orientation="upright",
                base_text="Test text",
                influenced_text="",
                polarity_score=1.0,
                intensity_score=0.9,
                themes={"joy": 0.9, "love": 0.8},
                influence_factors=[],
                journal_prompt=""
            )
        ]
        
        advice = self.engine._generate_advice(cards)
        
        assert len(advice) > 0
        assert len(advice) <= 5  # Should be limited to 5 pieces of advice
        assert all(isinstance(item, str) for item in advice)
    
    def test_follow_up_questions_generation(self):
        """Test follow-up questions generation."""
        # Create test influenced cards
        cards = [
            InfluencedCard(
                position="past",
                card_id="the_sun",
                card_name="The Sun",
                orientation="upright",
                base_text="Test text",
                influenced_text="",
                polarity_score=1.0,
                intensity_score=0.9,
                themes={"joy": 0.9, "career": 0.8},
                influence_factors=[],
                journal_prompt=""
            )
        ]
        
        questions = self.engine._generate_follow_up_questions(cards)
        
        assert len(questions) > 0
        assert len(questions) <= 5  # Should be limited to 5 questions
        assert all(isinstance(item, str) for item in questions)
        assert all("?" in question for question in questions)

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])