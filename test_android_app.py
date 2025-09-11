#!/usr/bin/env python3
"""
Test script for Android Tarot Studio App
Tests the Kivy-based Android application components.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path
sys.path.append('.')

def test_android_app():
    """Test the Android app implementation."""
    print("Testing Android Tarot Studio App...")
    
    try:
        # Test main app import
        from android_tarot_studio.main import TarotStudioApp
        print("✅ Main app class imported successfully")
        
        # Test screen imports
        from android_tarot_studio.android_screens.splash_screen import SplashScreen
        from android_tarot_studio.android_screens.readings_screen import ReadingsScreen
        from android_tarot_studio.android_screens.chat_screen import ChatScreen
        from android_tarot_studio.android_screens.history_screen import HistoryScreen
        from android_tarot_studio.android_screens.settings_screen import SettingsScreen
        print("✅ All screen classes imported successfully")
        
        # Test app creation
        app = TarotStudioApp()
        print("✅ App instance created successfully")
        
        # Test component initialization
        app._initialize_components()
        assert app.deck is not None, "Deck should be initialized"
        assert app.spread_manager is not None, "Spread manager should be initialized"
        assert app.ollama_client is not None, "Ollama client should be initialized"
        assert app.memory_store is not None, "Memory store should be initialized"
        assert app.db is not None, "Database should be initialized"
        print("✅ All components initialized")
        
        # Test screen creation
        splash = SplashScreen()
        readings = ReadingsScreen()
        chat = ChatScreen()
        history = HistoryScreen()
        settings = SettingsScreen()
        print("✅ All screens created successfully")
        
        # Test app methods
        deck = app.get_deck()
        assert deck is not None, "Should be able to get deck"
        
        spread_manager = app.get_spread_manager()
        assert spread_manager is not None, "Should be able to get spread manager"
        
        ollama_client = app.get_ollama_client()
        assert ollama_client is not None, "Should be able to get Ollama client"
        
        memory_store = app.get_memory_store()
        assert memory_store is not None, "Should be able to get memory store"
        
        db = app.get_db()
        assert db is not None, "Should be able to get database"
        print("✅ App methods work correctly")
        
        # Test card drawing
        initial_count = len(deck.cards)
        drawn_cards = app.draw_cards(3)
        assert len(drawn_cards) == 3, "Should draw 3 cards"
        assert len(deck.cards) == initial_count - 3, "Deck count should decrease"
        
        # Test deck reset
        app.reset_deck()
        assert len(deck.cards) == initial_count, "Deck should be reset"
        print("✅ Card drawing and deck reset work")
        
        # Test database operations
        cards = db.get_all_cards()
        assert len(cards) > 0, "Should have cards in database"
        
        spreads = db.get_all_spreads()
        assert len(spreads) > 0, "Should have spreads in database"
        print("✅ Database operations work")
        
        # Test AI chat
        response = app.send_chat_message("Hello")
        assert isinstance(response, str), "Should return string response"
        assert len(response) > 0, "Response should not be empty"
        print("✅ AI chat works")
        
        print("\n🎉 All Android app tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Android app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_kivy_imports():
    """Test Kivy imports."""
    print("\nTesting Kivy imports...")
    
    try:
        from kivy.app import App
        from kivy.uix.screenmanager import ScreenManager
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput
        from kivy.uix.spinner import Spinner
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.popup import Popup
        from kivy.uix.switch import Switch
        from kivy.uix.progressbar import ProgressBar
        from kivy.uix.image import Image
        from kivy.clock import Clock
        from kivy.animation import Animation
        from kivy.core.window import Window
        from kivy.utils import platform
        print("✅ All Kivy imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Kivy import failed: {e}")
        print("Please install Kivy: pip install kivy")
        return False

def test_tarot_studio_integration():
    """Test integration with tarot_studio modules."""
    print("\nTesting Tarot Studio integration...")
    
    try:
        # Test importing tarot_studio modules
        from tarot_studio.deck.deck import Deck
        from tarot_studio.spreads.spread_manager import SpreadManager
        from tarot_studio.ai.ollama_client import OllamaClient
        from tarot_studio.ai.memory import MemoryStore
        from tarot_studio.db.simple_db import SimpleDB
        print("✅ Tarot Studio modules imported successfully")
        
        # Test creating instances
        deck = Deck.load_from_file('tarot_studio/deck/card_data.json')
        spread_manager = SpreadManager()
        ollama_client = OllamaClient()
        memory_store = MemoryStore()
        db = SimpleDB("test_android_db")
        print("✅ Tarot Studio instances created successfully")
        
        # Test basic functionality
        assert len(deck.cards) == 78, "Should have 78 cards"
        
        available_spreads = spread_manager.get_available_spreads()
        assert len(available_spreads) > 0, "Should have available spreads"
        
        assert hasattr(ollama_client, 'generate_reading_interpretation'), "Should have AI methods"
        assert hasattr(memory_store, 'store_memory'), "Should have memory methods"
        
        cards = db.get_all_cards()
        assert len(cards) > 0, "Should have cards in database"
        print("✅ Tarot Studio functionality works")
        
        return True
        
    except Exception as e:
        print(f"❌ Tarot Studio integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = test_kivy_imports()
    success2 = test_tarot_studio_integration()
    success3 = test_android_app()
    
    if success1 and success2 and success3:
        print("\n🎉 All Android app tests passed!")
        print("\nReady for Android build and deployment!")
        sys.exit(0)
    else:
        print("\n❌ Some Android app tests failed!")
        print("Please fix issues before building for Android.")
        sys.exit(1)