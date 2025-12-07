# Spec: Douban HTML Search Scraper

## ADDED Requirements

### Requirement: HTML Search Functionality
The system MUST support scraping the Douban HTML search results page to find anime when the API fails.

#### Scenario: Search by Japanese Title
Given I have an anime with the Japanese title "葬送のフリーレン" (Frieren)
And the standard Chinese title search failed
When I search using `search_douban_html("葬送のフリーレン", 2023)`
Then the scraper should find the result "葬送的芙莉莲" within the top 3 results
And the result should include the Douban ID, Score, and Vote Count.

#### Scenario: Year Filtering
Given I search for "Fullmetal Alchemist"
And the search results return "Fullmetal Alchemist (2003)" and "Fullmetal Alchemist: Brotherhood (2009)"
When I provide the year `2009`
Then the scraper should select the "Brotherhood" result (allowing ±1 year tolerance).

#### Scenario: No Results
Given I search for a non-existent title "Khoajsdnlaksjd"
When I call `search_douban_html`
Then it should handle the "No results found" page gracefully and return `None`.

#### Scenario: Inspect Top 3 Results
Given a search query returns multiple results
When parsing the HTML
Then the scraper MUST iterate through at least the first 3 results (div.result)
And check the year match for each before returning `None`.

#### Scenario: Rate Limiting
Given the scraper makes multiple requests
When `search_douban_html` or `_get_douban_details` is called
Then it should respect the global `RATE_LIMIT_DELAY` of **5.0 seconds** before making the HTTP request.

#### Scenario: HTTP Errors
Given the Douban server returns a 429 (Too Many Requests)
When making a request
Then the system MUST log the error and wait/backoff or fail the specific item gracefully without crashing the entire script.

## MODIFIED Requirements

### Requirement: Fallback Search Strategy
The search logic MUST sequentially try multiple title variants until a match is found.

#### Scenario: Fallback Logic
Given the `search_douban` function with `titles={'cn': '...', 'jp': '...', 'en': '...'}`
When the Chinese title search returns `None`
Then it should automatically attempt to search using `titles['jp']` (if provided).
And if that fails, it should attempt `titles['en']` (if provided).

#### Scenario: Function Signature
Given the `search_douban` function
The signature MUST be `search_douban(titles: Dict[str, str], year: int)` to support multiple title variants.