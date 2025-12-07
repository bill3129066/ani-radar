"""
Anime-Lists Service
Provides MAL ID -> IMDb ID lookups using the Fribb/anime-lists community database.
Source: https://github.com/Fribb/anime-lists
"""

import json
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class AnimeListsService:
    """Service for looking up IMDb IDs from MAL IDs using anime-lists data."""

    def __init__(self, json_path: str):
        self.json_path = json_path
        self.mal_to_imdb: Dict[int, str] = {}
        self.is_loaded = False

    def load(self):
        """Load and index the anime-lists database."""
        if self.is_loaded:
            return

        if not os.path.exists(self.json_path):
            logger.error(f"anime-lists file not found at: {self.json_path}")
            return

        logger.info(f"Loading anime-lists from {self.json_path}...")

        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Build MAL ID -> IMDb ID index
            for entry in data:
                mal_id = entry.get('mal_id')
                imdb_id = entry.get('imdb_id')

                if mal_id and imdb_id:
                    self.mal_to_imdb[int(mal_id)] = imdb_id

            self.is_loaded = True
            logger.info(f"Loaded {len(self.mal_to_imdb)} MAL->IMDb mappings.")

        except Exception as e:
            logger.error(f"Failed to load anime-lists: {e}")
            raise

    def lookup(self, mal_id: int) -> Optional[str]:
        """
        Look up IMDb ID for a given MAL ID.

        Args:
            mal_id: MyAnimeList anime ID

        Returns:
            IMDb ID (e.g., 'tt1234567') or None if not found
        """
        if not self.is_loaded:
            self.load()

        if not mal_id:
            return None

        return self.mal_to_imdb.get(int(mal_id))

    def get_stats(self) -> Dict:
        """Return statistics about the loaded data."""
        if not self.is_loaded:
            self.load()

        return {
            'total_mappings': len(self.mal_to_imdb),
            'is_loaded': self.is_loaded
        }
