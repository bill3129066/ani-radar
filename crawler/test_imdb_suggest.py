import requests
import urllib.parse

def test_imdb_suggest(query):
    encoded = urllib.parse.quote(query)
    # The API usually takes the first character to shard? 
    # v2.sg.media-imdb.com/suggestion/h/hello.json
    first_char = query[0].lower()
    url = f"https://v2.sg.media-imdb.com/suggestion/{first_char}/{encoded}.json"
    print(f"Fetching {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        resp = requests.get(url, headers=headers)
        print(resp.status_code)
        if resp.status_code == 200:
            print(resp.json())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    test_imdb_suggest("Frieren")
    test_imdb_suggest("Sousou no Frieren")
