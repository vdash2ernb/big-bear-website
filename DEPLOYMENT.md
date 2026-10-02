# Launch preparation — keep the domain, replace the website

The local redesign is not published. Domain registration can remain where it is while a new static host serves the website. Hosting and registrar changes are separate decisions. Provider-specific instructions should be checked against the chosen provider's current documentation when it is selected.

## Before choosing a launch date

- Approve the logo quality, proposed service scope and process, business hours, phone, photography, and final copy.
- Confirm the actual service territory. Add only verified cities; do not publish the example city list as a factual coverage claim.
- Supply genuine reviews and project locations if those should be visible at launch.
- Choose and connect the inquiry destination using `DEVELOPMENT.md`, or explicitly choose a phone-only launch and remove the preview form.
- Review privacy text for the actual services collecting data. The current form makes no network requests and the site has no analytics.
- Obtain the current URL inventory and DNS records from the owner. The public navigation review found Home and Contact, but it is not a complete historical URL inventory. Sitemap/robots retrieval was unavailable through the research tool; verify them independently during migration planning.

## Prepare a staging version

1. Choose hosting that serves static HTML/CSS/JS and supports HTTPS, custom domains, redirects, and a form backend if needed.
2. Upload only the contents of `dist` to a private/protected staging location. Do not upload source notes, tools, credentials, or `source-assets`.
3. Keep `noindex, nofollow` on staging pages. It discourages search indexing; it does not make a site private. Use real staging access protection when privacy matters.
4. Confirm all twelve pages, relative asset paths, phone links, keyboard interactions, mobile layouts, and the quote flow on the actual host.
5. Choose the final URL policy. Current output uses explicit `.html` paths with `https://bigbearautomaticgates.com/` as the home canonical.

## Redirect plan

Configure server/host redirects, not JavaScript redirects:

| Existing or alternate path | Destination | Status |
| --- | --- | --- |
| `/contact` and `/contact/` | `/contact.html` | 301 |
| `/index.html` | `/` | 301 |
| HTTP scheme | HTTPS equivalent | 301 or 308 |
| `www` alternate hostname, if used | Chosen apex hostname | 301 or 308 |

Confirm that the host's extension-cleaning behavior does not redirect `.html` back to extensionless paths and create a loop. Extend the map with real historical URLs. Never redirect every missing page to the homepage; provide a host-level 404 response for genuinely missing content.

## Prepare production files

After content and lead delivery are approved, run:

```powershell
python tools/build_site.py --production
python tools/verify_site.py
```

This removes draft noindex tags and adds the sitemap URL to `robots.txt`. It does not deploy anything. The default renderer command recreates a noindex draft, so deliberately choose production mode for the launch artifact. The canonical domain must be updated in `tools/build_site.py` first if the approved production hostname changes.

Upload only `dist` contents. Configure useful caching for images and styles, and validate HTML freshness after updates. Recheck the deployed canonical tags, sitemap, robots file, redirects, and actual page status codes. Structured data preparation does not guarantee rich results.

## Domain switch

1. Export the original DNS zone and record the old hosting targets. Back up the old site's content, files where available, and URL structure.
2. Add the existing domain to the new host and complete its verification and HTTPS setup as directed.
3. Change only the web-serving records required by the selected host. Preserve MX, SPF, DKIM, DMARC, verification records, and unrelated subdomains. Avoid an unnecessary nameserver change.
4. Keep the old hosting account active through the transition and rollback period.
5. Verify HTTPS on the apex and `www`, forms, business email, redirects, and the production sitemap after DNS resolves to the new host. Submit the sitemap in the owner's Search Console account and monitor indexing and broken URLs.

No domain registration transfer is required by this plan. Do not cancel GoDaddy hosting until the owner confirms that the new website and business email are functioning.

## Rollback

Retain the prior website and DNS values. If launch verification fails, restore the previous web DNS records or host version, depending on the failure. DNS rollback is not instantaneous because caches may retain prior values. Keep inquiry channels working during recovery and account for any requests received by either system.
