# Live jobs HTTP API: reference

Input fields and output fields of the Actor, in one file.

## Input

Every field of the `conserving_celerytop/live-jobs-http-api` input, read from its published input schema. Each one is a flag of `run.py` (camelCase becomes kebab-case); lists are comma-separated. `--input-json` and `--input-file` pass a full input instead.

| Field | Flag | Type | Default | What it does |
|---|---|---|---|---|
| `companies` | `--companies` | list |  | One entry per company, up to 500. A job board link works best, such as boards.greenhouse.io/stripe, on Greenhouse, Lever, Ashby, Workday, Eightfold, Workable, Personio, Teamtailor, Recruitee and 13 more boards (list in the README). A website (stripe.com) works too, as does a plain name (stripe) for many companies. One company lookup per company, 1,000 jobs included, also when no board is found. |
| `companyLists` | `--company-lists` | list |  | Run on ready-made lists of companies instead of, or next to, your own list in Companies. Each list company is one company lookup (1,000 jobs included), and the filters apply as usual. To run only the lists, clear Companies. A company in two lists, or also in Companies, is read and charged once. At most 500 companies per run. API value: a list such as ["ai-companies"]. Values: `ai-companies`, `tech-companies`, `remote-first`, `europe-tech`, `startups`. |
| `excludeCompanies` | `--exclude-companies` | list |  | Companies to leave out, such as your own employer or companies you already track: company names, websites or job board links, up to 1,000. Most useful with Ready-made company lists. A company left out is not read and not charged. Leave empty to keep every company. |
| `outputMode` | `--output-mode` | str | `"jobs"` | jobs: one row per job. companies: one summary row per company with open jobs, recent postings, remote share, top departments, locations, seniority, job functions, leadership and first-hire roles, salary medians and top tools (all fields in the README). It costs one lookup per company, never the extra 1,000-job charge. both: job rows plus summary rows (rowType job, company or status). Values: `jobs`, `companies`, `both`. |
| `includeDescription` | `--include-description / --no-include-description` | bool | `false` | true: add each job's full description as plain text (up to 60,000 characters, no contact details) and the tools it names (field tools). Free on most boards; $0.01 per started 200 jobs on JazzHR, Paylocity, Freshteam, JOIN, Polymer, Workday, Eightfold, ClearCompany, GoHire and HiringThing portals. With Only new jobs, only new jobs are described. |
| `descriptionFormat` | `--description-format` | str | `"text"` | How each description comes, with Include job description on. text: plain text. html: the board's own HTML, kept safe: no scripts, styles, frames or event handlers. markdown: the same converted to Markdown. Every format has emails, phone numbers and profile links removed and is cut at 60,000 characters. Same price. Values: `text`, `html`, `markdown`. |
| `maxJobsPerCompany` | `--max-jobs-per-company` | int |  | Return at most this many jobs per company, the newest first, for example 50. To answer a quick question, 20 is enough. Leave empty for all jobs, up to 10,000 per company. Set 1,000 or less to never pay the $0.01 charge for each further 1,000 jobs. With Only new jobs, closed jobs come on top of this cap and count toward that charge. Summary rows still count every matching job. |
| `onlyNewJobs` | `--only-new-jobs / --no-only-new-jobs` | bool | `false` | true: return only jobs you have not received from this Actor before, plus jobs that closed since your previous check (field change is new or closed). The first check of a company returns all its jobs for one company lookup; a later check costs $0.002 per started 1,000 open jobs. Use it with a schedule. What you received is saved in your own Apify account, per Monitor name and set of filters. |
| `monitorName` | `--monitor-name` | str | `"default"` | Only used with Only new jobs. Name of the saved list of jobs you received, so separate watchlists do not mix, for example sales-accounts or competitors. Letters, numbers, - and _ only, up to 40 characters. Default: default. |
| `includeUpdatedJobs` | `--include-updated-jobs / --no-include-updated-jobs` | bool | `false` | Only used with Only new jobs. true: also return jobs you received before whose title, location, salary or job type changed since your previous check, with change updated, changedFields and the previous values. Each is one more row, so it counts toward the $0.01 per further 1,000 jobs. Default false: the price stays the same and changes are only counted in summary rows. |
| `skipReposts` | `--skip-reposts / --no-skip-reposts` | bool | `false` | Only used with Only new jobs. true: leave out a new job with the same title and location as a job you received that closed in the last 30 days, a repost under a new id. It gets no row and no alert, and never comes back as new; skippedRepostsCount says how many. Default false: reposts come as new jobs with reposted true. |
| `alertWebhookUrl` | `--alert-webhook-url` | str |  | Only used with Only new jobs. An https link that gets one short message after a check with new or closed jobs, and nothing on days without changes: the incoming webhook of a Slack, Discord or Teams channel, or a Make, Zapier or n8n webhook, such as https://hooks.slack.com/services/... It lists counts per company and the jobs with links. Free. Kept secret. |
| `alertMaxJobs` | `--alert-max-jobs` | int | `10` | Only used with Alert webhook URL. How many new and closed jobs the alert lists, one line each with title, location and salary when known, for example 20. More jobs are counted with a link to the dataset. A whole number from 1 to 50. Free. Default 10. |
| `alertOnFirstCheck` | `--alert-on-first-check / --no-alert-on-first-check` | bool | `false` | Only used with Alert webhook URL. true: also send an alert on the first check of a company, which returns all its open jobs as new. Default false: the first check sends nothing, and later checks alert only on new and closed jobs. Free. |
| `titleIncludes` | `--title-includes` | list |  | Keep only jobs whose title contains one of these words or phrases, ignoring case. Use it to check if a company is hiring for a role, for example data engineer or account executive. Whole words only, so engineer matches Software Engineer but not Engineering Manager. A list of up to 100. Leave empty for all titles. |
| `titleExcludes` | `--title-excludes` | list |  | Leave out jobs whose title contains any of these words or phrases, ignoring case. Whole words only, so intern does not match International. A list of up to 100, for example senior and intern. An excluded word wins over Title includes. Leave empty to keep every title. |
| `descriptionIncludes` | `--description-includes` | list |  | Keep only jobs whose description names any of these words or phrases, ignoring case, such as Snowflake, Rust or C++. Whole words only, so Rust does not match trust. A tool also matches its other names, so Postgres finds PostgreSQL. Up to 100. This turns on Include job description (see its price). Leave empty for all jobs. |
| `skills` | `--skills` | list |  | Keep only jobs that name at least one of these skills in their tools, such as Python, Snowflake or Salesforce, ignoring case. Other spellings work, so golang finds Go; matchedSkills lists the ones found. An unknown skill stops the run before any charge, with close names. Up to 100. This turns on Include job description (see its price). Leave empty for all jobs. |
| `department` | `--department` | str |  | Keep only jobs whose department, team or department path contains this text, ignoring case, for example engineering. For several, put one per line. A job that matches any of them is kept. In API input, put a line break between values, as in "engineering\nsales". Up to 100. Leave empty for all departments. |
| `seniorities` | `--seniorities` | list |  | Keep only jobs at one of these levels (field seniority), read from the title: Senior Engineer is senior, Head of Sales is director. A title without a level word, such as Software Engineer, has no seniority: those jobs are left out, and the company's warning says how many. Leave empty for all levels. Values: `intern`, `entry`, `mid`, `senior`, `staff_principal`, `lead_manager`, `director`, `vp`, `c_level`. |
| `jobFunctions` | `--job-functions` | list |  | Keep only jobs in these functions, read from each job's title, then its department and team (output field jobFunction). Pick one or more, for example Engineering and Data. English and German titles are read, and basic French, Spanish, Dutch and Swedish ones. In our tests about 9 in 10 jobs got the right function. API value: a list such as ["engineering", "data"]. Leave empty for all functions. Values: `engineering`, `data`, `product`, `design`, `sales`, `marketing`, `customer_success`, `operations`, `finance`, `legal`, `people_hr`, `it_security`, `research_science`, `healthcare`, `education`, `manufacturing_trades`, `retail_hospitality`, `other`. |
| `employmentTypes` | `--employment-types` | list |  | Keep only jobs with one of these job types (field employmentTypeNormalized), from the board's job type or the title. Jobs whose type is unknown are left out, and the company's warning says how many. Teamtailor gives no job type and Greenhouse only when the company sets one, so there mostly titles like Intern or Part-time tell. Leave empty for all. Values: `full_time`, `part_time`, `contract`, `temporary`, `internship`, `apprenticeship`, `volunteer`. |
| `maxExperienceYears` | `--max-experience-years` | int |  | Keep only jobs whose description asks for at most this many years of experience, read from phrases like 5+ years or mindestens 3 Jahre. A whole number from 0 to 50, such as 3. Jobs that give no years are left out; the warning says how many. This turns on Include job description (see its price). Leave empty for all. |
| `languages` | `--languages` | list |  | Keep only jobs written in one of these languages, as two-letter codes such as en, de or fr (field language). Greenhouse gives each job's language; elsewhere it is read from the description. This turns on Include job description (see its price). Jobs whose language is unknown are left out; the warning says how many. |
| `location` | `--location` | str |  | Keep only jobs in this place, such as London, California or Germany. A country name or code (DE) keeps jobs in that country; a US state or Canadian province keeps its region. Other text matches whole words, so York keeps New York, not Yorkshire. For several, put one per line; any match keeps a job. In API input, put a line break between values. Leave empty for all. |
| `locationExcludes` | `--location-excludes` | list |  | Leave out jobs in any of these places, matched like Location: India or IN also leaves out jobs in Bangalore, and California leaves out San Mateo, CA. A job with several places is left out when any of them matches. Jobs with no location are kept. A list of up to 100, for example India and Brazil. Leave empty to keep every location. |
| `near` | `--near` | str |  | Keep only jobs within the distance below of one city, such as Berlin or Austin, TX. Add the country or US state to a shared name (Cambridge, UK). Every place of a job counts; do not combine with Remote only. Jobs whose city we do not know (only a country, or a town under 15,000 people) are left out and counted in the warning. An unknown city stops the run free, with close matches. |
| `radiusKm` | `--radius-km` | int | `50` | How far from the city in Near a city a job may be, in kilometers, from 1 to 500. Default 50. Used only with Near a city. |
| `remoteOnly` | `--remote-only / --no-remote-only` | bool | `false` | true: keep only jobs that can be done fully remote. Hybrid and on-site jobs are left out. Default false. |
| `remoteRegions` | `--remote-regions` | list |  | Keep only remote jobs open to one of these places: worldwide, americas, us, canada, latam, emea, europe, uk, apac, or a country code such as DE. Read from the job's location and title, such as Remote (EMEA). A job open worldwide matches every value, and europe keeps a job open in Germany. Remote jobs whose places are unknown are left out and counted in the warning. |
| `workplaceTypes` | `--workplace-types` | list |  | Keep only jobs with one of these workplace types: remote, hybrid or onsite (field workplaceType), from the board's own field or the location text. Jobs whose workplace type is unknown are left out, and the company's warning says how many; Greenhouse marks only remote and hybrid jobs, so its on-site jobs are unknown. Leave empty for all jobs. Values: `remote`, `hybrid`, `onsite`. |
| `hasSalary` | `--has-salary / --no-has-salary` | bool | `false` | true: keep only jobs with a salary (salaryMin or salaryMax), from the board or written in the description. Many boards show pay only in the description. This turns on Include job description (see its price). Default false. |
| `minAnnualSalary` | `--min-annual-salary` | int |  | Keep jobs whose yearly salary (salaryAnnualMax, else salaryAnnualMin) reaches this amount in the currency below, such as 120000. Pay in the description counts too. This turns on Include job description (see its price). Jobs paid in another currency (no exchange rates) or with no yearly salary are left out; the warning says how many. Empty for no minimum. |
| `minAnnualSalaryCurrency` | `--min-annual-salary-currency` | str | `"USD"` | Currency of Minimum yearly salary, as a three-letter code such as USD, EUR or GBP. Only jobs whose salary is in this currency can pass. Used only with Minimum yearly salary. Default USD. |
| `postedSince` | `--posted-since` | str |  | Keep only jobs posted on or after this date. Use a date as YYYY-MM-DD, for example 2026-09-01, or a period as a number plus hours, days, weeks, months or years, for example 24 hours or 7 days. A period counts back from the start of each run, which suits schedules. Jobs whose board gives no posting date are left out. Leave empty for all dates. |
| `postedBefore` | `--posted-before` | str |  | Keep only jobs posted before this date. Use a date as YYYY-MM-DD, for example 2026-06-01, or a period such as 30 days for jobs posted more than 30 days ago. With Posted since it gives a date range. Jobs whose board gives no posting date are left out, and the company's warning says how many. Leave empty for all dates. |
| `visaSponsorship` | `--visa-sponsorship / --no-visa-sponsorship` | bool | `false` | true: keep only jobs whose description says the company sponsors visas. Jobs that do not mention it are left out, and the warning says how many. This reads the description, so it turns on Include job description, also with Rows to return: companies, with its price on JazzHR, Paylocity, Freshteam, JOIN, Polymer, Workday, Eightfold, ClearCompany, GoHire and HiringThing portals. Default false. |
| `ukVisaSponsorOnly` | `--uk-visa-sponsor-only / --no-uk-visa-sponsor-only` | bool | `false` | true: keep only jobs at companies on the UK Home Office register of licensed sponsors for workers (ukVisaSponsor true). The company name must match a register name exactly, once words like Ltd, Limited, PLC and UK are set aside, so a company listed under another legal name is left out, and so is a name too short or too common to match safely. The warning says why. Default false. |

