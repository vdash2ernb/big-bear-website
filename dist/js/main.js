/* Navigation and FAQs remain usable without JavaScript. */
const config = window.BIG_BEAR_CONFIG || {};
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
const mobile = window.matchMedia('(max-width: 960px)');
function setMenu(open) {
  menu.setAttribute('aria-expanded', String(open));
  menu.textContent = open ? 'Close ×' : 'Menu ☰';
  nav.classList.toggle('is-collapsed', !open);
}
if (menu && nav) {
  menu.hidden = false;
  setMenu(!mobile.matches);
  menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  mobile.addEventListener('change', e => setMenu(!e.matches));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && mobile.matches && menu.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      menu.focus();
    }
  });
}
 document.querySelectorAll('[data-year]').forEach(node => node.textContent = new Date().getFullYear());

// Empty data makes no rating or endorsement claims.
const reviewSection = document.querySelector('[data-reviews]');
if (reviewSection && Array.isArray(config.reviews)) {
  const grid = reviewSection.querySelector('[data-review-grid]');
  config.reviews.filter(r => r.name && r.text && Number.isInteger(r.rating) && r.rating >= 1 && r.rating <= 5).forEach(review => {
    const card = document.createElement('article');
    card.className = 'review-card';
    const rating = document.createElement('p');
    rating.className = 'rating';
    rating.textContent = `${review.rating} out of 5`;
    const quote = document.createElement('blockquote');
    quote.textContent = review.text;
    const name = document.createElement('p');
    name.textContent = review.name;
    card.append(rating, quote, name);
    try {
      const source = new URL(review.sourceUrl);
      if (source.protocol === 'https:') {
        const link = document.createElement('a');
        link.href = source.href;
        link.textContent = 'Read original review';
        card.append(link);
      }
    } catch { /* No source link when absent or invalid. */ }
    grid.append(card);
  });
  reviewSection.hidden = !grid.children.length;
}

const form = document.querySelector('#quote-form');
if (form) {
  form.hidden = false;
  const notice = form.querySelector('#form-notice');
  const submit = form.querySelector('#quote-submit');
  const result = form.querySelector('.form-result');
  let endpoint = null;
  // A deliberate same-origin HTTPS backend and privacy notice are required.
  try {
    if (config.quoteEndpoint && config.privacyUrl) {
      const url = new URL(config.quoteEndpoint, location.href);
      const privacy = new URL(config.privacyUrl, location.href);
      if (url.origin === location.origin && url.protocol === 'https:' && privacy.origin === location.origin) {
        endpoint = url.href;
        notice.replaceChildren(document.createTextNode('We’ll use your details to respond to this request. '));
        const link = document.createElement('a');
        link.href = privacy.href;
        link.textContent = 'Read our privacy notice.';
        notice.append(link);
        submit.textContent = 'Request Free Quote ↗';
      }
    }
  } catch { /* Invalid configuration keeps preview mode. */ }
  function showResult(message, error = false) {
    result.hidden = false;
    result.classList.toggle('error', error);
    result.textContent = message;
    result.focus({ preventScroll: true });
    result.scrollIntoView({ behavior: 'auto', block: 'nearest' });
  }
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form).entries());
    if (data.website) {
      showResult('We could not process this request. Please call (863) 591-GATE.', true);
      return;
    }
    for (const name of ['name', 'phone', 'email', 'location', 'service', 'message']) {
      data[name] = String(data[name] || '').trim();
      if (!data[name]) {
        showResult('Please complete all required fields.', true);
        form.elements.namedItem(name).focus();
        return;
      }
    }
    if (!endpoint) {
      showResult(`Your request is ready to review. Nothing has been sent.\n\n${data.name}\n${data.service}\nProperty location: ${data.location}\n\nOnline requests are not connected yet. Please call (863) 591-GATE to discuss your project.`);
      return;
    }
    submit.disabled = true;
    submit.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin', signal: controller.signal,
        body: JSON.stringify({ ...data, consent: data.consent === 'on', sourcePage: location.pathname })
      });
      const receipt = await response.json();
      if (!response.ok || receipt.accepted !== true || typeof receipt.requestId !== 'string' || !receipt.requestId.trim()) throw new Error('No confirmed receipt');
      form.reset();
      showResult('Thank you. Your quote request has been received. Big Bear will contact you about your project.');
    } catch {
      showResult('We could not confirm delivery. Your details are still here. Please call (863) 591-GATE before retrying to avoid sending a duplicate request.', true);
    } finally {
      clearTimeout(timeout);
      submit.disabled = false;
      submit.textContent = 'Request Free Quote ↗';
      form.removeAttribute('aria-busy');
    }
  });
}
