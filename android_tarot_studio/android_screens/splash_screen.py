#!/usr/bin/env python3
"""
Splash Screen for Tarot Studio Android App
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.animation import Animation

class SplashScreen(Screen):
    """Splash screen with loading animation."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
    
    def _build_ui(self):
        """Build the splash screen UI."""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=50,
            spacing=30
        )
        
        # App icon/logo
        logo_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.6
        )
        
        # Tarot card icon (using text for now)
        logo_label = Label(
            text='🔮',
            font_size=120,
            color=(0.35, 0.65, 1.0, 1.0),  # Blue color
            size_hint_y=0.7
        )
        
        # App title
        title_label = Label(
            text='Tarot Studio',
            font_size=36,
            color=(0.8, 0.8, 0.8, 1.0),  # Light gray
            bold=True,
            size_hint_y=0.3
        )
        
        logo_layout.add_widget(logo_label)
        logo_layout.add_widget(title_label)
        
        # Loading section
        loading_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.4,
            spacing=20
        )
        
        # Loading text
        loading_label = Label(
            text='Loading your tarot experience...',
            font_size=18,
            color=(0.6, 0.6, 0.6, 1.0),  # Gray
            size_hint_y=0.3
        )
        
        # Progress bar
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=0.2
        )
        
        # Version info
        version_label = Label(
            text='Android Edition',
            font_size=14,
            color=(0.5, 0.5, 0.5, 1.0),  # Dark gray
            size_hint_y=0.2
        )
        
        loading_layout.add_widget(loading_label)
        loading_layout.add_widget(self.progress_bar)
        loading_layout.add_widget(version_label)
        
        # Add to main layout
        main_layout.add_widget(logo_layout)
        main_layout.add_widget(loading_layout)
        
        self.add_widget(main_layout)
        
        # Start loading animation
        self._start_loading_animation()
    
    def _start_loading_animation(self):
        """Start the loading animation."""
        # Animate the progress bar
        anim = Animation(value=100, duration=2.0)
        anim.start(self.progress_bar)
        
        # Animate the logo (simplified for mock testing)
        try:
            # Try to find the logo widget, but don't fail if not found
            if hasattr(self, 'children') and len(self.children) > 0:
                main_layout = self.children[0]
                if hasattr(main_layout, 'children') and len(main_layout.children) > 1:
                    logo_layout = main_layout.children[1]
                    if hasattr(logo_layout, 'children') and len(logo_layout.children) > 0:
                        logo_widget = logo_layout.children[0]
                        logo_anim = Animation(font_size=140, duration=1.0) + Animation(font_size=120, duration=1.0)
                        logo_anim.repeat = True
                        logo_anim.start(logo_widget)
        except (IndexError, AttributeError):
            # Skip animation if widget structure is not as expected
            pass