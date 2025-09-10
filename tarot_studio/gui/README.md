# GUI Module - Tarot Studio

## Overview

The GUI Module provides a web-based user interface for the Tarot Studio application. It serves as a fallback implementation for environments where PyObjC (macOS native GUI) is not available, while maintaining the dark terminal-style aesthetics specified in the original design.

## Features

### Core Functionality
- **Web-Based Interface**: Runs in any modern web browser
- **Dark Terminal Aesthetics**: GitHub Dark theme with monospace fonts
- **Responsive Design**: Works on desktop and mobile devices
- **Real-Time Updates**: Dynamic content updates without page refresh
- **Local Server**: Runs entirely locally, no external dependencies

### User Interface Components
- **Sidebar Navigation**: Clean navigation between different views
- **Readings View**: Card drawing, spread selection, and reading creation
- **Chat View**: AI-powered conversation interface
- **History View**: Reading history and search functionality
- **Settings View**: Application configuration and preferences

### Technical Features
- **RESTful API**: Clean API endpoints for all operations
- **JSON Data Exchange**: Efficient data serialization
- **Error Handling**: Graceful error handling and user feedback
- **Status Messages**: Real-time status updates and notifications
- **Loading States**: Visual feedback for async operations

## Architecture

### Server Implementation
- **Simple HTTP Server**: Built-in Python HTTP server (no external dependencies)
- **Request Handler**: Custom handler for API endpoints and static content
- **Component Integration**: Seamless integration with all core modules
- **Session Management**: Basic session handling for user state

### Client Implementation
- **Vanilla JavaScript**: No external JavaScript frameworks
- **CSS3 Animations**: Smooth transitions and hover effects
- **Responsive Grid**: CSS Grid and Flexbox for layouts
- **Progressive Enhancement**: Works without JavaScript for basic functionality

## File Structure

```
gui/
├── simple_server.py      # Main HTTP server implementation
├── web_app.py           # Flask-based alternative (requires Flask)
├── templates/           # HTML templates
│   └── index.html       # Main application template
├── static/              # Static assets
│   └── style.css        # Additional CSS styles
└── README.md            # This documentation
```

## API Endpoints

### Cards API
- `GET /api/cards` - Get all tarot cards
- `GET /api/cards/<card_id>` - Get specific card details

### Spreads API
- `GET /api/spreads` - Get all available spreads
- `GET /api/spreads/<spread_id>` - Get specific spread details

### Readings API
- `GET /api/readings` - Get all readings
- `POST /api/readings` - Create new reading
- `GET /api/readings/<reading_id>` - Get specific reading

### Deck Operations
- `POST /api/draw-cards` - Draw cards from deck
- `POST /api/reset-deck` - Reset deck to full state

### AI Chat API
- `POST /api/chat` - Send message to AI assistant

### Memory API
- `GET /api/memories` - Get memories (with optional search)

### Settings API
- `GET /api/settings` - Get application settings
- `POST /api/settings` - Update application settings

## Usage

### Running the Server

```bash
# Simple server (no dependencies)
python3 tarot_studio/gui/simple_server.py

# Or use the demo script
python3 run_gui_demo.py
```

### Accessing the Interface

1. Start the server (default: http://127.0.0.1:8080)
2. Open your web browser
3. Navigate to the server URL
4. The interface will load automatically

### Basic Workflow

1. **Select a Spread**: Choose from available spreads (Single Card, Three Card, Celtic Cross)
2. **Ask a Question**: Optionally enter a question for your reading
3. **Draw Cards**: Click "Draw Cards" to draw the required number of cards
4. **Interpret**: View the cards in their spread positions
5. **Save Reading**: Save the reading to your history
6. **Chat**: Use the chat interface to discuss the reading with AI

## Customization

### Themes
The interface uses CSS custom properties for easy theming:

```css
:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --text-primary: #c9d1d9;
    --text-secondary: #7d8590;
    --accent-color: #58a6ff;
    --border-color: #30363d;
}
```

### Adding New Views
1. Add HTML structure to `index.html`
2. Add CSS styles for the new view
3. Add JavaScript functionality
4. Update navigation in the sidebar

### Extending API
1. Add new endpoint methods to `TarotRequestHandler`
2. Update client-side JavaScript to call new endpoints
3. Add error handling and user feedback

## Browser Compatibility

### Supported Browsers
- **Chrome/Chromium**: 80+
- **Firefox**: 75+
- **Safari**: 13+
- **Edge**: 80+

### Required Features
- ES6 JavaScript support
- CSS Grid and Flexbox
- Fetch API
- CSS Custom Properties

## Performance Considerations

### Optimization Strategies
- **Lazy Loading**: Components loaded on demand
- **Efficient Rendering**: Minimal DOM manipulation
- **Caching**: Browser caching for static assets
- **Compression**: Gzip compression for responses

### Memory Usage
- **Client**: ~5-10MB typical usage
- **Server**: ~50-100MB with all components loaded
- **Database**: Depends on stored readings and memories

## Security Considerations

### Local-First Design
- **No External Requests**: All data stays local
- **No User Authentication**: Single-user application
- **No Sensitive Data**: No personal information stored
- **CORS Headers**: Basic CORS support for development

### Data Privacy
- **Local Storage**: All data stored locally
- **No Tracking**: No analytics or tracking
- **No Cloud Sync**: No data sent to external services

## Troubleshooting

### Common Issues

#### Server Won't Start
- **Port in Use**: Try a different port (8081, 8082, etc.)
- **Permission Denied**: Run with appropriate permissions
- **Firewall**: Check local firewall settings

#### Cards Not Loading
- **Database Error**: Check database initialization
- **File Permissions**: Ensure read access to card data
- **Path Issues**: Verify file paths are correct

#### AI Chat Not Working
- **Ollama Not Running**: Start Ollama service locally
- **Model Not Available**: Install required AI models
- **Network Issues**: Check local network connectivity

### Debug Mode
Enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Adding New Features
1. **Backend**: Add API endpoints in `simple_server.py`
2. **Frontend**: Add UI components in `index.html`
3. **Styling**: Add CSS in the `<style>` section
4. **JavaScript**: Add functionality in the `<script>` section
5. **Testing**: Update test files as needed

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use modern ES6+ syntax
- **CSS**: Use semantic class names
- **HTML**: Use semantic HTML5 elements

## Future Enhancements

### Planned Features
- **Card Images**: Visual card representations
- **Advanced Spreads**: Custom spread creation
- **Export Functionality**: PDF/JSON export of readings
- **Offline Mode**: Service worker for offline usage
- **Mobile App**: Progressive Web App (PWA) support

### Technical Improvements
- **WebSocket Support**: Real-time updates
- **Caching Layer**: Redis for session management
- **API Versioning**: Versioned API endpoints
- **Rate Limiting**: API rate limiting
- **Monitoring**: Health checks and metrics

## Contributing

When contributing to the GUI Module:

1. **Maintain Compatibility**: Ensure cross-browser compatibility
2. **Follow Design**: Maintain dark terminal aesthetics
3. **Test Thoroughly**: Test on multiple browsers and devices
4. **Document Changes**: Update documentation for new features
5. **Performance**: Consider performance impact of changes

## License

This module is part of the Tarot Studio project and follows the same license terms.