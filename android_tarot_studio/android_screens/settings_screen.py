#!/usr/bin/env python3
"""
Settings Screen for Tarot Studio Android App
"""

from kivy.uix.screen import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class SettingsScreen(Screen):
    """Settings screen for app configuration."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = {}
        self._build_ui()
        self._load_settings()
    
    def _build_ui(self):
        """Build the settings screen UI."""
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        
        # Header
        header_layout = self._create_header()
        main_layout.add_widget(header_layout)
        
        # Settings content
        settings_content = self._create_settings_content()
        main_layout.add_widget(settings_content)
        
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
            text='⚙️ Settings',
            font_size=24,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_x=0.6
        )
        
        # Save button
        save_btn = Button(
            text='Save',
            font_size=16,
            size_hint_x=0.2,
            background_color=(0.12, 0.44, 0.92, 1.0)
        )
        save_btn.bind(on_press=self._save_settings)
        
        header_layout.add_widget(back_btn)
        header_layout.add_widget(title_label)
        header_layout.add_widget(save_btn)
        
        return header_layout
    
    def _create_settings_content(self):
        """Create the settings content area."""
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.85,
            spacing=20
        )
        
        # AI Settings Section
        ai_section = self._create_ai_section()
        content_layout.add_widget(ai_section)
        
        # App Settings Section
        app_section = self._create_app_section()
        content_layout.add_widget(app_section)
        
        # Data Settings Section
        data_section = self._create_data_section()
        content_layout.add_widget(data_section)
        
        # About Section
        about_section = self._create_about_section()
        content_layout.add_widget(about_section)
        
        return content_layout
    
    def _create_ai_section(self):
        """Create AI settings section."""
        ai_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.3,
            spacing=10
        )
        
        # Section title
        title_label = Label(
            text='🤖 AI Settings',
            font_size=20,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_y=0.2
        )
        
        # AI Model selection
        model_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.4,
            spacing=10
        )
        
        model_label = Label(
            text='AI Model:',
            font_size=16,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_x=0.4
        )
        
        self.ai_model_spinner = Spinner(
            text='llama3.2',
            values=['llama3.2', 'llama2', 'mistral', 'codellama'],
            size_hint_x=0.6,
            background_color=(0.3, 0.3, 0.3, 1.0)
        )
        
        model_layout.add_widget(model_label)
        model_layout.add_widget(self.ai_model_spinner)
        
        # AI Status
        status_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.4,
            spacing=10
        )
        
        status_label = Label(
            text='AI Status:',
            font_size=16,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_x=0.4
        )
        
        self.ai_status_label = Label(
            text='Offline',
            font_size=16,
            color=(0.9, 0.3, 0.3, 1.0),  # Red
            size_hint_x=0.6
        )
        
        status_layout.add_widget(status_label)
        status_layout.add_widget(self.ai_status_label)
        
        ai_layout.add_widget(title_label)
        ai_layout.add_widget(model_layout)
        ai_layout.add_widget(status_layout)
        
        return ai_layout
    
    def _create_app_section(self):
        """Create app settings section."""
        app_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.25,
            spacing=10
        )
        
        # Section title
        title_label = Label(
            text='📱 App Settings',
            font_size=20,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_y=0.3
        )
        
        # Auto-save setting
        autosave_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.35,
            spacing=10
        )
        
        autosave_label = Label(
            text='Auto-save readings:',
            font_size=16,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_x=0.7
        )
        
        self.autosave_switch = Switch(
            active=True,
            size_hint_x=0.3
        )
        
        autosave_layout.add_widget(autosave_label)
        autosave_layout.add_widget(self.autosave_switch)
        
        # Notifications setting
        notifications_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.35,
            spacing=10
        )
        
        notifications_label = Label(
            text='Enable notifications:',
            font_size=16,
            color=(0.8, 0.8, 0.8, 1.0),
            size_hint_x=0.7
        )
        
        self.notifications_switch = Switch(
            active=True,
            size_hint_x=0.3
        )
        
        notifications_layout.add_widget(notifications_label)
        notifications_layout.add_widget(self.notifications_switch)
        
        app_layout.add_widget(title_label)
        app_layout.add_widget(autosave_layout)
        app_layout.add_widget(notifications_layout)
        
        return app_layout
    
    def _create_data_section(self):
        """Create data settings section."""
        data_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.25,
            spacing=10
        )
        
        # Section title
        title_label = Label(
            text='💾 Data Settings',
            font_size=20,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_y=0.3
        )
        
        # Clear data button
        clear_btn = Button(
            text='Clear All Data',
            font_size=16,
            size_hint_y=0.35,
            background_color=(0.8, 0.3, 0.3, 1.0)  # Red
        )
        clear_btn.bind(on_press=self._clear_data)
        
        # Export data button
        export_btn = Button(
            text='Export Data',
            font_size=16,
            size_hint_y=0.35,
            background_color=(0.3, 0.6, 0.3, 1.0)  # Green
        )
        export_btn.bind(on_press=self._export_data)
        
        data_layout.add_widget(title_label)
        data_layout.add_widget(clear_btn)
        data_layout.add_widget(export_btn)
        
        return data_layout
    
    def _create_about_section(self):
        """Create about section."""
        about_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.2,
            spacing=10
        )
        
        # Section title
        title_label = Label(
            text='ℹ️ About',
            font_size=20,
            color=(0.35, 0.65, 1.0, 1.0),
            bold=True,
            size_hint_y=0.4
        )
        
        # Version info
        version_label = Label(
            text='Tarot Studio Android v1.0.0',
            font_size=14,
            color=(0.6, 0.6, 0.6, 1.0),
            size_hint_y=0.3
        )
        
        # Credits
        credits_label = Label(
            text='Built with Kivy & Python',
            font_size=12,
            color=(0.5, 0.5, 0.5, 1.0),
            size_hint_y=0.3
        )
        
        about_layout.add_widget(title_label)
        about_layout.add_widget(version_label)
        about_layout.add_widget(credits_label)
        
        return about_layout
    
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
    
    def _load_settings(self):
        """Load settings from the database."""
        try:
            app = self.parent.parent.parent.parent
        except AttributeError:
            app = None
        
        if app and hasattr(app, 'get_db'):
            db = app.get_db()
            if db:
                self.settings = db.settings
                
                # Update UI with loaded settings
                self.ai_model_spinner.text = self.settings.get('ai_model', 'llama3.2')
                self.autosave_switch.active = self.settings.get('auto_save', True)
                self.notifications_switch.active = self.settings.get('notifications', True)
                
                # Update AI status
                ai_status = self.settings.get('ai_status', 'offline')
                if ai_status == 'online':
                    self.ai_status_label.text = 'Online'
                    self.ai_status_label.color = (0.3, 0.9, 0.3, 1.0)  # Green
                else:
                    self.ai_status_label.text = 'Offline'
                    self.ai_status_label.color = (0.9, 0.3, 0.3, 1.0)  # Red
    
    def _save_settings(self, instance):
        """Save settings to the database."""
        # Collect current settings
        settings = {
            'ai_model': self.ai_model_spinner.text,
            'auto_save': self.autosave_switch.active,
            'notifications': self.notifications_switch.active,
            'ai_status': 'offline'  # Default to offline
        }
        
        # Save to database
        try:
            app = self.parent.parent.parent.parent
        except AttributeError:
            app = None
        
        if app and hasattr(app, 'get_db'):
            db = app.get_db()
            if db:
                for key, value in settings.items():
                    db.set_setting(key, value)
                
                self._show_popup('Success', 'Settings saved successfully!')
            else:
                self._show_popup('Error', 'Database not available')
        else:
            self._show_popup('Error', 'App not available')
    
    def _clear_data(self, instance):
        """Clear all app data."""
        # Create confirmation popup
        content = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20
        )
        
        warning_label = Label(
            text='This will delete all readings and data.\nAre you sure?',
            font_size=16,
            color=(0.9, 0.3, 0.3, 1.0),
            text_size=(300, None)
        )
        
        button_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=40
        )
        
        cancel_btn = Button(
            text='Cancel',
            background_color=(0.4, 0.4, 0.4, 1.0)
        )
        
        confirm_btn = Button(
            text='Delete All',
            background_color=(0.8, 0.3, 0.3, 1.0)
        )
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(confirm_btn)
        
        content.add_widget(warning_label)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='Clear Data',
            content=content,
            size_hint=(0.8, 0.4),
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        
        cancel_btn.bind(on_press=popup.dismiss)
        confirm_btn.bind(on_press=lambda x: self._confirm_clear_data(popup))
        
        popup.open()
    
    def _confirm_clear_data(self, popup):
        """Confirm clearing data."""
        popup.dismiss()
        
        # Clear data from database
        try:
            app = self.parent.parent.parent.parent
        except AttributeError:
            app = None
        
        if app and hasattr(app, 'get_db'):
            db = app.get_db()
            if db:
                # Clear readings
                readings = db.get_all_readings()
                for reading in readings:
                    db.delete_reading(reading['id'])
                
                self._show_popup('Success', 'All data cleared successfully!')
            else:
                self._show_popup('Error', 'Database not available')
    
    def _export_data(self, instance):
        """Export app data."""
        self._show_popup('Info', 'Export functionality will be implemented in a future version.')
    
    def _show_popup(self, title, message):
        """Show a popup message."""
        content = BoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20
        )
        
        label = Label(
            text=message,
            text_size=(300, None),
            color=(0.8, 0.8, 0.8, 1.0)
        )
        content.add_widget(label)
        
        btn = Button(
            text='OK',
            size_hint_y=None,
            height=40,
            background_color=(0.12, 0.44, 0.92, 1.0)
        )
        content.add_widget(btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4),
            background_color=(0.2, 0.2, 0.2, 1.0)
        )
        
        btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def _go_back(self, instance):
        """Go back to previous screen."""
        self._navigate_to_screen('readings')
    
    def _navigate_to_screen(self, screen_name):
        """Navigate to a different screen."""
        if hasattr(self.parent, 'current'):
            self.parent.current = screen_name