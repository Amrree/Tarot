#!/usr/bin/env python3
"""
Demo script to run the Tarot Studio GUI.
"""

import sys
import os
import time
import threading
import webbrowser

# Add the parent directory to the path
sys.path.append('.')

def main():
    """Run the GUI demo."""
    print("🔮 Tarot Studio - GUI Demo")
    print("=" * 50)
    
    try:
        from tarot_studio.gui.simple_server import TarotServer
        
        # Create and start server
        server = TarotServer(host='127.0.0.1', port=8080)
        
        print("Starting Tarot Studio server...")
        print("Server will be available at: http://127.0.0.1:8080")
        print("\nFeatures available:")
        print("✅ Complete 78-card tarot deck")
        print("✅ Multiple spread layouts (Single Card, Three Card, Celtic Cross)")
        print("✅ Card drawing and deck management")
        print("✅ Reading persistence and history")
        print("✅ AI chat interface (simplified)")
        print("✅ Dark terminal-style aesthetics")
        print("✅ Responsive web interface")
        
        print("\nPress Ctrl+C to stop the server")
        print("Opening browser in 3 seconds...")
        
        # Open browser after a delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://127.0.0.1:8080')
                print("✅ Browser opened!")
            except Exception as e:
                print(f"⚠️  Could not open browser automatically: {e}")
                print("Please manually open: http://127.0.0.1:8080")
        
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Start server
        server.start()
        
    except KeyboardInterrupt:
        print("\n\n👋 Tarot Studio server stopped. Thank you for using Tarot Studio!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()