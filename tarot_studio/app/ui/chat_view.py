"""
Chat view for Tarot Studio application.
"""

import objc
from Foundation import *
from AppKit import *
from Cocoa import *
import logging

logger = logging.getLogger(__name__)

class ChatView(NSView):
    """Chat view for AI conversations."""
    
    def init(self):
        """Initialize the chat view."""
        self = super(ChatView, self).init()
        
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
        self = super(ChatView, self).initWithFrame_(frame)
        
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
        title_label.setStringValue_("Chat with AI")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(16, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Chat area
        self.chat_area = NSScrollView.alloc().initWithFrame_(NSMakeRect(20, 200, 960, 500))
        self.chat_area.setHasVerticalScroller_(True)
        self.chat_area.setHasHorizontalScroller_(False)
        self.chat_area.setAutohidesScrollers_(True)
        
        # Chat text view
        self.chat_text = NSTextView.alloc().initWithFrame_(NSMakeRect(0, 0, 960, 500))
        self.chat_text.setString_("Welcome to Tarot Studio Chat!\n\nAsk me about your readings, cards, or anything tarot-related.")
        self.chat_text.setEditable_(False)
        self.chat_text.setSelectable_(True)
        self.chat_text.setFont_(NSFont.monospacedSystemFontOfSize_weight_(12, NSFontWeightRegular))
        self.chat_text.setTextColor_(NSColor.labelColor())
        self.chat_text.setBackgroundColor_(NSColor.clearColor())
        
        self.chat_area.setDocumentView_(self.chat_text)
        
        # Input area
        self.input_area = NSView.alloc().initWithFrame_(NSMakeRect(20, 20, 960, 160))
        self.input_area.setWantsLayer_(True)
        self.input_area.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        self.input_area.layer().setCornerRadius_(8)
        
        # Input text field
        self.input_field = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 100, 800, 40))
        self.input_field.setPlaceholderString_("Type your question...")
        self.input_field.setTarget_(self)
        self.input_field.setAction_('sendMessage:')
        
        # Send button
        self.send_button = NSButton.alloc().initWithFrame_(NSMakeRect(840, 100, 100, 40))
        self.send_button.setTitle_("Send")
        self.send_button.setTarget_(self)
        self.send_button.setAction_('sendMessage:')
        self.send_button.setBordered_(True)
        self.send_button.setBezelStyle_(NSBezelStyleRounded)
        
        # Memory toggle
        self.memory_toggle = NSButton.alloc().initWithFrame_(NSMakeRect(20, 60, 200, 30))
        self.memory_toggle.setTitle_("Enable Memory")
        self.memory_toggle.setButtonType_(NSButtonTypeSwitch)
        self.memory_toggle.setState_(NSControlStateValueOn)
        
        # Context label
        self.context_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 20, 920, 30))
        self.context_label.setStringValue_("No active reading context")
        self.context_label.setBordered_(False)
        self.context_label.setDrawsBackground_(False)
        self.context_label.setEditable_(False)
        self.context_label.setSelectable_(False)
        self.context_label.setFont_(NSFont.systemFontOfSize_(12))
        self.context_label.setTextColor_(NSColor.secondaryLabelColor())
        
        # Add subviews
        self.addSubview_(title_label)
        self.addSubview_(self.chat_area)
        self.addSubview_(self.input_area)
        
        self.input_area.addSubview_(self.input_field)
        self.input_area.addSubview_(self.send_button)
        self.input_area.addSubview_(self.memory_toggle)
        self.input_area.addSubview_(self.context_label)
    
    def sendMessage_(self, sender):
        """Send a message to the AI."""
        message = self.input_field.stringValue()
        if not message.strip():
            return
        
        # Add user message to chat
        self.addMessageToChat("You", message)
        
        # Clear input
        self.input_field.setStringValue_("")
        
        # Generate AI response
        self.generateAIResponse(message)
    
    def addMessageToChat(self, sender, message):
        """Add a message to the chat area."""
        current_text = self.chat_text.string()
        new_text = f"{current_text}\n> {sender}: {message}"
        self.chat_text.setString_(new_text)
        
        # Scroll to bottom
        self.chat_area.contentView().scrollToPoint_(NSMakePoint(0, self.chat_text.frame().size.height))
    
    def generateAIResponse(self, message):
        """Generate AI response."""
        # Add thinking indicator
        self.addMessageToChat("AI", "Thinking...")
        
        # Generate response (placeholder for now)
        response = "I'm here to help with your tarot questions! What would you like to know?"
        
        # Replace thinking message with actual response
        current_text = self.chat_text.string()
        new_text = current_text.replace("> AI: Thinking...", f"> AI: {response}")
        self.chat_text.setString_(new_text)
    
    def setSession_ollamaClient_memoryStore_(self, session, ollama_client, memory_store):
        """Set dependencies."""
        self.session = session
        self.ollama_client = ollama_client
        self.memory_store = memory_store