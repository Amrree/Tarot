"""
Readings view for Tarot Studio application.
"""

import objc
from Foundation import *
from AppKit import *
from Cocoa import *
import logging
import random
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ReadingsView(NSView):
    """Main readings view with draw panel and card display."""
    
    def init(self):
        """Initialize the readings view."""
        self = super(ReadingsView, self).init()
        
        if self:
            self.setWantsLayer_(True)
            self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
            
            # Initialize properties
            self.session = None
            self.ollama_client = None
            self.memory_store = None
            self.current_spread = None
            self.drawn_cards = []
            
            # Create UI components
            self.createUI()
            
        return self
    
    def initWithFrame_(self, frame):
        """Initialize with frame."""
        self = super(ReadingsView, self).initWithFrame_(frame)
        
        if self:
            self.setWantsLayer_(True)
            self.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
            
            # Initialize properties
            self.session = None
            self.ollama_client = None
            self.memory_store = None
            self.current_spread = None
            self.drawn_cards = []
            
            # Create UI components
            self.createUI()
            
        return self
    
    def createUI(self):
        """Create the UI components."""
        # Draw panel
        self.draw_panel = self.createDrawPanel()
        self.addSubview_(self.draw_panel)
        
        # Card display area
        self.card_display = self.createCardDisplay()
        self.addSubview_(self.card_display)
        
        # Interpretation panel
        self.interpretation_panel = self.createInterpretationPanel()
        self.addSubview_(self.interpretation_panel)
        
        # Set up constraints
        self.setupConstraints()
    
    def createDrawPanel(self):
        """Create the draw panel with spread selection."""
        panel = NSView.alloc().initWithFrame_(NSMakeRect(20, 600, 960, 120))
        panel.setWantsLayer_(True)
        panel.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        panel.layer().setCornerRadius_(8)
        
        # Title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 90, 200, 20))
        title_label.setStringValue_("Choose a Spread")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(16, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Spread buttons
        spreads = [
            {'id': 'single_card', 'name': 'Single Card'},
            {'id': 'three_card', 'name': 'Three Card'},
            {'id': 'celtic_cross', 'name': 'Celtic Cross'},
            {'id': 'relationship_cross', 'name': 'Relationship'}
        ]
        
        button_width = 120
        button_height = 40
        button_spacing = 20
        start_x = 20
        start_y = 40
        
        self.spread_buttons = []
        
        for i, spread in enumerate(spreads):
            button = NSButton.alloc().initWithFrame_(
                NSMakeRect(start_x + i * (button_width + button_spacing), start_y, button_width, button_height)
            )
            button.setTitle_(spread['name'])
            button.setTarget_(self)
            button.setAction_('selectSpread:')
            button.setTag_(i)
            button.setBordered_(True)
            button.setBezelStyle_(NSBezelStyleRounded)
            
            # Store spread info
            button.spread_id = spread['id']
            button.spread_name = spread['name']
            
            panel.addSubview_(button)
            self.spread_buttons.append(button)
        
        # Draw button
        self.draw_button = NSButton.alloc().initWithFrame_(NSMakeRect(800, 40, 120, 40))
        self.draw_button.setTitle_("Draw Cards")
        self.draw_button.setTarget_(self)
        self.draw_button.setAction_('drawCards:')
        self.draw_button.setBordered_(True)
        self.draw_button.setBezelStyle_(NSBezelStyleRounded)
        self.draw_button.setEnabled_(False)
        
        panel.addSubview_(title_label)
        panel.addSubview_(self.draw_button)
        
        return panel
    
    def createCardDisplay(self):
        """Create the card display area."""
        display = NSView.alloc().initWithFrame_(NSMakeRect(20, 200, 960, 380))
        display.setWantsLayer_(True)
        display.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        display.layer().setCornerRadius_(8)
        
        # Title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 350, 200, 20))
        title_label.setStringValue_("Your Reading")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(16, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Card slots
        self.card_slots = []
        card_width = 120
        card_height = 180
        card_spacing = 20
        start_x = 50
        start_y = 100
        
        # Create card slots based on current spread
        self.createCardSlots(display, start_x, start_y, card_width, card_height, card_spacing)
        
        display.addSubview_(title_label)
        
        return display
    
    def createCardSlots(self, parent_view, start_x, start_y, card_width, card_height, card_spacing):
        """Create card slots for the current spread."""
        # Clear existing slots
        for slot in self.card_slots:
            slot.removeFromSuperview()
        self.card_slots = []
        
        # Determine number of cards based on spread
        num_cards = 1  # Default to single card
        if self.current_spread == 'three_card':
            num_cards = 3
        elif self.current_spread == 'celtic_cross':
            num_cards = 10
        elif self.current_spread == 'relationship_cross':
            num_cards = 7
        
        # Create card slots
        for i in range(num_cards):
            slot = self.createCardSlot(
                NSMakeRect(start_x + i * (card_width + card_spacing), start_y, card_width, card_height),
                i
            )
            parent_view.addSubview_(slot)
            self.card_slots.append(slot)
    
    def createCardSlot(self, frame, index):
        """Create a single card slot."""
        slot = NSView.alloc().initWithFrame_(frame)
        slot.setWantsLayer_(True)
        slot.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        slot.layer().setBorderWidth_(2)
        slot.layer().setBorderColor_(NSColor.separatorColor().CGColor())
        slot.layer().setCornerRadius_(8)
        
        # Position label
        position_label = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 10, 100, 20))
        position_label.setStringValue_(f"Position {index + 1}")
        position_label.setBordered_(False)
        position_label.setDrawsBackground_(False)
        position_label.setEditable_(False)
        position_label.setSelectable_(False)
        position_label.setFont_(NSFont.systemFontOfSize_(12))
        position_label.setTextColor_(NSColor.secondaryLabelColor())
        
        # Card placeholder
        card_placeholder = NSTextField.alloc().initWithFrame_(NSMakeRect(10, 40, 100, 120))
        card_placeholder.setStringValue_("Card will appear here")
        card_placeholder.setBordered_(False)
        card_placeholder.setDrawsBackground_(False)
        card_placeholder.setEditable_(False)
        card_placeholder.setSelectable_(False)
        card_placeholder.setFont_(NSFont.systemFontOfSize_(10))
        card_placeholder.setTextColor_(NSColor.tertiaryLabelColor())
        card_placeholder.setAlignment_(NSTextAlignmentCenter)
        
        slot.addSubview_(position_label)
        slot.addSubview_(card_placeholder)
        
        # Store slot info
        slot.slot_index = index
        slot.position_label = position_label
        slot.card_placeholder = card_placeholder
        slot.card_data = None
        
        return slot
    
    def createInterpretationPanel(self):
        """Create the interpretation panel."""
        panel = NSView.alloc().initWithFrame_(NSMakeRect(20, 20, 960, 160))
        panel.setWantsLayer_(True)
        panel.layer().setBackgroundColor_(NSColor.controlBackgroundColor().CGColor())
        panel.layer().setCornerRadius_(8)
        
        # Title
        title_label = NSTextField.alloc().initWithFrame_(NSMakeRect(20, 130, 200, 20))
        title_label.setStringValue_("Interpretation")
        title_label.setBordered_(False)
        title_label.setDrawsBackground_(False)
        title_label.setEditable_(False)
        title_label.setSelectable_(False)
        title_label.setFont_(NSFont.systemFontOfSize_(16, NSFontWeightMedium))
        title_label.setTextColor_(NSColor.labelColor())
        
        # Interpretation text
        self.interpretation_text = NSTextView.alloc().initWithFrame_(NSMakeRect(20, 20, 920, 100))
        self.interpretation_text.setString_("Draw cards to see your interpretation...")
        self.interpretation_text.setEditable_(False)
        self.interpretation_text.setSelectable_(True)
        self.interpretation_text.setFont_(NSFont.systemFontOfSize_(12))
        self.interpretation_text.setTextColor_(NSColor.labelColor())
        self.interpretation_text.setBackgroundColor_(NSColor.clearColor())
        
        panel.addSubview_(title_label)
        panel.addSubview_(self.interpretation_text)
        
        return panel
    
    def setupConstraints(self):
        """Set up Auto Layout constraints."""
        self.draw_panel.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.card_display.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.interpretation_panel.setTranslatesAutoresizingMaskIntoConstraints_(False)
        
        NSLayoutConstraint.activateConstraints_([
            # Draw panel
            self.draw_panel.leadingAnchor().constraintEqualToAnchor_(self.leadingAnchor(), constant=20),
            self.draw_panel.trailingAnchor().constraintEqualToAnchor_(self.trailingAnchor(), constant=-20),
            self.draw_panel.topAnchor().constraintEqualToAnchor_(self.topAnchor(), constant=20),
            self.draw_panel.heightAnchor().constraintEqualToConstant_(120),
            
            # Card display
            self.card_display.leadingAnchor().constraintEqualToAnchor_(self.leadingAnchor(), constant=20),
            self.card_display.trailingAnchor().constraintEqualToAnchor_(self.trailingAnchor(), constant=-20),
            self.card_display.topAnchor().constraintEqualToAnchor_(self.draw_panel.bottomAnchor(), constant=20),
            self.card_display.heightAnchor().constraintEqualToConstant_(380),
            
            # Interpretation panel
            self.interpretation_panel.leadingAnchor().constraintEqualToAnchor_(self.leadingAnchor(), constant=20),
            self.interpretation_panel.trailingAnchor().constraintEqualToAnchor_(self.trailingAnchor(), constant=-20),
            self.interpretation_panel.topAnchor().constraintEqualToAnchor_(self.card_display.bottomAnchor(), constant=20),
            self.interpretation_panel.bottomAnchor().constraintEqualToAnchor_(self.bottomAnchor(), constant=-20)
        ])
    
    def selectSpread_(self, sender):
        """Handle spread selection."""
        # Update button states
        for button in self.spread_buttons:
            if button == sender:
                button.setBordered_(True)
                button.setBezelStyle_(NSBezelStyleRounded)
            else:
                button.setBordered_(False)
                button.setBezelStyle_(NSBezelStyleRounded)
        
        # Set current spread
        self.current_spread = sender.spread_id
        
        # Update card slots
        self.createCardSlots(self.card_display, 50, 100, 120, 180, 20)
        
        # Enable draw button
        self.draw_button.setEnabled_(True)
        
        logger.info(f"Selected spread: {sender.spread_name}")
    
    def drawCards_(self, sender):
        """Handle card drawing."""
        if not self.current_spread:
            return
        
        # Clear previous cards
        self.drawn_cards = []
        
        # Draw cards
        if self.session:
            cards = self.getRandomCards(len(self.card_slots))
            
            for i, card in enumerate(cards):
                if i < len(self.card_slots):
                    slot = self.card_slots[i]
                    self.displayCardInSlot(card, slot)
                    self.drawn_cards.append(card)
        
        # Generate interpretation
        self.generateInterpretation()
        
        logger.info(f"Drew {len(self.drawn_cards)} cards for {self.current_spread} spread")
    
    def getRandomCards(self, count):
        """Get random cards from the database."""
        if not self.session:
            return []
        
        from tarot_studio.db.models import Card
        
        # Get all cards
        all_cards = self.session.query(Card).all()
        
        # Select random cards
        selected_cards = random.sample(all_cards, min(count, len(all_cards)))
        
        # Convert to dict format
        cards = []
        for card in selected_cards:
            card_dict = {
                'id': card.id,
                'name': card.name,
                'arcana': card.arcana,
                'suit': card.suit,
                'number': card.number,
                'element': card.element,
                'keywords': card.keywords,
                'polarity': card.polarity,
                'intensity': card.intensity,
                'upright_meaning': card.upright_meaning,
                'reversed_meaning': card.reversed_meaning,
                'influence_rules': card.influence_rules,
                'orientation': random.choice(['upright', 'reversed'])
            }
            cards.append(card_dict)
        
        return cards
    
    def displayCardInSlot(self, card, slot):
        """Display a card in a slot."""
        # Update slot appearance
        slot.layer().setBorderColor_(NSColor.controlAccentColor().CGColor())
        
        # Update position label
        slot.position_label.setStringValue_(card['name'])
        slot.position_label.setTextColor_(NSColor.labelColor())
        
        # Update card placeholder
        orientation_text = " (Reversed)" if card['orientation'] == 'reversed' else ""
        slot.card_placeholder.setStringValue_(f"{card['name']}{orientation_text}")
        slot.card_placeholder.setTextColor_(NSColor.labelColor())
        
        # Store card data
        slot.card_data = card
    
    def generateInterpretation(self):
        """Generate interpretation for the drawn cards."""
        if not self.drawn_cards:
            return
        
        # Create spread data for AI
        spread_data = {
            'reading_id': f"reading_{random.randint(1000, 9999)}",
            'spread_name': self.current_spread.replace('_', ' ').title(),
            'cards': []
        }
        
        for i, card in enumerate(self.drawn_cards):
            card_info = {
                'position': f"position_{i+1}",
                'card': f"{card['name']} ({card['orientation']})",
                'orientation': card['orientation'],
                'meaning': card['upright_meaning'] if card['orientation'] == 'upright' else card['reversed_meaning']
            }
            spread_data['cards'].append(card_info)
        
        # Generate interpretation using AI
        if self.ollama_client:
            import asyncio
            
            async def get_interpretation():
                try:
                    response = await self.ollama_client.generate_reading_interpretation(spread_data)
                    return response
                except Exception as e:
                    logger.error(f"Failed to generate interpretation: {e}")
                    return None
            
            # Run async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(get_interpretation())
                if response:
                    self.displayInterpretation(response)
                else:
                    self.displayFallbackInterpretation()
            finally:
                loop.close()
        else:
            self.displayFallbackInterpretation()
    
    def displayInterpretation(self, response):
        """Display AI-generated interpretation."""
        interpretation_text = f"Summary: {response.summary}\n\n"
        
        if response.advice:
            interpretation_text += "Advice:\n"
            for advice in response.advice:
                interpretation_text += f"• {advice}\n"
            interpretation_text += "\n"
        
        if response.follow_up_questions:
            interpretation_text += "Questions to consider:\n"
            for question in response.follow_up_questions:
                interpretation_text += f"• {question}\n"
        
        self.interpretation_text.setString_(interpretation_text)
    
    def displayFallbackInterpretation(self):
        """Display fallback interpretation when AI is not available."""
        interpretation_text = "Your Reading:\n\n"
        
        for i, card in enumerate(self.drawn_cards):
            position_name = f"Position {i+1}"
            meaning = card['upright_meaning'] if card['orientation'] == 'upright' else card['reversed_meaning']
            
            interpretation_text += f"{position_name}: {card['name']} ({card['orientation']})\n"
            interpretation_text += f"{meaning}\n\n"
        
        interpretation_text += "Consider how these cards work together to tell your story."
        
        self.interpretation_text.setString_(interpretation_text)
    
    def setSession_ollamaClient_memoryStore_(self, session, ollama_client, memory_store):
        """Set dependencies."""
        self.session = session
        self.ollama_client = ollama_client
        self.memory_store = memory_store