#!/usr/bin/env python3
"""
Simple test script for the Tarot AI Module.

This script tests the core functionality of the AI module without pytest.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tarot_studio'))

from tarot_studio.ai.ollama_client import OllamaClient, ConversationContext
from tarot_studio.ai.memory import MemoryStore, MemoryEntry
from tarot_studio.ai.conversation_manager import ConversationManager
from tarot_studio.ai.prompt_templates import PromptTemplateManager
from tarot_studio.ai.ai_config import AIConfigManager
from datetime import datetime


def test_ollama_client():
    """Test OllamaClient functionality."""
    print("Testing OllamaClient...")
    
    # Create client
    client = OllamaClient("test-model", "http://localhost:11434")
    
    assert client.model_name == "test-model"
    assert client.base_url == "http://localhost:11434"
    assert len(client._available_models) == 0
    
    # Test model operations
    client._available_models = [
        type('ModelInfo', (), {
            'name': 'test-model',
            'size': 1000000000,
            'modified_at': '2024-01-01T00:00:00Z',
            'family': 'test',
            'format': 'gguf',
            'families': ['test'],
            'parameter_size': '1B',
            'quantization_level': 'Q4_0'
        })()
    ]
    
    assert client.is_model_available("test-model") == True
    assert client.is_model_available("non-existent") == False
    
    result = client.set_model("test-model")
    assert result == True
    assert client.model_name == "test-model"
    
    print("✅ OllamaClient tests passed")


def test_memory_store():
    """Test MemoryStore functionality."""
    print("Testing MemoryStore...")
    
    # Create temporary database
    import tempfile
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    try:
        memory_store = MemoryStore(temp_db.name)
        
        # Test storing memory
        memory_id = memory_store.store_memory(
            entity_type="person",
            entity_name="John Doe",
            description="A friend who loves tarot",
            context="Met at a tarot workshop",
            importance_score=0.8
        )
        assert memory_id is not None
        
        # Test searching memories
        results = memory_store.search_memories("john", limit=1)
        assert len(results) > 0
        assert "john" in results[0].memory.entity_name.lower()
        
        # Test getting recent memories
        recent_memories = memory_store.get_recent_memories(days=1, limit=10)
        assert len(recent_memories) >= 1
        assert any(memory.entity_name == "John Doe" for memory in recent_memories)
        
        print("✅ MemoryStore tests passed")
        
    finally:
        # Clean up
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)


def test_conversation_manager():
    """Test ConversationManager functionality."""
    print("Testing ConversationManager...")
    
    # Mock Ollama client and memory store
    mock_ollama_client = type('MockOllamaClient', (), {})()
    mock_memory_store = type('MockMemoryStore', (), {
        'search_memories': lambda self, query, limit: [],
        'store_memory': lambda self, memory: True
    })()
    
    conversation_manager = ConversationManager(mock_ollama_client, mock_memory_store)
    
    # Test creating session
    session = conversation_manager.create_session("card_chat", "test_user")
    assert session is not None
    assert session.conversation_type == "card_chat"
    assert session.user_id == "test_user"
    assert session.is_active == True
    
    # Test getting session
    retrieved_session = conversation_manager.get_session(session.session_id)
    assert retrieved_session == session
    
    # Test adding messages
    message = conversation_manager.add_message(
        session.session_id, "user", "Hello", {"test": "context"}
    )
    assert message is not None
    assert message.role == "user"
    assert message.content == "Hello"
    assert message.context == {"test": "context"}
    
    # Test getting session history
    history = conversation_manager.get_session_history(session.session_id)
    assert len(history) == 1
    assert history[0].content == "Hello"
    
    # Test ending session
    result = conversation_manager.end_session(session.session_id)
    assert result == True
    assert session.is_active == False
    
    print("✅ ConversationManager tests passed")


def test_prompt_templates():
    """Test PromptTemplateManager functionality."""
    print("Testing PromptTemplateManager...")
    
    template_manager = PromptTemplateManager()
    
    # Test getting templates
    assert len(template_manager.templates) > 0
    assert "card_interpretation" in template_manager.templates
    assert "reading_interpretation" in template_manager.templates
    
    # Test getting template by name
    template = template_manager.get_template("card_interpretation")
    assert template is not None
    assert template.name == "card_interpretation"
    assert template.category == "card_interpretation"
    
    # Test rendering template
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
    
    rendered = template_manager.render_template("card_interpretation", variables)
    assert rendered is not None
    assert "The Fool" in rendered
    assert "new beginnings" in rendered
    assert "What should I do?" in rendered
    
    # Test formatting functions
    cards = [
        {"position": "Past", "card_name": "The Fool", "orientation": "upright"},
        {"position": "Present", "card_name": "The Magician", "orientation": "reversed"}
    ]
    
    formatted_info = template_manager.format_cards_info(cards)
    assert "Past: The Fool (upright)" in formatted_info
    assert "Present: The Magician (reversed)" in formatted_info
    
    formatted_summary = template_manager.format_cards_summary(cards)
    assert "The Fool (upright)" in formatted_summary
    assert "The Magician (reversed)" in formatted_summary
    
    # Test creating custom template
    custom_template = template_manager.create_custom_template(
        name="custom_test",
        description="A custom test template",
        template="Hello {name}!",
        variables=["name"],
        category="custom"
    )
    
    assert custom_template.name == "custom_test"
    assert "custom_test" in template_manager.templates
    
    # Test rendering custom template
    rendered_custom = template_manager.render_template("custom_test", {"name": "Alice"})
    assert rendered_custom == "Hello Alice!"
    
    print("✅ PromptTemplateManager tests passed")


def test_ai_config():
    """Test AIConfigManager functionality."""
    print("Testing AIConfigManager...")
    
    # Create temporary config file
    import tempfile
    temp_config = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_config.close()
    
    try:
        config_manager = AIConfigManager(temp_config.name)
        
        # Test getting settings
        settings = config_manager.get_settings()
        assert settings.default_model == "llama3.2"
        assert settings.temperature == 0.7
        assert settings.max_tokens == 2048
        assert settings.enable_memory == True
        
        # Test updating settings
        config_manager.update_settings(temperature=0.8, max_tokens=1024)
        updated_settings = config_manager.get_settings()
        assert updated_settings.temperature == 0.8
        assert updated_settings.max_tokens == 1024
        
        # Test getting models
        models = config_manager.get_models()
        assert len(models) > 0
        assert any(model.name == "llama3.2" for model in models)
        
        enabled_models = config_manager.get_enabled_models()
        assert len(enabled_models) > 0
        assert all(model.enabled for model in enabled_models)
        
        recommended_models = config_manager.get_recommended_models()
        assert len(recommended_models) > 0
        assert all(model.recommended and model.enabled for model in recommended_models)
        
        # Test model operations
        model = config_manager.get_model("llama3.2")
        assert model is not None
        assert model.name == "llama3.2"
        
        # Test enabling/disabling models
        result = config_manager.disable_model("llama3.2")
        assert result == True
        assert config_manager.get_model("llama3.2").enabled == False
        
        result = config_manager.enable_model("llama3.2")
        assert result == True
        assert config_manager.get_model("llama3.2").enabled == True
        
        # Test setting default model
        result = config_manager.set_default_model("mistral")
        assert result == True
        assert config_manager.get_default_model() == "mistral"
        
        # Test configuration validation
        errors = config_manager.validate_config()
        assert len(errors) == 0  # Default config should be valid
        
        # Test configuration summary
        summary = config_manager.get_config_summary()
        assert "version" in summary
        assert "default_model" in summary
        assert "total_models" in summary
        assert "enabled_models" in summary
        assert "validation_errors" in summary
        
        # Test saving configuration
        config_manager.save_config()
        assert os.path.exists(temp_config.name)
        
        print("✅ AIConfigManager tests passed")
        
    finally:
        # Clean up
        if os.path.exists(temp_config.name):
            os.unlink(temp_config.name)


def test_integration():
    """Test integration between AI module components."""
    print("Testing AI Module Integration...")
    
    # Create temporary database
    import tempfile
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    try:
        # Test memory and template integration
        memory_store = MemoryStore(temp_db.name)
        template_manager = PromptTemplateManager()
        
        # Store memory
        memory_id = memory_store.store_memory(
            entity_type="card",
            entity_name="The Fool",
            description="The Fool represents new beginnings and taking risks",
            context="Card interpretation discussion",
            importance_score=0.8
        )
        
        # Search memories
        results = memory_store.search_memories("fool", limit=1)
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
        
        rendered = template_manager.render_template("card_interpretation", variables)
        assert rendered is not None
        assert "The Fool" in rendered
        assert "new beginnings" in rendered
        
        # Test config and template integration
        config_manager = AIConfigManager()
        settings = config_manager.get_settings()
        assert settings.temperature == 0.7
        
        templates = template_manager.get_all_templates()
        assert len(templates) > 0
        
        print("✅ AI Module Integration tests passed")
        
    finally:
        # Clean up
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)


def main():
    """Run all AI module tests."""
    print("Tarot AI Module - Test Suite")
    print("=" * 50)
    
    try:
        test_ollama_client()
        test_memory_store()
        test_conversation_manager()
        test_prompt_templates()
        test_ai_config()
        test_integration()
        
        print("\n" + "=" * 50)
        print("🎉 All AI module tests passed!")
        print("The AI module is working correctly.")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ AI module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)