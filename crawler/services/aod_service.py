import json
import logging
import os
import sys
from typing import Dict, List, Optional, Set, Any
from collections import defaultdict

# Add parent directory to path to import lib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.text_cleaner import normalize_for_match

logger = logging.getLogger(__name__)

class AnimeOfflineDatabase:
    def __init__(self, jsonl_path: str):
        self.jsonl_path = jsonl_path
        self.title_index: Dict[str, List[Dict]] = defaultdict(list)
        self.is_loaded = False
        
    def load(self):
        """Load and index the database."""
        if self.is_loaded:
            return

        if not os.path.exists(self.jsonl_path):
            logger.error(f"AOD file not found at: {self.jsonl_path}")
            return

        logger.info(f"Loading AOD from {self.jsonl_path}...")
        
        count = 0
        try:
            with open(self.jsonl_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        self._index_entry(entry)
                        count += 1
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.error(f"Failed to load AOD: {e}")
            raise

        self.is_loaded = True
        logger.info(f"Loaded {count} entries. Index size: {len(self.title_index)} unique keys.")

    def _index_entry(self, entry: Dict):
        """Add an entry to the index under all its titles."""
        # Extract MAL ID
        mal_id = None
        for source in entry.get('sources', []):
            if 'myanimelist.net/anime/' in source:
                try:
                    mal_id = int(source.split('/')[-1])
                    break
                except:
                    pass
        
        if not mal_id:
            return # Skip if no MAL ID (not useful for our goal)

        # Store minimal data needed for collision resolution
        compact_entry = {
            'mal_id': mal_id,
            'year': entry.get('animeSeason', {}).get('year'),
            'type': entry.get('type'), # TV, MOVIE, OVA, etc.
            'sources_count': len(entry.get('sources', [])),
            'title': entry.get('title') # Original title for debug
        }

        # Index by Main Title
        main_title = entry.get('title')
        if main_title:
            self._add_to_index(main_title, compact_entry)

        # Index by Synonyms
        for synonym in entry.get('synonyms', []):
            self._add_to_index(synonym, compact_entry)

    def _add_to_index(self, title: str, entry: Dict):
        norm_title = normalize_for_match(title)
        if norm_title:
            # Check if this mal_id is already in the list for this title (dedupe)
            exists = False
            for existing in self.title_index[norm_title]:
                if existing['mal_id'] == entry['mal_id']:
                    exists = True
                    break
            
            if not exists:
                self.title_index[norm_title].append(entry)

    def lookup(self, title: str, year: int = None, anime_type: str = None) -> Optional[int]:
        """
        Look up an anime by title.
        Returns the best matching MAL ID or None.
        """
        if not self.is_loaded:
            self.load()
            
        norm_title = normalize_for_match(title)
        matches = self.title_index.get(norm_title)
        
        if not matches:
            return None
        
        if len(matches) == 1:
            return matches[0]['mal_id']
            
        # Collision Resolution
        return self._resolve_collision(matches, year, anime_type)

    def _resolve_collision(self, matches: List[Dict], year: int = None, anime_type: str = None) -> int:
        """
        Pick the best match among multiple candidates.
        """
        candidates = list(matches)
        
        # 1. Filter by Year (if provided)
        # Allow +/- 1 year tolerance
        if year:
            year_matches = []
            for cand in candidates:
                c_year = cand.get('year')
                if c_year and abs(c_year - year) <= 1:
                    year_matches.append(cand)
            
            if year_matches:
                candidates = year_matches
                
        if len(candidates) == 1:
            return candidates[0]['mal_id']

        # 2. Filter by Type (if provided)
        # Bahamut types might not match AOD types perfectly, needs mapping if we use this strictly.
        # AOD types: TV, MOVIE, OVA, ONA, SPECIAL, MUSIC
        # For now, simplistic check if type is passed
        if anime_type:
             type_matches = [c for c in candidates if c.get('type') == anime_type]
             if type_matches:
                 candidates = type_matches

        if len(candidates) == 1:
            return candidates[0]['mal_id']

        # 3. Tie-breaker: Popularity (Source count as proxy)
        # The entry with more sources (links to other DBs) is likely the "Main" one.
        candidates.sort(key=lambda x: x['sources_count'], reverse=True)
        
        return candidates[0]['mal_id']
