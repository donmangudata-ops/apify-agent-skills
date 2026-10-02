# AI image upscaler: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/ai-image-upscaler` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `imageUrls` | `--image-urls` | list |  | Enter direct links to image files, one per line: PNG, JPEG, WebP, GIF, BMP or TIFF. Use your own photos, product shots, scans or artwork. |
| `imageBase64` | `--image-base64` | list |  | Paste images as base64 strings or data URIs (data:image/png;base64,...), one per line. Handy from Make, Zapier, n8n or your own code. Up to about 10 MB each. |
| `scale` | `--scale` | str | `"4"` | Choose how much larger each side gets. 4x turns 512 x 512 into 2048 x 2048. Values: `2`, `3`, `4`. |
| `outputFormat` | `--output-format` | str | `"png"` | Choose the file format of the enlarged images. PNG is lossless and keeps transparency; JPEG and WebP files are smaller. Values: `png`, `jpeg`, `webp`, `same`. |
| `noiseReduction` | `--noise-reduction` | int | `50` | Set how strongly noise and JPEG blocks are cleaned, from 0 (keep fine grain) to 100 (smoothest). 50 suits most photos. |
| `quality` | `--quality` | int | `92` | Set the compression quality for JPEG and WebP output, from 50 to 100. |
| `maxOutputMegapixels` | `--max-output-megapixels` | int | `16` | Cap the size of each enlarged image. An image that would be larger is enlarged less, to fit. 16 megapixels is 4096 x 4096. |
| `maxImages` | `--max-images` | int | `1000` | Enlarge at most this many images per run. |
| `maxFileSizeMb` | `--max-file-size-mb` | int | `25` | Download source files up to this size. |

## Output

Every field of a `conserving_celerytop/ai-image-upscaler` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `inputIndex` | Position of the image in your input (links, then uploads, then base64 entries), starting at 1. null for entries that could not be used. |
| `imageUrl` | The image link or upload link as entered. null for base64 input. |
| `source` | url for an image link, upload for an uploaded file, base64 for pasted image data. |
| `status` | ok when the enlarged image was saved, or why not: not_found, blocked, rate_limited, robots_disallowed, robots_unreadable, not_image, unsupported_format, broken_image, image_too_large, image_too_small, file_too_large, timeout, network_error, http_error, domain_not_found, too_many_redirects, out_of_memory, upscale_failed, invalid_input. |
| `outputUrl` | Link to the enlarged image file in this run's key-value store. |
| `outputKey` | Key of the enlarged image in the key-value store, for example upscaled-0001-photo.png. |
| `outputFormat` | png, jpeg or webp. |
| `outputWidth` | Width of the enlarged image in pixels. |
| `outputHeight` | Height of the enlarged image in pixels. |
| `outputSizeBytes` | File size of the enlarged image. |
| `inputFormat` | Format of the source image: png, jpeg, webp, gif, bmp or tiff. |
| `inputWidth` | Width of the source image in pixels, after EXIF rotation. |
| `inputHeight` | Height of the source image in pixels, after EXIF rotation. |
| `inputSizeBytes` | File size of the source image. |
| `scaleRequested` | The scale you asked for: 2, 3 or 4. |
| `scaleApplied` | The scale used. Lower than scaleRequested only when "Maximum output megapixels" capped the size. |
| `noiseReduction` | Noise reduction used, 0 to 100. |
| `hasTransparency` | true when the source had transparent areas, kept in PNG and WebP output. |
| `processingSeconds` | Seconds spent decoding, enlarging and encoding this image. |
| `billedImages` | Images billed for this row: 1 per started 307,200 input pixels (640 x 480). 0 when the image failed. |
| `charged` | true when this row was billed. |
| `note` | Extra information, for example when only the first frame of an animated GIF was used. |
| `processedAt` | When the image was processed (UTC, ISO 8601). |
| `error` | Why the image failed, in plain words. null when status is ok. |
