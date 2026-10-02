"""Render shared layout and content as ordinary, dependency-free HTML files.

Run `python tools/build_site.py` after editing this file or content.py.
CSS/JS are authored directly in dist and are never overwritten here.
"""
from pathlib import Path
from html import escape as esc
import json
import argparse
from content import SERVICES, FAQS, PROJECTS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
DOMAIN = 'https://bigbearautomaticgates.com'
parser = argparse.ArgumentParser()
parser.add_argument('--homepage-only', action='store_true')
parser.add_argument('--production', action='store_true', help='Remove draft noindex only after completing launch checks.')
args = parser.parse_args()

def href(path, prefix=''):
    return prefix + path

def button(label='Request Free Quote', url='contact.html#quote', secondary=False):
    return f'<a class="button{" button-outline" if secondary else ""}" href="{esc(url)}">{label}<span aria-hidden="true">↗</span></a>'

def photo(name='entrance', alt='Metal driveway gate at a tree-lined property entrance', cls='', priority=False):
    return f'<img class="{cls}" src="{{P}}images/{name}-960.webp" srcset="{{P}}images/{name}-640.webp 640w, {{P}}images/{name}-960.webp 960w, {{P}}images/{name}-1600.webp {1160 if name == "access" else 1600}w" sizes="{'100vw' if priority else '(max-width: 700px) 100vw, (max-width: 1100px) 50vw, 650px'}" width="1600" height="1200" alt="{esc(alt)}" {"fetchpriority=high" if priority else "loading=lazy"} decoding="async">'

