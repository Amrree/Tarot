#!/usr/bin/env python3
"""
Readings Screen for Tarot Studio Android App
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.animation import Animation

class ReadingsScreen(Screen):
    """Main readings screen for drawing cards and creating spreads."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_spread = None
        self.drawn_cards = []
        self._build_ui()
    
    def _build_ui(self):
        """Build the readings screen UI."""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        
        # Header
        header_layout = self._create_header()
        main_layout.add_widget(header_layout)
        
        # Content area
        content_layout = self._create_content()
        main_layout.add_widget(content_layout)
        
        # Bottom navigation
        bottom_nav = self._create_bottom_navigation()
        main_layout.add_widget(bottom_nav)
        
        self.add_widget(main_layout)
    
    def _create_header(self):
        """Create the header section."""
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            spacing=10
        )
        
        # App title
        title_label = Label(
            text='🔮 Tarot Studio',
            font_size=24,
            color=(0.35, 0.65, 1.0, 1.0),  # Blue
            bold=True,
            size_hint_x=0.7
        )
        
        # Settings button
        settings_btn = Button(
            text='⚙️',
            font_size=20,
            size_hint_x=0.3,
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        settings_btn.bind(on_press=self._open_settings)
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(settings_btn)
        
        return header_layout
    
    def _create_content(self):
        """Create the main content area."""
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.8,
            spacing=15
        )
        
        # Spread selection
        spread_section = self._create_spread_section()
        content_layout.add_widget(spread_section)
        
        # Question input
        question_section = self._create_question_section()
        content_layout.add_widget(question_section)
        
        # Action buttons
        action_section = self._create_action_section()
        content_layout.add_widget(action_section)
        
        # Cards display
        cards_section = self._create_cards_section()
        content_layout.add_widget(cards_section)
        
        return content_layout
    
    def _create_spread_section(self):
        """Create the spread selection section."""
        spread_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.2,
            spacing=10
        )
        
        # Label
        label = Label(
            text='Select Spread',
            font_size=18,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_y=0.3
        )
        
        # Spinner for spread selection
        self.spread_spinner = Spinner(
            text='Choose a spread...',
            values=['Single Card', 'Three Card', 'Celtic Cross'],
            size_hint_y=0.7,
            background_color=(0.3, 0.3, 0.3, 1.0)
        )
        self.spread_spinner.bind(text=self._on_spread_selected)
        
        spread_layout.add_widget(label)
        spread_layout.add_widget(self.spread_spinner)
        
        return spread_layout
    
    def _create_question_section(self):
        """Create the question input section."""
        question_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.2,
            spacing=10
        )
        
        # Label
        label = Label(
            text='Your Question (Optional)',
            font_size=18,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_y=0.3
        )
        
        # Text input
        self.question_input = TextInput(
            hint_text='What guidance do you seek?',
            multiline=True,
            size_hint_y=0.7,
            background_color=(0.2, 0.2, 0.2, 1.0),
            foreground_color=(0.8, 0.8, 0.8, 1.0)
        )
        
        question_layout.add_widget(label)
        question_layout.add_widget(self.question_input)
        
        return question_layout
    
    def _create_action_section(self):
        """Create the action buttons section."""
        action_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.15,
            spacing=15
        )
        
        # Draw cards button
        self.draw_btn = Button(
            text='Draw Cards',
            font_size=18,
            size_hint_x=0.6,
            background_color=(0.12, 0.44, 0.92, 1.0)  # Blue
        )
        self.draw_btn.bind(on_press=self._draw_cards)
        
        # Reset deck button
        self.reset_btn = Button(
            text='Reset Deck',
            font_size=16,
            size_hint_x=0.4,
            background_color=(0.4, 0.4, 0.4, 1.0)  # Gray
        )
        self.reset_btn.bind(on_press=self._reset_deck)
        
        action_layout.add_widget(self.draw_btn)
        action_layout.add_widget(self.reset_btn)
        
        return action_layout
    
    def _create_cards_section(self):
        """Create the cards display section."""
        cards_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.45,
            spacing=10
        )
        
        # Label
        self.cards_label = Label(
            text='Cards will appear here',
            font_size=16,
            color=(0.6, 0.6, 0.6, 1.0),
            size_hint_y=0.1
        )
        
        # Scrollable cards container
        self.cards_scroll = ScrollView(
            size_hint_y=0.9
        )
        
        self.cards_container = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=10,
            padding=10
        )
        self.cards_container.bind(minimum_height=self.cards_container.setter('height'))
        
        self.cards_scroll.add_widget(self.cards_container)
        
        cards_layout.add_widget(self.cards_label)
        cards_layout.add_widget(self.cards_scroll)
        
        return cards_layout
    
    def _create_bottom_navigation(self):
        """Create the bottom navigation."""
        nav_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            spacing=5
        )
        
        # Navigation buttons
        nav_buttons = [
            ('📖', 'readings', self._navigate_to_readings),
            ('💬', 'chat', self._navigate_to_chat),
            ('📚', 'history', self._navigate_to_history),
            ('⚙️', 'settings', self._navigate_to_settings)
        ]
        
        for icon, name, callback in nav_buttons:
            btn = Button(
                text=icon,
                font_size=20,
                background_color=(0.2, 0.2, 0.2, 1.0)
            )
            btn.bind(on_press=lambda x, screen=name: self._navigate_to_screen(screen))
            nav_layout.add_widget(btn)
        
        return nav_layout
    
    def _on_spread_selected(self, spinner, text):
        """Handle spread selection."""
        self.current_spread = text
        self.cards_label.text = f'Selected: {text}'
        
        # Update draw button text
        if text == 'Single Card':
            self.draw_btn.text = 'Draw 1 Card'
        elif text == 'Three Card':
            self.draw_btn.text = 'Draw 3 Cards'
        elif text == 'Celtic Cross':
            self.draw_btn.text = 'Draw 10 Cards'
    
    def _draw_cards(self, instance):
        """Draw cards for the selected spread."""
        if not self.current_spread:
            self._show_popup('Error', 'Please select a spread first!')
            return
        
        # Get number of cards to draw
        num_cards = 1
        if self.current_spread == 'Three Card':
            num_cards = 3
        elif self.current_spread == 'Celtic Cross':
            num_cards = 10
        
        # Get app instance to access deck
        try:
            app = self.parent.parent.parent.parent  # Navigate to app
        except AttributeError:
            app = None
        
        if app and hasattr(app, 'get_deck'):
            deck = app.get_deck()
            if deck:
                # Draw cards
                drawn_cards = []
                for _ in range(num_cards):
                    card = deck.draw_card()
                    if card:
                        drawn_cards.append(card)
                
                if drawn_cards:
                    self.drawn_cards = drawn_cards
                    self._display_cards(drawn_cards)
                    self._show_popup('Success', f'Drew {len(drawn_cards)} cards!')
                else:
                    self._show_popup('Error', 'No cards available in deck!')
            else:
                self._show_popup('Error', 'Deck not available!')
    
    def _display_cards(self, cards):
        """Display the drawn cards."""
        # Clear existing cards
        self.cards_container.clear_widgets()
        
        # Add cards
        for i, card in enumerate(cards):
            card_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=80,
                spacing=10,
                padding=10
            )
            
            # Card number
            number_label = Label(
                text=f'{i+1}',
                font_size=20,
                color=(0.35, 0.65, 1.0, 1.0),
                size_hint_x=0.1
            )
            
            # Card name
            name_label = Label(
                text=card.name,
                font_size=18,
                color=(0.8, 0.8, 0.8, 1.0),
                size_hint_x=0.4,
                text_size=(None, None),
                halign='left'
            )
            
            # Card keywords
            keywords_label = Label(
                text=', '.join(card.keywords[:3]),  # First 3 keywords
                font_size=14,
                color=(0.6, 0.6, 0.6, 1.0),
                size_hint_x=0.5,
                text_size=(None, None),
                halign='left'
            )
            
            card_layout.add_widget(number_label)
            card_layout.add_widget(name_label)
            card_layout.add_widget(keywords_label)
            
            self.cards_container.add_widget(card_layout)
        
        # Update label
        self.cards_label.text = f'Drawn {len(cards)} cards'
    
    def _reset_deck(self, instance):
        """Reset the deck."""
        try:
            app = self.parent.parent.parent.parent
        except AttributeError:
            app = None
        
        if app and hasattr(app, 'reset_deck'):
            app.reset_deck()
            self.drawn_cards = []
            self.cards_container.clear_widgets()
            self.cards_label.text = 'Deck reset - ready for new reading'
            self._show_popup('Success', 'Deck reset successfully!')
    
    def _show_popup(self, title, message):
        """Show a popup message."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        label = Label(text=message, text_size=(300, None))
        content.add_widget(label)
        
        btn = Button(text='OK', size_hint_y=None, height=40)
        content.add_widget(btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4),
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        
        btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def _navigate_to_screen(self, screen_name):
        """Navigate to a different screen."""
        if hasattr(self.parent, 'current'):
            self.parent.current = screen_name
    
    def _navigate_to_readings(self, instance):
        self._navigate_to_screen('readings')
    
    def _navigate_to_chat(self, instance):
        self._navigate_to_screen('chat')
    
    def _navigate_to_history(self, instance):
        self._navigate_to_screen('history')
    
    def _navigate_to_settings(self, instance):
        self._navigate_to_screen('settings')
    
    def _open_settings(self, instance):
        """Open settings screen."""
        self._navigate_to_screen('settings')