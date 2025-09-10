"""
Conversation Manager for Tarot Studio AI.

This module manages AI conversations, including chat with cards and readings,
context management, and conversation flow.
"""

import json
import uuid
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass, field
from datetime import datetime
import logging

from .ollama_client import OllamaClient, ConversationContext, AIResponse
from .memory import MemoryStore, MemoryEntry

logger = logging.getLogger(__name__)

@dataclass
class ConversationMessage:
    """A message in a conversation."""
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    context: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConversationSession:
    """A conversation session."""
    session_id: str
    user_id: Optional[str]
    conversation_type: str  # 'card_chat', 'reading_chat', 'general'
    context: ConversationContext
    messages: List[ConversationMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    is_active: bool = True

class ConversationManager:
    """Manages AI conversations and chat functionality."""
    
    def __init__(self, ollama_client: OllamaClient, memory_store: MemoryStore):
        self.ollama_client = ollama_client
        self.memory_store = memory_store
        self.active_sessions: Dict[str, ConversationSession] = {}
        self._session_lock = {}
        
    def create_session(
        self, 
        conversation_type: str = "general",
        user_id: Optional[str] = None,
        context: Optional[ConversationContext] = None
    ) -> ConversationSession:
        """Create a new conversation session."""
        session_id = str(uuid.uuid4())
        
        if context is None:
            context = ConversationContext(session_id=session_id)
        else:
            context.session_id = session_id
        
        session = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            conversation_type=conversation_type,
            context=context
        )
        
        self.active_sessions[session_id] = session
        self._session_lock[session_id] = False
        
        logger.info(f"Created conversation session {session_id} of type {conversation_type}")
        return session
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Get a conversation session by ID."""
        return self.active_sessions.get(session_id)
    
    def end_session(self, session_id: str) -> bool:
        """End a conversation session."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.is_active = False
            session.last_activity = datetime.now()
            
            # Store conversation in memory
            self._store_conversation_in_memory(session)
            
            del self.active_sessions[session_id]
            del self._session_lock[session_id]
            
            logger.info(f"Ended conversation session {session_id}")
            return True
        return False
    
    def add_message(
        self, 
        session_id: str, 
        role: str, 
        content: str,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[ConversationMessage]:
        """Add a message to a conversation session."""
        session = self.get_session(session_id)
        if not session or not session.is_active:
            return None
        
        message = ConversationMessage(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            timestamp=datetime.now(),
            context=context,
            metadata=metadata or {}
        )
        
        session.messages.append(message)
        session.last_activity = datetime.now()
        
        return message
    
    async def chat_with_card(
        self,
        session_id: str,
        card_data: Dict[str, Any],
        user_message: str,
        reading_context: Optional[Dict[str, Any]] = None
    ) -> Optional[AIResponse]:
        """Chat with a specific tarot card."""
        session = self.get_session(session_id)
        if not session:
            return None
        
        # Add user message
        self.add_message(session_id, "user", user_message, {"card": card_data})
        
        # Prepare context
        context = session.context
        context.card_context = card_data
        if reading_context:
            context.memory_context.append(reading_context)
        
        # Generate AI response
        try:
            response = await self._generate_card_response(card_data, user_message, context)
            
            # Add AI response to conversation
            if response:
                self.add_message(session_id, "assistant", response.summary, {"response": response})
                
                # Store relevant information in memory
                self._store_card_interaction_in_memory(card_data, user_message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in card chat: {e}")
            error_response = AIResponse(
                reading_id=session_id,
                cards=[],
                summary=f"I apologize, but I'm having trouble processing your question about {card_data.get('name', 'this card')}. Please try again.",
                advice=[],
                follow_up_questions=["Would you like to try asking about a different aspect of this card?"],
                raw_response=""
            )
            self.add_message(session_id, "assistant", error_response.summary)
            return error_response
    
    async def chat_with_reading(
        self,
        session_id: str,
        reading_data: Dict[str, Any],
        user_message: str
    ) -> Optional[AIResponse]:
        """Chat about a complete tarot reading."""
        session = self.get_session(session_id)
        if not session:
            return None
        
        # Add user message
        self.add_message(session_id, "user", user_message, {"reading": reading_data})
        
        # Prepare context
        context = session.context
        context.reading_id = reading_data.get('spread_id')
        context.memory_context.append(reading_data)
        
        # Generate AI response
        try:
            response = await self._generate_reading_response(reading_data, user_message, context)
            
            # Add AI response to conversation
            if response:
                self.add_message(session_id, "assistant", response.summary, {"response": response})
                
                # Store relevant information in memory
                self._store_reading_interaction_in_memory(reading_data, user_message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in reading chat: {e}")
            error_response = AIResponse(
                reading_id=session_id,
                cards=[],
                summary="I apologize, but I'm having trouble processing your question about this reading. Please try again.",
                advice=[],
                follow_up_questions=["Would you like to ask about a specific card or aspect of the reading?"],
                raw_response=""
            )
            self.add_message(session_id, "assistant", error_response.summary)
            return error_response
    
    async def general_chat(
        self,
        session_id: str,
        user_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[AIResponse]:
        """General conversation with the AI."""
        session = self.get_session(session_id)
        if not session:
            return None
        
        # Add user message
        self.add_message(session_id, "user", user_message, context)
        
        # Prepare context
        conversation_context = session.context
        if context:
            conversation_context.memory_context.append(context)
        
        # Generate AI response
        try:
            response = await self._generate_general_response(user_message, conversation_context)
            
            # Add AI response to conversation
            if response:
                self.add_message(session_id, "assistant", response.summary, {"response": response})
            
            return response
            
        except Exception as e:
            logger.error(f"Error in general chat: {e}")
            error_response = AIResponse(
                reading_id=session_id,
                cards=[],
                summary="I apologize, but I'm having trouble processing your message. Please try again.",
                advice=[],
                follow_up_questions=["Is there something specific about tarot you'd like to discuss?"],
                raw_response=""
            )
            self.add_message(session_id, "assistant", error_response.summary)
            return error_response
    
    async def _generate_card_response(
        self,
        card_data: Dict[str, Any],
        user_message: str,
        context: ConversationContext
    ) -> Optional[AIResponse]:
        """Generate AI response for card chat."""
        # Build prompt for card chat
        prompt = self._build_card_chat_prompt(card_data, user_message, context)
        
        # Get AI response
        response_text = await self.ollama_client.generate_response(prompt, context)
        
        if not response_text:
            return None
        
        # Parse response into structured format
        return self._parse_ai_response(response_text, context.reading_id or "card_chat")
    
    async def _generate_reading_response(
        self,
        reading_data: Dict[str, Any],
        user_message: str,
        context: ConversationContext
    ) -> Optional[AIResponse]:
        """Generate AI response for reading chat."""
        # Build prompt for reading chat
        prompt = self._build_reading_chat_prompt(reading_data, user_message, context)
        
        # Get AI response
        response_text = await self.ollama_client.generate_response(prompt, context)
        
        if not response_text:
            return None
        
        # Parse response into structured format
        return self._parse_ai_response(response_text, context.reading_id or "reading_chat")
    
    async def _generate_general_response(
        self,
        user_message: str,
        context: ConversationContext
    ) -> Optional[AIResponse]:
        """Generate AI response for general chat."""
        # Build prompt for general chat
        prompt = self._build_general_chat_prompt(user_message, context)
        
        # Get AI response
        response_text = await self.ollama_client.generate_response(prompt, context)
        
        if not response_text:
            return None
        
        # Parse response into structured format
        return self._parse_ai_response(response_text, "general_chat")
    
    def _build_card_chat_prompt(
        self,
        card_data: Dict[str, Any],
        user_message: str,
        context: ConversationContext
    ) -> str:
        """Build prompt for card chat."""
        card_name = card_data.get('name', 'Unknown Card')
        card_meaning = card_data.get('meaning', 'No meaning available')
        card_keywords = card_data.get('keywords', [])
        
        # Get relevant memories
        memories = self.memory_store.search_memories(f"{card_name} {user_message}", limit=3)
        memory_context = ""
        if memories:
            memory_context = "\nRelevant context from past conversations:\n"
            for memory in memories:
                memory_context += f"- {memory.memory.description}\n"
        
        prompt = f"""You are a wise tarot reader helping someone understand the {card_name} card.

Card Information:
- Name: {card_name}
- Meaning: {card_meaning}
- Keywords: {', '.join(card_keywords)}

User's Question: {user_message}
{memory_context}

Please provide a thoughtful, insightful response about this card in relation to their question. Be encouraging and helpful, drawing on tarot wisdom and the card's symbolism.

Respond in a conversational, warm tone as if you're speaking directly to them."""

        return prompt
    
    def _build_reading_chat_prompt(
        self,
        reading_data: Dict[str, Any],
        user_message: str,
        context: ConversationContext
    ) -> str:
        """Build prompt for reading chat."""
        spread_name = reading_data.get('layout_name', 'Unknown Spread')
        cards = reading_data.get('cards', [])
        
        # Format cards information
        cards_info = ""
        for card_info in cards:
            cards_info += f"- {card_info.get('position', 'Unknown Position')}: {card_info.get('card_name', 'Unknown Card')} ({card_info.get('orientation', 'upright')})\n"
        
        # Get relevant memories
        memories = self.memory_store.search_memories(f"{spread_name} {user_message}", limit=3)
        memory_context = ""
        if memories:
            memory_context = "\nRelevant context from past conversations:\n"
            for memory in memories:
                memory_context += f"- {memory.memory.description}\n"
        
        prompt = f"""You are a wise tarot reader helping someone understand their tarot reading.

Reading Information:
- Spread: {spread_name}
- Cards drawn:
{cards_info}

User's Question: {user_message}
{memory_context}

Please provide a thoughtful, insightful response about this reading in relation to their question. Consider the overall message of the spread and how the cards work together. Be encouraging and helpful, drawing on tarot wisdom.

Respond in a conversational, warm tone as if you're speaking directly to them."""

        return prompt
    
    def _build_general_chat_prompt(
        self,
        user_message: str,
        context: ConversationContext
    ) -> str:
        """Build prompt for general chat."""
        # Get relevant memories
        memories = self.memory_store.search_memories(user_message, limit=3)
        memory_context = ""
        if memories:
            memory_context = "\nRelevant context from past conversations:\n"
            for memory in memories:
                memory_context += f"- {memory.memory.description}\n"
        
        prompt = f"""You are a wise tarot reader and spiritual guide. The user is asking: {user_message}
{memory_context}

Please provide a thoughtful, helpful response. If their question is about tarot, draw on your knowledge of tarot symbolism and meanings. If it's about life guidance, offer wisdom and encouragement while staying within appropriate boundaries.

Respond in a conversational, warm tone as if you're speaking directly to them."""

        return prompt
    
    def _parse_ai_response(self, response_text: str, reading_id: str) -> AIResponse:
        """Parse AI response into structured format."""
        # Try to extract structured information from response
        summary = response_text.strip()
        
        # Extract advice (look for bullet points or numbered lists)
        advice = []
        follow_up_questions = []
        
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('•', '-', '*', '1.', '2.', '3.')):
                if '?' in line:
                    follow_up_questions.append(line.lstrip('•-*123. '))
                else:
                    advice.append(line.lstrip('•-*123. '))
        
        return AIResponse(
            reading_id=reading_id,
            cards=[],
            summary=summary,
            advice=advice,
            follow_up_questions=follow_up_questions,
            raw_response=response_text
        )
    
    def _store_conversation_in_memory(self, session: ConversationSession):
        """Store conversation in memory for future reference."""
        if not session.messages:
            return
        
        # Create memory entry for the conversation
        conversation_summary = f"Conversation about {session.conversation_type}"
        if session.context.card_context:
            conversation_summary += f" regarding {session.context.card_context.get('name', 'a card')}"
        elif session.context.reading_id:
            conversation_summary += f" regarding reading {session.context.reading_id}"
        
        memory_entry = MemoryEntry(
            id=str(uuid.uuid4()),
            entity_type='conversation',
            entity_name=f"Session {session.session_id}",
            description=conversation_summary,
            context=json.dumps({
                'session_id': session.session_id,
                'conversation_type': session.conversation_type,
                'message_count': len(session.messages),
                'duration': (session.last_activity - session.created_at).total_seconds()
            }),
            importance_score=0.5,
            last_mentioned=datetime.now(),
            created_at=session.created_at
        )
        
        self.memory_store.store_memory(memory_entry)
    
    def _store_card_interaction_in_memory(
        self,
        card_data: Dict[str, Any],
        user_message: str,
        response: AIResponse
    ):
        """Store card interaction in memory."""
        card_name = card_data.get('name', 'Unknown Card')
        
        memory_entry = MemoryEntry(
            id=str(uuid.uuid4()),
            entity_type='card',
            entity_name=card_name,
            description=f"Discussion about {card_name}: {user_message[:100]}...",
            context=json.dumps({
                'card_data': card_data,
                'user_message': user_message,
                'response_summary': response.summary[:200]
            }),
            importance_score=0.7,
            last_mentioned=datetime.now(),
            created_at=datetime.now()
        )
        
        self.memory_store.store_memory(memory_entry)
    
    def _store_reading_interaction_in_memory(
        self,
        reading_data: Dict[str, Any],
        user_message: str,
        response: AIResponse
    ):
        """Store reading interaction in memory."""
        reading_id = reading_data.get('spread_id', 'Unknown Reading')
        
        memory_entry = MemoryEntry(
            id=str(uuid.uuid4()),
            entity_type='reading',
            entity_name=f"Reading {reading_id}",
            description=f"Discussion about reading {reading_id}: {user_message[:100]}...",
            context=json.dumps({
                'reading_data': reading_data,
                'user_message': user_message,
                'response_summary': response.summary[:200]
            }),
            importance_score=0.8,
            last_mentioned=datetime.now(),
            created_at=datetime.now()
        )
        
        self.memory_store.store_memory(memory_entry)
    
    def get_session_history(self, session_id: str) -> List[ConversationMessage]:
        """Get conversation history for a session."""
        session = self.get_session(session_id)
        if session:
            return session.messages.copy()
        return []
    
    def get_active_sessions(self) -> List[ConversationSession]:
        """Get all active conversation sessions."""
        return [session for session in self.active_sessions.values() if session.is_active]
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Clean up old inactive sessions."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        sessions_to_remove = []
        for session_id, session in self.active_sessions.items():
            if session.last_activity < cutoff_time:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            self.end_session(session_id)
        
        logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")


# Import timedelta for cleanup function
from datetime import timedelta