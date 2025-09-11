#!/usr/bin/env python3
"""
Chat Screen for Tarot Studio Android App
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock

class ChatScreen(Screen):
    """Chat screen for AI conversation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_messages = []
        self._build_ui()
    
    def _build_ui(self):
        """Build the chat screen UI."""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        
        # Header
        header_layout = self._create_header()
        main_layout.add_widget(header_layout)
        
        # Chat messages area
        chat_area = self._create_chat_area()
        main_layout.add_widget(chat_area)
        
        # Input area
        input_area = self._create_input_area()
        main_layout.add_widget(input_area)
        
        # Bottom navigation
        bottom_nav = self._create_bottom_navigation()
        main_layout.add_widget(bottom_nav)
        
        self.add_widget(main_layout)
        
        # Add welcome message
        self._add_welcome_message()
    
    def _create_header(self):
        """Create the header section."""
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            spacing=10
        )
        
        # Back button
        back_btn = Button(
            text='←',
            font_size=24,
            size_hint_x=0.2,
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        back_btn.bind(on_press=self._go_back)
        
        # Title
        title_label = Label(
            text='💬 Tarot Chat',
            font_size=24,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_x=0.6
        )
        
        # Clear button
        clear_btn = Button(
            text='🗑️',
            font_size=20,
            size_hint_x=0.2,
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        clear_btn.bind(on_press=self._clear_chat)
        
        header_layout.add_widget(back_btn)
        header_layout.add_widget(title_label)
        header_layout.add_widget(clear_btn)
        
        return header_layout
    
    def _create_chat_area(self):
        """Create the chat messages area."""
        chat_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.7,
            spacing=10
        )
        
        # Scrollable chat container
        self.chat_scroll = ScrollView(
            size_hint_y=1.0
        )
        
        self.chat_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=10
        )
        self.chat_container.bind(minimum_height=self.chat_container.setter('height'))
        
        self.chat_scroll.add_widget(self.chat_container)
        chat_layout.add_widget(self.chat_scroll)
        
        return chat_layout
    
    def _create_input_area(self):
        """Create the input area."""
        input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.15,
            spacing=10
        )
        
        # Text input
        self.message_input = TextInput(
            hint_text='Ask me about tarot...',
            multiline=False,
            size_hint_x=0.8,
            background_color=(0.2, 0.2, 0.2, 1.0),
            foreground_color=(0.8, 0.8, 0.8, 1.0)
        )
        self.message_input.bind(on_text_validate=self._send_message)
        
        # Send button
        send_btn = Button(
            text='Send',
            font_size=16,
            size_hint_x=0.2,
            background_color=(0.12, 0.44, 0.92, 1.0)
        )
        send_btn.bind(on_press=self._send_message)
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(send_btn)
        
        return input_layout
    
    def _create_bottom_navigation(self):
        """Create the bottom navigation."""
        nav_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.05,
            spacing=5
        )
        
        # Navigation buttons
        nav_buttons = [
            ('📖', 'readings'),
            ('💬', 'chat'),
            ('📚', 'history'),
            ('⚙️', 'settings')
        ]
        
        for icon, name in nav_buttons:
            btn = Button(
                text=icon,
                font_size=20,
                background_color=(0.2, 0.2, 0.2, 1.0)
            )
            btn.bind(on_press=lambda x, screen=name: self._navigate_to_screen(screen))
            nav_layout.add_widget(btn)
        
        return nav_layout
    
    def _add_welcome_message(self):
        """Add welcome message to chat."""
        self._add_message('assistant', 'Hello! I\'m your Tarot assistant. Ask me about cards, spreads, or interpretations.')
    
    def _add_message(self, sender, message):
        """Add a message to the chat."""
        # Add to chat messages list
        self.chat_messages.append({'sender': sender, 'message': message})
        
        # Create message layout
        message_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=10,
            padding=10
        )
        
        # Sender indicator
        if sender == 'user':
            sender_color = (0.12, 0.44, 0.92, 1.0)  # Blue
            sender_text = 'You'
            alignment = 'right'
        else:
            sender_color = (0.35, 0.65, 1.0, 1.0)  # Light blue
            sender_text = 'Assistant'
            alignment = 'left'
        
        # Message content
        message_content = BoxLayout(
            orientation='vertical',
            size_hint_x=0.9
        )
        
        # Sender label
        sender_label = Label(
            text=sender_text,
            font_size=12,
            color=sender_color,
            size_hint_y=0.3,
            halign=alignment
        )
        
        # Message text
        message_label = Label(
            text=message,
            font_size=16,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_y=0.7,
            text_size=(None, None),
            halign=alignment
        )
        
        message_content.add_widget(sender_label)
        message_content.add_widget(message_label)
        
        # Add spacer for alignment
        if sender == 'user':
            spacer = Label(size_hint_x=0.1)
            message_layout.add_widget(spacer)
            message_layout.add_widget(message_content)
        else:
            message_layout.add_widget(message_content)
            spacer = Label(size_hint_x=0.1)
            message_layout.add_widget(spacer)
        
        self.chat_container.add_widget(message_layout)
        
        # Scroll to bottom
        Clock.schedule_once(self._scroll_to_bottom, 0.1)
    
    def _send_message(self, instance):
        """Send a message to the AI."""
        message = self.message_input.text.strip()
        if not message:
            return
        
        # Add user message
        self._add_message('user', message)
        
        # Clear input
        self.message_input.text = ''
        
        # Get AI response
        try:
            app = self.parent.parent.parent.parent
        except AttributeError:
            app = None
        
        if app and hasattr(app, 'send_chat_message'):
            response = app.send_chat_message(message)
            self._add_message('assistant', response)
        else:
            self._add_message('assistant', 'AI service not available')
    
    def _scroll_to_bottom(self, dt):
        """Scroll chat to bottom."""
        if self.chat_scroll:
            self.chat_scroll.scroll_y = 0
    
    def _clear_chat(self, instance):
        """Clear the chat history."""
        self.chat_container.clear_widgets()
        self._add_welcome_message()
    
    def _go_back(self, instance):
        """Go back to previous screen."""
        self._navigate_to_screen('readings')
    
    def _navigate_to_screen(self, screen_name):
        """Navigate to a different screen."""
        if hasattr(self.parent, 'current'):
            self.parent.current = screen_name