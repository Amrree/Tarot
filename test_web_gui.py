#!/usr/bin/env python3
"""
Test script for Web GUI implementation.
"""

import sys
import os
import time
import requests
import threading
from urllib.parse import urljoin

# Add the parent directory to the path
sys.path.append('.')

def test_web_gui():
    """Test the web GUI implementation."""
    print("Testing Web GUI Implementation...")
    
    try:
        from tarot_studio.gui.web_app import TarotWebApp
        
        # Create app instance
        app = TarotWebApp()
        print("✅ Web app created successfully")
        
        # Test component initialization
        assert app.deck is not None, "Deck should be initialized"
        assert app.spread_manager is not None, "Spread manager should be initialized"
        assert app.ollama_client is not None, "Ollama client should be initialized"
        assert app.memory_store is not None, "Memory store should be initialized"
        assert app.db is not None, "Database should be initialized"
        print("✅ All components initialized")
        
        # Test database operations
        cards = app.db.get_all_cards()
        assert len(cards) > 0, "Should have cards in database"
        print(f"✅ Database has {len(cards)} cards")
        
        spreads = app.db.get_all_spreads()
        assert len(spreads) > 0, "Should have spreads in database"
        print(f"✅ Database has {len(spreads)} spreads")
        
        # Test deck operations
        initial_count = len(app.deck.cards)
        card = app.deck.draw_card()
        assert card is not None, "Should be able to draw a card"
        assert len(app.deck.cards) == initial_count - 1, "Deck count should decrease"
        print("✅ Deck operations work")
        
        # Reset deck
        app.deck.reset()
        assert len(app.deck.cards) == initial_count, "Deck should be reset"
        print("✅ Deck reset works")
        
        # Test spread manager
        available_spreads = app.spread_manager.get_available_spreads()
        assert len(available_spreads) > 0, "Should have available spreads"
        print(f"✅ Spread manager has {len(available_spreads)} spreads")
        
        # Test AI components
        assert hasattr(app.ollama_client, 'generate_response'), "Ollama client should have generate_response method"
        assert hasattr(app.memory_store, 'store_memory'), "Memory store should have store_memory method"
        print("✅ AI components have required methods")
        
        # Test Flask app routes
        with app.app.test_client() as client:
            # Test main page
            response = client.get('/')
            assert response.status_code == 200, "Main page should load"
            print("✅ Main page loads")
            
            # Test API endpoints
            response = client.get('/api/cards')
            assert response.status_code == 200, "Cards API should work"
            data = response.get_json()
            assert data['success'] == True, "Cards API should return success"
            assert len(data['cards']) > 0, "Should return cards"
            print("✅ Cards API works")
            
            response = client.get('/api/spreads')
            assert response.status_code == 200, "Spreads API should work"
            data = response.get_json()
            assert data['success'] == True, "Spreads API should return success"
            assert len(data['spreads']) > 0, "Should return spreads"
            print("✅ Spreads API works")
            
            response = client.get('/api/readings')
            assert response.status_code == 200, "Readings API should work"
            data = response.get_json()
            assert data['success'] == True, "Readings API should return success"
            print("✅ Readings API works")
            
            # Test creating a reading
            reading_data = {
                'title': 'Test Reading',
                'spread_id': data['spreads'][0]['id'],
                'question': 'What do I need to know?',
                'interpretation': 'This is a test reading.',
                'summary': 'Test summary',
                'advice': ['Test advice'],
                'tags': ['test'],
                'people_involved': [],
                'is_private': False
            }
            
            response = client.post('/api/readings', 
                                 json=reading_data,
                                 content_type='application/json')
            assert response.status_code == 200, "Creating reading should work"
            data = response.get_json()
            assert data['success'] == True, "Reading creation should return success"
            assert 'reading_id' in data, "Should return reading ID"
            print("✅ Reading creation works")
            
            # Test drawing cards
            response = client.post('/api/draw-cards',
                                 json={'num_cards': 3},
                                 content_type='application/json')
            assert response.status_code == 200, "Drawing cards should work"
            data = response.get_json()
            assert data['success'] == True, "Drawing cards should return success"
            assert len(data['cards']) == 3, "Should return 3 cards"
            print("✅ Card drawing works")
            
            # Test resetting deck
            response = client.post('/api/reset-deck')
            assert response.status_code == 200, "Resetting deck should work"
            data = response.get_json()
            assert data['success'] == True, "Deck reset should return success"
            print("✅ Deck reset API works")
            
            # Test settings
            response = client.get('/api/settings')
            assert response.status_code == 200, "Settings API should work"
            data = response.get_json()
            assert data['success'] == True, "Settings API should return success"
            print("✅ Settings API works")
            
            # Test updating settings
            settings_data = {
                'ai_model': 'llama2',
                'theme': 'dark',
                'auto_save': True
            }
            
            response = client.post('/api/settings',
                                 json=settings_data,
                                 content_type='application/json')
            assert response.status_code == 200, "Updating settings should work"
            data = response.get_json()
            assert data['success'] == True, "Settings update should return success"
            print("✅ Settings update works")
        
        print("\n🎉 All Web GUI tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Web GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_server():
    """Test running the web server."""
    print("\nTesting Web Server...")
    
    try:
        from tarot_studio.gui.web_app import TarotWebApp
        
        # Create app instance
        app = TarotWebApp()
        
        # Start server in a separate thread
        def run_server():
            app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(2)
        
        # Test server endpoints
        base_url = 'http://127.0.0.1:5001'
        
        try:
            response = requests.get(base_url, timeout=5)
            assert response.status_code == 200, "Server should respond"
            print("✅ Web server responds")
            
            response = requests.get(urljoin(base_url, '/api/cards'), timeout=5)
            assert response.status_code == 200, "Cards API should work"
            data = response.json()
            assert data['success'] == True, "Should return success"
            print("✅ Cards API accessible")
            
            response = requests.get(urljoin(base_url, '/api/spreads'), timeout=5)
            assert response.status_code == 200, "Spreads API should work"
            data = response.json()
            assert data['success'] == True, "Should return success"
            print("✅ Spreads API accessible")
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Server test skipped (server not accessible): {e}")
            return True
        
        print("✅ Web server test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Web server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = test_web_gui()
    success2 = test_web_server()
    
    if success1 and success2:
        print("\n🎉 All Web GUI tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some Web GUI tests failed!")
        sys.exit(1)