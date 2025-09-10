"""
AI Configuration Manager for Tarot Studio.

This module manages AI configuration, model selection, and settings
for the tarot application.
"""

import json
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field, asdict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for an AI model."""
    name: str
    display_name: str
    description: str
    size: str
    family: str
    recommended: bool = False
    enabled: bool = True
    custom_parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AISettings:
    """AI settings and preferences."""
    default_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    context_length: int = 4096
    enable_memory: bool = True
    memory_retention_days: int = 30
    enable_conversation_history: bool = True
    max_conversation_history: int = 50
    enable_streaming: bool = True
    response_timeout: int = 30
    retry_attempts: int = 3
    enable_fallback: bool = True
    fallback_model: str = "llama3.2"
    custom_prompts: Dict[str, str] = field(default_factory=dict)
    user_preferences: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AIConfig:
    """Complete AI configuration."""
    settings: AISettings
    models: List[ModelConfig]
    version: str = "1.0.0"
    last_updated: str = ""

class AIConfigManager:
    """Manages AI configuration and settings."""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        self.config_path = Path(config_path) if config_path else Path("ai_config.json")
        self.config: Optional[AIConfig] = None
        self._load_default_config()
        self._load_config()
    
    def _load_default_config(self):
        """Load default AI configuration."""
        default_models = [
            ModelConfig(
                name="llama3.2",
                display_name="Llama 3.2",
                description="Meta's Llama 3.2 model - good balance of performance and speed",
                size="3B",
                family="llama",
                recommended=True,
                enabled=True
            ),
            ModelConfig(
                name="llama3.2:8b",
                display_name="Llama 3.2 8B",
                description="Meta's Llama 3.2 8B model - higher quality responses",
                size="8B",
                family="llama",
                recommended=True,
                enabled=True
            ),
            ModelConfig(
                name="llama3.2:70b",
                display_name="Llama 3.2 70B",
                description="Meta's Llama 3.2 70B model - highest quality responses",
                size="70B",
                family="llama",
                recommended=False,
                enabled=True
            ),
            ModelConfig(
                name="mistral",
                display_name="Mistral",
                description="Mistral AI's model - fast and efficient",
                size="7B",
                family="mistral",
                recommended=True,
                enabled=True
            ),
            ModelConfig(
                name="codellama",
                display_name="Code Llama",
                description="Meta's Code Llama - good for technical discussions",
                size="7B",
                family="llama",
                recommended=False,
                enabled=False
            ),
            ModelConfig(
                name="phi3",
                display_name="Phi-3",
                description="Microsoft's Phi-3 model - compact and efficient",
                size="3.8B",
                family="phi",
                recommended=True,
                enabled=True
            )
        ]
        
        default_settings = AISettings()
        
        self.config = AIConfig(
            settings=default_settings,
            models=default_models,
            version="1.0.0",
            last_updated=""
        )
    
    def _load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # Load settings
                settings_data = config_data.get('settings', {})
                settings = AISettings(**settings_data)
                
                # Load models
                models_data = config_data.get('models', [])
                models = [ModelConfig(**model_data) for model_data in models_data]
                
                self.config = AIConfig(
                    settings=settings,
                    models=models,
                    version=config_data.get('version', '1.0.0'),
                    last_updated=config_data.get('last_updated', '')
                )
                
                logger.info(f"Loaded AI configuration from {self.config_path}")
                
            except Exception as e:
                logger.error(f"Failed to load AI configuration: {e}")
                logger.info("Using default configuration")
        else:
            logger.info("No AI configuration file found, using defaults")
    
    def save_config(self):
        """Save configuration to file."""
        try:
            config_dict = asdict(self.config)
            config_dict['last_updated'] = str(datetime.now())
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2)
            
            logger.info(f"Saved AI configuration to {self.config_path}")
            
        except Exception as e:
            logger.error(f"Failed to save AI configuration: {e}")
    
    def get_settings(self) -> AISettings:
        """Get current AI settings."""
        return self.config.settings
    
    def update_settings(self, **kwargs):
        """Update AI settings."""
        for key, value in kwargs.items():
            if hasattr(self.config.settings, key):
                setattr(self.config.settings, key, value)
                logger.info(f"Updated setting {key} to {value}")
            else:
                logger.warning(f"Unknown setting: {key}")
    
    def get_models(self) -> List[ModelConfig]:
        """Get all available models."""
        return self.config.models.copy()
    
    def get_enabled_models(self) -> List[ModelConfig]:
        """Get only enabled models."""
        return [model for model in self.config.models if model.enabled]
    
    def get_recommended_models(self) -> List[ModelConfig]:
        """Get recommended models."""
        return [model for model in self.config.models if model.recommended and model.enabled]
    
    def get_model(self, name: str) -> Optional[ModelConfig]:
        """Get a specific model by name."""
        for model in self.config.models:
            if model.name == name:
                return model
        return None
    
    def enable_model(self, name: str) -> bool:
        """Enable a model."""
        model = self.get_model(name)
        if model:
            model.enabled = True
            logger.info(f"Enabled model {name}")
            return True
        return False
    
    def disable_model(self, name: str) -> bool:
        """Disable a model."""
        model = self.get_model(name)
        if model:
            model.enabled = False
            logger.info(f"Disabled model {name}")
            return True
        return False
    
    def add_model(self, model: ModelConfig):
        """Add a new model configuration."""
        # Check if model already exists
        existing_model = self.get_model(model.name)
        if existing_model:
            logger.warning(f"Model {model.name} already exists")
            return False
        
        self.config.models.append(model)
        logger.info(f"Added model {model.name}")
        return True
    
    def remove_model(self, name: str) -> bool:
        """Remove a model configuration."""
        for i, model in enumerate(self.config.models):
            if model.name == name:
                del self.config.models[i]
                logger.info(f"Removed model {name}")
                return True
        return False
    
    def set_default_model(self, name: str) -> bool:
        """Set the default model."""
        model = self.get_model(name)
        if model and model.enabled:
            self.config.settings.default_model = name
            logger.info(f"Set default model to {name}")
            return True
        return False
    
    def get_default_model(self) -> str:
        """Get the default model name."""
        return self.config.settings.default_model
    
    def validate_config(self) -> List[str]:
        """Validate the current configuration."""
        errors = []
        
        # Check if default model exists and is enabled
        default_model = self.get_model(self.config.settings.default_model)
        if not default_model:
            errors.append(f"Default model '{self.config.settings.default_model}' not found")
        elif not default_model.enabled:
            errors.append(f"Default model '{self.config.settings.default_model}' is disabled")
        
        # Check if fallback model exists and is enabled
        fallback_model = self.get_model(self.config.settings.fallback_model)
        if not fallback_model:
            errors.append(f"Fallback model '{self.config.settings.fallback_model}' not found")
        elif not fallback_model.enabled:
            errors.append(f"Fallback model '{self.config.settings.fallback_model}' is disabled")
        
        # Validate settings ranges
        if not 0.0 <= self.config.settings.temperature <= 2.0:
            errors.append("Temperature must be between 0.0 and 2.0")
        
        if not 0.0 <= self.config.settings.top_p <= 1.0:
            errors.append("Top-p must be between 0.0 and 1.0")
        
        if self.config.settings.max_tokens <= 0:
            errors.append("Max tokens must be greater than 0")
        
        if self.config.settings.context_length <= 0:
            errors.append("Context length must be greater than 0")
        
        return errors
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self._load_default_config()
        logger.info("Reset AI configuration to defaults")
    
    def export_config(self, export_path: Union[str, Path]) -> bool:
        """Export configuration to a file."""
        try:
            export_path = Path(export_path)
            config_dict = asdict(self.config)
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2)
            
            logger.info(f"Exported AI configuration to {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export AI configuration: {e}")
            return False
    
    def import_config(self, import_path: Union[str, Path]) -> bool:
        """Import configuration from a file."""
        try:
            import_path = Path(import_path)
            
            if not import_path.exists():
                logger.error(f"Import file {import_path} does not exist")
                return False
            
            with open(import_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate imported configuration
            if 'settings' not in config_data or 'models' not in config_data:
                logger.error("Invalid configuration file format")
                return False
            
            # Load imported configuration
            settings_data = config_data.get('settings', {})
            settings = AISettings(**settings_data)
            
            models_data = config_data.get('models', [])
            models = [ModelConfig(**model_data) for model_data in models_data]
            
            self.config = AIConfig(
                settings=settings,
                models=models,
                version=config_data.get('version', '1.0.0'),
                last_updated=config_data.get('last_updated', '')
            )
            
            logger.info(f"Imported AI configuration from {import_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import AI configuration: {e}")
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the current configuration."""
        return {
            'version': self.config.version,
            'last_updated': self.config.last_updated,
            'default_model': self.config.settings.default_model,
            'fallback_model': self.config.settings.fallback_model,
            'total_models': len(self.config.models),
            'enabled_models': len(self.get_enabled_models()),
            'recommended_models': len(self.get_recommended_models()),
            'memory_enabled': self.config.settings.enable_memory,
            'streaming_enabled': self.config.settings.enable_streaming,
            'validation_errors': self.validate_config()
        }


