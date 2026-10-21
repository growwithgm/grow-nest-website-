// Page behaviour: scroll state, header counter, dawn, dot field, form, copy buttons.

import { createField } from './field.js';

const root = document.documentElement;
const reduceQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const smoothstep = (a, b, v) => {
  const t = clamp((v - a) / (b - a), 0, 1);
  return t * t * (3 - 2 * t);
};

// ----------------------------------------------------------------- scenes

const scenes = [...document.querySelectorAll('[data-shape]')].map((el) => ({
  el,
  shape: el.dataset.shape,
  layout: el.dataset.layout || 'standard',
  name: el.dataset.name || '',
  tint: getComputedStyle(el).getPropertyValue('--tint').trim() || '#EEF0F7',
}));
const count = scenes.length;

// Each scene is fully formed while the viewport centre sits between a and b:
// its centre for short sections, or the whole stretch where a tall section
// covers the screen. Between b of one scene and a of the next, dots morph.
let keys = [];

function measure() {
  const vh = window.innerHeight;
  const sy = window.scrollY;
  const docH = root.scrollHeight;
  const lo = vh / 2;
  const hi = Math.max(lo, docH - vh / 2);
  keys = scenes.map(({ el }) => {
    const r = el.getBoundingClientRect();
    const top = r.top + sy;
    const half = Math.min(r.height, vh) / 2;
    return { a: clamp(top + half, lo, hi), b: clamp(top + r.height - half, lo, hi) };
  });
  for (let i = 1; i < keys.length; i++) {
    if (keys[i].a < keys[i - 1].b) keys[i].a = keys[i - 1].b;
    if (keys[i].b < keys[i].a) keys[i].b = keys[i].a;
  }
  update();
}

function progress() {
  const n = keys.length;
  if (!n) return 0;
  const c = window.scrollY + window.innerHeight / 2;
  if (c <= keys[0].b) return 0;
  for (let i = 0; i < n - 1; i++) {
    const k = keys[i];
    const next = keys[i + 1];
    if (c <= k.b) return i;
    if (c < next.a) return i + (c - k.b) / (next.a - k.b);
  }
  return n - 1;
}

// Dawn ramps in from Markets and reaches full strength at Contact.
const dawnAt = (p) => smoothstep(count - 4, count - 2, p);
let dawn = 0;

// ----------------------------------------------------------------- header

const counter = document.querySelector('.counter');
const counterName = document.querySelector('.counter-name');
const counterNum = document.querySelector('.counter-num');
let current = -1;

function setScene(i) {
  if (i === current) return;
  current = i;
  const s = scenes[i];
  if (!s) return;
  counterName.textContent = s.name;
  counterNum.textContent = `${i + 1}/${count}`;
  counter.style.setProperty('--scene-tint', s.tint);
}

function update() {
  const p = progress();
  setScene(clamp(Math.round(p), 0, count - 1));
  const d = dawnAt(p);
  if (Math.abs(d - dawn) > 0.002 || (d === 0 && dawn !== 0) || (d === 1 && dawn !== 1)) {
    dawn = d;
    root.style.setProperty('--dawn', d.toFixed(3));
  }
}

let ticking = false;
window.addEventListener(
  'scroll',
  () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      update();
    });
  },
  { passive: true },
);

// ------------------------------------------------------------------ field

const canvas = document.querySelector('canvas.dots');
let field = null;
try {
  field = createField(canvas, {
    scenes: scenes.map(({ shape, tint, layout }) => ({ shape, tint, layout })),
    getProgress: progress,
    getDawn: () => dawn,
    reduced: reduceQuery.matches,
  });
} catch {
  field = null;
}
root.dataset.field = field ? field.kind : 'none';
if (!field) canvas.remove();

reduceQuery.addEventListener?.('change', (e) => field?.setReduced(e.matches));

document.addEventListener('visibilitychange', () => {
  if (document.hidden) field?.pause();
  else field?.resume();
});

// --------------------------------------------------------------- measuring

let measureQueued = false;
function queueMeasure() {
  if (measureQueued) return;
  measureQueued = true;
  requestAnimationFrame(() => {
    measureQueued = false;
    measure();
  });
}

