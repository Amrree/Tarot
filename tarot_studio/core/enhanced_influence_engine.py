"""
Enhanced Tarot Influence Engine

This module implements a comprehensive, deterministic influence engine that computes
how neighboring cards modify meanings in tarot spreads, based on established
practitioner techniques and academic research.
"""

import json
import math
from typing import List, Dict, Any, Tuple, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class Orientation(Enum):
    """Card orientation enumeration."""
    UPRIGHT = "upright"
    REVERSED = "reversed"

class Arcana(Enum):
    """Card arcana enumeration."""
    MAJOR = "major"
    MINOR = "minor"

class Element(Enum):
    """Element enumeration."""
    FIRE = "fire"
    WATER = "water"
    AIR = "air"
    EARTH = "earth"

@dataclass
class CardMetadata:
    """Card metadata with all required attributes."""
    card_id: str
    name: str
    arcana: Arcana
    suit: Optional[str] = None
    number: Optional[int] = None
    element: Optional[Element] = None
    baseline_polarity: float = 0.0
    baseline_intensity: float = 0.5
    keywords: List[str] = None
    themes: Dict[str, float] = None
    base_upright_text: str = ""
    base_reversed_text: str = ""
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.themes is None:
            self.themes = {}

@dataclass
class CardPosition:
    """Represents a card in a specific position within a spread."""
    position_id: str
    card_id: str
    orientation: Orientation
    card_metadata: CardMetadata

@dataclass
class InfluenceFactor:
    """Represents how one card influences another."""
    source_position: str
    source_card_id: str
    effect: str  # String format like "+0.40" or "-0.20"
    explain: str
    confidence: str = "high"  # high, medium, low

@dataclass
class InfluencedCard:
    """A card with computed influence modifications."""
    position: str
    card_id: str
    card_name: str
    orientation: str
    base_text: str
    influenced_text: str
    polarity_score: float
    intensity_score: float
    themes: Dict[str, float]
    influence_factors: List[InfluenceFactor]
    journal_prompt: str

@dataclass
class EngineConfig:
    """Configuration for the influence engine."""
    dominance_multiplier: float = 1.5
    reversal_decay_factor: float = 0.8
    conflict_threshold: float = 0.5
    theme_threshold: float = 0.3
    adjacency_decay_factor: float = 0.5
    enable_llm_generation: bool = True
    llm_fallback_enabled: bool = True
    reversal_strategy: str = "conservative"  # conservative, assertive
    conflict_resolution: str = "damping"  # damping, neutralization, amplification
    elemental_system: str = "traditional"  # crowley, traditional, simplified

