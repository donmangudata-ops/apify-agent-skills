# Web page to Markdown: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/web-page-to-markdown` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `urls` | `--urls` | list |  | Enter the web pages to read, one per line, as full addresses (https://example.com/page) or domains. Up to 10,000 per run. Each page gives one row. |
| `outputFormats` | `--output-formats` | list | `["markdown"]` | Pick the formats to return for each page. Markdown keeps headings, lists, links, images and tables. Text is plain text with line breaks. HTML is the cleaned content HTML. Values: `markdown`, `text`, `html`. |
| `contentScope` | `--content-scope` | str | `"main"` | Main content keeps the article or main part of the page and drops menus, headers, footers, sidebars and cookie notices. Whole page keeps everything in the body except scripts and forms. Values: `main`, `full`. |
| `renderJavaScript` | `--render-java-script` | str | `"auto"` | Auto reads each page with a plain HTTP request and opens it in a browser only when it shows no content without JavaScript. Never uses plain HTTP only. Always opens every page in a browser. Browser pages cost more. Values: `auto`, `never`, `always`. |
| `includeLinks` | `--include-links / --no-include-links` | bool | `false` | Add a list of the links on each page, with their text, up to 1,000 per page. |
| `includeImages` | `--include-images / --no-include-images` | bool | `true` | Keep images in the Markdown as ![alt](address). Turn it off for text-only output. |
| `maxCharacters` | `--max-characters` | int | `200000` | Cut each output field at this many characters. The row then has truncated set to true. |
| `maxConcurrency` | `--max-concurrency` | int | `5` | How many pages to read in parallel, 1 to 20. At most 2 at a time go to the same site. |
| `timeoutSecs` | `--timeout-secs` | int | `30` | How long to wait for one page, 5 to 120 seconds. |

## Output

Every field of a `conserving_celerytop/web-page-to-markdown` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `url` | The page address as entered, normalized. |
| `finalUrl` | The address after redirects. |
| `status` | ok (charged), or a free status: robots_disallowed, robots_unreachable, blocked, http_error, not_found, timeout, not_html, unsupported_content, empty, invalid_url, invalid_input, network_error or error. |
| `httpStatus` | HTTP status of the page. |
| `fetchMode` | http (plain request) or browser (rendered with JavaScript). |
| `contentType` | Content type the server sent. |
| `title` | Page title (og:title or <title>). |
| `description` | Meta description. |
| `language` | Language from the html lang attribute. |
| `siteName` | og:site_name. |
| `canonicalUrl` | Canonical address of the page. |
| `imageUrl` | og:image of the page. |
| `publishedAt` | Publication date (ISO 8601) from meta tags or JSON-LD. |
| `modifiedAt` | Last modified date (ISO 8601) from meta tags or JSON-LD. |
| `contentScope` | main (main content found) or full (whole body used). |
| `markdown` | The content as Markdown. |
| `text` | The content as plain text. |
| `html` | The cleaned content HTML. |
| `links` | Links on the page: url and text. |
| `wordCount` | Words in the content. |
| `characterCount` | Characters in the plain text. |
| `approxTokens` | Rough LLM token count of the Markdown (characters / 4). |
| `truncated` | True when an output field was cut at the maximum characters, or the page was over 5 MB. |
| `fetchedAt` | When the page was read (ISO 8601). |
| `charged` | True for ok rows, which are charged. |
| `error` | Why the page was not read, for rows that are not ok. |