def header(active, prefix):
    nav = [('services.html','Services'),('gallery.html','Our Work'),('about.html','About Us'),('faq.html','FAQs'),('contact.html','Contact')]
    links = ''.join(f'<a href="{prefix}{url}" {"aria-current=page" if active==url else ""}>{label}</a>' for url,label in nav)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
    <div class="topbar"><div class="wrap"><span>GATE AUTOMATION &amp; SECURITY · LABELLE, FLORIDA</span><a href="tel:+18635914283">Let’s talk: (863) 591-GATE</a></div></div>
    <header class="header"><div class="wrap header-inner">
      <a class="brand" href="{prefix}index.html" aria-label="Big Bear Automatic Gates home"><img class="brand-logo" src="{prefix}images/big-bear-emblem.png" width="64" height="64" alt=""><span>BIG BEAR<small>AUTOMATIC GATES</small><span class="brand-caption">SMART ACCESS. BUILT TO LAST.</span></span></a>
      <button class="menu-toggle" type="button" aria-controls="navigation" aria-expanded="false" hidden>Menu <span aria-hidden="true">☰</span></button>
      <nav id="navigation" aria-label="Main navigation">{links}{button(url=prefix+'contact.html#quote')}</nav>
    </div></header>'''

def footer(prefix):
    return f'''<footer class="footer"><div class="wrap footer-grid"><div><a class="brand" href="{prefix}index.html"><img class="brand-logo" src="{prefix}images/big-bear-emblem.png" width="64" height="64" alt=""><span>BIG BEAR<small>AUTOMATIC GATES</small><span class="brand-caption">SMART ACCESS. BUILT TO LAST.</span></span></a><p>Security. Craftsmanship.<br>A better way to come home.</p></div><div><h2>Explore</h2><a href="{prefix}services.html">Our services</a><a href="{prefix}gallery.html">Our work</a><a href="{prefix}about.html">About Big Bear</a><a href="{prefix}faq.html">Common questions</a></div><div><h2>Get in touch</h2><a href="tel:+18635914283">(863) 591-GATE</a><p>LaBelle, FL 33935</p><a href="{prefix}contact.html#quote">Request a free quote</a></div><div><h2>Business hours</h2><p>Monday–Saturday<br>8:00 am–5:00 pm</p><p>Sunday · Closed</p></div></div><div class="wrap footer-bottom"><p>© <span data-year>2026</span> Big Bear Automatic Gates, LLC</p><span>Smart access. Built to last.</span><a href="#top">Back to top ↑</a></div></footer>
    <div class="mobile-contact" aria-label="Quick contact"><a href="tel:+18635914283">Call Big Bear</a><a href="{prefix}contact.html#quote">Request Free Quote ↗</a></div>'''

def cta():
    return '<section class="cta-band"><div class="wrap"><div><p class="eyebrow">YOUR PROPERTY. YOUR NEXT STEP.</p><h2>Let’s build a better entrance.</h2></div>'+button(url='{P}contact.html#quote')+'</div></section>'

def intro(kicker, title, desc):
    return f'<section class="page-intro"><div class="wrap"><p class="eyebrow">{kicker}</p><h1>{title}</h1><p class="intro-copy">{desc}</p></div></section>'

def services_grid():
    cards=[]
    for i,s in enumerate(SERVICES):
        cards.append(f'<article class="service-card"><a class="card-image" href="{{P}}services/{s["slug"]}.html" aria-label="Explore {s["title"]}">{photo(s["photo"],s["alt"])}<span class="card-index">0{i+1}</span></a><div class="card-body"><h3><a href="{{P}}services/{s["slug"]}.html">{s["title"]}</a></h3><p>{s["summary"]}</p><a class="text-link" href="{{P}}services/{s["slug"]}.html">Learn more <span aria-hidden="true">↗</span></a></div></article>')
    return '<div class="service-grid">'+''.join(cards)+'</div>'

def projects(limit=None):
    cards=[]
    for p in PROJECTS[:limit]:
        cards.append(f'<article class="project-card">{photo(p["photo"],p["alt"])}<div><p class="eyebrow">{p["category"]}</p><h3>{p["title"]}</h3><p>{p["description"]}</p></div></article>')
    return '<div class="project-grid">'+''.join(cards)+'</div>'

def faqs(limit=None):
    return '<div class="faq-list">'+''.join(f'<details><summary>{q}<span aria-hidden="true">+</span></summary><div class="faq-answer"><p>{a}</p></div></details>' for q,a in FAQS[:limit])+'</div>'

def process():
    steps=[('Consultation','Tell us about your entrance, your property, and what you want to improve.'),('Property assessment','Review the opening, access, site conditions, and everyday traffic.'),('Custom design','Bring the gate, operator, and access options together in a considered plan.'),('Installation','Coordinate the agreed work around your property and the chosen system.'),('Testing & handover','Review system operation and learn how to use your new entrance.')]
    return '<ol class="process-list">'+''.join(f'<li><span>0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i,(t,d) in enumerate(steps))+'</ol>'

def quote_form():
    options=''.join(f'<option>{s["title"]}</option>' for s in SERVICES)
    return f'''<form class="quote-form" id="quote-form" hidden>
      <h2>Tell us about your project.</h2><p class="form-notice" id="form-notice">Preview form: online requests are not connected yet. To request a quote now, call <a href="tel:+18635914283">(863) 591-GATE</a>.</p>
      <div class="form-grid"><label>Full name <span>*</span><input name="name" autocomplete="name" required maxlength="120"></label><label>Phone <span>*</span><input name="phone" type="tel" autocomplete="tel" required minlength="7" maxlength="30"></label><label>Email <span>*</span><input name="email" type="email" autocomplete="email" required maxlength="254"></label><label>Property location <span>*</span><input name="location" autocomplete="address-level2" placeholder="City or ZIP code" required maxlength="180"></label><label class="full">Service needed <span>*</span><select name="service" required><option value="">Select a service</option>{options}<option>Help choosing a solution</option></select></label><label class="full">Project details <span>*</span><textarea name="message" rows="4" required maxlength="4000" placeholder="Tell us about your gate, property, or security needs."></textarea></label></div>
      <div class="trap" aria-hidden="true"><label>Leave this blank<input name="website" tabindex="-1" autocomplete="off"></label></div>
      <label class="consent"><input type="checkbox" name="consent" required><span>Big Bear may contact me about this request. <span aria-label="required">*</span></span></label>
      <button class="button" type="submit" id="quote-submit">Review quote request <span aria-hidden="true">↗</span></button><p class="form-small">Fields marked * are required. Your details are not saved in this browser.</p>
      <div class="form-result" role="status" aria-live="polite" tabindex="-1" hidden></div>
    </form><noscript><p>Call <a href="tel:+18635914283">(863) 591-GATE</a> to discuss your project. JavaScript is needed to preview the quote form.</p></noscript>'''

def home():
    return f'''<section class="hero" aria-labelledby="hero-title">{photo('entrance','Custom metal driveway gate at a landscaped property entrance','hero-photo',True)}<div class="hero-shade"></div><div class="wrap hero-content"><p class="eyebrow"><span></span> CUSTOM GATES. CONFIDENT ARRIVALS.</p><h1 id="hero-title">A strong first impression.<br><em>A secure way home.</em></h1><p class="hero-copy">Custom automatic gates, access control, and security solutions. Designed around your property. Built around your peace of mind.</p><div class="actions">{button()}{button('Call Big Bear Today','tel:+18635914283',True)}</div><div class="hero-note"><span class="tiny-line"></span> RESIDENTIAL &amp; COMMERCIAL GATE SOLUTIONS</div></div><div class="hero-caption">CRAFTED FOR YOUR PROPERTY<br><span>Engineered for everyday life.</span></div></section>
    <div class="trust-strip"><div class="wrap"><span>Security by design</span><span>Custom craftsmanship</span><span>Modern access technology</span><span>Based in LaBelle, Florida</span></div></div>
    <section class="section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">01 / COMPLETE GATE SOLUTIONS</p><h2>More than a gate.<br>A considered entrance.</h2></div><div><p>From the first approach to the last detail, bring security, convenience, and a sense of arrival to your property.</p><a class="text-link" href="services.html">Explore all services <span aria-hidden="true">↗</span></a></div></div>{services_grid()}</div></section>
    <section class="section why"><div class="wrap why-grid"><div class="why-image">{photo('detail','Close view of metal gate craftsmanship')}<span class="image-label">STRENGTH IS IN THE DETAILS.</span></div><div><p class="eyebrow">02 / THE BIG BEAR APPROACH</p><h2>Protection with purpose.<br>Craftsmanship with character.</h2><p class="lead">An entrance should feel like part of your property. Its technology should make everyday access simpler.</p><div class="value-grid"><div><span>01</span><h3>Designed around you</h3><p>A considered fit for your entrance, style, and daily routine.</p></div><div><span>02</span><h3>Security in focus</h3><p>Gate and access decisions made together, from the start.</p></div><div><span>03</span><h3>Attention to detail</h3><p>Materials, finishes, and operation that work as one system.</p></div><div><span>04</span><h3>A local conversation</h3><p>Talk directly with Big Bear in LaBelle about your project.</p></div></div><a class="text-link" href="about.html">Get to know Big Bear <span aria-hidden="true">↗</span></a></div></div></section>
    <section class="section"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">03 / OUR WORK</p><h2>Every entrance tells a story.</h2></div><a class="text-link" href="gallery.html">View the project gallery <span aria-hidden="true">↗</span></a></div>{projects(3)}</div></section>
    <section class="section process"><div class="wrap"><p class="eyebrow">04 / FROM IDEA TO ENTRANCE</p><h2>A clear path to your new gate.</h2>{process()}</div></section>
    <section class="section reviews-section" hidden data-reviews><div class="wrap"><p class="eyebrow">CUSTOMER PERSPECTIVES</p><h2>Confidence, in their own words.</h2><div class="review-grid" data-review-grid></div></div></section>
    <section class="section areas"><div class="wrap area-grid"><div><p class="eyebrow">05 / LOCAL KNOWLEDGE</p><h2>Rooted in LaBelle.<br>Focused on your property.</h2><p>Planning a gate or security project in LaBelle or elsewhere in Southwest Florida? Share your location so we can confirm availability for your property.</p><a class="text-link" href="contact.html">Discuss your location <span aria-hidden="true">↗</span></a></div><div class="area-card"><span class="eyebrow">OUR HOME BASE</span><h3>LaBelle, Florida</h3><p>Big Bear Automatic Gates, LLC<br>LaBelle, FL 33935</p><div class="area-divider"></div><span class="eyebrow">LET’S TALK ABOUT YOUR PROJECT</span><a class="large-phone" href="tel:+18635914283">(863) 591-GATE</a><p>Monday–Saturday · 8 am–5 pm</p></div></div></section>
    <section class="section faq-section"><div class="wrap faq-grid"><div><p class="eyebrow">06 / A FEW GOOD QUESTIONS</p><h2>Before you<br>make an entrance.</h2><a class="text-link" href="faq.html">All frequently asked questions <span aria-hidden="true">↗</span></a></div>{faqs(5)}</div></section>
    <section class="section quote-section" id="contact"><div class="wrap quote-grid"><div><p class="eyebrow">07 / START YOUR PROJECT</p><h2>Your property deserves<br>a thoughtful entrance.</h2><p>Tell us what you have in mind. We’ll help you explore gate automation and security options for your home or business.</p><a class="large-phone" href="tel:+18635914283">(863) 591-GATE</a><p>Prefer to talk? Call Big Bear today.</p></div>{quote_form()}</div></section>'''

def service_page(s):
    items=''.join(f'<li>{x}</li>' for x in s['considerations'])
    return intro('GATE & SECURITY SOLUTIONS',s['title'],s['summary'])+f'<section class="section"><div class="wrap detail-grid"><div>{photo(s["photo"],s["alt"])}<p class="photo-note">Photography from Big Bear’s existing website; shown as an entrance reference.</p></div><div><p class="eyebrow">DESIGNED AROUND YOUR PROPERTY</p><h2>{s["heading"]}</h2><p class="lead">{s["body"]}</p><h3>What we’ll discuss</h3><ul class="check-list">{items}</ul>{button(url="../contact.html#quote")}</div></div></section><section class="section soft"><div class="wrap narrow"><p class="eyebrow">A USEFUL FIRST STEP</p><h2>Bring your questions. We’ll start there.</h2><p class="lead">{s["next"]}</p><a class="text-link" href="../services.html">Explore other gate and security services ↗</a></div></section>'+cta()

def page(path, title, description, body, active='', service=None):
    prefix='../' if '/' in path else ''
    canonical=DOMAIN+('/' if path=='index.html' else '/'+path)
    business={'@type':'LocalBusiness','@id':DOMAIN+'/#business','name':'Big Bear Automatic Gates, LLC','url':DOMAIN+'/','telephone':'+1-863-591-4283','address':{'@type':'PostalAddress','addressLocality':'LaBelle','addressRegion':'FL','postalCode':'33935','addressCountry':'US'},'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],'opens':'08:00','closes':'17:00'}]}
    graph=[business,{'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'about':{'@id':DOMAIN+'/#business'}}]
    if service:
        graph.append({'@type':'Service','name':service['title'],'description':service['summary'],'provider':{'@id':DOMAIN+'/#business'},'url':canonical})
    if path!='index.html':
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':DOMAIN+'/'},{'@type':'ListItem','position':2,'name':title.split(' | ')[0],'item':canonical}]})
    if path=='faq.html':
        graph.append({'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQS]})
    robots='' if args.production else '<meta name="robots" content="noindex, nofollow">'
    html=f'''<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title><meta name="description" content="{esc(description)}">
  {robots}<link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#2b2b2b">
  <link rel="icon" type="image/png" href="{prefix}images/favicon-copper.png">
  <link rel="stylesheet" href="{prefix}css/styles.css?v=6">
  <script src="{prefix}js/config.js?v=2" defer></script><script src="{prefix}js/main.js?v=2" defer></script>
  <script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')}</script>
