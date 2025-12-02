#!/usr/bin/env python3
"""
Bahamut Anime Crazy Scraper
Scrapes anime data from Bahamut Anime Crazy (動畫瘋)
"""

import requests
import time
import random
import json
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from pathlib import Path
import os

# User-Agent rotation pool
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# Bahamut Anime Crazy base URLs
BASE_URL = 'https://ani.gamer.com.tw'
ANIME_LIST_URL = f'{BASE_URL}/animeList.php'
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'bahamut_raw.json')

# Rate limiting configuration
MIN_DELAY = 2.0
MAX_DELAY = 4.0

def get_random_headers() -> Dict[str, str]:
    """Generate random headers with rotated User-Agent"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def rate_limit():
    """Apply rate limiting to avoid being blocked"""
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

def get_anime_list_page(page_num: int = 1) -> Optional[str]:
    """Fetch anime list page HTML"""
    try:
        params = {'page': page_num}
        response = requests.get(ANIME_LIST_URL, params=params, headers=get_random_headers(), timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Failed to fetch anime list page {page_num}: {e}")
        return None

def parse_anime_links(html: str) -> List[str]:
    """Extract anime detail page URLs from list page"""
    soup = BeautifulSoup(html, 'lxml')
    links = []
    # Use the correct selector for the anime cards
    anime_cards = soup.select('a.theme-list-main')
    for card in anime_cards:
        href = card.get('href')
        if href:
            # The href is relative, so we make it absolute
            full_url = BASE_URL + '/' + href
            if full_url not in links:
                links.append(full_url)
    return links

def extract_anime_id(url: str) -> str:
    """Extract anime ID from Bahamut URL"""
    match = re.search(r'sn=(\d+)', url)
    return match.group(1) if match else url

def scrape_anime_detail(url: str) -> Optional[Dict]:
    """Scrape individual anime detail page"""
    try:
        response = requests.get(url, headers=get_random_headers(), timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        anime = {
            'id': extract_anime_id(url),
            'bahamutUrl': url,
            'ratings': {'bahamut': {}},
        }

        # Title
        title_elem = soup.select_one('div.anime_name h1')
        anime['title'] = title_elem.get_text(strip=True) if title_elem else ''
        
        # Thumbnail from meta tag
        thumb_meta = soup.find('meta', property='og:image')
        anime['thumbnail'] = thumb_meta['content'] if thumb_meta else ''

        # Popularity (View Count)
        pop_elem = soup.select_one('.anime_info_detail .newanime-count span')
        if pop_elem:
            pop_text = pop_elem.text.strip()
            num_match = re.search(r'[\d.]+', pop_text)
            if num_match:
                num = float(num_match.group(0))
                if '萬' in pop_text:
                    num *= 10000
                anime['popularity'] = int(num)

        # Details from the right-side info box
        data_file = soup.select_one('.data-file')
        if data_file:
            for li in data_file.select('.type-list li.type'):
                title_span = li.find('span', class_='title')
                if title_span:
                    if '首播日期' in title_span.text:
                        content_p = li.find('p', class_='content')
                        if content_p:
                             year_match = re.search(r'(\d{4})', content_p.text)
                             if year_match:
                                anime['year'] = int(year_match.group(1))

        # Episodes
        episodes_list = soup.select('section.season ul li')
        anime['episodes'] = len(episodes_list) if episodes_list else 0

        # Genres
        anime['genres'] = [tag.text for tag in soup.select('.data-file .type-list .tag-list .tag')]

        # Ratings
        score_elem = soup.select_one('.acg-score .score-overall-number')
        if score_elem:
            try:
                anime['ratings']['bahamut']['score'] = float(score_elem.text)
            except (ValueError, TypeError):
                pass
        
        votes_elem = soup.select_one('.acg-score .score-overall-people')
        if votes_elem:
            votes_match = re.search(r'(\d+)', votes_elem.text.replace(',', ''))
            if votes_match:
                anime['ratings']['bahamut']['votes'] = int(votes_match.group(1))

        # --- Phase 1.5: Secondary Scrape for Japanese Title (ACG Database) ---
        # Find "作品資料" link
        acg_link = None
        for a in soup.find_all('a'):
            if a.text and "作品資料" in a.text:
                acg_link = a.get('href')
                break
        
        if not acg_link:
             # Fallback: search by href pattern
             for a in soup.find_all('a', href=True):
                if 'acg.gamer.com.tw/acgDetail.php' in a['href']:
                    acg_link = a['href']
                    break

        if acg_link:
            # Handle relative/protocol-less URLs
            if acg_link.startswith('//'):
                acg_link = 'https:' + acg_link
            elif acg_link.startswith('/'):
                acg_link = BASE_URL + acg_link # Unlikely but safe
            elif not acg_link.startswith('http'):
                 # Could be relative, but usually starts with //
                 pass

            # Rate limit before secondary request
            rate_limit()
            
            try:
                # Fetch ACG page
                # print(f"   ... Fetching ACG info: {acg_link}") 
                acg_response = requests.get(acg_link, headers=get_random_headers(), timeout=30)
                acg_response.raise_for_status()
                acg_soup = BeautifulSoup(acg_response.text, 'lxml')
                
                # Extract Japanese Title (First h2)
                # Structure: h1(Chinese) -> h2(Japanese) -> h2(English)
                first_h2 = acg_soup.find('h2')
                if first_h2:
                    anime['titleOriginal'] = first_h2.get_text(strip=True)
            except Exception as e:
                print(f"   ⚠️ Failed to fetch ACG page {acg_link}: {e}")

        return anime

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None

def main(limit: Optional[int] = None):
    """Orchestrate full scraping process"""
    print("🚀 Starting Bahamut Anime Crazy Scraper (HTML Version)")
    
    all_anime_urls = []
    page_num = 1
    max_pages = 200 # Safety limit
    
    print("📋 Step 1: Collecting anime URLs from list pages...")
    while page_num <= max_pages:
        print(f"   Fetching page {page_num}...")
        html = get_anime_list_page(page_num)
        rate_limit()

        if not html:
            break

        links = parse_anime_links(html)
        if not links:
            print("   No more anime links found. Stopping pagination.")
            break
        
        new_links_found = 0
        for link in links:
            if link not in all_anime_urls:
                all_anime_urls.append(link)
                new_links_found += 1

        print(f"   Found {new_links_found} new animes. Total unique: {len(all_anime_urls)}")
        if new_links_found == 0 and page_num > 5: # If no new animes for a few pages, stop
            print("   No new animes found for several pages, assuming end of list.")
            break
        
        page_num += 1

    print(f"\n✓ Collected {len(all_anime_urls)} unique anime URLs.")
    if not all_anime_urls:
        return

    scraped_animes = []
    urls_to_scrape = all_anime_urls[:limit] if limit else all_anime_urls
    
    print(f"\n📺 Step 2: Scraping {len(urls_to_scrape)} anime details...")
    for i, url in enumerate(urls_to_scrape):
        print(f"   [{i+1}/{len(urls_to_scrape)}] Scraping: {url}")
        anime_data = scrape_anime_detail(url)
        if anime_data:
            scraped_animes.append(anime_data)
        rate_limit()

    print(f"\n💾 Saving {len(scraped_animes)} scraped animes to {OUTPUT_FILE}...")
    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(scraped_animes, f, ensure_ascii=False, indent=4)
        
    print("\n✅ Scraping complete!")

if __name__ == '__main__':
    import sys
    is_test = 'test' in sys.argv
    main(limit=10 if is_test else None)
