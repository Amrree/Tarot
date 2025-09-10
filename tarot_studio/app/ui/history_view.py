"""
History view for Tarot Studio application.
"""

import objc
from Foundation import *
from AppKit import *
from Cocoa import *
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HistoryView(NSView):
    """History view for past readings."""
    
    def init(self):
        """Initialize the history view."""
        self = super(HistoryView, self).init()
        
        if self:
            self.setWantsLayer_(True)
            self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
            
            # Initialize properties
            self.session = None
            self.ollama_client = None
            self.memory_store = None
            self.readings = []
            
            # Create UI components
            self.createUI()
            
        return self
    
    def initWithFrame_(self, frame):
        """Initialize with frame."""
        self = super(HistoryView, self).initWithFrame_(frame)
        
        if self:
            self.setWantsLayer_(True)
            self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
            
            # Initialize properties
            self.session = None
            self.ollama_client = None
            self.memory_store = None
            self.readings = []
            
            # Create UI components
            self.createUI()
            
        return self
    
    def createUI(self):
        """Create the UI components."""
        # Title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 750, 200, 20))
        title_label.setStringValue_("Reading History")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(16, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Search field
        self.search_field = NSSearchField.alloc().initWithFrame_(NSMakeRect(20, 710, 300, 30))
        self.search_field.setPlaceholderString_("Search readings...")
        self.search_field.setTarget_(self)
        self.search_field.setAction_('searchReadings:')
        
        # Readings table
        self.readings_table = NSTableView.alloc().initWithFrame_(NSMakeRect(20, 200, 960, 480))
        self.readings_table.setHeaderView_(None)
        self.readings_table.setRowSizeStyle_(NSTableViewRowSizeStyleDefault)
        
        # Date column
        date_column = NSTableColumn.alloc().initWithIdentifier_("date")
        date_column.setTitle_("Date")
        date_column.setWidth_(150)
        date_column.setMinWidth_(100)
        date_column.setMaxWidth_(200)
        
        # Title column
        title_column = NSTableColumn.alloc().initWithIdentifier_("title")
        title_column.setTitle_("Title")
        title_column.setWidth_(300)
        title_column.setMinWidth_(200)
        title_column.setMaxWidth_(400)
        
        # Spread column
        spread_column = NSTableColumn.alloc().initWithIdentifier_("spread")
        spread_column.setTitle_("Spread")
        spread_column.setWidth_(150)
        spread_column.setMinWidth_(100)
        spread_column.setMaxWidth_(200)
        
        # Cards column
        cards_column = NSTableColumn.alloc().initWithIdentifier_("cards")
        cards_column.setTitle_("Cards")
        cards_column.setWidth_(360)
        cards_column.setMinWidth_(200)
        cards_column.setMaxWidth_(500)
        
        self.readings_table.addTableColumn_(date_column)
        self.readings_table.addTableColumn_(title_column)
        self.readings_table.addTableColumn_(spread_column)
        self.readings_table.addTableColumn_(cards_column)
        
        self.readings_table.setDataSource_(self)
        self.readings_table.setDelegate_(self)
        
        # Scroll view for table
        self.table_scroll = NSScrollView.alloc().initWithFrame_(NSMakeRect(20, 200, 960, 480))
        self.table_scroll.setDocumentView_(self.readings_table)
        self.table_scroll.setHasVerticalScroller_(True)
        self.table_scroll.setHasHorizontalScroller_(False)
        self.table_scroll.setAutohidesScrollers_(True)
        
        # Detail view
        self.detail_view = NSView.alloc().initWithFrame_(NSMakeRect(20, 20, 960, 160))
        self.detail_view.setWantsLayer_(True)
        self.detail_view.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        self.detail_view.layer().setCornerRadius_(8)
        
        # Detail text
        self.detail_text = NSTextView.alloc().initWithFrame_(NSMakeRect(20, 20, 920, 120))
        self.detail_text.setString_("Select a reading to view details...")
        self.detail_text.setEditable_(False)
        self.detail_text.setSelectable_(True)
        self.detail_text.setFont_(NSFont.systemFontOfSize_(12))
        self.detail_text.setTextColor_(NSColor.labelColor())
        self.detail_text.setBackgroundColor_(NSColor.clearColor())
        
        # Add subviews
        self.addSubview_(title_label)
        self.addSubview_(self.search_field)
        self.addSubview_(self.table_scroll)
        self.addSubview_(self.detail_view)
        
        self.detail_view.addSubview_(self.detail_text)
        
        # Load readings
        self.loadReadings()
    
    def loadReadings(self):
        """Load readings from database."""
        if not self.session:
            return
        
        from tarot_studio.db.models import Reading, ReadingCard, Card
        
        # Get all readings
        readings = self.session.query(Reading).order_by(Reading.created_at.desc()).all()
        
        self.readings = []
        for reading in readings:
            # Get cards for this reading
            reading_cards = self.session.query(ReadingCard).filter_by(reading_id=reading.id).all()
            
            cards_info = []
            for rc in reading_cards:
                card = self.session.query(Card).filter_by(id=rc.card_id).first()
                if card:
                    orientation = " (R)" if rc.orientation == "reversed" else ""
                    cards_info.append(f"{card.name}{orientation}")
            
            reading_data = {
                'id': reading.id,
                'title': reading.title,
                'spread_id': reading.spread_id,
                'created_at': reading.created_at,
                'cards': cards_info,
                'interpretation': reading.interpretation,
                'summary': reading.summary
            }
            self.readings.append(reading_data)
        
        # Reload table
        self.readings_table.reloadData()
    
    def searchReadings_(self, sender):
        """Handle search field changes."""
        search_term = self.search_field.stringValue().lower()
        
        if not search_term:
            self.loadReadings()
            return
        
        # Filter readings
        filtered_readings = []
        for reading in self.readings:
            if (search_term in reading['title'].lower() or
                search_term in reading['spread_id'].lower() or
                any(search_term in card.lower() for card in reading['cards'])):
                filtered_readings.append(reading)
        
        self.readings = filtered_readings
        self.readings_table.reloadData()
    
    # NSTableViewDataSource methods
    def numberOfRowsInTableView_(self, tableView):
        """Return number of rows in table."""
        return len(self.readings)
    
    def tableView_objectValueForTableColumn_row_(self, tableView, column, row):
        """Return value for table cell."""
        if row >= len(self.readings):
            return None
        
        reading = self.readings[row]
        column_id = column.identifier()
        
        if column_id == "date":
            return reading['created_at'].strftime("%Y-%m-%d %H:%M")
        elif column_id == "title":
            return reading['title']
        elif column_id == "spread":
            return reading['spread_id'].replace('_', ' ').title()
        elif column_id == "cards":
            return ", ".join(reading['cards'])
        
        return None
    
    # NSTableViewDelegate methods
    def tableViewSelectionDidChange_(self, notification):
        """Handle table selection change."""
        selected_row = self.readings_table.selectedRow()
        
        if selected_row >= 0 and selected_row < len(self.readings):
            reading = self.readings[selected_row]
            self.displayReadingDetails(reading)
    
    def displayReadingDetails(self, reading):
        """Display reading details."""
        details = f"Reading: {reading['title']}\n"
        details += f"Date: {reading['created_at'].strftime('%Y-%m-%d %H:%M')}\n"
        details += f"Spread: {reading['spread_id'].replace('_', ' ').title()}\n\n"
        
        details += "Cards:\n"
        for card in reading['cards']:
            details += f"• {card}\n"
        
        if reading['summary']:
            details += f"\nSummary:\n{reading['summary']}\n"
        
        if reading['interpretation']:
            details += f"\nInterpretation:\n{reading['interpretation']}\n"
        
        self.detail_text.setString_(details)
    
    def setSession_ollamaClient_memoryStore_(self, session, ollama_client, memory_store):
        """Set dependencies."""
        self.session = session
        self.ollama_client = ollama_client
        self.memory_store = memory_store