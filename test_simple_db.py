#!/usr/bin/env python3
"""
Test script for SimpleDB implementation.
"""

import sys
import os
sys.path.append('.')

def test_simple_db():
    """Test the SimpleDB implementation."""
    print("Testing SimpleDB implementation...")
    
    try:
        from tarot_studio.db.simple_db import SimpleDB
        
        # Create test database
        db = SimpleDB("test_simple_db")
        print("✅ SimpleDB created successfully")
        
        # Test card operations
        cards = db.get_all_cards()
        print(f"✅ Loaded {len(cards)} cards")
        
        if cards:
            first_card = cards[0]
            print(f"✅ First card: {first_card['name']}")
            
            # Test getting card by ID
            card_by_id = db.get_card(first_card['id'])
            assert card_by_id is not None
            print("✅ Get card by ID works")
        
        # Test spread operations
        spreads = db.get_all_spreads()
        print(f"✅ Loaded {len(spreads)} spreads")
        
        if spreads:
            first_spread = spreads[0]
            print(f"✅ First spread: {first_spread['name']}")
            
            # Test getting spread by ID
            spread_by_id = db.get_spread(first_spread['id'])
            assert spread_by_id is not None
            print("✅ Get spread by ID works")
        
        # Test reading operations
        reading_data = {
            'title': 'Test Reading',
            'spread_id': spreads[0]['id'] if spreads else 'single_card',
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
        
        # Test getting reading
        reading = db.get_reading(reading_id)
        assert reading is not None
        assert reading['title'] == 'Test Reading'
        print("✅ Retrieved reading successfully")
        
        # Test updating reading
        db.update_reading(reading_id, {'interpretation': 'Updated interpretation'})
        updated_reading = db.get_reading(reading_id)
        assert updated_reading['interpretation'] == 'Updated interpretation'
        print("✅ Updated reading successfully")
        
        # Test memory operations
        memory_id = db.store_memory(
            entity_type="person",
            entity_name="Test Person",
            description="A test person for memory testing",
            context="Testing memory functionality",
            importance_score=0.8
        )
        assert memory_id is not None
        print("✅ Stored memory successfully")
        
        # Test memory search
        search_results = db.search_memories("test", limit=5)
        assert len(search_results) > 0
        print("✅ Memory search works")
        
        # Test conversation operations
        conversation_id = db.create_conversation(
            title="Test Conversation",
            reading_id=reading_id,
            context="Testing conversation functionality"
        )
        assert conversation_id is not None
        print("✅ Created conversation successfully")
        
        # Test adding message
        success = db.add_message(conversation_id, "user", "Hello, this is a test message")
        assert success
        print("✅ Added message to conversation")
        
        # Test getting conversation
        conversation = db.get_conversation(conversation_id)
        assert conversation is not None
        assert len(conversation['messages']) == 1
        print("✅ Retrieved conversation successfully")
        
        # Test settings
        db.set_setting("test_key", "test_value")
        setting_value = db.get_setting("test_key")
        assert setting_value == "test_value"
        print("✅ Settings operations work")
        
        # Clean up
        db.delete_reading(reading_id)
        db.close()
        print("✅ Database closed successfully")
        
        print("\n🎉 All SimpleDB tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ SimpleDB test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_db()
    sys.exit(0 if success else 1)