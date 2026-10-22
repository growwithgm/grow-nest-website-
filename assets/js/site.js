/* Grow Nest site behaviour: mobile menu, header shadow, contact form, copy buttons. */
(() => {
  const EN = (document.documentElement.lang || '').toLowerCase().startsWith('en');
  const T = EN ? {
    copied: 'Copied', selected: 'Selected', name: 'Please enter your name.', email: 'Check your email: it looks incomplete.',
    msg: 'Tell us in one line what you need.', sending: 'Sending…', none: 'Not specified',
    ok: 'Thank you. We have received your message and will reply soon.', err: "We couldn't send it. Check your email or message us on WhatsApp.",
    subject: 'New enquiry from grownest.pro (EN)'
  } : {
    copied: 'Copiado', selected: 'Seleccionado', name: 'Escribe tu nombre.', email: 'Revisa tu email: parece incompleto.',
    msg: 'Cuéntanos en una línea qué necesitas.', sending: 'Enviando…', none: 'Sin indicar',
    ok: 'Gracias. Hemos recibido tu mensaje y te responderemos pronto.', err: 'No se ha podido enviar. Revisa tu email o escríbenos por WhatsApp.',
    subject: 'Nueva solicitud desde grownest.pro'
  };
  const header = document.querySelector('.site-header');
  const onScroll = () => header && header.classList.toggle('is-scrolled', window.scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // Mobile menu
  const btn = document.querySelector('.menu-btn');
  const menu = document.getElementById('mobile-menu');
  if (btn && menu) {
    const set = open => { btn.setAttribute('aria-expanded', String(open)); menu.hidden = !open; document.body.classList.toggle('menu-open', open); };
    btn.addEventListener('click', () => set(btn.getAttribute('aria-expanded') !== 'true'));
    menu.addEventListener('click', e => { if (e.target.closest('a')) set(false); });
    addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
  }

  // Copy buttons
  document.querySelectorAll('[data-copy]').forEach(b => {
    b.addEventListener('click', () => {
      const label = b.textContent;
      const done = t => { b.textContent = t; setTimeout(() => { b.textContent = label; }, 1600); };
      const fallback = () => {
        const el = document.getElementById(b.getAttribute('aria-controls'));
        if (!el) return;
        const r = document.createRange(); r.selectNodeContents(el);
        const s = getSelection(); s.removeAllRanges(); s.addRange(r); done(T.selected);
      };
      try { navigator.clipboard.writeText(b.dataset.copy).then(() => done(T.copied), fallback); } catch (e) { fallback(); }
    });
  });

  // Contact form (FormSubmit, sent to connect.grownest@gmail.com)
  document.querySelectorAll('form[data-contact]').forEach(form => {
    const status = form.querySelector('.form-status');
    const submit = form.querySelector('button[type="submit"]');
    const say = (msg, kind) => { status.textContent = msg; status.dataset.kind = kind; };
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (form.querySelector('[name="_honey"]').value) return;
      const data = Object.fromEntries(new FormData(form).entries());
      data.servicios = [...form.querySelectorAll('input[name="servicio"]:checked')].map(i => i.value).join(', ') || T.none;
      delete data.servicio;
      const email = (data.email || '').trim();
      if (!data.nombre || !data.nombre.trim()) { say(T.name, 'error'); form.nombre.focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { say(T.email, 'error'); form.email.focus(); return; }
      if (!data.mensaje || !data.mensaje.trim()) { say(T.msg, 'error'); form.mensaje.focus(); return; }
      submit.disabled = true; say(T.sending, 'info');
      try {
        const res = await fetch('https://formsubmit.co/ajax/connect.grownest@gmail.com', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ ...data, _subject: T.subject, _template: 'table', pagina: location.pathname })
        });
        const out = await res.json().catch(() => ({}));
        if (!res.ok || out.success === 'false' || out.success === false) throw new Error('send');
        form.reset(); say(T.ok, 'ok');
      } catch (err) {
        say(T.err, 'error');
      } finally { submit.disabled = false; }
    });
  });
})();
