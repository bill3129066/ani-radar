import re
import unicodedata
import logging

logger = logging.getLogger(__name__)

def normalize_for_match(text: str) -> str:
    """
    Normalize text for "Fuzzy-Exact" matching.
    1. NFKC normalization (Full-width -> Half-width).
    2. Lowercase.
    3. Remove specific punctuation/separators that cause mismatch.
    """
    if not text:
        return ""
    
    # 1. NFKC Normalization (e.g., Ａ -> A, １ -> 1, 　 -> space)
    normalized = unicodedata.normalize('NFKC', text)
    
    # 2. Lowercase
    normalized = normalized.lower()
    
    # 3. Strip aggressive punctuation
    # We remove things that often differ between databases:
    # - Colons (Re:Zero vs Re Zero)
    # - Dashes (Sword Art Online - Progressive vs Sword Art Online Progressive)
    # - Exclamations (K-On! vs K-On)
    # - Spaces (remove all spaces to be super robust? Or normalize to single space?)
    
    # 3.1 Handle Japanese Season markers common in Bahamut but maybe not in AOD synonyms
    # "第2期" -> " 2nd Season" or just " 2"
    # AOD often uses "Title 2" or "Title Season 2"
    # Let's try to normalize to " 2" to match "Title 2" patterns if we strip "Season" later?
    # Or keep it simple: normalize to numbers.
    
    # 第2期 -> 2
    normalized = re.sub(r'第\s*(\d+)\s*期', r' \1 ', normalized)
    
    # 參之章 (Season 3) - Specific to Fire Force but might appear elsewhere
    normalized = normalized.replace('參之章', ' 3 ')
    normalized = normalized.replace('弐ノ章', ' 2 ')
    
    # 続編 -> Season 2 (or just strip it?)
    # "怪獣8号 続編" -> "Kaiju 8-gou Sequel"
    
    # Replace standard separators with space
    normalized = re.sub(r'[:\-–—!?,.~/""''「」『』]', ' ', normalized)
    
    # Collapse multiple spaces and strip
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

def clean_bahamut_title(title: str) -> str:
    """
    Clean raw Bahamut titles by removing metadata tags.
    
    Examples:
    - "鬼滅之刃 柱訓練篇 [1]" -> "鬼滅之刃 柱訓練篇"
    - "SPY×FAMILY 間諜家家酒 (電影版)" -> "SPY×FAMILY 間諜家家酒"
    - "進擊的巨人 The Final Season [無修]" -> "進擊的巨人 The Final Season"
    """
    if not title:
        return ""
    
    cleaned = title
    
    # 1. Remove [1], [2], [12.5], [無修], [先行版] etc.
    # Pattern: Space (optional) + [ + anything + ]
    # We anchor to the end or check if it looks like metadata
    cleaned = re.sub(r'\s*\[[^\]]*\]', '', cleaned)
    
    # 2. Remove common Bahamut suffixes in parenthesis
    # These are usually (電影版), (OVA), (TV), (特別篇)
    # Be careful not to remove (2011) if it distinguishes the show, 
    # BUT AOD usually puts year in a separate field.
    # Let's target specific known keywords to be safe.
    keywords = ['電影版', '劇場版', 'OVA', 'OAD', 'TV', '特別篇', '總集篇', '無修', '重製版']
    pattern = r'\s*\((?:' + '|'.join(keywords) + r')[^)]*\)'
    cleaned = re.sub(pattern, '', cleaned)
    
    return cleaned.strip()
