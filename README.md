# Big Bear Automatic Gates — custom website

A 12-page HTML/CSS/JavaScript redesign with charcoal, steel, white, bronze accents, real project photography, and responsive layouts. Everything remains local.

## Preview

Open http://127.0.0.1:5500/ while the preview runs. Double-click `start-preview.cmd` to start it again. The preview uses Python already installed on this computer. No website framework or package installation is required.

## Website pages

- Home, About, Services, Gallery, FAQ, Contact.
- Six service pages: automatic gates, gate openers, access control, commercial gates, security integration, and repair/maintenance.
- Shared mobile navigation, persistent mobile call/quote buttons, nine FAQs, and a six-photo gallery.
- Quote form with validation and an explicit local-preview result. A CRM/server connection is still needed for real delivery.
- Review component ready for genuine reviews; hidden while no approved reviews are configured.

## Project structure

```text
big-bear-website/
  dist/                       Public website files
    index.html
    about.html
    services.html
    gallery.html
    contact.html
    faq.html
    services/                 Six service detail pages
    css/styles.css            Shared visual styles
    js/main.js                Navigation, form, review rendering
    js/config.js              Public integration configuration
    images/                   Responsive WebP photography
    assets/gate.jpeg          Original starter photograph
    sitemap.xml
    robots.txt
  tools/
    build_site.py             Shared layout and page renderer
    content.py                Service, FAQ, and project copy
    prepare_images.py         Responsive image preparation
    verify_site.py            Static checks
  source-assets/              Original project photographs
  start-preview.cmd
  DEVELOPMENT.md
  PROJECT-PLAN.md
  CONTENT-NOTES.md
  DEPLOYMENT.md
```

## Editing

Edit `dist/css/styles.css` for the design and `dist/js/main.js` for behavior. Edit `tools/content.py` for reusable copy or `tools/build_site.py` for page layouts, then run `python tools/build_site.py`. Save and refresh the preview. Direct edits to generated HTML are overwritten by that renderer.

For the full workflow, read `DEVELOPMENT.md`. The browser serves ordinary static files; Python is only a local authoring/preview helper. The website can be hosted on any suitable static host.

## Review and launch

`PROJECT-PLAN.md` records the public site audit, sitemap, wireframe, design choices, SEO preparation, and phased implementation. `CONTENT-NOTES.md` records factual limits and image sources. `DEPLOYMENT.md` explains staging, form integration, domain retention, redirects, and rollback.

The draft has noindex tags and is not ready for public lead collection. Confirm the service territory, logo quality, approved copy, review evidence, image rights, and inquiry destination before launch. No live website or DNS change has been made.
