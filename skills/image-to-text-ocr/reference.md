# Image to text OCR: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/image-to-text-ocr` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `imageUrls` | `--image-urls` | list |  | Enter direct links to image files, one per line: PNG, JPEG, WebP, TIFF, BMP or GIF. Use your own receipts, screenshots, scans or photos. |
| `imageBase64` | `--image-base64` | list |  | Paste images as base64 strings or data URIs (data:image/png;base64,...), one per line. Handy from Make, Zapier, n8n or your own code. Up to about 10 MB each. |
| `languages` | `--languages` | list | `["eng"]` | Choose the languages printed in the images, up to 4. Pick only the ones you need: each extra language makes reading slower. Values: `eng`, `deu`, `fra`, `spa`, `ita`, `por`, `nld`, `pol`, `ces`, `ron`, `hun`, `swe`, `dan`, `nor`, `fin`, `cat`, `tur`, `ell`, `rus`, `ukr`, `ara`, `heb`, `hin`, `ind`, `vie`, `tha`, `jpn`, `kor`, `chi_sim`, `chi_tra`. |
| `pageLayout` | `--page-layout` | str | `"auto"` | Tell the OCR how the text is laid out. Automatic suits most pages. Single block suits receipts and screenshots that come out in the wrong order. Sparse text suits signs, labels and memes. Values: `auto`, `single-column`, `single-block`, `sparse`, `single-line`, `single-word`. |
| `autoRotate` | `--auto-rotate / --no-auto-rotate` | bool | `true` | Detect pages that are sideways or upside down and turn them upright before reading. Turn off for faster runs when all images are upright. |
| `includeLines` | `--include-lines / --no-include-lines` | bool | `false` | Add each text line with its confidence and position (left, top, width, height in pixels). |
| `includeWords` | `--include-words / --no-include-words` | bool | `false` | Add each word with its confidence and bounding box in pixels. |
| `maxImages` | `--max-images` | int | `1000` | Read at most this many images in this run. Duplicate links count once. |
| `maxFileSizeMb` | `--max-file-size-mb` | int | `20` | Download image files up to this size. Larger files get the status file_too_large. |
| `maxTiffPages` | `--max-tiff-pages` | int | `10` | Read at most this many pages of each multi-page TIFF file. Each page read counts as one image. |
| `upscaleSmallImages` | `--upscale-small-images / --no-upscale-small-images` | bool | `true` | Enlarge screenshots and small images 2x before reading, which helps with small text. |

## Output

Every field of a `conserving_celerytop/image-to-text-ocr` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `inputIndex` | Position of the image in your input (links first, then base64 entries), starting at 1. null for entries that could not be used. |
| `imageUrl` | The image link as entered. null for base64 input. |
| `source` | url for an image link, base64 for pasted image data. |
| `status` | ok when text was found, or why not: no_text, not_found, blocked, rate_limited, robots_disallowed, robots_unreadable, not_image, unsupported_format, undecodable, image_too_large, file_too_large, timeout, ocr_failed, network_error, http_error, domain_not_found, too_many_redirects, invalid_input. |
| `text` | All text read from the image, lines separated by line breaks and blocks by a blank line. Pages of a TIFF file are separated by a blank line. |
| `meanConfidence` | Average word confidence from 0 to 100. Under about 60 usually means a hard image. |
| `wordCount` | Number of words read. |
| `lineCount` | Number of text lines read. |
| `characterCount` | Length of text in characters. |
| `languages` | Language codes used for this image. |
| `pageLayout` | Page layout setting used. |
| `rotationApplied` | Degrees the page was turned clockwise before reading (0, 90, 180 or 270). Camera orientation tags are applied first and not counted here. |
| `imageFormat` | File format: PNG, JPEG, WEBP, TIFF, BMP or GIF. |
| `imageWidth` | Width of the upright image in pixels. |
| `imageHeight` | Height of the upright image in pixels. |
| `fileSizeBytes` | Size of the image file in bytes. |
| `pageCount` | Pages read: 1 for normal images, more for multi-page TIFF files. |
| `pages` | Multi-page TIFF files only: text, confidence and size per page. |
| `lines` | With Include lines: one entry per line with text, confidence, left, top, width, height (pixels of the upright image) and page. |
| `words` | With Include word boxes: one entry per word with text, confidence, left, top, width, height, lineIndex and page. |
| `billedImages` | Images charged for this row: 1, or the number of pages read for a TIFF file. 0 when no text was found or the image failed. |
| `charged` | true when this row was charged. |
| `processedAt` | When the image was read (ISO 8601, UTC). |
| `error` | Plain-language reason when there is no text, or a note (for example pages left out). |
