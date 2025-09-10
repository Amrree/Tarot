"""
Main window for Tarot Studio application using PyObjC.
"""

import objc
from Foundation import *
from AppKit import *
from Cocoa import *
import logging

from tarot_studio.app.ui.sidebar import SidebarView
from tarot_studio.app.ui.readings_view import ReadingsView
from tarot_studio.app.ui.chat_view import ChatView
from tarot_studio.app.ui.history_view import HistoryView
from tarot_studio.app.ui.settings_view import SettingsView

logger = logging.getLogger(__name__)

class MainWindow(NSWindow):
    """Main application window."""
    
    def init(self):
        """Initialize the main window."""
        # Create window with dark theme
        self = super(MainWindow, self).initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(100, 100, 1200, 800),
            NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable,
            NSBackingStoreBuffered,
            False
        )
        
        if self:
            self.setTitle_("Tarot Studio")
            self.setMinSize_(NSMakeSize(800, 600))
            
            # Set dark appearance
            self.setAppearance_(NSAppearance.appearanceNamed_(NSAppearanceNameDarkAqua))
            
            # Create main content view
            self.contentView = self.createMainContentView()
            self.setContentView_(self.contentView)
            
            # Initialize components
            self.current_view = None
            self.session = None
            self.ollama_client = None
            self.memory_store = None
            
            # Set up window delegate
            self.setDelegate_(self)
            
        return self
    
    def initWithSession_ollamaClient_memoryStore_(self, session, ollama_client, memory_store):
        """Initialize with dependencies."""
        self = self.init()
        if self:
            self.session = session
            self.ollama_client = ollama_client
            self.memory_store = memory_store
            
            # Initialize views with dependencies
            self.sidebar_view.setSession_ollamaClient_memoryStore_(session, ollama_client, memory_store)
            self.readings_view.setSession_ollamaClient_memoryStore_(session, ollama_client, memory_store)
            self.chat_view.setSession_ollamaClient_memoryStore_(session, ollama_client, memory_store)
            self.history_view.setSession_ollamaClient_memoryStore_(session, ollama_client, memory_store)
            self.settings_view.setSession_ollamaClient_memoryStore_(session, ollama_client, memory_store)
            
            # Show default view
            self.showReadingsView()
            
        return self
    
    def createMainContentView(self):
        """Create the main content view with sidebar and content area."""
        # Main container
        main_view = NSView.alloc().initWithFrame_(NSMakeRect(0, 0, 1200, 800))
        
        # Create sidebar
        self.sidebar_view = SidebarView.alloc().initWithFrame_(NSMakeRect(0, 0, 200, 800))
        self.sidebar_view.setDelegate_(self)
        
        # Create content area
        self.content_area = NSView.alloc().initWithFrame_(NSMakeRect(200, 0, 1000, 800))
        
        # Create header
        self.header_view = self.createHeaderView()
        
        # Create views
        self.readings_view = ReadingsView.alloc().initWithFrame_(NSMakeRect(0, 0, 1000, 800))
        self.chat_view = ChatView.alloc().initWithFrame_(NSMakeRect(0, 0, 1000, 800))
        self.history_view = HistoryView.alloc().initWithFrame_(NSMakeRect(0, 0, 1000, 800))
        self.settings_view = SettingsView.alloc().initWithFrame_(NSMakeRect(0, 0, 1000, 800))
        
        # Add subviews
        main_view.addSubview_(self.sidebar_view)
        main_view.addSubview_(self.content_area)
        
        self.content_area.addSubview_(self.header_view)
        self.content_area.addSubview_(self.readings_view)
        self.content_area.addSubview_(self.chat_view)
        self.content_area.addSubview_(self.history_view)
        self.content_area.addSubview_(self.settings_view)
        
        # Set up constraints
        self.setupConstraints(main_view)
        
        return main_view
    
    def createHeaderView(self):
        """Create the header view."""
        header_view = NSView.alloc().initWithFrame_(NSMakeRect(0, 750, 1000, 50))
        header_view.setWantsLayer_(True)
        header_view.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        
        # App title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 15, 200, 20))
        title_label.setStringValue_("Tarot Studio")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.monospacedSystemFontOfSize_weight_(14, NSFontWeightRegular))
        title_label.setTextColor_(NSColor.labelColor())
        
        # AI status
        self.ai_status_label = NSTextField.alloc().initWithFrame_(NSMakeRect(800, 15, 180, 20))
        self.ai_status_label.setStringValue_("AI: Ready")
        self.ai_status_label.setBordered_(False)
        self.ai_status_label.setDrawsBackground_(False)
        self.ai_status_label.setEditable_(False)
        self.ai_status_label.setSelectable_(False)
        self.ai_status_label.setFont_(NSFont.monospacedSystemFontOfSize_weight_(12, NSFontWeightRegular))
        self.ai_status_label.setTextColor_(NSColor.secondaryLabelColor())
        
        header_view.addSubview_(title_label)
        header_view.addSubview_(self.ai_status_label)
        
        return header_view
    
    def setupConstraints(self, main_view):
        """Set up Auto Layout constraints."""
        main_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
        
        # Sidebar constraints
        self.sidebar_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
        NSLayoutConstraint.activateConstraints_([
            self.sidebar_view.leadingAnchor().constraintEqualToAnchor_(main_view.leadingAnchor()),
            self.sidebar_view.topAnchor().constraintEqualToAnchor_(main_view.topAnchor()),
            self.sidebar_view.bottomAnchor().constraintEqualToAnchor_(main_view.bottomAnchor()),
            self.sidebar_view.widthAnchor().constraintEqualToConstant_(200)
        ])
        
        # Content area constraints
        self.content_area.setTranslatesAutoresizingMaskIntoConstraints_(False)
        NSLayoutConstraint.activateConstraints_([
            self.content_area.leadingAnchor().constraintEqualToAnchor_(self.sidebar_view.trailingAnchor()),
            self.content_area.topAnchor().constraintEqualToAnchor_(main_view.topAnchor()),
            self.content_area.trailingAnchor().constraintEqualToAnchor_(main_view.trailingAnchor()),
            self.content_area.bottomAnchor().constraintEqualToAnchor_(main_view.bottomAnchor())
        ])
        
        # Header constraints
        self.header_view.setTranslatesAutoresizingMaskIntoConstraints_(False)
        NSLayoutConstraint.activateConstraints_([
            self.header_view.leadingAnchor().constraintEqualToAnchor_(self.content_area.leadingAnchor()),
            self.header_view.topAnchor().constraintEqualToAnchor_(self.content_area.topAnchor()),
            self.header_view.trailingAnchor().constraintEqualToAnchor_(self.content_area.trailingAnchor()),
            self.header_view.heightAnchor().constraintEqualToConstant_(50)
        ])
        
        # View constraints
        for view in [self.readings_view, self.chat_view, self.history_view, self.settings_view]:
            view.setTranslatesAutoresizingMaskIntoConstraints_(False)
            NSLayoutConstraint.activateConstraints_([
                view.leadingAnchor().constraintEqualToAnchor_(self.content_area.leadingAnchor()),
                view.topAnchor().constraintEqualToAnchor_(self.header_view.bottomAnchor()),
                view.trailingAnchor().constraintEqualToAnchor_(self.content_area.trailingAnchor()),
                view.bottomAnchor().constraintEqualToAnchor_(self.content_area.bottomAnchor())
            ])
    
    def showReadingsView(self):
        """Show the readings view."""
        self.hideAllViews()
        self.readings_view.setHidden_(False)
        self.current_view = self.readings_view
        self.sidebar_view.setActiveTab_("readings")
    
    def showChatView(self):
        """Show the chat view."""
        self.hideAllViews()
        self.chat_view.setHidden_(False)
        self.current_view = self.chat_view
        self.sidebar_view.setActiveTab_("chat")
    
    def showHistoryView(self):
        """Show the history view."""
        self.hideAllViews()
        self.history_view.setHidden_(False)
        self.current_view = self.history_view
        self.sidebar_view.setActiveTab_("history")
    
    def showSettingsView(self):
        """Show the settings view."""
        self.hideAllViews()
        self.settings_view.setHidden_(False)
        self.current_view = self.settings_view
        self.sidebar_view.setActiveTab_("settings")
    
    def hideAllViews(self):
        """Hide all content views."""
        for view in [self.readings_view, self.chat_view, self.history_view, self.settings_view]:
            view.setHidden_(True)
    
    def updateAIStatus(self, status):
        """Update AI status in header."""
        self.ai_status_label.setStringValue_(f"AI: {status}")
    
    # Sidebar delegate methods
    def sidebarDidSelectTab_(self, tab_name):
        """Handle sidebar tab selection."""
        if tab_name == "readings":
            self.showReadingsView()
        elif tab_name == "chat":
            self.showChatView()
        elif tab_name == "history":
            self.showHistoryView()
        elif tab_name == "settings":
            self.showSettingsView()
    
    # Window delegate methods
    def windowShouldClose_(self, sender):
        """Handle window close."""
        # Save any pending changes
        if self.session:
            try:
                self.session.commit()
            except Exception as e:
                logger.error(f"Failed to save changes: {e}")
        
        return True
    
    def windowWillClose_(self, notification):
        """Handle window will close."""
        # Clean up resources
        if self.session:
            self.session.close()
        
        # Quit application
        NSApp.terminate_(self)

# App delegate
class AppDelegate(NSObject):
    """Application delegate."""
    
    def applicationDidFinishLaunching_(self, notification):
        """Handle application launch."""
        # Create and show main window
        main_window = MainWindow.alloc().init()
        main_window.makeKeyAndOrderFront_(None)
        
        # Store reference to prevent garbage collection
        self.main_window = main_window
    
    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        """Quit when last window is closed."""
        return True

def run_app():
    """Run the application."""
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
    
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    
    app.run()