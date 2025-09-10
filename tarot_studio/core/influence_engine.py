"""
Card Influence Engine for Tarot Studio.

This module implements the rule-based system that computes how neighboring cards
modify meanings in tarot spreads.
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import json
import math

@dataclass
class CardPosition:
    """Represents a card in a specific position within a spread."""
    card_id: str
    position: str
    orientation: str  # 'upright' or 'reversed'
    card_data: Dict[str, Any]

@dataclass
class InfluenceFactor:
    """Represents how one card influences another."""
    source_card: str
    effect: float
    explanation: str
    influence_type: str  # 'adjacency', 'major_arcana', 'suit_interaction', etc.

@dataclass
class InfluencedCard:
    """A card with computed influence modifications."""
    card_id: str
    position: str
    orientation: str
    base_meaning: str
    influenced_meaning: str
    polarity_score: float
    influence_factors: List[InfluenceFactor]
    journal_prompt: str

class InfluenceEngine:
    """Core engine for computing card influences in tarot spreads."""
    
    def __init__(self):
        self.major_arcana_multiplier = 1.5
        self.max_polarity_range = 2.0
        self.min_polarity_range = -2.0
        
    def compute_influenced_meanings(
        self, 
        spread_positions: List[CardPosition],
        spread_layout: Dict[str, Any]
    ) -> List[InfluencedCard]:
        """
        Compute influenced meanings for all cards in a spread.
        
        Args:
            spread_positions: List of cards with their positions and orientations
            spread_layout: Layout definition with adjacency information
            
        Returns:
            List of InfluencedCard objects with computed influences
        """
        influenced_cards = []
        
        for card_pos in spread_positions:
            # Get base meaning
            base_meaning = self._get_base_meaning(card_pos)
            
            # Compute influence factors
            influence_factors = self._compute_influence_factors(
                card_pos, spread_positions, spread_layout
            )
            
            # Calculate final polarity score
            polarity_score = self._calculate_polarity_score(
                card_pos, influence_factors
            )
            
            # Generate influenced meaning (placeholder for now)
            influenced_meaning = self._generate_influenced_meaning(
                card_pos, influence_factors, polarity_score
            )
            
            # Generate journal prompt
            journal_prompt = self._generate_journal_prompt(
                card_pos, influence_factors
            )
            
            influenced_card = InfluencedCard(
                card_id=card_pos.card_id,
                position=card_pos.position,
                orientation=card_pos.orientation,
                base_meaning=base_meaning,
                influenced_meaning=influenced_meaning,
                polarity_score=polarity_score,
                influence_factors=influence_factors,
                journal_prompt=journal_prompt
            )
            
            influenced_cards.append(influenced_card)
        
        return influenced_cards
    
    def _get_base_meaning(self, card_pos: CardPosition) -> str:
        """Get the base meaning for a card based on its orientation."""
        if card_pos.orientation == 'upright':
            return card_pos.card_data['upright_meaning']
        else:
            return card_pos.card_data['reversed_meaning']
    
    def _compute_influence_factors(
        self, 
        target_card: CardPosition,
        all_cards: List[CardPosition],
        spread_layout: Dict[str, Any]
    ) -> List[InfluenceFactor]:
        """Compute all influence factors affecting a target card."""
        influence_factors = []
        
        # Get adjacency information
        adjacency_map = self._get_adjacency_map(target_card, spread_layout)
        
        for other_card in all_cards:
            if other_card.card_id == target_card.card_id:
                continue
                
            # Check if cards are adjacent
            if other_card.position in adjacency_map:
                adjacency_weight = adjacency_map[other_card.position]
                
                # Major Arcana influence
                if other_card.card_data['arcana'] == 'major':
                    influence_factor = self._compute_major_arcana_influence(
                        target_card, other_card, adjacency_weight
                    )
                    if influence_factor:
                        influence_factors.append(influence_factor)
                
                # Suit interaction influence
                if (target_card.card_data['arcana'] == 'minor' and 
                    other_card.card_data['arcana'] == 'minor'):
                    influence_factor = self._compute_suit_interaction_influence(
                        target_card, other_card, adjacency_weight
                    )
                    if influence_factor:
                        influence_factors.append(influence_factor)
                
                # Numeric progression influence
                if (target_card.card_data['arcana'] == 'minor' and 
                    other_card.card_data['arcana'] == 'minor' and
                    target_card.card_data['suit'] == other_card.card_data['suit']):
                    influence_factor = self._compute_numeric_progression_influence(
                        target_card, other_card, adjacency_weight
                    )
                    if influence_factor:
                        influence_factors.append(influence_factor)
                
                # General adjacency influence
                influence_factor = self._compute_adjacency_influence(
                    target_card, other_card, adjacency_weight
                )
                if influence_factor:
                    influence_factors.append(influence_factor)
        
        return influence_factors
    
    def _get_adjacency_map(
        self, 
        target_card: CardPosition, 
        spread_layout: Dict[str, Any]
    ) -> Dict[str, float]:
        """Get adjacency weights for neighboring positions."""
        # This is a simplified adjacency model
        # In a real implementation, this would be based on the spread layout
        adjacency_map = {}
        
        # For now, assume all other positions are adjacent with weight 1.0
        # This would be replaced with actual layout-specific adjacency rules
        for position_info in spread_layout.get('positions', []):
            if position_info['name'] != target_card.position:
                adjacency_map[position_info['name']] = 1.0
        
        return adjacency_map
    
    def _compute_major_arcana_influence(
        self, 
        target_card: CardPosition,
        major_card: CardPosition,
        adjacency_weight: float
    ) -> Optional[InfluenceFactor]:
        """Compute influence from Major Arcana cards."""
        base_effect = major_card.card_data['polarity'] * adjacency_weight
        major_multiplier = major_card.card_data.get('influence_rules', {}).get('major_arcana_multiplier', self.major_arcana_multiplier)
        
        final_effect = base_effect * major_multiplier
        
        # Apply specific Major Arcana rules
        effect_modifier = self._get_major_arcana_modifier(major_card.card_id)
        final_effect *= effect_modifier
        
        if abs(final_effect) > 0.1:  # Only include significant influences
            return InfluenceFactor(
                source_card=major_card.card_id,
                effect=final_effect,
                explanation=f"{major_card.card_id} influences through its major arcana energy",
                influence_type="major_arcana"
            )
        
        return None
    
    def _compute_suit_interaction_influence(
        self, 
        target_card: CardPosition,
        other_card: CardPosition,
        adjacency_weight: float
    ) -> Optional[InfluenceFactor]:
        """Compute influence from suit interactions."""
        target_suit = target_card.card_data['suit']
        other_suit = other_card.card_data['suit']
        
        # Get suit interaction modifier
        suit_interactions = other_card.card_data.get('influence_rules', {}).get('suit_interaction', {})
        suit_modifier = suit_interactions.get(target_suit, 0.0)
        
        if abs(suit_modifier) > 0.05:  # Only include significant interactions
            base_effect = other_card.card_data['polarity'] * adjacency_weight * suit_modifier
            
            return InfluenceFactor(
                source_card=other_card.card_id,
                effect=base_effect,
                explanation=f"{other_card.card_id} interacts with {target_suit} energy",
                influence_type="suit_interaction"
            )
        
        return None
    
    def _compute_numeric_progression_influence(
        self, 
        target_card: CardPosition,
        other_card: CardPosition,
        adjacency_weight: float
    ) -> Optional[InfluenceFactor]:
        """Compute influence from numeric progressions within the same suit."""
        target_number = target_card.card_data['number']
        other_number = other_card.card_data['number']
        
        # Check for sequential progression
        if abs(target_number - other_number) == 1:
            progression_effect = 0.2 * adjacency_weight
            if target_number > other_number:
                progression_effect *= 1.1  # Forward progression
            else:
                progression_effect *= 0.9  # Backward progression
            
            return InfluenceFactor(
                source_card=other_card.card_id,
                effect=progression_effect,
                explanation=f"Numeric progression with {other_card.card_id}",
                influence_type="numeric_progression"
            )
        
        return None
    
    def _compute_adjacency_influence(
        self, 
        target_card: CardPosition,
        other_card: CardPosition,
        adjacency_weight: float
    ) -> Optional[InfluenceFactor]:
        """Compute general adjacency influence."""
        adjacency_bonus = other_card.card_data.get('influence_rules', {}).get('adjacency_bonus', 0.0)
        
        if abs(adjacency_bonus) > 0.05:
            base_effect = other_card.card_data['polarity'] * adjacency_weight * adjacency_bonus
            
            return InfluenceFactor(
                source_card=other_card.card_id,
                effect=base_effect,
                explanation=f"{other_card.card_id} provides adjacency influence",
                influence_type="adjacency"
            )
        
        return None
    
    def _calculate_polarity_score(
        self, 
        card_pos: CardPosition,
        influence_factors: List[InfluenceFactor]
    ) -> float:
        """Calculate the final polarity score after applying influences."""
        base_polarity = card_pos.card_data['polarity']
        
        # Apply reversal modifier
        if card_pos.orientation == 'reversed':
            base_polarity *= -0.8  # Reversed cards have reduced polarity
        
        # Sum all influence effects
        total_influence = sum(factor.effect for factor in influence_factors)
        
        # Calculate final polarity
        final_polarity = base_polarity + total_influence
        
        # Clamp to valid range
        final_polarity = max(self.min_polarity_range, min(self.max_polarity_range, final_polarity))
        
        return final_polarity
    
    def _generate_influenced_meaning(
        self, 
        card_pos: CardPosition,
        influence_factors: List[InfluenceFactor],
        polarity_score: float
    ) -> str:
        """Generate influenced meaning text."""
        base_meaning = self._get_base_meaning(card_pos)
        
        if not influence_factors:
            return base_meaning
        
        # Create influence summary
        positive_influences = [f for f in influence_factors if f.effect > 0]
        negative_influences = [f for f in influence_factors if f.effect < 0]
        
        influence_text = ""
        
        if positive_influences:
            influence_text += f" This meaning is enhanced by {', '.join([f.source_card for f in positive_influences])}. "
        
        if negative_influences:
            influence_text += f" This meaning is tempered by {', '.join([f.source_card for f in negative_influences])}. "
        
        return base_meaning + influence_text
    
    def _generate_journal_prompt(
        self, 
        card_pos: CardPosition,
        influence_factors: List[InfluenceFactor]
    ) -> str:
        """Generate a journal prompt for the card."""
        base_prompt = f"Reflect on the {card_pos.card_id} in the {card_pos.position} position. "
        
        if influence_factors:
            influence_summary = "Consider how the influence of " + ", ".join([f.source_card for f in influence_factors]) + " affects this card's meaning. "
            base_prompt += influence_summary
        
        base_prompt += "What does this card tell you about your current situation?"
        
        return base_prompt
    
    def _get_major_arcana_modifier(self, card_id: str) -> float:
        """Get specific modifier for Major Arcana cards."""
        modifiers = {
            'the_sun': 1.2,      # The Sun brightens everything
            'the_moon': 0.8,      # The Moon adds mystery
            'the_tower': 0.6,     # The Tower destabilizes
            'the_devil': 0.7,     # The Devil adds shadow
            'the_star': 1.1,      # The Star brings hope
            'the_empress': 1.1,   # The Empress nurtures
            'the_emperor': 1.0,   # The Emperor provides structure
            'the_magician': 1.1,  # The Magician amplifies
            'the_high_priestess': 0.9,  # The High Priestess adds depth
            'the_hierophant': 0.9,      # The Hierophant adds tradition
            'the_lovers': 1.1,           # The Lovers harmonizes
            'the_chariot': 1.0,          # The Chariot drives forward
            'strength': 1.1,              # Strength empowers
            'the_hermit': 0.9,            # The Hermit adds introspection
            'wheel_of_fortune': 1.0,     # Wheel brings change
            'justice': 1.0,               # Justice balances
            'the_hanged_man': 0.8,       # Hanged Man slows down
            'death': 0.9,                 # Death transforms
            'temperance': 1.0,            # Temperance moderates
            'judgement': 1.1,             # Judgement awakens
            'the_world': 1.1,             # The World completes
            'the_fool': 1.0               # The Fool brings newness
        }
        
        return modifiers.get(card_id, 1.0)

# Example usage and testing
def create_test_spread() -> Tuple[List[CardPosition], Dict[str, Any]]:
    """Create a test spread for demonstration."""
    # Mock card data
    card_data_1 = {
        'id': 'the_sun',
        'arcana': 'major',
        'polarity': 1.0,
        'intensity': 0.9,
        'upright_meaning': 'Joy, success, and vitality',
        'reversed_meaning': 'Temporary setbacks',
        'influence_rules': {
            'adjacency_bonus': 0.6,
            'major_arcana_multiplier': 1.5,
            'themes': ['joy', 'success', 'vitality']
        }
    }
    
    card_data_2 = {
        'id': 'three_of_cups',
        'arcana': 'minor',
        'suit': 'cups',
        'polarity': 0.8,
        'intensity': 0.6,
        'upright_meaning': 'Celebration, friendship, and joy',
        'reversed_meaning': 'Isolation, exclusion',
        'influence_rules': {
            'adjacency_bonus': 0.3,
            'suit_interaction': {'cups': 0.2, 'swords': -0.1, 'pentacles': 0.3, 'wands': 0.0},
            'themes': ['celebration', 'friendship', 'joy']
        }
    }
    
    card_data_3 = {
        'id': 'ace_of_wands',
        'arcana': 'minor',
        'suit': 'wands',
        'polarity': 0.8,
        'intensity': 0.7,
        'upright_meaning': 'New inspiration and creative energy',
        'reversed_meaning': 'Blocked creativity',
        'influence_rules': {
            'adjacency_bonus': 0.2,
            'suit_interaction': {'cups': 0.1, 'swords': -0.1, 'pentacles': 0.0, 'wands': 0.0},
            'themes': ['inspiration', 'creativity', 'new_beginnings']
        }
    }
    
    spread_positions = [
        CardPosition('the_sun', 'present', 'upright', card_data_1),
        CardPosition('three_of_cups', 'past', 'upright', card_data_2),
        CardPosition('ace_of_wands', 'future', 'upright', card_data_3)
    ]
    
    spread_layout = {
        'positions': [
            {'name': 'past', 'description': 'What has influenced your current situation'},
            {'name': 'present', 'description': 'Your current circumstances'},
            {'name': 'future', 'description': 'What is likely to unfold'}
        ]
    }
    
    return spread_positions, spread_layout

if __name__ == "__main__":
    # Test the influence engine
    engine = InfluenceEngine()
    spread_positions, spread_layout = create_test_spread()
    
    influenced_cards = engine.compute_influenced_meanings(spread_positions, spread_layout)
    
    print("Influence Engine Test Results:")
    print("=" * 50)
    
    for card in influenced_cards:
        print(f"\nCard: {card.card_id} ({card.position})")
        print(f"Polarity Score: {card.polarity_score:.2f}")
        print(f"Influence Factors: {len(card.influence_factors)}")
        
        for factor in card.influence_factors:
            print(f"  - {factor.source_card}: {factor.effect:+.2f} ({factor.explanation})")
        
        print(f"Influenced Meaning: {card.influenced_meaning}")
        print(f"Journal Prompt: {card.journal_prompt}")