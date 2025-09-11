# Tarot Studio Android App

## Overview

Tarot Studio Android is a mobile version of the Tarot Studio application, built using Kivy and KivyMD for native Android performance. It preserves all the functionality of the original desktop/web application while providing an optimized mobile experience.

## Features

### Core Functionality
- **Complete Tarot Deck**: Full 78-card Rider-Waite deck with Major and Minor Arcana
- **Multiple Spreads**: Single Card, Three Card, and Celtic Cross spreads
- **AI Integration**: Local Ollama LLM integration for tarot interpretations
- **Reading History**: Persistent storage and search of past readings
- **Dark Theme**: Mobile-optimized dark terminal aesthetics
- **Offline Operation**: Fully functional without internet connection

### Mobile-Specific Features
- **Touch-Optimized UI**: Large buttons and touch-friendly interfaces
- **Responsive Design**: Adapts to different screen sizes and orientations
- **Native Performance**: Compiled to native Android APK
- **Material Design**: Modern Android UI components
- **Gesture Support**: Swipe navigation and touch interactions
- **Notification Support**: Reading reminders and updates

## Architecture

### Technology Stack
- **Kivy**: Cross-platform Python framework for mobile apps
- **KivyMD**: Material Design components for Kivy
- **Python 3.10+**: Core application logic
- **Buildozer**: Android build and packaging tool
- **Tarot Studio Core**: Reused modules from the main application

### Project Structure
```
android_tarot_studio/
├── main.py                    # Main application entry point
├── android_screens/           # Screen implementations
│   ├── __init__.py
│   ├── splash_screen.py       # Loading screen
│   ├── readings_screen.py     # Main readings interface
│   ├── chat_screen.py         # AI chat interface
│   ├── history_screen.py      # Reading history
│   └── settings_screen.py     # App settings
├── buildozer.spec            # Android build configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This documentation
```

## Installation and Setup

### Prerequisites
- Python 3.10 or higher
- Android SDK and NDK
- Buildozer
- Kivy and KivyMD

### Development Setup

1. **Install Dependencies**:
   ```bash
   pip install kivy kivymd buildozer
   ```

2. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd android_tarot_studio
   ```

3. **Test the Application**:
   ```bash
   python test_android_app.py
   ```

4. **Run in Desktop Mode** (for testing):
   ```bash
   python main.py
   ```

### Android Build Setup

1. **Install Buildozer**:
   ```bash
   pip install buildozer
   ```

2. **Initialize Buildozer** (if needed):
   ```bash
   buildozer init
   ```

3. **Build APK**:
   ```bash
   buildozer android debug
   ```

4. **Build Release APK**:
   ```bash
   buildozer android release
   ```

## Usage

### Running the App

1. **Desktop Testing**:
   ```bash
   python main.py
   ```

2. **Android Installation**:
   - Build APK using Buildozer
   - Install on Android device
   - Launch from app drawer

### App Navigation

- **Splash Screen**: Loading screen with app initialization
- **Readings Screen**: Main interface for drawing cards and creating spreads
- **Chat Screen**: AI-powered conversation about tarot readings
- **History Screen**: View and search past readings
- **Settings Screen**: Configure app preferences and AI settings

### Creating a Reading

1. **Select Spread**: Choose from Single Card, Three Card, or Celtic Cross
2. **Ask Question**: Optionally enter a question for your reading
3. **Draw Cards**: Tap "Draw Cards" to draw the required number of cards
4. **View Results**: Cards are displayed with names and keywords
5. **Save Reading**: Save the reading to your history

### Using AI Chat

1. **Navigate to Chat**: Tap the chat icon in bottom navigation
2. **Ask Questions**: Type questions about tarot, cards, or interpretations
3. **Get Responses**: Receive AI-generated responses about tarot
4. **Clear History**: Tap trash icon to clear chat history

## Configuration

### Buildozer Configuration

The `buildozer.spec` file contains all Android build settings:

- **App Information**: Name, package, version
- **Requirements**: Python packages and dependencies
- **Permissions**: Android permissions required
- **Architecture**: Target Android architectures
- **Signing**: Release signing configuration

### App Settings

Configure the app through the Settings screen:

- **AI Model**: Select Ollama model (llama3.2, llama2, mistral, etc.)
- **Auto-save**: Automatically save readings
- **Notifications**: Enable reading reminders
- **Data Management**: Clear data or export readings

## Development

### Adding New Screens

1. **Create Screen Class**:
   ```python
   from kivy.uix.screen import Screen
   
   class NewScreen(Screen):
       def __init__(self, **kwargs):
           super().__init__(**kwargs)
           self._build_ui()
       
       def _build_ui(self):
           # Build UI components
           pass
   ```

2. **Add to Main App**:
   ```python
   # In main.py
   self.screen_manager.add_widget(NewScreen(name='new_screen'))
   ```

3. **Add Navigation**:
   ```python
   # Add navigation button in other screens
   btn = Button(text='New Screen')
   btn.bind(on_press=lambda x: self._navigate_to_screen('new_screen'))
   ```

### Customizing UI

The app uses KivyMD Material Design components:

- **Colors**: Dark theme with blue accents
- **Typography**: Clear, readable fonts
- **Layouts**: Responsive BoxLayout and GridLayout
- **Components**: Buttons, labels, inputs, switches

### Testing

Run the test suite to verify functionality:

```bash
python test_android_app.py
```

Tests cover:
- Kivy imports and setup
- Tarot Studio module integration
- App initialization and components
- Screen creation and navigation
- Core functionality (deck, spreads, AI, database)

## Deployment

### Google Play Store

1. **Build Release APK**:
   ```bash
   buildozer android release
   ```

2. **Sign APK** (if not auto-signed):
   ```bash
   jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore app-release-unsigned.apk alias_name
   ```

3. **Upload to Play Console**:
   - Create developer account
   - Upload APK/AAB
   - Fill store listing
   - Submit for review

### Direct Distribution

1. **Build Debug APK**:
   ```bash
   buildozer android debug
   ```

2. **Distribute APK**:
   - Share APK file directly
   - Users enable "Unknown Sources"
   - Install APK manually

## Troubleshooting

### Common Issues

#### Build Failures
- **NDK Issues**: Ensure Android NDK is properly installed
- **SDK Issues**: Check Android SDK path and API levels
- **Dependencies**: Verify all requirements are installed

#### Runtime Issues
- **Import Errors**: Check Python path and module imports
- **Permission Errors**: Verify Android permissions in buildozer.spec
- **Performance Issues**: Optimize UI updates and memory usage

#### Testing Issues
- **Desktop Mode**: Test on desktop before building for Android
- **Device Testing**: Test on actual Android devices
- **Screen Sizes**: Test on different screen sizes and densities

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

- **Lazy Loading**: Load screens only when needed
- **Memory Management**: Properly dispose of unused widgets
- **Image Optimization**: Use appropriate image sizes
- **Code Optimization**: Profile and optimize slow operations

## Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 Python guidelines
2. **Documentation**: Document all public methods and classes
3. **Testing**: Add tests for new functionality
4. **UI/UX**: Follow Material Design guidelines
5. **Performance**: Optimize for mobile performance

### Pull Request Process

1. **Fork Repository**: Create your own fork
2. **Create Branch**: Use descriptive branch names
3. **Make Changes**: Implement features or fixes
4. **Test Thoroughly**: Run all tests and manual testing
5. **Submit PR**: Create pull request with description

## License

This Android app is part of the Tarot Studio project and follows the same license terms.

## Support

For issues and questions:

1. **Check Documentation**: Review this README and code comments
2. **Run Tests**: Use test suite to identify issues
3. **Check Logs**: Enable debug logging for detailed information
4. **Create Issue**: Submit detailed bug reports or feature requests

## Future Enhancements

### Planned Features
- **Card Images**: Visual card representations
- **Custom Spreads**: User-defined spread layouts
- **Export Functionality**: Share readings as images or text
- **Offline AI**: Local AI models for complete offline operation
- **Widgets**: Home screen widgets for quick access
- **Voice Input**: Speech-to-text for questions
- **Accessibility**: Screen reader and accessibility support

### Technical Improvements
- **Performance**: Further optimization for low-end devices
- **Battery**: Optimize battery usage
- **Storage**: Efficient data storage and compression
- **Security**: Enhanced data encryption and security
- **Analytics**: Usage analytics (privacy-focused)
- **Updates**: Over-the-air update system