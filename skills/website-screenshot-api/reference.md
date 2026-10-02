# Website screenshots: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/website-screenshot-api` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `urls` | `--urls` | list |  | Enter the pages to capture, one per line, as a full URL (https://example.com/pricing) or a domain (example.com). Each URL gives one file. |
| `format` | `--format` | str | `"png"` | Choose the file type: PNG (sharp, lossless), JPEG or WebP (smaller files) or PDF (printable document). Values: `png`, `jpeg`, `webp`, `pdf`. |
| `fullPage` | `--full-page / --no-full-page` | bool | `true` | Capture the whole scrolling page, top to bottom. Turn off to capture only the visible screen area. |
| `device` | `--device` | str | `"desktop"` | Choose the screen: Desktop 1920x1080, Laptop 1366x768, Tablet 820x1180 at 2x, Mobile 390x844 at 3x, or Custom to set the size yourself. Values: `desktop`, `laptop`, `tablet`, `mobile`, `custom`. |
| `selector` | `--selector` | str |  | Capture one element only, for example #pricing or .hero. The first match is used. Leave empty to capture the page. |
| `hideSelectors` | `--hide-selectors` | list |  | CSS selectors of elements to hide before the capture, for example cookie banners, chat widgets or pop-ups (#onetrust-banner-sdk, .cookie-notice). |
| `delaySeconds` | `--delay-seconds` | int | `1` | Wait this long after the page loads, so animations and late content settle. |
| `waitUntil` | `--wait-until` | str | `"load"` | Choose when the page counts as loaded: after the load event, after the HTML is parsed, or when the network has been quiet for half a second. Values: `load`, `domcontentloaded`, `networkidle`. |
| `waitForSelector` | `--wait-for-selector` | str |  | Wait until this CSS selector is visible before the capture, for example #chart. If it never shows, the page is captured anyway with a warning. |
| `scrollPage` | `--scroll-page / --no-scroll-page` | bool | `true` | Scroll through the page before a full-page capture or PDF, so images that load on scroll appear. |
| `darkMode` | `--dark-mode / --no-dark-mode` | bool | `false` | Ask the page for its dark color scheme (prefers-color-scheme: dark). |
| `quality` | `--quality` | int | `80` | Image quality from 1 to 100 for JPEG and WebP. Higher means sharper and larger files. |
| `maxHeight` | `--max-height` | int | `15000` | Stop full-page captures at this height in CSS pixels. The final image is at most 16,000 pixels tall, so the mobile preset (3x) stops at 5,333. |
| `viewportWidth` | `--viewport-width` | int | `1280` | Screen width in CSS pixels when Device is Custom. |
| `viewportHeight` | `--viewport-height` | int | `800` | Screen height in CSS pixels when Device is Custom. |
| `deviceScaleFactor` | `--device-scale-factor` | int |  | Device pixel ratio: 1, 2 or 3 (2 gives a retina image twice as wide). Leave empty to use the device preset. |
| `pdfFormat` | `--pdf-format` | str | `"A4"` | Paper size for PDF files. Values: `A4`, `Letter`, `Legal`, `A3`, `A5`, `Tabloid`. |
| `pdfLandscape` | `--pdf-landscape / --no-pdf-landscape` | bool | `false` | Print PDF pages in landscape orientation. |
| `printBackground` | `--print-background / --no-print-background` | bool | `true` | Include background colors and images in PDF files. |
| `timeoutSeconds` | `--timeout-seconds` | int | `30` | Give each page this long to load. A page that shows content by then is captured as it is. |
| `maxConcurrency` | `--max-concurrency` | int | `4` | Open up to this many pages at once. Memory also sets a cap: one page per 512 MB above the first 512 MB (1 GB gives 1, 2 GB gives 3, 4 GB gives 7). |

## Output

Every field of a `conserving_celerytop/website-screenshot-api` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `url` | The URL as captured (after adding https:// to a bare domain). |
| `finalUrl` | The page address after redirects. |
| `status` | ok, or why there is no file: invalid_url, robots_disallowed, robots_unreachable, blocked, host_stopped, private_address, domain_not_found, timeout, network_error, tls_error, too_many_redirects, not_a_page, selector_not_found, browser_error. |
| `httpStatus` | HTTP status of the page. Pages that answer 404 or 500 are captured as they look. |
| `pageTitle` | The page title. |
| `format` | png, jpeg, webp or pdf. |
| `device` | desktop, laptop, tablet, mobile or custom. |
| `width` | Image width in pixels (null for PDF). |
| `height` | Image height in pixels (null for PDF). |
| `pageHeight` | Full height of the page in CSS pixels. |
| `truncated` | True when the page was taller than Maximum height and the image stops there. |
| `fileSizeBytes` | Size of the saved file in bytes. |
| `screenshotUrl` | Public link to the PNG, JPEG, WebP or PDF file in the run's key-value store. |
| `fileKey` | Key of the file in the key-value store. |
| `capturedAt` | When the URL was processed (ISO 8601). |
| `warnings` | Notes about the capture, for example a slow page or a Wait for element that never showed. |
| `error` | Why there is no file, in plain words. |
| `charged` | True when this row was charged (one capture event). |
