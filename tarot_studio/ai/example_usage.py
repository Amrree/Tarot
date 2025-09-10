"""
Example Usage of the Tarot AI Module

This file demonstrates how to use the AI module for various tarot-related
AI interactions, including card chat, reading interpretation, and conversation management.
"""

import asyncio
import json
from datetime import datetime
from tarot_studio.ai.ollama_client import OllamaClient, ConversationContext
from tarot_studio.ai.memory import MemoryStore
from tarot_studio.ai.conversation_manager import ConversationManager
from tarot_studio.ai.prompt_templates import PromptTemplateManager
from tarot_studio.ai.ai_config import AIConfigManager


def example_ollama_client():
    """Example of using OllamaClient."""
    print("=== OllamaClient Example ===")
    
    # Create client
    client = OllamaClient("llama3.2", "http://localhost:11434")
    
    print(f"Model: {client.model_name}")
    print(f"Base URL: {client.base_url}")
    
    # Check connection (this would be async in real usage)
    print("Checking connection...")
    # is_connected = await client.check_connection()
    # print(f"Connected: {is_connected}")
    
    # Get available models
    models = client.get_available_models()
    print(f"Available models: {len(models)}")
    for model in models:
        print(f"  - {model.name} ({model.size})")
    
    # Set model
    result = client.set_model("llama3.2")
    print(f"Set model result: {result}")
    
    # Get model info
    model_info = client.get_model_info()
    if model_info:
        print(f"Current model: {model_info.name}")
        print(f"Size: {model_info.size}")
        print(f"Family: {model_info.family}")
    
    return client


def example_memory_store():
    """Example of using MemoryStore."""
    print("\n=== MemoryStore Example ===")
    
    # Create memory store
    memory_store = MemoryStore("example_memories.db")
    
    # Store some memories
    print("Storing memories...")
    
    memory_id1 = memory_store.store_memory(
        entity_type="person",
        entity_name="Alice",
        description="Alice loves The Fool card and is interested in new beginnings",
        context="Met at a tarot workshop",
        importance_score=0.8
    )
    print(f"Stored memory 1: {memory_id1}")
    
    memory_id2 = memory_store.store_memory(
        entity_type="card",
        entity_name="The Fool",
        description="The Fool represents new beginnings, innocence, and taking risks",
        context="Card interpretation discussion",
        importance_score=0.9
    )
    print(f"Stored memory 2: {memory_id2}")
    
    memory_id3 = memory_store.store_memory(
        entity_type="concept",
        entity_name="Career Change",
        description="Alice is considering a career change and seeking guidance",
        context="Life guidance session",
        importance_score=0.7
    )
    print(f"Stored memory 3: {memory_id3}")
    
    # Search memories
    print("\nSearching memories...")
    
    results = memory_store.search_memories("fool", limit=3)
    print(f"Found {len(results)} memories for 'fool':")
    for result in results:
        print(f"  - {result.memory.entity_name}: {result.memory.description}")
        print(f"    Relevance: {result.relevance_score:.2f}")
    
    results = memory_store.search_memories("alice", limit=2)
    print(f"\nFound {len(results)} memories for 'alice':")
    for result in results:
        print(f"  - {result.memory.entity_name}: {result.memory.description}")
    
    # Get recent memories
    print("\nRecent memories:")
    recent = memory_store.get_recent_memories(days=1, limit=5)
    for memory in recent:
        print(f"  - {memory.entity_name} ({memory.entity_type}): {memory.description}")
    
    return memory_store


def example_conversation_manager():
    """Example of using ConversationManager."""
    print("\n=== ConversationManager Example ===")
    
    # Create mock Ollama client and memory store
    mock_ollama_client = type('MockOllamaClient', (), {
        'generate_response': lambda self, prompt, context: "This is a mock AI response about tarot."
    })()
    
    memory_store = MemoryStore("conversation_memories.db")
    conversation_manager = ConversationManager(mock_ollama_client, memory_store)
    
    # Create session
    session = conversation_manager.create_session("card_chat", "user123")
    print(f"Created session: {session.session_id}")
    print(f"Session type: {session.conversation_type}")
    print(f"User ID: {session.user_id}")
    
    # Add messages
    print("\nAdding messages...")
    
    user_message = conversation_manager.add_message(
        session.session_id, "user", "Tell me about The Fool card"
    )
    print(f"User message: {user_message.content}")
    
    assistant_message = conversation_manager.add_message(
        session.session_id, "assistant", "The Fool represents new beginnings and taking a leap of faith..."
    )
    print(f"Assistant message: {assistant_message.content}")
    
    # Get session history
    print("\nSession history:")
    history = conversation_manager.get_session_history(session.session_id)
    for message in history:
        print(f"  {message.role}: {message.content}")
    
    # Chat with a card (mock)
    print("\nChatting with a card...")
    card_data = {
        "name": "The Fool",
        "meaning": "New beginnings and taking a leap of faith",
        "keywords": ["new beginnings", "innocence", "free spirit"]
    }
    
    # This would be async in real usage
    # response = await conversation_manager.chat_with_card(
    #     session.session_id,
    #     card_data,
    #     "What does The Fool mean for my career change?"
    # )
    # print(f"Card chat response: {response.summary}")
    
    # End session
    result = conversation_manager.end_session(session.session_id)
    print(f"Session ended: {result}")
    
    return conversation_manager


