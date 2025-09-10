#!/usr/bin/env python3
"""
Comprehensive Test Suite for Tarot Studio

This script tests all completed modules and their integration,
providing a complete validation of the project's functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tarot_studio'))

from datetime import datetime
import tempfile
import json


def test_deck_module():
    """Test the Deck module functionality."""
    print("Testing Deck Module...")
    
    try:
        from tarot_studio.deck import Deck, Card, Orientation, Arcana, Suit, Element
        
        # Test loading deck
        deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
        assert len(deck) == 78, f"Expected 78 cards, got {len(deck)}"
        
        # Test deck info
        info = deck.get_deck_info()
        assert info['total_cards'] == 78
        assert info['major_arcana'] == 22
        assert info['minor_arcana'] == 56
        
        # Test shuffling
        deck.shuffle(seed=42)
        assert len(deck) == 78  # Should still have all cards
        
        # Test drawing cards
        card = deck.draw_card()
        assert card is not None
        assert len(deck) == 77  # Should have one less card
        
        # Test drawing multiple cards
        cards = deck.draw_cards(3)
        assert len(cards) == 3
        assert len(deck) == 74  # Should have 3 less cards
        
        # Test reset
        deck.reset()
        assert len(deck) == 78  # Should be back to full deck
        
        # Test filtering
        major_cards = deck.get_major_arcana()
        assert len(major_cards) == 22
        
        minor_cards = deck.get_minor_arcana()
        assert len(minor_cards) == 56
        
        print("✅ Deck Module tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Deck Module test failed: {e}")
        return False


def test_spreads_module():
    """Test the Spreads module functionality."""
    print("Testing Spreads Module...")
    
    try:
        from tarot_studio.spreads import (
            SpreadLayout, SpreadPosition, TarotSpread, SpreadManager,
            PositionType
        )
        from tarot_studio.deck import Deck
        
        # Test creating layouts
        single_layout = SpreadLayout.create_single_card()
        assert single_layout.card_count == 1
        assert single_layout.id == "single_card"
        
        three_layout = SpreadLayout.create_three_card()
        assert three_layout.card_count == 3
        assert three_layout.id == "three_card"
        
        celtic_layout = SpreadLayout.create_celtic_cross()
        assert celtic_layout.card_count == 10
        assert celtic_layout.id == "celtic_cross"
        
        # Test layout validation
        errors = single_layout.validate()
        assert len(errors) == 0, f"Layout validation errors: {errors}"
        
        # Test spread manager
        manager = SpreadManager()
        spreads = manager.get_available_spreads()
        assert len(spreads) > 0
        
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
            'test_spread',
            'Test Spread',
            'A test spread',
            positions
        )
        assert custom_layout.card_count == 2
        
        # Test creating tarot spread
        deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
        deck.shuffle(seed=123)
        
        spread = TarotSpread.create_three_card_reading(deck, "What does my future hold?")
        reading = spread.draw_cards()
        
        assert reading is not None
        assert len(reading.cards) == 3
        assert reading.user_context == "What does my future hold?"
        
        # Test reading summary
        summary = spread.get_reading_summary()
        assert summary['card_count'] == 3
        assert summary['layout_name'] == 'Three Card'
        
        # Test position meanings
        meanings = spread.get_all_meanings()
        assert len(meanings) == 3
        
        print("✅ Spreads Module tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Spreads Module test failed: {e}")
        return False


def test_ai_module():
    """Test the AI module functionality."""
    print("Testing AI Module...")
    
    try:
        from tarot_studio.ai.ollama_client import OllamaClient, ConversationContext
        from tarot_studio.ai.memory import MemoryStore
        from tarot_studio.ai.conversation_manager import ConversationManager
        from tarot_studio.ai.prompt_templates import PromptTemplateManager
        from tarot_studio.ai.ai_config import AIConfigManager
        
        # Test OllamaClient
        client = OllamaClient("test-model", "http://localhost:11434")
        assert client.model_name == "test-model"
        assert client.base_url == "http://localhost:11434"
        
        # Test MemoryStore
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        memory_store = MemoryStore(temp_db.name)
        memory_id = memory_store.store_memory(
            entity_type="card",
            entity_name="The Fool",
            description="The Fool represents new beginnings",
            context="Card interpretation",
            importance_score=0.8
        )
        assert memory_id is not None
        
        # Test memory search
        results = memory_store.search_memories("fool", limit=1)
        assert len(results) > 0
        
        # Test ConversationManager
        mock_ollama_client = type('MockOllamaClient', (), {})()
        conversation_manager = ConversationManager(mock_ollama_client, memory_store)
        
        session = conversation_manager.create_session("card_chat", "test_user")
        assert session is not None
        assert session.conversation_type == "card_chat"
        
        # Test PromptTemplateManager
        template_manager = PromptTemplateManager()
        templates = template_manager.get_all_templates()
        assert len(templates) > 0
        
        # Test template rendering
        variables = {
            "card_name": "The Fool",
            "arcana_type": "Major Arcana",
            "suit": "None",
            "number": "0",
            "element": "Air",
            "keywords": "new beginnings, innocence",
            "upright_meaning": "New beginnings and taking a leap of faith",
            "reversed_meaning": "Recklessness or being held back",
            "orientation": "upright",
            "user_question": "What should I do?",
            "context": "User is at a crossroads"
        }
        
        prompt = template_manager.render_template("card_interpretation", variables)
        assert prompt is not None
        assert "The Fool" in prompt
        
        # Test AIConfigManager
        config_manager = AIConfigManager()
        settings = config_manager.get_settings()
        assert settings.default_model == "llama3.2"
        assert settings.temperature == 0.7
        
        models = config_manager.get_models()
        assert len(models) > 0
        
        # Clean up
        os.unlink(temp_db.name)
        
        print("✅ AI Module tests passed")
        return True
        
    except Exception as e:
        print(f"❌ AI Module test failed: {e}")
        return False


def test_influence_engine():
    """Test the Influence Engine functionality."""
    print("Testing Influence Engine...")
    
    try:
        from tarot_studio.core.enhanced_influence_engine import EnhancedInfluenceEngine
        
        # Test engine initialization
        engine = EnhancedInfluenceEngine()
        assert engine is not None
        
        # Test spread data processing
        spread_data = {
            "reading_id": "test_reading",
            "date_time": datetime.now().isoformat(),
            "spread_type": "three_card",
            "positions": [
                {"position_id": "past", "card_id": "the_fool", "orientation": "upright"},
                {"position_id": "present", "card_id": "the_magician", "orientation": "upright"},
                {"position_id": "future", "card_id": "the_world", "orientation": "upright"}
            ],
            "user_context": "What does my future hold?"
        }
        
        # Create simple card database
        card_database = {
            "the_fool": {
                "id": "the_fool",
                "name": "The Fool",
                "arcana": "major",
                "keywords": ["new beginnings", "innocence"],
                "polarity": 0.7,
                "intensity": 0.8
            },
            "the_magician": {
                "id": "the_magician",
                "name": "The Magician",
                "arcana": "major",
                "keywords": ["manifestation", "power"],
                "polarity": 0.8,
                "intensity": 0.9
            },
            "the_world": {
                "id": "the_world",
                "name": "The World",
                "arcana": "major",
                "keywords": ["completion", "success"],
                "polarity": 0.9,
                "intensity": 0.8
            }
        }
        
        # Test influence processing
        result = engine.compute_influenced_meanings(spread_data, card_database)
        assert result is not None
        assert 'cards' in result
        assert 'summary' in result
        assert 'advice' in result
        
        print("✅ Influence Engine tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Influence Engine test failed: {e}")
        return False


def test_module_integration():
    """Test integration between modules."""
    print("Testing Module Integration...")
    
    try:
        from tarot_studio.deck import Deck
        from tarot_studio.spreads import TarotSpread, SpreadManager
        from tarot_studio.ai.memory import MemoryStore
        from tarot_studio.ai.conversation_manager import ConversationManager
        from tarot_studio.ai.prompt_templates import PromptTemplateManager
        
        # Test deck and spreads integration
        deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
        deck.shuffle(seed=456)
        
        spread = TarotSpread.create_three_card_reading(deck, "What does my future hold?")
        reading = spread.draw_cards()
        
        assert len(reading.cards) == 3
        
        # Test AI and spreads integration
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        memory_store = MemoryStore(temp_db.name)
        mock_ollama_client = type('MockOllamaClient', (), {})()
        conversation_manager = ConversationManager(mock_ollama_client, memory_store)
        
        # Store reading in memory
        memory_id = memory_store.store_memory(
            entity_type="reading",
            entity_name=f"Reading {reading.spread_id}",
            description=f"Three card reading: {reading.user_context}",
            context=json.dumps({
                'spread_id': reading.spread_id,
                'layout_name': spread.layout.name,
                'cards': [{'position': card.position.name, 'card_name': card.card.name} for card in reading.cards]
            }),
            importance_score=0.8
        )
        
        # Test template integration
        template_manager = PromptTemplateManager()
        
        # Format cards for template
        cards_info = template_manager.format_cards_info([
            {'position': card.position.name, 'card_name': card.card.name, 'orientation': card.card.orientation.value}
            for card in reading.cards
        ])
        
        # Render reading interpretation template
        variables = {
            'spread_name': spread.layout.name,
            'user_question': reading.user_context,
            'reading_date': reading.reading_date.strftime('%Y-%m-%d'),
            'cards_info': cards_info,
            'context': 'Integration test'
        }
        
        prompt = template_manager.render_template('reading_interpretation', variables)
        assert prompt is not None
        assert spread.layout.name in prompt
        assert reading.user_context in prompt
        
        # Clean up
        os.unlink(temp_db.name)
        
        print("✅ Module Integration tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Module Integration test failed: {e}")
        return False


def test_file_structure():
    """Test that all required files exist and are properly structured."""
    print("Testing File Structure...")
    
    try:
        required_files = [
            # Core modules
            'tarot_studio/__init__.py',
            'tarot_studio/deck/__init__.py',
            'tarot_studio/deck/card.py',
            'tarot_studio/deck/deck.py',
            'tarot_studio/deck/card_data.json',
            'tarot_studio/deck/README.md',
            
            # Spreads module
            'tarot_studio/spreads/__init__.py',
            'tarot_studio/spreads/spread_layout.py',
            'tarot_studio/spreads/tarot_spread.py',
            'tarot_studio/spreads/spread_manager.py',
            'tarot_studio/spreads/README.md',
            
            # AI module
            'tarot_studio/ai/__init__.py',
            'tarot_studio/ai/ollama_client.py',
            'tarot_studio/ai/memory.py',
            'tarot_studio/ai/conversation_manager.py',
            'tarot_studio/ai/prompt_templates.py',
            'tarot_studio/ai/ai_config.py',
            'tarot_studio/ai/README.md',
            
            # Core engine
            'tarot_studio/core/enhanced_influence_engine.py',
            
            # Tests
            'tarot_studio/tests/test_deck_module.py',
            'tarot_studio/tests/test_spreads_module.py',
            'tarot_studio/tests/test_ai_module.py',
            
            # Documentation
            'Updates.md',
            'PROJECT_SUMMARY.md',
            'requirements.txt',
            'setup.py'
        ]
        
        for file_path in required_files:
            assert os.path.exists(file_path), f"Required file {file_path} does not exist"
            
            # Check that file is not empty
            with open(file_path, 'r') as f:
                content = f.read()
                assert len(content) > 50, f"File {file_path} appears to be empty or too small"
        
        print("✅ File Structure tests passed")
        return True
        
    except Exception as e:
        print(f"❌ File Structure test failed: {e}")
        return False


def test_database_module():
    """Test Database Module functionality."""
    print("Testing Database Module...")
    
    try:
        from tarot_studio.db.simple_db import SimpleDB
        
        # Create test database
        db = SimpleDB("test_comprehensive_db")
        
        # Test card operations
        cards = db.get_all_cards()
        assert len(cards) == 78, f"Expected 78 cards, got {len(cards)}"
        
        # Test major and minor arcana
        major_cards = db.get_cards_by_arcana('major')
        minor_cards = db.get_cards_by_arcana('minor')
        assert len(major_cards) == 22
        assert len(minor_cards) == 56
        
        # Test card by ID
        first_card = cards[0]
        card_by_id = db.get_card(first_card['id'])
        assert card_by_id is not None
        assert card_by_id['name'] == first_card['name']
        
        # Test spread operations
        spreads = db.get_all_spreads()
        assert len(spreads) >= 3
        
        # Test reading operations
        reading_data = {
            'title': 'Test Reading',
            'spread_id': spreads[0]['id'],
            'question': 'What do I need to know?',
            'interpretation': 'This is a test reading.',
            'summary': 'Test summary',
            'advice': ['Test advice'],
            'tags': ['test'],
            'people_involved': [],
            'is_private': False
        }
        
        reading_id = db.create_reading(reading_data)
        assert reading_id is not None
        
        reading = db.get_reading(reading_id)
        assert reading is not None
        assert reading['title'] == 'Test Reading'
        
        # Test memory operations
        memory_id = db.store_memory(
            entity_type="person",
            entity_name="Test Person",
            description="A test person",
            importance_score=0.8
        )
        assert memory_id is not None
        
        # Test memory search
        search_results = db.search_memories("test", limit=5)
        assert len(search_results) > 0
        
        # Test conversation operations
        conversation_id = db.create_conversation(
            title="Test Conversation",
            reading_id=reading_id
        )
        assert conversation_id is not None
        
        # Test adding message
        success = db.add_message(conversation_id, "user", "Test message")
        assert success
        
        # Test settings
        db.set_setting("test_key", "test_value")
        setting_value = db.get_setting("test_key")
        assert setting_value == "test_value"
        
        # Clean up
        db.close()
        
        print("✅ Database Module tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Database Module test failed: {e}")
        return False


def test_gui_module():
    """Test GUI Module functionality."""
    print("Testing GUI Module...")
    
    try:
        from tarot_studio.gui.simple_server import TarotServer
        
        # Test server creation
        server = TarotServer(host='127.0.0.1', port=8084)
        print("✅ GUI server created successfully")
        
        # Test component initialization by creating a mock handler
        from tarot_studio.gui.simple_server import TarotRequestHandler
        
        # Create a mock handler class for testing
        class MockHandler(TarotRequestHandler):
            def __init__(self):
                # Initialize components without calling parent constructor
                self._initialize_components()
        
        handler = MockHandler()
        
        # Test component initialization
        assert handler.deck is not None, "Deck should be initialized"
        assert handler.spread_manager is not None, "Spread manager should be initialized"
        assert handler.ollama_client is not None, "Ollama client should be initialized"
        assert handler.memory_store is not None, "Memory store should be initialized"
        assert handler.db is not None, "Database should be initialized"
        print("✅ GUI components initialized")
        
        # Test database operations
        cards = handler.db.get_all_cards()
        assert len(cards) > 0, "Should have cards in database"
        
        spreads = handler.db.get_all_spreads()
        assert len(spreads) > 0, "Should have spreads in database"
        print("✅ GUI database operations work")
        
        # Test deck operations
        initial_count = len(handler.deck.cards)
        card = handler.deck.draw_card()
        assert card is not None, "Should be able to draw a card"
        
        handler.deck.reset()
        assert len(handler.deck.cards) == initial_count, "Deck should be reset"
        print("✅ GUI deck operations work")
        
        # Test HTML content generation
        html_content = handler._get_html_content()
        assert len(html_content) > 1000, "HTML content should be substantial"
        assert '<html' in html_content, "Should contain HTML structure"
        assert 'Tarot Studio' in html_content, "Should contain app title"
        print("✅ HTML content generation works")
        
        print("✅ GUI Module tests passed")
        return True
        
    except Exception as e:
        print(f"❌ GUI Module test failed: {e}")
        return False


def test_data_integrity():
    """Test data integrity and consistency."""
    print("Testing Data Integrity...")
    
    try:
        # Test card data integrity
        with open('tarot_studio/deck/card_data.json', 'r') as f:
            card_data = json.load(f)
        
        assert 'deck_info' in card_data
        assert 'major_arcana' in card_data
        assert 'minor_arcana' in card_data
        
        # Check deck info
        deck_info = card_data['deck_info']
        assert deck_info['total_cards'] == 78
        assert deck_info['major_arcana_count'] == 22
        assert deck_info['minor_arcana_count'] == 56
        
        # Check major arcana
        major_arcana = card_data['major_arcana']
        assert len(major_arcana) == 22
        
        for card in major_arcana:
            assert 'id' in card
            assert 'name' in card
            assert 'arcana' in card
            assert card['arcana'] == 'major'
            assert 'upright_meaning' in card
            assert 'reversed_meaning' in card
        
        # Check minor arcana
        minor_arcana = card_data['minor_arcana']
        assert len(minor_arcana) == 4  # Four suits
        
        total_minor_cards = 0
        for suit, suit_data in minor_arcana.items():
            # Filter out metadata keys (element, theme) to get actual cards
            card_keys = [k for k in suit_data.keys() if k not in ['element', 'theme']]
            assert len(card_keys) == 14  # 10 numbered + 4 court cards
            total_minor_cards += len(card_keys)
            
            for rank in card_keys:
                card = suit_data[rank]
                # Minor arcana cards have keywords, upright_meaning, and reversed_meaning
                assert 'keywords' in card
                assert 'upright_meaning' in card
                assert 'reversed_meaning' in card
                assert isinstance(card['keywords'], list)
                assert len(card['keywords']) > 0
        
        assert total_minor_cards == 56
        
        print("✅ Data Integrity tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Data Integrity test failed: {e}")
        return False


def main():
    """Run all comprehensive tests."""
    print("Tarot Studio - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        test_deck_module,
        test_spreads_module,
        test_ai_module,
        test_influence_engine,
        test_database_module,
        test_gui_module,
        test_module_integration,
        test_file_structure,
        test_data_integrity
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"Comprehensive Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Tarot Studio project is working correctly.")
        print("\nCompleted Modules:")
        print("✅ Deck Module - 100% Complete")
        print("✅ Spreads Module - 100% Complete") 
        print("✅ AI Module - 100% Complete")
        print("✅ Influence Engine - 100% Complete")
        print("✅ Database Module - 100% Complete")
        print("✅ GUI Module - 100% Complete")
        print("✅ Core Integration - 100% Complete")
        print("\nReady for:")
        print("🔄 History Module completion")
        print("🔄 Final packaging and distribution")
        print("🔄 Production deployment")
        return True
    else:
        print("❌ Some tests failed.")
        print("Please review the failed tests and fix issues before proceeding.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)