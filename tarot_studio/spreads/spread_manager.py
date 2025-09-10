"""
Spread Manager

This module provides the SpreadManager class for managing multiple spreads,
templates, and spread-related operations.
"""

from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import json
from datetime import datetime

from .spread_layout import SpreadLayout, SpreadPosition, PositionType
from .tarot_spread import TarotSpread, SpreadReading
from ..deck import Deck


class SpreadManager:
    """
    Manages multiple tarot spreads, templates, and spread-related operations.
    
    This class provides functionality for:
    - Managing spread templates and layouts
    - Creating custom spreads
    - Saving and loading spread configurations
    - Organizing spreads by category and difficulty
    """
    
    def __init__(self):
        """Initialize the spread manager."""
        self.spread_templates: Dict[str, SpreadLayout] = {}
        self.custom_spreads: Dict[str, SpreadLayout] = {}
        self.recent_readings: List[SpreadReading] = []
        self._load_default_templates()
    
    def _load_default_templates(self) -> None:
        """Load default spread templates."""
        # Single Card
        self.spread_templates['single_card'] = SpreadLayout.create_single_card()
        
        # Three Card
        self.spread_templates['three_card'] = SpreadLayout.create_three_card()
        
        # Celtic Cross
        self.spread_templates['celtic_cross'] = SpreadLayout.create_celtic_cross()
        
        # Relationship Cross
        self.spread_templates['relationship_cross'] = SpreadLayout.create_relationship_cross()
        
        # Year Ahead
        self.spread_templates['year_ahead'] = SpreadLayout.create_year_ahead()
    
    def get_available_spreads(self) -> List[Dict[str, Any]]:
        """
        Get list of all available spreads.
        
        Returns:
            List of dictionaries containing spread information
        """
        spreads = []
        
        # Add templates
        for template_id, layout in self.spread_templates.items():
            spreads.append({
                'id': template_id,
                'name': layout.name,
                'description': layout.description,
                'category': layout.category,
                'difficulty': layout.difficulty,
                'card_count': layout.card_count,
                'estimated_time': layout.estimated_time,
                'type': 'template'
            })
        
        # Add custom spreads
        for custom_id, layout in self.custom_spreads.items():
            spreads.append({
                'id': custom_id,
                'name': layout.name,
                'description': layout.description,
                'category': layout.category,
                'difficulty': layout.difficulty,
                'card_count': layout.card_count,
                'estimated_time': layout.estimated_time,
                'type': 'custom'
            })
        
        return spreads
    
    def get_spreads_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get spreads filtered by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of spreads in the specified category
        """
        all_spreads = self.get_available_spreads()
        return [spread for spread in all_spreads if spread['category'] == category]
    
    def get_spreads_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """
        Get spreads filtered by difficulty.
        
        Args:
            difficulty: Difficulty level to filter by
            
        Returns:
            List of spreads with the specified difficulty
        """
        all_spreads = self.get_available_spreads()
        return [spread for spread in all_spreads if spread['difficulty'] == difficulty]
    
    def get_spread_layout(self, spread_id: str) -> Optional[SpreadLayout]:
        """
        Get a spread layout by ID.
        
        Args:
            spread_id: ID of the spread to get
            
        Returns:
            SpreadLayout if found, None otherwise
        """
        # Check templates first
        if spread_id in self.spread_templates:
            return self.spread_templates[spread_id]
        
        # Check custom spreads
        if spread_id in self.custom_spreads:
            return self.custom_spreads[spread_id]
        
        return None
    
    def create_custom_spread(
        self,
        spread_id: str,
        name: str,
        description: str,
        positions: List[Dict[str, Any]],
        category: str = "custom",
        difficulty: str = "intermediate",
        estimated_time: int = 20
    ) -> SpreadLayout:
        """
        Create a custom spread layout.
        
        Args:
            spread_id: Unique identifier for the spread
            name: Human-readable name
            description: Description of the spread
            positions: List of position dictionaries
            category: Category of the spread
            difficulty: Difficulty level
            estimated_time: Estimated time in minutes
            
        Returns:
            Created SpreadLayout
            
        Raises:
            ValueError: If spread_id already exists or positions are invalid
        """
        if spread_id in self.spread_templates or spread_id in self.custom_spreads:
            raise ValueError(f"Spread ID '{spread_id}' already exists")
        
        # Create positions
        spread_positions = []
        for pos_data in positions:
            position = SpreadPosition(
                id=pos_data['id'],
                name=pos_data['name'],
                description=pos_data['description'],
                position_type=PositionType(pos_data.get('position_type', 'custom')),
                coordinates=pos_data.get('coordinates'),
                importance=pos_data.get('importance', 1.0)
            )
            spread_positions.append(position)
        
        # Create layout
        layout = SpreadLayout(
            id=spread_id,
            name=name,
            description=description,
            positions=spread_positions,
            category=category,
            difficulty=difficulty,
            estimated_time=estimated_time
        )
        
        # Validate layout
        errors = layout.validate()
        if errors:
            raise ValueError(f"Invalid spread layout: {', '.join(errors)}")
        
        # Store custom spread
        self.custom_spreads[spread_id] = layout
        
        return layout
    
    def create_spread_from_template(
        self,
        template_id: str,
        deck: Deck,
        user_context: Optional[str] = None
    ) -> TarotSpread:
        """
        Create a tarot spread from a template.
        
        Args:
            template_id: ID of the template to use
            deck: Deck to draw cards from
            user_context: Optional user context
            
        Returns:
            TarotSpread instance
            
        Raises:
            ValueError: If template_id not found
        """
        layout = self.get_spread_layout(template_id)
        if layout is None:
            raise ValueError(f"Template '{template_id}' not found")
        
        return TarotSpread(layout, deck, user_context)
    
    def save_custom_spread(self, spread_id: str, file_path: Union[str, Path]) -> None:
        """
        Save a custom spread to a file.
        
        Args:
            spread_id: ID of the custom spread to save
            file_path: Path to save the spread to
            
        Raises:
            ValueError: If spread_id not found
        """
        layout = self.custom_spreads.get(spread_id)
        if layout is None:
            raise ValueError(f"Custom spread '{spread_id}' not found")
        
        layout.save_to_file(file_path)
    
    def load_custom_spread(self, file_path: Union[str, Path]) -> SpreadLayout:
        """
        Load a custom spread from a file.
        
        Args:
            file_path: Path to load the spread from
            
        Returns:
            Loaded SpreadLayout
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If spread_id already exists
        """
        layout = SpreadLayout.load_from_file(file_path)
        
        if layout.id in self.spread_templates or layout.id in self.custom_spreads:
            raise ValueError(f"Spread ID '{layout.id}' already exists")
        
        self.custom_spreads[layout.id] = layout
        return layout
    
    def delete_custom_spread(self, spread_id: str) -> bool:
        """
        Delete a custom spread.
        
        Args:
            spread_id: ID of the custom spread to delete
            
        Returns:
            True if deleted, False if not found
        """
        if spread_id in self.custom_spreads:
            del self.custom_spreads[spread_id]
            return True
        return False
    
    def add_recent_reading(self, reading: SpreadReading) -> None:
        """
        Add a reading to the recent readings list.
        
        Args:
            reading: Reading to add
        """
        self.recent_readings.append(reading)
        
        # Keep only the last 50 readings
        if len(self.recent_readings) > 50:
            self.recent_readings = self.recent_readings[-50:]
    
    def get_recent_readings(self, limit: int = 10) -> List[SpreadReading]:
        """
        Get recent readings.
        
        Args:
            limit: Maximum number of readings to return
            
        Returns:
            List of recent readings
        """
        return self.recent_readings[-limit:]
    
    def get_spread_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about available spreads.
        
        Returns:
            Dictionary with spread statistics
        """
        all_spreads = self.get_available_spreads()
        
        # Count by category
        categories = {}
        for spread in all_spreads:
            category = spread['category']
            categories[category] = categories.get(category, 0) + 1
        
        # Count by difficulty
        difficulties = {}
        for spread in all_spreads:
            difficulty = spread['difficulty']
            difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
        
        # Calculate average card count
        total_cards = sum(spread['card_count'] for spread in all_spreads)
        avg_cards = total_cards / len(all_spreads) if all_spreads else 0
        
        return {
            'total_spreads': len(all_spreads),
            'template_spreads': len(self.spread_templates),
            'custom_spreads': len(self.custom_spreads),
            'categories': categories,
            'difficulties': difficulties,
            'average_card_count': round(avg_cards, 1),
            'recent_readings_count': len(self.recent_readings)
        }
    
    def export_all_spreads(self, file_path: Union[str, Path]) -> None:
        """
        Export all spreads to a JSON file.
        
        Args:
            file_path: Path to save the export to
        """
        export_data = {
            'templates': {tid: layout.to_dict() for tid, layout in self.spread_templates.items()},
            'custom_spreads': {cid: layout.to_dict() for cid, layout in self.custom_spreads.items()},
            'export_date': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
    
    def import_spreads(self, file_path: Union[str, Path]) -> Dict[str, int]:
        """
        Import spreads from a JSON file.
        
        Args:
            file_path: Path to load the import from
            
        Returns:
            Dictionary with import statistics
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        imported_templates = 0
        imported_custom = 0
        skipped = 0
        
        # Import templates
        for template_id, layout_data in import_data.get('templates', {}).items():
            if template_id not in self.spread_templates:
                layout = SpreadLayout.from_dict(layout_data)
                self.spread_templates[template_id] = layout
                imported_templates += 1
            else:
                skipped += 1
        
        # Import custom spreads
        for custom_id, layout_data in import_data.get('custom_spreads', {}).items():
            if custom_id not in self.custom_spreads:
                layout = SpreadLayout.from_dict(layout_data)
                self.custom_spreads[custom_id] = layout
                imported_custom += 1
            else:
                skipped += 1
        
        return {
            'imported_templates': imported_templates,
            'imported_custom': imported_custom,
            'skipped': skipped
        }
    
    def search_spreads(self, query: str) -> List[Dict[str, Any]]:
        """
        Search spreads by name or description.
        
        Args:
            query: Search query
            
        Returns:
            List of matching spreads
        """
        query_lower = query.lower()
        all_spreads = self.get_available_spreads()
        
        matches = []
        for spread in all_spreads:
            if (query_lower in spread['name'].lower() or 
                query_lower in spread['description'].lower()):
                matches.append(spread)
        
        return matches


# Example usage and testing
if __name__ == "__main__":
    from tarot_studio.deck import Deck
    
    # Create spread manager
    manager = SpreadManager()
    
    # Get available spreads
    spreads = manager.get_available_spreads()
    print(f"Available spreads: {len(spreads)}")
    
    for spread in spreads:
        print(f"- {spread['name']}: {spread['card_count']} cards ({spread['difficulty']})")
    
    # Get spreads by category
    daily_spreads = manager.get_spreads_by_category('daily')
    print(f"\nDaily spreads: {len(daily_spreads)}")
    
    # Create a custom spread
    custom_positions = [
        {
            'id': 'situation',
            'name': 'Current Situation',
            'description': 'What is happening now',
            'position_type': 'situation',
            'coordinates': (0.3, 0.5),
            'importance': 1.0
        },
        {
            'id': 'obstacle',
            'name': 'Main Obstacle',
            'description': 'What is blocking progress',
            'position_type': 'challenge',
            'coordinates': (0.7, 0.5),
            'importance': 0.9
        },
        {
            'id': 'guidance',
            'name': 'Guidance',
            'description': 'What you need to know',
            'position_type': 'advice',
            'coordinates': (0.5, 0.3),
            'importance': 0.8
        }
    ]
    
    try:
        custom_layout = manager.create_custom_spread(
            'custom_situation',
            'Situation Analysis',
            'A 3-card spread for analyzing current situations',
            custom_positions,
            category='analysis',
            difficulty='beginner',
            estimated_time=15
        )
        print(f"\nCreated custom spread: {custom_layout.name}")
    except ValueError as e:
        print(f"Error creating custom spread: {e}")
    
    # Get statistics
    stats = manager.get_spread_statistics()
    print(f"\nSpread Statistics:")
    print(f"Total spreads: {stats['total_spreads']}")
    print(f"Categories: {stats['categories']}")
    print(f"Difficulties: {stats['difficulties']}")
    print(f"Average card count: {stats['average_card_count']}")
    
    # Test creating a spread from template
    deck = Deck.load_from_file('card_data.json')
    deck.shuffle(seed=123)
    
    three_card_spread = manager.create_spread_from_template(
        'three_card',
        deck,
        'What does my future hold?'
    )
    
    reading = three_card_spread.draw_cards()
    print(f"\nCreated reading: {reading.spread_id}")
    print(f"Layout: {three_card_spread.layout.name}")
    print(f"Cards: {len(reading.cards)}")
    
    # Add to recent readings
    manager.add_recent_reading(reading)
    print(f"Recent readings: {len(manager.get_recent_readings())}")