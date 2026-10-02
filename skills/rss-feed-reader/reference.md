# RSS feed reader: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/rss-feed-reader` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `feedUrls` | `--feed-urls` | list |  | Enter RSS or Atom feed addresses, one per line. |
| `maxItemsPerFeed` | `--max-items-per-feed` | int | `50` | Return at most this many of the newest items from each feed. |
| `publishedSince` | `--published-since` | str |  | Keep only items published on or after this date, as 2026-09-01 or a period such as 24 hours or 7 days. Leave empty for all. |
| `includeContent` | `--include-content / --no-include-content` | bool | `false` | Add the full item content (content:encoded or Atom content) as plain text, when the feed has it. |
| `maxResults` | `--max-results` | int | `1000` | Stop after this many items in total. |

## Output

Every field of a `conserving_celerytop/rss-feed-reader` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `feedUrl` | The feed address. |
| `feedTitle` | The feed title. |
| `title` | Item title. |
| `url` | Item link. |
| `publishedAt` | Publication date (ISO 8601). |
| `summary` | Item description as plain text. |
| `content` | Full content as plain text, when asked for. |
| `categories` | Item categories or tags. |
| `imageUrl` | Item image, when the feed has one. |
| `enclosureUrl` | Attached file (audio, video or image). |
| `guid` | Item ID from the feed. |
| `status` | ok (charged), or a free status: feed_error, not_a_feed, no_items, robots_disallowed, not_found, invalid_url or invalid_input. |
| `error` | Why the row is not ok. |
| `charged` | True when this row was charged. |
