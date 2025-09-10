#!/usr/bin/env python3
"""
Example usage of the Database Module (SimpleDB implementation).
"""

import sys
import os
sys.path.append('.')

from tarot_studio.db.simple_db import SimpleDB

def main():
    """Demonstrate database module usage."""
    print("Tarot Studio - Database Module Example")
    print("=" * 50)
    
    # Initialize database
    print("\n1. Initializing Database...")
    db = SimpleDB("example_tarot_data")
    print("✅ Database initialized")
    
    # Explore cards
    print("\n2. Exploring Cards...")
    cards = db.get_all_cards()
    print(f"📚 Total cards: {len(cards)}")
    
    # Show major arcana
    major_cards = db.get_cards_by_arcana('major')
    print(f"🔮 Major Arcana: {len(major_cards)} cards")
    for card in major_cards[:3]:
        print(f"   - {card['name']}: {', '.join(card['keywords'][:3])}")
    
    # Show minor arcana by suit
    print(f"\n🃏 Minor Arcana by suit:")
    for suit in ['wands', 'cups', 'swords', 'pentacles']:
        suit_cards = db.get_cards_by_suit(suit)
        print(f"   - {suit.title()}: {len(suit_cards)} cards")
    
    # Explore spreads
    print("\n3. Exploring Spreads...")
    spreads = db.get_all_spreads()
    print(f"📋 Available spreads: {len(spreads)}")
    for spread in spreads:
        print(f"   - {spread['name']}: {len(spread['positions'])} positions")
        print(f"     {spread['description']}")
    
    # Create a reading
    print("\n4. Creating a Reading...")
    reading_data = {
        'title': 'Example Reading',
        'spread_id': 'three_card',
        'question': 'What guidance do I need for today?',
        'interpretation': 'The cards suggest focusing on new opportunities and trusting your intuition.',
        'summary': 'A day of new beginnings and intuitive guidance.',
        'advice': [
            'Trust your instincts',
            'Be open to new opportunities',
            'Take action on your ideas'
        ],
        'tags': ['daily', 'guidance', 'new beginnings'],
        'people_involved': [],
        'is_private': False
    }
    
    reading_id = db.create_reading(reading_data)
    print(f"✅ Created reading: {reading_id}")
    
    # Retrieve and display reading
    reading = db.get_reading(reading_id)
    print(f"\n📖 Reading Details:")
    print(f"   Title: {reading['title']}")
    print(f"   Question: {reading['question']}")
    print(f"   Interpretation: {reading['interpretation']}")
    print(f"   Advice: {', '.join(reading['advice'])}")
    
    # Store memories
    print("\n5. Storing Memories...")
    memories = [
        {
            'entity_type': 'concept',
            'entity_name': 'new opportunities',
            'description': 'Focus on emerging possibilities and chances for growth',
            'context': 'Daily reading guidance',
            'importance_score': 0.8
        },
        {
            'entity_type': 'concept',
            'entity_name': 'intuition',
            'description': 'Trusting inner wisdom and gut feelings',
            'context': 'Reading advice',
            'importance_score': 0.9
        },
        {
            'entity_type': 'person',
            'entity_name': 'Tarot Reader',
            'description': 'The person conducting this reading',
            'context': 'Reading session',
            'importance_score': 0.6
        }
    ]
    
    for memory_data in memories:
        memory_id = db.store_memory(**memory_data)
        print(f"✅ Stored memory: {memory_data['entity_name']}")
    
    # Search memories
    print("\n6. Searching Memories...")
    search_results = db.search_memories("opportunities", limit=3)
    print(f"🔍 Found {len(search_results)} memories about 'opportunities':")
    for memory in search_results:
        print(f"   - {memory['entity_name']}: {memory['description']}")
    
    # Create conversation
    print("\n7. Creating Conversation...")
    conversation_id = db.create_conversation(
        title="Reading Discussion",
        reading_id=reading_id,
        context="Discussing the reading interpretation and guidance"
    )
    print(f"✅ Created conversation: {conversation_id}")
    
    # Add conversation messages
    messages = [
        ("user", "What does the Three of Wands mean in this context?"),
        ("assistant", "The Three of Wands represents expansion and looking toward the future. In your reading, it suggests that new opportunities are on the horizon and you should be prepared to take action."),
        ("user", "How can I best prepare for these opportunities?"),
        ("assistant", "The cards suggest trusting your intuition and being open to new experiences. Focus on developing your skills and maintaining a positive mindset.")
    ]
    
    for role, content in messages:
        db.add_message(conversation_id, role, content)
        print(f"💬 Added {role} message")
    
    # Retrieve conversation
    conversation = db.get_conversation(conversation_id)
    print(f"\n📝 Conversation: {conversation['title']}")
    print(f"   Messages: {len(conversation['messages'])}")
    for message in conversation['messages']:
        print(f"   {message['role'].title()}: {message['content'][:50]}...")
    
    # Settings management
    print("\n8. Managing Settings...")
    settings = [
        ("ai_model", "llama2"),
        ("theme", "dark"),
        ("auto_save", True),
        ("notifications", False)
    ]
    
    for key, value in settings:
        db.set_setting(key, value)
        print(f"⚙️  Set {key} = {value}")
    
    # Retrieve settings
    print(f"\n📊 Current Settings:")
    for key, _ in settings:
        value = db.get_setting(key)
        print(f"   {key}: {value}")
    
    # Create custom spread
    print("\n9. Creating Custom Spread...")
    custom_spread_data = {
        'name': 'Decision Making Spread',
        'description': 'A spread to help with important decisions',
        'positions': [
            {'name': 'Current Situation', 'description': 'Where you are now'},
            {'name': 'Option A', 'description': 'First choice or path'},
            {'name': 'Option B', 'description': 'Second choice or path'},
            {'name': 'Outcome A', 'description': 'Likely result of Option A'},
            {'name': 'Outcome B', 'description': 'Likely result of Option B'},
            {'name': 'Guidance', 'description': 'What the universe suggests'}
        ],
        'is_custom': True,
        'created_by': 'example_user'
    }
    
    custom_spread_id = db.create_spread(custom_spread_data)
    print(f"✅ Created custom spread: {custom_spread_data['name']}")
    
    # Show all spreads
    all_spreads = db.get_all_spreads()
    print(f"\n📋 All Spreads ({len(all_spreads)}):")
    for spread in all_spreads:
        custom_marker = " (Custom)" if spread['is_custom'] else ""
        print(f"   - {spread['name']}{custom_marker}: {len(spread['positions'])} positions")
    
    # Data persistence demonstration
    print("\n10. Testing Data Persistence...")
    db.close()
    print("💾 Database closed and data saved")
    
    # Reopen and verify data
    db2 = SimpleDB("example_tarot_data")
    print("🔄 Database reopened")
    
    # Verify data persistence
    assert len(db2.get_all_cards()) == len(cards)
    assert len(db2.get_all_spreads()) == len(all_spreads)
    assert len(db2.get_all_readings()) == 1
    assert len(db2.get_all_conversations()) == 1
    assert db2.get_setting("ai_model") == "llama2"
    
    print("✅ All data persisted correctly")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Database Summary:")
    print(f"   Cards: {len(db2.get_all_cards())}")
    print(f"   Spreads: {len(db2.get_all_spreads())}")
    print(f"   Readings: {len(db2.get_all_readings())}")
    print(f"   Conversations: {len(db2.get_all_conversations())}")
    print(f"   Memories: {len(db2.memories)}")
    print(f"   Settings: {len(db2.settings)}")
    
    db2.close()
    print("\n🎉 Database module example completed successfully!")

if __name__ == "__main__":
    main()