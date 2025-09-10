"""
Sidebar component for Tarot Studio application.
"""

import objc
from Foundation import *
from AppKit import *
from Cocoa import *
import logging

logger = logging.getLogger(__name__)

class SidebarView(NSView):
    """Sidebar with navigation tabs."""
    
    def init(self):
        """Initialize the sidebar."""
        self = super(SidebarView, self).init()
        
        if self:
            self.setWantsLayer_(True)
            self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
            
            # Initialize properties
            self.delegate = None
            self.active_tab = "readings"
            self.tabs = []
            
            # Create tabs
            self.createTabs()
            
        return self
    
    def initWithFrame_(self, frame):
        """Initialize with frame."""
        self = super(SidebarView, self).initWithFrame_(frame)
        
        if self:
            self.setWantsLayer_(True)
            self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
            
            # Initialize properties
            self.delegate = None
            self.active_tab = "readings"
            self.tabs = []
            
            # Create tabs
            self.createTabs()
            
        return self
    
    def createTabs(self):
        """Create navigation tabs."""
        tab_configs = [
            {
                'id': 'readings',
                'title': 'Readings',
                'icon': '📖',
                'description': 'Draw and interpret tarot cards'
            },
            {
                'id': 'chat',
                'title': 'Chat',
                'icon': '💬',
                'description': 'Chat with AI about readings'
            },
            {
                'id': 'history',
                'title': 'History',
                'icon': '📚',
                'description': 'View past readings'
            },
            {
                'id': 'settings',
                'title': 'Settings',
                'icon': '⚙️',
                'description': 'App preferences and configuration'
            }
        ]
        
        y_offset = 20
        tab_height = 60
        
        for i, config in enumerate(tab_configs):
            tab_view = self.createTabView(config, NSMakeRect(10, y_offset, 180, tab_height))
            self.addSubview_(tab_view)
            self.tabs.append(tab_view)
            
            y_offset += tab_height + 10
    
    def createTabView(self, config, frame):
        """Create a single tab view."""
        tab_view = NSView.alloc().initWithFrame_(frame)
        tab_view.setWantsLayer_(True)
        tab_view.layer().setCornerRadius_(8)
        tab_view.layer().setBackgroundColor_(NSColor.clearColor().CGColor())
        
        # Set up hover tracking
        tracking_area = NSTrackingArea.alloc().initWithRect_options_owner_userInfo_(
            frame,
            NSTrackingMouseEnteredAndExited | NSTrackingActiveInKeyWindow,
            tab_view,
            None
        )
        tab_view.addTrackingArea_(tracking_area)
        
        # Icon label
        icon_label = NSTextField.alloc().initWithFrame_(NSMakeRect(15, 35, 30, 20))
        icon_label.setStringValue_(config['icon'])
        icon_label.setBordered_(False)
        icon_label.setDrawsBackground_(False)
        icon_label.setEditable_(False)
        icon_label.setSelectable_(False)
        icon_label.setFont_(NSFont.systemFontOfSize_(20))
        icon_label.setTextColor_(NSColor.labelColor())
        
        # Title label
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(50, 35, 120, 20))
        title_label.setStringValue_(config['title'])
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(14, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Description label
        desc_label = NSTextField.alloc().initWithFrame_(NSMakeRect(15, 15, 155, 15))
        desc_label.setStringValue_(config['description'])
        desc_label.setBordered_(False)
        desc_label.setDrawsBackground_(False)
        desc_label.setEditable_(False)
        desc_label.setSelectable_(False)
        desc_label.setFont_(NSFont.systemFontOfSize_(10))
        desc_label.setTextColor_(NSColor.secondaryLabelColor())
        
        # Add subviews
        tab_view.addSubview_(icon_label)
        tab_view.addSubview_(title_label)
        tab_view.addSubview_(desc_label)
        
        # Store configuration
        tab_view.tab_id = config['id']
        tab_view.tab_config = config
        tab_view.icon_label = icon_label
        tab_view.title_label = title_label
        tab_view.desc_label = desc_label
        
        # Set up click handling
        tab_view.setTarget_(self)
        tab_view.setAction_('tabClicked:')
        
        # Update appearance
        self.updateTabAppearance(tab_view)
        
        return tab_view
    
    def updateTabAppearance(self, tab_view):
        """Update tab appearance based on active state."""
        is_active = tab_view.tab_id == self.active_tab
        
        if is_active:
            # Active tab styling
            tab_view.layer().setBackgroundColor_(NSColor.selectedControlColor().CGColor())
            tab_view.title_label.setTextColor_(NSColor.alternateSelectedControlTextColor())
            tab_view.icon_label.setTextColor_(NSColor.alternateSelectedControlTextColor())
            tab_view.desc_label.setTextColor_(NSColor.alternateSelectedControlTextColor())
        else:
            # Inactive tab styling
            tab_view.layer().setBackgroundColor_(NSColor.clearColor().CGColor())
            tab_view.title_label.setTextColor_(NSColor.labelColor())
            tab_view.icon_label.setTextColor_(NSColor.labelColor())
            tab_view.desc_label.setTextColor_(NSColor.secondaryLabelColor())
    
    def setActiveTab_(self, tab_id):
        """Set the active tab."""
        self.active_tab = tab_id
        
        # Update all tab appearances
        for tab_view in self.tabs:
            self.updateTabAppearance(tab_view)
    
    def tabClicked_(self, sender):
        """Handle tab click."""
        tab_id = sender.tab_id
        
        if tab_id != self.active_tab:
            self.setActiveTab_(tab_id)
            
            # Notify delegate
            if self.delegate and hasattr(self.delegate, 'sidebarDidSelectTab_'):
                self.delegate.sidebarDidSelectTab_(tab_id)
    
    def mouseEntered_(self, event):
        """Handle mouse entered event."""
        # Find the tab view under the mouse
        mouse_point = self.convertPoint_fromView_(event.locationInWindow(), None)
        
        for tab_view in self.tabs:
            if NSPointInRect(mouse_point, tab_view.frame()):
                if tab_view.tab_id != self.active_tab:
                    # Show hover effect
                    tab_view.layer().setBackgroundColor_(NSColor.controlHighlightColor().CGColor())
                break
    
    def mouseExited_(self, event):
        """Handle mouse exited event."""
        # Reset all tab appearances
        for tab_view in self.tabs:
            self.updateTabAppearance(tab_view)
    
    def setDelegate_(self, delegate):
        """Set the delegate."""
        self.delegate = delegate
    
    def setSession_ollamaClient_memoryStore_(self, session, ollama_client, memory_store):
        """Set dependencies."""
        self.session = session
        self.ollama_client = ollama_client
        self.memory_store = memory_store