# Big Bear — audit, sitemap, and design plan

## Phase 1 — current public site audit

Reviewed September 11, 2026: the public homepage and contact page, plus the rendered homepage gallery. This is a public-facing content/design assessment, not an account audit, analytics analysis, or measured ranking report. GoDaddy/Airo editing constraints are reported in the client brief; the hosting account has not been inspected.

| Observation | Effect | Rebuild response |
| --- | --- | --- |
| The homepage search result title is “Top Security Camera Systems for Your Property,” while the headline emphasizes vehicle gates. | The title does not clearly express the company's primary gate positioning. | Distinct gate-focused page titles and descriptions. |
| Public navigation exposes Home and Contact; no dedicated service pages were found in that navigation. | Visitors have little service-specific information to evaluate. | Six substantive service detail pages and a services overview. |
| Extracted homepage content is brief and emphasizes a general headline, about heading, and image gallery. | Craftsmanship, project process, and common buying questions are underexplained. | Clear service cards, positioning, process, and FAQs. |
| The existing contact form exposes name and email in the public extraction. | Lead qualification may require additional follow-up. | Quote fields for phone, property location, service, and project details. |
| Existing project photographs are valuable but lack verified installation locations in the material reviewed. | They can demonstrate actual work, but cannot responsibly support invented local case studies. | Real-photo gallery with descriptive captions; locations await confirmation. |
| No verified customer review dataset was supplied or established. | Review claims would be unsupported. | A styled review component prepared but hidden until real reviews are approved. |
| LaBelle address and phone are public; wider service territory is unconfirmed. | City-specific claims could be inaccurate. | LaBelle-focused copy and availability wording instead of invented city coverage. |

Source pages: [Homepage](https://bigbearautomaticgates.com/) and [Contact](https://bigbearautomaticgates.com/contact). Search extraction for Contact was approximately three months old; confirm hours, number, and service scope with the client before launch. The rendered gallery was inspected directly for image selection. No unsupported license, insurance, review-score, warranty, response-time, or experience claims are included.

## Phase 2 — sitemap and wireframe

```text
Home
├── Services
│   ├── Automatic Gate Installation
│   ├── Gate Openers & Operators
│   ├── Access Control Systems
│   ├── Commercial Gate Systems
│   ├── Security Integration
│   └── Gate Repair & Maintenance
├── Our Work / Gallery
├── About Us
├── FAQs
└── Contact / Quote
```

Homepage wireframe, top to bottom:

```text
Slim local identity / phone strip
White wordmark + navigation + bronze quote button
Full-width entrance photograph with dark overlay
  Strong headline / short copy / quote and call buttons
Brand values strip
Six service cards with real photographs
Dark craftsmanship / company positioning section
Three featured project photographs
Five-step process
Verified reviews (hidden until supplied)
LaBelle location / coverage confirmation
Five expandable FAQs
Quote form beside direct phone contact
Four-column footer
Mobile-only persistent call / quote bar
```

Internal page layouts:

- Services: introductory heading, six photo cards, quote prompt.
- Service detail: title, image, specific guidance, four assessment topics, next-step CTA.
- Gallery: six photographs with truthful descriptive captions; no invented locations.
- About: positioning, real photography, proposed project process.
- FAQ: nine keyboard-operable native accordions.
- Contact: phone, location, hours, full quote form.

## Phases 3 and 4 — implementation

Twelve standalone HTML pages share one stylesheet and a small JavaScript file. A Python authoring helper keeps headers, footers, and reusable sections consistent; the website runs without Python or a build service on its production host. Existing project directory and preview address are retained.

Visual decisions: charcoal #191c1d; steel #51585b; white; light neutral #f3f3f0; bronze #c5a16b. A locally available Segoe UI/Arial stack avoids external font requests. Large architectural headings, restrained 4–6px radii, fine borders, and generous spacing set the tone. No stock imagery, decorative illustrations, certification seals, or aggressive sales copy.

The client-supplied copper-and-steel BB/bear identity supersedes the blue bear artwork. The header and footer use the new emblem and horizontal wordmark; the favicon uses the emblem. The current palette is charcoal #2b2b2b, copper #b87333, steel gray, and warm white #f7f5ef. Service descriptions and process steps are proposed copy based on the brief and require client review before publication.

## Phase 5 — SEO and performance

- Unique title and description, one H1, canonical production URL, semantic sections, and navigation on every page.
- LocalBusiness and WebPage JSON-LD; BreadcrumbList on internal pages; Service markup on service detail pages; FAQPage only where answers are visible.
- Business data limited to known contact facts. No aggregate ratings, fictional street address, unconfirmed territory, or keyword-stuffed city pages.
- Responsive 640/960/1600 image variants, WebP compression, lazy loading below the hero, explicit image dimensions, and system fonts.
- Draft pages retain `noindex, nofollow`. A sitemap is prepared for the production domain. Metadata is preparation, not a promise of search rankings or rich-result eligibility.
- Native FAQ accordions, labeled form fields, visible keyboard focus, reduced-motion support, responsive menu, and persistent mobile contact controls.

Guidance checked: [Google title links](https://developers.google.com/search/docs/appearance/title-link), [LocalBusiness structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business), and [noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing). LocalBusiness rich-result requirements may need more verified address detail; no street address is fabricated. FAQ markup does not promise Google FAQ rich results.

## Phase 6 — launch preparation

See `DEPLOYMENT.md` for domain migration, static hosting, redirects, form integration, launch verification, and rollback. No website publishing or DNS change has been performed.
