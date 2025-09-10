#!/usr/bin/env python3
"""
Script to fix Major Arcana cards by adding the 'arcana' field.
"""

import json

# Load the card data
with open('card_data.json', 'r') as f:
    data = json.load(f)

# Add 'arcana': 'major' to all Major Arcana cards
for card in data['major_arcana']:
    card['arcana'] = 'major'

# Save the fixed data
with open('card_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✅ Fixed Major Arcana cards by adding 'arcana' field")