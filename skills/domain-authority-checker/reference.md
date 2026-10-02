# Domain authority checker: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/domain-authority-checker` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `domains` | `--domains` | list |  | Enter the domains to check, one per line. Full URLs work too; the Actor keeps the registrable domain (www.example.co.uk becomes example.co.uk). Up to 10,000 domains per run. |
| `signals` | `--signals` | list | `["majestic", "crux"]` | Choose which open sources to read. majestic: Majestic Million rank, referring subnets and referring IPs. crux: Chrome UX Report popularity bucket (top 1,000 to top 1,000,000). rdap: domain creation date, age, expiry and registrar from the registry's RDAP server. Values: `majestic`, `crux`, `rdap`. |
| `rdapRequestsPerSecond` | `--rdap-requests-per-second` | num | `2` | Set how fast the Actor asks each registry RDAP server. Lower values are gentler on registries; 10,000 .com domains take about 85 minutes at 2 per second. |

## Output

Every field of a `conserving_celerytop/domain-authority-checker` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `domain` | Registrable domain that was checked. |
| `input` | The entry as you typed it. |
| `popularityScore` | 0 to 100, from Majestic rank and Chrome UX Report bucket. Formula in the README. |
| `majesticRank` | Position in the Majestic Million (1 is highest). Null if not in the list. |
| `majesticTldRank` | Position among domains with the same TLD. |
| `majesticRefSubnets` | Number of distinct class C subnets linking to the domain, from Majestic. |
| `majesticRefIPs` | Number of distinct IP addresses linking to the domain, from Majestic. |
| `cruxRankBucket` | Chrome UX Report popularity bucket: 1000 means top 1,000, up to 1000000. |
| `cruxOrigin` | The origin (for example https://www.example.com) that gave the best bucket. |
| `domainCreated` | Registration date from RDAP, ISO 8601. |
| `domainAgeYears` | Years since registration, one decimal. |
| `registrar` | Registrar name from RDAP. |
| `expires` | Expiry date from RDAP, ISO 8601. |
| `rdapStatus` | ok, rdap_not_found, rdap_unsupported_tld, rdap_rate_limited or rdap_error. Null when the rdap signal is off. |
| `sources` | Credit for every source that returned data for this row. Majestic Million by Majestic-12 Ltd, https://majestic.com/reports/majestic-million, licensed under CC BY 3.0 https://creativecommons.org/licenses/by/3.0/. Chrome UX Report by Google, https://developer.chrome.com/docs/crux, licensed under CC BY 4.0 https://creativecommons.org/licenses/by/4.0/. Keep this credit when you share the data. |
| `status` | ok, partial (a source failed), failed (no source answered, not charged) or invalid_input (not charged). |
| `error` | Error detail, if any. |
| `checkedAt` | When the row was built, ISO 8601. |
