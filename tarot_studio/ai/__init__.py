"""
Tarot AI Module

This module provides comprehensive AI functionality for the Tarot Studio application,
including Ollama integration, memory management, conversation handling, and prompt templates.
"""

from .ollama_client import OllamaClient, AIResponse, ConversationContext, ModelInfo, AIError
from .memory import MemoryStore, MemoryEntry, MemorySearchResult
from .conversation_manager import ConversationManager, ConversationMessage, ConversationSession
from .prompt_templates import PromptTemplateManager, PromptTemplate
from .ai_config import AIConfigManager, AISettings, ModelConfig, AIConfig

__all__ = [
    'OllamaClient',
    'AIResponse',
    'ConversationContext',
    'ModelInfo',
    'AIError',
    'MemoryStore',
    'MemoryEntry',
    'MemorySearchResult',
    'ConversationManager',
    'ConversationMessage',
    'ConversationSession',
    'PromptTemplateManager',
    'PromptTemplate',
    'AIConfigManager',
    'AISettings',
    'ModelConfig',
    'AIConfig'
]

__version__ = '1.0.0'
__author__ = 'Tarot Studio Team'
__description__ = 'Comprehensive AI functionality for tarot applications'