def example_prompt_templates():
    """Example of using PromptTemplateManager."""
    print("\n=== PromptTemplateManager Example ===")
    
    template_manager = PromptTemplateManager()
    
    # Get available templates
    print("Available templates:")
    templates = template_manager.get_all_templates()
    for template in templates:
        print(f"  - {template.name}: {template.description}")
    
    # Get templates by category
    print("\nTemplates by category:")
    categories = template_manager.get_template_categories()
    for category in categories:
        category_templates = template_manager.get_templates_by_category(category)
        print(f"  {category}: {len(category_templates)} templates")
    
    # Render card interpretation template
    print("\nRendering card interpretation template...")
    variables = {
        "card_name": "The Fool",
        "arcana_type": "Major Arcana",
        "suit": "None",
        "number": "0",
        "element": "Air",
        "keywords": "new beginnings, innocence, free spirit",
        "upright_meaning": "The Fool represents new beginnings, innocence, and a free spirit. This card signifies taking a leap of faith and embracing the unknown.",
        "reversed_meaning": "Reversed, The Fool suggests recklessness, carelessness, or being held back by fear.",
        "orientation": "upright",
        "user_question": "What does The Fool mean for my career change?",
        "context": "User is considering leaving their current job to start a new business"
    }
    
    prompt = template_manager.render_template("card_interpretation", variables)
    print("Generated prompt:")
    print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
    
    # Render reading interpretation template
    print("\nRendering reading interpretation template...")
    reading_variables = {
        "spread_name": "Three Card",
        "user_question": "What does my future hold?",
        "reading_date": datetime.now().strftime("%Y-%m-%d"),
        "cards_info": template_manager.format_cards_info([
            {"position": "Past", "card_name": "The Fool", "orientation": "upright"},
            {"position": "Present", "card_name": "The Magician", "orientation": "upright"},
            {"position": "Future", "card_name": "The World", "orientation": "upright"}
        ]),
        "context": "User is at a crossroads in life"
    }
    
    reading_prompt = template_manager.render_template("reading_interpretation", reading_variables)
    print("Generated reading prompt:")
    print(reading_prompt[:200] + "..." if len(reading_prompt) > 200 else reading_prompt)
    
    # Create custom template
    print("\nCreating custom template...")
    custom_template = template_manager.create_custom_template(
        name="career_advice",
        description="Template for career advice based on tarot cards",
        template="""Based on the {card_name} card, here's my advice for your career:

The {card_name} represents {keywords}. In the context of your career change, this suggests:

{advice}

Consider these next steps:
1. {step1}
2. {step2}
3. {step3}

Remember: {encouragement}""",
        variables=["card_name", "keywords", "advice", "step1", "step2", "step3", "encouragement"],
        category="custom"
    )
    
    print(f"Created custom template: {custom_template.name}")
    
    # Render custom template
    custom_variables = {
        "card_name": "The Fool",
        "keywords": "new beginnings and taking risks",
        "advice": "This is the perfect time to take that leap of faith into your new career",
        "step1": "Research your new field thoroughly",
        "step2": "Start building connections in your target industry",
        "step3": "Create a transition plan with realistic timelines",
        "encouragement": "Trust your instincts and embrace the unknown - great things await!"
    }
    
    custom_prompt = template_manager.render_template("career_advice", custom_variables)
    print("Generated custom prompt:")
    print(custom_prompt)
    
    return template_manager