window.addEventListener('resize', () => {
  field?.resize();
  queueMeasure();
});
window.addEventListener('load', queueMeasure);
document.fonts?.ready.then(queueMeasure);
if ('ResizeObserver' in window) {
  const ro = new ResizeObserver(queueMeasure);
  ro.observe(document.querySelector('main'));
  const foot = document.querySelector('footer');
  if (foot) ro.observe(foot);
}
measure();

// ------------------------------------------------------------------- form

const ENDPOINT = 'https://formsubmit.co/ajax/connect.grownest@gmail.com';
const MSG_OK = 'Thanks. We have your message and will reply soon.';
const MSG_ERR = 'That did not send. Check your email address, or message us on WhatsApp.';

const form = document.querySelector('form.enquiry');

function looksLikeUrl(v) {
  const s = /^[a-z][a-z0-9+.-]*:\/\//i.test(v) ? v : `https://${v}`;
  try {
    const u = new URL(s);
    return /^https?:$/.test(u.protocol) && /^[^\s.]+(\.[^\s.]+)+$/.test(u.hostname);
  } catch {
    return false;
  }
}

const looksLikeEmail = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

if (form) {
  const status = form.querySelector('.form-status');
  const button = form.querySelector('button[type="submit"]');
  const f = form.elements;
  const checked = [f.name, f.email, f.store_url, f.message];

  const validate = () => {
    f.email.setCustomValidity(
      f.email.value.trim() && !looksLikeEmail(f.email.value.trim()) ? 'Please enter a valid email address.' : '',
    );
    f.store_url.setCustomValidity(
      f.store_url.value.trim() && !looksLikeUrl(f.store_url.value.trim()) ? 'Please enter a valid URL.' : '',
    );
    let ok = true;
    for (const el of checked) {
      const valid = el.checkValidity();
      el.setAttribute('aria-invalid', valid ? 'false' : 'true');
      ok = ok && valid;
    }
    return ok;
  };

  for (const el of checked) {
    el.addEventListener('input', () => {
      if (el.getAttribute('aria-invalid') === 'true') validate();
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    status.textContent = '';
    status.className = 'form-status';

    // Honeypot: people never see this field, bots fill it.
    if (f._honey.value) return;

    if (!validate()) {
      form.reportValidity();
      return;
    }

    const body = {
      name: f.name.value.trim(),
      email: f.email.value.trim(),
      whatsapp: f.whatsapp.value.trim(),
      store_url: f.store_url.value.trim(),
      services: [...form.querySelectorAll('input[name="services"]:checked')].map((c) => c.value).join(', '),
      message: f.message.value.trim(),
      _subject: 'New enquiry from grownest.pro',
      _template: 'table',
      _honey: '',
    };

    button.disabled = true;
    form.setAttribute('aria-busy', 'true');
    let ok = false;
    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(body),
      });
      const json = await res.json().catch(() => ({}));
      ok = res.ok && String(json.success) === 'true';
    } catch {
      ok = false;
    }
    button.disabled = false;
    form.removeAttribute('aria-busy');

    if (ok) {
      form.reset();
      for (const el of checked) el.setAttribute('aria-invalid', 'false');
      status.textContent = MSG_OK;
      status.classList.add('is-ok');
    } else {
      status.textContent = MSG_ERR;
      status.classList.add('is-error');
    }
  });
}

// ----------------------------------------------------------- copy buttons

for (const btn of document.querySelectorAll('[data-copy]')) {
  const label = btn.textContent;
  btn.addEventListener('click', async () => {
    const el = document.getElementById(btn.dataset.copy);
    if (!el) return;
    const text = el.textContent.trim();
    let ok = false;
    try {
      await navigator.clipboard.writeText(text);
      ok = true;
    } catch {
      ok = false;
    }
    if (ok) {
      btn.textContent = 'Copied';
      setTimeout(() => (btn.textContent = label), 1600);
    } else {
      // No clipboard access: select the text so it can be copied by hand.
      const range = document.createRange();
      range.selectNodeContents(el);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    }
  });
}
