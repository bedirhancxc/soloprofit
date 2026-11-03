# SoloProfit — free business calculators

**Live website:** [Use SoloProfit's free business calculators](https://bedirhancxc.github.io/soloprofit/)

SoloProfit provides free, browser-based tools for freelancers, creators and small business owners. Enter your own assumptions to estimate pricing, profit margins and the sales or subscribers needed to cover expenses. No signup is required, and calculations happen locally in your browser.

## Available calculators

- [Freelance hourly rate calculator](https://bedirhancxc.github.io/soloprofit/freelance-hourly-rate/) — turn a yearly income target and business expenses into a billable hourly rate.
- [Profit margin calculator](https://bedirhancxc.github.io/soloprofit/profit-margin/) — determine the share of revenue remaining after costs.
- [Subscription break-even calculator](https://bedirhancxc.github.io/soloprofit/subscription-break-even/) — estimate how many active paying subscribers cover recurring expenses.
- [Markup calculator](https://bedirhancxc.github.io/soloprofit/markup-calculator/) — calculate selling price and gross margin from unit cost and markup.
- [Business break-even calculator](https://bedirhancxc.github.io/soloprofit/break-even-calculator/) — estimate units and sales revenue needed to cover fixed costs.

The [homepage](https://bedirhancxc.github.io/soloprofit/) also contains quick calculators for project pricing, subscription revenue and profit targets.

## Publishing and tests

The repository is a static HTML/CSS/JavaScript website deployed on GitHub Pages through GitHub Actions. The workflow validates the site, runs calculator regression tests and checks publicly published files. There is no database, API key or payment requirement.

To check the files locally:

```bash
python3 scripts/check_site.py
node scripts/check_inline_scripts.js
node scripts/test_existing_calculators.js
node scripts/test_home_calculators.js
node scripts/test_markup.js
node scripts/test_break_even.js
```

For exact behavior and limitations of each calculation, consult the corresponding page. All monetary estimates are illustrative, not legal, tax or financial advice.

**Private traffic analytics:** All six SoloProfit calculator pages now include a shared, privacy-focused PostHog loader in `assets/analytics.js`. It is **inactive until the site owner's public `phc_...` project token is configured**, and makes no analytics requests while inactive. No public visit count, leaderboard or dashboard is shown.

To activate it for this GitHub Pages site, the site owner must set two **GitHub Actions repository variables** (Settings > Secrets and variables > Actions > Variables): `POSTHOG_PROJECT_TOKEN` (the **public** `phc_...` token from PostHog Project Settings) and `POSTHOG_API_HOST` (the exact project's ingestion host, `https://us.i.posthog.com` or `https://eu.i.posthog.com`). In PostHog Project Settings > Web analytics, enable **Cookieless server hash mode**. Trigger the `Test and Deploy SoloProfit` workflow with **Run workflow** (or push a new commit). The GitHub Pages build then generates `assets/analytics-config.js` from these deployment variables. It remains absent from the GitHub source repository, and is safely inert if variables are unset. Confirm that a real pageview subsequently arrives in the private PostHog project. Never add a personal `phx_...` API key, password, or other secrets to repository code or browser variables.

Only a sanitized page path and referring domain are intentionally captured; interactive forms, calculator numbers, surveys, and session replay are excluded. The site footer discloses cookieless analytics without displaying visitor figures. Daily unique-user metrics are approximate and may include some undetected bots. Site visitors cannot see the private PostHog dashboard; the site owner can authorize ChatGPT to read traffic results using the PostHog connection.

GitHub Actions tests are **not** human visitors, and Search Console measures only Google Search visibility.
