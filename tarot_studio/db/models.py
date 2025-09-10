"""
SQLAlchemy models for Tarot Studio database.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, 
    ForeignKey, JSON, create_engine, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
import json

Base = declarative_base()

class Card(Base):
    """Tarot card model."""
    __tablename__ = 'cards'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    arcana = Column(String(10), nullable=False)  # 'major' or 'minor'
    suit = Column(String(20), nullable=True)  # Only for minor arcana
    number = Column(Integer, nullable=False)
    element = Column(String(20), nullable=True)
    astrology = Column(String(20), nullable=True)  # Only for major arcana
    keywords = Column(SQLiteJSON, nullable=False)
    polarity = Column(Float, nullable=False)
    intensity = Column(Float, nullable=False)
    upright_meaning = Column(Text, nullable=False)
    reversed_meaning = Column(Text, nullable=False)
    influence_rules = Column(SQLiteJSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    readings = relationship("ReadingCard", back_populates="card")
    
    def __repr__(self):
        return f"<Card(id='{self.id}', name='{self.name}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'arcana': self.arcana,
            'suit': self.suit,
            'number': self.number,
            'element': self.element,
            'astrology': self.astrology,
            'keywords': self.keywords,
            'polarity': self.polarity,
            'intensity': self.intensity,
            'upright_meaning': self.upright_meaning,
            'reversed_meaning': self.reversed_meaning,
            'influence_rules': self.influence_rules
        }

class Spread(Base):
    """Tarot spread layout model."""
    __tablename__ = 'spreads'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    positions = Column(SQLiteJSON, nullable=False)  # List of position definitions
    is_custom = Column(Boolean, default=False)
    created_by = Column(String(100), nullable=True)  # User who created custom spread
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    readings = relationship("Reading", back_populates="spread")
    
    def __repr__(self):
        return f"<Spread(id='{self.id}', name='{self.name}')>"

class Reading(Base):
    """Tarot reading model."""
    __tablename__ = 'readings'
    
    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    spread_id = Column(String(50), ForeignKey('spreads.id'), nullable=False)
    question = Column(Text, nullable=True)
    interpretation = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    advice = Column(SQLiteJSON, nullable=True)  # List of advice items
    tags = Column(SQLiteJSON, nullable=True)  # List of tags
    people_involved = Column(SQLiteJSON, nullable=True)  # List of people names
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    spread = relationship("Spread", back_populates="readings")
    cards = relationship("ReadingCard", back_populates="reading", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="reading")
    
    def __repr__(self):
        return f"<Reading(id='{self.id}', title='{self.title}')>"

class ReadingCard(Base):
    """Association table for readings and cards with positions and orientations."""
    __tablename__ = 'reading_cards'
    
    id = Column(Integer, primary_key=True)
    reading_id = Column(String(50), ForeignKey('readings.id'), nullable=False)
    card_id = Column(String(50), ForeignKey('cards.id'), nullable=False)
    position = Column(String(50), nullable=False)  # Position in spread
    orientation = Column(String(10), nullable=False)  # 'upright' or 'reversed'
    influenced_meaning = Column(Text, nullable=True)
    polarity_score = Column(Float, nullable=True)
    influence_factors = Column(SQLiteJSON, nullable=True)  # List of influence factors
    journal_prompt = Column(Text, nullable=True)
    
    # Relationships
    reading = relationship("Reading", back_populates="cards")
    card = relationship("Card", back_populates="readings")
    
    def __repr__(self):
        return f"<ReadingCard(reading_id='{self.reading_id}', card_id='{self.card_id}', position='{self.position}')>"

class Conversation(Base):
    """AI conversation model."""
    __tablename__ = 'conversations'
    
    id = Column(String(50), primary_key=True)
    reading_id = Column(String(50), ForeignKey('readings.id'), nullable=True)
    title = Column(String(200), nullable=False)
    context = Column(Text, nullable=True)  # Context for the conversation
    is_memory_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reading = relationship("Reading", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id='{self.id}', title='{self.title}')>"

class ConversationMessage(Base):
    """Individual message in a conversation."""
    __tablename__ = 'conversation_messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(String(50), ForeignKey('conversations.id'), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<ConversationMessage(id={self.id}, role='{self.role}')>"

class Memory(Base):
    """Semantic memory for AI context."""
    __tablename__ = 'memories'
    
    id = Column(String(50), primary_key=True)
    entity_type = Column(String(50), nullable=False)  # 'person', 'place', 'concept', etc.
    entity_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    context = Column(Text, nullable=True)  # Context where this entity was mentioned
    importance_score = Column(Float, default=1.0)
    last_mentioned = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Index for efficient searching
    __table_args__ = (
        Index('idx_memory_entity', 'entity_type', 'entity_name'),
        Index('idx_memory_importance', 'importance_score'),
    )
    
    def __repr__(self):
        return f"<Memory(id='{self.id}', entity_type='{self.entity_type}', entity_name='{self.entity_name}')>"

class UserSettings(Base):
    """User application settings."""
    __tablename__ = 'user_settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=False)
    encrypted = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserSettings(key='{self.key}')>"

# Database initialization functions
def create_database(db_path: str = "tarot_studio.db"):
    """Create database and tables."""
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Get database session."""
    Session = sessionmaker(bind=engine)
    return Session()

