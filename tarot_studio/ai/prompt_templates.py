"""
Prompt Templates for Tarot Studio AI.

This module contains comprehensive prompt templates for various AI interactions,
including tarot interpretations, card meanings, and conversational features.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class PromptTemplate:
    """A prompt template for AI interactions."""
    name: str
    description: str
    template: str
    variables: List[str]
    category: str
    version: str = "1.0.0"

class PromptTemplateManager:
    """Manages prompt templates for AI interactions."""
    
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default prompt templates."""
        
        # Card Interpretation Templates
        self.templates['card_interpretation'] = PromptTemplate(
            name="card_interpretation",
            description="Interpret a single tarot card",
            template="""You are a wise tarot reader. Interpret the following tarot card for the user.

Card Information:
- Name: {card_name}
- Arcana: {arcana_type}
- Suit: {suit}
- Number: {number}
- Element: {element}
- Keywords: {keywords}
- Upright Meaning: {upright_meaning}
- Reversed Meaning: {reversed_meaning}
- Current Orientation: {orientation}

User's Question: {user_question}
Context: {context}

Please provide a thoughtful interpretation of this card in relation to their question. Consider:
1. The card's traditional meaning
2. How it relates to their specific question
3. The symbolism and imagery
4. Practical guidance or advice

Respond in a warm, conversational tone as if you're speaking directly to them.""",
            variables=[
                "card_name", "arcana_type", "suit", "number", "element", 
                "keywords", "upright_meaning", "reversed_meaning", "orientation",
                "user_question", "context"
            ],
            category="card_interpretation"
        )
        
        # Reading Interpretation Templates
        self.templates['reading_interpretation'] = PromptTemplate(
            name="reading_interpretation",
            description="Interpret a complete tarot reading",
            template="""You are a wise tarot reader. Interpret the following tarot reading for the user.

Reading Information:
- Spread: {spread_name}
- Question: {user_question}
- Date: {reading_date}

Cards and Positions:
{cards_info}

Context: {context}

Please provide a comprehensive interpretation of this reading. Consider:
1. The overall message and theme
2. How the cards work together
3. The progression from past to present to future (if applicable)
4. Key insights and guidance
5. Practical advice for moving forward

Respond in a warm, conversational tone as if you're speaking directly to them.""",
            variables=[
                "spread_name", "user_question", "reading_date", "cards_info", "context"
            ],
            category="reading_interpretation"
        )
        
        # Card Chat Templates
        self.templates['card_chat'] = PromptTemplate(
            name="card_chat",
            description="Chat with a specific tarot card",
            template="""You are the {card_name} card speaking directly to the user. You embody the energy, wisdom, and symbolism of this card.

Card Information:
- Name: {card_name}
- Meaning: {card_meaning}
- Keywords: {keywords}
- Orientation: {orientation}

User's Message: {user_message}
Previous Context: {previous_context}

As the {card_name} card, respond to their message. You should:
1. Speak as if you ARE the card
2. Draw on the card's traditional meanings and symbolism
3. Be encouraging and wise
4. Offer guidance relevant to their situation
5. Use the card's energy to inform your response

Respond in first person as the card itself.""",
            variables=[
                "card_name", "card_meaning", "keywords", "orientation", 
                "user_message", "previous_context"
            ],
            category="card_chat"
        )
        
        # Reading Chat Templates
        self.templates['reading_chat'] = PromptTemplate(
            name="reading_chat",
            description="Chat about a tarot reading",
            template="""You are a wise tarot reader discussing a tarot reading with the user.

Reading Information:
- Spread: {spread_name}
- Cards: {cards_summary}
- Original Question: {original_question}

User's Message: {user_message}
Previous Context: {previous_context}

Please respond thoughtfully to their message about this reading. Consider:
1. The specific cards and their meanings
2. How the cards relate to their current question
3. The overall message of the spread
4. Practical guidance and advice
5. Encouragement and support

Respond in a warm, conversational tone as if you're speaking directly to them.""",
            variables=[
                "spread_name", "cards_summary", "original_question", 
                "user_message", "previous_context"
            ],
            category="reading_chat"
        )
        
        # General Tarot Chat Templates
        self.templates['general_tarot_chat'] = PromptTemplate(
            name="general_tarot_chat",
            description="General tarot conversation",
            template="""You are a wise tarot reader and spiritual guide. The user is asking: {user_message}

Context: {context}

Please provide a thoughtful, helpful response. If their question is about tarot, draw on your knowledge of tarot symbolism and meanings. If it's about life guidance, offer wisdom and encouragement while staying within appropriate boundaries.

Consider:
1. The spiritual and symbolic aspects
2. Practical guidance and advice
3. Encouragement and support
4. Appropriate boundaries and limitations

Respond in a conversational, warm tone as if you're speaking directly to them.""",
            variables=["user_message", "context"],
            category="general_chat"
        )
        
        # Influence Engine Templates
        self.templates['influence_interpretation'] = PromptTemplate(
            name="influence_interpretation",
            description="Interpret influenced card meanings",
            template="""You are a wise tarot reader interpreting a card with influences from other cards.

Card Information:
- Name: {card_name}
- Position: {position}
- Base Meaning: {base_meaning}
- Influenced Meaning: {influenced_meaning}
- Influence Score: {influence_score}
- Influence Factors: {influence_factors}

Reading Context:
- Spread: {spread_name}
- Question: {user_question}
- Other Cards: {other_cards}

Please provide an interpretation that considers:
1. The base meaning of the card
2. How other cards influence this card's meaning
3. The specific influence factors at play
4. The overall message in the context of the reading
5. Practical guidance based on the influenced meaning

Respond in a warm, conversational tone.""",
            variables=[
                "card_name", "position", "base_meaning", "influenced_meaning",
                "influence_score", "influence_factors", "spread_name", 
                "user_question", "other_cards"
            ],
            category="influence_interpretation"
        )
        
        # Journal Prompt Templates
        self.templates['journal_prompt'] = PromptTemplate(
            name="journal_prompt",
            description="Generate journal prompts for readings",
            template="""Based on this tarot reading, generate thoughtful journal prompts to help the user reflect deeper.

Reading Information:
- Spread: {spread_name}
- Question: {user_question}
- Cards: {cards_summary}

Please generate 3-5 journal prompts that will help the user:
1. Reflect on the reading's message
2. Explore their feelings and thoughts
3. Consider practical next steps
4. Connect with their intuition
5. Process any emotions that arise

Make the prompts personal, introspective, and encouraging.""",
            variables=["spread_name", "user_question", "cards_summary"],
            category="journal_prompts"
        )
        
        # Advice Generation Templates
        self.templates['advice_generation'] = PromptTemplate(
            name="advice_generation",
            description="Generate practical advice from readings",
            template="""Based on this tarot reading, generate practical, actionable advice for the user.

Reading Information:
- Spread: {spread_name}
- Question: {user_question}
- Cards: {cards_summary}
- Key Themes: {key_themes}

Please generate 3-5 pieces of practical advice that will help the user:
1. Address the core issues revealed in the reading
2. Take positive action steps
3. Navigate challenges or opportunities
4. Make informed decisions
5. Move forward with confidence

Make the advice specific, actionable, and encouraging.""",
            variables=["spread_name", "user_question", "cards_summary", "key_themes"],
            category="advice_generation"
        )
        
        # Follow-up Question Templates
        self.templates['follow_up_questions'] = PromptTemplate(
            name="follow_up_questions",
            description="Generate follow-up questions for readings",
            template="""Based on this tarot reading, generate thoughtful follow-up questions to help the user explore further.

Reading Information:
- Spread: {spread_name}
- Question: {user_question}
- Cards: {cards_summary}

Please generate 3-5 follow-up questions that will help the user:
1. Explore specific aspects of the reading
2. Clarify any confusion or uncertainty
3. Dive deeper into particular cards or themes
4. Consider different perspectives
5. Connect the reading to their life situation

Make the questions open-ended, thoughtful, and encouraging.""",
            variables=["spread_name", "user_question", "cards_summary"],
            category="follow_up_questions"
        )
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a prompt template by name."""
        return self.templates.get(name)
    
    def get_templates_by_category(self, category: str) -> List[PromptTemplate]:
        """Get all templates in a category."""
        return [template for template in self.templates.values() if template.category == category]
    
    def render_template(
        self, 
        template_name: str, 
        variables: Dict[str, Any],
        custom_template: Optional[str] = None
    ) -> Optional[str]:
        """Render a template with variables."""
        template = self.get_template(template_name)
        if not template and not custom_template:
            return None
        
        template_text = custom_template or template.template
        
        try:
            return template_text.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing required variable: {e}")
    
    def create_custom_template(
        self,
        name: str,
        description: str,
        template: str,
        variables: List[str],
        category: str
    ) -> PromptTemplate:
        """Create a custom prompt template."""
        custom_template = PromptTemplate(
            name=name,
            description=description,
            template=template,
            variables=variables,
            category=category
        )
        
        self.templates[name] = custom_template
        return custom_template
    
    def format_cards_info(self, cards: List[Dict[str, Any]]) -> str:
        """Format cards information for templates."""
        if not cards:
            return "No cards drawn"
        
        formatted_cards = []
        for card in cards:
            position = card.get('position', 'Unknown Position')
            card_name = card.get('card_name', 'Unknown Card')
            orientation = card.get('orientation', 'upright')
            
            formatted_cards.append(f"- {position}: {card_name} ({orientation})")
        
        return '\n'.join(formatted_cards)
    
    def format_cards_summary(self, cards: List[Dict[str, Any]]) -> str:
        """Format cards summary for templates."""
        if not cards:
            return "No cards drawn"
        
        card_names = []
        for card in cards:
            card_name = card.get('card_name', 'Unknown Card')
            orientation = card.get('orientation', 'upright')
            card_names.append(f"{card_name} ({orientation})")
        
        return ', '.join(card_names)
    
    def format_influence_factors(self, factors: List[Dict[str, Any]]) -> str:
        """Format influence factors for templates."""
        if not factors:
            return "No influence factors"
        
        formatted_factors = []
        for factor in factors:
            factor_type = factor.get('type', 'Unknown')
            strength = factor.get('strength', 0)
            description = factor.get('description', 'No description')
            
            formatted_factors.append(f"- {factor_type} (strength: {strength}): {description}")
        
        return '\n'.join(formatted_factors)
    
    def get_all_templates(self) -> List[PromptTemplate]:
        """Get all available templates."""
        return list(self.templates.values())
    
    def get_template_categories(self) -> List[str]:
        """Get all template categories."""
        categories = set(template.category for template in self.templates.values())
        return sorted(list(categories))


# Example usage and testing
if __name__ == "__main__":
    # Create template manager
    manager = PromptTemplateManager()
    
    # Test card interpretation template
    card_variables = {
        "card_name": "The Fool",
        "arcana_type": "Major Arcana",
        "suit": "None",
        "number": "0",
        "element": "Air",
        "keywords": "new beginnings, innocence, free spirit",
        "upright_meaning": "The Fool represents new beginnings and taking a leap of faith",
        "reversed_meaning": "Reversed, The Fool suggests recklessness or being held back",
        "orientation": "upright",
        "user_question": "What should I do about my career change?",
        "context": "User is considering leaving their current job"
    }
    
    rendered_prompt = manager.render_template("card_interpretation", card_variables)
    print("Card Interpretation Prompt:")
    print(rendered_prompt)
    print("\n" + "="*50 + "\n")
    
    # Test reading interpretation template
    reading_variables = {
        "spread_name": "Three Card",
        "user_question": "What does my future hold?",
        "reading_date": datetime.now().strftime("%Y-%m-%d"),
        "cards_info": manager.format_cards_info([
            {"position": "Past", "card_name": "The Fool", "orientation": "upright"},
            {"position": "Present", "card_name": "The Magician", "orientation": "upright"},
            {"position": "Future", "card_name": "The World", "orientation": "upright"}
        ]),
        "context": "User is at a crossroads in life"
    }
    
    rendered_reading_prompt = manager.render_template("reading_interpretation", reading_variables)
    print("Reading Interpretation Prompt:")
    print(rendered_reading_prompt)
    print("\n" + "="*50 + "\n")
    
    # Test template categories
    categories = manager.get_template_categories()
    print(f"Available template categories: {categories}")
    
    # Test custom template creation
    custom_template = manager.create_custom_template(
        name="custom_advice",
        description="Custom advice template",
        template="Based on {situation}, here's my advice: {advice}",
        variables=["situation", "advice"],
        category="custom"
    )
    
    print(f"Created custom template: {custom_template.name}")
    print(f"Template categories now: {manager.get_template_categories()}")