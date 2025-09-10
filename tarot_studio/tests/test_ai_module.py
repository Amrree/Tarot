"""
Unit tests for the Tarot AI Module.

This module contains comprehensive tests for all AI-related functionality,
including Ollama client, memory system, conversation manager, and configuration.
"""

import pytest
import json
import tempfile
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

# Import AI module components
from tarot_studio.ai.ollama_client import (
    OllamaClient, AIResponse, ConversationContext, ModelInfo, AIError
)
from tarot_studio.ai.memory import MemoryStore, MemoryEntry, MemorySearchResult
from tarot_studio.ai.conversation_manager import (
    ConversationManager, ConversationMessage, ConversationSession
)
from tarot_studio.ai.prompt_templates import PromptTemplateManager, PromptTemplate
from tarot_studio.ai.ai_config import AIConfigManager, AISettings, ModelConfig, AIConfig


class TestOllamaClient:
    """Test suite for OllamaClient class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = OllamaClient("test-model", "http://localhost:11434")
    
    def test_client_initialization(self):
        """Test OllamaClient initialization."""
        assert self.client.model_name == "test-model"
        assert self.client.base_url == "http://localhost:11434"
        assert len(self.client._available_models) == 0
        assert self.client._last_connection_check == 0
    
    def test_connection_cache(self):
        """Test connection cache functionality."""
        # Test cache validity
        assert not self.client._is_connection_cache_valid()
        
        # Mock time to test cache
        with patch('time.time', return_value=1000):
            self.client._last_connection_check = 1000
            assert self.client._is_connection_cache_valid()
            
            # Test cache expiration
            with patch('time.time', return_value=1031):  # 31 seconds later
                assert not self.client._is_connection_cache_valid()
    
    @patch('tarot_studio.ai.ollama_client.Client')
    def test_check_connection_success(self, mock_client_class):
        """Test successful connection check."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.list.return_value = {
            'models': [
                {
                    'name': 'llama3.2',
                    'size': 3000000000,
                    'modified_at': '2024-01-01T00:00:00Z',
                    'family': 'llama',
                    'format': 'gguf',
                    'families': ['llama'],
                    'parameter_size': '3B',
                    'quantization_level': 'Q4_0'
                }
            ]
        }
        
        # Test async method
        import asyncio
        result = asyncio.run(self.client.check_connection())
        
        assert result == True
        assert len(self.client._available_models) == 1
        assert self.client._available_models[0].name == 'llama3.2'
    
    @patch('tarot_studio.ai.ollama_client.Client')
    def test_check_connection_failure(self, mock_client_class):
        """Test connection check failure."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.list.side_effect = Exception("Connection failed")
        
        import asyncio
        result = asyncio.run(self.client.check_connection())
        
        assert result == False
        assert len(self.client._available_models) == 0
    
    def test_get_available_models(self):
        """Test getting available models."""
        # Add some test models
        self.client._available_models = [
            ModelInfo(
                name="test-model-1",
                size=1000000000,
                modified_at="2024-01-01T00:00:00Z",
                family="test",
                format="gguf",
                families=["test"],
                parameter_size="1B",
                quantization_level="Q4_0"
            ),
            ModelInfo(
                name="test-model-2",
                size=2000000000,
                modified_at="2024-01-02T00:00:00Z",
                family="test",
                format="gguf",
                families=["test"],
                parameter_size="2B",
                quantization_level="Q4_0"
            )
        ]
        
        models = self.client.get_available_models()
        assert len(models) == 2
        assert models[0].name == "test-model-1"
        assert models[1].name == "test-model-2"
    
    def test_is_model_available(self):
        """Test model availability check."""
        self.client._available_models = [
            ModelInfo(
                name="available-model",
                size=1000000000,
                modified_at="2024-01-01T00:00:00Z",
                family="test",
                format="gguf",
                families=["test"],
                parameter_size="1B",
                quantization_level="Q4_0"
            )
        ]
        
        assert self.client.is_model_available("available-model") == True
        assert self.client.is_model_available("non-existent-model") == False
    
    def test_set_model(self):
        """Test setting active model."""
        self.client._available_models = [
            ModelInfo(
                name="test-model",
                size=1000000000,
                modified_at="2024-01-01T00:00:00Z",
                family="test",
                format="gguf",
                families=["test"],
                parameter_size="1B",
                quantization_level="Q4_0"
            )
        ]
        
        result = self.client.set_model("test-model")
        assert result == True
        assert self.client.model_name == "test-model"
        
        result = self.client.set_model("non-existent-model")
        assert result == False
        assert self.client.model_name == "test-model"  # Should not change
    
    def test_get_model_info(self):
        """Test getting model information."""
        test_model = ModelInfo(
            name="test-model",
            size=1000000000,
            modified_at="2024-01-01T00:00:00Z",
            family="test",
            format="gguf",
            families=["test"],
            parameter_size="1B",
            quantization_level="Q4_0"
        )
        
        self.client._available_models = [test_model]
        self.client.model_name = "test-model"
        
        model_info = self.client.get_model_info()
        assert model_info == test_model
        
        # Test with non-existent model
        self.client.model_name = "non-existent-model"
        model_info = self.client.get_model_info()
        assert model_info is None


class TestMemoryStore:
    """Test suite for MemoryStore class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.memory_store = MemoryStore(self.temp_db.name)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_memory_store_initialization(self):
        """Test MemoryStore initialization."""
        assert self.memory_store.db_path == self.temp_db.name
        assert os.path.exists(self.temp_db.name)
    
    def test_store_memory(self):
        """Test storing memory entries."""
        memory = MemoryEntry(
            id="test-memory-1",
            entity_type="person",
            entity_name="John Doe",
            description="A friend who loves tarot",
            context="Met at a tarot workshop",
            importance_score=0.8,
            last_mentioned=datetime.now(),
            created_at=datetime.now()
        )
        
        result = self.memory_store.store_memory(memory)
        assert result == True
    
    def test_search_memories(self):
        """Test searching memories."""
        # Store some test memories
        memories = [
            MemoryEntry(
                id="memory-1",
                entity_type="person",
                entity_name="Alice",
                description="Alice loves The Fool card",
                context="Discussed tarot cards",
                importance_score=0.9,
                last_mentioned=datetime.now(),
                created_at=datetime.now()
            ),
            MemoryEntry(
                id="memory-2",
                entity_type="card",
                entity_name="The Fool",
                description="The Fool represents new beginnings",
                context="Card interpretation",
                importance_score=0.7,
                last_mentioned=datetime.now(),
                created_at=datetime.now()
            ),
            MemoryEntry(
                id="memory-3",
                entity_type="concept",
                entity_name="New Beginnings",
                description="Starting fresh and taking risks",
                context="Life guidance",
                importance_score=0.6,
                last_mentioned=datetime.now(),
                created_at=datetime.now()
            )
        ]
        
        for memory in memories:
            self.memory_store.store_memory(memory)
        
        # Test search
        results = self.memory_store.search_memories("fool", limit=2)
        assert len(results) <= 2
        assert all("fool" in result.memory.description.lower() or 
                  "fool" in result.memory.entity_name.lower() 
                  for result in results)
        
        # Test search with different query
        results = self.memory_store.search_memories("alice", limit=1)
        assert len(results) <= 1
        if results:
            assert "alice" in results[0].memory.entity_name.lower()
    
    def test_get_memory_by_id(self):
        """Test getting memory by ID."""
        memory = MemoryEntry(
            id="test-memory-id",
            entity_type="person",
            entity_name="Test Person",
            description="Test description",
            context="Test context",
            importance_score=0.5,
            last_mentioned=datetime.now(),
            created_at=datetime.now()
        )
        
        self.memory_store.store_memory(memory)
        
        retrieved_memory = self.memory_store.get_memory_by_id("test-memory-id")
        assert retrieved_memory is not None
        assert retrieved_memory.id == "test-memory-id"
        assert retrieved_memory.entity_name == "Test Person"
        
        # Test non-existent memory
        non_existent = self.memory_store.get_memory_by_id("non-existent-id")
        assert non_existent is None
    
    def test_update_memory(self):
        """Test updating memory entries."""
        memory = MemoryEntry(
            id="update-test",
            entity_type="person",
            entity_name="Original Name",
            description="Original description",
            context="Original context",
            importance_score=0.5,
            last_mentioned=datetime.now(),
            created_at=datetime.now()
        )
        
        self.memory_store.store_memory(memory)
        
        # Update memory
        updated_memory = MemoryEntry(
            id="update-test",
            entity_type="person",
            entity_name="Updated Name",
            description="Updated description",
            context="Updated context",
            importance_score=0.8,
            last_mentioned=datetime.now(),
            created_at=memory.created_at
        )
        
        result = self.memory_store.update_memory(updated_memory)
        assert result == True
        
        # Verify update
        retrieved = self.memory_store.get_memory_by_id("update-test")
        assert retrieved.entity_name == "Updated Name"
        assert retrieved.description == "Updated description"
        assert retrieved.importance_score == 0.8
    
    def test_delete_memory(self):
        """Test deleting memory entries."""
        memory = MemoryEntry(
            id="delete-test",
            entity_type="person",
            entity_name="To Delete",
            description="This will be deleted",
            context="Delete context",
            importance_score=0.5,
            last_mentioned=datetime.now(),
            created_at=datetime.now()
        )
        
        self.memory_store.store_memory(memory)
        
        # Verify memory exists
        assert self.memory_store.get_memory_by_id("delete-test") is not None
        
        # Delete memory
        result = self.memory_store.delete_memory("delete-test")
        assert result == True
        
        # Verify memory is deleted
        assert self.memory_store.get_memory_by_id("delete-test") is None
        
        # Test deleting non-existent memory
        result = self.memory_store.delete_memory("non-existent")
        assert result == False
    
    def test_get_memories_by_type(self):
        """Test getting memories by type."""
        memories = [
            MemoryEntry(
                id="person-1",
                entity_type="person",
                entity_name="Person 1",
                description="First person",
                context="Context 1",
                importance_score=0.7,
                last_mentioned=datetime.now(),
                created_at=datetime.now()
            ),
            MemoryEntry(
                id="card-1",
                entity_type="card",
                entity_name="Card 1",
                description="First card",
                context="Context 2",
                importance_score=0.6,
                last_mentioned=datetime.now(),
                created_at=datetime.now()
            ),
            MemoryEntry(
                id="person-2",
                entity_type="person",
                entity_name="Person 2",
                description="Second person",
                context="Context 3",
                importance_score=0.8,
                last_mentioned=datetime.now(),
                created_at=datetime.now()
            )
        ]
        
        for memory in memories:
            self.memory_store.store_memory(memory)
        
        # Get person memories
        person_memories = self.memory_store.get_memories_by_type("person")
        assert len(person_memories) == 2
        assert all(memory.entity_type == "person" for memory in person_memories)
        
        # Get card memories
        card_memories = self.memory_store.get_memories_by_type("card")
        assert len(card_memories) == 1
        assert all(memory.entity_type == "card" for memory in card_memories)
    
    def test_cleanup_old_memories(self):
        """Test cleaning up old memories."""
        # Create old memory
        old_memory = MemoryEntry(
            id="old-memory",
            entity_type="person",
            entity_name="Old Person",
            description="Old description",
            context="Old context",
            importance_score=0.3,
            last_mentioned=datetime.now() - timedelta(days=35),
            created_at=datetime.now() - timedelta(days=35)
        )
        
        # Create recent memory
        recent_memory = MemoryEntry(
            id="recent-memory",
            entity_type="person",
            entity_name="Recent Person",
            description="Recent description",
            context="Recent context",
            importance_score=0.8,
            last_mentioned=datetime.now(),
            created_at=datetime.now()
        )
        
        self.memory_store.store_memory(old_memory)
        self.memory_store.store_memory(recent_memory)
        
        # Cleanup memories older than 30 days
        deleted_count = self.memory_store.cleanup_old_memories(days=30)
        assert deleted_count == 1
        
        # Verify old memory is deleted
        assert self.memory_store.get_memory_by_id("old-memory") is None
        
        # Verify recent memory still exists
        assert self.memory_store.get_memory_by_id("recent-memory") is not None