class EnhancedInfluenceEngine:
    """Enhanced influence engine with comprehensive rule set."""
    
    def __init__(self, config: EngineConfig = None):
        self.config = config or EngineConfig()
        self.card_metadata_cache: Dict[str, CardMetadata] = {}
        self.adjacency_matrices: Dict[str, Dict[str, Dict[str, float]]] = {}
        self.elemental_affinity_matrix = self._build_elemental_affinity_matrix()
        
        # Load canonical adjacency matrices
        self._load_canonical_adjacency_matrices()
    
    def _build_elemental_affinity_matrix(self) -> Dict[str, Dict[str, float]]:
        """Build elemental affinity matrix based on research."""
        if self.config.elemental_system == "crowley":
            # Crowley's elemental dignity system
            return {
                "fire": {"fire": 1.2, "water": 0.6, "air": 1.0, "earth": 0.8},
                "water": {"fire": 0.6, "water": 1.2, "air": 0.8, "earth": 1.0},
                "air": {"fire": 1.0, "water": 0.8, "air": 1.2, "earth": 0.6},
                "earth": {"fire": 0.8, "water": 1.0, "air": 0.6, "earth": 1.2}
            }
        elif self.config.elemental_system == "simplified":
            # Simplified elemental system
            return {
                "fire": {"fire": 1.1, "water": 0.7, "air": 1.0, "earth": 0.9},
                "water": {"fire": 0.7, "water": 1.1, "air": 0.9, "earth": 1.0},
                "air": {"fire": 1.0, "water": 0.9, "air": 1.1, "earth": 0.7},
                "earth": {"fire": 0.9, "water": 1.0, "air": 0.7, "earth": 1.1}
            }
        else:  # traditional
            # Traditional elemental system
            return {
                "fire": {"fire": 1.15, "water": 0.65, "air": 1.0, "earth": 0.85},
                "water": {"fire": 0.65, "water": 1.15, "air": 0.85, "earth": 1.0},
                "air": {"fire": 1.0, "water": 0.85, "air": 1.15, "earth": 0.65},
                "earth": {"fire": 0.85, "water": 1.0, "air": 0.65, "earth": 1.15}
            }
    
    def _load_canonical_adjacency_matrices(self):
        """Load canonical adjacency matrices for standard spreads."""
        # Three-card spread
        self.adjacency_matrices["three_card"] = {
            "past": {"present": 1.0, "future": 0.5},
            "present": {"past": 1.0, "future": 1.0},
            "future": {"past": 0.5, "present": 1.0}
        }
        
        # Celtic Cross
        self.adjacency_matrices["celtic_cross"] = {
            "situation": {"challenge": 1.0, "past": 0.4, "future": 0.4, "above": 0.4, "below": 0.4},
            "challenge": {"situation": 1.0, "past": 0.4, "future": 0.4, "above": 0.4, "below": 0.4},
            "past": {"situation": 0.4, "challenge": 0.4, "future": 0.8, "advice": 0.6},
            "future": {"situation": 0.4, "challenge": 0.4, "past": 0.8, "advice": 0.6},
            "above": {"situation": 0.4, "challenge": 0.4, "below": 0.8, "advice": 0.6},
            "below": {"situation": 0.4, "challenge": 0.4, "above": 0.8, "advice": 0.6},
            "advice": {"past": 0.6, "future": 0.6, "above": 0.6, "below": 0.6, "external": 0.8},
            "external": {"advice": 0.8, "hopes_fears": 0.8, "outcome": 0.6},
            "hopes_fears": {"external": 0.8, "outcome": 0.8},
            "outcome": {"external": 0.6, "hopes_fears": 0.8}
        }
        
        # Relationship Cross
        self.adjacency_matrices["relationship_cross"] = {
            "you": {"partner": 1.0, "connection": 0.8, "challenge": 0.6},
            "partner": {"you": 1.0, "connection": 0.8, "challenge": 0.6},
            "connection": {"you": 0.8, "partner": 0.8, "challenge": 0.8, "advice": 0.8},
            "challenge": {"you": 0.6, "partner": 0.6, "connection": 0.8, "advice": 0.8},
            "advice": {"connection": 0.8, "challenge": 0.8, "outcome": 0.8, "lesson": 0.8},
            "outcome": {"advice": 0.8, "lesson": 0.8},
            "lesson": {"advice": 0.8, "outcome": 0.8}
        }
        
        # Year Ahead
        self.adjacency_matrices["year_ahead"] = {}
        months = ["january", "february", "march", "april", "may", "june",
                 "july", "august", "september", "october", "november", "december"]
        
        for i, month in enumerate(months):
            self.adjacency_matrices["year_ahead"][month] = {}
            prev_month = months[i-1] if i > 0 else months[-1]
            next_month = months[i+1] if i < len(months)-1 else months[0]
            
            self.adjacency_matrices["year_ahead"][month][prev_month] = 1.0
            self.adjacency_matrices["year_ahead"][month][next_month] = 1.0
            
            # Special case for year-end connection
            if month == "january":
                self.adjacency_matrices["year_ahead"][month]["december"] = 0.5
            elif month == "december":
                self.adjacency_matrices["year_ahead"][month]["january"] = 0.5
    
    def load_card_metadata(self, card_data: Dict[str, Any]) -> CardMetadata:
        """Load card metadata from dictionary."""
        return CardMetadata(
            card_id=card_data["card_id"],
            name=card_data["name"],
            arcana=Arcana(card_data["arcana"]),
            suit=card_data.get("suit"),
            number=card_data.get("number"),
            element=Element(card_data["element"]) if card_data.get("element") else None,
            baseline_polarity=card_data["polarity"],
            baseline_intensity=card_data["intensity"],
            keywords=card_data.get("keywords", []),
            themes=card_data.get("themes", {}),
            base_upright_text=card_data["upright_meaning"],
            base_reversed_text=card_data["reversed_meaning"]
        )
    
    def compute_influenced_meanings(
        self, 
        spread_data: Dict[str, Any],
        card_database: Dict[str, Dict[str, Any]],
        rule_overrides: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Compute influenced meanings for all cards in a spread.
        
        Args:
            spread_data: Spread input data
            card_database: Complete card database
            rule_overrides: Optional rule overrides
            
        Returns:
            Structured JSON result matching the API contract
        """
        try:
            # Validate input
            self._validate_input(spread_data, card_database)
            
            # Load card positions
            card_positions = self._load_card_positions(spread_data, card_database)
            
            # Get adjacency matrix
            adjacency_matrix = self._get_adjacency_matrix(spread_data["spread_type"], card_positions)
            
            # Apply rule pipeline
            influenced_cards = self._apply_rule_pipeline(card_positions, adjacency_matrix, rule_overrides)
            
            # Generate natural language
            influenced_cards = self._generate_natural_language(influenced_cards)
            
            # Create summary and advice
            summary = self._generate_summary(influenced_cards)
            advice = self._generate_advice(influenced_cards)
            follow_up_questions = self._generate_follow_up_questions(influenced_cards)
            
            # Build result
            result = {
                "reading_id": spread_data["reading_id"],
                "summary": summary,
                "cards": [asdict(card) for card in influenced_cards],
                "advice": advice,
                "follow_up_questions": follow_up_questions
            }
            
            # Validate output
            self._validate_output(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error computing influenced meanings: {e}")
            return self._create_error_response(spread_data["reading_id"], str(e))
    
    def _validate_input(self, spread_data: Dict[str, Any], card_database: Dict[str, Dict[str, Any]]):
        """Validate input data."""
        required_fields = ["reading_id", "spread_type", "positions"]
        for field in required_fields:
            if field not in spread_data:
                raise ValueError(f"Missing required field: {field}")
        
        for position in spread_data["positions"]:
            if position["card_id"] not in card_database:
                raise ValueError(f"Invalid card ID: {position['card_id']}")
            
            if position["orientation"] not in ["upright", "reversed"]:
                raise ValueError(f"Invalid orientation: {position['orientation']}")
    
    def _load_card_positions(self, spread_data: Dict[str, Any], card_database: Dict[str, Dict[str, Any]]) -> List[CardPosition]:
        """Load card positions with metadata."""
        card_positions = []
        
        for position_data in spread_data["positions"]:
            card_data = card_database[position_data["card_id"]]
            card_metadata = self.load_card_metadata(card_data)
            
            card_position = CardPosition(
                position_id=position_data["position_id"],
                card_id=position_data["card_id"],
                orientation=Orientation(position_data["orientation"]),
                card_metadata=card_metadata
            )
            
            card_positions.append(card_position)
        
        return card_positions
    
    def _get_adjacency_matrix(self, spread_type: str, card_positions: List[CardPosition]) -> Dict[str, Dict[str, float]]:
        """Get adjacency matrix for the spread."""
        if spread_type in self.adjacency_matrices:
            return self.adjacency_matrices[spread_type]
        else:
            # Compute dynamic adjacency matrix
            return self._compute_dynamic_adjacency_matrix(card_positions)
    
    def _compute_dynamic_adjacency_matrix(self, card_positions: List[CardPosition]) -> Dict[str, Dict[str, float]]:
        """Compute adjacency matrix for custom spreads."""
        adjacency_matrix = {}
        
        for card1 in card_positions:
            adjacency_matrix[card1.position_id] = {}
            
            for card2 in card_positions:
                if card1.position_id != card2.position_id:
                    # Use distance-based weighting
                    distance = 1.0  # Default distance
                    weight = 1.0 / (1.0 + distance * self.config.adjacency_decay_factor)
                    adjacency_matrix[card1.position_id][card2.position_id] = weight
        
        return adjacency_matrix
    
    def _apply_rule_pipeline(
        self, 
        card_positions: List[CardPosition], 
        adjacency_matrix: Dict[str, Dict[str, float]],
        rule_overrides: List[Dict[str, Any]] = None
    ) -> List[InfluencedCard]:
        """Apply the complete rule pipeline."""
        influenced_cards = []
        
        for card_pos in card_positions:
            # Initialize influenced card
            influenced_card = InfluencedCard(
                position=card_pos.position_id,
                card_id=card_pos.card_id,
                card_name=card_pos.card_metadata.name,
                orientation=card_pos.orientation.value,
                base_text=self._get_base_text(card_pos),
                influenced_text="",  # Will be filled later
                polarity_score=card_pos.card_metadata.baseline_polarity,
                intensity_score=card_pos.card_metadata.baseline_intensity,
                themes=card_pos.card_metadata.themes.copy(),
                influence_factors=[],
                journal_prompt=""
            )
            
            # Apply reversal modifier
            if card_pos.orientation == Orientation.REVERSED:
                influenced_card.polarity_score *= -0.8
                influenced_card.intensity_score *= 0.9
            
            # Get neighbors
            neighbors = self._get_neighbors(card_pos, card_positions, adjacency_matrix)
            
            # Apply rules in order
            self._apply_major_dominance(influenced_card, neighbors)
            self._apply_adjacency_influence(influenced_card, neighbors, adjacency_matrix)
            self._apply_elemental_dignities(influenced_card, neighbors)
            self._apply_numerical_sequences(influenced_card, card_positions)
            self._apply_reversal_propagation(influenced_card, neighbors)
            self._apply_conflict_resolution(influenced_card, card_positions)
            self._apply_narrative_boost(influenced_card, card_positions)
            self._apply_local_overrides(influenced_card, rule_overrides)
            
            # Normalize scores
            influenced_card.polarity_score = max(-2.0, min(2.0, influenced_card.polarity_score))
            influenced_card.intensity_score = max(0.0, min(1.0, influenced_card.intensity_score))
            
            # Generate journal prompt
            influenced_card.journal_prompt = self._generate_journal_prompt(influenced_card)
            
            influenced_cards.append(influenced_card)
        
        return influenced_cards
    
    def _get_base_text(self, card_pos: CardPosition) -> str:
        """Get base text for the card orientation."""
        if card_pos.orientation == Orientation.UPRIGHT:
            return card_pos.card_metadata.base_upright_text
        else:
            return card_pos.card_metadata.base_reversed_text
    
    def _get_neighbors(self, card_pos: CardPosition, all_cards: List[CardPosition], adjacency_matrix: Dict[str, Dict[str, float]]) -> List[CardPosition]:
        """Get neighboring cards based on adjacency matrix."""
        neighbors = []
        
        if card_pos.position_id in adjacency_matrix:
            for neighbor_pos_id, weight in adjacency_matrix[card_pos.position_id].items():
                if weight > 0:
                    neighbor = next((c for c in all_cards if c.position_id == neighbor_pos_id), None)
                    if neighbor:
                        neighbors.append(neighbor)
        
        return neighbors
    
    def _apply_major_dominance(self, influenced_card: InfluencedCard, neighbors: List[CardPosition]):
        """Apply Major Arcana dominance rule."""
        if influenced_card.card_id.startswith("the_") or influenced_card.card_id in ["strength", "justice", "temperance", "judgement"]:
            # This is a Major Arcana card
            for neighbor in neighbors:
                if not (neighbor.card_metadata.card_id.startswith("the_") or neighbor.card_metadata.card_id in ["strength", "justice", "temperance", "judgement"]):
                    # Neighbor is Minor Arcana
                    enhanced_influence = neighbor.card_metadata.baseline_polarity * self.config.dominance_multiplier
                    
                    influenced_card.influence_factors.append(InfluenceFactor(
                        source_position=neighbor.position_id,
                        source_card_id=neighbor.card_id,
                        effect=f"{enhanced_influence:+.2f}",
                        explain=f"Major Arcana dominance ({self.config.dominance_multiplier}x)",
                        confidence="high"
                    ))
    
    def _apply_adjacency_influence(self, influenced_card: InfluencedCard, neighbors: List[CardPosition], adjacency_matrix: Dict[str, Dict[str, float]]):
        """Apply adjacency influence rule."""
        for neighbor in neighbors:
            weight = adjacency_matrix.get(influenced_card.position, {}).get(neighbor.position_id, 0.0)
            if weight > 0:
                influence = neighbor.card_metadata.baseline_polarity * weight
                influenced_card.polarity_score += influence
                
                influenced_card.influence_factors.append(InfluenceFactor(
                    source_position=neighbor.position_id,
                    source_card_id=neighbor.card_id,
                    effect=f"{influence:+.2f}",
                    explain=f"Adjacency influence (weight: {weight:.2f})",
                    confidence="high"
                ))
    
    def _apply_elemental_dignities(self, influenced_card: InfluencedCard, neighbors: List[CardPosition]):
        """Apply elemental dignities rule."""
        if influenced_card.card_id in ["the_sun", "the_magician", "the_emperor", "strength", "the_tower", "judgement"]:
            card_element = "fire"
        elif influenced_card.card_id in ["the_high_priestess", "the_chariot", "death", "the_moon"]:
            card_element = "water"
        elif influenced_card.card_id in ["the_fool", "the_hierophant", "the_lovers", "justice", "the_star"]:
            card_element = "air"
        elif influenced_card.card_id in ["the_empress", "the_hermit", "temperance", "the_world"]:
            card_element = "earth"
        else:
            # Minor Arcana elemental assignment
            if influenced_card.card_id.endswith("_wands"):
                card_element = "fire"
            elif influenced_card.card_id.endswith("_cups"):
                card_element = "water"
            elif influenced_card.card_id.endswith("_swords"):
                card_element = "air"
            elif influenced_card.card_id.endswith("_pentacles"):
                card_element = "earth"
            else:
                return  # No element assigned
        
        for neighbor in neighbors:
            # Determine neighbor element
            if neighbor.card_id in ["the_sun", "the_magician", "the_emperor", "strength", "the_tower", "judgement"]:
                neighbor_element = "fire"
            elif neighbor.card_id in ["the_high_priestess", "the_chariot", "death", "the_moon"]:
                neighbor_element = "water"
            elif neighbor.card_id in ["the_fool", "the_hierophant", "the_lovers", "justice", "the_star"]:
                neighbor_element = "air"
            elif neighbor.card_id in ["the_empress", "the_hermit", "temperance", "the_world"]:
                neighbor_element = "earth"
            else:
                if neighbor.card_id.endswith("_wands"):
                    neighbor_element = "fire"
                elif neighbor.card_id.endswith("_cups"):
                    neighbor_element = "water"
                elif neighbor.card_id.endswith("_swords"):
                    neighbor_element = "air"
                elif neighbor.card_id.endswith("_pentacles"):
                    neighbor_element = "earth"
                else:
                    continue
            
            # Apply elemental affinity
            if card_element in self.elemental_affinity_matrix and neighbor_element in self.elemental_affinity_matrix[card_element]:
                affinity = self.elemental_affinity_matrix[card_element][neighbor_element]
                
                if affinity != 1.0:
                    influenced_card.polarity_score *= affinity
                    
                    influenced_card.influence_factors.append(InfluenceFactor(
                        source_position=neighbor.position_id,
                        source_card_id=neighbor.card_id,
                        effect=f"{affinity:.2f}x",
                        explain=f"Elemental affinity: {card_element} + {neighbor_element}",
                        confidence="high"
                    ))
    
    def _apply_numerical_sequences(self, influenced_card: InfluencedCard, all_cards: List[CardPosition]):
        """Apply numerical sequence detection rule."""
        # Group cards by suit
        suit_groups = {}
        for card in all_cards:
            if card.card_metadata.suit:
                if card.card_metadata.suit not in suit_groups:
                    suit_groups[card.card_metadata.suit] = []
                suit_groups[card.card_metadata.suit].append(card)
        
        # Check for sequences in the same suit
        for suit, suit_cards in suit_groups.items():
            if len(suit_cards) >= 2:
                numbers = [card.card_metadata.number for card in suit_cards if card.card_metadata.number is not None]
                numbers.sort()
                
                # Check for ascending sequence
                for i in range(len(numbers) - 1):
                    if numbers[i+1] == numbers[i] + 1:
                        # Found a sequence
                        influenced_card.themes["continuity"] = influenced_card.themes.get("continuity", 0.0) + 0.3
                        influenced_card.intensity_score += 0.1
                        
                        influenced_card.influence_factors.append(InfluenceFactor(
                            source_position="numerical_sequence",
                            source_card_id="system",
                            effect="+0.10",
                            explain=f"Numerical sequence detected in {suit} suit",
                            confidence="medium"
                        ))
                        break
    
    def _apply_reversal_propagation(self, influenced_card: InfluencedCard, neighbors: List[CardPosition]):
        """Apply reversal propagation rule."""
        reversed_neighbors = [n for n in neighbors if n.orientation == Orientation.REVERSED]
        
        if reversed_neighbors:
            decay_factor = self.config.reversal_decay_factor
            
            for neighbor in reversed_neighbors:
                stability_reduction = neighbor.card_metadata.baseline_intensity * (1.0 - decay_factor)
                influenced_card.intensity_score -= stability_reduction
                
                influenced_card.influence_factors.append(InfluenceFactor(
                    source_position=neighbor.position_id,
                    source_card_id=neighbor.card_id,
                    effect=f"-{stability_reduction:.2f}",
                    explain=f"Reversal propagation (decay: {decay_factor})",
                    confidence="high"
                ))
    
    def _apply_conflict_resolution(self, influenced_card: InfluencedCard, all_cards: List[CardPosition]):
        """Apply conflict resolution rule."""
        if self.config.conflict_resolution == "damping":
            # Check for opposing polarities
            positive_cards = [c for c in all_cards if c.card_metadata.baseline_polarity > self.config.conflict_threshold]
            negative_cards = [c for c in all_cards if c.card_metadata.baseline_polarity < -self.config.conflict_threshold]
            
            if positive_cards and negative_cards:
                # Apply damping factor
                damping_factor = 0.7
                influenced_card.polarity_score *= damping_factor
                
                influenced_card.influence_factors.append(InfluenceFactor(
                    source_position="conflict_resolution",
                    source_card_id="system",
                    effect=f"{damping_factor:.2f}x",
                    explain="Conflict resolution damping",
                    confidence="medium"
                ))
    
    def _apply_narrative_boost(self, influenced_card: InfluencedCard, all_cards: List[CardPosition]):
        """Apply narrative boost rule."""
        # Find shared themes across cards
        theme_counts = {}
        
        for card in all_cards:
            for theme, weight in card.card_metadata.themes.items():
                if weight >= self.config.theme_threshold:
                    theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Boost themes that appear in multiple cards
        for theme, count in theme_counts.items():
            if count >= 2:  # Theme appears in at least 2 cards
                boost_factor = 1.0 + (count - 1) * 0.2  # 20% boost per additional card
                
                if theme in influenced_card.themes:
                    influenced_card.themes[theme] *= boost_factor
                    
                    influenced_card.influence_factors.append(InfluenceFactor(
                        source_position="narrative_boost",
                        source_card_id="system",
                        effect=f"{boost_factor:.2f}x",
                        explain=f"Narrative boost: {theme} theme",
                        confidence="medium"
                    ))
    
    def _apply_local_overrides(self, influenced_card: InfluencedCard, rule_overrides: List[Dict[str, Any]]):
        """Apply local rule overrides."""
        if not rule_overrides:
            return
        
        for override in rule_overrides:
            if override.get("type") == "polarity_multiplier":
                if override.get("card_id") == influenced_card.card_id:
                    multiplier = override.get("multiplier", 1.0)
                    influenced_card.polarity_score *= multiplier
                    
                    influenced_card.influence_factors.append(InfluenceFactor(
                        source_position="local_override",
                        source_card_id="system",
                        effect=f"{multiplier:.2f}x",
                        explain="Local polarity override",
                        confidence="high"
                    ))
            
            elif override.get("type") == "theme_boost":
                theme = override.get("theme")
                if theme in influenced_card.themes:
                    boost_factor = override.get("boost_factor", 1.0)
                    influenced_card.themes[theme] *= boost_factor
                    
                    influenced_card.influence_factors.append(InfluenceFactor(
                        source_position="local_override",
                        source_card_id="system",
                        effect=f"{boost_factor:.2f}x",
                        explain=f"Local theme boost: {theme}",
                        confidence="high"
                    ))
    
    def _generate_natural_language(self, influenced_cards: List[InfluencedCard]) -> List[InfluencedCard]:
        """Generate natural language interpretations."""
        for card in influenced_cards:
            if self.config.enable_llm_generation:
                # Try LLM generation first
                try:
                    card.influenced_text = self._generate_llm_interpretation(card)
                except Exception as e:
                    logger.warning(f"LLM generation failed for {card.card_id}: {e}")
                    if self.config.llm_fallback_enabled:
                        card.influenced_text = self._generate_template_interpretation(card)
                    else:
                        raise
            else:
                # Use template generation
                card.influenced_text = self._generate_template_interpretation(card)
        
        return influenced_cards
    
    def _generate_template_interpretation(self, card: InfluencedCard) -> str:
        """Generate interpretation using deterministic templates."""
        base_text = card.base_text
        
        if not card.influence_factors:
            return base_text
        
        # Generate influence summary
        positive_factors = [f for f in card.influence_factors if float(f.effect.replace("x", "")) > 0]
        negative_factors = [f for f in card.influence_factors if float(f.effect.replace("x", "")) < 0]
        
        influence_summary = ""
        
        if positive_factors:
            sources = [f.source_card_id for f in positive_factors]
            influence_summary += f" This meaning is enhanced by {', '.join(sources)}. "
        
        if negative_factors:
            sources = [f.source_card_id for f in negative_factors]
            influence_summary += f" This meaning is tempered by {', '.join(sources)}. "
        
        return base_text + influence_summary
    
    def _generate_llm_interpretation(self, card: InfluencedCard) -> str:
        """Generate interpretation using LLM (placeholder for now)."""
        # This would integrate with the Ollama client
        # For now, fall back to template generation
        return self._generate_template_interpretation(card)
    
    def _generate_summary(self, influenced_cards: List[InfluencedCard]) -> str:
        """Generate overall reading summary."""
        # Simple summary based on dominant themes and polarities
        total_polarity = sum(card.polarity_score for card in influenced_cards)
        avg_polarity = total_polarity / len(influenced_cards)
        
        if avg_polarity > 0.5:
            sentiment = "positive and uplifting"
        elif avg_polarity < -0.5:
            sentiment = "challenging but transformative"
        else:
            sentiment = "balanced and nuanced"
        
        # Find dominant themes
        all_themes = {}
        for card in influenced_cards:
            for theme, weight in card.themes.items():
                all_themes[theme] = all_themes.get(theme, 0) + weight
        
        dominant_themes = sorted(all_themes.items(), key=lambda x: x[1], reverse=True)[:3]
        theme_names = [theme for theme, _ in dominant_themes]
        
        if theme_names:
            return f"A reading that is {sentiment}, focusing on {', '.join(theme_names)}."
        else:
            return f"A reading that is {sentiment}."
    
    def _generate_advice(self, influenced_cards: List[InfluencedCard]) -> List[str]:
        """Generate practical advice based on the reading."""
        advice = []
        
        # Analyze overall polarity
        total_polarity = sum(card.polarity_score for card in influenced_cards)
        
        if total_polarity > 0:
            advice.append("Embrace the positive energy around you")
            advice.append("Take action on your goals")
        elif total_polarity < 0:
            advice.append("Face challenges with courage and patience")
            advice.append("Seek support from trusted friends")
        else:
            advice.append("Maintain balance in all areas of life")
            advice.append("Trust your intuition")
        
        # Add theme-specific advice
        all_themes = {}
        for card in influenced_cards:
            for theme, weight in card.themes.items():
                all_themes[theme] = all_themes.get(theme, 0) + weight
        
        if "love" in all_themes and all_themes["love"] > 0.5:
            advice.append("Nurture your relationships")
        
        if "career" in all_themes and all_themes["career"] > 0.5:
            advice.append("Focus on your professional development")
        
        if "creativity" in all_themes and all_themes["creativity"] > 0.5:
            advice.append("Express your creative side")
        
        return advice[:5]  # Limit to 5 pieces of advice
    
    def _generate_follow_up_questions(self, influenced_cards: List[InfluencedCard]) -> List[str]:
        """Generate follow-up questions for reflection."""
        questions = []
        
        # General reflection questions
        questions.append("What does this reading tell you about your current situation?")
        questions.append("How can you apply these insights to your life?")
        
        # Theme-specific questions
        all_themes = {}
        for card in influenced_cards:
            for theme, weight in card.themes.items():
                all_themes[theme] = all_themes.get(theme, 0) + weight
        
        if "love" in all_themes and all_themes["love"] > 0.5:
            questions.append("What relationships are most important to you?")
        
        if "career" in all_themes and all_themes["career"] > 0.5:
            questions.append("What professional goals are you working toward?")
        
        if "creativity" in all_themes and all_themes["creativity"] > 0.5:
            questions.append("How can you express your creativity more fully?")
        
        return questions[:5]  # Limit to 5 questions
    
    def _generate_journal_prompt(self, card: InfluencedCard) -> str:
        """Generate journal prompt for the card."""
        base_prompt = f"Reflect on {card.card_name} in the {card.position} position. "
        
        if card.influence_factors:
            influence_summary = "Consider how the influence of " + ", ".join([f.source_card_id for f in card.influence_factors]) + " affects this card's meaning. "
            base_prompt += influence_summary
        
        base_prompt += "What does this card tell you about your current situation?"
        
        return base_prompt
    
    def _validate_output(self, result: Dict[str, Any]):
        """Validate output against schema."""
        # Check required fields
        required_fields = ["reading_id", "summary", "cards"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required output field: {field}")
        
        # Validate card structure
        for card in result["cards"]:
            required_card_fields = ["position", "card_id", "card_name", "orientation", "base_text", "influenced_text", "polarity_score", "intensity_score", "themes", "influence_factors", "journal_prompt"]
            for field in required_card_fields:
                if field not in card:
                    raise ValueError(f"Missing required card field: {field}")
            
            # Validate numeric ranges
            if not (-2.0 <= card["polarity_score"] <= 2.0):
                raise ValueError(f"Polarity score out of range: {card['polarity_score']}")
            
            if not (0.0 <= card["intensity_score"] <= 1.0):
                raise ValueError(f"Intensity score out of range: {card['intensity_score']}")
    
    def _create_error_response(self, reading_id: str, error_message: str) -> Dict[str, Any]:
        """Create error response."""
        return {
            "reading_id": reading_id,
            "summary": f"Error processing reading: {error_message}",
            "cards": [],
            "advice": ["Please check your input and try again"],
            "follow_up_questions": ["What went wrong with this reading?"]
        }

# Example usage and testing
def create_test_card_database() -> Dict[str, Dict[str, Any]]:
    """Create a test card database."""
    return {
        "the_sun": {
            "card_id": "the_sun",
            "name": "The Sun",
            "arcana": "major",
            "element": "fire",
            "polarity": 1.0,
            "intensity": 0.9,
            "keywords": ["joy", "success", "vitality"],
            "themes": {"joy": 0.9, "success": 0.8, "vitality": 0.7},
            "upright_meaning": "The Sun represents joy, success, and vitality. This card signifies achievement, optimism, and the fulfillment of goals.",
            "reversed_meaning": "Reversed, The Sun suggests temporary setbacks, overconfidence, or blocked success."
        },
        "three_of_cups": {
            "card_id": "three_of_cups",
            "name": "Three of Cups",
            "arcana": "minor",
            "suit": "cups",
            "number": 3,
            "element": "water",
            "polarity": 0.8,
            "intensity": 0.6,
            "keywords": ["celebration", "friendship", "joy"],
            "themes": {"celebration": 0.9, "friendship": 0.8, "joy": 0.7},
            "upright_meaning": "The Three of Cups represents celebration, friendship, and joy. This card signifies a time of happiness and social connection.",
            "reversed_meaning": "Reversed, the Three of Cups suggests isolation, exclusion, or lack of celebration."
        },
        "ace_of_wands": {
            "card_id": "ace_of_wands",
            "name": "Ace of Wands",
            "arcana": "minor",
            "suit": "wands",
            "number": 1,
            "element": "fire",
            "polarity": 0.8,
            "intensity": 0.7,
            "keywords": ["inspiration", "creativity", "new_beginnings"],
            "themes": {"inspiration": 0.9, "creativity": 0.8, "new_beginnings": 0.7},
            "upright_meaning": "The Ace of Wands represents new inspiration, creative energy, and the spark of new beginnings. This card signifies the potential for growth and the excitement of starting something new.",
            "reversed_meaning": "Reversed, the Ace of Wands suggests blocked creativity, lack of inspiration, or delays in new projects."
        }
    }

def create_test_spread() -> Dict[str, Any]:
    """Create a test spread."""
    return {
        "reading_id": "test_reading_001",
        "date_time": "2024-01-15T10:30:00Z",
        "spread_type": "three_card",
        "positions": [
            {"position_id": "past", "card_id": "the_sun", "orientation": "upright"},
            {"position_id": "present", "card_id": "three_of_cups", "orientation": "upright"},
            {"position_id": "future", "card_id": "ace_of_wands", "orientation": "upright"}
        ],
        "user_context": "What does my future hold?"
    }

if __name__ == "__main__":
    # Test the enhanced influence engine
    engine = EnhancedInfluenceEngine()
    card_database = create_test_card_database()
    spread_data = create_test_spread()
    
    result = engine.compute_influenced_meanings(spread_data, card_database)
    
    print("Enhanced Influence Engine Test Results:")
    print("=" * 50)
    print(f"Reading ID: {result['reading_id']}")
    print(f"Summary: {result['summary']}")
    print(f"Cards: {len(result['cards'])}")
    
    for card in result['cards']:
        print(f"\nCard: {card['card_name']} ({card['position']})")
        print(f"Polarity Score: {card['polarity_score']:.2f}")
        print(f"Intensity Score: {card['intensity_score']:.2f}")
        print(f"Influence Factors: {len(card['influence_factors'])}")
        
        for factor in card['influence_factors']:
            print(f"  - {factor['source_card_id']}: {factor['effect']} ({factor['explain']})")
        
        print(f"Influenced Text: {card['influenced_text'][:100]}...")
        print(f"Journal Prompt: {card['journal_prompt']}")
    
    print(f"\nAdvice: {result['advice']}")
    print(f"Follow-up Questions: {result['follow_up_questions']}")