"""
Tarot Spread Management

This module provides the TarotSpread class that manages a complete tarot spread
with cards, positions, and integration with the deck and influence engine.
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from .spread_layout import SpreadLayout, SpreadPosition
from ..deck import Deck, Card, Orientation
from ..core.enhanced_influence_engine import EnhancedInfluenceEngine, EngineConfig


@dataclass
class SpreadCard:
    """
    Represents a card in a specific position within a spread.
    
    Attributes:
        position: The position this card occupies
        card: The actual tarot card
        drawn_at: When the card was drawn
        notes: Optional user notes for this card
    """
    position: SpreadPosition
    card: Card
    drawn_at: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert spread card to dictionary."""
        return {
            'position_id': self.position.id,
            'position_name': self.position.name,
            'card_id': self.card.id,
            'card_name': self.card.name,
            'orientation': self.card.orientation.value,
            'drawn_at': self.drawn_at.isoformat(),
            'notes': self.notes
        }


@dataclass
class SpreadReading:
    """
    Represents a complete tarot reading with influenced meanings.
    
    Attributes:
        spread_id: Unique identifier for this reading
        layout: The spread layout used
        cards: List of cards in their positions
        influenced_meanings: Results from the influence engine
        reading_date: When the reading was performed
        user_context: Optional user question or context
        notes: Optional user notes for the reading
    """
    spread_id: str
    layout: SpreadLayout
    cards: List[SpreadCard] = field(default_factory=list)
    influenced_meanings: Optional[Dict[str, Any]] = None
    reading_date: datetime = field(default_factory=datetime.now)
    user_context: Optional[str] = None
    notes: Optional[str] = None
    
    def get_card_by_position(self, position_id: str) -> Optional[SpreadCard]:
        """Get a card by its position ID."""
        for spread_card in self.cards:
            if spread_card.position.id == position_id:
                return spread_card
        return None
    
    def get_cards_by_type(self, position_type) -> List[SpreadCard]:
        """Get all cards of a specific position type."""
        return [sc for sc in self.cards if sc.position.position_type == position_type]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reading to dictionary."""
        return {
            'spread_id': self.spread_id,
            'layout': self.layout.to_dict(),
            'cards': [card.to_dict() for card in self.cards],
            'influenced_meanings': self.influenced_meanings,
            'reading_date': self.reading_date.isoformat(),
            'user_context': self.user_context,
            'notes': self.notes
        }


class TarotSpread:
    """
    Manages a complete tarot spread with cards, positions, and meanings.
    
    This class handles the creation of spreads from layouts, drawing cards
    from a deck, and integrating with the influence engine for enhanced meanings.
    """
    
    def __init__(self, layout: SpreadLayout, deck: Deck, user_context: Optional[str] = None):
        """
        Initialize a tarot spread.
        
        Args:
            layout: The spread layout to use
            deck: The deck to draw cards from
            user_context: Optional user question or context
        """
        self.layout = layout
        self.deck = deck
        self.user_context = user_context
        self.reading: Optional[SpreadReading] = None
        self.influence_engine = EnhancedInfluenceEngine()
        
        # Validate layout
        errors = layout.validate()
        if errors:
            raise ValueError(f"Invalid spread layout: {', '.join(errors)}")
    
    def draw_cards(self, orientations: Optional[List[Orientation]] = None) -> SpreadReading:
        """
        Draw cards for the spread.
        
        Args:
            orientations: Optional list of orientations for each card.
                        If None, orientations are determined randomly.
                        Must have length equal to layout.card_count.
        
        Returns:
            SpreadReading object with drawn cards
            
        Raises:
            ValueError: If deck doesn't have enough cards or orientations list is invalid
        """
        if len(self.deck) < self.layout.card_count:
            raise ValueError(f"Deck has {len(self.deck)} cards, but spread requires {self.layout.card_count}")
        
        if orientations is not None and len(orientations) != self.layout.card_count:
            raise ValueError(f"Orientations list must have {self.layout.card_count} elements")
        
        # Generate unique reading ID
        reading_id = str(uuid.uuid4())
        
        # Draw cards from deck
        drawn_cards = self.deck.draw_cards(self.layout.card_count, orientations)
        
        # Create spread cards
        spread_cards = []
        for i, (position, card) in enumerate(zip(self.layout.positions, drawn_cards)):
            spread_card = SpreadCard(
                position=position,
                card=card,
                drawn_at=datetime.now()
            )
            spread_cards.append(spread_card)
        
        # Create reading
        self.reading = SpreadReading(
            spread_id=reading_id,
            layout=self.layout,
            cards=spread_cards,
            reading_date=datetime.now(),
            user_context=self.user_context
        )
        
        return self.reading
    
    def apply_influence_engine(self, card_database: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Apply the influence engine to get enhanced meanings.
        
        Args:
            card_database: Complete card database for influence calculations
            
        Returns:
            Influence engine results
            
        Raises:
            ValueError: If no reading has been drawn yet
        """
        if self.reading is None:
            raise ValueError("No reading drawn yet. Call draw_cards() first.")
        
        # Prepare spread data for influence engine
        spread_data = {
            "reading_id": self.reading.spread_id,
            "date_time": self.reading.reading_date.isoformat(),
            "spread_type": self.layout.id,
            "positions": [
                {
                    "position_id": card.position.id,
                    "card_id": card.card.id,
                    "orientation": card.card.orientation.value
                }
                for card in self.reading.cards
            ],
            "user_context": self.user_context
        }
        
        # Apply influence engine
        influenced_meanings = self.influence_engine.compute_influenced_meanings(
            spread_data, card_database
        )
        
        # Store results
        self.reading.influenced_meanings = influenced_meanings
        
        return influenced_meanings
    
    def get_reading_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the reading.
        
        Returns:
            Dictionary with reading summary information
        """
        if self.reading is None:
            raise ValueError("No reading drawn yet. Call draw_cards() first.")
        
        summary = {
            'spread_id': self.reading.spread_id,
            'layout_name': self.layout.name,
            'layout_description': self.layout.description,
            'card_count': len(self.reading.cards),
            'reading_date': self.reading.reading_date.isoformat(),
            'user_context': self.user_context,
            'has_influenced_meanings': self.reading.influenced_meanings is not None
        }
        
        # Add card information
        cards_info = []
        for spread_card in self.reading.cards:
            card_info = {
                'position': spread_card.position.name,
                'position_description': spread_card.position.description,
                'card_name': spread_card.card.name,
                'orientation': spread_card.card.orientation.value,
                'importance': spread_card.position.importance
            }
            cards_info.append(card_info)
        
        summary['cards'] = cards_info
        
        # Add influenced meanings summary if available
        if self.reading.influenced_meanings:
            summary['influenced_summary'] = self.reading.influenced_meanings.get('summary', '')
            summary['advice'] = self.reading.influenced_meanings.get('advice', [])
            summary['follow_up_questions'] = self.reading.influenced_meanings.get('follow_up_questions', [])
        
        return summary
    
    def get_position_meaning(self, position_id: str) -> Optional[str]:
        """
        Get the meaning for a specific position.
        
        Args:
            position_id: ID of the position to get meaning for
            
        Returns:
            Meaning text if available, None otherwise
        """
        if self.reading is None:
            return None
        
        spread_card = self.reading.get_card_by_position(position_id)
        if spread_card is None:
            return None
        
        # Try to get influenced meaning first
        if self.reading.influenced_meanings:
            for card_data in self.reading.influenced_meanings.get('cards', []):
                if card_data['position'] == position_id:
                    return card_data.get('influenced_text', card_data.get('base_text'))
        
        # Fall back to base card meaning
        return spread_card.card.get_meaning()
    
    def get_all_meanings(self) -> Dict[str, str]:
        """
        Get meanings for all positions in the spread.
        
        Returns:
            Dictionary mapping position IDs to meanings
        """
        if self.reading is None:
            return {}
        
        meanings = {}
        for spread_card in self.reading.cards:
            meaning = self.get_position_meaning(spread_card.position.id)
            if meaning:
                meanings[spread_card.position.id] = meaning
        
        return meanings
    
    def add_notes(self, position_id: str, notes: str) -> None:
        """
        Add notes to a specific position.
        
        Args:
            position_id: ID of the position to add notes to
            notes: Notes to add
        """
        if self.reading is None:
            raise ValueError("No reading drawn yet. Call draw_cards() first.")
        
        spread_card = self.reading.get_card_by_position(position_id)
        if spread_card is None:
            raise ValueError(f"Position {position_id} not found in reading")
        
        spread_card.notes = notes
    
    def add_reading_notes(self, notes: str) -> None:
        """
        Add notes to the entire reading.
        
        Args:
            notes: Notes to add to the reading
        """
        if self.reading is None:
            raise ValueError("No reading drawn yet. Call draw_cards() first.")
        
        self.reading.notes = notes
    
    def reset_deck(self) -> None:
        """Reset the deck to its original state."""
        self.deck.reset()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the spread to a dictionary representation.
        
        Returns:
            Dictionary containing all spread information
        """
        if self.reading is None:
            return {
                'layout': self.layout.to_dict(),
                'user_context': self.user_context,
                'reading': None
            }
        
        return {
            'layout': self.layout.to_dict(),
            'user_context': self.user_context,
            'reading': self.reading.to_dict()
        }
    
    @classmethod
    def create_from_layout(cls, layout: SpreadLayout, deck: Deck, user_context: Optional[str] = None) -> 'TarotSpread':
        """
        Create a tarot spread from a layout.
        
        Args:
            layout: The spread layout to use
            deck: The deck to draw cards from
            user_context: Optional user question or context
            
        Returns:
            TarotSpread instance
        """
        return cls(layout, deck, user_context)
    
    @classmethod
    def create_three_card_reading(cls, deck: Deck, user_context: Optional[str] = None) -> 'TarotSpread':
        """
        Create a three-card reading.
        
        Args:
            deck: The deck to draw cards from
            user_context: Optional user question or context
            
        Returns:
            TarotSpread instance with three-card layout
        """
        layout = SpreadLayout.create_three_card()
        return cls(layout, deck, user_context)
    
    @classmethod
    def create_celtic_cross_reading(cls, deck: Deck, user_context: Optional[str] = None) -> 'TarotSpread':
        """
        Create a Celtic Cross reading.
        
        Args:
            deck: The deck to draw cards from
            user_context: Optional user question or context
            
        Returns:
            TarotSpread instance with Celtic Cross layout
        """
        layout = SpreadLayout.create_celtic_cross()
        return cls(layout, deck, user_context)
    
    @classmethod
    def create_single_card_reading(cls, deck: Deck, user_context: Optional[str] = None) -> 'TarotSpread':
        """
        Create a single card reading.
        
        Args:
            deck: The deck to draw cards from
            user_context: Optional user question or context
            
        Returns:
            TarotSpread instance with single card layout
        """
        layout = SpreadLayout.create_single_card()
        return cls(layout, deck, user_context)