## Output

Every field of a `conserving_celerytop/live-jobs-http-api` result row, read from its published dataset schema. The CSV has the same columns; lists and objects are written as JSON text.

| Field | What it holds |
|---|---|
| `rowType` | job: one job. status: a company with no job rows to return; its job fields are null. On a later onlyNewJobs check, a company whose board was read gets rows only for new, updated or closed jobs, and any other company gets a status row only when its status changed since the previous check; every status is in the COMPANIES record. company: one summary row per company, when outputMode (Rows to return) is companies or both. |
| `company` | The entry as you sent it. |
| `ats` | Job board system, for example greenhouse, lever or ashby. null when the entry was not looked up. |
| `companySlug` | The company's name on its job board. |
| `companyName` | The company name the board gives (Greenhouse boards with open jobs), else for a company from a ready-made list (companyLists) the name the list gives it. null elsewhere. |
| `matchedBy` | How the board was matched: link (you gave the board link), website (found on the company website), directory (a plain name found in our directory of company job boards), name, or name variant (another spelling, such as odys-aviation). A name can belong to another company: then warning says so. null when no board was found. |
| `careerPageSource` | For a company website entry: how its job board was found: homepage link, careers page link, redirect or name match. |
| `boardUrl` | For a company website entry, or a plain name found in the directory: the job board found, also when it is a board we do not read. With outputMode companies or both: the board link you gave, the board found on the website, or the board's usual address for a plain name. |
| `companyStatus` | What happened. Charged: ok (jobs match your filters), no_matching_jobs, no_open_jobs, not_found, source_error (the board failed or did not answer), no_job_board_found (a website we read links no supported job board), internal_error after the job board was read. Not charged: skipped_time_limit, skipped_spending_limit, skipped_client_disconnected, duplicate, invalid_input, unsupported_job_board, website_unavailable, other internal_error. The README lists every status. |
| `charged` | true when this company was charged in this run. Every row of the company has the same value. |
| `chargedEvent` | The charged event: company-lookup (one per company) or new-jobs-check ($0.002). null when not charged. |
| `fetchedAt` | When the lookup started. |
| `warning` | What a delivered company is missing, for example some descriptions. |
| `error` | Why the company has no jobs in the response, when something went wrong. |
| `jobId` | The job's id on its board. |
| `jobKey` | A key for the job that stays the same in every run: board system, board name and job id, such as greenhouse:stripe:7532733 (the job's link where a board gives no id). |
| `requisitionId` | Greenhouse: the company's own requisition id, when it sets one. null elsewhere. |
| `title` | Job title. |
| `department` | Department, as the board names it. |
| `departmentPath` | Department levels joined with " > ". |
| `team` | Team, as the board names it. |
| `location` | Location text. |
| `locations` | When a job lists several places: each location text. |
| `city` | City, spelled as in GeoNames, for example Munich for München. |
| `region` | In the US and Canada: the state or province code, for example CA or ON. |
| `country` | Country name in English, read from the location. |
| `countryCode` | ISO 3166-1 alpha-2 country code, for example DE. null for Remote or EMEA alone. |
| `countryCodes` | Every country code found in the location. |
| `remote` | true when the job can be done fully remote, false for hybrid and on-site jobs. |
| `workplaceType` | remote, hybrid or onsite. |
| `seniority` | Read from the title: intern, entry, mid, senior, staff_principal, lead_manager, director, vp or c_level. |
| `jobFunction` | What the job does, read from the title, then the department and team: engineering, data, product, design, sales, marketing, customer_success, operations, finance, legal, people_hr, it_security, research_science, healthcare, education, manufacturing_trades, retail_hospitality, other. Set on every open job; null only on closed jobs. |
| `employmentType` | In the board's words, for example FullTime. |
| `employmentTypeNormalized` | full_time, part_time, contract, temporary, internship, apprenticeship or volunteer. |
| `language` | ISO 639-1 code of the language the job is written in, such as en or de: Greenhouse's own label, else read from the first 1,500 characters of the description, else from the title. null when unsure. |
| `salaryMin` | Lowest published pay. |
| `salaryMax` | Highest published pay. |
| `salaryCurrency` | Three-letter currency code, for example USD. |
| `salaryPeriod` | year, month, week, day or hour. |
| `salaryAnnualMin` | salaryMin per year: hour x 2,080, day x 260, week x 52, month x 12. null when the period is unknown. |
| `salaryAnnualMax` | salaryMax per year, computed like salaryAnnualMin. |
| `salaryRanges` | Every pay range the job lists, for example one per pay zone or level: from Greenhouse and Ashby pay fields, or from the description (salarySource text). On Greenhouse and from the description, salaryMin to salaryPeriod hold the first one; on Ashby they span the ranges in the first one's currency and period. When one of the currencies is that of the job's country, the main salary uses the ranges in that currency instead. label: the zone or level, or the words before the range in the description. |
| `salarySource` | board when the pay comes from the job board's pay fields; text when it was read from the description (only with a description, and only when the board gives no pay); null without pay. |
| `experienceYearsMin` | Years of experience the description asks for, for example 5 for "5+ years" or "5-7 years". With several, the highest required one. Only with a description. |
| `experienceYearsMax` | Upper end of a range such as "5-7 years", else null. |
| `experienceLevel` | experienceYearsMin as a bucket: 0-2, 2-5, 5-10 or 10+. |
| `educationMin` | Lowest education the description asks for: none (it says no degree is needed), high_school, vocational (apprenticeship, German Ausbildung), associate, bachelor, master or phd. |
| `educationRequired` | false when the description accepts equivalent experience or only prefers the degree; true when it asks for it; null without educationMin. |
| `visaSponsorship` | true when the description says the company sponsors visas, false when it says it does not; null when it says neither. |
| `visaSponsorshipText` | The sentence visaSponsorship was read from, up to 200 characters. |
| `securityClearance` | true when the description asks for a government security clearance (held or obtainable, required or preferred). Otherwise null. |
| `postedAt` | When the job was posted (on some boards: created or last updated). |
| `updatedAt` | When the job was last updated. |
| `applicationDeadline` | Greenhouse: the last day to apply, when the company sets one. null elsewhere. |
| `url` | Link to the job posting. |
| `applyUrl` | Link to the application form. |
| `companyDomain` | The domain of the job's link when it is the company's own website, such as stripe.com for a Greenhouse job shown on stripe.com/jobs. null when the link is on the job board. |
| `description` | The job description, only with includeDescription: plain text, or safe HTML or Markdown with descriptionFormat. Emails, phone numbers and profile links are removed. |
| `tools` | Technologies and business tools named in the title and description, such as Python, Snowflake or Salesforce, in order of first mention, from a list of about 1,400. Words with an everyday meaning (Go, R, Swift, Excel) count only next to other tools or words like programming. The company's own products are left out. null without includeDescription or when the job has no description; [] when it names none. |
| `change` | With onlyNewJobs: new for a job you have not received before, closed for a job you received before that is no longer open (a closed row keeps only jobId, title, url and location). null otherwise. |
| `alertText` | With onlyNewJobs, on a new or closed job: one plain line for an alert in Slack, an email or a sheet, for example "New at Stripe: Senior Data Engineer, Remote (US), USD 180,000 to 240,000 a year". It names the company, then the title, location and pay when known. A closed job has no pay. null otherwise. |
| `changedFields` | With change updated: the fields that changed: title, location, salaryMin, salaryMax, salaryCurrency, salaryPeriod or employmentType. A value the board leaves out this time is not a change. |
| `previous` | With change updated: the earlier value of each title, location and salary field that changed, for example {"salaryMax": 180000}. The earlier job type is not kept. |
| `reposted` | With change new: true when a job with the same title and location closed in the last 30 days (a repost under a new id). null on the first check of a company. With skipReposts, such jobs are left out. |
| `firstSeenAt` | With onlyNewJobs: when this monitor first returned the job. For a job received before this field existed: the last check before it did. |
| `closedAt` | With change closed: the time of the check that found the job gone. |
| `daysOpen` | With change closed: whole days from postedAt or firstSeenAt, whichever is earlier, to closedAt. null when neither is known. |
| `matchedSkills` | With skills: the skills you asked for that this job names, as the tools field names them (golang is Go), in the order you gave them. null without skills. |
| `latitude` | Latitude of the city's center, from GeoNames, to about 1 km (two decimals), for example 52.52 for Berlin. null when the city is not one we know. |
| `longitude` | Longitude of the city's center, like latitude, for example 13.41 for Berlin. |
| `timeZone` | IANA time zone of the city, from GeoNames, for example Europe/Berlin. null when the city is not one we know. |
| `ukVisaSponsor` | true when the company is on the UK Home Office register of licensed sponsors for workers; false when it is not and the job is in the United Kingdom; null for a job elsewhere at a company not on it, and when the name is too short or too common to match safely. The company name must match a register name exactly, once words like Ltd, Limited, PLC and UK are set aside, so false can also mean the company is listed under another legal name. |
| `ukSponsorRoutes` | With ukVisaSponsor true: the routes the company is licensed for, such as Skilled Worker. null otherwise. |
| `remoteRegions` | Where a remote job may be done from, read from its location and title: worldwide, americas, us, canada, latam, emea, europe, uk, apac, or a country code such as DE. [] when the job is not remote or the location does not say, as with a plain "Remote". |
| `openJobs` | Open jobs that pass your filters. |
| `jobsPostedLast7Days` | Of those, jobs posted in the last 7 days. null when the board gives no posting dates (HiringThing, Trakstar Hire, and Freshteam in companies mode). |
| `jobsPostedLast30Days` | Of those, jobs posted in the last 30 days. null when the board gives no posting dates. |
| `jobsOpenOver90Days` | Of those, jobs posted more than 90 days ago. With onlyNewJobs, also jobs this monitor first returned more than 90 days ago. null when a job has no posting date and was not returned that long ago. |
| `newestPostedAt` | Posting date of the newest job. |
| `oldestPostedAt` | Posting date of the oldest job. |
| `remoteJobs` | Jobs that can be done fully remote. |
| `remoteShare` | remoteJobs / openJobs, 0 to 1, two decimals. |
| `engineeringShare` | Share of engineering jobs, by keywords in the title, department and team. |
| `salesShare` | Share of sales jobs, by keywords. A job that is both counts as sales. |
| `salaryCoverage` | Share of jobs with a published salary. |
| `medianSalaryMin` | Median salaryMin of the currency and pay period with the most jobs (at least 3 jobs). |
| `medianSalaryMax` | Median salaryMax of that currency and pay period. |
| `medianSalaryCurrency` | Currency of the medians. |
| `medianSalaryPeriod` | Pay period of the medians. |
| `salaryMedians` | Medians for every currency and pay period with at least 3 jobs. |
| `topDepartments` | Up to 5 departments with the most jobs (top level of the department path). |
| `topLocations` | Up to 5 location texts with the most jobs. |
| `countries` | Up to 10 countries with the most jobs. A job in several countries counts in each. null when no job has a country. |
| `seniorityCounts` | Jobs per seniority level, for example {"senior": 12, "entry": 3}. |
| `functionCounts` | Jobs per job function (the jobFunction field), for example {"engineering": 40, "sales": 12}. engineeringShare and salesShare use simpler keyword rules. |
| `functionCountsLast30Days` | Jobs posted in the last 30 days per job function, for example {"engineering": 9, "sales": 4}. Same dates as jobsPostedLast30Days: {} when none was posted then, null when the board gives no posting dates. |
| `leadershipRoles` | Up to 5 open director, VP and C-level jobs (the seniority field), newest first. Account director titles are left out. With onlyNewJobs, such jobs that closed since the previous check follow the open ones, with status closed. [] when there are none. |
| `firstHireRoles` | Up to 5 jobs that are a first or founding hire, newest first. cue is title when the title says Founding or first hire, and text when the description says the job is a first hire, a founding member of a team, or builds a team or function from scratch (only with includeDescription). [] when there are none. |
| `topTools` | With includeDescription: up to 15 tools named in the most jobs, each job counted once, with the tool's category (language, cloud, crm_sales...). null without descriptions. |
| `toolCoverage` | With includeDescription: share of jobs with a description that name at least one tool, 0 to 1. null without descriptions. |
| `visaSponsorshipShare` | Share of jobs with a description that say the company sponsors visas, 0 to 1. null without descriptions. |
| `medianExperienceYearsMin` | Median experienceYearsMin of the jobs whose description gives years of experience. null without descriptions. |
| `newJobs` | With onlyNewJobs: new jobs since the previous check. |
| `closedJobs` | With onlyNewJobs: jobs closed since the previous check. |
| `updatedJobs` | With onlyNewJobs: jobs received before whose title, location, salary or job type changed since the previous check, also without includeUpdatedJobs. |
| `repostedJobs` | With onlyNewJobs: new jobs with the title and location of a job that closed in the last 30 days. With skipReposts they are not new jobs: see skippedReposts. |
| `medianDaysOpen` | With onlyNewJobs: median daysOpen of the jobs that closed since the previous check. null when none closed. |
| `previousCheckAt` | With onlyNewJobs: time of the previous check. |
| `newFunctions` | With onlyNewJobs: job functions (jobFunction values, not other) that have open jobs passing your filters now and had none at the previous check, for example ["sales"]. [] when there is none. null on a first check, when the board was read only in part or listed no jobs at all, when the previous check was made before this field existed, and once after we change how job functions are read. |
| `newCountries` | With onlyNewJobs: countries, as ISO 3166-1 alpha-2 codes, where the company has open jobs passing your filters now and had none at the previous check, for example ["JP"]. A job in several countries counts in each, and jobs with no country, such as Remote alone, are left out. [] when there is none. null on a first check, when the board was read only in part or listed no jobs at all, and when the previous check was made before this field existed. |
| `skippedReposts` | With onlyNewJobs and skipReposts: reposted jobs left out, which newJobs and repostedJobs do not count. null without skipReposts. |
| `companyIndustry` | For a company from the ready-made lists (companyLists): its industry, one of ai, fintech, security, developer-tools, healthtech, e-commerce, marketplace, saas, hardware, climate, crypto, gaming, media, education, mobility or other, from Wikidata. null when not known, and for other companies. |
| `companyCountry` | For a company from the ready-made lists: the two-letter code of the country of its headquarters, such as US or DE, from Wikidata. null when not known, and for other companies. |
| `companySizeBand` | For a company from the ready-made lists: its number of employees as a band, 1-50, 51-200, 201-1000, 1001-5000 or 5000+, from the latest count in Wikidata. null when not known, and for other companies. |
