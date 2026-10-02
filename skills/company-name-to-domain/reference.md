# Company name to domain: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/company-name-to-domain` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `companies` | `--companies` | list |  | Enter one company name per line, for example Acme Widgets Inc. Add a country code after a bar to try that country's domains first, for example Globex GmbH \| de. |
| `country` | `--country` | str |  | Enter a two-letter country code (de, uk, br) to try that country's domain endings first for every company. |
| `tlds` | `--tlds` | list | `["com", "io", "co", "ai", "net", "org"]` | Domain endings to try, in order. The default covers most company sites. |
| `minConfidence` | `--min-confidence` | str | `"medium"` | Return a domain only at this confidence or above. High: the homepage names the company in its structured data, site name or title. Low: a partial match. Values: `high`, `medium`, `low`. |
| `maxCompanies` | `--max-companies` | int | `100` | Check at most this many companies in one run. |
| `maxCandidates` | `--max-candidates` | int | `12` | Check DNS for at most this many name-based domains per company. |
| `maxHomepages` | `--max-homepages` | int | `5` | Read at most this many live homepages per company. |
| `maxConcurrency` | `--max-concurrency` | int | `5` | Check this many companies at the same time. |

## Output

Every field of a `conserving_celerytop/company-name-to-domain` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `inputName` | The company name as you entered it. |
| `companyName` | The name used for matching (a trailing country code removed). |
| `country` | The country code used for domain endings, if any. |
| `domain` | The company's registrable domain, for example acme.com. |
| `website` | The homepage address after redirects. |
| `confidence` | high, medium or low. |
| `score` | 0 to 100, the sum of the matched signals. |
| `siteName` | The site's own name from structured data or og:site_name. |
| `pageTitle` | The homepage <title>. |
| `matchedSignals` | Which signals named the company: signal, match (exact or contains) and value. |
| `triedDomain` | The name-based domain that led to the website. |
| `domainAliases` | Other tried domains that redirect to the same site. |
| `otherMatches` | Other live domains that also matched, with score and confidence. |
| `weakerMatchSkipped` | True when a match was found below the minimum confidence. |
| `domainsTried` | Name-based domains checked in DNS. |
| `homepagesRead` | Homepages read for this company. |
| `rejectedCandidates` | Live domains that were not chosen, with the reason (parked_or_for_sale, name_not_on_page, robots_disallowed, blocked and more). |
| `noDnsCandidates` | Tried domains that do not exist in DNS. |
| `status` | found, not_found, invalid_input or error. |
| `checkedAt` | When the company was checked (ISO 8601). |
| `charged` | True when this row was charged. |
| `error` | Why the entry could not be used, if so. |
