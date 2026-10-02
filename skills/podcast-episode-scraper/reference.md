# Podcast episode scraper: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/podcast-episode-scraper` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `feedUrls` | `--feed-urls` | list |  | Enter podcast RSS feed addresses, one per line. Most podcast apps show the feed under Share or About. |
| `maxEpisodesPerFeed` | `--max-episodes-per-feed` | int | `20` | Return at most this many of the newest episodes of each podcast. |
| `publishedSince` | `--published-since` | str |  | Keep only episodes published on or after this date, as 2026-09-01 or a period such as 30 days. Leave empty for all. |
| `maxResults` | `--max-results` | int | `1000` | Stop after this many episodes in total. |

## Output

Every field of a `conserving_celerytop/podcast-episode-scraper` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `feedUrl` | The podcast feed address. |
| `podcastTitle` | Show title. |
| `podcastImageUrl` | Show artwork. |
| `podcastLanguage` | Show language from the feed. |
| `title` | Episode title. |
| `episodeUrl` | Episode web page. |
| `audioUrl` | Audio (or video) file URL. |
| `audioType` | File type, such as audio/mpeg. |
| `audioBytes` | File size in bytes, as the feed states it. |
| `durationSeconds` | Episode length in seconds (itunes:duration). |
| `season` | Season number. |
| `episode` | Episode number. |
| `publishedAt` | Publication date (ISO 8601). |
| `description` | Episode description as plain text. |
| `imageUrl` | Episode artwork. |
| `guid` | Episode ID from the feed. |
| `status` | ok (charged), or a free status: feed_error, not_a_feed, no_episodes, robots_disallowed, not_found, invalid_url or invalid_input. |
| `error` | Why the row is not ok. |
| `charged` | True when this row was charged. |
