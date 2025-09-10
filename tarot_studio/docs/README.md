# Tarot Studio

A native macOS Tarot reading application with AI integration, inspired by the sleek dark terminal-style aesthetics of "Zed."

## Features

- **Complete 78-card Rider-Waite deck** with upright and reversed meanings
- **Card influence engine** that computes how neighboring cards modify meanings
- **AI-powered interpretations** via local Ollama LLM
- **Native macOS interface** with dark theme and monospaced typography
- **Local-first data storage** with encryption for sensitive data
- **Conversational AI** that remembers past readings and contexts
- **Multiple spread layouts** including Single Card, Three Card, Celtic Cross, and more
- **Reading history and journal** with searchable past readings
- **Custom spread editor** for personalized layouts

## Requirements

- macOS 10.15 (Catalina) or later
- Python 3.10 or later
- Ollama (for AI features)

## Installation

### Option 1: Pre-built App (Recommended)

1. Download the latest release from the releases page
2. Open the DMG file and drag Tarot Studio to your Applications folder
3. Launch the app from Applications

### Option 2: Build from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tarot-studio.git
   cd tarot-studio
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the app:
   ```bash
   ./tarot_studio/packaging/build_app.sh
   ```

4. The app will be created in `tarot_studio/packaging/dist/Tarot Studio.app`

## Setup

### Installing Ollama

1. Download and install Ollama from [https://ollama.ai](https://ollama.ai)
2. Install a recommended model:
   ```bash
   ollama pull llama3.2
   ```
3. Start Ollama:
   ```bash
   ollama serve
   ```

### First Launch

1. Launch Tarot Studio
2. Go to Settings and test the Ollama connection
3. Select your preferred model
4. Start drawing cards!

## Usage

### Drawing Cards

1. Select a spread from the Readings tab
2. Click "Draw Cards" to get your reading
3. View the AI-generated interpretation
4. Save the reading to your history

### Chat with AI

1. Go to the Chat tab
2. Ask questions about your readings or tarot in general
3. Enable memory to let the AI remember your conversations
4. The AI can reference past readings and provide personalized insights

### Viewing History

1. Go to the History tab
2. Browse your past readings
3. Search for specific cards or topics
4. Click on a reading to view full details

## Architecture

### Core Components

- **Influence Engine**: Computes how cards influence each other in spreads
- **AI Integration**: Ollama client for generating interpretations
- **Memory System**: Semantic memory for AI context and recall
- **Database**: SQLite with SQLAlchemy for data persistence
- **UI Framework**: Native macOS interface using PyObjC

### Card Influence System

The influence engine uses a rule-based system to compute how neighboring cards modify meanings:

- **Major Arcana dominance**: Major cards have stronger influence (1.5x multiplier)
- **Suit interactions**: Different suits interact in specific ways
- **Numeric progressions**: Sequential numbers create continuity
- **Adjacency effects**: Cards influence their neighbors based on position
- **Reversal propagation**: Reversed cards affect nearby cards differently

### AI Integration

- **Structured responses**: AI returns JSON with specific fields for UI rendering
- **Context awareness**: AI can reference past readings and conversations
- **Memory system**: Semantic storage of entities, people, and concepts
- **Streaming responses**: Real-time UI updates as AI generates text

## Development

### Project Structure

```
tarot_studio/
├── app/                    # Main application
│   ├── ui/                # UI components
│   ├── core/              # Core business logic
│   └── models/            # Data models
├── ai/                    # AI integration
│   ├── ollama/            # Ollama client
│   └── memory/            # Memory system
├── db/                    # Database
│   ├── models.py          # SQLAlchemy models
│   ├── schemas/           # JSON schemas
│   └── migrations/        # Database migrations
├── tests/                 # Test suite
├── packaging/             # App packaging
└── docs/                  # Documentation
```

### Running Tests

```bash
pytest tests/ -v
```

### Development Mode

```bash
python -m tarot_studio.app.main
```

### Building for Distribution

```bash
./tarot_studio/packaging/build_app.sh
```

## Configuration

### Ollama Settings

- **Model**: Choose from available Ollama models (llama3.2 recommended)
- **URL**: Ollama server URL (default: http://localhost:11434)
- **Temperature**: Controls response creativity (0.7 recommended)

### Database Settings

- **Location**: SQLite database stored locally
- **Encryption**: Sensitive data encrypted with user passphrase
- **Backup**: Export/import functionality for data portability

### Appearance Settings

- **Theme**: Dark theme (matches macOS dark mode)
- **Font**: Monospaced font for terminal aesthetic
- **Font Size**: Adjustable text size

## Privacy & Security

- **Local-first**: All data stored locally by default
- **No telemetry**: No external analytics or tracking
- **Encryption**: Sensitive fields encrypted at rest
- **No cloud sync**: Data stays on your device unless explicitly exported

## Troubleshooting

### Common Issues

**Ollama connection failed**
- Ensure Ollama is running: `ollama serve`
- Check the URL in Settings (default: http://localhost:11434)
- Verify the model is installed: `ollama list`

**App won't launch**
- Check macOS version (10.15+ required)
- Try running from terminal to see error messages
- Reinstall the app if corrupted

**Cards not loading**
- Check database file permissions
- Try resetting the database in Settings
- Reinstall the app to restore default data

### Getting Help

- Check the [Issues](https://github.com/yourusername/tarot-studio/issues) page
- Create a new issue with detailed error information
- Include macOS version and error logs

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by the clean, terminal-style aesthetics of Zed editor
- Built with the Rider-Waite Tarot deck
- AI powered by Ollama and local LLMs
- Native macOS interface using PyObjC

## Roadmap

- [ ] Custom deck support
- [ ] Advanced spread editor
- [ ] Card image integration
- [ ] Export to PDF
- [ ] Voice input for questions
- [ ] Accessibility improvements
- [ ] Multi-language support