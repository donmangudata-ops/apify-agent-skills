# apify-agent-skills

Agent Skills (SKILL.md folders) that let Claude, Codex, Cursor and other AI agents run data tools on Apify: job boards, hiring signals, H-1B salaries, company registries, domains and DNS, web pages to Markdown, articles and feeds, screenshots, podcasts and transcription, and images. One skill per Actor.

They follow the open Agent Skills format, so they work in Claude Code, claude.ai (uploaded skills), Codex, Cursor, OpenCode and any agent that reads SKILL.md. The skills are free and MIT licensed. The data comes from paid Actors built and published by Don Mangu, the author of these skills, which run on your own Apify account with your own token. Every script prints the price ceiling from live prices before it runs and sets a hard spending cap.

25 skills.

## Jobs and hiring data

| Skill | Ask your agent | Billed per |
|---|---|---|
| [software-engineer-jobs](skills/software-engineer-jobs/SKILL.md) | "Find remote senior backend engineer jobs that use Go, posted this week, paying at least $150k." | matching job |
| [ai-jobs-search](skills/ai-jobs-search/SKILL.md) | "Find machine learning engineer jobs at AI startups posted in the last 7 days, remote or in New York." | matching job |
| [company-hiring-signals](skills/company-hiring-signals/SKILL.md) | "Which of these 200 accounts are hiring sales people right now? Rank them." | company |
| [ashby-jobs-api](skills/ashby-jobs-api/SKILL.md) | "List every open engineering job at Linear and Ashby on Ashby, with salary where published." | company |
| [greenhouse-jobs-api](skills/greenhouse-jobs-api/SKILL.md) | "List every open engineering job at Dropbox and Stripe on Greenhouse, with salary where published." | company |
| [lever-jobs-api](skills/lever-jobs-api/SKILL.md) | "List every open engineering job at Outreach and Nium on Lever, with salary where published." | company |
| [workday-jobs-api](skills/workday-jobs-api/SKILL.md) | "List every open engineering job at Intel and Adobe on Workday, with salary where published." | company |
| [live-jobs-http-api](skills/live-jobs-http-api/SKILL.md) | "Are Databricks, OpenAI and Linear hiring engineers this week?" | company |
| [jobs-mcp-server](skills/jobs-mcp-server/SKILL.md) | "List the open engineering jobs at Stripe and Palantir." | tool call |
| [h1b-perm-salary-data](skills/h1b-perm-salary-data/SKILL.md) | "What do H-1B software engineers earn at Microsoft in Washington? Give me the median and range." | row |

## Companies, domains and SEO

| Skill | Ask your agent | Billed per |
|---|---|---|
| [company-name-to-domain](skills/company-name-to-domain/SKILL.md) | "Here are 300 company names from a trade show list. Find each one's website." | domain found |
| [open-company-registries](skills/open-company-registries/SKILL.md) | "Is this Norwegian supplier active, and what is its org number and LEI?" | company |
| [domain-authority-checker](skills/domain-authority-checker/SKILL.md) | "Score these 500 guest post sites by domain authority and drop anything under 30." | domain |
| [dns-lookup](skills/dns-lookup/SKILL.md) | "Which of these 2,000 lead domains have no MX record?" | domain |
| [sitemap-url-extractor](skills/sitemap-url-extractor/SKILL.md) | "Get every blog post URL on competitor.com with its last updated date." | URL |

## Web content for AI

| Skill | Ask your agent | Billed per |
|---|---|---|
| [web-page-to-markdown](skills/web-page-to-markdown/SKILL.md) | "Turn every page of our help center into Markdown for a RAG index." | page |
| [article-extractor](skills/article-extractor/SKILL.md) | "Get the full text of every article this publication posted this week and summarize them." | article |
| [rss-feed-reader](skills/rss-feed-reader/SKILL.md) | "Give me everything these 20 industry blogs published in the last 24 hours." | item |
| [website-screenshot-api](skills/website-screenshot-api/SKILL.md) | "Screenshot the pricing pages of these 12 competitors, full page." | capture |
| [crossref-works-search](skills/crossref-works-search/SKILL.md) | "Find the 30 most cited papers on retrieval augmented generation since 2023." | work |

## Audio and podcasts

| Skill | Ask your agent | Billed per |
|---|---|---|
| [audio-podcast-transcription](skills/audio-podcast-transcription/SKILL.md) | "Transcribe the last three episodes of this podcast feed and give me show notes." | audio minute |
| [podcast-episode-scraper](skills/podcast-episode-scraper/SKILL.md) | "List every episode of these five podcasts from the last month with audio links." | episode |

## Images

| Skill | Ask your agent | Billed per |
|---|---|---|
| [image-converter-compressor](skills/image-converter-compressor/SKILL.md) | "Convert all the product photos in this list to WebP under 200 KB each." | image |
| [ai-image-upscaler](skills/ai-image-upscaler/SKILL.md) | "Upscale these 40 product thumbnails to 4x for print." | image |
| [image-to-text-ocr](skills/image-to-text-ocr/SKILL.md) | "Pull the text out of these 50 receipt photos so I can log the totals." | image |

## Covered in hiring-signals-skills

These Actors already ship inside the multi-Actor skills of https://github.com/donmangudata-ops/hiring-signals-skills:

- `live-career-page-jobs-api`: used by account-research, hiring-signals, competitor-hiring-tracker, tech-job-search
- `tech-jobs-search`: used by tech-job-search
- `website-tech-stack-detector`: used by account-research, hiring-signals

## Install

Claude Code: copy a skill folder into `~/.claude/skills/` (all projects) or `.claude/skills/` (one project). claude.ai: zip one skill folder and upload it under Settings, Capabilities, Skills. Other agents: point them at `skills/<name>/SKILL.md`, or use `npx skills add <repo> -s <name>`.

## Setup

1. A free Apify account. 2. An API token from Apify Console, Settings, API & Integrations, set as `APIFY_TOKEN` in the environment. Never write it into a file, a URL or a chat. 3. Python 3.9 or newer; the scripts use the standard library only.

## How each skill is built

- `SKILL.md`: when to use it (in the description, which the agent always sees), cost and disclosure, workflow, commands, output and limits. Under 100 lines.
- `run.py`: starts the Actor through the Apify API with a hard spending cap, waits, and writes `<out>.json` and a formula-safe `<out>.csv`. Prices are read live, never hardcoded.
- `reference.md`: every input flag (`#input`) and output field (`#output`), read from the Actor's published schemas, loaded only when needed.

Each skill folder is flat (`SKILL.md`, `run.py`, `reference.md`), with no subfolders.

Check all skills with `python validate_skills.py`. A blank skill to copy is in `skills/_template/`.

## License

MIT. Not affiliated with or endorsed by any of the job boards, registers or websites named.
