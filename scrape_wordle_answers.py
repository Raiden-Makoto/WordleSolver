#!/usr/bin/env python3
"""
Web scraper to get all historical Wordle answers from Rock Paper Shotgun
"""

import requests
from bs4 import BeautifulSoup
import re
import time

def scrape_wordle_answers(url="https://www.rockpapershotgun.com/wordle-past-answers"):
    """
    Scrape all Wordle answers from Rock Paper Shotgun's archive page
    """
    print(f"Scraping Wordle answers from: {url}")
    
    # Set headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"Successfully fetched page (status: {response.status_code})")
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for the "All Wordle answers" section
        # The words are typically in a list or paragraph format
        words = set()
        
        # Method 1: Look for lists containing words
        for ul in soup.find_all('ul'):
            for li in ul.find_all('li'):
                text = li.get_text().strip().upper()
                # Look for 5-letter words
                if len(text) == 5 and text.isalpha():
                    words.add(text.lower())
        
        # Method 2: Look for paragraphs with multiple words
        for p in soup.find_all('p'):
            text = p.get_text()
            # Find all 5-letter words in uppercase
            found_words = re.findall(r'\b[A-Z]{5}\b', text)
            for word in found_words:
                words.add(word.lower())
        
        # Method 3: Look for div or section containing word lists
        for div in soup.find_all(['div', 'section']):
            text = div.get_text()
            # Find patterns like "WORD" or bullet points with words
            found_words = re.findall(r'\b[A-Z]{5}\b', text)
            for word in found_words:
                words.add(word.lower())
        
        # Convert to sorted list
        word_list = sorted(list(words))
        
        print(f"Found {len(word_list)} unique 5-letter words")
        
        return word_list
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return []
    except Exception as e:
        print(f"Error parsing the page: {e}")
        return []

