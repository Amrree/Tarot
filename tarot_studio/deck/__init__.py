"""
Tarot Deck Module

This module provides a complete implementation of a tarot deck system,
including Card and Deck classes for representing individual cards
and complete decks with shuffling, drawing, and reset functionality.

Classes:
    Card: Represents a single tarot card with metadata and meanings
    Deck: Represents a complete 78-card tarot deck
    CardMetadata: Metadata container for card information
    Orientation: Enumeration for card orientations (upright/reversed)
    Arcana: Enumeration for arcana types (major/minor)
    Suit: Enumeration for Minor Arcana suits
    Element: Enumeration for card elements

Example:
    >>> from tarot_studio.deck import Deck, Orientation
    >>> deck = Deck.load_from_file('card_data.json')
    >>> deck.shuffle()
    >>> card = deck.draw_card(Orientation.UPRIGHT)
    >>> print(card.name)
    "The Sun"
"""

from .card import (
    Card,
    CardMetadata,
    Orientation,
    Arcana,
    Suit,
    Element
)

from .deck import Deck

__all__ = [
    'Card',
    'CardMetadata',
    'Deck',
    'Orientation',
    'Arcana',
    'Suit',
    'Element'
]

__version__ = '1.0.0'
__author__ = 'Tarot Studio Team'
__description__ = 'Complete tarot deck implementation with 78 cards'