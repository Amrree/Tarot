"""
Spread Layout Definitions

This module defines the structure and positions of various tarot spreads,
including canonical spreads like Three-Card, Celtic Cross, and custom layouts.
"""

from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
import math


class PositionType(Enum):
    """Types of positions in a spread."""
    PAST = "past"
    PRESENT = "present"
    FUTURE = "future"
    SITUATION = "situation"
    CHALLENGE = "challenge"
    ADVICE = "advice"
    OUTCOME = "outcome"
    HOPES_FEARS = "hopes_fears"
    EXTERNAL = "external"
    ABOVE = "above"
    BELOW = "below"
    LESSON = "lesson"
    CONNECTION = "connection"
    PARTNER = "partner"
    YOU = "you"
    CUSTOM = "custom"


@dataclass
class SpreadPosition:
    """
    Represents a single position within a tarot spread.
    
    Attributes:
        id: Unique identifier for the position
        name: Human-readable name for the position
        description: What this position represents in the reading
        position_type: Type of position (past, present, future, etc.)
        coordinates: Optional (x, y) coordinates for visual layout
        importance: Relative importance of this position (1.0 = most important)
    """
    id: str
    name: str
    description: str
    position_type: PositionType
    coordinates: Optional[Tuple[float, float]] = None
    importance: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert position to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'position_type': self.position_type.value,
            'coordinates': self.coordinates,
            'importance': self.importance
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpreadPosition':
        """Create position from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            position_type=PositionType(data['position_type']),
            coordinates=data.get('coordinates'),
            importance=data.get('importance', 1.0)
        )


@dataclass
class SpreadLayout:
    """
    Defines the complete structure of a tarot spread.
    
    Attributes:
        id: Unique identifier for the layout
        name: Human-readable name for the layout
        description: Description of what this spread is used for
        positions: List of positions in the spread
        category: Category of spread (daily, relationship, career, etc.)
        difficulty: Difficulty level (beginner, intermediate, advanced)
        estimated_time: Estimated time to complete reading (minutes)
        card_count: Number of cards required
    """
    id: str
    name: str
    description: str
    positions: List[SpreadPosition] = field(default_factory=list)
    category: str = "general"
    difficulty: str = "beginner"
    estimated_time: int = 10
    card_count: int = 0
    
    def __post_init__(self):
        """Calculate card count after initialization."""
        if self.card_count == 0:
            self.card_count = len(self.positions)
    
    def add_position(self, position: SpreadPosition) -> None:
        """Add a position to the spread."""
        self.positions.append(position)
        self.card_count = len(self.positions)
    
    def get_position_by_id(self, position_id: str) -> Optional[SpreadPosition]:
        """Get a position by its ID."""
        for position in self.positions:
            if position.id == position_id:
                return position
        return None
    
    def get_positions_by_type(self, position_type: PositionType) -> List[SpreadPosition]:
        """Get all positions of a specific type."""
        return [pos for pos in self.positions if pos.position_type == position_type]
    
    def get_most_important_positions(self, count: int = 3) -> List[SpreadPosition]:
        """Get the most important positions in the spread."""
        sorted_positions = sorted(self.positions, key=lambda p: p.importance, reverse=True)
        return sorted_positions[:count]
    
    def validate(self) -> List[str]:
        """
        Validate the spread layout.
        
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Check for duplicate position IDs
        position_ids = [pos.id for pos in self.positions]
        if len(position_ids) != len(set(position_ids)):
            errors.append("Duplicate position IDs found")
        
        # Check for empty positions
        if not self.positions:
            errors.append("Spread must have at least one position")
        
        # Check for reasonable card count
        if self.card_count > 21:
            errors.append("Spread has too many cards (max 21 recommended)")
        
        # Check position importance values
        for position in self.positions:
            if position.importance < 0 or position.importance > 2.0:
                errors.append(f"Position {position.id} has invalid importance value")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert layout to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'positions': [pos.to_dict() for pos in self.positions],
            'category': self.category,
            'difficulty': self.difficulty,
            'estimated_time': self.estimated_time,
            'card_count': self.card_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpreadLayout':
        """Create layout from dictionary."""
        positions = [SpreadPosition.from_dict(pos_data) for pos_data in data.get('positions', [])]
        
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            positions=positions,
            category=data.get('category', 'general'),
            difficulty=data.get('difficulty', 'beginner'),
            estimated_time=data.get('estimated_time', 10),
            card_count=data.get('card_count', len(positions))
        )
    
    @classmethod
    def create_single_card(cls) -> 'SpreadLayout':
        """Create a single card spread layout."""
        position = SpreadPosition(
            id="guidance",
            name="Guidance",
            description="What you need to know right now",
            position_type=PositionType.PRESENT,
            coordinates=(0.5, 0.5),
            importance=1.0
        )
        
        return cls(
            id="single_card",
            name="Single Card",
            description="A simple one-card reading for daily guidance",
            positions=[position],
            category="daily",
            difficulty="beginner",
            estimated_time=5,
            card_count=1
        )
    
    @classmethod
    def create_three_card(cls) -> 'SpreadLayout':
        """Create a three-card spread layout (Past, Present, Future)."""
        positions = [
            SpreadPosition(
                id="past",
                name="Past",
                description="What has influenced your current situation",
                position_type=PositionType.PAST,
                coordinates=(0.2, 0.5),
                importance=0.8
            ),
            SpreadPosition(
                id="present",
                name="Present",
                description="Your current circumstances and mindset",
                position_type=PositionType.PRESENT,
                coordinates=(0.5, 0.5),
                importance=1.0
            ),
            SpreadPosition(
                id="future",
                name="Future",
                description="What is likely to unfold",
                position_type=PositionType.FUTURE,
                coordinates=(0.8, 0.5),
                importance=0.8
            )
        ]
        
        return cls(
            id="three_card",
            name="Three Card",
            description="Past, Present, Future reading for understanding life flow",
            positions=positions,
            category="general",
            difficulty="beginner",
            estimated_time=15,
            card_count=3
        )
    
    @classmethod
    def create_celtic_cross(cls) -> 'SpreadLayout':
        """Create a Celtic Cross spread layout."""
        positions = [
            # Cross positions (center)
            SpreadPosition(
                id="situation",
                name="Situation",
                description="What is happening now",
                position_type=PositionType.SITUATION,
                coordinates=(0.3, 0.4),
                importance=1.0
            ),
            SpreadPosition(
                id="challenge",
                name="Challenge",
                description="What is blocking or helping you",
                position_type=PositionType.CHALLENGE,
                coordinates=(0.3, 0.6),
                importance=1.0
            ),
            
            # Staff positions (right side)
            SpreadPosition(
                id="past",
                name="Past",
                description="What has led to this situation",
                position_type=PositionType.PAST,
                coordinates=(0.5, 0.3),
                importance=0.8
            ),
            SpreadPosition(
                id="future",
                name="Future",
                description="What is likely to happen",
                position_type=PositionType.FUTURE,
                coordinates=(0.7, 0.3),
                importance=0.8
            ),
            SpreadPosition(
                id="above",
                name="Above",
                description="Your conscious goals and aspirations",
                position_type=PositionType.ABOVE,
                coordinates=(0.5, 0.1),
                importance=0.7
            ),
            SpreadPosition(
                id="below",
                name="Below",
                description="Your subconscious influences",
                position_type=PositionType.BELOW,
                coordinates=(0.5, 0.7),
                importance=0.7
            ),
            SpreadPosition(
                id="advice",
                name="Advice",
                description="How to approach the situation",
                position_type=PositionType.ADVICE,
                coordinates=(0.7, 0.1),
                importance=0.9
            ),
            SpreadPosition(
                id="external",
                name="External",
                description="People or events affecting you",
                position_type=PositionType.EXTERNAL,
                coordinates=(0.7, 0.5),
                importance=0.6
            ),
            SpreadPosition(
                id="hopes_fears",
                name="Hopes & Fears",
                description="Your inner hopes and concerns",
                position_type=PositionType.HOPES_FEARS,
                coordinates=(0.7, 0.7),
                importance=0.6
            ),
            SpreadPosition(
                id="outcome",
                name="Outcome",
                description="The likely resolution",
                position_type=PositionType.OUTCOME,
                coordinates=(0.9, 0.5),
                importance=0.9
            )
        ]
        
        return cls(
            id="celtic_cross",
            name="Celtic Cross",
            description="A comprehensive 10-card spread for deep insight",
            positions=positions,
            category="comprehensive",
            difficulty="intermediate",
            estimated_time=45,
            card_count=10
        )
    
    @classmethod
    def create_relationship_cross(cls) -> 'SpreadLayout':
        """Create a relationship cross spread layout."""
        positions = [
            SpreadPosition(
                id="you",
                name="You",
                description="Your role in the relationship",
                position_type=PositionType.YOU,
                coordinates=(0.2, 0.5),
                importance=1.0
            ),
            SpreadPosition(
                id="partner",
                name="Partner",
                description="Your partner's role",
                position_type=PositionType.PARTNER,
                coordinates=(0.8, 0.5),
                importance=1.0
            ),
            SpreadPosition(
                id="connection",
                name="Connection",
                description="What binds you together",
                position_type=PositionType.CONNECTION,
                coordinates=(0.5, 0.3),
                importance=0.9
            ),
            SpreadPosition(
                id="challenge",
                name="Challenge",
                description="What challenges the relationship",
                position_type=PositionType.CHALLENGE,
                coordinates=(0.5, 0.7),
                importance=0.8
            ),
            SpreadPosition(
                id="advice",
                name="Advice",
                description="How to strengthen the relationship",
                position_type=PositionType.ADVICE,
                coordinates=(0.3, 0.5),
                importance=0.9
            ),
            SpreadPosition(
                id="outcome",
                name="Outcome",
                description="Where the relationship is heading",
                position_type=PositionType.OUTCOME,
                coordinates=(0.7, 0.5),
                importance=0.9
            ),
            SpreadPosition(
                id="lesson",
                name="Lesson",
                description="What you can learn from this relationship",
                position_type=PositionType.LESSON,
                coordinates=(0.5, 0.5),
                importance=0.7
            )
        ]
        
        return cls(
            id="relationship_cross",
            name="Relationship Cross",
            description="A 7-card spread for relationship insights",
            positions=positions,
            category="relationship",
            difficulty="intermediate",
            estimated_time=30,
            card_count=7
        )
    
    @classmethod
    def create_year_ahead(cls) -> 'SpreadLayout':
        """Create a year-ahead spread layout."""
        months = [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"
        ]
        
        positions = []
        for i, month in enumerate(months):
            # Arrange months in a circle
            angle = (i / 12) * 2 * 3.14159
            x = 0.5 + 0.3 * math.cos(angle)
            y = 0.5 + 0.3 * math.sin(angle)
            
            position = SpreadPosition(
                id=month,
                name=month.title(),
                description=f"{month.title()} energy and focus",
                position_type=PositionType.CUSTOM,
                coordinates=(x, y),
                importance=0.5
            )
            positions.append(position)
        
        return cls(
            id="year_ahead",
            name="Year Ahead",
            description="A 12-card spread for yearly guidance",
            positions=positions,
            category="yearly",
            difficulty="advanced",
            estimated_time=60,
            card_count=12
        )
    
    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> 'SpreadLayout':
        """Load a spread layout from a JSON file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Spread layout file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """Save the spread layout to a JSON file."""
        file_path = Path(file_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)


# Math is already imported at the top


# Example usage and testing
if __name__ == "__main__":
    # Test single card spread
    single_layout = SpreadLayout.create_single_card()
    print(f"Single Card Layout: {single_layout.name}")
    print(f"Positions: {len(single_layout.positions)}")
    print(f"Validation: {single_layout.validate()}")
    
    # Test three card spread
    three_layout = SpreadLayout.create_three_card()
    print(f"\nThree Card Layout: {three_layout.name}")
    print(f"Positions: {len(three_layout.positions)}")
    print(f"Card count: {three_layout.card_count}")
    
    # Test Celtic Cross
    celtic_layout = SpreadLayout.create_celtic_cross()
    print(f"\nCeltic Cross Layout: {celtic_layout.name}")
    print(f"Positions: {len(celtic_layout.positions)}")
    print(f"Difficulty: {celtic_layout.difficulty}")
    
    # Test validation
    errors = celtic_layout.validate()
    if errors:
        print(f"Validation errors: {errors}")
    else:
        print("Layout is valid!")
    
    # Test dictionary conversion
    layout_dict = celtic_layout.to_dict()
    restored_layout = SpreadLayout.from_dict(layout_dict)
    print(f"\nRestored layout: {restored_layout.name}")
    print(f"Positions match: {len(restored_layout.positions) == len(celtic_layout.positions)}")