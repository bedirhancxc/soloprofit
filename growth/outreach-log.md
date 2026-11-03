# SoloProfit growth and outreach log

**Goal:** earn genuine, relevant human visitors to the existing SoloProfit calculators, not bot hits. Long-term milestone: 1,000 verified visits per 30 days, then grow further.

**Measurement:** Private PostHog loader exists at `assets/analytics.js`, but the public project token remains empty as of 2026-11-03. A live trusted human-visitor count is **not available**. Search Console previously showed 0 impressions and 0 Google clicks as reported by site owner. GitHub Actions fetches and API checks are **not visits**. LaunchAgentic directory last showed **1 tracked website redirect click** and 0 agent visits (2026-11-03); this does *not* demonstrate a page was loaded by a human.

## Existing outreach — do NOT submit again to these services

| Channel | Last known status on 2026-11-03 | Evidence or comments |
| --- | --- | --- |
| TechTools Launchpad | Public listing confirmed | Public tool ID 7097 |
| PromoteIndex | API accepted | Slug `soloprofit`; public stats rate limited |
| LaunchAgentic | Public listing confirmed | https://launchagentic.space/p/soloprofit; 1 tracked redirect click was observed |
| Zearches | Public listing confirmed | Software & SaaS Tools directory category |
| The Tool Directory | Submission accepted, editorial decision pending | Human-reviewed free standard listing |
| The Free Tools Directory | Submission endpoint accepted, editorial decision pending | GitHub Actions run 41627658033 returned HTTP 200; no approval inferred |
| MeWebLink | Attempt failed with HTTP 422 | Do not retry automatically |
| QuestStack | Attempt failed with HTTP 429 | Honor rate/submission limits; do not retry automatically |
| FlowPath | Relevant tool-review email sent | No reply verified |
| Fr. Tools | Relevant tool-review email sent | No reply verified |
| Calculators Cloud | Free editorial article pitch sent (markup vs. margin) | Pending editorial response; no follow-up spam |
| EpicTools | Direct editorial submission email sent 2026-11-03 | Official editor invitation at https://epictools.dev/submit; no listing approval or website visit confirmed |
| Linkrena | Free launch API returned HTTP 401 on 2026-11-03 | Official site advertised account-free listing, but endpoint required sign-in. No retry or bypass; no public listing |
| NoUploadTools | Investigated, not submitted | Official tool submit form requires Cloudflare Turnstile challenge; do not bypass. |

## Autonomous agent coordination

- Agent 1 SEO: search indexing and long-tail relevance of **existing six indexed pages**.
- Agent 2 Discovery: at most **one good-fit free submission per hour and two per day**, never duplicate a row above; verify actual live listing separately.
- Agent 3 UX: prioritize first-result ease of use, not endless cosmetic changes.
- Agent 4 Editorial partnerships: at most **one targeted invited editorial pitch per day**; avoid prior contacts and avoid reciprocal/pay-for-link deals.
- Agent 5 Measurement: independent audit of real site visits vs listing, API view and redirect click; stop guessing until private analytics is activated.

Do not add new calculator pages, buy traffic, generate artificial visits or reviews, or automate unsolicited bulk email. Keep private contacts, account tokens, personal API keys and visitor logs out of this public GitHub repository.

## Next meaningful checkpoints

1. Verify whether The Free Tools Directory and The Tool Directory actually publish SoloProfit, without creating artificial clicks.
2. Use only permissioned, relevant communities/resource editors for new discovery.
3. When PostHog is connected and a **public** project token activated, privately report daily estimated unique visitors and source breakdown; clearly flag bots and data limitations.
4. Evaluate search indexing in the owner's Search Console; a live HTTP 200 and sitemap alone do not prove indexing or ranking.

**Repository discovery audit (2026-11-03):** GitHub repository metadata had empty description, homepage URL, topic tags, and no OSI license; the connected GitHub integration cannot directly change repository settings. Do not mislabel the repository open source until the owner chooses a license. This limits discovery in GitHub search and eligibility for some curated open-source directories.