class TestConversationManager:
    """Test suite for ConversationManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_ollama_client = Mock(spec=OllamaClient)
        self.mock_memory_store = Mock(spec=MemoryStore)
        self.conversation_manager = ConversationManager(
            self.mock_ollama_client, 
            self.mock_memory_store
        )
    
    def test_conversation_manager_initialization(self):
        """Test ConversationManager initialization."""
        assert self.conversation_manager.ollama_client == self.mock_ollama_client
        assert self.conversation_manager.memory_store == self.mock_memory_store
        assert len(self.conversation_manager.active_sessions) == 0
    
    def test_create_session(self):
        """Test creating conversation sessions."""
        session = self.conversation_manager.create_session(
            conversation_type="card_chat",
            user_id="test_user"
        )
        
        assert session is not None
        assert session.conversation_type == "card_chat"
        assert session.user_id == "test_user"
        assert session.is_active == True
        assert session.session_id in self.conversation_manager.active_sessions
    
    def test_get_session(self):
        """Test getting conversation sessions."""
        session = self.conversation_manager.create_session("test_type")
        session_id = session.session_id
        
        retrieved_session = self.conversation_manager.get_session(session_id)
        assert retrieved_session == session
        
        # Test non-existent session
        non_existent = self.conversation_manager.get_session("non-existent-id")
        assert non_existent is None
    
    def test_end_session(self):
        """Test ending conversation sessions."""
        session = self.conversation_manager.create_session("test_type")
        session_id = session.session_id
        
        # Add some messages
        self.conversation_manager.add_message(session_id, "user", "Hello")
        self.conversation_manager.add_message(session_id, "assistant", "Hi there")
        
        # End session
        result = self.conversation_manager.end_session(session_id)
        assert result == True
        
        # Verify session is ended
        assert session.is_active == False
        assert session_id not in self.conversation_manager.active_sessions
        
        # Test ending non-existent session
        result = self.conversation_manager.end_session("non-existent-id")
        assert result == False
    
    def test_add_message(self):
        """Test adding messages to sessions."""
        session = self.conversation_manager.create_session("test_type")
        session_id = session.session_id
        
        # Add user message
        message = self.conversation_manager.add_message(
            session_id, "user", "Hello", {"test": "context"}
        )
        
        assert message is not None
        assert message.role == "user"
        assert message.content == "Hello"
        assert message.context == {"test": "context"}
        assert len(session.messages) == 1
        
        # Add assistant message
        message = self.conversation_manager.add_message(
            session_id, "assistant", "Hi there", metadata={"response_time": 1.5}
        )
        
        assert message is not None
        assert message.role == "assistant"
        assert message.content == "Hi there"
        assert message.metadata == {"response_time": 1.5}
        assert len(session.messages) == 2
        
        # Test adding to non-existent session
        message = self.conversation_manager.add_message(
            "non-existent-id", "user", "Hello"
        )
        assert message is None
    
    def test_get_session_history(self):
        """Test getting session history."""
        session = self.conversation_manager.create_session("test_type")
        session_id = session.session_id
        
        # Add some messages
        self.conversation_manager.add_message(session_id, "user", "Message 1")
        self.conversation_manager.add_message(session_id, "assistant", "Response 1")
        self.conversation_manager.add_message(session_id, "user", "Message 2")
        
        history = self.conversation_manager.get_session_history(session_id)
        assert len(history) == 3
        assert history[0].content == "Message 1"
        assert history[1].content == "Response 1"
        assert history[2].content == "Message 2"
        
        # Test non-existent session
        history = self.conversation_manager.get_session_history("non-existent-id")
        assert len(history) == 0
    
    def test_get_active_sessions(self):
        """Test getting active sessions."""
        # Create multiple sessions
        session1 = self.conversation_manager.create_session("type1")
        session2 = self.conversation_manager.create_session("type2")
        session3 = self.conversation_manager.create_session("type3")
        
        # End one session
        self.conversation_manager.end_session(session2.session_id)
        
        active_sessions = self.conversation_manager.get_active_sessions()
        assert len(active_sessions) == 2
        assert session1 in active_sessions
        assert session3 in active_sessions
        assert session2 not in active_sessions


class TestPromptTemplateManager:
    """Test suite for PromptTemplateManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.template_manager = PromptTemplateManager()
    
    def test_template_manager_initialization(self):
        """Test PromptTemplateManager initialization."""
        assert len(self.template_manager.templates) > 0
        assert "card_interpretation" in self.template_manager.templates
        assert "reading_interpretation" in self.template_manager.templates
        assert "card_chat" in self.template_manager.templates
    
    def test_get_template(self):
        """Test getting templates by name."""
        template = self.template_manager.get_template("card_interpretation")
        assert template is not None
        assert template.name == "card_interpretation"
        assert template.category == "card_interpretation"
        
        # Test non-existent template
        template = self.template_manager.get_template("non-existent")
        assert template is None
    
    def test_get_templates_by_category(self):
        """Test getting templates by category."""
        card_templates = self.template_manager.get_templates_by_category("card_interpretation")
        assert len(card_templates) == 1
        assert card_templates[0].name == "card_interpretation"
        
        reading_templates = self.template_manager.get_templates_by_category("reading_interpretation")
        assert len(reading_templates) == 1
        assert reading_templates[0].name == "reading_interpretation"
    
    def test_render_template(self):
        """Test rendering templates with variables."""
        variables = {
            "card_name": "The Fool",
            "arcana_type": "Major Arcana",
            "suit": "None",
            "number": "0",
            "element": "Air",
            "keywords": "new beginnings, innocence",
            "upright_meaning": "New beginnings and taking a leap of faith",
            "reversed_meaning": "Recklessness or being held back",
            "orientation": "upright",
            "user_question": "What should I do?",
            "context": "User is at a crossroads"
        }
        
        rendered = self.template_manager.render_template("card_interpretation", variables)
        assert rendered is not None
        assert "The Fool" in rendered
        assert "new beginnings" in rendered
        assert "What should I do?" in rendered
    
    def test_render_template_missing_variables(self):
        """Test rendering template with missing variables."""
        variables = {
            "card_name": "The Fool",
            "user_question": "What should I do?"
            # Missing required variables
        }
        
        with pytest.raises(ValueError, match="Missing required variable"):
            self.template_manager.render_template("card_interpretation", variables)
    
    def test_create_custom_template(self):
        """Test creating custom templates."""
        custom_template = self.template_manager.create_custom_template(
            name="custom_test",
            description="A custom test template",
            template="Hello {name}, you are {age} years old.",
            variables=["name", "age"],
            category="custom"
        )
        
        assert custom_template.name == "custom_test"
        assert custom_template.category == "custom"
        assert "custom_test" in self.template_manager.templates
        
        # Test rendering custom template
        variables = {"name": "Alice", "age": "25"}
        rendered = self.template_manager.render_template("custom_test", variables)
        assert "Hello Alice, you are 25 years old." == rendered
    
    def test_format_cards_info(self):
        """Test formatting cards information."""
        cards = [
            {"position": "Past", "card_name": "The Fool", "orientation": "upright"},
            {"position": "Present", "card_name": "The Magician", "orientation": "reversed"},
            {"position": "Future", "card_name": "The World", "orientation": "upright"}
        ]
        
        formatted = self.template_manager.format_cards_info(cards)
        assert "Past: The Fool (upright)" in formatted
        assert "Present: The Magician (reversed)" in formatted
        assert "Future: The World (upright)" in formatted
    
    def test_format_cards_summary(self):
        """Test formatting cards summary."""
        cards = [
            {"card_name": "The Fool", "orientation": "upright"},
            {"card_name": "The Magician", "orientation": "reversed"},
            {"card_name": "The World", "orientation": "upright"}
        ]
        
        summary = self.template_manager.format_cards_summary(cards)
        assert "The Fool (upright)" in summary
        assert "The Magician (reversed)" in summary
        assert "The World (upright)" in summary
    
    def test_get_template_categories(self):
        """Test getting template categories."""
        categories = self.template_manager.get_template_categories()
        assert "card_interpretation" in categories
        assert "reading_interpretation" in categories
        assert "card_chat" in categories
        assert "reading_chat" in categories
        assert "general_chat" in categories


