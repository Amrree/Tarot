"""
Main entry point for Tarot Studio application.
"""

import sys
import os
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tarot_studio.app.ui.main_window import MainWindow
from tarot_studio.db.models import create_database, load_cards_from_json, create_default_spreads
from tarot_studio.ai.ollama_client import OllamaClient
from tarot_studio.ai.memory import MemoryStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TarotStudioApp:
    """Main application class."""
    
    def __init__(self):
        self.db_path = "tarot_studio.db"
        self.engine = None
        self.session = None
        self.ollama_client = None
        self.memory_store = None
        self.main_window = None
        
    def initialize(self):
        """Initialize the application."""
        logger.info("Initializing Tarot Studio...")
        
        try:
            # Initialize database
            self.engine = create_database(self.db_path)
            from tarot_studio.db.models import get_session
            self.session = get_session(self.engine)
            
            # Load cards if database is empty
            self._ensure_cards_loaded()
            
            # Initialize AI client
            self.ollama_client = OllamaClient()
            
            # Initialize memory store
            self.memory_store = MemoryStore(self.db_path)
            
            logger.info("Application initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            return False
    
    def _ensure_cards_loaded(self):
        """Ensure cards are loaded into the database."""
        from tarot_studio.db.models import Card
        
        # Check if cards are already loaded
        card_count = self.session.query(Card).count()
        if card_count == 0:
            logger.info("Loading cards from JSON...")
            json_path = Path(__file__).parent.parent / "db" / "schemas" / "card_schema.json"
            if json_path.exists():
                load_cards_from_json(str(json_path), self.session)
                create_default_spreads(self.session)
            else:
                logger.error(f"Card schema file not found: {json_path}")
        else:
            logger.info(f"Database already contains {card_count} cards")
    
    def run(self):
        """Run the application."""
        if not self.initialize():
            logger.error("Failed to initialize application")
            return False
        
        try:
            # Create and show main window
            self.main_window = MainWindow(
                session=self.session,
                ollama_client=self.ollama_client,
                memory_store=self.memory_store
            )
            
            self.main_window.show()
            
            logger.info("Application started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            return False

def main():
    """Main entry point."""
    app = TarotStudioApp()
    success = app.run()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()