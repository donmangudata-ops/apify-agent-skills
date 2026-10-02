# Company hiring signals: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/company-hiring-signals` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `companies` | `--companies` | list |  | One company per line, up to 500. A company website such as stripe.com works when the site links to its job board, a job board link such as jobs.lever.co/palantir always works, and a plain name works for many companies. Each company gets one row of hiring signals for $0.06, however many jobs it has, also when no board is found. |
| `companyLists` | `--company-lists` | list |  | Add ready-made lists of companies, instead of or next to your own list. Each company in a list gets one row for $0.06. A company in two lists, or in a list and in Companies, is read and charged once. At most 500 companies per run in all. API value: a list such as ["ai-companies"]. Values: `ai-companies`, `tech-companies`, `remote-first`, `europe-tech`, `startups`. |
| `excludeCompanies` | `--exclude-companies` | list |  | Companies to leave out, such as your own customers or companies you already track: names, websites or job board links, up to 1,000. Most useful with Ready-made company lists. A company left out is not read and not charged. Leave empty to keep every company. |
| `department` | `--department` | str |  | Count only jobs whose department, team or department path contains this text, ignoring case, for example sales. The hiring score and every count then describe those jobs. For several, put one per line. In API input, put a line break between values, as in "sales\nmarketing". Leave empty for all departments. |
| `location` | `--location` | str |  | Count only jobs in this place, such as London, California or Germany. A country name or code keeps jobs in that country, and a US state or Canadian province keeps its region. For several, put one per line. In API input, put a line break between values. Leave empty for all places. |
| `postedSince` | `--posted-since` | str |  | Count only jobs posted on or after this date: a date as YYYY-MM-DD, such as 2026-09-01, or a period such as 90 days. Jobs whose board gives no posting date are then left out. Leave empty for all dates. |
| `includeDescription` | `--include-description / --no-include-description` | bool | `false` | true: also read each job's description, to add toolsNamed (the tools the job posts name most, such as Python or Salesforce) and first hires that only the job text mentions. Free on most boards. $0.01 per started 200 jobs on JazzHR, Paylocity, Freshteam, JOIN, Polymer, Workday, Eightfold, ClearCompany, GoHire and HiringThing portals. Default false. |
| `onlyNewJobs` | `--only-new-jobs / --no-only-new-jobs` | bool | `false` | true: each row also gets newJobs and closedJobs since your previous check of that company, and previousCheckAt. The first check of a company costs $0.06. A later check costs $0.002 per started 1,000 open jobs on its board. Use it with a weekly or daily schedule. What you received is saved in your own Apify account, per Monitor name and set of filters. Default false. |
| `monitorName` | `--monitor-name` | str | `"default"` | Only used with New and closed jobs. Name of the saved state of your previous check, so separate tables or lists do not mix, for example clay-accounts. Letters, numbers, - and _ only, up to 40 characters. Default: default. |

## Output

Every field of a `conserving_celerytop/company-hiring-signals` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `rowType` | Always company: one hiring signals row per company. |
| `company` | The entry as you sent it. |
| `companyName` | The company name the board gives (Greenhouse boards with open jobs), else for a company from a ready-made list (companyLists) the name the list gives it. null elsewhere. |
| `companyDomain` | The company's domain: the website you gave, else the domain most of its job links use. null when neither is known. |
| `ats` | Job board system, for example greenhouse, lever or ashby. null when the entry was not looked up. |
| `boardUrl` | The job board the numbers come from: the link you gave, the board found on the website, or the board's usual address for a plain name. |
| `matchedBy` | How the board was matched: link (you gave the board link), website (found on the company website), directory (a plain name found in our directory of company job boards), name, or name variant (another spelling, such as odys-aviation). A name can belong to another company: then warning says so. null when no board was found. |
| `companyStatus` | What happened. Charged: ok (jobs match your filters), no_matching_jobs, no_open_jobs, not_found, source_error (the board failed or did not answer), no_job_board_found (a website we read links no supported job board), internal_error after the job board was read. Not charged: skipped_time_limit, skipped_spending_limit, skipped_client_disconnected, duplicate, invalid_input, unsupported_job_board, website_unavailable, other internal_error. The README lists every status. |
| `hiringScore` | How actively the company hires, 0 to 100: 40 points for open jobs, 40 for jobs posted in the last 30 days and 20 for jobs posted in the last 7 days. Each part is log(1 + count) / log(1 + full), at most 1, with full at 100 open jobs, 30 jobs in 30 days and 10 jobs in 7 days, so the first jobs count most: 1 open job posted this week scores 20. Counts use the jobs that pass your filters. null when the board gives no posting dates. |
| `openJobs` | Open jobs that pass your filters. |
| `jobsPostedLast7Days` | Of those, jobs posted in the last 7 days. null when the board gives no posting dates (HiringThing, Trakstar Hire, and Freshteam without includeDescription). |
| `jobsPostedLast30Days` | Of those, jobs posted in the last 30 days. null when the board gives no posting dates. |
| `newestPostedAt` | Posting date of the newest job. |
| `oldestOpenJobDays` | Days since the oldest open job was posted. null when no job has a posting date. |
| `medianJobAgeDays` | Median days since the open jobs were posted, over the jobs with a posting date. null when none has one. |
| `topDepartmentsText` | Up to 5 departments with the most jobs and their counts, such as "Engineering (12); Sales (5)". Empty text when no job has a department. |
| `topLocationsText` | Up to 5 location texts with the most jobs and their counts, such as "London (8); Remote (5)". Empty text when no job has a location. |
| `jobFunctionMix` | Share of the open jobs in each job function, read from the title, then the department and team, most first, such as "engineering 45%, sales 20%, legal <1%". Empty text without open jobs. |
| `seniorityMix` | Share of the open jobs at each seniority level read from the title, most first, such as "senior 40%, lead_manager 10%". Jobs whose title gives no level are not listed, so the shares can add up to less than 100%. |
| `remoteShare` | Share of the open jobs that can be done fully remote, 0 to 1, two decimals. |
| `salaryCoverage` | Share of jobs with a published salary. |
| `leadershipRolesText` | Titles of up to 5 open director, VP and C-level jobs, newest first, joined with "; ". Empty text when there are none. |
| `firstHireRolesText` | Titles of up to 5 jobs that are a first or founding hire, newest first, joined with "; ". Cues in the description count only with includeDescription. Empty text when there are none. |
| `toolsNamed` | With includeDescription: up to 15 tools named in the most jobs, most first, joined with ", ", such as "Python, Snowflake, Salesforce". null without descriptions. |
| `newJobs` | With onlyNewJobs: new jobs since the previous check. |
| `closedJobs` | With onlyNewJobs: jobs closed since the previous check. |
| `previousCheckAt` | With onlyNewJobs: time of the previous check. |
| `charged` | true when this company was charged in this run. |
| `chargedEvent` | The charged event: company-lookup ($0.06) or new-jobs-check ($0.002 per started 1,000 open jobs). null when not charged. |
| `warning` | What a delivered company is missing, for example some descriptions. |
| `error` | Why the company has no numbers, when something went wrong. |
| `fetchedAt` | When the lookup started. |