def example_ai_config():
    """Example of using AIConfigManager."""
    print("\n=== AIConfigManager Example ===")
    
    # Create config manager
    config_manager = AIConfigManager("example_ai_config.json")
    
    # Get current settings
    print("Current AI settings:")
    settings = config_manager.get_settings()
    print(f"  Default model: {settings.default_model}")
    print(f"  Temperature: {settings.temperature}")
    print(f"  Max tokens: {settings.max_tokens}")
    print(f"  Enable memory: {settings.enable_memory}")
    print(f"  Enable streaming: {settings.enable_streaming}")
    
    # Get available models
    print("\nAvailable models:")
    models = config_manager.get_models()
    for model in models:
        status = "✓" if model.enabled else "✗"
        recommended = "★" if model.recommended else " "
        print(f"  {status} {recommended} {model.display_name} ({model.name}) - {model.size}")
    
    # Get enabled models
    print("\nEnabled models:")
    enabled_models = config_manager.get_enabled_models()
    for model in enabled_models:
        print(f"  - {model.display_name} ({model.name})")
    
    # Get recommended models
    print("\nRecommended models:")
    recommended_models = config_manager.get_recommended_models()
    for model in recommended_models:
        print(f"  - {model.display_name} ({model.name})")
    
    # Update settings
    print("\nUpdating settings...")
    config_manager.update_settings(
        temperature=0.8,
        max_tokens=1024,
        enable_memory=True
    )
    
    updated_settings = config_manager.get_settings()
    print(f"Updated temperature: {updated_settings.temperature}")
    print(f"Updated max tokens: {updated_settings.max_tokens}")
    
    # Set default model
    print("\nSetting default model...")
    result = config_manager.set_default_model("mistral")
    print(f"Set default model result: {result}")
    print(f"New default model: {config_manager.get_default_model()}")
    
    # Enable/disable models
    print("\nManaging models...")
    config_manager.disable_model("codellama")
    config_manager.enable_model("phi3")
    
    # Validate configuration
    print("\nValidating configuration...")
    errors = config_manager.validate_config()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid!")
    
    # Get configuration summary
    print("\nConfiguration summary:")
    summary = config_manager.get_config_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Save configuration
    config_manager.save_config()
    print("\nConfiguration saved to file")
    
    return config_manager


def example_integration():
    """Example of integrating AI module components."""
    print("\n=== AI Module Integration Example ===")
    
    # Initialize all components
    config_manager = AIConfigManager()
    ollama_client = OllamaClient()
    memory_store = MemoryStore("integration_memories.db")
    conversation_manager = ConversationManager(ollama_client, memory_store)
    template_manager = PromptTemplateManager()
    
    print("Initialized all AI components")
    
    # Store some context in memory
    memory_id = memory_store.store_memory(
        entity_type="person",
        entity_name="Sarah",
        description="Sarah is interested in tarot and is considering a career change",
        context="Initial consultation",
        importance_score=0.8
    )
    print(f"Stored memory: {memory_id}")
    
    # Create conversation session
    session = conversation_manager.create_session("general_chat", "sarah123")
    print(f"Created session: {session.session_id}")
    
    # Add conversation context
    conversation_manager.add_message(
        session.session_id, "user", "Hi, I'm Sarah and I'm interested in tarot"
    )
    
    # Search for relevant memories
    memories = memory_store.search_memories("sarah", limit=1)
    if memories:
        context = f"Previous context: {memories[0].memory.description}"
        print(f"Found relevant context: {context}")
    
    # Generate prompt using template
    variables = {
        "user_message": "Can you help me understand what tarot can do for me?",
        "context": context if memories else "New user"
    }
    
    prompt = template_manager.render_template("general_tarot_chat", variables)
    print("Generated prompt:")
    print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
    
    # This would be async in real usage
    # response = await ollama_client.generate_response(prompt)
    # print(f"AI Response: {response}")
    
    # Add AI response to conversation
    conversation_manager.add_message(
        session.session_id, "assistant", "Tarot can help you gain insights into your life and make better decisions..."
    )
    
    # Get conversation history
    history = conversation_manager.get_session_history(session.session_id)
    print(f"\nConversation history ({len(history)} messages):")
    for message in history:
        print(f"  {message.role}: {message.content}")
    
    # End session
    conversation_manager.end_session(session.session_id)
    print("Session ended")
    
    # Clean up
    import os
    if os.path.exists("integration_memories.db"):
        os.unlink("integration_memories.db")
    if os.path.exists("example_ai_config.json"):
        os.unlink("example_ai_config.json")
    
    print("Integration example completed")


def main():
    """Run all AI module examples."""
    print("Tarot AI Module - Example Usage")
    print("=" * 50)
    
    try:
        # Run examples
        example_ollama_client()
        example_memory_store()
        example_conversation_manager()
        example_prompt_templates()
        example_ai_config()
        example_integration()
        
        print("\n" + "=" * 50)
        print("🎉 All AI module examples completed successfully!")
        print("The AI module is ready for integration with the tarot application.")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()