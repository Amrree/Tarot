"""
Ollama AI client for Tarot Studio.

This module provides integration with local Ollama LLM for generating
tarot interpretations and conversational features.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass
import ollama
from ollama import Client
import logging

logger = logging.getLogger(__name__)

@dataclass
class AIResponse:
    """Structured response from AI."""
    reading_id: str
    cards: List[Dict[str, Any]]
    summary: str
    advice: List[str]
    follow_up_questions: List[str]
    raw_response: str

@dataclass
class ConversationContext:
    """Context for AI conversations."""
    reading_id: Optional[str] = None
    card_context: Optional[Dict[str, Any]] = None
    memory_context: List[Dict[str, Any]] = None
    conversation_history: List[Dict[str, str]] = None

class OllamaClient:
    """Client for interacting with Ollama LLM."""
    
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.client = Client(host=base_url)
        self.model_name = model_name
        self.base_url = base_url
        
    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            models = self.client.list()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False
    
    async def pull_model(self, model_name: str = None) -> bool:
        """Pull a model from Ollama registry."""
        model = model_name or self.model_name
        try:
            logger.info(f"Pulling model {model}...")
            self.client.pull(model)
            logger.info(f"Successfully pulled model {model}")
            return True
        except Exception as e:
            logger.error(f"Failed to pull model {model}: {e}")
            return False
    
    async def generate_reading_interpretation(
        self, 
        spread_data: Dict[str, Any],
        context: Optional[ConversationContext] = None
    ) -> AIResponse:
        """Generate a complete reading interpretation."""
        
        prompt = self._build_reading_prompt(spread_data, context)
        
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': 2000
                }
            )
            
            # Parse the JSON response
            response_text = response['response']
            parsed_response = self._parse_json_response(response_text)
            
            return AIResponse(
                reading_id=spread_data.get('reading_id', 'unknown'),
                cards=parsed_response.get('cards', []),
                summary=parsed_response.get('summary', ''),
                advice=parsed_response.get('advice', []),
                follow_up_questions=parsed_response.get('follow_up_questions', []),
                raw_response=response_text
            )
            
        except Exception as e:
            logger.error(f"Failed to generate reading interpretation: {e}")
            return self._create_error_response(spread_data.get('reading_id', 'unknown'))
    
    async def chat_with_card(
        self, 
        card_data: Dict[str, Any],
        user_message: str,
        context: Optional[ConversationContext] = None
    ) -> str:
        """Chat about a specific card."""
        
        prompt = self._build_card_chat_prompt(card_data, user_message, context)
        
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'max_tokens': 1000
                }
            )
            
            return response['response']
            
        except Exception as e:
            logger.error(f"Failed to generate card chat response: {e}")
            return "I'm sorry, I'm having trouble connecting to the AI right now. Please try again later."
    
    async def chat_with_reading(
        self, 
        reading_data: Dict[str, Any],
        user_message: str,
        context: Optional[ConversationContext] = None
    ) -> str:
        """Chat about a complete reading."""
        
        prompt = self._build_reading_chat_prompt(reading_data, user_message, context)
        
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'max_tokens': 1500
                }
            )
            
            return response['response']
            
        except Exception as e:
            logger.error(f"Failed to generate reading chat response: {e}")
            return "I'm sorry, I'm having trouble connecting to the AI right now. Please try again later."
    
    async def stream_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream AI response for real-time UI updates."""
        try:
            stream = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                stream=True,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9
                }
            )
            
            for chunk in stream:
                if 'response' in chunk:
                    yield chunk['response']
                    
        except Exception as e:
            logger.error(f"Failed to stream response: {e}")
            yield "Error: Unable to generate response"
    
    def _build_reading_prompt(self, spread_data: Dict[str, Any], context: Optional[ConversationContext]) -> str:
        """Build prompt for reading interpretation."""
        
        prompt = f"""You are an expert tarot reader with deep knowledge of the Rider-Waite deck. 
You are interpreting a tarot reading and must respond with a valid JSON object.

READING DATA:
{json.dumps(spread_data, indent=2)}

INSTRUCTIONS:
1. Analyze each card in its position and orientation
2. Consider how cards influence each other
3. Provide a comprehensive interpretation
4. Return ONLY valid JSON in this exact format:

{{
  "reading_id": "{spread_data.get('reading_id', 'unknown')}",
  "cards": [
    {{
      "position": "position_name",
      "card": "card_name (orientation)",
      "base_meaning": "card's base meaning",
      "influenced_meaning": "how other cards modify this meaning",
      "polarity_score": 0.5,
      "influence_factors": [
        {{"source_card": "card_name", "effect": "+0.3", "explain": "explanation"}}
      ],
      "journal_prompt": "reflection question for this card"
    }}
  ],
  "summary": "overall reading summary",
  "advice": ["practical advice item 1", "practical advice item 2"],
  "follow_up_questions": ["question 1", "question 2"]
}}

IMPORTANT: Return ONLY the JSON object, no other text."""

        if context and context.memory_context:
            prompt += f"\n\nMEMORY CONTEXT:\n{json.dumps(context.memory_context, indent=2)}"
        
        return prompt
    
    def _build_card_chat_prompt(self, card_data: Dict[str, Any], user_message: str, context: Optional[ConversationContext]) -> str:
        """Build prompt for card-specific chat."""
        
        prompt = f"""You are a knowledgeable tarot reader. The user is asking about this card:

CARD: {card_data.get('name', 'Unknown')}
ORIENTATION: {card_data.get('orientation', 'upright')}
MEANING: {card_data.get('meaning', 'No meaning provided')}
POSITION: {card_data.get('position', 'No position')}

USER QUESTION: {user_message}

Please provide a helpful, insightful response about this card. Be conversational but informative.
If you don't have enough context to answer fully, say so and ask for clarification."""

        if context and context.conversation_history:
            prompt += f"\n\nCONVERSATION HISTORY:\n"
            for msg in context.conversation_history[-5:]:  # Last 5 messages
                prompt += f"{msg['role']}: {msg['content']}\n"
        
        return prompt
    
    def _build_reading_chat_prompt(self, reading_data: Dict[str, Any], user_message: str, context: Optional[ConversationContext]) -> str:
        """Build prompt for reading-specific chat."""
        
        prompt = f"""You are a knowledgeable tarot reader. The user is asking about this reading:

READING: {reading_data.get('title', 'Untitled Reading')}
SPREAD: {reading_data.get('spread_name', 'Unknown Spread')}
CARDS: {json.dumps(reading_data.get('cards', []), indent=2)}

USER QUESTION: {user_message}

Please provide a helpful, insightful response about this reading. Consider the overall message
and how the cards work together. Be conversational but informative."""

        if context and context.conversation_history:
            prompt += f"\n\nCONVERSATION HISTORY:\n"
            for msg in context.conversation_history[-5:]:  # Last 5 messages
                prompt += f"{msg['role']}: {msg['content']}\n"
        
        return prompt
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response from AI."""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_text = response_text[start_idx:end_idx]
                return json.loads(json_text)
            else:
                # Fallback: try to parse the entire response
                return json.loads(response_text)
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {response_text}")
            return self._create_fallback_response()
    
    def _create_error_response(self, reading_id: str) -> AIResponse:
        """Create error response when AI fails."""
        return AIResponse(
            reading_id=reading_id,
            cards=[],
            summary="I'm sorry, I'm having trouble generating an interpretation right now. Please try again.",
            advice=["Try asking a more specific question", "Check your connection to the AI service"],
            follow_up_questions=["What would you like to know about this reading?"],
            raw_response=""
        )
    
    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create fallback response when JSON parsing fails."""
        return {
            "cards": [],
            "summary": "I'm having trouble processing the response. Please try again.",
            "advice": ["Try rephrasing your question", "Check the AI service connection"],
            "follow_up_questions": ["What would you like to explore further?"]
        }

# Example usage and testing
async def test_ollama_client():
    """Test the Ollama client."""
    client = OllamaClient()
    
    # Check connection
    if not await client.check_connection():
        print("Failed to connect to Ollama. Make sure Ollama is running.")
        return
    
    # Test reading interpretation
    test_spread = {
        "reading_id": "test_reading_001",
        "spread_name": "Three Card Spread",
        "cards": [
            {
                "position": "past",
                "card": "The Sun",
                "orientation": "upright",
                "meaning": "Joy, success, and vitality"
            },
            {
                "position": "present", 
                "card": "Three of Cups",
                "orientation": "upright",
                "meaning": "Celebration, friendship, and joy"
            },
            {
                "position": "future",
                "card": "Ace of Wands",
                "orientation": "upright", 
                "meaning": "New inspiration and creative energy"
            }
        ]
    }
    
    print("Testing reading interpretation...")
    response = await client.generate_reading_interpretation(test_spread)
    print(f"Summary: {response.summary}")
    print(f"Advice: {response.advice}")
    print(f"Follow-up questions: {response.follow_up_questions}")

if __name__ == "__main__":
    asyncio.run(test_ollama_client())