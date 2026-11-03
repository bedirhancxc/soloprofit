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

**Traffic and analytics:** This repository's GitHub Actions runs are publication and availability checks, **not website visitor counts**. Google Search Console reports only Google Search visibility; full-site analytics have not been configured.
