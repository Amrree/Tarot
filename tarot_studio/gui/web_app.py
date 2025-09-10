#!/usr/bin/env python3
"""
Web-based GUI for Tarot Studio application.
Fallback implementation for environments without PyObjC.
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename

# Add the parent directory to the path to import tarot_studio modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tarot_studio.deck.deck import Deck
from tarot_studio.spreads.spread_manager import SpreadManager
from tarot_studio.ai.ollama_client import OllamaClient
from tarot_studio.ai.memory import MemoryStore
from tarot_studio.db.simple_db import SimpleDB

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TarotWebApp:
    """Web-based Tarot Studio application."""
    
    def __init__(self):
        """Initialize the web application."""
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        self.app.secret_key = 'tarot_studio_secret_key_2024'
        
        # Initialize core components
        self.deck = None
        self.spread_manager = None
        self.ollama_client = None
        self.memory_store = None
        self.db = None
        
        # Initialize components
        self._initialize_components()
        
        # Set up routes
        self._setup_routes()
    
    def _initialize_components(self):
        """Initialize all core components."""
        try:
            # Initialize deck
            self.deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
            logger.info(f"Deck loaded: {len(self.deck._original_order)} cards")
            
            # Initialize spread manager
            self.spread_manager = SpreadManager()
            logger.info("Spread manager initialized")
            
            # Initialize AI components
            self.ollama_client = OllamaClient()
            self.memory_store = MemoryStore()
            logger.info("AI components initialized")
            
            # Initialize database
            self.db = SimpleDB("tarot_studio_data")
            logger.info("Database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            # Create fallback components
            self._create_fallback_components()
    
    def _create_fallback_components(self):
        """Create fallback components when initialization fails."""
        logger.info("Creating fallback components...")
        
        # Create minimal deck
        self.deck = Deck()
        
        # Create minimal spread manager
        self.spread_manager = SpreadManager()
        
        # Create minimal AI components
        self.ollama_client = OllamaClient()
        self.memory_store = MemoryStore()
        
        # Create minimal database
        self.db = SimpleDB("tarot_studio_data")
    
    def _setup_routes(self):
        """Set up Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main application page."""
            return render_template('index.html')
        
        @self.app.route('/api/cards')
        def get_cards():
            """Get all cards."""
            try:
                cards = self.db.get_all_cards()
                return jsonify({
                    'success': True,
                    'cards': cards,
                    'total': len(cards)
                })
            except Exception as e:
                logger.error(f"Error getting cards: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/cards/<card_id>')
        def get_card(card_id):
            """Get a specific card."""
            try:
                card = self.db.get_card(card_id)
                if card:
                    return jsonify({
                        'success': True,
                        'card': card
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Card not found'
                    })
            except Exception as e:
                logger.error(f"Error getting card {card_id}: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/spreads')
        def get_spreads():
            """Get all spreads."""
            try:
                spreads = self.db.get_all_spreads()
                return jsonify({
                    'success': True,
                    'spreads': spreads,
                    'total': len(spreads)
                })
            except Exception as e:
                logger.error(f"Error getting spreads: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/spreads/<spread_id>')
        def get_spread(spread_id):
            """Get a specific spread."""
            try:
                spread = self.db.get_spread(spread_id)
                if spread:
                    return jsonify({
                        'success': True,
                        'spread': spread
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Spread not found'
                    })
            except Exception as e:
                logger.error(f"Error getting spread {spread_id}: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/readings', methods=['GET'])
        def get_readings():
            """Get all readings."""
            try:
                readings = self.db.get_all_readings()
                return jsonify({
                    'success': True,
                    'readings': readings,
                    'total': len(readings)
                })
            except Exception as e:
                logger.error(f"Error getting readings: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/readings', methods=['POST'])
        def create_reading():
            """Create a new reading."""
            try:
                data = request.get_json()
                
                # Validate required fields
                required_fields = ['title', 'spread_id']
                for field in required_fields:
                    if field not in data:
                        return jsonify({
                            'success': False,
                            'error': f'Missing required field: {field}'
                        })
                
                # Create reading
                reading_id = self.db.create_reading(data)
                
                return jsonify({
                    'success': True,
                    'reading_id': reading_id,
                    'message': 'Reading created successfully'
                })
                
            except Exception as e:
                logger.error(f"Error creating reading: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/readings/<reading_id>')
        def get_reading(reading_id):
            """Get a specific reading."""
            try:
                reading = self.db.get_reading(reading_id)
                if reading:
                    return jsonify({
                        'success': True,
                        'reading': reading
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Reading not found'
                    })
            except Exception as e:
                logger.error(f"Error getting reading {reading_id}: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/draw-cards', methods=['POST'])
        def draw_cards():
            """Draw cards for a reading."""
            try:
                data = request.get_json()
                num_cards = data.get('num_cards', 1)
                
                # Draw cards from deck
                drawn_cards = []
                for _ in range(num_cards):
                    card = self.deck.draw_card()
                    if card:
                        drawn_cards.append({
                            'id': card.id,
                            'name': card.name,
                            'arcana': card.arcana.value,
                            'suit': card.suit.value if card.suit else None,
                            'orientation': 'upright',  # Default to upright
                            'keywords': card.keywords,
                            'upright_meaning': card.upright_meaning,
                            'reversed_meaning': card.reversed_meaning
                        })
                
                return jsonify({
                    'success': True,
                    'cards': drawn_cards,
                    'remaining': len(self.deck.cards)
                })
                
            except Exception as e:
                logger.error(f"Error drawing cards: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/reset-deck', methods=['POST'])
        def reset_deck():
            """Reset the deck."""
            try:
                self.deck.reset()
                return jsonify({
                    'success': True,
                    'message': 'Deck reset successfully',
                    'total_cards': len(self.deck.cards)
                })
            except Exception as e:
                logger.error(f"Error resetting deck: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            """Handle AI chat requests."""
            try:
                data = request.get_json()
                message = data.get('message', '')
                context = data.get('context', '')
                
                if not message:
                    return jsonify({
                        'success': False,
                        'error': 'Message is required'
                    })
                
                # Generate AI response
                response = self.ollama_client.generate_response(
                    message, 
                    context=context,
                    memory_store=self.memory_store
                )
                
                # Store conversation if we have a reading context
                reading_id = data.get('reading_id')
                if reading_id:
                    conversation_id = self.db.create_conversation(
                        title=f"Chat about reading {reading_id}",
                        reading_id=reading_id,
                        context=context
                    )
                    self.db.add_message(conversation_id, "user", message)
                    self.db.add_message(conversation_id, "assistant", response)
                
                return jsonify({
                    'success': True,
                    'response': response
                })
                
            except Exception as e:
                logger.error(f"Error in chat: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/memories', methods=['GET'])
        def get_memories():
            """Get memories."""
            try:
                query = request.args.get('query', '')
                limit = int(request.args.get('limit', 10))
                
                if query:
                    memories = self.db.search_memories(query, limit=limit)
                else:
                    memories = self.db.get_recent_memories(days=7, limit=limit)
                
                return jsonify({
                    'success': True,
                    'memories': memories,
                    'total': len(memories)
                })
                
            except Exception as e:
                logger.error(f"Error getting memories: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/settings', methods=['GET'])
        def get_settings():
            """Get application settings."""
            try:
                settings = self.db.settings
                return jsonify({
                    'success': True,
                    'settings': settings
                })
            except Exception as e:
                logger.error(f"Error getting settings: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
        
        @self.app.route('/api/settings', methods=['POST'])
        def update_settings():
            """Update application settings."""
            try:
                data = request.get_json()
                
                for key, value in data.items():
                    self.db.set_setting(key, value)
                
                return jsonify({
                    'success': True,
                    'message': 'Settings updated successfully'
                })
                
            except Exception as e:
                logger.error(f"Error updating settings: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
    
    def run(self, host='127.0.0.1', port=5000, debug=False):
        """Run the web application."""
        logger.info(f"Starting Tarot Studio Web App on http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Main entry point."""
    app = TarotWebApp()
    app.run(debug=True)

if __name__ == '__main__':
    main()