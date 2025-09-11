#!/usr/bin/env python3
"""
Mock Kivy implementation for testing Android app without Kivy dependencies.
This allows testing the app structure and logic without requiring Kivy installation.
"""

import sys
from typing import Any, Dict, List, Optional, Callable

class MockWidget:
    """Mock widget base class."""
    
    def __init__(self, **kwargs):
        self.children = []
        self.parent = None
        self.size_hint_x = 1.0
        self.size_hint_y = 1.0
        self.height = 100
        self.width = 100
        self.text = kwargs.get('text', '')
        self.font_size = kwargs.get('font_size', 16)
        self.color = kwargs.get('color', (1, 1, 1, 1))
        self.background_color = kwargs.get('background_color', (0, 0, 0, 1))
        self.hint_text = kwargs.get('hint_text', '')
        self.multiline = kwargs.get('multiline', False)
        self.active = kwargs.get('active', False)
        self.values = kwargs.get('values', [])
        self.max = kwargs.get('max', 100)
        self.value = kwargs.get('value', 0)
        self.orientation = kwargs.get('orientation', 'horizontal')
        self.spacing = kwargs.get('spacing', 0)
        self.padding = kwargs.get('padding', 0)
        self.cols = kwargs.get('cols', 1)
        self.bold = kwargs.get('bold', False)
        self.halign = kwargs.get('halign', 'left')
        self.text_size = kwargs.get('text_size', (None, None))
        
        # Bind callbacks
        self._callbacks = {}
    
    def add_widget(self, widget):
        """Add a child widget."""
        widget.parent = self
        self.children.append(widget)
    
    def remove_widget(self, widget):
        """Remove a child widget."""
        if widget in self.children:
            widget.parent = None
            self.children.remove(widget)
    
    def clear_widgets(self):
        """Clear all child widgets."""
        for widget in self.children:
            widget.parent = None
        self.children.clear()
    
    def bind(self, **kwargs):
        """Bind callbacks to events."""
        for event, callback in kwargs.items():
            self._callbacks[event] = callback
    
    def _trigger_event(self, event, *args):
        """Trigger an event callback."""
        if event in self._callbacks:
            self._callbacks[event](*args)
    
    def setter(self, attr):
        """Create a setter for an attribute."""
        def setter_func(value):
            setattr(self, attr, value)
        return setter_func

class MockScreen(MockWidget):
    """Mock screen class."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', 'screen')

class MockApp:
    """Mock app class."""
    
    def __init__(self, **kwargs):
        self.screen_manager = None
        self.deck = None
        self.spread_manager = None
        self.ollama_client = None
        self.memory_store = None
        self.db = None
        self.current_reading = None
        self.drawn_cards = []
    
    def build(self):
        """Build the app."""
        return self.screen_manager
    
    def run(self):
        """Run the app."""
        print("Mock app running...")
    
    def get_deck(self):
        """Get the deck."""
        return self.deck
    
    def get_spread_manager(self):
        """Get the spread manager."""
        return self.spread_manager
    
    def get_ollama_client(self):
        """Get the Ollama client."""
        return self.ollama_client
    
    def get_memory_store(self):
        """Get the memory store."""
        return self.memory_store
    
    def get_db(self):
        """Get the database."""
        return self.db
    
    def draw_cards(self, num_cards):
        """Draw cards."""
        if not self.deck:
            return []
        
        drawn = []
        for _ in range(num_cards):
            card = self.deck.draw_card()
            if card:
                drawn.append(card)
        
        self.drawn_cards = drawn
        return drawn
    
    def reset_deck(self):
        """Reset the deck."""
        if self.deck:
            self.deck.reset()
            self.drawn_cards = []
    
    def save_reading(self, reading_data):
        """Save a reading."""
        if self.db:
            return self.db.create_reading(reading_data)
        return None
    
    def get_readings(self):
        """Get all readings."""
        if self.db:
            return self.db.get_all_readings()
        return []
    
    def send_chat_message(self, message, context=None):
        """Send a chat message."""
        return f"Mock AI response to: {message}"

class MockBoxLayout(MockWidget):
    """Mock box layout."""
    pass

class MockGridLayout(MockWidget):
    """Mock grid layout."""
    pass

class MockLabel(MockWidget):
    """Mock label widget."""
    pass

class MockButton(MockWidget):
    """Mock button widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disabled = kwargs.get('disabled', False)
    
    def _on_press(self, *args):
        """Handle button press."""
        self._trigger_event('on_press', *args)

class MockTextInput(MockWidget):
    """Mock text input widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get('text', '')
    
    def bind(self, **kwargs):
        """Bind text change events."""
        super().bind(**kwargs)
        if 'on_text_validate' in kwargs:
            self._text_validate_callback = kwargs['on_text_validate']

class MockSpinner(MockWidget):
    """Mock spinner widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get('text', '')
        self.values = kwargs.get('values', [])
    
    def bind(self, **kwargs):
        """Bind selection events."""
        super().bind(**kwargs)
        if 'text' in kwargs:
            self._text_callback = kwargs['text']

class MockScrollView(MockWidget):
    """Mock scroll view widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_y = 0
    
    def add_widget(self, widget):
        """Add widget to scroll view."""
        super().add_widget(widget)

class MockPopup(MockWidget):
    """Mock popup widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', '')
        self.content = kwargs.get('content', None)
        self.size_hint = kwargs.get('size_hint', (0.8, 0.4))
    
    def open(self):
        """Open the popup."""
        print(f"Mock popup opened: {self.title}")
    
    def dismiss(self):
        """Dismiss the popup."""
        print(f"Mock popup dismissed: {self.title}")

