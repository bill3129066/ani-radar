import json
import os

ENRICHED = '../data/animes_enriched.json'
RAW = '../data/bahamut_raw.json'

def restore():
    if not os.path.exists(ENRICHED):
        print("Enriched file not found!")
        return

    with open(ENRICHED, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} items from enriched.")
    
    raw_data = []
    for item in data:
        # Create a copy to avoid modifying enriched data (though we are just reading)
        raw_item = item.copy()
        
        # Keep only bahamut ratings in raw
        if 'ratings' in raw_item:
            bahamut = raw_item['ratings'].get('bahamut')
            raw_item['ratings'] = {}
            if bahamut:
                raw_item['ratings']['bahamut'] = bahamut
                
        # Remove fields that cross_platform adds? 
        # Actually cross_platform adds to 'ratings'.
        # It doesn't add top-level fields usually.
        # But wait, my NEW scraper adds 'titleEnglish'.
        # The OLD enriched data won't have it.
        # So this restored raw file will be the "Old Raw" state (which is fine).
        
        raw_data.append(raw_item)
        
    with open(RAW, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=4)
        
    print(f"Restored {len(raw_data)} items to {RAW}")

if __name__ == '__main__':
    restore()
