# Image converter and compressor: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/image-converter-compressor` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `imageUrls` | `--image-urls` | list |  | Enter direct links to image files, one per line: JPEG, PNG, WebP, AVIF, GIF, TIFF or BMP. Use your own photos, product shots, banners or screenshots. |
| `imageBase64` | `--image-base64` | list |  | Paste images as base64 strings or data URIs (data:image/png;base64,...), one per line. Handy from Make, Zapier, n8n or your own code. Up to about 10 MB each. |
| `outputFormat` | `--output-format` | str | `"webp"` | Choose the format of the new files. WebP and AVIF give the smallest files for the web; JPEG works everywhere; PNG is lossless and keeps transparency. Values: `webp`, `avif`, `jpeg`, `png`, `same`. |
| `quality` | `--quality` | int | `80` | Set the compression quality for WebP, AVIF and JPEG, from 1 (smallest file) to 100 (best image). 75 to 85 suits most web images. |
| `targetSizeKb` | `--target-size-kb` | int |  | Enter the largest file size you want per image. Quality is lowered step by step until the file fits, then the image is made smaller if needed. WebP, AVIF and JPEG only. |
| `maxWidth` | `--max-width` | int |  | Shrink wider images to this width, keeping the aspect ratio. Smaller images keep their size. |
| `maxHeight` | `--max-height` | int |  | Shrink taller images to this height, keeping the aspect ratio. Smaller images keep their size. |
| `keepMetadata` | `--keep-metadata / --no-keep-metadata` | bool | `false` | Keep EXIF and XMP data (camera, date, GPS, copyright) in the new files. Off gives smaller files and removes location data. The color profile is always kept. |
| `autoRotate` | `--auto-rotate / --no-auto-rotate` | bool | `true` | Turn photos upright using the camera's orientation tag, so they display the same everywhere. |
| `lossless` | `--lossless / --no-lossless` | bool | `false` | Save WebP without any quality loss (AVIF at top quality). Files are larger than lossy ones but usually smaller than PNG. |
| `backgroundColor` | `--background-color` | str | `"#ffffff"` | Enter the color that fills transparent areas when saving JPEG, as a hex code. |
| `keepAnimation` | `--keep-animation / --no-keep-animation` | bool | `true` | Keep all frames of animated GIF, WebP, PNG and AVIF files when the output is WebP, AVIF or PNG. JPEG output always takes the first frame. |
| `returnBase64` | `--return-base64 / --no-return-base64` | bool | `false` | Add each new file as a data URI in the dataset row (files up to 2 MB), for tools that cannot open links. |
| `maxImages` | `--max-images` | int | `1000` | Convert at most this many images per run. |
| `maxFileSizeMb` | `--max-file-size-mb` | int | `25` | Download source files up to this size. |

## Output

Every field of a `conserving_celerytop/image-converter-compressor` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `inputIndex` | Position of the image in your input (links, then uploads, then base64 entries), starting at 1. null for entries that could not be used. |
| `imageUrl` | The image link or upload link as entered. null for base64 input. |
| `source` | url for an image link, upload for an uploaded file, base64 for pasted image data. |
| `status` | ok when the new file was saved, or why not: not_found, blocked, rate_limited, robots_disallowed, robots_unreadable, not_image, unsupported_format, corrupt_image, too_large, too_many_frames, file_too_large, timeout, network_error, http_error, domain_not_found, too_many_redirects, out_of_memory, convert_failed, invalid_input. |
| `outputUrl` | Link to the new image file in this run's key-value store. |
| `outputKey` | Key of the new file in the key-value store, for example converted-0001-photo.webp. |
| `outputFormat` | webp, avif, jpeg or png. |
| `outputWidth` | Width of the new image in pixels. |
| `outputHeight` | Height of the new image in pixels. |
| `outputSizeBytes` | Size of the new file in bytes. |
| `inputFormat` | Format of the source file, for example jpeg, png, gif. |
| `inputWidth` | Width of the source image in pixels. |
| `inputHeight` | Height of the source image in pixels. |
| `inputSizeBytes` | Size of the source file in bytes. |
| `savedBytes` | Bytes saved: source size minus new size. Negative when the new file is larger. |
| `savedPercent` | Percent of the source size saved. |
| `qualityUsed` | Quality the file was saved at. Lower than your setting when a target size was reached. null for PNG and lossless output. |
| `targetSizeKb` | The target size you set, in KB. |
| `targetMet` | true when the file fits the target size. null when no target was set. |
| `resized` | true when the image was made smaller. |
| `frames` | Number of frames saved: 1 for still images. |
| `hasTransparency` | true when the image has transparent pixels. |
| `metadataKept` | true when EXIF or XMP data was copied to the new file. |
| `outputBase64` | The new file as a data URI, when Return base64 is on and the file is up to 2 MB. |
| `billedImages` | Images billed for this row: 1 per started 16 megapixels of a converted image, 0 for failures. |
| `charged` | true when this image was billed. |
| `note` | What was changed on the way, for example rotation, flattened transparency or a missed target. |
| `processingSeconds` | Seconds spent converting this image. |
| `processedAt` | When the row was written (UTC, ISO 8601). |
| `error` | Why the image could not be converted. |
