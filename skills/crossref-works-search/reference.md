# Crossref scholarly works search: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/crossref-works-search` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `query` | `--query` | str |  | Enter words to find in titles, abstracts, authors, journals and other metadata, for example "large language models". Leave empty to search by author, journal, ISSN or funder only. |
| `author` | `--author` | str |  | Enter an author name to match, for example "Jennifer Doudna". |
| `journal` | `--journal` | str |  | Enter a journal, book series or proceedings title to match, for example "Nature Communications". For an exact journal use Journal ISSNs. |
| `issns` | `--issns` | list |  | Add ISSNs to keep works from those journals only, for example 1476-4687. Several ISSNs are combined with OR. |
| `publishedFrom` | `--published-from` | str |  | Enter the earliest publication date as 2024, 2024-05 or 2024-05-17. |
| `publishedUntil` | `--published-until` | str |  | Enter the latest publication date as 2025, 2025-12 or 2025-12-31. |
| `types` | `--types` | list |  | Choose the work types to return. Several types are combined with OR. Leave empty for all types. Values: `journal-article`, `book-chapter`, `proceedings-article`, `posted-content`, `book`, `monograph`, `edited-book`, `reference-book`, `reference-entry`, `book-part`, `book-section`, `book-track`, `dataset`, `report`, `report-component`, `dissertation`, `peer-review`, `standard`, `component`, `journal-issue`, `journal-volume`, `journal`, `proceedings`, `proceedings-series`, `book-series`, `book-set`, `report-series`, `database`, `grant`, `other`. |
| `funders` | `--funders` | list |  | Add funders by Funder Registry ID (100000001 or 10.13039/100000001) or by exact name (National Science Foundation). Several funders are combined with OR. |
| `dois` | `--dois` | list |  | Add DOIs or doi.org links to look up those works directly, up to 10,000. When DOIs are given, the search fields and filters are not used. Unknown DOIs return a free row with status not_found. |
| `sortBy` | `--sort-by` | str | `"relevance"` | Choose the order of the results. Values: `relevance`, `newest`, `oldest`, `most-cited`, `recently-updated`. |
| `maxResults` | `--max-results` | int | `100` | Set how many works to return from a search, from 1 to 10,000. |
| `onlyWithAbstract` | `--only-with-abstract / --no-only-with-abstract` | bool | `false` | Return only works whose record includes an abstract. |
| `includeAbstracts` | `--include-abstracts / --no-include-abstracts` | bool | `false` | Turn on to add the abstract text to each row when the publisher deposited one. Off by default: abstracts are the publisher's text and can be under copyright, so you are responsible for how you reuse them. |

## Output

Every field of a `conserving_celerytop/crossref-works-search` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `doi` | DOI in lower case, for example 10.1038/nature12373. |
| `doiUrl` | https://doi.org/ link to the work. |
| `title` | Work title. |
| `subtitle` | Subtitle, when present. |
| `authors` | Author names as published on the work (names only). |
| `authorCount` | Number of authors listed. |
| `journal` | Journal, book, series or proceedings title (container title). |
| `journalAbbreviation` | Short journal title. |
| `issn` | ISSNs of the journal. |
| `isbn` | ISBNs of the book. |
| `publisher` | Publisher name. |
| `type` | Work type, for example journal-article or book-chapter. |
| `publishedDate` | Earliest publication date (YYYY, YYYY-MM or YYYY-MM-DD). |
| `publishedYear` | Publication year. |
| `publishedPrintDate` | Print publication date. |
| `publishedOnlineDate` | Online publication date. |
| `volume` | Volume. |
| `issue` | Issue. |
| `pages` | Page range or article number. |
| `citationCount` | Times cited by other works registered with Crossref. |
| `referencesCount` | Number of references the work cites. |
| `license` | License URL (the version of record license when there is one). |
| `licenses` | Every license with its URL, content version and start date. |
| `hasAbstract` | True when the publisher deposited an abstract. |
| `abstract` | Abstract as plain text, when present and Include abstracts is on. |
| `subjects` | Subject areas, when present. |
| `funders` | Funders named on the work, with Funder Registry ID and award numbers. |
| `publisherUrl` | Landing page the DOI resolves to. |
| `links` | Full-text links deposited by the publisher, with content type and intended use. |
| `relevanceScore` | Crossref relevance score for the search words. |
| `createdDate` | Date the DOI record was created. |
| `indexedAt` | Last time Crossref indexed the record. |
| `status` | ok, not_found (DOI unknown to Crossref, free) or invalid_input (not a DOI, free). |
| `error` | Why a row has no data. |