# Import datetime for last_updated
from datetime import datetime


# Example usage and testing
if __name__ == "__main__":
    # Create config manager
    config_manager = AIConfigManager("test_ai_config.json")
    
    # Test getting settings
    settings = config_manager.get_settings()
    print(f"Default model: {settings.default_model}")
    print(f"Temperature: {settings.temperature}")
    print(f"Max tokens: {settings.max_tokens}")
    
    # Test getting models
    models = config_manager.get_models()
    print(f"\nTotal models: {len(models)}")
    
    enabled_models = config_manager.get_enabled_models()
    print(f"Enabled models: {len(enabled_models)}")
    
    recommended_models = config_manager.get_recommended_models()
    print(f"Recommended models: {len(recommended_models)}")
    
    for model in recommended_models:
        print(f"  - {model.display_name} ({model.name})")
    
    # Test model operations
    llama_model = config_manager.get_model("llama3.2")
    if llama_model:
        print(f"\nLlama 3.2 model: {llama_model.display_name}")
        print(f"Enabled: {llama_model.enabled}")
        print(f"Recommended: {llama_model.recommended}")
    
    # Test configuration validation
    errors = config_manager.validate_config()
    if errors:
        print(f"\nConfiguration errors: {errors}")
    else:
        print("\nConfiguration is valid")
    
    # Test configuration summary
    summary = config_manager.get_config_summary()
    print(f"\nConfiguration summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Test updating settings
    config_manager.update_settings(temperature=0.8, max_tokens=1024)
    print(f"\nUpdated temperature to: {config_manager.get_settings().temperature}")
    print(f"Updated max tokens to: {config_manager.get_settings().max_tokens}")
    
    # Save configuration
    config_manager.save_config()
    print("\nConfiguration saved")
    
    # Clean up test file
    import os
    if os.path.exists("test_ai_config.json"):
        os.remove("test_ai_config.json")
        print("Test configuration file cleaned up")