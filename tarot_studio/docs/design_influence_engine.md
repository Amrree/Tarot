# Design Document: Tarot Influence Engine

## Overview

The Tarot Influence Engine is a deterministic system that computes how neighboring cards modify meanings in tarot spreads. It processes spread data and produces structured JSON output suitable for UI rendering, incorporating established practitioner techniques for card-to-card influence.

## Architecture

### High-Level Design

```
Input: Spread Data
    ↓
Card Metadata Loading
    ↓
Adjacency Map Computation
    ↓
Rule Pipeline Execution
    ↓
Natural Language Generation
    ↓
Output: Structured JSON
```

### Core Components

1. **Card Metadata Manager** - Loads and manages card attributes
2. **Adjacency Calculator** - Computes position-based relationships
3. **Rule Engine** - Applies influence rules in configurable order
4. **Natural Language Generator** - Produces human-readable interpretations
5. **Output Formatter** - Ensures JSON schema compliance

## Data Model

### Card Schema

```json
{
  "card_id": "string",
  "name": "string",
  "arcana": "major|minor",
  "suit": "wands|cups|swords|pentacles|null",
  "number": "integer|null",
  "element": "fire|water|air|earth|null",
  "baseline_polarity": "float (-1.0 to 1.0)",
  "baseline_intensity": "float (0.0 to 1.0)",
  "keywords": ["string"],
  "themes": {"theme_name": "float (0.0 to 1.0)"},
  "base_upright_text": "string",
  "base_reversed_text": "string"
}
```

### Spread Schema

```json
{
  "reading_id": "string",
  "date_time": "ISO8601 string",
  "spread_type": "string",
  "positions": [
    {
      "position_id": "string",
      "card_id": "string",
      "orientation": "upright|reversed"
    }
  ],
  "user_context": "string (optional)"
}
```

### Influence Primitives

```json
{
  "polarity": "float (-2.0 to 2.0)",
  "intensity": "float (0.0 to 1.0)",
  "themes": {"theme_name": "float (0.0 to 1.0)"},
  "adjacency_weight": "float (0.0 to 1.0)",
  "dominance_multiplier": "float (default 1.5)"
}
```

## Adjacency Strategy

### Standard Spread Adjacency

For canonical spreads, we use predefined adjacency matrices:

#### Three-Card Spread
```
Position Layout: [Past] [Present] [Future]
Adjacency Matrix:
- Past ↔ Present: 1.0
- Present ↔ Future: 1.0
- Past ↔ Future: 0.5 (indirect)
```

#### Celtic Cross
```
Position Layout:
[1] [2]
[3] [4] [5] [6]
    [7] [8] [9] [10]

Adjacency Matrix:
- 1 ↔ 2: 1.0 (cross)
- 2 ↔ 3: 0.8 (cross to staff)
- 3 ↔ 4: 0.8 (staff)
- 4 ↔ 5: 0.8 (staff)
- 5 ↔ 6: 0.8 (staff)
- 7 ↔ 8: 0.6 (staff)
- 8 ↔ 9: 0.6 (staff)
- 9 ↔ 10: 0.6 (staff)
- Cross positions (1,2) ↔ Staff positions (3-10): 0.4
```

### Dynamic Adjacency

For custom spreads, adjacency is computed using distance metrics:

```python
def compute_adjacency_weight(pos1, pos2, spread_layout):
    # Euclidean distance in 2D space
    distance = sqrt((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2)
    
    # Inverse distance weighting with decay factor
    weight = 1.0 / (1.0 + distance * decay_factor)
    
    return min(weight, 1.0)
```

## Rule Pipeline

### Rule Execution Order

1. **Major Dominance Adjustment** - Apply Major Arcana multipliers
2. **Adjacency Accumulation** - Compute neighbor influences
3. **Elemental Adjustments** - Apply elemental dignity rules
4. **Numerical Sequence Adjustments** - Detect and weight progressions
5. **Reversal Propagation** - Apply reversal effects
6. **Conflict Resolution** - Resolve opposing polarities
7. **Score Normalization** - Clamp values to valid ranges
8. **Theme Aggregation** - Combine and boost shared themes

