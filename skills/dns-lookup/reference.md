# DNS lookup: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/dns-lookup` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `domains` | `--domains` | list |  | Enter domains, one per line. Website addresses and email addresses work too; the domain is taken from them. |
| `recordTypes` | `--record-types` | list | `["A", "AAAA", "CNAME", "MX", "NS", "TXT", "CAA", "SOA"]` | Pick the DNS record types to look up. Leave empty for all. Values: `A`, `AAAA`, `CNAME`, `MX`, `NS`, `TXT`, `CAA`, `SOA`. |
| `includeEmailPolicy` | `--include-email-policy / --no-include-email-policy` | bool | `true` | Add the SPF record and the DMARC policy (from _dmarc.<domain>), with has-SPF and has-DMARC flags. |
| `maxConcurrency` | `--max-concurrency` | int | `10` | How many domains to look up in parallel. |
| `maxResults` | `--max-results` | int | `10000` | Stop after this many domains. |

## Output

Every field of a `conserving_celerytop/dns-lookup` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `input` | The entry as given. |
| `domain` | The domain looked up. |
| `a` | IPv4 addresses. |
| `aaaa` | IPv6 addresses. |
| `cname` | CNAME targets. |
| `mx` | Mail servers with priority, lowest first. |
| `ns` | Name servers. |
| `txt` | TXT records. |
| `caa` | CAA records (which certificate authorities may issue). |
| `soa` | SOA record. |
| `spf` | The SPF record. |
| `dmarcPolicy` | DMARC tags (v, p, sp, pct, adkim, aspf) and whether reports are requested. Report addresses are not returned. |
| `hasMx` | True when the domain has mail servers. |
| `hasSpf` | True when the domain has an SPF record. |
| `hasDmarc` | True when the domain has a DMARC record. |
| `failedTypes` | Record types whose lookup timed out or failed. |
| `status` | ok (charged), or a free status: not_found, dns_error, invalid_domain or invalid_input. |
| `error` | Why the row is not ok. |
| `charged` | True when this row was charged. |
