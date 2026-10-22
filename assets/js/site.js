/* Grow Nest site behaviour: mobile menu, header shadow, contact form, copy buttons. */
(() => {
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
        const s = getSelection(); s.removeAllRanges(); s.addRange(r); done('Seleccionado');
      };
      try { navigator.clipboard.writeText(b.dataset.copy).then(() => done('Copiado'), fallback); } catch (e) { fallback(); }
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
      data.servicios = [...form.querySelectorAll('input[name="servicio"]:checked')].map(i => i.value).join(', ') || 'Sin indicar';
      delete data.servicio;
      const email = (data.email || '').trim();
      if (!data.nombre || !data.nombre.trim()) { say('Escribe tu nombre.', 'error'); form.nombre.focus(); return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { say('Revisa tu email: parece incompleto.', 'error'); form.email.focus(); return; }
      if (!data.mensaje || !data.mensaje.trim()) { say('Cuéntanos en una línea qué necesitas.', 'error'); form.mensaje.focus(); return; }
      submit.disabled = true; say('Enviando…', 'info');
      try {
        const res = await fetch('https://formsubmit.co/ajax/connect.grownest@gmail.com', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ ...data, _subject: 'Nueva solicitud desde grownest.pro', _template: 'table', pagina: location.pathname })
        });
        const out = await res.json().catch(() => ({}));
        if (!res.ok || out.success === 'false' || out.success === false) throw new Error('send');
        form.reset(); say('Gracias. Hemos recibido tu mensaje y te responderemos pronto.', 'ok');
      } catch (err) {
        say('No se ha podido enviar. Revisa tu email o escríbenos por WhatsApp.', 'error');
      } finally { submit.disabled = false; }
    });
  });
})();
