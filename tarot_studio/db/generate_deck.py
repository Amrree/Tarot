#!/usr/bin/env python3
"""
Generate complete 78-card Rider-Waite Tarot deck JSON file.
This script creates the full deck with all Major and Minor Arcana cards.
"""

import json
from typing import Dict, List, Any

def create_minor_arcana_suit(suit: str, suit_element: str, suit_keywords: List[str]) -> List[Dict[str, Any]]:
    """Create all 14 cards for a Minor Arcana suit."""
    cards = []
    
    # Define card meanings and properties for each suit
    suit_meanings = {
        "wands": {
            "theme": "creativity, passion, action, inspiration",
            "polarity_base": 0.4,
            "intensity_base": 0.8,
            "ace": {"keywords": ["inspiration", "new beginnings", "creativity", "passion"], "polarity": 0.8},
            "two": {"keywords": ["planning", "future", "personal power", "ambition"], "polarity": 0.6},
            "three": {"keywords": ["expansion", "foresight", "leadership", "progress"], "polarity": 0.7},
            "four": {"keywords": ["celebration", "harmony", "home", "community"], "polarity": 0.8},
            "five": {"keywords": ["conflict", "competition", "disagreement", "challenge"], "polarity": -0.3},
            "six": {"keywords": ["victory", "success", "recognition", "leadership"], "polarity": 0.9},
            "seven": {"keywords": ["challenge", "competition", "defending", "perseverance"], "polarity": 0.2},
            "eight": {"keywords": ["speed", "action", "rapid change", "progress"], "polarity": 0.5},
            "nine": {"keywords": ["resilience", "perseverance", "defense", "strength"], "polarity": 0.3},
            "ten": {"keywords": ["burden", "responsibility", "overload", "hard work"], "polarity": -0.4},
            "page": {"keywords": ["enthusiasm", "inspiration", "new ideas", "energy"], "polarity": 0.6},
            "knight": {"keywords": ["adventure", "passion", "impulsiveness", "energy"], "polarity": 0.4},
            "queen": {"keywords": ["confidence", "leadership", "independence", "creativity"], "polarity": 0.8},
            "king": {"keywords": ["leadership", "vision", "charisma", "inspiration"], "polarity": 0.7}
        },
        "cups": {
            "theme": "emotions, relationships, intuition",
            "polarity_base": 0.3,
            "intensity_base": 0.6,
            "ace": {"keywords": ["new love", "emotional beginnings", "intuition", "spirituality"], "polarity": 0.7},
            "two": {"keywords": ["partnership", "balance", "harmony", "choices"], "polarity": 0.6},
            "three": {"keywords": ["celebration", "friendship", "community", "joy"], "polarity": 0.8},
            "four": {"keywords": ["apathy", "disconnection", "boredom", "stagnation"], "polarity": -0.4},
            "five": {"keywords": ["loss", "grief", "disappointment", "regret"], "polarity": -0.6},
            "six": {"keywords": ["nostalgia", "memories", "childhood", "innocence"], "polarity": 0.4},
            "seven": {"keywords": ["choices", "illusion", "fantasy", "wishful thinking"], "polarity": -0.2},
            "eight": {"keywords": ["abandonment", "withdrawal", "disappointment", "escape"], "polarity": -0.5},
            "nine": {"keywords": ["satisfaction", "contentment", "gratitude", "fulfillment"], "polarity": 0.9},
            "ten": {"keywords": ["happiness", "fulfillment", "joy", "family"], "polarity": 0.8},
            "page": {"keywords": ["emotional messages", "intuition", "creativity", "sensitivity"], "polarity": 0.5},
            "knight": {"keywords": ["romance", "charm", "idealism", "pursuit"], "polarity": 0.6},
            "queen": {"keywords": ["compassion", "intuition", "emotional intelligence", "nurturing"], "polarity": 0.8},
            "king": {"keywords": ["emotional balance", "wisdom", "diplomacy", "control"], "polarity": 0.7}
        },
        "swords": {
            "theme": "thoughts, communication, conflict",
            "polarity_base": -0.1,
            "intensity_base": 0.8,
            "ace": {"keywords": ["new ideas", "mental clarity", "breakthrough", "truth"], "polarity": 0.5},
            "two": {"keywords": ["difficult choices", "indecision", "balance", "conflict"], "polarity": -0.3},
            "three": {"keywords": ["heartbreak", "sorrow", "betrayal", "pain"], "polarity": -0.7},
            "four": {"keywords": ["rest", "contemplation", "recovery", "peace"], "polarity": 0.2},
            "five": {"keywords": ["conflict", "defeat", "betrayal", "loss"], "polarity": -0.6},
            "six": {"keywords": ["transition", "change", "moving on", "release"], "polarity": 0.1},
            "seven": {"keywords": ["deception", "betrayal", "theft", "dishonesty"], "polarity": -0.8},
            "eight": {"keywords": ["restriction", "imprisonment", "self-imposed limits", "trapped"], "polarity": -0.7},
            "nine": {"keywords": ["anxiety", "worry", "fear", "nightmares"], "polarity": -0.9},
            "ten": {"keywords": ["rock bottom", "failure", "betrayal", "endings"], "polarity": -1.0},
            "page": {"keywords": ["new ideas", "curiosity", "learning", "communication"], "polarity": 0.3},
            "knight": {"keywords": ["action", "impulsiveness", "conflict", "aggression"], "polarity": -0.2},
            "queen": {"keywords": ["independence", "clarity", "directness", "truth"], "polarity": 0.4},
            "king": {"keywords": ["authority", "mental clarity", "truth", "leadership"], "polarity": 0.6}
        },
        "pentacles": {
            "theme": "material world, work, money, health",
            "polarity_base": 0.2,
            "intensity_base": 0.7,
            "ace": {"keywords": ["new opportunities", "manifestation", "abundance", "potential"], "polarity": 0.8},
            "two": {"keywords": ["balance", "priorities", "time management", "choices"], "polarity": 0.3},
            "three": {"keywords": ["teamwork", "collaboration", "learning", "skill building"], "polarity": 0.6},
            "four": {"keywords": ["stability", "security", "conservation", "foundation"], "polarity": 0.7},
            "five": {"keywords": ["financial loss", "poverty", "instability", "crisis"], "polarity": -0.6},
            "six": {"keywords": ["generosity", "charity", "giving", "sharing"], "polarity": 0.8},
            "seven": {"keywords": ["hard work", "perseverance", "long-term goals", "patience"], "polarity": 0.5},
            "eight": {"keywords": ["skill development", "quality", "mastery", "dedication"], "polarity": 0.7},
            "nine": {"keywords": ["abundance", "luxury", "self-sufficiency", "comfort"], "polarity": 0.9},
            "ten": {"keywords": ["wealth", "legacy", "family", "prosperity"], "polarity": 0.8},
            "page": {"keywords": ["new opportunities", "learning", "practical skills", "ambition"], "polarity": 0.6},
            "knight": {"keywords": ["hard work", "reliability", "practicality", "perseverance"], "polarity": 0.5},
            "queen": {"keywords": ["practicality", "nurturing", "abundance", "down-to-earth"], "polarity": 0.8},
            "king": {"keywords": ["financial security", "practicality", "reliability", "success"], "polarity": 0.7}
        }
    }
    
    suit_data = suit_meanings[suit]
    
    # Create numbered cards (1-10)
    number_names = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    for i in range(1, 11):
        card_data = suit_data[number_names[i-1]]
        card = {
            "id": f"{number_names[i-1]}_of_{suit}",
            "name": f"{number_names[i-1].title()} of {suit.title()}",
            "arcana": "minor",
            "suit": suit,
            "number": i,
            "element": suit_element,
            "keywords": card_data["keywords"],
            "polarity": card_data["polarity"],
            "intensity": suit_data["intensity_base"] + (0.1 if i <= 5 else -0.1),
            "upright_meaning": f"The {number_names[i-1].title()} of {suit.title()} represents {', '.join(card_data['keywords'][:2])}. This card signifies {suit_data['theme']} and the energy of {suit_element}. It's about finding balance and understanding in matters of {suit_data['theme']}.",
            "reversed_meaning": f"Reversed, the {number_names[i-1].title()} of {suit.title()} suggests challenges with {', '.join(card_data['keywords'][:2])}. There may be obstacles or difficulties in matters of {suit_data['theme']} that need to be addressed.",
            "influence_rules": {
                "adjacency_bonus": 0.1 if card_data["polarity"] > 0 else -0.1,
                "suit_interaction": {
                    "cups": 0.1 if suit == "cups" else -0.1 if suit == "swords" else 0.0,
                    "swords": 0.1 if suit == "swords" else -0.1 if suit == "cups" else 0.0,
                    "pentacles": 0.1 if suit == "pentacles" else 0.0,
                    "wands": 0.1 if suit == "wands" else 0.0
                },
                "themes": card_data["keywords"][:3]
            }
        }
        cards.append(card)
    
    # Create court cards (Page, Knight, Queen, King)
    court_cards = ["page", "knight", "queen", "king"]
    for court in court_cards:
        card_data = suit_data[court]
        card = {
            "id": f"{court}_of_{suit}",
            "name": f"{court.title()} of {suit.title()}",
            "arcana": "minor",
            "suit": suit,
            "number": 11 + court_cards.index(court),
            "element": suit_element,
            "keywords": card["keywords"],
            "polarity": card["polarity"],
            "intensity": suit_data["intensity_base"] + 0.2,
            "upright_meaning": f"The {court.title()} of {suit.title()} represents {', '.join(card['keywords'][:2])}. This card signifies the {court} energy in matters of {suit_data['theme']}. It's about embracing the {court} qualities in your approach to {suit_data['theme']}.",
            "reversed_meaning": f"Reversed, the {court.title()} of {suit.title()} suggests challenges with {', '.join(card['keywords'][:2])}. There may be a need to develop more {court} qualities or to approach {suit_data['theme']} differently.",
            "influence_rules": {
                "adjacency_bonus": 0.2 if card["polarity"] > 0 else -0.1,
                "suit_interaction": {
                    "cups": 0.1 if suit == "cups" else -0.1 if suit == "swords" else 0.0,
                    "swords": 0.1 if suit == "swords" else -0.1 if suit == "cups" else 0.0,
                    "pentacles": 0.1 if suit == "pentacles" else 0.0,
                    "wands": 0.1 if suit == "wands" else 0.0
                },
                "themes": card["keywords"][:3]
            }
        }
        cards.append(card)
    
    return cards

