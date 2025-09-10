"""
Deck class for the Tarot Deck Module.

This module defines the Deck class that represents a complete tarot deck
with shuffling, drawing, and reset functionality.
"""

import json
import random
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from .card import Card, Orientation, Arcana, Suit, Element


class Deck:
    """
    Represents a complete tarot deck with 78 cards.
    
    A Deck object contains all 78 tarot cards (22 Major Arcana + 56 Minor Arcana)
    and provides methods for shuffling, drawing cards, and resetting the deck.
    
    Attributes:
        cards (List[Card]): List of all cards in the deck
        drawn_cards (List[Card]): List of cards that have been drawn
        is_shuffled (bool): Whether the deck has been shuffled
    
    Example:
        >>> deck = Deck.load_from_file('card_data.json')
        >>> deck.shuffle()
        >>> card = deck.draw_card()
        >>> print(card.name)
        "The Sun"
        >>> deck.reset()
        >>> print(len(deck.cards))
        78
    """
    
    def __init__(self, cards: List[Card] = None):
        """
        Initialize a Deck object.
        
        Args:
            cards: Optional list of cards to initialize the deck with.
                  If None, creates an empty deck.
        """
        self.cards = cards.copy() if cards else []
        self.drawn_cards = []
        self.is_shuffled = False
        self._original_order = self.cards.copy() if cards else []
    
    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> 'Deck':
        """
        Load a deck from a JSON file.
        
        Args:
            file_path: Path to the JSON file containing card data
            
        Returns:
            Deck object loaded from the file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file contains invalid data
            json.JSONDecodeError: If the file is not valid JSON
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Card data file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {e}")
        
        return cls.from_data(data)
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'Deck':
        """
        Create a deck from dictionary data.
        
        Args:
            data: Dictionary containing deck information and card data
            
        Returns:
            Deck object created from the data
            
        Raises:
            ValueError: If the data is invalid or missing required fields
        """
        cards = []
        
        # Load Major Arcana cards
        if 'major_arcana' in data:
            for card_data in data['major_arcana']:
                try:
                    card = Card.from_data(card_data)
                    cards.append(card)
                except Exception as e:
                    raise ValueError(f"Error loading Major Arcana card: {e}")
        
        # Load Minor Arcana cards
        if 'minor_arcana' in data:
            minor_data = data['minor_arcana']
            
            for suit_name, suit_data in minor_data.items():
                if suit_name in ['wands', 'cups', 'swords', 'pentacles']:
                    suit = Suit(suit_name)
                    element = Element(suit_data.get('element', 'fire'))
                    
                    # Load numbered cards (Ace through Ten)
                    for card_name, card_info in suit_data.items():
                        if card_name in ['ace', 'two', 'three', 'four', 'five', 
                                       'six', 'seven', 'eight', 'nine', 'ten']:
                            number = cls._get_card_number(card_name)
                            
                            card_data = {
                                'id': f"{card_name}_of_{suit_name}",
                                'name': f"{card_name.title()} of {suit_name.title()}",
                                'arcana': 'minor',
                                'suit': suit_name,
                                'number': number,
                                'element': element.value,
                                'keywords': card_info.get('keywords', []),
                                'upright_meaning': card_info.get('upright_meaning', ''),
                                'reversed_meaning': card_info.get('reversed_meaning', '')
                            }
                            
                            try:
                                card = Card.from_data(card_data)
                                cards.append(card)
                            except Exception as e:
                                raise ValueError(f"Error loading Minor Arcana card {card_name} of {suit_name}: {e}")
                    
                    # Load court cards (Page, Knight, Queen, King)
                    for court_rank in ['page', 'knight', 'queen', 'king']:
                        if court_rank in suit_data:
                            card_info = suit_data[court_rank]
                            
                            card_data = {
                                'id': f"{court_rank}_of_{suit_name}",
                                'name': f"{court_rank.title()} of {suit_name.title()}",
                                'arcana': 'minor',
                                'suit': suit_name,
                                'number': None,
                                'element': element.value,
                                'keywords': card_info.get('keywords', []),
                                'upright_meaning': card_info.get('upright_meaning', ''),
                                'reversed_meaning': card_info.get('reversed_meaning', '')
                            }
                            
                            try:
                                card = Card.from_data(card_data)
                                cards.append(card)
                            except Exception as e:
                                raise ValueError(f"Error loading court card {court_rank} of {suit_name}: {e}")
        
        if len(cards) != 78:
            raise ValueError(f"Expected 78 cards, but loaded {len(cards)} cards")
        
        return cls(cards)
    
    @staticmethod
    def _get_card_number(card_name: str) -> int:
        """Convert card name to number."""
        number_map = {
            'ace': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        return number_map.get(card_name, 0)
    
    def shuffle(self, seed: Optional[int] = None) -> None:
        """
        Shuffle the deck.
        
        Args:
            seed: Optional random seed for reproducible shuffling
        """
        if seed is not None:
            random.seed(seed)
        
        random.shuffle(self.cards)
        self.is_shuffled = True
    
    def draw_card(self, orientation: Optional[Orientation] = None) -> Card:
        """
        Draw a single card from the deck.
        
        Args:
            orientation: Optional orientation to set for the drawn card.
                        If None, orientation is determined randomly.
        
        Returns:
            The drawn card
            
        Raises:
            ValueError: If the deck is empty
        """
        if not self.cards:
            raise ValueError("Cannot draw from an empty deck")
        
        card = self.cards.pop(0)
        
        if orientation is None:
            # Randomly determine orientation
            orientation = Orientation.UPRIGHT if random.random() < 0.5 else Orientation.REVERSED
        
        card.set_orientation(orientation)
        self.drawn_cards.append(card)
        
        return card
    
    def draw_cards(self, count: int, orientations: Optional[List[Orientation]] = None) -> List[Card]:
        """
        Draw multiple cards from the deck.
        
        Args:
            count: Number of cards to draw
            orientations: Optional list of orientations for each card.
                        If None, orientations are determined randomly.
                        If provided, must have length equal to count.
        
        Returns:
            List of drawn cards
            
        Raises:
            ValueError: If the deck doesn't have enough cards or orientations list is invalid
        """
        if count > len(self.cards):
            raise ValueError(f"Cannot draw {count} cards from deck with {len(self.cards)} cards")
        
        if orientations is not None and len(orientations) != count:
            raise ValueError(f"Orientations list must have {count} elements")
        
        drawn = []
        for i in range(count):
            orientation = orientations[i] if orientations else None
            card = self.draw_card(orientation)
            drawn.append(card)
        
        return drawn
    
    def reset(self) -> None:
        """Reset the deck to its original state with all cards."""
        self.cards = self._original_order.copy()
        self.drawn_cards = []
        self.is_shuffled = False
    
    def get_card_by_id(self, card_id: str) -> Optional[Card]:
        """
        Get a card by its ID from the remaining cards.
        
        Args:
            card_id: The ID of the card to find
            
        Returns:
            The card if found, None otherwise
        """
        for card in self.cards:
            if card.id == card_id:
                return card
        return None
    
    def get_card_by_name(self, name: str) -> Optional[Card]:
        """
        Get a card by its name from the remaining cards.
        
        Args:
            name: The name of the card to find
            
        Returns:
            The card if found, None otherwise
        """
        for card in self.cards:
            if card.name.lower() == name.lower():
                return card
        return None
    
    def get_major_arcana(self) -> List[Card]:
        """
        Get all Major Arcana cards from the remaining cards.
        
        Returns:
            List of Major Arcana cards
        """
        return [card for card in self.cards if card.is_major_arcana()]
    
    def get_minor_arcana(self) -> List[Card]:
        """
        Get all Minor Arcana cards from the remaining cards.
        
        Returns:
            List of Minor Arcana cards
        """
        return [card for card in self.cards if card.is_minor_arcana()]
    
    def get_cards_by_suit(self, suit: Suit) -> List[Card]:
        """
        Get all cards of a specific suit from the remaining cards.
        
        Args:
            suit: The suit to filter by
            
        Returns:
            List of cards of the specified suit
        """
        return [card for card in self.cards if card.suit == suit]
    
    def get_cards_by_element(self, element: Element) -> List[Card]:
        """
        Get all cards of a specific element from the remaining cards.
        
        Args:
            element: The element to filter by
            
        Returns:
            List of cards of the specified element
        """
        return [card for card in self.cards if card.element == element]
    
    def get_cards_with_keyword(self, keyword: str) -> List[Card]:
        """
        Get all cards containing a specific keyword from the remaining cards.
        
        Args:
            keyword: The keyword to search for
            
        Returns:
            List of cards containing the keyword
        """
        return [card for card in self.cards if card.has_keyword(keyword)]
    
    def count_remaining(self) -> int:
        """
        Get the number of cards remaining in the deck.
        
        Returns:
            Number of cards remaining
        """
        return len(self.cards)
    
    def count_drawn(self) -> int:
        """
        Get the number of cards that have been drawn.
        
        Returns:
            Number of cards drawn
        """
        return len(self.drawn_cards)
    
    def is_empty(self) -> bool:
        """
        Check if the deck is empty.
        
        Returns:
            True if the deck is empty, False otherwise
        """
        return len(self.cards) == 0
    
    def get_deck_info(self) -> Dict[str, Any]:
        """
        Get information about the deck.
        
        Returns:
            Dictionary containing deck statistics
        """
        major_count = len(self.get_major_arcana())
        minor_count = len(self.get_minor_arcana())
        
        suit_counts = {}
        for suit in Suit:
            suit_counts[suit.value] = len(self.get_cards_by_suit(suit))
        
        element_counts = {}
        for element in Element:
            element_counts[element.value] = len(self.get_cards_by_element(element))
        
        return {
            'total_cards': len(self.cards),
            'drawn_cards': len(self.drawn_cards),
            'major_arcana': major_count,
            'minor_arcana': minor_count,
            'suit_counts': suit_counts,
            'element_counts': element_counts,
            'is_shuffled': self.is_shuffled,
            'is_empty': self.is_empty()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the deck to a dictionary representation.
        
        Returns:
            Dictionary containing all deck information
        """
        return {
            'remaining_cards': [card.to_dict() for card in self.cards],
            'drawn_cards': [card.to_dict() for card in self.drawn_cards],
            'deck_info': self.get_deck_info()
        }
    
    def __len__(self) -> int:
        """Get the number of cards remaining in the deck."""
        return len(self.cards)
    
    def __str__(self) -> str:
        """String representation of the deck."""
        return f"Deck({len(self.cards)} cards remaining, {len(self.drawn_cards)} drawn)"
    
    def __repr__(self) -> str:
        """Detailed string representation of the deck."""
        return f"Deck(cards={len(self.cards)}, drawn={len(self.drawn_cards)}, shuffled={self.is_shuffled})"


# Example usage and testing
if __name__ == "__main__":
    # Test deck loading
    try:
        deck = Deck.load_from_file('card_data.json')
        print(f"Loaded deck: {deck}")
        print(f"Deck info: {deck.get_deck_info()}")
        
        # Test shuffling
        deck.shuffle(seed=42)
        print(f"After shuffling: {deck}")
        
        # Test drawing cards
        card1 = deck.draw_card()
        print(f"Drew card: {card1}")
        
        card2 = deck.draw_card(Orientation.REVERSED)
        print(f"Drew reversed card: {card2}")
        
        cards = deck.draw_cards(3)
        print(f"Drew 3 cards: {[str(card) for card in cards]}")
        
        print(f"Remaining cards: {len(deck)}")
        print(f"Drawn cards: {deck.count_drawn()}")
        
        # Test filtering
        major_cards = deck.get_major_arcana()
        print(f"Major Arcana remaining: {len(major_cards)}")
        
        wands_cards = deck.get_cards_by_suit(Suit.WANDS)
        print(f"Wands remaining: {len(wands_cards)}")
        
        # Test reset
        deck.reset()
        print(f"After reset: {deck}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()