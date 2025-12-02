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

# User-Agent rotation pool
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# Bahamut Anime Crazy base URLs
BASE_URL = 'https://ani.gamer.com.tw'
ANIME_LIST_URL = f'{BASE_URL}/animeList.php'

# Rate limiting configuration
MIN_DELAY = 2.0  # Minimum seconds between requests
MAX_DELAY = 4.0  # Maximum seconds between requests


def get_random_headers() -> Dict[str, str]:
    """Generate random headers with rotated User-Agent"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }


def rate_limit():
    """Apply rate limiting to avoid being blocked"""
    sleep_time = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(sleep_time)


def get_anime_list_page(page_num: int = 1) -> Optional[str]:
    """
    Fetch anime list page HTML

    Args:
        page_num: Page number to fetch

    Returns:
        HTML content or None if request fails
    """
    try:
        params = {
            'page': page_num,
        }
        response = requests.get(
            ANIME_LIST_URL,
            params=params,
            headers=get_random_headers(),
            timeout=30
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Failed to fetch anime list page {page_num}: {e}")
        return None


def parse_anime_links(html: str) -> List[str]:
    """
    Extract anime detail page URLs from list page

    Args:
        html: HTML content of anime list page

    Returns:
        List of anime detail page URLs
    """
    soup = BeautifulSoup(html, 'lxml')
    links = []

    # Find all anime links - typical patterns on anime list sites
    # Looking for links with patterns like /animeRef.php?sn=XXXXX
    anime_links = soup.find_all('a', href=re.compile(r'/animeRef\.php\?sn=\d+'))

    for link in anime_links:
        href = link.get('href')
        if href:
            # Convert to absolute URL if needed
            if href.startswith('/'):
                href = BASE_URL + href
            elif not href.startswith('http'):
                href = BASE_URL + '/' + href

            # Avoid duplicates
            if href not in links:
                links.append(href)

    return links


def extract_anime_id(url: str) -> str:
    """
    Extract anime ID from Bahamut URL

    Args:
        url: Bahamut anime URL

    Returns:
        Anime ID (sn parameter)
    """
    match = re.search(r'sn=(\d+)', url)
    if match:
        return match.group(1)
    return url  # Fallback to full URL if pattern doesn't match


def scrape_anime_detail(url: str) -> Optional[Dict]:
    """
    Scrape individual anime detail page

    Args:
        url: Anime detail page URL

    Returns:
        Dictionary with anime data or None if scraping fails
    """
    try:
        response = requests.get(
            url,
            headers=get_random_headers(),
            timeout=30
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Initialize anime data structure
        anime = {
            'id': extract_anime_id(url),
            'title': '',
            'titleOriginal': '',
            'thumbnail': '',
            'year': 0,
            'genres': [],
            'episodes': 0,
            'bahamutUrl': url,
            'popularity': 0,
            'tags': [],
            'ratings': {
                'bahamut': {
                    'score': 0.0,
                    'votes': 0
                }
            }
        }

        # Extract Chinese title
        title_elem = soup.find('h1', class_='anime_name') or soup.find('div', class_='anime-title')
        if title_elem:
            anime['title'] = title_elem.get_text(strip=True)

        # Extract Japanese original title (CRITICAL for cross-platform matching)
        # Look for common patterns: "原文:", "日文:", or in a specific class
        original_title_elem = soup.find('span', string=re.compile(r'原文[:：]')) or \
                             soup.find('div', class_='original-title')
        if original_title_elem:
            # Get the next sibling or parent text
            if original_title_elem.next_sibling:
                anime['titleOriginal'] = original_title_elem.next_sibling.strip()
            elif original_title_elem.parent:
                text = original_title_elem.parent.get_text(strip=True)
                # Remove the label
                anime['titleOriginal'] = re.sub(r'原文[:：]\s*', '', text)

        # Alternative: check for data attributes or meta tags
        if not anime['titleOriginal']:
            meta_original = soup.find('meta', {'property': 'og:title:original'}) or \
                          soup.find('span', class_='jp-title')
            if meta_original:
                anime['titleOriginal'] = meta_original.get('content', '') if meta_original.name == 'meta' else meta_original.get_text(strip=True)

        # Extract thumbnail
        thumbnail_elem = soup.find('img', class_='anime-cover') or \
                        soup.find('meta', {'property': 'og:image'})
        if thumbnail_elem:
            if thumbnail_elem.name == 'meta':
                anime['thumbnail'] = thumbnail_elem.get('content', '')
            else:
                anime['thumbnail'] = thumbnail_elem.get('src', '')

        # Extract year
        year_elem = soup.find('span', string=re.compile(r'首播[:：]')) or \
                   soup.find('div', class_='anime-year')
        if year_elem:
            year_text = year_elem.parent.get_text(strip=True) if year_elem.parent else year_elem.get_text(strip=True)
            year_match = re.search(r'(\d{4})', year_text)
            if year_match:
                anime['year'] = int(year_match.group(1))

        # Extract genres
        genre_container = soup.find('div', class_='anime-genre') or \
                         soup.find_all('a', href=re.compile(r'genre'))
        if genre_container:
            if isinstance(genre_container, list):
                anime['genres'] = [g.get_text(strip=True) for g in genre_container]
            else:
                genre_tags = genre_container.find_all('a')
                anime['genres'] = [g.get_text(strip=True) for g in genre_tags]

        # Extract episode count
        episode_elem = soup.find('span', string=re.compile(r'集數[:：]')) or \
                      soup.find('div', class_='anime-episodes')
        if episode_elem:
            episode_text = episode_elem.parent.get_text(strip=True) if episode_elem.parent else episode_elem.get_text(strip=True)
            episode_match = re.search(r'(\d+)', episode_text)
            if episode_match:
                anime['episodes'] = int(episode_match.group(1))

        # Extract Bahamut rating (1-5 scale)
        rating_elem = soup.find('div', class_='anime-rating') or \
                     soup.find('span', class_='score')
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
            if rating_match:
                anime['ratings']['bahamut']['score'] = float(rating_match.group(1))

        # Extract vote count
        votes_elem = soup.find('span', string=re.compile(r'評分人數[:：]')) or \
                    soup.find('span', class_='vote-count')
        if votes_elem:
            votes_text = votes_elem.parent.get_text(strip=True) if votes_elem.parent else votes_elem.get_text(strip=True)
            votes_match = re.search(r'(\d+)', votes_text.replace(',', ''))
            if votes_match:
                anime['ratings']['bahamut']['votes'] = int(votes_match.group(1))

        # Extract popularity (view count)
        popularity_elem = soup.find('span', string=re.compile(r'觀看次數[:：]|人氣[:：]')) or \
                         soup.find('div', class_='view-count')
        if popularity_elem:
            popularity_text = popularity_elem.parent.get_text(strip=True) if popularity_elem.parent else popularity_elem.get_text(strip=True)
            popularity_match = re.search(r'(\d+)', popularity_text.replace(',', ''))
            if popularity_match:
                anime['popularity'] = int(popularity_match.group(1))

        # Extract tags (optional additional metadata)
        tag_container = soup.find_all('a', class_='tag') or \
                       soup.find_all('span', class_='anime-tag')
        if tag_container:
            anime['tags'] = [tag.get_text(strip=True) for tag in tag_container]

        return anime

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None


def save_progress(animes: List[Dict], output_file: str):
    """
    Save progress incrementally to avoid data loss

    Args:
        animes: List of anime dictionaries
        output_file: Path to output JSON file
    """
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(animes, f, ensure_ascii=False, indent=2)

        print(f"💾 Progress saved: {len(animes)} anime")
    except Exception as e:
        print(f"❌ Failed to save progress: {e}")


def main():
    """
    Orchestrate full scraping process
    """
    print("🚀 Starting Bahamut Anime Crazy Scraper")
    print("=" * 60)

    output_file = '../data/bahamut_raw.json'
    all_anime_urls = []
    scraped_animes = []

    # Step 1: Collect all anime URLs from list pages
    print("\n📋 Step 1: Collecting anime URLs...")
    page_num = 1
    max_pages = 100  # Safety limit

    while page_num <= max_pages:
        print(f"   Fetching page {page_num}...")
        html = get_anime_list_page(page_num)

        if not html:
            print(f"   ⚠️  Failed to fetch page {page_num}, stopping pagination")
            break

        links = parse_anime_links(html)

        if not links:
            print(f"   ℹ️  No more anime found on page {page_num}, stopping")
            break

        new_links = [link for link in links if link not in all_anime_urls]
        all_anime_urls.extend(new_links)
        print(f"   ✓ Found {len(new_links)} new anime (total: {len(all_anime_urls)})")

        # Rate limiting between page requests
        rate_limit()
        page_num += 1

    print(f"\n✓ Collected {len(all_anime_urls)} unique anime URLs")

    if not all_anime_urls:
        print("❌ No anime URLs found. Please check the scraper logic.")
        return

    # Step 2: Scrape each anime detail page
    print(f"\n📺 Step 2: Scraping anime details...")
    print(f"   Estimated time: {len(all_anime_urls) * 3 / 60:.1f} minutes")
    print()

    for idx, url in enumerate(all_anime_urls, 1):
        print(f"   [{idx}/{len(all_anime_urls)}] Scraping: {url}")

        anime = scrape_anime_detail(url)

        if anime:
            scraped_animes.append(anime)
            print(f"   ✓ {anime['title']} ({anime.get('titleOriginal', 'N/A')})")
        else:
            print(f"   ✗ Failed to scrape this anime, continuing...")

        # Save progress every 100 anime
        if idx % 100 == 0:
            save_progress(scraped_animes, output_file)

        # Rate limiting between detail page requests
        rate_limit()

    # Final save
    save_progress(scraped_animes, output_file)

    # Summary
    print("\n" + "=" * 60)
    print("✅ Scraping Complete!")
    print(f"   Total anime scraped: {len(scraped_animes)}/{len(all_anime_urls)}")
    print(f"   Success rate: {len(scraped_animes)/len(all_anime_urls)*100:.1f}%")
    print(f"   Output file: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
