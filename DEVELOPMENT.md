# Local editing and integration

## Start the preview

Double-click `start-preview.cmd`, or open a terminal in this project and run:

```powershell
python -m http.server 5500 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:5500/. Keep the terminal running; Ctrl+C stops it. Reuse an existing server rather than starting a second instance. If another application owns port 5500, use a different port in both the command and browser address.

## Source of truth

| Change | Edit | Next step |
| --- | --- | --- |
| Colors, fonts, spacing, responsive layout | `dist/css/styles.css` | Save and refresh |
| Menu, form behavior, review rendering | `dist/js/main.js` | Save and refresh |
| Review data / future form configuration | `dist/js/config.js` | Save and refresh |
| Service copy, FAQ answers, gallery captions | `tools/content.py` | Run the page renderer |
| Header, footer, homepage, internal layouts | `tools/build_site.py` | Run the page renderer |
| Project photos | `source-assets/` and image helper | Generate responsive copies, then review |

```powershell
python tools/build_site.py
python tools/verify_site.py
node --check dist/js/main.js
```

The renderer creates 12 ordinary HTML files in `dist`; no server-side Python is needed to host them. CSS and JavaScript are not generated. You can directly edit a generated HTML file for a quick experiment, but a later renderer run overwrites that experiment. Put durable content changes in the files listed above. Keep the existing project name and `dist` layout when continuing this task.

The original gate JPEG is retained under `dist/assets` from the first starter. New source photographs are outside the public directory. `tools/prepare_images.py` uses Pillow to produce optimized variants; routine text/style changes need only standard Python. The bundled image-processing Python used in this workspace is available through Codex's workspace dependencies.

## Quote form status

The current form is a local preview. Required-field and email validation work, and a valid request produces an explicit “Nothing has been sent” result. No data is written to browser storage or transmitted in this configuration. A click-to-call option is available throughout.

No CRM account, email inbox, webhook, or recipient address has been chosen. `quoteEndpoint` and `privacyUrl` remain null. Live submission mode activates only for a configured same-origin HTTPS endpoint and a same-origin privacy URL. The preview Python server cannot receive quote submissions.

For a future HubSpot or GoHighLevel integration:

1. Choose the CRM account and destination pipeline/form. Establish the approved privacy notice and contact purpose.
2. Implement a same-origin server endpoint such as `/api/quote`. Store CRM tokens in the hosting provider's server environment, never in HTML or `config.js`.
3. Validate lengths, required fields, email/phone, consent, service values, and request origin server-side. Add spam protection, rate limiting, safe logs, and durable submission/duplicate handling as appropriate. The client honeypot is only an additional signal.
4. Map the fields into the selected CRM. Decide what constitutes acceptance: confirmed CRM delivery or a durable queue with retries and operational monitoring.
5. Return JSON only after acceptance is established. The frontend expects an HTTP success response with `{"accepted":true,"requestId":"non-empty-receipt-id"}`. Other outcomes, malformed JSON, or a 15-second timeout display an unconfirmed-delivery message and retain fields.
6. Test success, validation failure, CRM failure, rate limiting, timeout, and retries on a staging endpoint with test data. The live network branches have not been integration-tested against a backend.
7. Set `quoteEndpoint` and `privacyUrl` only after the endpoint and notice are ready. Verify that the preview notice is replaced, submissions arrive, and the receipt shown reflects the backend result.

Payload fields: `name`, `phone`, `email`, `location`, `service`, `message`, `consent` (boolean), `website` (honeypot), and `sourcePage`. Client validation is not a security boundary. Do not point the public browser directly at a secret-bearing CRM webhook.

## Reviews and project evidence

The review section is styled and hidden when `reviews` is empty. Add client-approved real review objects with `name`, `text`, integer `rating` from 1 to 5, and an HTTPS `sourceUrl`. Review text is inserted as text, not HTML. No aggregate rating schema is emitted. A future Google Reviews integration still needs an authorized source and its applicable display rules.

Gallery captions currently describe visible photographs. Confirm project names, locations, ownership, and installation scope before converting them to case studies. Never fill missing reviews, license badges, or project locations with realistic-looking invented data.

## Verification workflow

The static checker covers all 12 pages, link targets, anchors, local images and scripts, unique titles/descriptions, one H1 per page, and parseable JSON-LD. Browser checks covered all routes, desktop and narrow layouts, menu opening/Escape, the FAQ accordion, and the required-field/valid-preview form states. No public deployment, real CRM delivery, or search-ranking outcome was tested.
