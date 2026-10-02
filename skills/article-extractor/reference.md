# Article extractor: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/article-extractor` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `articleUrls` | `--article-urls` | list |  | Enter the addresses of article pages, one per line: news stories, blog posts, press releases or guides. |
| `feedUrls` | `--feed-urls` | list |  | Enter RSS, Atom or XML sitemap addresses, one per line. The newest articles of each are read, up to Articles per feed. |
| `maxArticlesPerFeed` | `--max-articles-per-feed` | int | `20` | Read at most this many of the newest articles from each feed or sitemap. |
| `publishedSince` | `--published-since` | str |  | Keep only articles published on or after this date, as 2026-09-01 or a period such as 24 hours or 7 days. Older feed and sitemap items are skipped before they are read; an article URL published earlier gives a free row marked too_old. Leave empty for all dates. |
| `outputFormats` | `--output-formats` | list | `["text"]` | Pick the formats to return for each article. Values: `text`, `markdown`, `html`. |
| `maxArticles` | `--max-articles` | int | `100` | Read at most this many articles in the run, from URLs and feeds together, up to 5,000. |
| `onlyNewArticles` | `--only-new-articles / --no-only-new-articles` | bool | `false` | Skip articles returned by an earlier run with the same Monitor name. Schedule the Actor to get each new article once. |
| `monitorName` | `--monitor-name` | str | `"default"` | A name for this list of feeds, so several monitors can run side by side. Letters, digits and dashes. |
| `includeImages` | `--include-images / --no-include-images` | bool | `false` | Keep images inside the article in the Markdown and HTML output. The main image of each article is in imageUrl either way. |
| `maxCharacters` | `--max-characters` | int | `100000` | Cut the text, Markdown and HTML at this many characters. The row then has truncated set to true. |
| `maxConcurrency` | `--max-concurrency` | int | `5` | How many articles to read in parallel, 1 to 20. At most 2 at a time go to the same site. |
| `timeoutSecs` | `--timeout-secs` | int | `30` | How long to wait for one page or feed, 5 to 120 seconds. |

## Output

Every field of a `conserving_celerytop/article-extractor` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `url` | The article (or feed) address. |
| `finalUrl` | The address after redirects. |
| `status` | ok (charged), or a free status: not_article, too_old, blocked, robots_disallowed, robots_unreachable, http_error, not_found, timeout, not_html, invalid_url, feed_error, not_a_feed, invalid_input or network_error. |
| `httpStatus` | HTTP status of the page. |
| `source` | url (given as an article URL), feed or sitemap. |
| `feedUrl` | The feed or sitemap the article came from. |
| `title` | Article title. |
| `description` | Meta description or summary. |
| `siteName` | Site or publication name. |
| `language` | Language from the page. |
| `publishedAt` | Publication date (ISO 8601), from the page or the feed. |
| `modifiedAt` | Last modified date (ISO 8601). |
| `imageUrl` | Main image of the article. |
| `canonicalUrl` | Canonical address. |
| `excerpt` | The description, or the first 300 characters of the text. |
| `text` | Article text with paragraph breaks. |
| `markdown` | Article as Markdown. |
| `html` | Article as clean HTML. |
| `wordCount` | Words in the article. |
| `readingTimeMinutes` | Reading time at 230 words a minute. |
| `truncated` | True when the output was cut at the maximum characters, or the page was over 5 MB. |
| `fetchedAt` | When the page was read (ISO 8601). |
| `charged` | True for ok rows, which are charged. |
| `error` | Why the row is not ok. |
