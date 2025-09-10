#!/usr/bin/env python3
"""
Test script for Database Module (SimpleDB implementation).
"""

import sys
import os
sys.path.append('.')

def test_db_module():
    """Test the Database Module implementation."""
    print("Testing Database Module...")
    
    try:
        from tarot_studio.db.simple_db import SimpleDB
        
        # Create test database
        db = SimpleDB("test_db_module")
        print("✅ Database created successfully")
        
        # Test card operations
        cards = db.get_all_cards()
        assert len(cards) == 78, f"Expected 78 cards, got {len(cards)}"
        print(f"✅ Loaded {len(cards)} cards")
        
        # Test major and minor arcana
        major_cards = db.get_cards_by_arcana('major')
        minor_cards = db.get_cards_by_arcana('minor')
        assert len(major_cards) == 22, f"Expected 22 major arcana, got {len(major_cards)}"
        assert len(minor_cards) == 56, f"Expected 56 minor arcana, got {len(minor_cards)}"
        print("✅ Major and minor arcana counts correct")
        
        # Test card by ID
        first_card = cards[0]
        card_by_id = db.get_card(first_card['id'])
        assert card_by_id is not None
        assert card_by_id['name'] == first_card['name']
        print("✅ Get card by ID works")
        
        # Test cards by suit
        wands_cards = db.get_cards_by_suit('wands')
        assert len(wands_cards) == 14, f"Expected 14 wands cards, got {len(wands_cards)}"
        print("✅ Get cards by suit works")
        
        # Test spread operations
        spreads = db.get_all_spreads()
        assert len(spreads) >= 3, f"Expected at least 3 spreads, got {len(spreads)}"
        print(f"✅ Loaded {len(spreads)} spreads")
        
        # Test spread by ID
        first_spread = spreads[0]
        spread_by_id = db.get_spread(first_spread['id'])
        assert spread_by_id is not None
        assert spread_by_id['name'] == first_spread['name']
        print("✅ Get spread by ID works")
        
        # Test creating custom spread
        custom_spread_data = {
            'name': 'Test Custom Spread',
            'description': 'A test spread for testing',
            'positions': [
                {'name': 'Position 1', 'description': 'First position'},
                {'name': 'Position 2', 'description': 'Second position'}
            ],
            'is_custom': True,
            'created_by': 'test_user'
        }
        
        custom_spread_id = db.create_spread(custom_spread_data)
        assert custom_spread_id is not None
        custom_spread = db.get_spread(custom_spread_id)
        assert custom_spread['name'] == 'Test Custom Spread'
        print("✅ Create custom spread works")
        
        # Test reading operations
        reading_data = {
            'title': 'Test Reading',
            'spread_id': first_spread['id'],
            'question': 'What do I need to know?',
            'interpretation': 'This is a test reading.',
            'summary': 'Test summary',
            'advice': ['Test advice 1', 'Test advice 2'],
            'tags': ['test'],
            'people_involved': [],
            'is_private': False
        }
        
        reading_id = db.create_reading(reading_data)
        assert reading_id is not None
        print("✅ Created reading successfully")
        
        # Test getting and updating reading
        reading = db.get_reading(reading_id)
        assert reading is not None
        assert reading['title'] == 'Test Reading'
        
        db.update_reading(reading_id, {'interpretation': 'Updated interpretation'})
        updated_reading = db.get_reading(reading_id)
        assert updated_reading['interpretation'] == 'Updated interpretation'
        print("✅ Reading operations work")
        
        # Test memory operations
        memory_id = db.store_memory(
            entity_type="person",
            entity_name="Test Person",
            description="A test person for memory testing",
            context="Testing memory functionality",
            importance_score=0.8
        )
        assert memory_id is not None
        
        # Test memory search
        search_results = db.search_memories("test", limit=5)
        assert len(search_results) > 0
        
        # Test recent memories
        recent_memories = db.get_recent_memories(days=1, limit=10)
        assert len(recent_memories) >= 1
        print("✅ Memory operations work")
        
        # Test conversation operations
        conversation_id = db.create_conversation(
            title="Test Conversation",
            reading_id=reading_id,
            context="Testing conversation functionality"
        )
        assert conversation_id is not None
        
        # Test adding messages
        success = db.add_message(conversation_id, "user", "Hello, this is a test message")
        assert success
        
        success = db.add_message(conversation_id, "assistant", "This is a test response")
        assert success
        
        # Test getting conversation
        conversation = db.get_conversation(conversation_id)
        assert conversation is not None
        assert len(conversation['messages']) == 2
        print("✅ Conversation operations work")
        
        # Test settings
        db.set_setting("test_key", "test_value")
        setting_value = db.get_setting("test_key")
        assert setting_value == "test_value"
        
        db.set_setting("ai_model", "llama2")
        ai_model = db.get_setting("ai_model")
        assert ai_model == "llama2"
        print("✅ Settings operations work")
        
        # Test data persistence
        db.close()
        
        # Reopen database and verify data persistence
        db2 = SimpleDB("test_db_module")
        assert len(db2.get_all_cards()) == 78
        assert len(db2.get_all_spreads()) >= 4  # 3 default + 1 custom
        assert len(db2.get_all_readings()) == 1
        assert len(db2.get_all_conversations()) == 1
        assert db2.get_setting("test_key") == "test_value"
        print("✅ Data persistence works")
        
        db2.close()
        print("\n🎉 All Database Module tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database Module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_db_module()
    sys.exit(0 if success else 1)