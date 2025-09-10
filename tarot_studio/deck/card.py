"""
Card class for the Tarot Deck Module.

This module defines the Card class that represents individual tarot cards
with their metadata, meanings, and orientation support.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass


class Orientation(Enum):
    """Card orientation enumeration."""
    UPRIGHT = "upright"
    REVERSED = "reversed"


class Arcana(Enum):
    """Card arcana type enumeration."""
    MAJOR = "major"
    MINOR = "minor"


class Suit(Enum):
    """Card suit enumeration for Minor Arcana."""
    WANDS = "wands"
    CUPS = "cups"
    SWORDS = "swords"
    PENTACLES = "pentacles"


class Element(Enum):
    """Element enumeration."""
    FIRE = "fire"
    WATER = "water"
    AIR = "air"
    EARTH = "earth"


@dataclass
class CardMetadata:
    """Metadata for a tarot card."""
    id: str
    name: str
    arcana: Arcana
    suit: Optional[Suit] = None
    number: Optional[int] = None
    element: Optional[Element] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []


class Card:
    """
    Represents a single tarot card with its metadata and meanings.
    
    A Card object contains all the information needed to represent a tarot card,
    including its metadata (name, suit, number, etc.) and its meanings for both
    upright and reversed orientations.
    
    Attributes:
        metadata (CardMetadata): The card's metadata
        upright_meaning (str): The meaning when the card is upright
        reversed_meaning (str): The meaning when the card is reversed
        orientation (Orientation): The current orientation of the card
    
    Example:
        >>> card = Card.from_data(card_data)
        >>> print(card.name)
        "The Sun"
        >>> print(card.get_meaning())
        "The Sun represents joy, success, and vitality..."
        >>> card.flip()
        >>> print(card.get_meaning())
        "Reversed, The Sun suggests temporary setbacks..."
    """
    
    def __init__(
        self,
        metadata: CardMetadata,
        upright_meaning: str,
        reversed_meaning: str,
        orientation: Orientation = Orientation.UPRIGHT
    ):
        """
        Initialize a Card object.
        
        Args:
            metadata: The card's metadata
            upright_meaning: The meaning when upright
            reversed_meaning: The meaning when reversed
            orientation: The initial orientation (default: UPRIGHT)
        """
        self.metadata = metadata
        self.upright_meaning = upright_meaning
        self.reversed_meaning = reversed_meaning
        self.orientation = orientation
    
    @classmethod
    def from_data(cls, card_data: Dict[str, Any], orientation: Orientation = Orientation.UPRIGHT) -> 'Card':
        """
        Create a Card object from dictionary data.
        
        Args:
            card_data: Dictionary containing card information
            orientation: Initial orientation (default: UPRIGHT)
            
        Returns:
            Card object initialized from the data
            
        Raises:
            ValueError: If required fields are missing from card_data
        """
        # Validate required fields
        required_fields = ['id', 'name', 'upright_meaning', 'reversed_meaning']
        for field in required_fields:
            if field not in card_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Parse arcana type
        arcana = Arcana.MAJOR if card_data.get('arcana') == 'major' else Arcana.MINOR
        
        # Parse suit if present
        suit = None
        if 'suit' in card_data and card_data['suit']:
            try:
                suit = Suit(card_data['suit'])
            except ValueError:
                raise ValueError(f"Invalid suit: {card_data['suit']}")
        
        # Parse element if present
        element = None
        if 'element' in card_data and card_data['element']:
            try:
                element = Element(card_data['element'])
            except ValueError:
                raise ValueError(f"Invalid element: {card_data['element']}")
        
        # Create metadata
        metadata = CardMetadata(
            id=card_data['id'],
            name=card_data['name'],
            arcana=arcana,
            suit=suit,
            number=card_data.get('number'),
            element=element,
            keywords=card_data.get('keywords', [])
        )
        
        return cls(
            metadata=metadata,
            upright_meaning=card_data['upright_meaning'],
            reversed_meaning=card_data['reversed_meaning'],
            orientation=orientation
        )
    
    @property
    def id(self) -> str:
        """Get the card's unique identifier."""
        return self.metadata.id
    
    @property
    def name(self) -> str:
        """Get the card's name."""
        return self.metadata.name
    
    @property
    def arcana(self) -> Arcana:
        """Get the card's arcana type (Major or Minor)."""
        return self.metadata.arcana
    
    @property
    def suit(self) -> Optional[Suit]:
        """Get the card's suit (for Minor Arcana only)."""
        return self.metadata.suit
    
    @property
    def number(self) -> Optional[int]:
        """Get the card's number (for numbered cards only)."""
        return self.metadata.number
    
    @property
    def element(self) -> Optional[Element]:
        """Get the card's associated element."""
        return self.metadata.element
    
    @property
    def keywords(self) -> List[str]:
        """Get the card's keywords."""
        return self.metadata.keywords.copy()
    
    def get_meaning(self) -> str:
        """
        Get the card's meaning based on its current orientation.
        
        Returns:
            The card's meaning text for the current orientation
        """
        if self.orientation == Orientation.UPRIGHT:
            return self.upright_meaning
        else:
            return self.reversed_meaning
    
    def flip(self) -> None:
        """Flip the card to the opposite orientation."""
        if self.orientation == Orientation.UPRIGHT:
            self.orientation = Orientation.REVERSED
        else:
            self.orientation = Orientation.UPRIGHT
    
    def set_orientation(self, orientation: Orientation) -> None:
        """
        Set the card's orientation.
        
        Args:
            orientation: The new orientation to set
        """
        self.orientation = orientation
    
    def is_major_arcana(self) -> bool:
        """
        Check if this card is from the Major Arcana.
        
        Returns:
            True if the card is Major Arcana, False otherwise
        """
        return self.metadata.arcana == Arcana.MAJOR
    
    def is_minor_arcana(self) -> bool:
        """
        Check if this card is from the Minor Arcana.
        
        Returns:
            True if the card is Minor Arcana, False otherwise
        """
        return self.metadata.arcana == Arcana.MINOR
    
    def is_upright(self) -> bool:
        """
        Check if the card is currently upright.
        
        Returns:
            True if the card is upright, False if reversed
        """
        return self.orientation == Orientation.UPRIGHT
    
    def is_reversed(self) -> bool:
        """
        Check if the card is currently reversed.
        
        Returns:
            True if the card is reversed, False if upright
        """
        return self.orientation == Orientation.REVERSED
    
    def has_keyword(self, keyword: str) -> bool:
        """
        Check if the card has a specific keyword.
        
        Args:
            keyword: The keyword to search for
            
        Returns:
            True if the card has the keyword, False otherwise
        """
        return keyword.lower() in [k.lower() for k in self.metadata.keywords]
    
    def get_display_name(self) -> str:
        """
        Get the card's display name with orientation indicator.
        
        Returns:
            The card's name with orientation indicator (e.g., "The Sun (Reversed)")
        """
        if self.orientation == Orientation.REVERSED:
            return f"{self.name} (Reversed)"
        else:
            return self.name
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the card to a dictionary representation.
        
        Returns:
            Dictionary containing all card information
        """
        return {
            'id': self.id,
            'name': self.name,
            'arcana': self.arcana.value,
            'suit': self.suit.value if self.suit else None,
            'number': self.number,
            'element': self.element.value if self.element else None,
            'keywords': self.keywords,
            'orientation': self.orientation.value,
            'upright_meaning': self.upright_meaning,
            'reversed_meaning': self.reversed_meaning,
            'current_meaning': self.get_meaning()
        }
    
    def __str__(self) -> str:
        """String representation of the card."""
        return self.get_display_name()
    
    def __repr__(self) -> str:
        """Detailed string representation of the card."""
        return f"Card(id='{self.id}', name='{self.name}', orientation={self.orientation.value})"
    
    def __eq__(self, other) -> bool:
        """Check if two cards are equal (same ID and orientation)."""
        if not isinstance(other, Card):
            return False
        return self.id == other.id and self.orientation == other.orientation
    
    def __hash__(self) -> int:
        """Hash the card based on its ID and orientation."""
        return hash((self.id, self.orientation.value))


# Example usage and testing
if __name__ == "__main__":
    # Test card creation from data
    test_data = {
        'id': 'the_sun',
        'name': 'The Sun',
        'arcana': 'major',
        'element': 'fire',
        'keywords': ['joy', 'success', 'vitality'],
        'upright_meaning': 'The Sun represents joy, success, and vitality.',
        'reversed_meaning': 'Reversed, The Sun suggests temporary setbacks.'
    }
    
    # Create card
    card = Card.from_data(test_data)
    print(f"Created card: {card}")
    print(f"Arcana: {card.arcana.value}")
    print(f"Element: {card.element.value}")
    print(f"Keywords: {card.keywords}")
    print(f"Upright meaning: {card.get_meaning()}")
    
    # Test flipping
    card.flip()
    print(f"After flipping: {card}")
    print(f"Reversed meaning: {card.get_meaning()}")
    
    # Test dictionary conversion
    card_dict = card.to_dict()
    print(f"Card as dict: {card_dict}")
    
    # Test Minor Arcana card
    minor_data = {
        'id': 'ace_of_wands',
        'name': 'Ace of Wands',
        'arcana': 'minor',
        'suit': 'wands',
        'number': 1,
        'element': 'fire',
        'keywords': ['inspiration', 'creativity'],
        'upright_meaning': 'The Ace of Wands represents new inspiration.',
        'reversed_meaning': 'Reversed, the Ace of Wands suggests blocked creativity.'
    }
    
    minor_card = Card.from_data(minor_data)
    print(f"Minor Arcana card: {minor_card}")
    print(f"Suit: {minor_card.suit.value}")
    print(f"Number: {minor_card.number}")
    print(f"Is Major Arcana: {minor_card.is_major_arcana()}")
    print(f"Is Minor Arcana: {minor_card.is_minor_arcana()}")