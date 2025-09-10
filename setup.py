from setuptools import setup, find_packages

setup(
    name="tarot-studio",
    version="1.0.0",
    description="A native macOS Tarot reading application with AI integration",
    author="Tarot Studio Team",
    packages=find_packages(),
    install_requires=[
        "PyObjC>=9.0",
        "SQLAlchemy>=2.0.0",
        "ollama>=0.1.0",
        "cryptography>=41.0.0",
        "python-dateutil>=2.8.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "packaging": [
            "py2app>=0.28.0",
        ],
    },
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "tarot-studio=tarot_studio.app.main:main",
        ],
    },
)