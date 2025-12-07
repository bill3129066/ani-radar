# data-enrichment Specification

## Purpose
TBD - created by archiving change improve-imdb-coverage. Update Purpose after archive.
## Requirements
### Requirement: Title Field Propagation

The data enrichment pipeline SHALL propagate `titleEnglish` and `titleOriginal` fields from raw Bahamut data through to the final dataset. These fields SHALL be synced even for previously-enriched entries.

#### Scenario: titleEnglish synced from raw data

- **GIVEN** an anime entry in `bahamut_raw.json` with `titleEnglish: "Frieren: Beyond Journey's End"`
- **WHEN** the enrichment pipeline processes the entry
- **THEN** the `titleEnglish` field SHALL be preserved in `animes_enriched.json`
- **AND** the `titleEnglish` field SHALL be preserved in `animes.json`

#### Scenario: Already-enriched entries updated with new fields

- **GIVEN** an anime entry that was previously enriched (exists in `animes_enriched.json`)
- **AND** the raw data contains a `titleEnglish` field not present in enriched data
- **WHEN** the enrichment pipeline runs
- **THEN** the `titleEnglish` field SHALL be synced from raw data to the enriched record

### Requirement: Multi-Source IMDb ID Resolution

The data enrichment pipeline SHALL resolve IMDb IDs for anime entries using a multi-source lookup strategy with the following priority order:

1. **anime-lists local database**: Direct MAL ID to IMDb ID mapping (instant, no API call)
2. **IMDb search with English title**: Search using `titleEnglish` field
3. **IMDb search with Japanese title**: Search using `titleOriginal` field as fallback

#### Scenario: IMDb ID found via anime-lists

- **GIVEN** an anime entry with MAL ID 52991
- **WHEN** the enrichment pipeline processes the entry
- **AND** anime-lists contains a mapping for MAL ID 52991 to IMDb ID tt21621240
- **THEN** the anime entry SHALL be enriched with IMDb ID tt21621240
- **AND** no IMDb API search SHALL be performed

#### Scenario: IMDb ID found via English title search

- **GIVEN** an anime entry with `titleEnglish: "Frieren: Beyond Journey's End"`
- **WHEN** anime-lists does not contain a mapping for this anime
- **AND** IMDb search with the English title returns a match
- **THEN** the anime entry SHALL be enriched with the matched IMDb ID

#### Scenario: IMDb ID found via Japanese title fallback

- **GIVEN** an anime entry without `titleEnglish` but with `titleOriginal`
- **WHEN** anime-lists does not contain a mapping
- **AND** IMDb search with the Japanese title returns a match
- **THEN** the anime entry SHALL be enriched with the matched IMDb ID

#### Scenario: No IMDb match found

- **GIVEN** an anime entry where all lookup methods fail
- **WHEN** the enrichment pipeline completes for this entry
- **THEN** the anime entry MAY be marked with `no_imdb_match: true`

### Requirement: IMDb Coverage Target

The data enrichment pipeline SHALL achieve a minimum IMDb rating coverage of 80% for all anime entries that have a corresponding MAL entry.

#### Scenario: Coverage validation after enrichment

- **GIVEN** a dataset with 1408 anime entries that have MAL ratings
- **WHEN** the full enrichment pipeline completes
- **THEN** at least 1127 entries (80% of 1408) SHALL have IMDb ratings

### Requirement: IMDb Rate Limiting

The data enrichment pipeline SHALL implement rate limiting for IMDb requests to prevent service bans.

#### Scenario: IMDb scraping rate limiting

- **GIVEN** IMDb may block rapid requests
- **WHEN** fetching IMDb ratings
- **THEN** the system SHALL wait at least 1 second between requests
- **AND** the system SHALL rotate User-Agent headers

### Requirement: Enrichment Progress Checkpointing

The data enrichment pipeline SHALL save progress periodically to enable resumption after interruptions.

#### Scenario: Checkpoint save during processing

- **GIVEN** a large batch of anime entries to enrich
- **WHEN** processing entries
- **THEN** the system SHALL save progress to the output file periodically

#### Scenario: Resume from checkpoint

- **GIVEN** a previous enrichment run was interrupted
- **WHEN** the enrichment pipeline is restarted
- **THEN** the system SHALL detect existing enriched entries
- **AND** the system SHALL skip entries that already have IMDb data