class MockSwitch(MockWidget):
    """Mock switch widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = kwargs.get('active', False)

class MockProgressBar(MockWidget):
    """Mock progress bar widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = kwargs.get('max', 100)
        self.value = kwargs.get('value', 0)

class MockImage(MockWidget):
    """Mock image widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = kwargs.get('source', '')

class MockScreenManager(MockWidget):
    """Mock screen manager."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = 'splash'
        self.screens = {}
    
    def add_widget(self, screen):
        """Add a screen."""
        self.screens[screen.name] = screen
        super().add_widget(screen)
    
    def remove_widget(self, screen):
        """Remove a screen."""
        if screen.name in self.screens:
            del self.screens[screen.name]
        super().remove_widget(screen)

class MockModalView(MockWidget):
    """Mock modal view widget."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', '')
        self.content = kwargs.get('content', None)
        self.size_hint = kwargs.get('size_hint', (0.8, 0.4))
    
    def open(self):
        """Open the modal view."""
        print(f"Mock modal view opened: {self.title}")
    
    def dismiss(self):
        """Dismiss the modal view."""
        print(f"Mock modal view dismissed: {self.title}")

class MockWindow:
    """Mock window class."""
    
    def __init__(self):
        self.size = (360, 640)
        self.clearcolor = (0.05, 0.07, 0.09, 1)
    
    @staticmethod
    def set_size(size):
        """Set window size."""
        pass
    
    @staticmethod
    def set_clearcolor(color):
        """Set clear color."""
        pass

class MockClock:
    """Mock clock class."""
    
    @staticmethod
    def schedule_once(callback, delay=0):
        """Schedule a callback."""
        print(f"Mock clock scheduled callback with delay {delay}")
    
    @staticmethod
    def schedule_interval(callback, interval):
        """Schedule an interval callback."""
        print(f"Mock clock scheduled interval callback with interval {interval}")

class MockAnimation:
    """Mock animation class."""
    
    def __init__(self, **kwargs):
        self.properties = kwargs
        self.duration = kwargs.get('duration', 1.0)
        self.target = None
    
    def start(self, widget):
        """Start animation on widget."""
        self.target = widget
        print(f"Mock animation started on {widget.__class__.__name__}")
    
    def stop(self):
        """Stop animation."""
        print("Mock animation stopped")
    
    def __add__(self, other):
        """Combine animations."""
        return MockAnimation(**{**self.properties, **other.properties})

class MockPlatform:
    """Mock platform class."""
    
    @staticmethod
    def get_platform():
        """Get platform name."""
        return 'android'

# Mock module setup
class MockModule:
    """Mock module for Kivy imports."""
    
    def __init__(self, name):
        self.name = name
    
    def __getattr__(self, name):
        """Get attribute from mock module."""
        if name == 'App':
            return MockApp
        elif name == 'Screen':
            return MockScreen
        elif name == 'BoxLayout':
            return MockBoxLayout
        elif name == 'GridLayout':
            return MockGridLayout
        elif name == 'Label':
            return MockLabel
        elif name == 'Button':
            return MockButton
        elif name == 'TextInput':
            return MockTextInput
        elif name == 'Spinner':
            return MockSpinner
        elif name == 'ScrollView':
            return MockScrollView
        elif name == 'Popup':
            return MockPopup
        elif name == 'Switch':
            return MockSwitch
        elif name == 'ProgressBar':
            return MockProgressBar
        elif name == 'Image':
            return MockImage
        elif name == 'ScreenManager':
            return MockScreenManager
        elif name == 'ModalView':
            return MockModalView
        elif name == 'Window':
            return MockWindow()
        elif name == 'Clock':
            return MockClock
        elif name == 'Animation':
            return MockAnimation
        elif name == 'platform':
            return MockPlatform.get_platform()
        else:
            return MockWidget

# Install mock modules
sys.modules['kivy'] = MockModule('kivy')
sys.modules['kivy.app'] = MockModule('kivy.app')
sys.modules['kivy.uix.screen'] = MockModule('kivy.uix.screen')
sys.modules['kivy.uix.boxlayout'] = MockModule('kivy.uix.boxlayout')
sys.modules['kivy.uix.gridlayout'] = MockModule('kivy.uix.gridlayout')
sys.modules['kivy.uix.label'] = MockModule('kivy.uix.label')
sys.modules['kivy.uix.button'] = MockModule('kivy.uix.button')
sys.modules['kivy.uix.textinput'] = MockModule('kivy.uix.textinput')
sys.modules['kivy.uix.spinner'] = MockModule('kivy.uix.spinner')
sys.modules['kivy.uix.scrollview'] = MockModule('kivy.uix.scrollview')
sys.modules['kivy.uix.popup'] = MockModule('kivy.uix.popup')
sys.modules['kivy.uix.switch'] = MockModule('kivy.uix.switch')
sys.modules['kivy.uix.progressbar'] = MockModule('kivy.uix.progressbar')
sys.modules['kivy.uix.image'] = MockModule('kivy.uix.image')
sys.modules['kivy.uix.screenmanager'] = MockModule('kivy.uix.screenmanager')
sys.modules['kivy.uix.modalview'] = MockModule('kivy.uix.modalview')
sys.modules['kivy.core.window'] = MockModule('kivy.core.window')
sys.modules['kivy.clock'] = MockModule('kivy.clock')
sys.modules['kivy.animation'] = MockModule('kivy.animation')
sys.modules['kivy.utils'] = MockModule('kivy.utils')

print("Mock Kivy modules installed successfully")