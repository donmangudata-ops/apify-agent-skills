# Sitemap URL extractor: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/sitemap-url-extractor` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `startUrls` | `--start-urls` | list |  | Enter websites (example.com), whose sitemaps are found through robots.txt and the usual addresses, or sitemap addresses directly. One per line. |
| `urlContains` | `--url-contains` | str |  | Keep only URLs that contain this text, for example /blog/ or /products/. Leave empty for all. |
| `maxUrlsPerSite` | `--max-urls-per-site` | int | `1000` | Return at most this many URLs for each website or sitemap you enter. |
| `maxSitemapsPerSite` | `--max-sitemaps-per-site` | int | `50` | Read at most this many sitemap files per website, counting the files inside sitemap indexes. |
| `maxResults` | `--max-results` | int | `5000` | Stop after this many URLs in total. |

## Output

Every field of a `conserving_celerytop/sitemap-url-extractor` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `input` | The website or sitemap as entered. |
| `url` | Page URL from the sitemap. |
| `lastModified` | lastmod (ISO 8601). |
| `changeFrequency` | changefreq, such as daily or weekly. |
| `priority` | priority from 0.0 to 1.0. |
| `sitemapUrl` | The sitemap file the URL was listed in. |
| `imageCount` | Number of image entries for the URL (image sitemaps). |
| `status` | ok (charged), or a free status: no_sitemap, no_urls, robots_disallowed, not_found, invalid_url, error or invalid_input. |
| `error` | Why the row is not ok. |
| `charged` | True when this row was charged. |
