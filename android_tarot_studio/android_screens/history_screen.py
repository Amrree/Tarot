#!/usr/bin/env python3
"""
History Screen for Tarot Studio Android App
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

class HistoryScreen(Screen):
    """History screen for viewing past readings."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.readings = []
        self._build_ui()
    
    def _build_ui(self):
        """Build the history screen UI."""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        
        # Header
        header_layout = self._create_header()
        main_layout.add_widget(header_layout)
        
        # Search area
        search_area = self._create_search_area()
        main_layout.add_widget(search_area)
        
        # Readings list
        readings_area = self._create_readings_area()
        main_layout.add_widget(readings_area)
        
        # Bottom navigation
        bottom_nav = self._create_bottom_navigation()
        main_layout.add_widget(bottom_nav)
        
        self.add_widget(main_layout)
        
        # Load readings
        self._load_readings()
    
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
            text='📚 Reading History',
            font_size=24,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_x=0.6
        )
        
        # Refresh button
        refresh_btn = Button(
            text='🔄',
            font_size=20,
            size_hint_x=0.2,
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        refresh_btn.bind(on_press=self._refresh_readings)
        
        header_layout.add_widget(back_btn)
        header_layout.add_widget(title_label)
        header_layout.add_widget(refresh_btn)
        
        return header_layout
    
    def _create_search_area(self):
        """Create the search area."""
        search_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            spacing=10
        )
        
        # Search input
        self.search_input = TextInput(
            hint_text='Search readings...',
            multiline=False,
            size_hint_x=0.8,
            background_color=(0.2, 0.2, 0.2, 1.0),
            foreground_color=(0.8, 0.8, 0.8, 1.0)
        )
        self.search_input.bind(text=self._on_search_text)
        
        # Search button
        search_btn = Button(
            text='🔍',
            font_size=20,
            size_hint_x=0.2,
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        search_btn.bind(on_press=self._perform_search)
        
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_btn)
        
        return search_layout
    
    def _create_readings_area(self):
        """Create the readings list area."""
        readings_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.75,
            spacing=10
        )
        
        # Status label
        self.status_label = Label(
            text='Loading readings...',
            font_size=16,
            color=(0.6, 0.6, 0.6, 1.0),
            size_hint_y=0.1
        )
        
        # Scrollable readings container
        self.readings_scroll = ScrollView(
            size_hint_y=0.9
        )
        
        self.readings_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=10
        )
        self.readings_container.bind(minimum_height=self.readings_container.setter('height'))
        
        self.readings_scroll.add_widget(self.readings_container)
        
        readings_layout.add_widget(self.status_label)
        readings_layout.add_widget(self.readings_scroll)
        
        return readings_layout
    
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
    
    def _load_readings(self):
        """Load readings from the database."""
        try:
            app = self.parent.parent.parent.parent
            if hasattr(app, 'get_readings'):
                self.readings = app.get_readings()
                self._display_readings(self.readings)
            else:
                self.status_label.text = 'Database not available'
        except AttributeError:
            # Handle case where parent chain is not available (e.g., during testing)
            self.readings = []
            self._display_readings(self.readings)
            self.status_label.text = 'No readings available (test mode)'
    
    def _display_readings(self, readings):
        """Display readings in the list."""
        # Clear existing readings
        self.readings_container.clear_widgets()
        
        if not readings:
            # No readings message
            no_readings_label = Label(
                text='No readings found.\nCreate your first reading!',
                font_size=18,
                color=(0.6, 0.6, 0.6, 1.0),
                size_hint_y=None,
                height=100
            )
            self.readings_container.add_widget(no_readings_label)
            self.status_label.text = 'No readings available'
            return
        
        # Add readings
        for reading in readings:
            reading_widget = self._create_reading_widget(reading)
            self.readings_container.add_widget(reading_widget)
        
        self.status_label.text = f'Found {len(readings)} readings'
    
    def _create_reading_widget(self, reading):
        """Create a widget for a single reading."""
        reading_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=120,
            spacing=5,
            padding=10
        )
        
        # Reading header
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.4,
            spacing=10
        )
        
        # Title
        title_label = Label(
            text=reading.get('title', 'Untitled Reading'),
            font_size=18,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_x=0.7,
            text_size=(None, None),
            halign='left'
        )
        
        # Date
        date_label = Label(
            text=reading.get('created_at', 'Unknown date')[:10],  # Just the date part
            font_size=12,
            color=(0.6, 0.6, 0.6, 1.0),
            size_hint_x=0.3,
            halign='right'
        )
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(date_label)
        
        # Reading content
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.6,
            spacing=5
        )
        
        # Question
        question_text = reading.get('question', 'No question asked')
        if len(question_text) > 50:
            question_text = question_text[:47] + '...'
        
        question_label = Label(
            text=f'Q: {question_text}',
            font_size=14,
            color=(0.8, 0.8, 0.8, 1.0),
            text_size=(None, None),
            halign='left'
        )
        
        # Summary
        summary_text = reading.get('summary', 'No summary available')
        if len(summary_text) > 60:
            summary_text = summary_text[:57] + '...'
        
        summary_label = Label(
            text=f'Summary: {summary_text}',
            font_size=12,
            color=(0.6, 0.6, 0.6, 1.0),
            text_size=(None, None),
            halign='left'
        )
        
        content_layout.add_widget(question_label)
        content_layout.add_widget(summary_label)
        
        # Add to main layout
        reading_layout.add_widget(header_layout)
        reading_layout.add_widget(content_layout)
        
        # Add tap handler
        reading_layout.bind(on_touch_down=lambda x, y, reading=reading: self._on_reading_tap(reading, y))
        
        return reading_layout
    
    def _on_reading_tap(self, reading, touch):
        """Handle tap on reading item."""
        if touch.is_double_tap:
            self._show_reading_details(reading)
    
    def _show_reading_details(self, reading):
        """Show detailed reading information."""
        # Create popup content
        content = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20
        )
        
        # Title
        title_label = Label(
            text=reading.get('title', 'Untitled Reading'),
            font_size=20,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_y=0.2
        )
        
        # Date
        date_label = Label(
            text=f"Date: {reading.get('created_at', 'Unknown')}",
            font_size=14,
            color=(0.6, 0.6, 0.6, 1.0),
            size_hint_y=0.1
        )
        
        # Question
        question_label = Label(
            text=f"Question: {reading.get('question', 'No question')}",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_y=0.2,
            text_size=(400, None),
            halign='left'
        )
        
        # Summary
        summary_label = Label(
            text=f"Summary: {reading.get('summary', 'No summary')}",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_y=0.3,
            text_size=(400, None),
            halign='left'
        )
        
        # Close button
        close_btn = Button(
            text='Close',
            size_hint_y=0.2,
            background_color=(0.12, 0.44, 0.92, 1.0)
        )
        
        content.add_widget(title_label)
        content.add_widget(date_label)
        content.add_widget(question_label)
        content.add_widget(summary_label)
        content.add_widget(close_btn)
        
        # Create popup
        popup = Popup(
            title='Reading Details',
            content=content,
            size_hint=(0.9, 0.8),
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def _on_search_text(self, instance, text):
        """Handle search text changes."""
        if text:
            filtered_readings = [r for r in self.readings if 
                               text.lower() in r.get('title', '').lower() or
                               text.lower() in r.get('question', '').lower() or
                               text.lower() in r.get('summary', '').lower()]
            self._display_readings(filtered_readings)
        else:
            self._display_readings(self.readings)
    
    def _perform_search(self, instance):
        """Perform search."""
        # Search is handled in _on_search_text
        pass
    
    def _refresh_readings(self, instance):
        """Refresh the readings list."""
        self._load_readings()
    
    def _go_back(self, instance):
        """Go back to previous screen."""
        self._navigate_to_screen('readings')
    
    def _navigate_to_screen(self, screen_name):
        """Navigate to a different screen."""
        if hasattr(self.parent, 'current'):
            self.parent.current = screen_name