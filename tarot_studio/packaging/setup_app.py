"""
Setup script for creating macOS .app bundle using py2app.
"""

from setuptools import setup
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import the main module
from tarot_studio.app.main import TarotStudioApp

APP = ['tarot_studio/app/main.py']
DATA_FILES = [
    ('tarot_studio/db/schemas', ['tarot_studio/db/schemas/card_schema.json']),
    ('tarot_studio/db/migrations', ['tarot_studio/db/migrations/']),
    ('tarot_studio/docs', ['tarot_studio/docs/']),
]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'tarot_studio/packaging/icon.icns',  # You'll need to create this
    'plist': {
        'CFBundleName': 'Tarot Studio',
        'CFBundleDisplayName': 'Tarot Studio',
        'CFBundleIdentifier': 'com.tarotstudio.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundleExecutable': 'Tarot Studio',
        'CFBundleIconFile': 'icon.icns',
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,
        'NSAppearanceName': 'NSAppearanceNameDarkAqua',
        'LSMinimumSystemVersion': '10.15.0',
        'LSApplicationCategoryType': 'public.app-category.lifestyle',
        'NSHumanReadableCopyright': 'Copyright © 2024 Tarot Studio Team. All rights reserved.',
        'NSAppleScriptEnabled': False,
        'NSSupportsAutomaticGraphicsSwitching': True,
    },
    'packages': [
        'tarot_studio',
        'tarot_studio.app',
        'tarot_studio.app.ui',
        'tarot_studio.core',
        'tarot_studio.ai',
        'tarot_studio.ai.ollama',
        'tarot_studio.ai.memory',
        'tarot_studio.db',
        'tarot_studio.db.migrations',
        'tarot_studio.db.schemas',
    ],
    'includes': [
        'objc',
        'Foundation',
        'AppKit',
        'Cocoa',
        'sqlalchemy',
        'ollama',
        'cryptography',
        'python-dateutil',
        'pydantic',
    ],
    'excludes': [
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    'optimize': 2,
    'compressed': True,
    'strip': True,
    'semi_standalone': False,
    'site_packages': True,
    'use_pythonpath': True,
}

setup(
    name='Tarot Studio',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'PyObjC>=9.0',
        'SQLAlchemy>=2.0.0',
        'ollama>=0.1.0',
        'cryptography>=41.0.0',
        'python-dateutil>=2.8.0',
        'pydantic>=2.0.0',
    ],
)