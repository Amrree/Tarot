.PHONY: install dev-install test clean package app

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio black flake8 mypy py2app

# Run tests
test:
	pytest tests/ -v

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Package as macOS app
package: clean
	python setup.py py2app --packages=tarot_studio

# Create distributable app bundle
app: package
	codesign --force --deep --sign - dist/TarotStudio.app
	create-dmg dist/TarotStudio.app dist/

# Run in development mode
dev:
	python -m tarot_studio.app.main

# Format code
format:
	black tarot_studio/ tests/
	flake8 tarot_studio/ tests/

# Type checking
type-check:
	mypy tarot_studio/