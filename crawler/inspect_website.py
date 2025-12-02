#!/usr/bin/env python3
"""
Website Inspector Tool
Helps inspect Bahamut Anime Crazy website structure to verify selectors
"""

import requests
from bs4 import BeautifulSoup
from bahamut_scraper import get_random_headers, BASE_URL, ANIME_LIST_URL


def inspect_list_page():
    """
    Fetch and display the structure of anime list page
    """
    print("🔍 Inspecting Anime List Page")
    print("=" * 60)
    print(f"URL: {ANIME_LIST_URL}\n")

    try:
        response = requests.get(ANIME_LIST_URL, headers=get_random_headers(), timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        print("📋 All <a> tags with anime-related hrefs (first 10):")
        print("-" * 60)

        # Find all links
        all_links = soup.find_all('a', href=True)
        anime_links = [link for link in all_links if 'anime' in link.get('href', '').lower()][:10]

        for i, link in enumerate(anime_links, 1):
            href = link.get('href')
            text = link.get_text(strip=True)
            classes = link.get('class', [])

            print(f"\n{i}. Text: {text[:50]}")
            print(f"   href: {href}")
            print(f"   class: {classes}")

        print("\n" + "=" * 60)
        print("💡 Use these patterns to update parse_anime_links() in bahamut_scraper.py")

    except Exception as e:
        print(f"❌ Failed to inspect list page: {e}")


def inspect_detail_page(url: str):
    """
    Fetch and display the structure of an anime detail page

    Args:
        url: Anime detail page URL
    """
    print("🔍 Inspecting Anime Detail Page")
    print("=" * 60)
    print(f"URL: {url}\n")

    try:
        response = requests.get(url, headers=get_random_headers(), timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # Display page title
        page_title = soup.find('title')
        print(f"Page Title: {page_title.get_text(strip=True) if page_title else 'N/A'}\n")

        # Find all headings
        print("📌 All Headings (h1-h3):")
        print("-" * 60)
        for tag in ['h1', 'h2', 'h3']:
            headings = soup.find_all(tag)
            for heading in headings:
                classes = heading.get('class', [])
                print(f"{tag.upper()}: {heading.get_text(strip=True)[:60]}")
                if classes:
                    print(f"      class: {classes}")

        # Find all divs with specific classes (likely to contain anime info)
        print("\n📦 Divs with 'anime', 'info', or 'detail' in class name (first 10):")
        print("-" * 60)
        info_divs = []
        for div in soup.find_all('div', class_=True):
            classes = div.get('class', [])
            class_str = ' '.join(classes)
            if any(keyword in class_str.lower() for keyword in ['anime', 'info', 'detail', 'data', 'rating', 'score']):
                info_divs.append((div, classes))

        for i, (div, classes) in enumerate(info_divs[:10], 1):
            text = div.get_text(strip=True)[:80]
            print(f"\n{i}. class: {classes}")
            print(f"   Text: {text}")

        # Find all spans (often contain specific data points)
        print("\n📊 Spans with text containing '原文', '評分', '集數', '首播', '觀看' (first 10):")
        print("-" * 60)
        keywords = ['原文', '評分', '集數', '首播', '觀看', '人氣', '日文']
        relevant_spans = []

        for span in soup.find_all('span'):
            text = span.get_text(strip=True)
            if any(keyword in text for keyword in keywords):
                relevant_spans.append(span)

        for i, span in enumerate(relevant_spans[:10], 1):
            classes = span.get('class', [])
            text = span.get_text(strip=True)
            print(f"\n{i}. Text: {text}")
            if classes:
                print(f"   class: {classes}")
            if span.parent:
                print(f"   Parent: {span.parent.name} {span.parent.get('class', [])}")

        # Find all images (for thumbnail)
        print("\n🖼️  Images (first 5):")
        print("-" * 60)
        for i, img in enumerate(soup.find_all('img')[:5], 1):
            src = img.get('src', '')
            alt = img.get('alt', '')
            classes = img.get('class', [])
            print(f"\n{i}. src: {src[:80]}")
            print(f"   alt: {alt[:60]}")
            if classes:
                print(f"   class: {classes}")

        print("\n" + "=" * 60)
        print("💡 Use these patterns to update scrape_anime_detail() in bahamut_scraper.py")

    except Exception as e:
        print(f"❌ Failed to inspect detail page: {e}")


def main():
    """
    Main inspector function
    """
    print("\n🔧 Bahamut Anime Crazy Website Inspector")
    print("=" * 60)
    print("\nThis tool helps you inspect the website structure to verify scraper selectors.")
    print("\nOptions:")
    print("  1. Inspect anime list page")
    print("  2. Inspect anime detail page (you need to provide a URL)")
    print()

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == '1':
        print()
        inspect_list_page()
    elif choice == '2':
        print()
        url = input("Enter anime detail page URL: ").strip()
        if url:
            print()
            inspect_detail_page(url)
        else:
            print("❌ No URL provided")
    else:
        print("❌ Invalid choice")

    print("\n✅ Inspection complete!")
    print("\nNext steps:")
    print("  1. Review the output above")
    print("  2. Update selectors in bahamut_scraper.py")
    print("  3. Run: python test_scraper.py")
    print()


if __name__ == '__main__':
    main()