class TestAIConfigManager:
    """Test suite for AIConfigManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_config.close()
        
        self.config_manager = AIConfigManager(self.temp_config.name)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_config.name):
            os.unlink(self.temp_config.name)
    
    def test_config_manager_initialization(self):
        """Test AIConfigManager initialization."""
        assert self.config_manager.config_path == self.temp_config.name
        assert self.config_manager.config is not None
        assert len(self.config_manager.config.models) > 0
    
    def test_get_settings(self):
        """Test getting AI settings."""
        settings = self.config_manager.get_settings()
        assert settings.default_model == "llama3.2"
        assert settings.temperature == 0.7
        assert settings.max_tokens == 2048
        assert settings.enable_memory == True
    
    def test_update_settings(self):
        """Test updating AI settings."""
        self.config_manager.update_settings(
            temperature=0.8,
            max_tokens=1024,
            enable_memory=False
        )
        
        settings = self.config_manager.get_settings()
        assert settings.temperature == 0.8
        assert settings.max_tokens == 1024
        assert settings.enable_memory == False
    
    def test_get_models(self):
        """Test getting all models."""
        models = self.config_manager.get_models()
        assert len(models) > 0
        assert any(model.name == "llama3.2" for model in models)
        assert any(model.name == "mistral" for model in models)
    
    def test_get_enabled_models(self):
        """Test getting enabled models."""
        enabled_models = self.config_manager.get_enabled_models()
        assert len(enabled_models) > 0
        assert all(model.enabled for model in enabled_models)
    
    def test_get_recommended_models(self):
        """Test getting recommended models."""
        recommended_models = self.config_manager.get_recommended_models()
        assert len(recommended_models) > 0
        assert all(model.recommended and model.enabled for model in recommended_models)
    
    def test_get_model(self):
        """Test getting specific model."""
        model = self.config_manager.get_model("llama3.2")
        assert model is not None
        assert model.name == "llama3.2"
        assert model.display_name == "Llama 3.2"
        
        # Test non-existent model
        model = self.config_manager.get_model("non-existent")
        assert model is None
    
    def test_enable_disable_model(self):
        """Test enabling and disabling models."""
        # Disable a model
        result = self.config_manager.disable_model("llama3.2")
        assert result == True
        
        model = self.config_manager.get_model("llama3.2")
        assert model.enabled == False
        
        # Enable the model
        result = self.config_manager.enable_model("llama3.2")
        assert result == True
        
        model = self.config_manager.get_model("llama3.2")
        assert model.enabled == True
    
    def test_set_default_model(self):
        """Test setting default model."""
        result = self.config_manager.set_default_model("mistral")
        assert result == True
        
        default_model = self.config_manager.get_default_model()
        assert default_model == "mistral"
        
        # Test setting non-existent model
        result = self.config_manager.set_default_model("non-existent")
        assert result == False
    
    def test_add_remove_model(self):
        """Test adding and removing models."""
        new_model = ModelConfig(
            name="test-model",
            display_name="Test Model",
            description="A test model",
            size="1B",
            family="test",
            recommended=False,
            enabled=True
        )
        
        # Add model
        result = self.config_manager.add_model(new_model)
        assert result == True
        
        model = self.config_manager.get_model("test-model")
        assert model is not None
        assert model.name == "test-model"
        
        # Remove model
        result = self.config_manager.remove_model("test-model")
        assert result == True
        
        model = self.config_manager.get_model("test-model")
        assert model is None
    
    def test_validate_config(self):
        """Test configuration validation."""
        errors = self.config_manager.validate_config()
        assert len(errors) == 0  # Default config should be valid
        
        # Test invalid configuration
        self.config_manager.update_settings(temperature=3.0)  # Invalid temperature
        errors = self.config_manager.validate_config()
        assert len(errors) > 0
        assert any("Temperature" in error for error in errors)
    
    def test_save_load_config(self):
        """Test saving and loading configuration."""
        # Update some settings
        self.config_manager.update_settings(temperature=0.8, max_tokens=1024)
        
        # Save configuration
        self.config_manager.save_config()
        assert os.path.exists(self.temp_config.name)
        
        # Create new config manager and load
        new_config_manager = AIConfigManager(self.temp_config.name)
        settings = new_config_manager.get_settings()
        assert settings.temperature == 0.8
        assert settings.max_tokens == 1024
    
    def test_export_import_config(self):
        """Test exporting and importing configuration."""
        # Update some settings
        self.config_manager.update_settings(temperature=0.9)
        
        # Export configuration
        export_path = self.temp_config.name + ".export"
        result = self.config_manager.export_config(export_path)
        assert result == True
        assert os.path.exists(export_path)
        
        # Import configuration
        new_config_manager = AIConfigManager()
        result = new_config_manager.import_config(export_path)
        assert result == True
        
        settings = new_config_manager.get_settings()
        assert settings.temperature == 0.9
        
        # Clean up
        os.unlink(export_path)
    
    def test_get_config_summary(self):
        """Test getting configuration summary."""
        summary = self.config_manager.get_config_summary()
        
        assert "version" in summary
        assert "default_model" in summary
        assert "total_models" in summary
        assert "enabled_models" in summary
        assert "validation_errors" in summary
        
        assert summary["default_model"] == "llama3.2"
        assert summary["total_models"] > 0
        assert summary["enabled_models"] > 0
        assert len(summary["validation_errors"]) == 0


class TestAIIntegration:
    """Integration tests for AI module components."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.memory_store = MemoryStore(self.temp_db.name)
        self.template_manager = PromptTemplateManager()
        self.config_manager = AIConfigManager()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_memory_and_template_integration(self):
        """Test integration between memory and template systems."""
        # Store some memories
        memory = MemoryEntry(
            id="test-memory",
            entity_type="card",
            entity_name="The Fool",
            description="The Fool represents new beginnings and taking risks",
            context="Card interpretation discussion",
            importance_score=0.8,
            last_mentioned=datetime.now(),
            created_at=datetime.now()
        )
        self.memory_store.store_memory(memory)
        
        # Search memories
        results = self.memory_store.search_memories("fool", limit=1)
        assert len(results) > 0
        
        # Use template with memory context
        variables = {
            "card_name": "The Fool",
            "arcana_type": "Major Arcana",
            "suit": "None",
            "number": "0",
            "element": "Air",
            "keywords": "new beginnings, innocence",
            "upright_meaning": "New beginnings and taking a leap of faith",
            "reversed_meaning": "Recklessness or being held back",
            "orientation": "upright",
            "user_question": "What does The Fool mean for me?",
            "context": f"Previous discussion: {results[0].memory.description}"
        }
        
        rendered = self.template_manager.render_template("card_interpretation", variables)
        assert rendered is not None
        assert "The Fool" in rendered
        assert "new beginnings" in rendered
    
    def test_config_and_template_integration(self):
        """Test integration between config and template systems."""
        # Get current settings
        settings = self.config_manager.get_settings()
        assert settings.temperature == 0.7
        
        # Get available templates
        templates = self.template_manager.get_all_templates()
        assert len(templates) > 0
        
        # Test that config settings can influence template rendering
        # (This would be used in actual AI generation)
        card_template = self.template_manager.get_template("card_interpretation")
        assert card_template is not None
        assert card_template.category == "card_interpretation"
    
    def test_conversation_and_memory_integration(self):
        """Test integration between conversation and memory systems."""
        # Mock Ollama client for conversation manager
        mock_ollama_client = Mock(spec=OllamaClient)
        conversation_manager = ConversationManager(mock_ollama_client, self.memory_store)
        
        # Create session
        session = conversation_manager.create_session("card_chat")
        
        # Add messages
        conversation_manager.add_message(session.session_id, "user", "Tell me about The Fool")
        conversation_manager.add_message(session.session_id, "assistant", "The Fool represents new beginnings...")
        
        # Get session history
        history = conversation_manager.get_session_history(session.session_id)
        assert len(history) == 2
        
        # End session (this should store conversation in memory)
        conversation_manager.end_session(session.session_id)
        
        # Check if conversation was stored in memory
        memories = self.memory_store.search_memories("conversation", limit=1)
        assert len(memories) > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])