</head><body id="top">{header(active,prefix)}<main id="main">{body.replace('{P}',prefix)}</main>{footer(prefix)}</body></html>'''
    target=OUT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(html,encoding='utf-8')

page('index.html','Automatic Gates & Security in LaBelle | Big Bear','Custom automatic gates, gate openers, and access control for residential and commercial properties. Talk to Big Bear Automatic Gates in LaBelle, Florida.',home())
if not args.homepage_only:
    page('services.html','Gate Installation & Security Services | Big Bear','Explore automatic gate installation, operators, access control, commercial gates, security integration, and repair with Big Bear in LaBelle, Florida.',intro('OUR SERVICES','Security, considered<br>from every angle.','Gate design, automation, and access technology should work together. Explore the right starting point for your property.')+'<section class="section"><div class="wrap">'+services_grid()+'</div></section>'+cta(),'services.html')
    for s in SERVICES:
        page('services/'+s['slug']+'.html',s['title']+' in LaBelle | Big Bear',s['summary']+' Discuss your property with Big Bear Automatic Gates in LaBelle, Florida.',service_page(s),'services.html',s)
    page('about.html','About Big Bear Automatic Gates | LaBelle, FL','Meet Big Bear Automatic Gates, LLC, a LaBelle-based gate automation and security company focused on security, craftsmanship, and thoughtful design.',intro('ABOUT BIG BEAR','A strong entrance.<br>A personal approach.','Security, quality, reliability, and custom design. Four ideas that shape the way we think about your property.')+f'<section class="section"><div class="wrap detail-grid">{photo("detail","Metal gate and entrance details")}<div><p class="eyebrow">BASED IN LABELLE, FLORIDA</p><h2>Craftsmanship meets<br>modern access.</h2><p class="lead">Big Bear Automatic Gates, LLC brings gate automation and security solutions together for property owners looking for a more considered entrance.</p><p>We start with the way you use your property: who comes and goes, the character of the entrance, and what you want to protect. That conversation helps shape a solution with purpose.</p><p>From custom driveway gate concepts to access-control planning, our focus is an entrance that balances security, privacy, and convenience.</p>{button(url="contact.html#quote")}</div></div></section><section class="section process"><div class="wrap"><p class="eyebrow">HOW A PROJECT TAKES SHAPE</p><h2>Thoughtful from the first conversation.</h2>{process()}</div></section>'+cta(),'about.html')
    page('gallery.html','Gate Project Gallery | Big Bear Automatic Gates','Explore gate and entrance photography from Big Bear Automatic Gates. Discuss a custom gate and automation project for your property.',intro('THE PROJECT GALLERY','Made for an entrance.<br>Built to make an impression.','A closer look at gates and entrances featured by Big Bear. Find details that inspire your next project.')+'<section class="section"><div class="wrap">'+projects()+'<p class="gallery-note">Project photography from our existing website. Contact Big Bear to discuss the details and location of a featured installation.</p></div></section>'+cta(),'gallery.html')
    page('faq.html','Automatic Gate Questions & Answers | Big Bear','Get answers about automatic gate costs, project timing, gate styles, repairs, and access control before discussing your project with Big Bear.',intro('FREQUENTLY ASKED QUESTIONS','Good questions.<br>A more confident decision.','Planning a new entrance or improving an existing gate? Start with the essentials, then talk with us about your property.')+'<section class="section"><div class="wrap narrow">'+faqs()+'</div></section>'+cta(),'faq.html')
    page('contact.html','Request a Gate Quote | Big Bear Automatic Gates','Contact Big Bear Automatic Gates in LaBelle, Florida. Call (863) 591-GATE to discuss gate automation, access control, or your next project.',intro('CONTACT BIG BEAR','Let’s talk about<br>your entrance.','A free quote starts with a conversation about your property, your priorities, and the way you want your gate to work.')+'<section class="section quote-section" id="quote"><div class="wrap quote-grid"><div><p class="eyebrow">A LOCAL CONVERSATION</p><h2>Call Big Bear today.</h2><a class="large-phone" href="tel:+18635914283">(863) 591-GATE</a><p>Big Bear Automatic Gates, LLC<br>LaBelle, FL 33935</p><dl class="hours"><dt>Monday–Saturday</dt><dd>8:00 am–5:00 pm</dd><dt>Sunday</dt><dd>Closed</dd></dl><h3>Where is your property?</h3><p>Include your city or ZIP code so we can confirm service availability and discuss the next step.</p></div>'+quote_form()+'</div></section>','contact.html')
    paths=sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob('*.html'))
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{DOMAIN}{"/" if p=="index.html" else "/"+p}</loc></url>\n' for p in paths)+'</urlset>\n',encoding='utf-8')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n'+('Sitemap: '+DOMAIN+'/sitemap.xml\n' if args.production else '# Draft: each HTML page carries noindex. This is not access control.\n'),encoding='utf-8')
print('Rendered homepage.' if args.homepage_only else 'Rendered all 12 HTML pages, sitemap, and robots.txt.')
