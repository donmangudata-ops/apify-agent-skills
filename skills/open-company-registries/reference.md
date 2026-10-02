# Company registry search: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/open-company-registries` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `companyNames` | `--company-names` | list |  | Company names or parts of names to search for. Each name is searched in every registry picked under Registries. |
| `registrationNumbers` | `--registration-numbers` | list |  | LEI codes (20 characters), Norwegian organisation numbers (9 digits) or Finnish Business IDs (1234567-8). Each number goes to the registry it belongs to. |
| `registries` | `--registries` | list | `["gleif", "norway", "finland"]` | Registries to search company names in: gleif (Global LEI Index, all countries), norway (Brønnøysund Register Centre) and finland (PRH trade register). Values: `gleif`, `norway`, `finland`. |
| `maxResultsPerSearch` | `--max-results-per-search` | int | `10` | Most companies to return for one name in one registry. |
| `maxResults` | `--max-results` | int | `100` | Most rows for the whole run, across all names, numbers and registries. |
| `activeOnly` | `--active-only / --no-active-only` | bool | `true` | Return active companies only in name searches. Lookups by registration number always return the company, with its status. |
| `areas` | `--areas` | list |  | Find active companies whose business address is in these places. Norway: municipality name or four-digit municipality number (Oslo, Bergen, 0301). Finland: city or town (Helsinki, Espoo). Leave empty to skip the area search. |
| `areaCountry` | `--area-country` | str | `"norway"` | Register to search by area. Values: `norway`, `finland`. |
| `industries` | `--industries` | list |  | Plain-language industries. Each maps to official industry codes. Leave empty and add no industry codes to get every industry. Values: `restaurants`, `cafes-bars`, `hotels`, `hair-beauty`, `fitness`, `construction`, `electricians-plumbers`, `cleaning`, `real-estate-agents`, `it-consulting`, `marketing-advertising`, `accounting`, `legal`, `architecture-engineering`, `retail`, `car-repair`. |
| `industryCodes` | `--industry-codes` | list |  | NACE based industry codes, as used by both registers today (Norway SN2025, Finland TOL 2025), for example 56.1, 62.01 or 4321. Each code includes the codes under it. |
| `postalCodes` | `--postal-codes` | list |  | Optional. Keep only companies whose business address has one of these postal codes (Norway 4 digits, Finland 5 digits). Can be used without a municipality. |
| `registeredSince` | `--registered-since` | str |  | Only companies registered on or after this date. A date (2026-01-01) or a period back from today such as 30 days or 6 months. Newest companies come first. |
| `maxResultsPerArea` | `--max-results-per-area` | int | `1000` | Most companies for one municipality or city (and postal code). Max results still caps the whole run. |
| `leiCountries` | `--lei-countries` | list |  | Two-letter country codes of the legal address, such as DE or SE. Applies to GLEIF name searches only. |
| `maxRetries` | `--max-retries` | int | `3` | Retries per request after a timeout or a server error, with growing pauses. |

## Output

Every field of a `conserving_celerytop/open-company-registries` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `recordType` | company, or error for a registration number that returned nothing |
| `registry` | GLEIF, Brreg or PRH |
| `registryName` | Registry name |
| `country` | ISO country code of the company |
| `companyName` | Company name |
| `otherNames` | Previous, parallel and auxiliary names |
| `registrationNumber` | National registration number |
| `lei` | Legal Entity Identifier (GLEIF rows) |
| `legalForm` | Legal form |
| `legalFormCode` | ELF code (GLEIF) or the national form code |
| `status` | active or inactive |
| `statusDetail` | Status detail |
| `foundedDate` | Founded date |
| `registeredDate` | Registered date |
| `closedDate` | Closed date |
| `industryCode` | Industry code |
| `industryDescription` | Industry description |
| `industryCodeSystem` | Industry code system |
| `employees` | Registered employee count (Brreg) |
| `employeeBand` | Registered employees as a band: 0, 1-4, 5-9, 10-19, 20-49, 50-99, 100-249, 250-499, 500-999, 1000+ (Brreg) |
| `website` | Website |
| `street` | Street |
| `postalCode` | Postal code |
| `city` | City |
| `municipality` | Municipality of the address (Brreg) |
| `municipalityCode` | Four-digit municipality number (Brreg) |
| `addressCountry` | Address country |
| `vatRegistered` | VAT registered |
| `inLiquidation` | In liquidation |
| `bankrupt` | Bankrupt |
| `lastUpdated` | Last updated |
| `sourceUrl` | Source URL |
| `licence` | Licence |
| `attribution` | Attribution |
| `query` | Query |
| `queryType` | name, registrationNumber or area |
| `error` | Error |
| `fetchedAt` | Fetched at |
