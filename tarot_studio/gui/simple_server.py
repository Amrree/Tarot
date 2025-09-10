#!/usr/bin/env python3
"""
Simple HTTP server for Tarot Studio GUI.
No external dependencies required.
"""

import os
import sys
import json
import logging
import http.server
import socketserver
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional

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

class TarotRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for Tarot Studio."""
    
    def __init__(self, *args, **kwargs):
        # Initialize components
        self.deck = None
        self.spread_manager = None
        self.ollama_client = None
        self.memory_store = None
        self.db = None
        
        self._initialize_components()
        super().__init__(*args, **kwargs)
    
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
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            if self.path == '/' or self.path == '/index.html':
                self._serve_main_page()
            elif self.path.startswith('/api/'):
                self._handle_api_request()
            else:
                # Try to serve static files
                super().do_GET()
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            self._send_error_response(500, str(e))
    
    def do_POST(self):
        """Handle POST requests."""
        try:
            if self.path.startswith('/api/'):
                self._handle_api_request()
            else:
                self._send_error_response(404, "Not Found")
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self._send_error_response(500, str(e))
    
    def _serve_main_page(self):
        """Serve the main HTML page."""
        html_content = self._get_html_content()
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html_content.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _handle_api_request(self):
        """Handle API requests."""
        path = self.path[5:]  # Remove '/api/' prefix
        
        if path == 'cards':
            self._handle_cards_api()
        elif path == 'spreads':
            self._handle_spreads_api()
        elif path == 'readings':
            self._handle_readings_api()
        elif path == 'draw-cards':
            self._handle_draw_cards_api()
        elif path == 'reset-deck':
            self._handle_reset_deck_api()
        elif path == 'chat':
            self._handle_chat_api()
        elif path == 'memories':
            self._handle_memories_api()
        elif path == 'settings':
            self._handle_settings_api()
        else:
            self._send_error_response(404, "API endpoint not found")
    
    def _handle_cards_api(self):
        """Handle cards API requests."""
        try:
            cards = self.db.get_all_cards()
            response = {
                'success': True,
                'cards': cards,
                'total': len(cards)
            }
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def _handle_spreads_api(self):
        """Handle spreads API requests."""
        try:
            spreads = self.db.get_all_spreads()
            response = {
                'success': True,
                'spreads': spreads,
                'total': len(spreads)
            }
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def _handle_readings_api(self):
        """Handle readings API requests."""
        try:
            readings = self.db.get_all_readings()
            response = {
                'success': True,
                'readings': readings,
                'total': len(readings)
            }
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def _handle_draw_cards_api(self):
        """Handle draw cards API requests."""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
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
                        'orientation': 'upright',
                        'keywords': card.keywords,
                        'upright_meaning': card.upright_meaning,
                        'reversed_meaning': card.reversed_meaning
                    })
            
            response = {
                'success': True,
                'cards': drawn_cards,
                'remaining': len(self.deck.cards)
            }
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def _handle_reset_deck_api(self):
        """Handle reset deck API requests."""
        try:
            self.deck.reset()
            response = {
                'success': True,
                'message': 'Deck reset successfully',
                'total_cards': len(self.deck.cards)
            }
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def _handle_chat_api(self):
        """Handle chat API requests."""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            message = data.get('message', '')
            context = data.get('context', '')
            
            if not message:
                self._send_error_response(400, "Message is required")
                return
            
            # Generate AI response (simplified)
            response_text = f"I received your message: '{message}'. This is a simplified response since Ollama may not be available."
            
            # Store conversation if we have a reading context
            reading_id = data.get('reading_id')
            if reading_id:
                conversation_id = self.db.create_conversation(
                    title=f"Chat about reading {reading_id}",
                    reading_id=reading_id,
                    context=context
                )
                self.db.add_message(conversation_id, "user", message)
                self.db.add_message(conversation_id, "assistant", response_text)
            
            response = {
                'success': True,
                'response': response_text
            }
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def _handle_memories_api(self):
        """Handle memories API requests."""
        try:
            # Parse query parameters
            query_params = urllib.parse.parse_qs(self.path.split('?')[1] if '?' in self.path else '')
            query = query_params.get('query', [''])[0]
            limit = int(query_params.get('limit', ['10'])[0])
            
            if query:
                memories = self.db.search_memories(query, limit=limit)
            else:
                memories = self.db.get_recent_memories(days=7, limit=limit)
            
            response = {
                'success': True,
                'memories': memories,
                'total': len(memories)
            }
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def _handle_settings_api(self):
        """Handle settings API requests."""
        try:
            if self.command == 'GET':
                settings = self.db.settings
                response = {
                    'success': True,
                    'settings': settings
                }
                self._send_json_response(response)
            elif self.command == 'POST':
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                for key, value in data.items():
                    self.db.set_setting(key, value)
                
                response = {
                    'success': True,
                    'message': 'Settings updated successfully'
                }
                self._send_json_response(response)
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def _send_json_response(self, data):
        """Send JSON response."""
        json_data = json.dumps(data, ensure_ascii=False)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(json_data.encode('utf-8'))))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def _send_error_response(self, status_code, message):
        """Send error response."""
        error_data = {
            'success': False,
            'error': message
        }
        json_data = json.dumps(error_data, ensure_ascii=False)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(json_data.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def _get_html_content(self):
        """Get the HTML content for the main page."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tarot Studio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            background-color: #0d1117;
            color: #c9d1d9;
            line-height: 1.6;
            overflow-x: hidden;
        }

        .container {
            display: flex;
            height: 100vh;
        }

        /* Sidebar */
        .sidebar {
            width: 250px;
            background-color: #161b22;
            border-right: 1px solid #30363d;
            padding: 20px;
            overflow-y: auto;
        }

        .logo {
            font-size: 18px;
            font-weight: bold;
            color: #58a6ff;
            margin-bottom: 30px;
            text-align: center;
            padding: 10px;
            border: 1px solid #30363d;
            border-radius: 4px;
        }

        .nav-item {
            display: block;
            padding: 12px 16px;
            color: #c9d1d9;
            text-decoration: none;
            border-radius: 4px;
            margin-bottom: 4px;
            transition: all 0.2s ease;
            cursor: pointer;
        }

        .nav-item:hover {
            background-color: #21262d;
            color: #58a6ff;
        }

        .nav-item.active {
            background-color: #1f6feb;
            color: #ffffff;
        }

        .nav-item i {
            margin-right: 8px;
            width: 16px;
            text-align: center;
        }

        /* Main Content */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .header {
            background-color: #161b22;
            border-bottom: 1px solid #30363d;
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            font-size: 20px;
            color: #c9d1d9;
        }

        .ai-status {
            font-size: 12px;
            color: #7d8590;
            padding: 4px 8px;
            background-color: #21262d;
            border-radius: 4px;
            border: 1px solid #30363d;
        }

        .ai-status.online {
            color: #3fb950;
            border-color: #3fb950;
        }

        .ai-status.offline {
            color: #f85149;
            border-color: #f85149;
        }

        .content {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
        }

        /* View Styles */
        .view {
            display: none;
        }

        .view.active {
            display: block;
        }

        /* Card Display */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .card:hover {
            border-color: #58a6ff;
            transform: translateY(-2px);
        }

        .card.selected {
            border-color: #1f6feb;
            background-color: #1f6feb20;
        }

        .card-name {
            font-weight: bold;
            color: #58a6ff;
            margin-bottom: 8px;
        }

        .card-keywords {
            font-size: 12px;
            color: #7d8590;
            margin-bottom: 8px;
        }

        .card-meaning {
            font-size: 12px;
            color: #c9d1d9;
            line-height: 1.4;
        }

        /* Spread Display */
        .spread-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 24px 0;
        }

        .spread-title {
            font-size: 18px;
            color: #58a6ff;
            margin-bottom: 16px;
        }

        .spread-positions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            width: 100%;
            max-width: 800px;
        }

        .spread-position {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .spread-position.empty {
            border-style: dashed;
            color: #7d8590;
        }

        .spread-position.filled {
            border-color: #58a6ff;
        }

        .position-name {
            font-weight: bold;
            color: #c9d1d9;
            margin-bottom: 8px;
        }

        .position-description {
            font-size: 12px;
            color: #7d8590;
            margin-bottom: 8px;
        }

        .position-card {
            font-size: 14px;
            color: #58a6ff;
        }

        /* Buttons */
        .btn {
            background-color: #1f6feb;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-family: inherit;
            font-size: 14px;
            transition: all 0.2s ease;
        }

        .btn:hover {
            background-color: #1f6febcc;
        }

        .btn:disabled {
            background-color: #30363d;
            color: #7d8590;
            cursor: not-allowed;
        }

        .btn-secondary {
            background-color: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
        }

        .btn-secondary:hover {
            background-color: #30363d;
        }

        /* Forms */
        .form-group {
            margin-bottom: 16px;
        }

        .form-label {
            display: block;
            margin-bottom: 4px;
            color: #c9d1d9;
            font-size: 14px;
        }

        .form-input {
            width: 100%;
            padding: 8px 12px;
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 4px;
            color: #c9d1d9;
            font-family: inherit;
            font-size: 14px;
        }

        .form-input:focus {
            outline: none;
            border-color: #58a6ff;
        }

        .form-textarea {
            resize: vertical;
            min-height: 100px;
        }

        /* Chat Interface */
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 16px;
            padding: 16px;
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
        }

        .chat-message {
            margin-bottom: 16px;
            padding: 12px;
            border-radius: 8px;
        }

        .chat-message.user {
            background-color: #1f6feb20;
            border-left: 3px solid #1f6feb;
        }

        .chat-message.assistant {
            background-color: #21262d;
            border-left: 3px solid #58a6ff;
        }

        .chat-message-header {
            font-size: 12px;
            color: #7d8590;
            margin-bottom: 4px;
        }

        .chat-message-content {
            color: #c9d1d9;
            line-height: 1.5;
        }

        .chat-input-container {
            display: flex;
            gap: 8px;
        }

        .chat-input {
            flex: 1;
        }

        /* Loading States */
        .loading {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #30363d;
            border-radius: 50%;
            border-top-color: #58a6ff;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Utility Classes */
        .hidden {
            display: none !important;
        }

        .text-center {
            text-align: center;
        }

        .text-muted {
            color: #7d8590;
        }

        .mb-16 {
            margin-bottom: 16px;
        }

        .mt-16 {
            margin-top: 16px;
        }

        .status-message {
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 16px;
        }

        .status-message.success {
            background-color: #1f6feb20;
            border: 1px solid #1f6feb;
            color: #58a6ff;
        }

        .status-message.error {
            background-color: #f8514920;
            border: 1px solid #f85149;
            color: #f85149;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="logo">🔮 Tarot Studio</div>
            
            <nav>
                <a href="#" class="nav-item active" data-view="readings">
                    <i>📖</i> Readings
                </a>
                <a href="#" class="nav-item" data-view="chat">
                    <i>💬</i> Chat
                </a>
                <a href="#" class="nav-item" data-view="history">
                    <i>📚</i> History
                </a>
                <a href="#" class="nav-item" data-view="settings">
                    <i>⚙️</i> Settings
                </a>
            </nav>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Header -->
            <div class="header">
                <h1 id="view-title">Readings</h1>
                <div class="ai-status offline" id="ai-status">AI: Offline</div>
            </div>

            <!-- Content Area -->
            <div class="content">
                <!-- Status Messages -->
                <div id="status-messages"></div>

                <!-- Readings View -->
                <div id="readings-view" class="view active">
                    <div class="form-group">
                        <label class="form-label">Select Spread</label>
                        <select class="form-input" id="spread-select">
                            <option value="">Loading spreads...</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Question (Optional)</label>
                        <textarea class="form-input form-textarea" id="question-input" placeholder="What guidance do you seek?"></textarea>
                    </div>

                    <div class="text-center mb-16">
                        <button class="btn" id="draw-cards-btn">Draw Cards</button>
                        <button class="btn btn-secondary" id="reset-deck-btn">Reset Deck</button>
                    </div>

                    <div id="spread-container" class="spread-container hidden">
                        <div class="spread-title" id="spread-title"></div>
                        <div class="spread-positions" id="spread-positions"></div>
                    </div>

                    <div class="mt-16">
                        <button class="btn" id="save-reading-btn" disabled>Save Reading</button>
                    </div>
                </div>

                <!-- Chat View -->
                <div id="chat-view" class="view">
                    <div class="chat-container">
                        <div class="chat-messages" id="chat-messages">
                            <div class="chat-message assistant">
                                <div class="chat-message-header">Tarot Assistant</div>
                                <div class="chat-message-content">Hello! I'm your Tarot assistant. Ask me about cards, spreads, or interpretations.</div>
                            </div>
                        </div>
                        
                        <div class="chat-input-container">
                            <input type="text" class="form-input chat-input" id="chat-input" placeholder="Ask me about tarot...">
                            <button class="btn" id="send-chat-btn">Send</button>
                        </div>
                    </div>
                </div>

                <!-- History View -->
                <div id="history-view" class="view">
                    <h2>Reading History</h2>
                    <div id="readings-list" class="mt-16">
                        <div class="text-center text-muted">Loading readings...</div>
                    </div>
                </div>

                <!-- Settings View -->
                <div id="settings-view" class="view">
                    <h2>Settings</h2>
                    
                    <div class="form-group">
                        <label class="form-label">AI Model</label>
                        <select class="form-input" id="ai-model-select">
                            <option value="llama2">Llama 2</option>
                            <option value="mistral">Mistral</option>
                            <option value="codellama">Code Llama</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Theme</label>
                        <select class="form-input" id="theme-select">
                            <option value="dark">Dark Terminal</option>
                            <option value="light">Light</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label">
                            <input type="checkbox" id="auto-save-checkbox"> Auto-save readings
                        </label>
                    </div>

                    <div class="form-group">
                        <label class="form-label">
                            <input type="checkbox" id="notifications-checkbox"> Enable notifications
                        </label>
                    </div>

                    <button class="btn" id="save-settings-btn">Save Settings</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global state
        let currentView = 'readings';
        let currentSpread = null;
        let drawnCards = [];
        let spreads = [];
        let readings = [];

        // Initialize the application
        document.addEventListener('DOMContentLoaded', function() {
            initializeApp();
        });

        async function initializeApp() {
            try {
                await loadSpreads();
                await loadReadings();
                await checkAIStatus();
                setupEventListeners();
                showStatusMessage('Tarot Studio initialized successfully!', 'success');
            } catch (error) {
                console.error('Error initializing app:', error);
                showStatusMessage('Failed to initialize application: ' + error.message, 'error');
            }
        }

        function setupEventListeners() {
            // Navigation
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    const view = this.dataset.view;
                    switchView(view);
                });
            });

            // Readings view
            document.getElementById('draw-cards-btn').addEventListener('click', drawCards);
            document.getElementById('reset-deck-btn').addEventListener('click', resetDeck);
            document.getElementById('save-reading-btn').addEventListener('click', saveReading);

            // Chat view
            document.getElementById('send-chat-btn').addEventListener('click', sendChatMessage);
            document.getElementById('chat-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendChatMessage();
                }
            });

            // Settings view
            document.getElementById('save-settings-btn').addEventListener('click', saveSettings);
        }

        function switchView(viewName) {
            // Update navigation
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            document.querySelector(`[data-view="${viewName}"]`).classList.add('active');

            // Update content
            document.querySelectorAll('.view').forEach(view => {
                view.classList.remove('active');
            });
            document.getElementById(`${viewName}-view`).classList.add('active');

            // Update title
            const titles = {
                'readings': 'Readings',
                'chat': 'Chat',
                'history': 'History',
                'settings': 'Settings'
            };
            document.getElementById('view-title').textContent = titles[viewName];

            currentView = viewName;
        }

        async function loadSpreads() {
            try {
                const response = await fetch('/api/spreads');
                const data = await response.json();
                
                if (data.success) {
                    spreads = data.spreads;
                    const select = document.getElementById('spread-select');
                    select.innerHTML = '<option value="">Select a spread...</option>';
                    
                    spreads.forEach(spread => {
                        const option = document.createElement('option');
                        option.value = spread.id;
                        option.textContent = `${spread.name} (${spread.positions.length} cards)`;
                        select.appendChild(option);
                    });

                    select.addEventListener('change', function() {
                        const spreadId = this.value;
                        if (spreadId) {
                            currentSpread = spreads.find(s => s.id === spreadId);
                            updateSpreadDisplay();
                        } else {
                            hideSpreadDisplay();
                        }
                    });
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error loading spreads:', error);
                showStatusMessage('Failed to load spreads: ' + error.message, 'error');
            }
        }

        async function loadReadings() {
            try {
                const response = await fetch('/api/readings');
                const data = await response.json();
                
                if (data.success) {
                    readings = data.readings;
                    updateReadingsList();
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error loading readings:', error);
                showStatusMessage('Failed to load readings: ' + error.message, 'error');
            }
        }

        async function checkAIStatus() {
            try {
                const response = await fetch('/api/settings');
                const data = await response.json();
                
                if (data.success) {
                    const aiStatus = document.getElementById('ai-status');
                    // For now, assume AI is offline if Ollama is not available
                    aiStatus.textContent = 'AI: Offline';
                    aiStatus.className = 'ai-status offline';
                }
            } catch (error) {
                console.error('Error checking AI status:', error);
            }
        }

        function updateSpreadDisplay() {
            if (!currentSpread) return;

            const container = document.getElementById('spread-container');
            const title = document.getElementById('spread-title');
            const positions = document.getElementById('spread-positions');

            title.textContent = currentSpread.name;
            positions.innerHTML = '';

            currentSpread.positions.forEach((position, index) => {
                const positionDiv = document.createElement('div');
                positionDiv.className = 'spread-position empty';
                positionDiv.innerHTML = `
                    <div class="position-name">${position.name}</div>
                    <div class="position-description">${position.description}</div>
                    <div class="position-card">No card drawn</div>
                `;
                positions.appendChild(positionDiv);
            });

            container.classList.remove('hidden');
        }

        function hideSpreadDisplay() {
            document.getElementById('spread-container').classList.add('hidden');
            drawnCards = [];
        }

        async function drawCards() {
            if (!currentSpread) {
                showStatusMessage('Please select a spread first', 'error');
                return;
            }

            const numCards = currentSpread.positions.length;
            const button = document.getElementById('draw-cards-btn');
            button.disabled = true;
            button.innerHTML = '<span class="loading"></span> Drawing...';

            try {
                const response = await fetch('/api/draw-cards', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ num_cards: numCards })
                });

                const data = await response.json();

                if (data.success) {
                    drawnCards = data.cards;
                    updateSpreadWithCards();
                    document.getElementById('save-reading-btn').disabled = false;
                    showStatusMessage(`Drew ${drawnCards.length} cards successfully!`, 'success');
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error drawing cards:', error);
                showStatusMessage('Failed to draw cards: ' + error.message, 'error');
            } finally {
                button.disabled = false;
                button.textContent = 'Draw Cards';
            }
        }

        function updateSpreadWithCards() {
            const positions = document.querySelectorAll('.spread-position');
            
            positions.forEach((position, index) => {
                if (index < drawnCards.length) {
                    const card = drawnCards[index];
                    position.className = 'spread-position filled';
                    position.innerHTML = `
                        <div class="position-name">${currentSpread.positions[index].name}</div>
                        <div class="position-description">${currentSpread.positions[index].description}</div>
                        <div class="position-card">${card.name}</div>
                    `;
                }
            });
        }

        async function resetDeck() {
            try {
                const response = await fetch('/api/reset-deck', {
                    method: 'POST'
                });

                const data = await response.json();

                if (data.success) {
                    hideSpreadDisplay();
                    document.getElementById('save-reading-btn').disabled = true;
                    showStatusMessage('Deck reset successfully!', 'success');
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error resetting deck:', error);
                showStatusMessage('Failed to reset deck: ' + error.message, 'error');
            }
        }

        async function saveReading() {
            if (!currentSpread || drawnCards.length === 0) {
                showStatusMessage('Please draw cards first', 'error');
                return;
            }

            const question = document.getElementById('question-input').value;
            const readingData = {
                title: `${currentSpread.name} Reading`,
                spread_id: currentSpread.id,
                question: question,
                interpretation: 'Interpretation will be added here...',
                summary: 'Reading summary...',
                advice: ['Advice item 1', 'Advice item 2'],
                tags: ['web-reading'],
                people_involved: [],
                is_private: false
            };

            try {
                const response = await fetch('/api/readings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(readingData)
                });

                const data = await response.json();

                if (data.success) {
                    showStatusMessage('Reading saved successfully!', 'success');
                    await loadReadings();
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error saving reading:', error);
                showStatusMessage('Failed to save reading: ' + error.message, 'error');
            }
        }

        async function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();

            if (!message) return;

            // Add user message to chat
            addChatMessage('user', message);
            input.value = '';

            // Send to AI
            const button = document.getElementById('send-chat-btn');
            button.disabled = true;
            button.textContent = 'Sending...';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();

                if (data.success) {
                    addChatMessage('assistant', data.response);
                } else {
                    addChatMessage('assistant', 'Sorry, I encountered an error. Please try again.');
                }
            } catch (error) {
                console.error('Error sending chat message:', error);
                addChatMessage('assistant', 'Sorry, I encountered an error. Please try again.');
            } finally {
                button.disabled = false;
                button.textContent = 'Send';
            }
        }

        function addChatMessage(role, content) {
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${role}`;
            
            const header = role === 'user' ? 'You' : 'Tarot Assistant';
            messageDiv.innerHTML = `
                <div class="chat-message-header">${header}</div>
                <div class="chat-message-content">${content}</div>
            `;
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function updateReadingsList() {
            const container = document.getElementById('readings-list');
            
            if (readings.length === 0) {
                container.innerHTML = '<div class="text-center text-muted">No readings yet</div>';
                return;
            }

            container.innerHTML = '';
            readings.forEach(reading => {
                const readingDiv = document.createElement('div');
                readingDiv.className = 'card';
                readingDiv.innerHTML = `
                    <div class="card-name">${reading.title}</div>
                    <div class="card-keywords">${reading.spread_id}</div>
                    <div class="card-meaning">${reading.question || 'No question'}</div>
                `;
                container.appendChild(readingDiv);
            });
        }

        async function saveSettings() {
            const settings = {
                ai_model: document.getElementById('ai-model-select').value,
                theme: document.getElementById('theme-select').value,
                auto_save: document.getElementById('auto-save-checkbox').checked,
                notifications: document.getElementById('notifications-checkbox').checked
            };

            try {
                const response = await fetch('/api/settings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(settings)
                });

                const data = await response.json();

                if (data.success) {
                    showStatusMessage('Settings saved successfully!', 'success');
                } else {
                    throw new Error(data.error);
                }
            } catch (error) {
                console.error('Error saving settings:', error);
                showStatusMessage('Failed to save settings: ' + error.message, 'error');
            }
        }

        function showStatusMessage(message, type) {
            const container = document.getElementById('status-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `status-message ${type}`;
            messageDiv.textContent = message;
            
            container.appendChild(messageDiv);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.parentNode.removeChild(messageDiv);
                }
            }, 5000);
        }
    </script>
</body>
</html>'''

class TarotServer:
    """Simple HTTP server for Tarot Studio."""
    
    def __init__(self, host='127.0.0.1', port=8080):
        """Initialize the server."""
        self.host = host
        self.port = port
        self.server = None
    
    def start(self):
        """Start the server."""
        try:
            self.server = socketserver.TCPServer((self.host, self.port), TarotRequestHandler)
            logger.info(f"Tarot Studio server starting on http://{self.host}:{self.port}")
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")
    
    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()

def main():
    """Main entry point."""
    server = TarotServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop()

if __name__ == '__main__':
    main()