### Rule Implementations

#### 1. Adjacency Influence

```python
def apply_adjacency_influence(card, neighbors, adjacency_matrix):
    total_influence = 0.0
    influence_factors = []
    
    for neighbor in neighbors:
        weight = adjacency_matrix[card.position][neighbor.position]
        influence = neighbor.baseline_polarity * weight
        total_influence += influence
        
        influence_factors.append({
            "source_position": neighbor.position,
            "source_card_id": neighbor.card_id,
            "effect": f"{influence:+.2f}",
            "explain": f"Adjacency influence from {neighbor.name}"
        })
    
    return total_influence, influence_factors
```

#### 2. Elemental Dignities

```python
def apply_elemental_dignities(card, neighbors):
    elemental_affinity_matrix = {
        "fire": {"fire": 1.2, "water": 0.6, "air": 1.0, "earth": 0.8},
        "water": {"fire": 0.6, "water": 1.2, "air": 0.8, "earth": 1.0},
        "air": {"fire": 1.0, "water": 0.8, "air": 1.2, "earth": 0.6},
        "earth": {"fire": 0.8, "water": 1.0, "air": 0.6, "earth": 1.2}
    }
    
    total_modifier = 1.0
    influence_factors = []
    
    for neighbor in neighbors:
        if card.element and neighbor.element:
            affinity = elemental_affinity_matrix[card.element][neighbor.element]
            total_modifier *= affinity
            
            influence_factors.append({
                "source_position": neighbor.position,
                "source_card_id": neighbor.card_id,
                "effect": f"{affinity:.2f}x",
                "explain": f"Elemental affinity: {card.element} + {neighbor.element}"
            })
    
    return total_modifier, influence_factors
```

#### 3. Major Dominance

```python
def apply_major_dominance(card, neighbors, dominance_multiplier=1.5):
    if card.arcana == "major":
        # Major Arcana influence neighbors more strongly
        influence_factors = []
        
        for neighbor in neighbors:
            if neighbor.arcana == "minor":
                enhanced_influence = neighbor.baseline_polarity * dominance_multiplier
                
                influence_factors.append({
                    "source_position": neighbor.position,
                    "source_card_id": neighbor.card_id,
                    "effect": f"{enhanced_influence:+.2f}",
                    "explain": f"Major Arcana dominance ({dominance_multiplier}x)"
                })
        
        return influence_factors
    
    return []
```

#### 4. Suit Predominance

```python
def apply_suit_predominance(cards):
    suit_counts = {}
    for card in cards:
        if card.suit:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
    
    dominant_suit = max(suit_counts, key=suit_counts.get) if suit_counts else None
    dominance_threshold = len(cards) * 0.4  # 40% threshold
    
    if dominant_suit and suit_counts[dominant_suit] >= dominance_threshold:
        return {
            "dominant_suit": dominant_suit,
            "boost_factor": 1.2,
            "suppress_factor": 0.8
        }
    
    return None
```

#### 5. Numerical Sequence Detection

```python
def detect_numerical_sequences(cards):
    sequences = []
    
    # Group by suit
    suit_groups = {}
    for card in cards:
        if card.suit and card.number:
            if card.suit not in suit_groups:
                suit_groups[card.suit] = []
            suit_groups[card.suit].append(card)
    
    # Detect sequences within each suit
    for suit, suit_cards in suit_groups.items():
        numbers = sorted([card.number for card in suit_cards])
        
        # Check for ascending sequence
        if len(numbers) >= 2:
            for i in range(len(numbers) - 1):
                if numbers[i+1] == numbers[i] + 1:
                    sequences.append({
                        "type": "ascending",
                        "suit": suit,
                        "start": numbers[i],
                        "length": 2
                    })
    
    return sequences
```

#### 6. Reversal Propagation

