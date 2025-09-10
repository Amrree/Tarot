"""
Settings view for Tarot Studio application.
"""

import objc
from Foundation import *
from AppKit import *
from Cocoa import *
import logging

logger = logging.getLogger(__name__)

class SettingsView(NSView):
    """Settings view for app configuration."""
    
    def init(self):
        """Initialize the settings view."""
        self = super(SettingsView, self).init()
        
        if self:
            self.setWantsLayer_(True)
            self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
            
            # Initialize properties
            self.session = None
            self.ollama_client = None
            self.memory_store = None
            
            # Create UI components
            self.createUI()
            
        return self
    
    def initWithFrame_(self, frame):
        """Initialize with frame."""
        self = super(SettingsView, self).initWithFrame_(frame)
        
        if self:
            self.setWantsLayer_(True)
            self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
            
            # Initialize properties
            self.session = None
            self.ollama_client = None
            self.memory_store = None
            
            # Create UI components
            self.createUI()
            
        return self
    
    def createUI(self):
        """Create the UI components."""
        # Title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 750, 200, 20))
        title_label.setStringValue_("Settings")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(16, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # AI Settings section
        ai_section = self.createAISettingsSection()
        self.addSubview_(ai_section)
        
        # Database Settings section
        db_section = self.createDatabaseSettingsSection()
        self.addSubview_(db_section)
        
        # Appearance Settings section
        appearance_section = self.createAppearanceSettingsSection()
        self.addSubview_(appearance_section)
        
        # Add title
        self.addSubview_(title_label)
    
    def createAISettingsSection(self):
        """Create AI settings section."""
        section = NSView.alloc().initWithFrame_(NSMakeRect(20, 600, 960, 120))
        section.setWantsLayer_(True)
        section.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        section.layer().setCornerRadius_(8)
        
        # Section title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 90, 200, 20))
        title_label.setStringValue_("AI Settings")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(14, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Ollama URL
        url_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 60, 100, 20))
        url_label.setStringValue_("Ollama URL:")
        url_label.setBordered_(False)
        url_label.setDrawsBackground_(False)
        url_label.setEditable_(False)
        url_label.setSelectable_(False)
        url_label.setFont_(NSFont.systemFontOfSize_(12))
        url_label.setTextColor_(NSColor.labelColor())
        
        self.ollama_url_field = NSTextField.alloc().initWithFrame_(NSMakeRect(130, 60, 300, 20))
        self.ollama_url_field.setStringValue_("http://localhost:11434")
        self.ollama_url_field.setPlaceholderString_("http://localhost:11434")
        
        # Model selection
        model_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 30, 100, 20))
        model_label.setStringValue_("Model:")
        model_label.setBordered_(False)
        model_label.setDrawsBackground_(False)
        model_label.setEditable_(False)
        model_label.setSelectable_(False)
        model_label.setFont_(NSFont.systemFontOfSize_(12))
        model_label.setTextColor_(NSColor.labelColor())
        
        self.model_field = NSTextField.alloc().initWithFrame_(NSMakeRect(130, 30, 300, 20))
        self.model_field.setStringValue_("llama3.2")
        self.model_field.setPlaceholderString_("llama3.2")
        
        # Test connection button
        self.test_button = NSButton.alloc().initWithFrame_(NSMakeRect(450, 45, 120, 30))
        self.test_button.setTitle_("Test Connection")
        self.test_button.setTarget_(self)
        self.test_button.setAction_('testConnection:')
        self.test_button.setBordered_(True)
        self.test_button.setBezelStyle_(NSBezelStyleRounded)
        
        # Status label
        self.status_label = NSTextField.alloc().initWithFrame_(NSMakeRect(600, 45, 200, 20))
        self.status_label.setStringValue_("Not connected")
        self.status_label.setBordered_(False)
        self.status_label.setDrawsBackground_(False)
        self.status_label.setEditable_(False)
        self.status_label.setSelectable_(False)
        self.status_label.setFont_(NSFont.systemFontOfSize_(12))
        self.status_label.setTextColor_(NSColor.secondaryLabelColor())
        
        section.addSubview_(title_label)
        section.addSubview_(url_label)
        section.addSubview_(self.ollama_url_field)
        section.addSubview_(model_label)
        section.addSubview_(self.model_field)
        section.addSubview_(self.test_button)
        section.addSubview_(self.status_label)
        
        return section
    
    def createDatabaseSettingsSection(self):
        """Create database settings section."""
        section = NSView.alloc().initWithFrame_(NSMakeRect(20, 450, 960, 120))
        section.setWantsLayer_(True)
        section.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        section.layer().setCornerRadius_(8)
        
        # Section title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 90, 200, 20))
        title_label.setStringValue_("Database Settings")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(14, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Export button
        self.export_button = NSButton.alloc().initWithFrame_(NSMakeRect(20, 50, 120, 30))
        self.export_button.setTitle_("Export Data")
        self.export_button.setTarget_(self)
        self.export_button.setAction_('exportData:')
        self.export_button.setBordered_(True)
        self.export_button.setBezelStyle_(NSBezelStyleRounded)
        
        # Import button
        self.import_button = NSButton.alloc().initWithFrame_(NSMakeRect(160, 50, 120, 30))
        self.import_button.setTitle_("Import Data")
        self.import_button.setTarget_(self)
        self.import_button.setAction_('importData:')
        self.import_button.setBordered_(True)
        self.import_button.setBezelStyle_(NSBezelStyleRounded)
        
        # Clear data button
        self.clear_button = NSButton.alloc().initWithFrame_(NSMakeRect(300, 50, 120, 30))
        self.clear_button.setTitle_("Clear All Data")
        self.clear_button.setTarget_(self)
        self.clear_button.setAction_('clearData:')
        self.clear_button.setBordered_(True)
        self.clear_button.setBezelStyle_(NSBezelStyleRounded)
        
        # Database info
        self.db_info_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 20, 400, 20))
        self.db_info_label.setStringValue_("Database: tarot_studio.db")
        self.db_info_label.setBordered_(False)
        self.db_info_label.setDrawsBackground_(False)
        self.db_info_label.setEditable_(False)
        self.db_info_label.setSelectable_(False)
        self.db_info_label.setFont_(NSFont.systemFontOfSize_(12))
        self.db_info_label.setTextColor_(NSColor.secondaryLabelColor())
        
        section.addSubview_(title_label)
        section.addSubview_(self.export_button)
        section.addSubview_(self.import_button)
        section.addSubview_(self.clear_button)
        section.addSubview_(self.db_info_label)
        
        return section
    
    def createAppearanceSettingsSection(self):
        """Create appearance settings section."""
        section = NSView.alloc().initWithFrame_(NSMakeRect(20, 300, 960, 120))
        section.setWantsLayer_(True)
        section.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        section.layer().setCornerRadius_(8)
        
        # Section title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 90, 200, 20))
        title_label.setStringValue_("Appearance")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(14, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Theme selection
        theme_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 60, 100, 20))
        theme_label.setStringValue_("Theme:")
        theme_label.setBordered_(False)
        theme_label.setDrawsBackground_(False)
        theme_label.setEditable_(False)
        theme_label.setSelectable_(False)
        theme_label.setFont_(NSFont.systemFontOfSize_(12))
        theme_label.setTextColor_(NSColor.labelColor())
        
        self.theme_popup = NSPopUpButton.alloc().initWithFrame_(NSMakeRect(130, 60, 200, 20))
        self.theme_popup.addItemWithTitle_("Dark")
        self.theme_popup.addItemWithTitle_("Light")
        self.theme_popup.addItemWithTitle_("Auto")
        self.theme_popup.selectItemWithTitle_("Dark")
        
        # Font size
        font_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 30, 100, 20))
        font_label.setStringValue_("Font Size:")
        font_label.setBordered_(False)
        font_label.setDrawsBackground_(False)
        font_label.setEditable_(False)
        font_label.setSelectable_(False)
        font_label.setFont_(NSFont.systemFontOfSize_(12))
        font_label.setTextColor_(NSColor.labelColor())
        
        self.font_slider = NSSlider.alloc().initWithFrame_(NSMakeRect(130, 30, 200, 20))
        self.font_slider.setMinValue_(10)
        self.font_slider.setMaxValue_(20)
        self.font_slider.setDoubleValue_(12)
        self.font_slider.setTarget_(self)
        self.font_slider.setAction_('fontSizeChanged:')
        
        self.font_size_label = NSTextField.alloc().initWithFrame_(NSMakeRect(340, 30, 50, 20))
        self.font_size_label.setStringValue_("12")
        self.font_size_label.setBordered_(False)
        self.font_size_label.setDrawsBackground_(False)
        self.font_size_label.setEditable_(False)
        self.font_size_label.setSelectable_(False)
        self.font_size_label.setFont_(NSFont.systemFontOfSize_(12))
        self.font_size_label.setTextColor_(NSColor.labelColor())
        
        section.addSubview_(title_label)
        section.addSubview_(theme_label)
        section.addSubview_(self.theme_popup)
        section.addSubview_(font_label)
        section.addSubview_(self.font_slider)
        section.addSubview_(self.font_size_label)
        
        return section
    
    def testConnection_(self, sender):
        """Test Ollama connection."""
        if not self.ollama_client:
            self.status_label.setStringValue_("No client available")
            return
        
        # Update client settings
        self.ollama_client.base_url = self.ollama_url_field.stringValue()
        self.ollama_client.model_name = self.model_field.stringValue()
        
        # Test connection
        import asyncio
        
        async def test():
            try:
                connected = await self.ollama_client.check_connection()
                return connected
            except Exception as e:
                logger.error(f"Connection test failed: {e}")
                return False
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            connected = loop.run_until_complete(test())
            if connected:
                self.status_label.setStringValue_("Connected")
                self.status_label.setTextColor_(NSColor.systemGreenColor())
            else:
                self.status_label.setStringValue_("Connection failed")
                self.status_label.setTextColor_(NSColor.systemRedColor())
        finally:
            loop.close()
    
    def exportData_(self, sender):
        """Export application data."""
        # Show save dialog
        save_panel = NSSavePanel.savePanel()
        save_panel.setAllowedFileTypes_(["json"])
        save_panel.setNameFieldStringValue_("tarot_studio_backup.json")
        
        if save_panel.runModal() == NSFileHandlingPanelOKButton:
            file_path = save_panel.URL().path()
            # TODO: Implement data export
            logger.info(f"Export data to: {file_path}")
    
    def importData_(self, sender):
        """Import application data."""
        # Show open dialog
        open_panel = NSOpenPanel.openPanel()
        open_panel.setAllowedFileTypes_(["json"])
        open_panel.setCanChooseFiles_(True)
        open_panel.setCanChooseDirectories_(False)
        
        if open_panel.runModal() == NSFileHandlingPanelOKButton:
            file_path = open_panel.URL().path()
            # TODO: Implement data import
            logger.info(f"Import data from: {file_path}")
    
    def clearData_(self, sender):
        """Clear all application data."""
        # Show confirmation dialog
        alert = NSAlert.alloc().init()
        alert.setMessageText_("Clear All Data")
        alert.setInformativeText_("This will permanently delete all readings, conversations, and settings. This action cannot be undone.")
        alert.addButtonWithTitle_("Clear All Data")
        alert.addButtonWithTitle_("Cancel")
        alert.setAlertStyle_(NSAlertStyleWarning)
        
        if alert.runModal() == NSAlertFirstButtonReturn:
            # TODO: Implement data clearing
            logger.info("Clear all data confirmed")
    
    def fontSizeChanged_(self, sender):
        """Handle font size change."""
        font_size = int(self.font_slider.doubleValue())
        self.font_size_label.setStringValue_(str(font_size))
        # TODO: Apply font size changes to UI
    
    def setSession_ollamaClient_memoryStore_(self, session, ollama_client, memory_store):
        """Set dependencies."""
        self.session = session
        self.ollama_client = ollama_client
        self.memory_store = memory_store