# Example usage and testing
if __name__ == "__main__":
    from tarot_studio.deck import Deck
    
    # Load deck
    deck = Deck.load_from_file('card_data.json')
    deck.shuffle(seed=42)
    
    # Create three-card reading
    spread = TarotSpread.create_three_card_reading(deck, "What does my future hold?")
    
    # Draw cards
    reading = spread.draw_cards()
    print(f"Reading ID: {reading.spread_id}")
    print(f"Layout: {spread.layout.name}")
    print(f"Cards drawn: {len(reading.cards)}")
    
    # Show cards
    for spread_card in reading.cards:
        print(f"{spread_card.position.name}: {spread_card.card.name} ({spread_card.card.orientation.value})")
    
    # Get reading summary
    summary = spread.get_reading_summary()
    print(f"\nSummary: {summary['layout_name']}")
    print(f"User context: {summary['user_context']}")
    
    # Test position meaning
    past_meaning = spread.get_position_meaning('past')
    if past_meaning:
        print(f"\nPast meaning: {past_meaning[:100]}...")
    
    # Test adding notes
    spread.add_notes('present', 'This feels very relevant to my current situation')
    spread.add_reading_notes('A very insightful reading')
    
    print(f"\nReading notes: {reading.notes}")
    print(f"Present card notes: {reading.get_card_by_position('present').notes}")