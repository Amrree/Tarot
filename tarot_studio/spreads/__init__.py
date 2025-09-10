"""
Tarot Spreads Module

This module provides comprehensive spread management for tarot readings,
including layout definitions, position management, drawing logic, and
integration with the deck and influence engine modules.

Classes:
    SpreadLayout: Defines the structure and positions of a tarot spread
    SpreadPosition: Represents a single position within a spread
    TarotSpread: Manages a complete tarot spread with cards and meanings
    SpreadManager: Handles spread creation, validation, and management

Example:
    >>> from tarot_studio.spreads import TarotSpread, SpreadLayout
    >>> from tarot_studio.deck import Deck
    >>> 
    >>> # Create a three-card spread
    >>> layout = SpreadLayout.create_three_card()
    >>> deck = Deck.load_from_file('card_data.json')
    >>> spread = TarotSpread.create_from_layout(layout, deck)
    >>> 
    >>> # Get the reading
    >>> reading = spread.get_reading()
    >>> print(f"Past: {reading['past']['card'].name}")
"""

from .spread_layout import SpreadLayout, SpreadPosition, PositionType
from .tarot_spread import TarotSpread
from .spread_manager import SpreadManager

__all__ = [
    'SpreadLayout',
    'SpreadPosition',
    'PositionType',
    'TarotSpread',
    'SpreadManager'
]

__version__ = '1.0.0'
__author__ = 'Tarot Studio Team'
__description__ = 'Comprehensive tarot spread management system'