def save_words_to_file(words, filename="all_historical_wordles.txt"):
    """
    Save the scraped words to a file
    """
    if not words:
        print("No words to save!")
        return False
    
    try:
        with open(filename, 'w') as f:
            for word in words:
                f.write(f"{word}\n")
        
        print(f"Saved {len(words)} words to {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False

def fallback_word_list():
    """
    Fallback list of known Wordle answers if scraping fails
    """
    return [
        "split", "tower", "annex", "mirth", "spore", "union", "ratty",
        "aback", "abase", "abate", "abbey", "abide", "about", "above", 
        "abyss", "acorn", "acrid", "actor", "acute", "adage", "adapt",
        "adept", "admin", "admit", "adobe", "adopt", "adore", "adult",
        "affix", "after", "again", "agape", "agate", "agent", "agile",
        "aging", "aglow", "agony", "agree", "ahead", "aisle", "alarm",
        "album", "alert", "alien", "alike", "alive", "allow", "aloft",
        "alone", "aloof", "aloud", "alpha", "altar", "alter", "amass",
        "amber", "amble", "amiss", "ample", "angel", "anger", "angle",
        "angry", "angst", "annex", "anode", "antic", "anvil", "aorta",
        "apart", "aphid", "apple", "apply", "apron", "aptly", "arbor",
        "ardor", "argue", "aroma", "arrow", "artsy", "ascot", "ashen",
        "aside", "askew", "assay", "asset", "atlas", "atoll", "atone",
        "atria", "audio", "audit", "avail", "avert", "await", "awake",
        "award", "aware", "awash", "awful", "axiom", "azure", "bacon",
        "badge", "badly", "bagel", "baker", "baler", "balmy", "balsa",
        "banal", "banjo", "barge", "basic", "basin", "baste", "bathe",
        "baton", "batty", "bawdy", "bayou", "beach", "beady", "beast",
        "beaut", "beefy", "beget", "begin", "being", "belch", "belie",
        "belly", "below", "bench", "beret", "berth", "beset", "bevel",
        "bicep", "bilge", "binge", "biome", "birch", "birth", "black",
        "blade", "blame", "bland", "blank", "blare", "blaze", "bleak",
        "bleed", "bleep", "blimp", "blink", "bliss", "block", "bloke",
        "blond", "blown", "bluff", "blurb", "blurt", "blush", "board",
        "boast", "bongo", "bonus", "booby", "boost", "booty", "booze",
        "boozy", "borax", "borne", "bossy", "bough", "boxer", "brace",
        "braid", "brain", "brake", "brand", "brash", "brass", "brave",
        "bravo", "brawn", "bread", "break", "breed", "briar", "bribe",
        "bride", "brief", "brine", "bring", "brink", "briny", "brisk",
        "broad", "broke", "brook", "broom", "broth", "brown", "brush",
        "brute", "buddy", "buggy", "bugle", "build", "built", "bulky",
        "bully", "bunch", "burly", "burnt", "cable", "cacao", "cache",
        "cadet", "camel", "cameo", "candy", "canny", "canoe", "canon",
        "caper", "carat", "cargo", "carol", "carry", "carve", "catch",
        "cater", "caulk", "cause", "cease", "cedar", "chafe", "chain",
        "chalk", "champ", "chant", "chaos", "chard", "charm", "chart",
        "chase", "cheap", "cheat", "check", "cheek", "cheer", "chest",
        "chief", "child", "chill", "chime", "chock", "choir", "choke",
        "chord", "chore", "chose", "chunk", "chute", "cider", "cigar",
        "cinch", "circa", "civic", "clash", "class", "clean", "clear",
        "cleft", "clerk", "click", "climb", "cling", "cloak", "clock",
        "clone", "close", "cloth", "cloud", "clove", "clown", "cluck",
        "coach", "coast", "cocoa", "colon", "comet", "comfy", "comma",
        "condo", "conic", "coral", "corer", "corny", "could", "count",
        "court", "cover", "covet", "cower", "coyly", "craft", "cramp",
        "crane", "crank", "crass", "crate", "crave", "crawl", "craze",
        "crazy", "creak", "cream", "credo", "crepe", "crept", "crest",
        "crime", "crimp", "crisp", "croak", "crone", "crook", "cross",
        "crowd", "crown", "crumb", "crush", "crust", "crypt", "cumin",
        "curio", "curly", "curse", "curve", "cyber", "cynic", "daddy",
        "daisy", "dance", "dandy", "datum", "daunt", "death", "debit",
        "debug", "debut", "decal", "decay", "decoy", "decry", "deity",
        "delay", "delta", "delve", "denim", "depot", "depth", "deter",
        "devil", "diary", "dicey", "digit", "diner", "dingo", "dingy",
        "dirge", "disco", "ditto", "ditty", "dodge", "dogma", "doing",
        "dolly", "donor", "donut", "dopey", "doubt", "dowel", "dowry",
        "dozen", "draft", "drain", "drake", "drama", "drank", "drape",
        "drawl", "drawn", "dread", "dream", "dress", "dried", "drier",
        "drift", "drill", "drink", "drive", "droit", "droll", "drone",
        "drool", "droop", "dross", "drove", "drown", "druid", "drunk",
        "dryer", "dryly", "duchy", "dully", "dummy", "dumpy", "dunce",
        "dusky", "dusty", "dutch", "duvet", "dwarf", "dwell", "dwelt",
        "dying"
    ]

if __name__ == "__main__":
    print("Wordle Answer Scraper")
    print("=" * 40)
    
    # Try to scrape the words
    words = scrape_wordle_answers()
    
    # If scraping failed or returned too few words, use fallback
    if len(words) < 100:
        print(f"Scraping returned only {len(words)} words, using fallback list...")
        words = fallback_word_list()
    
    # Save to file
    if save_words_to_file(words):
        print("\nSuccess! You can now test your solver with:")
        print("python entropy.py")
        print("Choose option 3 to test on historical Wordles")
    else:
        print("\nFailed to save words to file")
    
    print(f"\nFirst 10 words: {words[:10]}")
    print(f"Last 10 words: {words[-10:]}")