def generate_complete_deck():
    """Generate the complete 78-card deck."""
    
    # Major Arcana (already defined in the original file)
    major_arcana = [
        {
            "id": "the_fool",
            "name": "The Fool",
            "arcana": "major",
            "number": 0,
            "element": "Air",
            "astrology": "Uranus",
            "keywords": ["new beginnings", "innocence", "spontaneity", "faith", "adventure"],
            "polarity": 0.2,
            "intensity": 0.6,
            "upright_meaning": "The Fool represents new beginnings, innocence, and the pure potential of starting fresh. This card suggests taking a leap of faith, embracing spontaneity, and trusting in the journey ahead. It's about approaching life with an open heart and mind, ready for whatever adventures await.",
            "reversed_meaning": "When reversed, The Fool warns against recklessness and poor judgment. It may indicate foolish decisions, lack of direction, or being too naive. There might be a need for more careful planning and consideration before taking action.",
            "influence_rules": {
                "adjacency_bonus": 0.1,
                "major_arcana_multiplier": 1.5,
                "themes": ["new_beginnings", "innocence", "adventure"]
            }
        },
        {
            "id": "the_magician",
            "name": "The Magician",
            "arcana": "major",
            "number": 1,
            "element": "Air",
            "astrology": "Mercury",
            "keywords": ["manifestation", "willpower", "skill", "concentration", "power"],
            "polarity": 0.8,
            "intensity": 0.9,
            "upright_meaning": "The Magician represents the power of manifestation and the ability to turn ideas into reality. This card signifies having all the tools and resources needed to achieve your goals. It's about focused willpower, skill, and the confidence to take action.",
            "reversed_meaning": "Reversed, The Magician suggests manipulation, misuse of power, or lack of focus. There may be untapped potential or resources that aren't being utilized properly. It warns against using abilities for selfish purposes.",
            "influence_rules": {
                "adjacency_bonus": 0.3,
                "major_arcana_multiplier": 1.5,
                "themes": ["manifestation", "power", "skill"]
            }
        },
        {
            "id": "the_high_priestess",
            "name": "The High Priestess",
            "arcana": "major",
            "number": 2,
            "element": "Water",
            "astrology": "Moon",
            "keywords": ["intuition", "mystery", "subconscious", "wisdom", "secrets"],
            "polarity": 0.0,
            "intensity": 0.7,
            "upright_meaning": "The High Priestess represents intuition, inner wisdom, and the mysteries of the subconscious mind. This card suggests trusting your instincts and looking within for answers. It's about accessing hidden knowledge and understanding the deeper truths.",
            "reversed_meaning": "Reversed, The High Priestess indicates ignoring intuition or being disconnected from inner wisdom. There may be secrets being kept or a lack of self-awareness. It suggests the need to listen more carefully to your inner voice.",
            "influence_rules": {
                "adjacency_bonus": 0.2,
                "major_arcana_multiplier": 1.5,
                "themes": ["intuition", "mystery", "wisdom"]
            }
        },
        {
            "id": "the_empress",
            "name": "The Empress",
            "arcana": "major",
            "number": 3,
            "element": "Earth",
            "astrology": "Venus",
            "keywords": ["fertility", "abundance", "nature", "creativity", "nurturing"],
            "polarity": 0.9,
            "intensity": 0.8,
            "upright_meaning": "The Empress represents fertility, abundance, and the nurturing aspects of life. This card signifies creativity, growth, and the flourishing of ideas or projects. It's about embracing the natural flow of life and nurturing what you care about.",
            "reversed_meaning": "Reversed, The Empress suggests creative blocks, overindulgence, or neglect of nurturing aspects. There may be issues with fertility or abundance, or a need to reconnect with nature and creativity.",
            "influence_rules": {
                "adjacency_bonus": 0.4,
                "major_arcana_multiplier": 1.5,
                "themes": ["fertility", "abundance", "creativity"]
            }
        },
        {
            "id": "the_emperor",
            "name": "The Emperor",
            "arcana": "major",
            "number": 4,
            "element": "Fire",
            "astrology": "Aries",
            "keywords": ["authority", "structure", "leadership", "stability", "control"],
            "polarity": 0.7,
            "intensity": 0.9,
            "upright_meaning": "The Emperor represents authority, structure, and leadership. This card signifies the need for order, discipline, and taking control of situations. It's about establishing boundaries and creating a solid foundation for success.",
            "reversed_meaning": "Reversed, The Emperor suggests abuse of power, rigidity, or lack of structure. There may be authoritarian behavior or a need to be more flexible in leadership approaches.",
            "influence_rules": {
                "adjacency_bonus": 0.3,
                "major_arcana_multiplier": 1.5,
                "themes": ["authority", "structure", "leadership"]
            }
        },
        {
            "id": "the_hierophant",
            "name": "The Hierophant",
            "arcana": "major",
            "number": 5,
            "element": "Earth",
            "astrology": "Taurus",
            "keywords": ["tradition", "spirituality", "education", "conformity", "guidance"],
            "polarity": 0.3,
            "intensity": 0.6,
            "upright_meaning": "The Hierophant represents tradition, spiritual guidance, and conventional wisdom. This card suggests following established paths, seeking education, and learning from mentors or institutions. It's about finding meaning through structured belief systems.",
            "reversed_meaning": "Reversed, The Hierophant indicates rebellion against tradition or unconventional approaches. There may be a need to break free from restrictive beliefs or find your own spiritual path.",
            "influence_rules": {
                "adjacency_bonus": 0.2,
                "major_arcana_multiplier": 1.5,
                "themes": ["tradition", "spirituality", "education"]
            }
        },
        {
            "id": "the_lovers",
            "name": "The Lovers",
            "arcana": "major",
            "number": 6,
            "element": "Air",
            "astrology": "Gemini",
            "keywords": ["love", "relationships", "choices", "harmony", "unity"],
            "polarity": 0.8,
            "intensity": 0.8,
            "upright_meaning": "The Lovers represent love, relationships, and important choices. This card signifies harmony, unity, and the power of love to bring people together. It's about making decisions from the heart and choosing love over fear.",
            "reversed_meaning": "Reversed, The Lovers suggest disharmony, difficult choices, or relationship challenges. There may be conflicts in relationships or the need to make difficult decisions about love and commitment.",
            "influence_rules": {
                "adjacency_bonus": 0.4,
                "major_arcana_multiplier": 1.5,
                "themes": ["love", "relationships", "choices"]
            }
        },
        {
            "id": "the_chariot",
            "name": "The Chariot",
            "arcana": "major",
            "number": 7,
            "element": "Water",
            "astrology": "Cancer",
            "keywords": ["determination", "control", "victory", "willpower", "direction"],
            "polarity": 0.6,
            "intensity": 0.9,
            "upright_meaning": "The Chariot represents determination, control, and the drive to achieve victory. This card signifies strong willpower and the ability to overcome obstacles through focused determination. It's about taking control of your direction and moving forward with purpose.",
            "reversed_meaning": "Reversed, The Chariot suggests lack of direction, control issues, or giving up too easily. There may be internal conflicts or the need to find better balance in pursuing goals.",
            "influence_rules": {
                "adjacency_bonus": 0.3,
                "major_arcana_multiplier": 1.5,
                "themes": ["determination", "control", "victory"]
            }
        },
        {
            "id": "strength",
            "name": "Strength",
            "arcana": "major",
            "number": 8,
            "element": "Fire",
            "astrology": "Leo",
            "keywords": ["inner strength", "courage", "patience", "compassion", "self-control"],
            "polarity": 0.8,
            "intensity": 0.8,
            "upright_meaning": "Strength represents inner strength, courage, and the power of gentle control. This card signifies the ability to overcome challenges through patience, compassion, and self-control rather than brute force. It's about finding strength within yourself.",
            "reversed_meaning": "Reversed, Strength suggests inner weakness, lack of confidence, or giving up too easily. There may be a need to develop more self-control or find healthier ways to deal with challenges.",
            "influence_rules": {
                "adjacency_bonus": 0.4,
                "major_arcana_multiplier": 1.5,
                "themes": ["inner_strength", "courage", "patience"]
            }
        },
        {
            "id": "the_hermit",
            "name": "The Hermit",
            "arcana": "major",
            "number": 9,
            "element": "Earth",
            "astrology": "Virgo",
            "keywords": ["introspection", "guidance", "wisdom", "solitude", "searching"],
            "polarity": 0.1,
            "intensity": 0.7,
            "upright_meaning": "The Hermit represents introspection, inner guidance, and the search for wisdom. This card suggests taking time for self-reflection and seeking answers within. It's about finding your own path and trusting your inner light.",
            "reversed_meaning": "Reversed, The Hermit indicates isolation, loneliness, or being lost in your search. There may be a need to seek guidance from others or to come out of isolation.",
            "influence_rules": {
                "adjacency_bonus": 0.2,
                "major_arcana_multiplier": 1.5,
                "themes": ["introspection", "guidance", "wisdom"]
            }
        },
        {
            "id": "wheel_of_fortune",
            "name": "Wheel of Fortune",
            "arcana": "major",
            "number": 10,
            "element": "Fire",
            "astrology": "Jupiter",
            "keywords": ["change", "cycles", "luck", "destiny", "karma"],
            "polarity": 0.0,
            "intensity": 0.8,
            "upright_meaning": "The Wheel of Fortune represents change, cycles, and the turning of fate. This card signifies that change is coming and that luck is on your side. It's about embracing the natural cycles of life and trusting in destiny.",
            "reversed_meaning": "Reversed, The Wheel suggests resistance to change, bad luck, or being stuck in cycles. There may be a need to break free from negative patterns or to accept necessary changes.",
            "influence_rules": {
                "adjacency_bonus": 0.3,
                "major_arcana_multiplier": 1.5,
                "themes": ["change", "cycles", "luck"]
            }
        },
        {
            "id": "justice",
            "name": "Justice",
            "arcana": "major",
            "number": 11,
            "element": "Air",
            "astrology": "Libra",
            "keywords": ["justice", "balance", "fairness", "truth", "karma"],
            "polarity": 0.5,
            "intensity": 0.8,
            "upright_meaning": "Justice represents fairness, balance, and the truth coming to light. This card signifies that justice will be served and that balance will be restored. It's about making fair decisions and taking responsibility for your actions.",
            "reversed_meaning": "Reversed, Justice suggests unfairness, imbalance, or injustice. There may be a need to seek justice or to restore balance in your life.",
            "influence_rules": {
                "adjacency_bonus": 0.3,
                "major_arcana_multiplier": 1.5,
                "themes": ["justice", "balance", "fairness"]
            }
        },
        {
            "id": "the_hanged_man",
            "name": "The Hanged Man",
            "arcana": "major",
            "number": 12,
            "element": "Water",
            "astrology": "Neptune",
            "keywords": ["sacrifice", "surrender", "patience", "perspective", "letting go"],
            "polarity": -0.2,
            "intensity": 0.6,
            "upright_meaning": "The Hanged Man represents sacrifice, surrender, and gaining new perspective. This card suggests that sometimes you need to let go of control and see things from a different angle. It's about patience and trusting the process.",
            "reversed_meaning": "Reversed, The Hanged Man indicates resistance to necessary sacrifice or being stuck in a situation. There may be a need to let go of something that's no longer serving you.",
            "influence_rules": {
                "adjacency_bonus": 0.1,
                "major_arcana_multiplier": 1.5,
                "themes": ["sacrifice", "surrender", "patience"]
            }
        },
        {
            "id": "death",
            "name": "Death",
            "arcana": "major",
            "number": 13,
            "element": "Water",
            "astrology": "Scorpio",
            "keywords": ["transformation", "endings", "change", "rebirth", "letting go"],
            "polarity": -0.1,
            "intensity": 0.9,
            "upright_meaning": "Death represents transformation, endings, and new beginnings. This card signifies that something in your life is coming to an end to make way for something new. It's about embracing change and transformation.",
            "reversed_meaning": "Reversed, Death suggests resistance to change or being stuck in the past. There may be a need to let go of something that's holding you back from transformation.",
            "influence_rules": {
                "adjacency_bonus": 0.2,
                "major_arcana_multiplier": 1.5,
                "themes": ["transformation", "endings", "change"]
            }
        },
        {
            "id": "temperance",
            "name": "Temperance",
            "arcana": "major",
            "number": 14,
            "element": "Fire",
            "astrology": "Sagittarius",
            "keywords": ["balance", "moderation", "patience", "harmony", "healing"],
            "polarity": 0.6,
            "intensity": 0.7,
            "upright_meaning": "Temperance represents balance, moderation, and patience. This card signifies the need to find balance in all areas of life and to practice moderation. It's about healing through patience and finding harmony.",
            "reversed_meaning": "Reversed, Temperance suggests imbalance, excess, or lack of patience. There may be a need to find better balance or to practice more moderation in your life.",
            "influence_rules": {
                "adjacency_bonus": 0.3,
                "major_arcana_multiplier": 1.5,
                "themes": ["balance", "moderation", "patience"]
            }
        },
        {
            "id": "the_devil",
            "name": "The Devil",
            "arcana": "major",
            "number": 15,
            "element": "Earth",
            "astrology": "Capricorn",
            "keywords": ["temptation", "bondage", "materialism", "addiction", "shadow self"],
            "polarity": -0.8,
            "intensity": 0.9,
            "upright_meaning": "The Devil represents temptation, bondage, and the shadow aspects of human nature. This card suggests being trapped by material desires, addictions, or negative patterns. It's about recognizing and breaking free from limiting beliefs.",
            "reversed_meaning": "Reversed, The Devil indicates breaking free from bondage or overcoming addictions. There may be liberation from limiting beliefs or the recognition of your own power to change.",
            "influence_rules": {
                "adjacency_bonus": -0.3,
                "major_arcana_multiplier": 1.5,
                "themes": ["temptation", "bondage", "materialism"]
            }
        },
        {
            "id": "the_tower",
            "name": "The Tower",
            "arcana": "major",
            "number": 16,
            "element": "Fire",
            "astrology": "Mars",
            "keywords": ["sudden change", "revelation", "disruption", "breakthrough", "awakening"],
            "polarity": -0.6,
            "intensity": 1.0,
            "upright_meaning": "The Tower represents sudden change, revelation, and the breaking down of false structures. This card signifies a major breakthrough or awakening that may be disruptive but ultimately liberating. It's about truth being revealed and old foundations being destroyed.",
            "reversed_meaning": "Reversed, The Tower suggests avoiding necessary change or being in denial about a situation. There may be a need to accept that change is coming and to prepare for it.",
            "influence_rules": {
                "adjacency_bonus": -0.4,
                "major_arcana_multiplier": 1.5,
                "themes": ["sudden_change", "revelation", "disruption"]
            }
        },
        {
            "id": "the_star",
            "name": "The Star",
            "arcana": "major",
            "number": 17,
            "element": "Air",
            "astrology": "Aquarius",
            "keywords": ["hope", "inspiration", "guidance", "healing", "renewal"],
            "polarity": 0.9,
            "intensity": 0.8,
            "upright_meaning": "The Star represents hope, inspiration, and guidance from above. This card signifies healing, renewal, and the promise of better times ahead. It's about having faith in the future and trusting in divine guidance.",
            "reversed_meaning": "Reversed, The Star suggests loss of hope, despair, or lack of faith. There may be a need to reconnect with your inner light and to have more faith in the future.",
            "influence_rules": {
                "adjacency_bonus": 0.5,
                "major_arcana_multiplier": 1.5,
                "themes": ["hope", "inspiration", "guidance"]
            }
        },
        {
            "id": "the_moon",
            "name": "The Moon",
            "arcana": "major",
            "number": 18,
            "element": "Water",
            "astrology": "Pisces",
            "keywords": ["illusion", "intuition", "fear", "subconscious", "mystery"],
            "polarity": -0.3,
            "intensity": 0.7,
            "upright_meaning": "The Moon represents illusion, intuition, and the mysteries of the subconscious. This card suggests that things may not be as they appear and that you need to trust your intuition. It's about navigating through uncertainty and illusion.",
            "reversed_meaning": "Reversed, The Moon indicates clarity, truth being revealed, or overcoming fears. There may be a breakthrough in understanding or the resolution of confusing situations.",
            "influence_rules": {
                "adjacency_bonus": 0.1,
                "major_arcana_multiplier": 1.5,
                "themes": ["illusion", "intuition", "fear"]
            }
        },
        {
            "id": "the_sun",
            "name": "The Sun",
            "arcana": "major",
            "number": 19,
            "element": "Fire",
            "astrology": "Sun",
            "keywords": ["joy", "success", "vitality", "optimism", "achievement"],
            "polarity": 1.0,
            "intensity": 0.9,
            "upright_meaning": "The Sun represents joy, success, and vitality. This card signifies achievement, optimism, and the fulfillment of goals. It's about basking in success and enjoying the positive energy of life.",
            "reversed_meaning": "Reversed, The Sun suggests temporary setbacks, overconfidence, or blocked success. There may be delays in achieving goals or the need to be more realistic about expectations.",
            "influence_rules": {
                "adjacency_bonus": 0.6,
                "major_arcana_multiplier": 1.5,
                "themes": ["joy", "success", "vitality"]
            }
        },
        {
            "id": "judgement",
            "name": "Judgement",
            "arcana": "major",
            "number": 20,
            "element": "Fire",
            "astrology": "Pluto",
            "keywords": ["rebirth", "awakening", "forgiveness", "redemption", "calling"],
            "polarity": 0.7,
            "intensity": 0.8,
            "upright_meaning": "Judgement represents rebirth, awakening, and the call to a higher purpose. This card signifies forgiveness, redemption, and the opportunity for a fresh start. It's about answering your calling and embracing transformation.",
            "reversed_meaning": "Reversed, Judgement suggests self-doubt, lack of forgiveness, or ignoring your calling. There may be a need to forgive yourself or others and to listen to your inner voice.",
            "influence_rules": {
                "adjacency_bonus": 0.4,
                "major_arcana_multiplier": 1.5,
                "themes": ["rebirth", "awakening", "forgiveness"]
            }
        },
        {
            "id": "the_world",
            "name": "The World",
            "arcana": "major",
            "number": 21,
            "element": "Earth",
            "astrology": "Saturn",
            "keywords": ["completion", "achievement", "success", "wholeness", "accomplishment"],
            "polarity": 0.9,
            "intensity": 0.9,
            "upright_meaning": "The World represents completion, achievement, and success. This card signifies the successful completion of a major life cycle and the achievement of your goals. It's about wholeness, accomplishment, and the fulfillment of your potential.",
            "reversed_meaning": "Reversed, The World suggests incomplete projects, lack of closure, or unfinished business. There may be a need to complete what you've started or to find closure in some area of your life.",
            "influence_rules": {
                "adjacency_bonus": 0.5,
                "major_arcana_multiplier": 1.5,
                "themes": ["completion", "achievement", "success"]
            }
        }
    ]
    
    # Minor Arcana suits
    minor_arcana = []
    
    # Wands (Fire)
    minor_arcana.extend(create_minor_arcana_suit("wands", "Fire", ["creativity", "passion", "action", "inspiration"]))
    
    # Cups (Water)
    minor_arcana.extend(create_minor_arcana_suit("cups", "Water", ["emotions", "relationships", "intuition", "spirituality"]))
    
    # Swords (Air)
    minor_arcana.extend(create_minor_arcana_suit("swords", "Air", ["thoughts", "communication", "conflict", "truth"]))
    
    # Pentacles (Earth)
    minor_arcana.extend(create_minor_arcana_suit("pentacles", "Earth", ["material world", "work", "money", "health"]))
    
    # Combine all cards
    all_cards = major_arcana + minor_arcana
    
    # Create the complete deck structure
    deck = {
        "deck_info": {
            "name": "Rider-Waite Tarot",
            "version": "1.0",
            "description": "Complete 78-card Rider-Waite Tarot deck with upright and reversed meanings",
            "total_cards": 78,
            "major_arcana_count": 22,
            "minor_arcana_count": 56
        },
        "cards": all_cards
    }
    
    return deck

if __name__ == "__main__":
    deck = generate_complete_deck()
    
    # Write to file
    with open("/workspace/tarot_studio/db/schemas/card_schema.json", "w") as f:
        json.dump(deck, f, indent=2)
    
    print(f"Generated complete deck with {len(deck['cards'])} cards")
    print(f"Major Arcana: {len([c for c in deck['cards'] if c['arcana'] == 'major'])}")
    print(f"Minor Arcana: {len([c for c in deck['cards'] if c['arcana'] == 'minor'])}")