```python
def apply_reversal_propagation(card, neighbors, decay_factor=0.8):
    if card.orientation == "reversed":
        influence_factors = []
        
        for neighbor in neighbors:
            # Reversed cards reduce stability/continuity of neighbors
            stability_reduction = neighbor.baseline_intensity * (1.0 - decay_factor)
            
            influence_factors.append({
                "source_position": neighbor.position,
                "source_card_id": neighbor.card_id,
                "effect": f"-{stability_reduction:.2f}",
                "explain": f"Reversal propagation (decay: {decay_factor})"
            })
        
        return influence_factors
    
    return []
```

#### 7. Conflict Resolution

```python
def resolve_conflicts(cards, conflict_threshold=0.5):
    # Identify cards with opposing polarities
    positive_cards = [c for c in cards if c.final_polarity > conflict_threshold]
    negative_cards = [c for c in cards if c.final_polarity < -conflict_threshold]
    
    if positive_cards and negative_cards:
        # Apply damping factor to reduce extreme polarities
        damping_factor = 0.7
        
        for card in positive_cards + negative_cards:
            card.final_polarity *= damping_factor
            
            card.influence_factors.append({
                "source_position": "conflict_resolution",
                "source_card_id": "system",
                "effect": f"{damping_factor:.2f}x",
                "explain": "Conflict resolution damping"
            })
    
    return cards
```

#### 8. Narrative Boost

```python
def apply_narrative_boost(cards, theme_threshold=0.3):
    # Find shared themes across cards
    theme_counts = {}
    
    for card in cards:
        for theme, weight in card.themes.items():
            if weight >= theme_threshold:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
    
    # Boost themes that appear in multiple cards
    for theme, count in theme_counts.items():
        if count >= 2:  # Theme appears in at least 2 cards
            boost_factor = 1.0 + (count - 1) * 0.2  # 20% boost per additional card
            
            for card in cards:
                if theme in card.themes:
                    card.themes[theme] *= boost_factor
                    
                    card.influence_factors.append({
                        "source_position": "narrative_boost",
                        "source_card_id": "system",
                        "effect": f"{boost_factor:.2f}x",
                        "explain": f"Narrative boost: {theme} theme"
                    })
    
    return cards
```

#### 9. Local Overrides

```python
def apply_local_overrides(cards, rule_overrides):
    if not rule_overrides:
        return cards
    
    for override in rule_overrides:
        if override["type"] == "polarity_multiplier":
            for card in cards:
                if card.card_id == override["card_id"]:
                    card.final_polarity *= override["multiplier"]
        
        elif override["type"] == "theme_boost":
            for card in cards:
                if override["theme"] in card.themes:
                    card.themes[override["theme"]] *= override["boost_factor"]
    
    return cards
```

## Configuration Options

### Engine Configuration

```json
{
  "dominance_multiplier": 1.5,
  "reversal_decay_factor": 0.8,
  "conflict_threshold": 0.5,
  "theme_threshold": 0.3,
  "adjacency_decay_factor": 0.5,
  "enable_llm_generation": true,
  "llm_fallback_enabled": true,
  "rule_overrides": []
}
```

### Strategy Options

```json
{
  "reversal_strategy": "conservative|assertive",
  "conflict_resolution": "damping|neutralization|amplification",
  "elemental_system": "crowley|traditional|simplified"
}
```

## Natural Language Generation

### Template-Based Generation

When LLM is unavailable, the engine uses deterministic templates:

```python
def generate_influenced_text(card, influence_factors):
    base_text = card.base_upright_text if card.orientation == "upright" else card.base_reversed_text
    
    if not influence_factors:
        return base_text
    
    # Generate influence summary
    positive_factors = [f for f in influence_factors if float(f["effect"]) > 0]
    negative_factors = [f for f in influence_factors if float(f["effect"]) < 0]
    
    influence_summary = ""
    
    if positive_factors:
        sources = [f["source_card_id"] for f in positive_factors]
        influence_summary += f" This meaning is enhanced by {', '.join(sources)}. "
    
    if negative_factors:
        sources = [f["source_card_id"] for f in negative_factors]
        influence_summary += f" This meaning is tempered by {', '.join(sources)}. "
    
    return base_text + influence_summary
```

