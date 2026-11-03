# ChangeOrder Studio — MVP v1

An offline-first, no-signup change order generator and lightweight scope-change tracker for freelancers, agencies, and consultants. This is a **free product prototype**, not a paid SaaS yet.

## What works

- Create a live, printable change order from project and change request details.
- Hourly calculations or a fixed extra fee override; USD/EUR/GBP/TRY/CAD/AUD.
- Track requests as Draft, Sent, Approved or Declined, with currency-aware totals.
- Save records in browser `localStorage`; JSON export/import; delete individual/all records.
- Copy an approval request message; print or save the document as PDF from a browser.
- Responsive mobile/desktop interface; keyboard accessible labels and status.

## Privacy and limitations

- **No back end**, no analytics, no third-party scripts or outbound network calls.
- Local data will vanish if the browser data is cleared, or will not follow users to other devices. Export a backup frequently.
- Marking a request as Approved is not a client-verified approval or e-signature.
- No online sharing links, payment collection, customer accounts, email sending, subscription entitlement or server-side validation exist.
- The quoted fee is a *proposal*, not a guarantee of recovery or legal enforceability. Adapt the document to the governing contract and law.
- Printed copy is a change order, not an invoice.

## Run

Open `index.html` in a modern browser, or use `python3 -m http.server 8000` from this directory and open `http://localhost:8000/`.

## Launch checklist

1. Run browser checks and accessibility checks on desktop + mobile.
2. Put this project in its **own** public GitHub repository. Enable GitHub Pages or another static hosting service. Do **not** merge it into SoloProfit's live site.
3. Add verified search engine indexing and a real canonical URL only after the live URL is known.
4. Share a useful free tool organically without automated spam. Measure voluntary usage with a consent-respecting approach.
5. Validate repeat usage, user interviews and conversion intent before selecting a paid tier.
6. Payment provider onboarding, KYC, tax registration and external billable services require the account owner's setup/approval; never silently open paid accounts.

## Monetization hypothesis (not enabled)

Offer the core creator and tracker for free; once demand is demonstrated, consider paid team features such as authenticated client approvals, synchronized projects, customizable branding and hosted client links. Do not advertise paid features before they exist. The initial goal is real user value, not invented traffic or revenue.