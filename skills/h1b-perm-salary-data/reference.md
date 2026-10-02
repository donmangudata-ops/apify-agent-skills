# H-1B and PERM salary data: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/h1b-perm-salary-data` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `programs` | `--programs` | list | `["lca"]` | LCA covers H-1B, H-1B1 and E-3 labor condition applications (fiscal year 2020 on). PERM covers green card labor certifications (fiscal year 2024 on). Values: `lca`, `perm`. |
| `jobTitles` | `--job-titles` | list |  | Words to find in the job title, such as software engineer or data scientist. A case matches when its title contains any one of them. |
| `employers` | `--employers` | list |  | Company names or parts of them, such as Google or Amazon. A case matches when the employer name contains any one of them. |
| `socCodes` | `--soc-codes` | list |  | Occupation codes such as 15-1252 (software developers), or a prefix such as 15-12 or 15. |
| `states` | `--states` | list |  | Two-letter codes such as CA, NY or TX (full names work too). |
| `cities` | `--cities` | list |  | City names as filed, such as Seattle or New York. Exact match, not case sensitive. |
| `fiscalYears` | `--fiscal-years` | list |  | US federal fiscal years, such as 2026 (October 2025 to September 2026). Empty: the latest year DOL has published. |
| `quarters` | `--quarters` | list |  | Limit to quarters of the fiscal year by decision date. Q1 is October to December. Empty: all quarters. Values: `1`, `2`, `3`, `4`. |
| `visaClasses` | `--visa-classes` | list |  | Empty: all visa classes. Values: `H-1B`, `H-1B1 Chile`, `H-1B1 Singapore`, `E-3 Australian`. |
| `caseStatuses` | `--case-statuses` | list | `["Certified"]` | Certified by default. Certified - Withdrawn means the employer withdrew a certified case. Values: `Certified`, `Certified - Withdrawn`, `Certified - Expired`, `Denied`, `Withdrawn`. |
| `wageLevels` | `--wage-levels` | list |  | Level I is entry level, IV is fully competent. Empty: all levels. Values: `I`, `II`, `III`, `IV`. |
| `fullTimeOnly` | `--full-time-only / --no-full-time-only` | bool | `false` | Leave out part-time positions. |
| `minAnnualWage` | `--min-annual-wage` | int |  | Offered wage converted to a yearly amount (hourly times 2,080). |
| `maxAnnualWage` | `--max-annual-wage` | int |  | Offered wage converted to a yearly amount. |
| `outputMode` | `--output-mode` | str | `"cases"` | Cases: one row per case. Summary: median, 25th, 75th and 90th percentile annual wage per group. Values: `cases`, `summary`. |
| `groupBy` | `--group-by` | str | `"socState"` | Used in summary mode. Values: `socState`, `jobTitleState`, `soc`, `jobTitle`, `employer`, `employerJobTitle`. |
| `minCasesPerGroup` | `--min-cases-per-group` | int | `3` | Groups with fewer cases are left out. |
| `maxResults` | `--max-results` | int | `100` | Case rows, or summary rows in summary mode. |

## Output

Every field of a `conserving_celerytop/h1b-perm-salary-data` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `rowType` | case, summary or error |
| `program` | LCA or PERM |
| `caseNumber` | DOL case number |
| `caseStatus` | Certified, Certified - Withdrawn, Certified - Expired, Denied or Withdrawn |
| `visaClass` | H-1B, H-1B1 Chile, H-1B1 Singapore, E-3 Australian or PERM (green card) |
| `receivedDate` | Date DOL received the case |
| `decisionDate` | Date of the decision |
| `fiscalYear` | US federal fiscal year of the decision |
| `fiscalQuarter` | Fiscal quarter of the decision, 1 to 4 |
| `employerName` | Employer |
| `employerCity` | Employer city |
| `employerState` | Employer state |
| `employerPostalCode` | Employer postal code |
| `naicsCode` | Employer industry code (NAICS) |
| `jobTitle` | Job title as filed |
| `socCode` | Occupation code (SOC) |
| `socTitle` | Occupation title (SOC) |
| `fullTime` | Full-time position |
| `wageFrom` | Offered wage, lower end, in wageUnit |
| `wageTo` | Offered wage, upper end, in wageUnit |
| `wageUnit` | Year, Month, Bi-Weekly, Week or Hour |
| `annualWage` | Offered wage per year in USD |
| `annualWageTo` | Upper end of the offered wage per year in USD |
| `prevailingWage` | Prevailing wage (LCA), in prevailingWageUnit |
| `prevailingWageUnit` | Unit of the prevailing wage |
| `annualPrevailingWage` | Prevailing wage per year in USD (LCA) |
| `pwWageLevel` | Prevailing wage level I to IV (LCA) |
| `worksiteCity` | Worksite city |
| `worksiteCounty` | Worksite county |
| `worksiteState` | Worksite state |
| `worksitePostalCode` | Worksite postal code |
| `beginDate` | Employment start date (LCA) |
| `endDate` | Employment end date (LCA) |
| `sourceFile` | DOL disclosure file the row comes from |
| `groupBy` | Summary grouping |
| `cases` | Summary: cases in the group |
| `employers` | Summary: distinct employers in the group |
| `medianAnnualWage` | Summary: median annual wage |
| `p25AnnualWage` | Summary: 25th percentile annual wage |
| `p75AnnualWage` | Summary: 75th percentile annual wage |
| `p90AnnualWage` | Summary: 90th percentile annual wage |
| `minAnnualWageSeen` | Summary: lowest annual wage |
| `maxAnnualWageSeen` | Summary: highest annual wage |
| `medianAnnualPrevailingWage` | Summary: median annual prevailing wage (LCA) |
| `fiscalYears` | Summary: fiscal years in the group |
| `status` | Error rows: invalid_input or error |
| `error` | Error rows: what went wrong |
| `charged` | Error rows: always false |
