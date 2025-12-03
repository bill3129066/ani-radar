import requests
import json

def debug_jikan(mal_id):
    url = f"https://api.jikan.moe/v4/anime/{mal_id}/full"
    print(f"Fetching {url}...")
    resp = requests.get(url)
    data = resp.json().get('data', {})
    
    external = data.get('external', [])
    print(f"External links found: {len(external)}")
    for link in external:
        print(f" - {link.get('name')}: {link.get('url')}")

if __name__ == "__main__":
    debug_jikan(52991) # Frieren
