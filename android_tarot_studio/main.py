#!/usr/bin/env python3
"""
Tarot Studio Android Application
Main entry point for the Kivy-based Android app.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path to import tarot_studio modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.utils import platform

# Import our custom screens
from android_tarot_studio.android_screens.readings_screen import ReadingsScreen
from android_tarot_studio.android_screens.chat_screen import ChatScreen
from android_tarot_studio.android_screens.history_screen import HistoryScreen
from android_tarot_studio.android_screens.settings_screen import SettingsScreen
from android_tarot_studio.android_screens.splash_screen import SplashScreen

# Import tarot studio modules
from tarot_studio.deck.deck import Deck
from tarot_studio.spreads.spread_manager import SpreadManager
from tarot_studio.ai.ollama_client import OllamaClient
from tarot_studio.ai.memory import MemoryStore
from tarot_studio.db.simple_db import SimpleDB

class TarotStudioApp(App):
    """Main Tarot Studio Android Application."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize core components
        self.deck = None
        self.spread_manager = None
        self.ollama_client = None
        self.memory_store = None
        self.db = None
        
        # Screen manager
        self.screen_manager = None
        
        # App state
        self.current_reading = None
        self.drawn_cards = []
        
    def build(self):
        """Build the application UI."""
        # Set window properties for mobile
        if platform == 'android':
            # Android-specific window settings
            Window.clearcolor = (0.05, 0.07, 0.09, 1)  # Dark background
        else:
            # Desktop testing
            Window.size = (360, 640)  # Mobile-like size for testing
            Window.clearcolor = (0.05, 0.07, 0.09, 1)
        
        # Initialize core components
        self._initialize_components()
        
        # Create screen manager
        self.screen_manager = ScreenManager()
        
        # Add screens
        self.screen_manager.add_widget(SplashScreen(name='splash'))
        self.screen_manager.add_widget(ReadingsScreen(name='readings'))
        self.screen_manager.add_widget(ChatScreen(name='chat'))
        self.screen_manager.add_widget(HistoryScreen(name='history'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        
        # Start with splash screen
        self.screen_manager.current = 'splash'
        
        return self.screen_manager
    
    def _initialize_components(self):
        """Initialize all core components."""
        try:
            # Initialize deck
            self.deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
            print(f"✅ Deck loaded: {len(self.deck._original_order)} cards")
            
            # Initialize spread manager
            self.spread_manager = SpreadManager()
            print("✅ Spread manager initialized")
            
            # Initialize AI components
            self.ollama_client = OllamaClient()
            self.memory_store = MemoryStore()
            print("✅ AI components initialized")
            
            # Initialize database
            self.db = SimpleDB("tarot_studio_android_data")
            print("✅ Database initialized")
            
        except Exception as e:
            print(f"❌ Error initializing components: {e}")
            # Create fallback components
            self._create_fallback_components()
    
    def _create_fallback_components(self):
        """Create fallback components when initialization fails."""
        print("Creating fallback components...")
        
        # Create minimal deck
        self.deck = Deck()
        
        # Create minimal spread manager
        self.spread_manager = SpreadManager()
        
        # Create minimal AI components
        self.ollama_client = OllamaClient()
        self.memory_store = MemoryStore()
        
        # Create minimal database
        self.db = SimpleDB("tarot_studio_android_data")
    
    def on_start(self):
        """Called when the app starts."""
        # Move to main screen after splash
        if self.screen_manager:
            # Simulate loading time
            from kivy.clock import Clock
            Clock.schedule_once(self._finish_splash, 2.0)
    
    def _finish_splash(self, dt):
        """Finish splash screen and move to main app."""
        if self.screen_manager:
            self.screen_manager.current = 'readings'
    
    def get_deck(self):
        """Get the deck instance."""
        return self.deck
    
    def get_spread_manager(self):
        """Get the spread manager instance."""
        return self.spread_manager
    
    def get_ollama_client(self):
        """Get the Ollama client instance."""
        return self.ollama_client
    
    def get_memory_store(self):
        """Get the memory store instance."""
        return self.memory_store
    
    def get_db(self):
        """Get the database instance."""
        return self.db
    
    def draw_cards(self, num_cards):
        """Draw cards from the deck."""
        if not self.deck:
            return []
        
        drawn = []
        for _ in range(num_cards):
            if len(self.deck.cards) > 0:  # Check if deck has cards
                card = self.deck.draw_card()
                if card:
                    drawn.append(card)
            else:
                break  # Stop if deck is empty
        
        self.drawn_cards = drawn
        return drawn
    
    def reset_deck(self):
        """Reset the deck."""
        if self.deck:
            self.deck.reset()
            self.drawn_cards = []
    
    def save_reading(self, reading_data):
        """Save a reading to the database."""
        if self.db:
            return self.db.create_reading(reading_data)
        return None
    
    def get_readings(self):
        """Get all readings from the database."""
        if self.db:
            return self.db.get_all_readings()
        return []
    
    def send_chat_message(self, message, context=None):
        """Send a chat message to the AI."""
        if self.ollama_client:
            try:
                # For now, return a simple response
                # In a full implementation, this would call the AI
                return f"I received your message: '{message}'. This is a simplified response for the Android app."
            except Exception as e:
                return f"Sorry, I encountered an error: {str(e)}"
        return "AI service not available"

def main():
    """Main entry point."""
    app = TarotStudioApp()
    app.run()

if __name__ == '__main__':
    main()