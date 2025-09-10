#!/usr/bin/env python3
"""
Simple test script for the Enhanced Tarot Influence Engine.
This verifies core functionality without requiring pytest.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tarot_studio'))

from tarot_studio.core.enhanced_influence_engine import EnhancedInfluenceEngine, EngineConfig

def test_engine_initialization():
    """Test engine initialization."""
    print("Testing engine initialization...")
    
    # Test default config
    engine = EnhancedInfluenceEngine()
    assert engine.config.dominance_multiplier == 1.5
    assert engine.config.reversal_decay_factor == 0.8
    assert engine.config.conflict_threshold == 0.5
    assert engine.config.theme_threshold == 0.3
    print("✅ Default config initialization passed")
    
    # Test custom config
    config = EngineConfig(
        dominance_multiplier=2.0,
        reversal_decay_factor=0.7,
        conflict_threshold=0.6
    )
    engine = EnhancedInfluenceEngine(config)
    assert engine.config.dominance_multiplier == 2.0
    assert engine.config.reversal_decay_factor == 0.7
    assert engine.config.conflict_threshold == 0.6
    print("✅ Custom config initialization passed")

def test_elemental_affinity_matrix():
    """Test elemental affinity matrix."""
    print("Testing elemental affinity matrix...")
    
    # Test traditional system
    config = EngineConfig(elemental_system="traditional")
    engine = EnhancedInfluenceEngine(config)
    
    # Fire + Fire should reinforce
    assert engine.elemental_affinity_matrix["fire"]["fire"] > 1.0
    # Fire + Water should oppose
    assert engine.elemental_affinity_matrix["fire"]["water"] < 1.0
    # Fire + Air should be neutral
    assert engine.elemental_affinity_matrix["fire"]["air"] == 1.0
    print("✅ Traditional elemental system passed")
    
    # Test Crowley system
    config = EngineConfig(elemental_system="crowley")
    engine = EnhancedInfluenceEngine(config)
    
    assert engine.elemental_affinity_matrix["fire"]["fire"] == 1.2
    assert engine.elemental_affinity_matrix["fire"]["water"] == 0.6
    assert engine.elemental_affinity_matrix["fire"]["air"] == 1.0
    assert engine.elemental_affinity_matrix["fire"]["earth"] == 0.8
    print("✅ Crowley elemental system passed")

def test_adjacency_matrices():
    """Test canonical adjacency matrices."""
    print("Testing adjacency matrices...")
    
    engine = EnhancedInfluenceEngine()
    
    # Three-card spread
    three_card_matrix = engine.adjacency_matrices["three_card"]
    assert three_card_matrix["past"]["present"] == 1.0
    assert three_card_matrix["present"]["future"] == 1.0
    assert three_card_matrix["past"]["future"] == 0.5
    print("✅ Three-card adjacency matrix passed")
    
    # Celtic Cross
    celtic_matrix = engine.adjacency_matrices["celtic_cross"]
    assert celtic_matrix["situation"]["challenge"] == 1.0
    assert celtic_matrix["past"]["future"] == 0.8
    assert celtic_matrix["advice"]["external"] == 0.8
    print("✅ Celtic Cross adjacency matrix passed")

def test_complete_reading():
    """Test complete reading processing."""
    print("Testing complete reading processing...")
    
    engine = EnhancedInfluenceEngine()
    
    # Create test card database
    card_database = {
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
        }
    }
    
    # Create test spread
    spread_data = {
        "reading_id": "test_001",
        "date_time": "2024-01-15T10:30:00Z",
        "spread_type": "three_card",
        "positions": [
            {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
            {"position_id": "present", "card_id": "ace_of_wands", "orientation": "upright"},
            {"position_id": "future", "card_id": "two_of_wands", "orientation": "upright"}
        ],
        "user_context": "What does my future hold?"
    }
    
    # Process reading
    result = engine.compute_influenced_meanings(spread_data, card_database)
    
    # Validate result structure
    assert result["reading_id"] == "test_001"
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
    
    print("✅ Complete reading processing passed")

def test_deterministic_output():
    """Test deterministic output."""
    print("Testing deterministic output...")
    
    engine = EnhancedInfluenceEngine()
    
    # Create test data
    card_database = {
        "the_sun": {
            "card_id": "the_sun", "name": "The Sun", "arcana": "major", "element": "fire",
            "polarity": 1.0, "intensity": 0.9, "keywords": ["joy"], "themes": {"joy": 0.9},
            "upright_meaning": "The Sun represents joy.", "reversed_meaning": "Reversed, The Sun suggests setbacks."
        }
    }
    
    spread_data = {
        "reading_id": "test_deterministic",
        "spread_type": "single_card",
        "positions": [{"position_id": "guidance", "card_id": "the_sun", "orientation": "upright"}]
    }
    
    # Run the same input multiple times
    result1 = engine.compute_influenced_meanings(spread_data, card_database)
    result2 = engine.compute_influenced_meanings(spread_data, card_database)
    
    # Results should be identical
    assert result1["reading_id"] == result2["reading_id"]
    assert result1["summary"] == result2["summary"]
    assert len(result1["cards"]) == len(result2["cards"])
    
    for card1, card2 in zip(result1["cards"], result2["cards"]):
        assert card1["polarity_score"] == card2["polarity_score"]
        assert card1["intensity_score"] == card2["intensity_score"]
        assert card1["influenced_text"] == card2["influenced_text"]
    
    print("✅ Deterministic output test passed")

def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")
    
    engine = EnhancedInfluenceEngine()
    
    # Test invalid card ID
    spread_data = {
        "reading_id": "test_error",
        "spread_type": "single_card",
        "positions": [{"position_id": "guidance", "card_id": "invalid_card", "orientation": "upright"}]
    }
    
    card_database = {}
    result = engine.compute_influenced_meanings(spread_data, card_database)
    
    # Should return error response
    assert "Error processing reading" in result["summary"]
    assert len(result["cards"]) == 0
    
    print("✅ Error handling test passed")

def main():
    """Run all tests."""
    print("Enhanced Tarot Influence Engine - Test Suite")
    print("=" * 50)
    
    try:
        test_engine_initialization()
        test_elemental_affinity_matrix()
        test_adjacency_matrices()
        test_complete_reading()
        test_deterministic_output()
        test_error_handling()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Enhanced Influence Engine is working correctly.")
        print("✅ Engine initialization")
        print("✅ Elemental affinity matrices")
        print("✅ Adjacency matrices")
        print("✅ Complete reading processing")
        print("✅ Deterministic output")
        print("✅ Error handling")
        print("\nThe Enhanced Tarot Influence Engine is ready for production use!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())