def load_cards_from_json(json_path: str, session):
    """Load cards from JSON file into database."""
    with open(json_path, 'r') as f:
        deck_data = json.load(f)
    
    for card_data in deck_data['cards']:
        card = Card(
            id=card_data['id'],
            name=card_data['name'],
            arcana=card_data['arcana'],
            suit=card_data.get('suit'),
            number=card_data['number'],
            element=card_data.get('element'),
            astrology=card_data.get('astrology'),
            keywords=card_data['keywords'],
            polarity=card_data['polarity'],
            intensity=card_data['intensity'],
            upright_meaning=card_data['upright_meaning'],
            reversed_meaning=card_data['reversed_meaning'],
            influence_rules=card_data['influence_rules']
        )
        session.add(card)
    
    session.commit()
    print(f"Loaded {len(deck_data['cards'])} cards into database")

def create_default_spreads(session):
    """Create default tarot spreads."""
    spreads = [
        {
            'id': 'single_card',
            'name': 'Single Card',
            'description': 'A simple one-card reading for daily guidance or quick insights.',
            'positions': [
                {'name': 'Guidance', 'description': 'What you need to know right now'}
            ]
        },
        {
            'id': 'three_card',
            'name': 'Three Card Spread',
            'description': 'Past, Present, Future reading for understanding life flow.',
            'positions': [
                {'name': 'Past', 'description': 'What has influenced your current situation'},
                {'name': 'Present', 'description': 'Your current circumstances and mindset'},
                {'name': 'Future', 'description': 'What is likely to unfold'}
            ]
        },
        {
            'id': 'celtic_cross',
            'name': 'Celtic Cross',
            'description': 'A comprehensive 10-card spread for deep insight.',
            'positions': [
                {'name': 'Present Situation', 'description': 'What is happening now'},
                {'name': 'Challenge', 'description': 'What is blocking or helping you'},
                {'name': 'Past', 'description': 'What has led to this situation'},
                {'name': 'Future', 'description': 'What is likely to happen'},
                {'name': 'Above', 'description': 'Your conscious goals and aspirations'},
                {'name': 'Below', 'description': 'Your subconscious influences'},
                {'name': 'Advice', 'description': 'How to approach the situation'},
                {'name': 'External Influences', 'description': 'People or events affecting you'},
                {'name': 'Hopes and Fears', 'description': 'Your inner hopes and concerns'},
                {'name': 'Outcome', 'description': 'The likely resolution'}
            ]
        },
        {
            'id': 'relationship_cross',
            'name': 'Relationship Cross',
            'description': 'A 7-card spread for relationship insights.',
            'positions': [
                {'name': 'You', 'description': 'Your role in the relationship'},
                {'name': 'Partner', 'description': 'Your partner\'s role'},
                {'name': 'Connection', 'description': 'What binds you together'},
                {'name': 'Challenge', 'description': 'What challenges the relationship'},
                {'name': 'Advice', 'description': 'How to strengthen the relationship'},
                {'name': 'Outcome', 'description': 'Where the relationship is heading'},
                {'name': 'Lesson', 'description': 'What you can learn from this relationship'}
            ]
        }
    ]
    
    for spread_data in spreads:
        spread = Spread(
            id=spread_data['id'],
            name=spread_data['name'],
            description=spread_data['description'],
            positions=spread_data['positions'],
            is_custom=False
        )
        session.add(spread)
    
    session.commit()
    print(f"Created {len(spreads)} default spreads")