### LLM Integration

When LLM is available, the engine provides structured context:

```python
def generate_llm_prompt(card, influence_factors, numeric_scores):
    prompt = f"""
    Generate a natural language interpretation for this tarot card:
    
    Card: {card.name} ({card.orientation})
    Base Meaning: {card.base_text}
    Polarity Score: {numeric_scores['polarity']:.2f}
    Intensity Score: {numeric_scores['intensity']:.2f}
    Themes: {numeric_scores['themes']}
    
    Influence Factors:
    {json.dumps(influence_factors, indent=2)}
    
    Return ONLY a JSON object with this exact structure:
    {{
        "influenced_text": "natural language interpretation",
        "confidence": "high|medium|low",
        "key_themes": ["theme1", "theme2"],
        "journal_prompt": "reflection question"
    }}
    """
    
    return prompt
```

## API Contract

### Input Schema

```json
{
  "reading_id": "string",
  "date_time": "ISO8601 string",
  "spread_type": "string",
  "positions": [
    {
      "position_id": "string",
      "card_id": "string",
      "orientation": "upright|reversed"
    }
  ],
  "user_context": "string (optional)",
  "engine_config": "object (optional)",
  "rule_overrides": "array (optional)"
}
```

### Output Schema

```json
{
  "reading_id": "string",
  "summary": "string",
  "cards": [
    {
      "position": "string",
      "card_id": "string",
      "card_name": "string",
      "orientation": "upright|reversed",
      "base_text": "string",
      "influenced_text": "string",
      "polarity_score": "float (-2.0 to 2.0)",
      "intensity_score": "float (0.0 to 1.0)",
      "themes": {"theme_name": "float (0.0 to 1.0)"},
      "influence_factors": [
        {
          "source_position": "string",
          "source_card_id": "string",
          "effect": "string",
          "explain": "string"
        }
      ],
      "journal_prompt": "string"
    }
  ],
  "advice": ["string"],
  "follow_up_questions": ["string"]
}
```

## Error Handling

### Validation Errors

- Invalid card IDs → Return error with valid card list
- Invalid orientations → Default to "upright"
- Missing required fields → Return error with missing field list
- Invalid numeric ranges → Clamp to valid ranges with warning

### Processing Errors

- Rule application failures → Log error, continue with remaining rules
- LLM generation failures → Fall back to template generation
- Schema validation failures → Return error with validation details

## Performance Considerations

### Optimization Strategies

1. **Caching** - Cache card metadata and adjacency matrices
2. **Lazy Loading** - Load card data only when needed
3. **Batch Processing** - Process multiple cards simultaneously
4. **Rule Ordering** - Optimize rule execution order for efficiency

### Scalability

- Support for spreads up to 21 cards (Celtic Cross + additional positions)
- Configurable rule sets for different deck types
- Extensible architecture for custom rules

## Testing Strategy

### Unit Tests

- Individual rule functions with known inputs/outputs
- Edge cases for each rule type
- Configuration validation
- Schema compliance

### Integration Tests

- Complete spread processing
- Rule interaction effects
- LLM fallback behavior
- Performance benchmarks

### Validation Tests

- JSON schema compliance
- Numeric range validation
- Deterministic output verification
- Error handling coverage

## Implementation Notes

### Deterministic Behavior

The engine must produce identical outputs for identical inputs, ensuring:
- Consistent rule application order
- Deterministic random number generation (if used)
- Stable floating-point calculations
- Reproducible LLM prompts

### Extensibility

The architecture supports:
- Custom rule implementations
- Additional spread types
- Alternative elemental systems
- User-defined influence patterns

### Maintainability

Code organization follows:
- Single responsibility principle
- Clear separation of concerns
- Comprehensive documentation
- Extensive test coverage

This design provides a robust foundation for implementing a deterministic tarot influence engine that can handle complex card interactions while maintaining consistency and reliability for UI rendering.