#!/usr/bin/env python3
"""Builds the static Grow Nest site in Spanish (main, ranks in Spain) and English (/en/).

Run:  python3 tools/build.py
Every page gets its own title, meta description, canonical URL, hreflang links
(es-ES, en, x-default = Spanish), Open Graph tags and JSON-LD.
All copy lives in this file: UI strings in UI, services in SERVICES, pages below.
"""
import json, os, time
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.grownest.pro"
V = time.strftime("%Y%m%d%H%M")
TODAY = time.strftime("%Y-%m-%d")
WA_NUMBER = "447429917026"
PHONE = "+44 7429 917026"
EMAIL = "connect.grownest@gmail.com"
AREA = ["ES", "GB", "DE", "FR", "NL", "IT", "PT", "US", "AE", "SA", "AU"]

def e(s): return escape(s, quote=False)
def a(s): return escape(s, quote=True)

# ---------------------------------------------------------------- URLs per language
PATHS = {
    "home": {"es": "/", "en": "/en/"},
    "google": {"es": "/agencia-google-ads/", "en": "/en/google-ads-agency/"},
    "shopify": {"es": "/agencia-shopify/", "en": "/en/shopify-agency/"},
    "whatsapp": {"es": "/whatsapp-marketing/", "en": "/en/whatsapp-marketing/"},
    "email": {"es": "/email-marketing-ecommerce/", "en": "/en/email-marketing/"},
    "envios": {"es": "/logistica-ecommerce/", "en": "/en/shipping-and-returns/"},
    "marketplaces": {"es": "/tiktok-shop-amazon/", "en": "/en/tiktok-shop-amazon/"},
    "apps": {"es": "/desarrollo-a-medida/", "en": "/en/custom-apps/"},
    "about": {"es": "/sobre-nosotros/", "en": "/en/about/"},
    "contact": {"es": "/contacto/", "en": "/en/contact/"},
    "privacy": {"es": "/politica-de-privacidad/", "en": "/en/privacy-policy/"},
}
def url(key, lang): return PATHS[key][lang]

# ---------------------------------------------------------------- UI strings
UI = {
    "es": {
        "html_lang": "es-ES", "og_locale": "es_ES", "og_alt_locale": "en_GB",
        "skip": "Saltar al contenido", "home_aria": "Grow Nest, inicio", "nav_aria": "Principal",
        "nav": [("Meta Ads", "/#meta-ads"), ("Servicios", "/#servicios"), ("Cómo trabajamos", "/#como-trabajamos"), ("Sobre nosotros", "/sobre-nosotros/"), ("Contacto", "/contacto/")],
        "cta": "Pide tu propuesta", "menu": "Abrir menú", "menu_aria": "Menú móvil", "meta_agency": "Agencia Meta Ads",
        "lang_aria": "Idioma",
        "foot_blurb": "Agencia de performance marketing para ecommerce. De la web a las ventas: tienda, Meta Ads, Google Ads, optimización y envíos en un solo equipo.",
        "foot_services": "Servicios", "foot_contact": "Contacto",
        "foot_links": [("Sobre nosotros", "/sobre-nosotros/"), ("Cómo trabajamos", "/#como-trabajamos"), ("Preguntas frecuentes", "/#faq"), ("Contacto", "/contacto/"), ("Política de privacidad", "/politica-de-privacidad/")],
        "foot_markets": "Campañas en Europa, Reino Unido, Estados Unidos, el Golfo y Australia",
        "rights": "© 2026 Grow Nest. Todos los derechos reservados.", "tagline": "Donde el crecimiento digital despega.",
        "logo_alt": "Grow Nest. Where Digital Growth Takes Flight",
        "wa_label": "Escríbenos por WhatsApp", "wa_text": "Hola%20Grow%20Nest%2C%20me%20gustar%C3%ADa%20recibir%20una%20propuesta.",
        "f_name": "Nombre", "f_email": "Email", "f_wa": "WhatsApp", "f_opt": "(opcional)", "f_web": "Web de tu tienda", "f_web_ph": "tutienda.com",
        "f_need": "¿Qué necesitas?", "f_msg": "Mensaje", "f_msg_ph": "Qué vendes, en qué países y qué quieres mejorar primero.", "f_hp": "No rellenar",
        "f_send": "Enviar mensaje", "f_note": "Usamos tus datos solo para responderte. Más información en la", "f_note_link": "política de privacidad",
        "options": ["Meta Ads", "Google Ads", "Shopify", "WhatsApp", "Email marketing", "Envíos y devoluciones", "TikTok Shop / Amazon", "Apps a medida", "Creatividades"],
        "r_phone": "WhatsApp / teléfono", "r_email": "Email", "r_addr": "Dirección", "address": "18 Albert Road, Ilford IG1 1HN, Reino Unido", "copy": "Copiar",
        "direct_aria": "Contacto directo", "contact_label": "Contacto", "contact_h2": "Haz despegar tu marca",
        "contact_lead": "Cuéntanos qué vendes y qué quieres mejorar primero. Respondemos por WhatsApp o por email.",
        "faq_label": "Preguntas frecuentes", "faq_h2": "Preguntas frecuentes", "go": "Ver servicio", "related": "También te puede interesar",
        "band_p": "Te respondemos por WhatsApp o por email con los siguientes pasos.", "home": "Inicio", "crumb_aria": "Ruta de navegación",
        "og_img_alt": "Grow Nest, agencia de Facebook y Meta Ads para ecommerce", "form_aria": "Formulario de contacto",
    },
    "en": {
        "html_lang": "en", "og_locale": "en_GB", "og_alt_locale": "es_ES",
        "skip": "Skip to content", "home_aria": "Grow Nest, home", "nav_aria": "Main",
        "nav": [("Meta Ads", "/en/#meta-ads"), ("Services", "/en/#services"), ("How we work", "/en/#how-we-work"), ("About", "/en/about/"), ("Contact", "/en/contact/")],
        "cta": "Get a proposal", "menu": "Open menu", "menu_aria": "Mobile menu", "meta_agency": "Meta Ads agency",
        "lang_aria": "Language",
        "foot_blurb": "Performance marketing agency for ecommerce. From website to sales: store, Meta Ads, Google Ads, page optimisation and shipping in one team.",
        "foot_services": "Services", "foot_contact": "Contact",
        "foot_links": [("About us", "/en/about/"), ("How we work", "/en/#how-we-work"), ("FAQ", "/en/#faq"), ("Contact", "/en/contact/"), ("Privacy policy", "/en/privacy-policy/")],
        "foot_markets": "Campaigns across Europe, the UK, the US, the Gulf and Australia",
        "rights": "© 2026 Grow Nest. All rights reserved.", "tagline": "Where digital growth takes flight.",
        "logo_alt": "Grow Nest. Where Digital Growth Takes Flight",
        "wa_label": "Message us on WhatsApp", "wa_text": "Hi%20Grow%20Nest%2C%20I%27d%20like%20a%20proposal.",
        "f_name": "Name", "f_email": "Email", "f_wa": "WhatsApp", "f_opt": "(optional)", "f_web": "Your store's website", "f_web_ph": "yourstore.com",
        "f_need": "What do you need?", "f_msg": "Message", "f_msg_ph": "What you sell, in which countries, and what you want to fix first.", "f_hp": "Do not fill",
        "f_send": "Send message", "f_note": "We only use your details to reply to you. More in our", "f_note_link": "privacy policy",
        "options": ["Meta Ads", "Google Ads", "Shopify", "WhatsApp", "Email marketing", "Shipping and returns", "TikTok Shop / Amazon", "Custom apps", "Creatives"],
        "r_phone": "WhatsApp / phone", "r_email": "Email", "r_addr": "Address", "address": "18 Albert Road, Ilford IG1 1HN, United Kingdom", "copy": "Copy",
        "direct_aria": "Direct contact", "contact_label": "Contact", "contact_h2": "Let your brand take flight",
        "contact_lead": "Tell us what you sell and what you want to fix first. We reply on WhatsApp or by email.",
        "faq_label": "FAQ", "faq_h2": "Frequently asked questions", "go": "View service", "related": "You may also like",
        "band_p": "We reply on WhatsApp or by email with the next steps.", "home": "Home", "crumb_aria": "Breadcrumb",
        "og_img_alt": "Grow Nest, Facebook and Meta Ads agency for ecommerce", "form_aria": "Contact form",
    },
}
def wa(lang): return f"https://wa.me/{WA_NUMBER}?text={UI[lang]['wa_text']}"

ICONS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9M12 3C9.5 5.7 8.2 8.7 8.2 12s1.3 6.3 3.8 9"/>',
    "megaphone": '<path d="M3 10v4a1 1 0 0 0 1 1h3l6 4V5L7 9H4a1 1 0 0 0-1 1Z"/><path d="M16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4.2-4.2"/>',
    "bag": '<path d="M6 8h12l1 12H5L6 8Z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
    "chat": '<path d="M4 20l1.4-4.1A8 8 0 1 1 8.2 18.6Z"/><path d="M9 10.5h6M9 13.5h4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "truck": '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    "cart": '<path d="M3 4h2l2.3 11h11.2L21 7H6.2"/><circle cx="9.5" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    "play": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m10 9 5 3-5 3Z"/>',
    "team": '<circle cx="9" cy="8" r="3"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.2A4.5 4.5 0 0 1 21 18.5"/>',
    "tool": '<path d="M14.5 5.5a4 4 0 0 0 4.9 4.9l-8.6 8.6a2.1 2.1 0 1 1-3-3l8.6-8.6a4 4 0 0 0-1.9-1.9Z"/>',
    "chart": '<path d="M4 20V11M10 20V5M16 20v-6M2 20h20"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}
def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

# ---------------------------------------------------------------- services
SERVICES = [
    {"key": "google", "icon": "search",
     "name": {"es": "Google Ads y Shopping", "en": "Google Ads & Shopping"}, "short": {"es": "Google Ads", "en": "Google Ads"},
     "card": {"es": "Tus productos en Google justo cuando alguien los busca.", "en": "Your products on Google right when people search for them."}},
    {"key": "shopify", "icon": "bag",
     "name": {"es": "Tiendas Shopify y B2B", "en": "Shopify stores & B2B"}, "short": {"es": "Shopify", "en": "Shopify"},
     "card": {"es": "Tiendas rápidas, páginas optimizadas para convertir y venta B2B.", "en": "Fast stores, pages optimised to convert, and B2B selling."}},
    {"key": "whatsapp", "icon": "chat",
     "name": {"es": "WhatsApp marketing", "en": "WhatsApp marketing"}, "short": {"es": "WhatsApp marketing", "en": "WhatsApp marketing"},
     "card": {"es": "Carritos recuperados y avisos de pedido que sí se leen.", "en": "Recovered carts and order updates people actually read."}},
    {"key": "email", "icon": "mail",
     "name": {"es": "Email marketing con Klaviyo", "en": "Email marketing with Klaviyo"}, "short": {"es": "Email marketing", "en": "Email marketing"},
     "card": {"es": "Flujos que siguen vendiendo después del primer pedido.", "en": "Flows that keep selling after the first order."}},
    {"key": "envios", "icon": "truck",
     "name": {"es": "Envíos y devoluciones", "en": "Shipping & returns"}, "short": {"es": "Envíos y devoluciones", "en": "Shipping & returns"},
     "card": {"es": "Seguimiento diario y menos paquetes devueltos.", "en": "Daily tracking and fewer returned parcels."}},
    {"key": "marketplaces", "icon": "cart",
     "name": {"es": "TikTok Shop y Amazon", "en": "TikTok Shop & Amazon"}, "short": {"es": "TikTok Shop y Amazon", "en": "TikTok Shop & Amazon"},
     "card": {"es": "Los pedidos de marketplace, con el mismo control que tu tienda.", "en": "Marketplace orders with the same control as your store."}},
    {"key": "apps", "icon": "code",
     "name": {"es": "Apps y dashboards a medida", "en": "Custom apps & dashboards"}, "short": {"es": "Apps a medida", "en": "Custom apps"},
     "card": {"es": "Si ninguna app lo resuelve, la creamos.", "en": "If no app solves it, we build one."}},
    {"key": None, "icon": "play",
     "name": {"es": "Creatividades y vídeos de producto", "en": "Creatives & product videos"}, "short": {"es": "Creatividades", "en": "Creatives"},
     "card": {"es": "Anuncios que frenan el scroll. Incluido en la gestión de Meta Ads.", "en": "Ads that stop the scroll. Included in Meta Ads management."}},
]

# ---------------------------------------------------------------- shared parts
def alternates(key):
    es, en = BASE + url(key, "es"), BASE + url(key, "en")
    return es, en

def head(p, lang):
    T = UI[lang]
    me = BASE + p["path"]
    es, en = alternates(p["key"]) if p.get("key") else (me, me)
    title, desc = p["title"], p["desc"]
    alt = "" if not p.get("key") else f"""<link rel="alternate" hreflang="es-ES" href="{es}">
<link rel="alternate" hreflang="en" href="{en}">
<link rel="alternate" hreflang="x-default" href="{es}">
<meta property="og:locale:alternate" content="{T['og_alt_locale']}">
"""
    return f"""<!doctype html>
<html lang="{T['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{a(desc)}">
<link rel="canonical" href="{me}">
{alt}<meta name="robots" content="{p.get('robots', 'index, follow, max-image-preview:large')}">
<meta name="theme-color" content="#08121D">
<meta property="og:type" content="website">
<meta property="og:locale" content="{T['og_locale']}">
<meta property="og:site_name" content="Grow Nest">
<meta property="og:title" content="{a(title)}">
<meta property="og:description" content="{a(desc)}">
<meta property="og:url" content="{me}">
<meta property="og:image" content="{BASE}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{a(T['og_img_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{a(title)}">
<meta name="twitter:description" content="{a(desc)}">
<meta name="twitter:image" content="{BASE}/assets/img/og-image.png">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,600..800&amp;family=IBM+Plex+Sans:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={V}">
<script type="application/ld+json">{json.dumps(jsonld(p, lang), ensure_ascii=False, separators=(',', ':'))}</script>
<script src="/assets/js/site.js?v={V}" defer></script>
<script type="module" src="/assets/js/hero.js?v={V}"></script>
</head>
<body>
<a class="skip" href="#main">{e(T['skip'])}</a>
"""

def lang_switch(p, lang):
    key = p.get("key") or "home"
    cur = ' aria-current="true"'
    return (f'<nav class="lang" aria-label="{a(UI[lang]["lang_aria"])}">'
            f'<a href="{url(key, "es")}" lang="es" hreflang="es"{cur if lang == "es" else ""}>ES</a>'
            f'<a href="{url(key, "en")}" lang="en" hreflang="en"{cur if lang == "en" else ""}>EN</a></nav>')

def header(p, lang):
    T = UI[lang]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == p["path"] else ""}>{e(t)}</a>' for t, h in T["nav"])
    mob = [(T["meta_agency"], url("home", lang))] + [(s["short"][lang], url(s["key"], lang)) for s in SERVICES if s["key"]] + [(T["nav"][3][0], url("about", lang)), (T["nav"][4][0], url("contact", lang))]
    mlinks = "".join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in mob)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{url('home', lang)}" aria-label="{a(T['home_aria'])}"><img src="/assets/img/logo-wordmark-light.png" alt="Grow Nest" width="81" height="40"></a>
    <nav class="nav" aria-label="{a(T['nav_aria'])}">{links}</nav>
    {lang_switch(p, lang)}
    <a class="btn btn-primary btn-sm header-cta" href="{url('contact', lang)}">{e(T['cta'])}</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="{a(T['menu'])}">{icon('menu')}</button>
  </div>
</header>
<nav id="mobile-menu" class="mobile-menu" aria-label="{a(T['menu_aria'])}" hidden>
  <ul>{mlinks}</ul>
  <a class="btn btn-primary" href="{url('contact', lang)}">{e(T['cta'])}</a>
</nav>
"""

def footer(lang):
    T = UI[lang]
    svc = "".join(f'<li><a href="{url(s["key"], lang)}">{e(s["short"][lang])}</a></li>' for s in SERVICES if s["key"])
    comp = "".join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in T["foot_links"])
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="logo" src="/assets/img/logo-light.png" alt="{a(T['logo_alt'])}" width="180" height="97">
        <p>{e(T['foot_blurb'])}</p>
      </div>
      <div>
        <h2>{e(T['foot_services'])}</h2>
        <ul><li><a href="{url('home', lang)}">{e(T['meta_agency'])}</a></li>{svc}</ul>
      </div>
      <div>
        <h2>Grow Nest</h2>
        <ul>{comp}</ul>
      </div>
      <div>
        <h2>{e(T['foot_contact'])}</h2>
        <ul>
          <li><a href="{wa(lang)}" target="_blank" rel="noopener">WhatsApp: {PHONE}</a></li>
          <li>{EMAIL}</li>
          <li>{e(T['foot_markets'])}</li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>{e(T['rights'])}</span>
      <span>{e(T['tagline'])}</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{wa(lang)}" target="_blank" rel="noopener" aria-label="{a(T['wa_label'])}">{icon('chat')}<span>WhatsApp</span></a>
</body>
</html>
"""

def form(pid, lang):
    T = UI[lang]
    opts = "".join(f'<label><input type="checkbox" name="servicio" value="{a(o)}"> {e(o)}</label>' for o in T["options"])
    return f"""<form class="form" data-contact novalidate>
  <div class="row">
    <label class="field" for="{pid}-nombre"><span>{e(T['f_name'])}</span><input id="{pid}-nombre" name="nombre" type="text" autocomplete="name" required></label>
    <label class="field" for="{pid}-email"><span>{e(T['f_email'])}</span><input id="{pid}-email" name="email" type="email" autocomplete="email" required></label>
  </div>
  <div class="row">
    <label class="field" for="{pid}-whatsapp"><span>{e(T['f_wa'])} <small>{e(T['f_opt'])}</small></span><input id="{pid}-whatsapp" name="whatsapp" type="tel" autocomplete="tel"></label>
    <label class="field" for="{pid}-web"><span>{e(T['f_web'])}</span><input id="{pid}-web" name="web" type="text" inputmode="url" placeholder="{a(T['f_web_ph'])}"></label>
  </div>
  <fieldset>
    <legend>{e(T['f_need'])}</legend>
    <div class="opts">{opts}</div>
  </fieldset>
  <label class="field" for="{pid}-mensaje"><span>{e(T['f_msg'])}</span><textarea id="{pid}-mensaje" name="mensaje" required placeholder="{a(T['f_msg_ph'])}"></textarea></label>
  <div class="hp" aria-hidden="true"><label>{e(T['f_hp'])} <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
  <button class="btn btn-primary" type="submit">{e(T['f_send'])} {icon('arrow')}</button>
  <p class="form-status" role="status" aria-live="polite"></p>
  <p class="form-note">{e(T['f_note'])} <a href="{url('privacy', lang)}">{e(T['f_note_link'])}</a>.</p>
</form>"""

def reach(lang, with_address=False):
    T = UI[lang]; s = "a" if with_address else "b"
    addr = f'<div class="item"><small>{e(T["r_addr"])}</small><span>{e(T["address"])}</span></div>' if with_address else ""
    return f"""<div class="reach">
  <a class="btn btn-primary" href="{wa(lang)}" target="_blank" rel="noopener">{icon('chat')} {e(T['wa_label'])}</a>
  <div class="item"><small>{e(T['r_phone'])}</small><span id="tel-{s}">{PHONE}</span><button class="copy" type="button" data-copy="+{WA_NUMBER}" aria-controls="tel-{s}">{e(T['copy'])}</button></div>
  <div class="item"><small>{e(T['r_email'])}</small><span id="mail-{s}">{EMAIL}</span><button class="copy" type="button" data-copy="{EMAIL}" aria-controls="mail-{s}">{e(T['copy'])}</button></div>
  {addr}
</div>"""

def contact_section(pid, lang, sid):
    T = UI[lang]
    return f"""<section class="section dark" id="{sid}" aria-labelledby="{pid}-title">
  <div class="wrap contact-grid">
    <div>
      <p class="label">{e(T['contact_label'])}</p>
      <h2 id="{pid}-title">{e(T['contact_h2'])}</h2>
      <p class="lead">{e(T['contact_lead'])}</p>
      <div style="margin-top:28px">{form(pid, lang)}</div>
    </div>
    <aside aria-label="{a(T['direct_aria'])}" style="padding-top:8px">{reach(lang)}</aside>
  </div>
</section>"""

def faq_html(items, h2, pid, lang):
    qs = "".join(f"<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>" for q, ans in items)
    return f"""<section class="section" id="faq" aria-labelledby="{pid}-faq">
  <div class="wrap">
    <div class="section-head"><p class="label">{e(UI[lang]['faq_label'])}</p><h2 id="{pid}-faq">{e(h2)}</h2></div>
    <div class="faq">{qs}</div>
  </div>
</section>"""

def checks(items, cols=False):
    lis = "".join(f"<li>{icon('check')}<span>{e(i)}</span></li>" for i in items)
    return f'<ul class="checks{" cols" if cols else ""}">{lis}</ul>'

def card(s, lang):
    if s["key"]:
        return f'<a class="card" href="{url(s["key"], lang)}"><span class="ico">{icon(s["icon"])}</span><h3>{e(s["name"][lang])}</h3><p>{e(s["card"][lang])}</p><span class="go">{e(UI[lang]["go"])} {icon("arrow")}</span></a>'
    return f'<div class="card"><span class="ico">{icon(s["icon"])}</span><h3>{e(s["name"][lang])}</h3><p>{e(s["card"][lang])}</p></div>'

# ---------------------------------------------------------------- JSON-LD
ORG = {
    "@type": "Organization", "@id": BASE + "/#org", "name": "Grow Nest", "url": BASE + "/",
    "logo": BASE + "/assets/img/grownest-logo.png", "email": EMAIL, "telephone": "+447429917026",
    "slogan": "Donde el crecimiento digital despega",
    "description": "Agencia de performance marketing para ecommerce: Meta Ads, Google Ads, Shopify, WhatsApp, email y envíos en un solo equipo.",
    "founder": {"@type": "Person", "name": "Ghulam Muhammad"},
    "address": {"@type": "PostalAddress", "streetAddress": "18 Albert Road", "addressLocality": "Ilford", "postalCode": "IG1 1HN", "addressCountry": "GB"},
    "areaServed": AREA, "knowsLanguage": ["es", "en"],
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+447429917026", "email": EMAIL, "availableLanguage": ["es", "en"]},
}
WEBSITE = {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Grow Nest", "inLanguage": ["es-ES", "en"], "publisher": {"@id": BASE + "/#org"}}

def jsonld(p, lang):
    me = BASE + p["path"]
    graph = [ORG, WEBSITE]
    page = {"@type": p.get("pagetype", "WebPage"), "@id": me + "#webpage", "url": me, "name": p["title"], "description": p["desc"], "inLanguage": UI[lang]["html_lang"], "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#org"}}
    if p.get("key") and p["key"] != "home":
        crumbs = [{"@type": "ListItem", "position": 1, "name": UI[lang]["home"], "item": BASE + url("home", lang)}, {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": me}]
        graph.append({"@type": "BreadcrumbList", "@id": me + "#breadcrumb", "itemListElement": crumbs})
        page["breadcrumb"] = {"@id": me + "#breadcrumb"}
    graph.append(page)
    if p.get("service"):
        graph.append({"@type": "Service", "@id": me + "#service", "name": p["service"], "serviceType": p["service"], "description": p["desc"], "url": me, "provider": {"@id": BASE + "/#org"}, "areaServed": AREA, "availableLanguage": ["es", "en"]})
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "@id": me + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in p["faq"]]})
    return {"@context": "https://schema.org", "@graph": graph}

# ---------------------------------------------------------------- home content
HOME = {
    "es": {
        "key": "home", "path": "/",
        "title": "Agencia Facebook y Meta Ads para Ecommerce | Grow Nest",
        "desc": "Agencia de Facebook y Meta Ads para ecommerce. De la web a las ventas: tienda, Meta Ads, Google Ads, optimización de páginas y envíos en un solo equipo.",
        "service": "Gestión de publicidad en Facebook e Instagram (Meta Ads) para ecommerce",
        "eyebrow": "Performance marketing · Ecommerce",
        "h1": "Agencia de Facebook y Meta Ads", "h1_grad": "para ecommerce",
        "lead": "De la web a las ventas, nos encargamos de todo: creamos tu tienda, lanzamos Meta Ads y Google Ads, optimizamos cada página y cuidamos lo que pasa después del clic.",
        "trust": "Gestionamos campañas en Europa, Reino Unido, Estados Unidos, el Golfo y Australia.",
        "platforms_label": "Plataformas con las que trabajamos a diario",
        "j_label": "Performance marketing", "j_h2": "De la web a las ventas, nos encargamos de todo",
        "j_lead": "No solo lanzamos anuncios. Creamos tu tienda, le llevamos tráfico con Meta Ads y Google Ads, optimizamos cada página y cuidamos lo que pasa después de la compra. Un solo equipo, de principio a fin.",
        "journey": [("bag", "Web y tienda", "Creamos o mejoramos tu tienda Shopify para que venda en el móvil."),
                    ("megaphone", "Meta Ads", "Campañas en Facebook e Instagram que crean demanda."),
                    ("search", "Google Ads", "Google Shopping y Búsqueda para quien ya busca tu producto."),
                    ("tool", "Optimización de páginas", "Fichas, landing pages y checkout que convierten más visitas en pedidos."),
                    ("chart", "Medición", "Píxel, API de Conversiones y GA4 que cuentan las ventas reales."),
                    ("chat", "Venta y recompra", "WhatsApp, email y envíos para que el pedido llegue y el cliente vuelva.")],
        "m_label": "Meta Ads", "m_h2": "Facebook e Instagram Ads que venden",
        "m_lead": "Somos una agencia de Meta Ads especializada en tiendas online. Creamos, lanzamos y optimizamos tus campañas de Facebook e Instagram cada semana. Medimos cada euro con los pedidos de tu tienda, no con las estimaciones de la plataforma. Y si lo que frena las ventas no es el anuncio sino la página, el checkout o el envío, también lo arreglamos.",
        "m_h3": "Qué incluye la gestión de Meta Ads",
        "m_items": ["Estrategia por país, producto y margen", "Campañas de captación, catálogo dinámico y retargeting", "Creatividades: imágenes y vídeos cortos de producto", "Píxel de Meta y API de Conversiones bien configurados", "Catálogo de productos sincronizado con tu tienda", "Pruebas A/B de anuncios y audiencias", "Informe mensual claro y avisos por WhatsApp"],
        "m_link": "Pide tu propuesta de Meta Ads",
        "phone": {"brand": "Tu marca", "sp": "Publicidad", "row": "Nueva colección", "buy": "Comprar", "toast": "Pedido confirmado", "toast_s": "Medido en tu tienda, no en la plataforma"},
        "p_id": "como-trabajamos", "p_label": "Cómo trabajamos", "p_h2": "De la auditoría a las ventas",
        "steps": [("Auditoría", "Revisamos tu cuenta publicitaria, tu medición y tu tienda. Te decimos qué falla y qué falta."),
                  ("Plan", "Recibes por escrito qué haremos, en qué orden y qué necesitamos de ti."),
                  ("Lanzamiento", "Montamos campañas, creatividades y medición, y lo revisamos todo antes de publicar."),
                  ("Optimización", "Revisión semanal, avisos por WhatsApp e informe mensual. Escalamos lo que funciona.")],
        "s_id": "servicios", "s_label": "Servicios", "s_h2": "Todo lo que tu tienda online necesita para vender más",
        "s_lead": "Las campañas funcionan mejor cuando la tienda, los mensajes y los envíos también funcionan. Por eso lo hacemos todo en el mismo equipo.",
        "band_h2": "¿No sabes por dónde empezar?", "band_p": "Revisamos tu cuenta y tu tienda, y te decimos qué arreglar primero.",
        "w_label": "Por qué Grow Nest", "w_h2": "Por qué trabajar con Grow Nest",
        "why": [("team", "De la web a las ventas", "Tienda, Meta Ads, Google Ads, optimización de páginas y envíos en el mismo equipo. Nada se pierde entre agencias."),
                ("tool", "Construimos, no solo aconsejamos", "Si falta una herramienta, la programamos."),
                ("chart", "Datos en los que confiar", "Primero arreglamos la medición. Después leemos los resultados en los pedidos de tu tienda."),
                ("lock", "Tus cuentas son tuyas", "Trabajamos con acceso de colaborador y de partner.")],
        "mk_label": "Mercados", "mk_h2": "Campañas en cualquier mercado",
        "mk_lead": "Tanto si vendes solo en España como en veinte países, lanzamos tus campañas en Europa, Reino Unido, Estados Unidos, el Golfo y donde quieras crecer, en el idioma y la moneda de cada mercado. Trabajamos en español y en inglés.",
        "markets": ["España", "Reino Unido", "Alemania", "Francia", "Países Bajos", "Estados Unidos", "Emiratos Árabes", "Australia"],
        "faq_h2": "Preguntas frecuentes sobre Facebook y Meta Ads", "contact_id": "contacto",
        "faq": [
            ("¿Qué hace una agencia de Facebook Ads?", "Planifica, crea y optimiza tus anuncios de Facebook e Instagram para vender más con el mismo presupuesto. En Grow Nest también configuramos la medición, el catálogo y las creatividades."),
            ("¿Solo gestionáis los anuncios?", "No. Nos encargamos de todo, de la web a las ventas: creamos o mejoramos tu tienda, lanzamos Meta Ads y Google Ads, optimizamos las páginas, configuramos la medición y cuidamos los mensajes y los envíos."),
            ("¿Facebook Ads y Meta Ads son lo mismo?", "Sí. Meta Ads es el nombre actual de la plataforma que publica tus anuncios en Facebook, Instagram, Messenger y el resto de apps de Meta."),
            ("¿Cuánto cuesta anunciarse en Facebook e Instagram?", "Meta no tiene una tarifa fija. Tú decides el presupuesto diario y Meta cobra por impresiones o clics. En la auditoría te recomendamos un presupuesto según tu margen y tus objetivos."),
            ("¿Cuánto cobra Grow Nest por gestionar Meta Ads?", "Depende de los mercados, las campañas y las creatividades que necesites. Te damos un precio cerrado después de la auditoría."),
            ("¿Cuánto tardan en verse los resultados?", "Los primeros datos llegan en 7 a 14 días. Hacia los 30 días ya se ve con claridad qué funciona."),
            ("¿Trabajáis solo con tiendas de España?", "No. Gestionamos campañas en Europa, Reino Unido, Estados Unidos, el Golfo, Australia y otros mercados."),
            ("¿Hay permanencia?", "No. Después de la puesta en marcha, el servicio es mes a mes."),
            ("¿Garantizáis ventas?", "No. La publicidad es probar y aprender. Garantizamos el trabajo, informes claros y consejos honestos sobre lo que funciona y lo que no."),
        ],
    },
    "en": {
        "key": "home", "path": "/en/",
        "title": "Facebook & Meta Ads Agency for Ecommerce | Grow Nest",
        "desc": "Facebook and Meta Ads agency for ecommerce. From website to sales: store, Meta Ads, Google Ads, page optimisation and shipping, all in one team.",
        "service": "Facebook and Instagram advertising (Meta Ads) management for ecommerce",
        "eyebrow": "Performance marketing · Ecommerce",
        "h1": "Facebook & Meta Ads agency", "h1_grad": "for ecommerce",
        "lead": "From website to sales, we handle everything: we build your store, run Meta Ads and Google Ads, optimise every page and look after what happens after the click.",
        "trust": "We run campaigns across Europe, the UK, the US, the Gulf and Australia.",
        "platforms_label": "Platforms we work with every day",
        "j_label": "Performance marketing", "j_h2": "From website to sales, we handle everything",
        "j_lead": "We don't just run ads. We build your store, bring it traffic with Meta Ads and Google Ads, optimise every page and look after what happens after the purchase. One team, start to finish.",
        "journey": [("bag", "Website & store", "We build or improve your Shopify store so it sells on mobile."),
                    ("megaphone", "Meta Ads", "Facebook and Instagram campaigns that create demand."),
                    ("search", "Google Ads", "Google Shopping and Search for people already looking for your product."),
                    ("tool", "Page optimisation", "Product pages, landing pages and checkout that turn more visits into orders."),
                    ("chart", "Measurement", "Meta Pixel, Conversions API and GA4 that count real sales."),
                    ("chat", "Sale & repeat order", "WhatsApp, email and shipping so the order arrives and the customer comes back.")],
        "m_label": "Meta Ads", "m_h2": "Facebook and Instagram Ads that sell",
        "m_lead": "We are a Meta Ads agency focused on online stores. We build, launch and optimise your Facebook and Instagram campaigns every week. We measure every euro against your store's orders, not the platform's estimates. And if what's holding sales back isn't the ad but the page, the checkout or the delivery, we fix that too.",
        "m_h3": "What our Meta Ads management includes",
        "m_items": ["Strategy by country, product and margin", "Prospecting, dynamic catalogue and retargeting campaigns", "Creatives: images and short product videos", "Meta Pixel and Conversions API set up properly", "Product catalogue synced with your store", "A/B tests of ads and audiences", "A clear monthly report and WhatsApp updates"],
        "m_link": "Get a Meta Ads proposal",
        "phone": {"brand": "Your brand", "sp": "Sponsored", "row": "New collection", "buy": "Shop now", "toast": "Order confirmed", "toast_s": "Measured in your store, not the platform"},
        "p_id": "how-we-work", "p_label": "How we work", "p_h2": "From audit to sales",
        "steps": [("Audit", "We review your ad account, tracking and store, and tell you what's broken and what's missing."),
                  ("Plan", "You get a written plan: what we'll do, in what order, and what we need from you."),
                  ("Launch", "We set up campaigns, creatives and tracking, and check everything before going live."),
                  ("Optimise", "Weekly reviews, WhatsApp updates and a monthly report. We scale what works.")],
        "s_id": "services", "s_label": "Services", "s_h2": "Everything your online store needs to sell more",
        "s_lead": "Campaigns work better when the store, the messages and the shipping work too. That's why we do it all in one team.",
        "band_h2": "Not sure where to start?", "band_p": "We review your account and your store and tell you what to fix first.",
        "w_label": "Why Grow Nest", "w_h2": "Why work with Grow Nest",
        "why": [("team", "From website to sales", "Store, Meta Ads, Google Ads, page optimisation and shipping in one team. Nothing falls between agencies."),
                ("tool", "We build, not just advise", "If a tool is missing, we code it."),
                ("chart", "Numbers you can trust", "We fix tracking first, then read results from your store's orders."),
                ("lock", "Your accounts stay yours", "We work through collaborator and partner access.")],
        "mk_label": "Markets", "mk_h2": "Campaigns in any market",
        "mk_lead": "Whether you sell only in Spain or in twenty countries, we launch your campaigns across Europe, the UK, the US, the Gulf and wherever you want to grow, in each market's language and currency. We work in Spanish and English.",
        "markets": ["Spain", "United Kingdom", "Germany", "France", "Netherlands", "United States", "UAE", "Australia"],
        "faq_h2": "Facebook and Meta Ads: frequently asked questions", "contact_id": "contact",
        "faq": [
            ("What does a Facebook Ads agency do?", "It plans, creates and optimises your Facebook and Instagram ads so they sell more on the same budget. At Grow Nest we also set up tracking, the product catalogue and the creatives."),
            ("Do you only manage the ads?", "No. We handle everything from website to sales: we build or improve your store, run Meta Ads and Google Ads, optimise the pages, set up tracking and look after messages and shipping."),
            ("Are Facebook Ads and Meta Ads the same thing?", "Yes. Meta Ads is the current name of the platform that runs your ads on Facebook, Instagram, Messenger and Meta's other apps."),
            ("How much does it cost to advertise on Facebook and Instagram?", "Meta has no fixed price. You set a daily budget and Meta charges for impressions or clicks. In the audit we recommend a budget based on your margin and goals."),
            ("How much does Grow Nest charge to manage Meta Ads?", "It depends on the markets, campaigns and creatives you need. We give you a fixed quote after the audit."),
            ("How soon will I see results?", "First data arrives in 7 to 14 days. By around 30 days it's clear what works."),
            ("Do you only work with stores in Spain?", "No. We run campaigns across Europe, the UK, the US, the Gulf, Australia and other markets."),
            ("Is there a minimum contract?", "No. After the setup period, the service runs month to month."),
            ("Do you guarantee sales?", "No. Advertising means testing and learning. We guarantee the work, clear reporting and honest advice about what is and isn't working."),
        ],
    },
}

def build_home(lang):
    p, T = HOME[lang], UI[lang]
    P = p["phone"]
    journey = "".join(f'<li><span class="ico">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, t, d in p["journey"])
    steps = "".join(f'<li><span class="n">0{i}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(p["steps"], 1))
    why = "".join(f'<li>{icon(i)}<div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, t, d in p["why"])
    cards = "".join(card(s, lang) for s in SERVICES)
    chips = "".join(f"<li>{e(m)}</li>" for m in p["markets"])
    platforms = "".join(f"<li>{e(x)}</li>" for x in ["Meta Ads", "Google Ads", "Shopify", "Klaviyo", "WhatsApp Business API", "TikTok Shop", "Amazon", "GA4"])
    cid = p["contact_id"]
    body = f"""{header(p, lang)}
<main id="main">
<section class="hero" data-field-host aria-labelledby="h1">
  <div class="wrap">
    <div class="hero-copy">
      <p class="label">{e(p['eyebrow'])}</p>
      <h1 id="h1">{e(p['h1'])} <span class="grad-text">{e(p['h1_grad'])}</span></h1>
      <p class="lead">{e(p['lead'])}</p>
      <div class="actions">
        <a class="btn btn-primary" href="#{cid}">{e(T['cta'])} {icon('arrow')}</a>
        <a class="btn btn-light" href="{wa(lang)}" target="_blank" rel="noopener">{icon('chat')} {e(T['wa_label'])}</a>
      </div>
      <p class="trust">{icon('globe')}{e(p['trust'])}</p>
    </div>
    <div class="hero-visual"><canvas data-shapes="growth,phone,bag" aria-hidden="true"></canvas></div>
  </div>
</section>
<section class="platforms" aria-label="{a(p['platforms_label'])}">
  <div class="wrap"><p>{e(p['platforms_label'])}</p><ul>{platforms}</ul></div>
</section>
<section class="section soft" id="performance" aria-labelledby="perf-title">
  <div class="wrap">
    <div class="section-head"><p class="label">{e(p['j_label'])}</p><h2 id="perf-title">{e(p['j_h2'])}</h2><p class="lead">{e(p['j_lead'])}</p></div>
    <ol class="journey">{journey}</ol>
  </div>
</section>
<section class="section" id="meta-ads" aria-labelledby="meta-title">
  <div class="wrap split">
    <div>
      <p class="label">{e(p['m_label'])}</p>
      <h2 id="meta-title">{e(p['m_h2'])}</h2>
      <p class="lead">{e(p['m_lead'])}</p>
      <h3 style="margin-top:28px">{e(p['m_h3'])}</h3>
      {checks(p['m_items'])}
      <a class="more-link" href="#{cid}">{e(p['m_link'])} {icon('arrow')}</a>
    </div>
    <div class="phone-wrap" aria-hidden="true">
      <div class="phone"><div class="screen">
        <div class="ad-top"><i></i><div><b>{e(P['brand'])}</b><small>{e(P['sp'])}</small></div></div>
        <div class="ad-img"></div>
        <div class="ad-row">{e(P['row'])}<span>{e(P['buy'])}</span></div>
        <div class="ad-lines"><i></i><i></i></div>
      </div></div>
      <div class="toast">{icon('check')}<div>{e(P['toast'])}<small>{e(P['toast_s'])}</small></div></div>
    </div>
  </div>
</section>
<section class="section soft" id="{p['p_id']}" aria-labelledby="proc-title">
  <div class="wrap">
    <div class="section-head"><p class="label">{e(p['p_label'])}</p><h2 id="proc-title">{e(p['p_h2'])}</h2></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>
<section class="section" id="{p['s_id']}" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="section-head"><p class="label">{e(p['s_label'])}</p><h2 id="svc-title">{e(p['s_h2'])}</h2><p class="lead">{e(p['s_lead'])}</p></div>
    <div class="cards">{cards}</div>
    <div class="band" style="margin-top:44px">
      <div><h2>{e(p['band_h2'])}</h2><p>{e(p['band_p'])}</p></div>
      <div class="actions"><a class="btn btn-primary" href="#{cid}">{e(T['cta'])}</a></div>
    </div>
  </div>
</section>
<section class="section soft" aria-labelledby="why-title">
  <div class="wrap">
    <div class="section-head"><p class="label">{e(p['w_label'])}</p><h2 id="why-title">{e(p['w_h2'])}</h2></div>
    <ul class="why">{why}</ul>
  </div>
</section>
<section class="section dark" data-field-host aria-labelledby="mk-title">
  <div class="wrap split">
    <div>
      <p class="label">{e(p['mk_label'])}</p>
      <h2 id="mk-title">{e(p['mk_h2'])}</h2>
      <p class="lead">{e(p['mk_lead'])}</p>
      <ul class="chips">{chips}</ul>
    </div>
    <div class="globe-box"><canvas data-shapes="globe" data-count="1500" aria-hidden="true"></canvas></div>
  </div>
</section>
{faq_html(p['faq'], p['faq_h2'], 'home', lang)}
{contact_section('home', lang, cid)}
</main>
{footer(lang)}"""
    return head(p, lang) + body

# ---------------------------------------------------------------- service pages
SERVICE_PAGES = {
    "google": {
        "shape": "search",
        "es": {"crumb": "Agencia Google Ads", "service": "Gestión de Google Ads y Google Shopping para ecommerce",
               "title": "Agencia Google Ads y Shopping para Ecommerce | Grow Nest",
               "desc": "Campañas de Google Shopping y Búsqueda para tiendas online, con medición limpia y limpieza de búsquedas cada semana.",
               "label": "Google Ads", "h1": "Agencia Google Ads para ecommerce",
               "intro": "Llevamos tus productos a Google Shopping y a la Búsqueda justo cuando alguien los está buscando. Gestionamos campañas de Google Ads para tiendas online en varios países, con medición limpia y revisión semanal.",
               "blocks": [{"h2": "Qué incluye nuestra gestión de Google Ads", "items": ["Campañas de Google Shopping, Búsqueda, Display y YouTube", "Alta y revisión de Google Merchant Center y del feed de productos", "Campañas por país: Europa, Reino Unido, Estados Unidos y el Golfo", "Limpieza de términos de búsqueda y listas de palabras clave negativas", "GA4 y Google Tag Manager con las conversiones bien definidas", "Informe mensual con ventas reales, no solo clics"]},
                          {"h2": "Resultados medidos en tu tienda", "para": "Google Ads cuenta las conversiones a su manera. Nosotros contrastamos cada campaña con los pedidos de tu tienda y las UTM, y decidimos el presupuesto con esos datos."}],
               "faq": [("¿Qué es Google Shopping?", "Son los anuncios con foto, precio y nombre de la tienda que aparecen al buscar un producto. Salen del feed de productos de Merchant Center."),
                       ("¿Google Ads o Meta Ads?", "Google llega a quien ya busca tu producto. Meta crea demanda en quien todavía no lo busca. La mayoría de tiendas necesita los dos."),
                       ("¿Cuánto tarda Google Ads en dar resultados?", "Los primeros datos llegan en 7 a 14 días. Hacia los 30 días ya se ve qué campañas merecen más presupuesto.")],
               "cta": "Pide tu propuesta de Google Ads", "related": ("home", "megaphone", "Agencia de Facebook y Meta Ads", "Campañas en Facebook e Instagram medidas con tus pedidos reales.")},
        "en": {"crumb": "Google Ads agency", "service": "Google Ads and Google Shopping management for ecommerce",
               "title": "Google Ads & Shopping Agency for Ecommerce | Grow Nest",
               "desc": "Google Shopping and Search campaigns for online stores, with clean tracking and weekly search-term clean-up.",
               "label": "Google Ads", "h1": "Google Ads agency for ecommerce",
               "intro": "We put your products on Google Shopping and Search right when people are looking for them. We run Google Ads for online stores in several countries, with clean tracking and weekly reviews.",
               "blocks": [{"h2": "What our Google Ads management includes", "items": ["Google Shopping, Search, Display and YouTube campaigns", "Google Merchant Center and product feed setup and review", "Campaigns by country: Europe, the UK, the US and the Gulf", "Search-term clean-up and negative keyword lists", "GA4 and Google Tag Manager with clearly defined conversions", "A monthly report with real sales, not just clicks"]},
                          {"h2": "Results measured in your store", "para": "Google Ads counts conversions its own way. We check every campaign against your store's orders and UTMs, and set budgets from that data."}],
               "faq": [("What is Google Shopping?", "The ads with a photo, price and store name that appear when you search for a product. They come from your product feed in Merchant Center."),
                       ("Google Ads or Meta Ads?", "Google reaches people already searching for your product. Meta creates demand among people who aren't searching yet. Most stores need both."),
                       ("How long does Google Ads take to work?", "First data arrives in 7 to 14 days. By around 30 days you can see which campaigns deserve more budget.")],
               "cta": "Get a Google Ads proposal", "related": ("home", "megaphone", "Facebook & Meta Ads agency", "Facebook and Instagram campaigns measured against your real orders.")},
    },
    "shopify": {
        "shape": "bag",
        "es": {"crumb": "Agencia Shopify", "service": "Desarrollo de tiendas Shopify y Shopify B2B",
               "title": "Agencia Shopify en España: Tiendas y B2B | Grow Nest",
               "desc": "Creamos tiendas Shopify rápidas, optimizamos cada página para convertir y montamos venta al por mayor con Shopify B2B nativo.",
               "label": "Shopify", "h1": "Agencia Shopify en España: tiendas y B2B",
               "intro": "Creamos y mejoramos tiendas Shopify rápidas que venden en el móvil. Y si vendes al por mayor, lo montamos con Shopify B2B nativo, en la misma tienda y sin apps extra.",
               "blocks": [{"h2": "Desarrollo de tiendas Shopify", "items": ["Tiendas nuevas y rediseños", "Temas y secciones a medida en Liquid", "Mercados, monedas, impuestos y zonas de envío", "Google Merchant Center y feeds de producto", "Shopify Flow, formularios y facturas con Order Printer", "Velocidad, móvil y checkout", "Optimización de fichas de producto y landing pages para convertir más visitas en pedidos"]},
                          {"h2": "Shopify B2B para vender al por mayor", "items": ["Cuentas de empresa, listas de precios y precios por cantidad", "Productos solo para mayoristas y envíos B2B propios", "Landing de mayoristas que capta clientes profesionales", "CRM de leads con seguimiento por WhatsApp y email"]}],
               "faq": [("¿Shopify sirve para vender al por mayor?", "Sí. Shopify B2B permite cuentas de empresa, precios propios y pedidos por volumen sin abrir una segunda tienda."),
                       ("¿Podré editar la tienda yo mismo?", "Sí. Creamos secciones que se editan desde el editor de Shopify, sin tocar código."),
                       ("¿Trabajáis con WooCommerce?", "Sí, si tu tienda ya funciona en WooCommerce. Para tiendas nuevas recomendamos Shopify.")],
               "cta": "Pide tu propuesta de Shopify", "related": ("envios", "truck", "Envíos y devoluciones", "Tarifas, etiquetas y seguimiento para cada pedido.")},
        "en": {"crumb": "Shopify agency", "service": "Shopify store development and Shopify B2B",
               "title": "Shopify Agency in Spain: Stores & B2B | Grow Nest",
               "desc": "We build fast Shopify stores, optimise every page to convert and set up wholesale with native Shopify B2B.",
               "label": "Shopify", "h1": "Shopify agency in Spain: stores and B2B",
               "intro": "We build and improve fast Shopify stores that sell on mobile. If you sell wholesale, we set it up with native Shopify B2B, in the same store and without extra apps.",
               "blocks": [{"h2": "Shopify store development", "items": ["New stores and redesigns", "Custom themes and Liquid sections", "Markets, currencies, taxes and shipping zones", "Google Merchant Center and product feeds", "Shopify Flow, forms, and Order Printer invoices", "Speed, mobile and checkout", "Product page and landing page optimisation to turn more visits into orders"]},
                          {"h2": "Shopify B2B for wholesale", "items": ["Company accounts, price lists and volume pricing", "Wholesale-only products and separate B2B shipping rules", "Wholesale landing pages that capture trade leads", "A lead CRM with WhatsApp and email follow-up"]}],
               "faq": [("Can Shopify handle wholesale?", "Yes. Shopify B2B gives you company accounts, custom prices and bulk orders without opening a second store."),
                       ("Will I be able to edit the store myself?", "Yes. We build sections you edit in the Shopify editor, with no code."),
                       ("Do you work with WooCommerce?", "Yes, if your store already runs on WooCommerce. For new stores we recommend Shopify.")],
               "cta": "Get a Shopify proposal", "related": ("envios", "truck", "Shipping & returns", "Rates, labels and tracking for every order.")},
    },
    "whatsapp": {
        "shape": "chat",
        "es": {"crumb": "WhatsApp marketing", "service": "WhatsApp marketing y WhatsApp Business API para ecommerce",
               "title": "Agencia WhatsApp Marketing para Ecommerce | Grow Nest",
               "desc": "WhatsApp Business API conectado a tu tienda: carritos recuperados, avisos de pedido y envío, y campañas que se leen.",
               "label": "WhatsApp marketing", "h1": "Agencia de WhatsApp marketing para ecommerce",
               "intro": "Conectamos la API de WhatsApp Business a tu tienda y automatizamos los mensajes que recuperan ventas y ahorran trabajo a tu equipo. Mensajes que tus clientes sí abren.",
               "blocks": [{"h2": "Qué automatizamos en WhatsApp", "items": ["Alta de WhatsApp Business API y aprobación de plantillas", "Recuperación de carritos y checkouts abandonados", "Confirmación de pedido, envío y entrega", "Avisos de vuelta al stock", "Campañas a listas grandes de clientes", "Bandeja compartida para tu equipo"]},
                          {"h2": "Cómo recuperamos un carrito abandonado", "flow": ["El cliente deja productos en el carrito sin pagar.", "Recibe un WhatsApp con su carrito y un enlace directo para terminar la compra.", "Si no compra, le llega un segundo recordatorio más tarde."]}],
               "faq": [("¿Qué es la API de WhatsApp Business?", "Es la versión oficial de WhatsApp para empresas. Permite enviar mensajes automáticos desde tu tienda con plantillas aprobadas por Meta."),
                       ("¿Puedo escribir a todos mis clientes por WhatsApp?", "Solo a los que han dado su consentimiento. Te ayudamos a recogerlo en el checkout y en tus formularios."),
                       ("¿Funciona con Shopify?", "Sí. Conectamos WhatsApp a los eventos de tu tienda: carrito, pedido, envío y entrega.")],
               "cta": "Pide tu propuesta de WhatsApp", "related": ("email", "mail", "Email marketing para ecommerce", "Flujos de Klaviyo que venden después del primer pedido.")},
        "en": {"crumb": "WhatsApp marketing", "service": "WhatsApp marketing and WhatsApp Business API for ecommerce",
               "title": "WhatsApp Marketing Agency for Ecommerce | Grow Nest",
               "desc": "WhatsApp Business API connected to your store: recovered carts, order and delivery updates, and campaigns people read.",
               "label": "WhatsApp marketing", "h1": "WhatsApp marketing agency for ecommerce",
               "intro": "We connect the WhatsApp Business API to your store and automate the messages that recover sales and save your team time. Messages your customers actually open.",
               "blocks": [{"h2": "What we automate on WhatsApp", "items": ["WhatsApp Business API setup and template approval", "Abandoned cart and checkout recovery", "Order, shipping and delivery updates", "Back-in-stock alerts", "Campaigns to large customer lists", "A shared inbox for your team"]},
                          {"h2": "How we recover an abandoned cart", "flow": ["The customer leaves products in the cart without paying.", "They get a WhatsApp message with their cart and a direct link to finish buying.", "If they don't buy, a second reminder arrives later."]}],
               "faq": [("What is the WhatsApp Business API?", "The official version of WhatsApp for businesses. It sends automatic messages from your store using templates approved by Meta."),
                       ("Can I message all my customers on WhatsApp?", "Only those who have given consent. We help you collect it at checkout and in your forms."),
                       ("Does it work with Shopify?", "Yes. We connect WhatsApp to your store's events: cart, order, shipping and delivery.")],
               "cta": "Get a WhatsApp proposal", "related": ("email", "mail", "Email marketing for ecommerce", "Klaviyo flows that sell after the first order.")},
    },
    "email": {
        "shape": "mail",
        "es": {"crumb": "Email marketing", "service": "Email marketing y Klaviyo para ecommerce",
               "title": "Agencia Email Marketing Ecommerce y Klaviyo | Grow Nest",
               "desc": "Flujos de Klaviyo que venden después del primer pedido, enviados desde un dominio que llega a la bandeja de entrada.",
               "label": "Email marketing", "h1": "Agencia de email marketing para ecommerce",
               "intro": "Creamos flujos y campañas en Klaviyo o Shopify Email que siguen vendiendo después del primer pedido. Enviados desde un dominio que llega a la bandeja de entrada, no a spam.",
               "blocks": [{"h2": "Flujos de email que montamos", "items": ["Bienvenida para nuevos suscriptores", "Carrito y checkout abandonado", "Productos vistos y no comprados", "Post-compra: gracias, reseña y siguiente compra", "Recuperación de clientes inactivos"]},
                          {"h2": "Qué más incluye", "items": ["Formularios y popups de suscripción", "Segmentos y calendario de campañas", "Entregabilidad: SPF, DKIM, DMARC y dominio de envío propio"]}],
               "faq": [("¿Klaviyo o Shopify Email?", "Shopify Email basta para empezar. Klaviyo es mejor cuando necesitas segmentos avanzados y flujos con varias ramas."),
                       ("¿Por qué mis emails llegan a spam?", "Casi siempre es la configuración del dominio: SPF, DKIM o DMARC. Lo revisamos y lo corregimos.")],
               "cta": "Pide tu propuesta de email marketing", "related": ("whatsapp", "chat", "WhatsApp marketing", "Carritos recuperados y avisos de pedido por WhatsApp.")},
        "en": {"crumb": "Email marketing", "service": "Email marketing and Klaviyo for ecommerce",
               "title": "Email Marketing & Klaviyo Agency for Ecommerce | Grow Nest",
               "desc": "Klaviyo flows that keep selling after the first order, sent from a domain that reaches the inbox.",
               "label": "Email marketing", "h1": "Email marketing agency for ecommerce",
               "intro": "We build Klaviyo or Shopify Email flows and campaigns that keep selling after the first order. Sent from a domain that lands in the inbox, not in spam.",
               "blocks": [{"h2": "Email flows we build", "items": ["Welcome series for new subscribers", "Abandoned cart and checkout", "Browse abandonment", "Post-purchase: thank you, review and next order", "Win-back for inactive customers"]},
                          {"h2": "What else is included", "items": ["Signup forms and pop-ups", "Segments and a campaign calendar", "Deliverability: SPF, DKIM, DMARC and your own sending domain"]}],
               "faq": [("Klaviyo or Shopify Email?", "Shopify Email is enough to start. Klaviyo is better when you need advanced segments and flows with several branches."),
                       ("Why do my emails land in spam?", "Almost always it's the domain setup: SPF, DKIM or DMARC. We check it and fix it.")],
               "cta": "Get an email marketing proposal", "related": ("whatsapp", "chat", "WhatsApp marketing", "Recovered carts and order updates on WhatsApp.")},
    },
    "envios": {
        "shape": "van",
        "es": {"crumb": "Envíos y devoluciones", "service": "Logística de envíos y devoluciones para ecommerce",
               "title": "Envíos y Devoluciones para Ecommerce | Grow Nest",
               "desc": "Tarifas, etiquetas, seguimiento diario y alertas de devolución para que cada paquete llegue a su destino.",
               "label": "Envíos y devoluciones", "h1": "Envíos y devoluciones para ecommerce",
               "intro": "Nuestro trabajo no acaba en el checkout. Configuramos tarifas, etiquetas y seguimiento para que cada paquete llegue a su destino, y te avisamos antes de que vuelva.",
               "blocks": [{"h2": "Qué hacemos en logística", "items": ["Tarifas de transportistas y zonas de envío por peso (FedEx, Correos)", "Calculadoras de envío en la tienda y barras de envío gratis por país", "Generación de etiquetas y archivos de envío masivos", "Seguimiento diario de cada pedido, con alertas de paquetes parados", "Recordatorios al cliente para recoger su paquete antes de que se devuelva", "App de escaneo para paquetes de salida y devueltos en el almacén"]},
                          {"h2": "Menos devoluciones, más pedidos entregados", "para": "Muchos paquetes vuelven porque el cliente no estaba en casa o no sabe que su pedido le espera en la oficina. Nuestro seguimiento detecta esos casos a tiempo y le envía al cliente la dirección de recogida."}],
               "faq": [("¿Con qué transportistas trabajáis?", "FedEx y Correos. Si usas otro, cuéntanoslo y lo revisamos."),
                       ("¿Sirve también para pedidos de marketplace?", "Sí. Los pedidos de Shopify, TikTok Shop y Amazon se siguen en el mismo sistema.")],
               "cta": "Pide tu propuesta de logística", "related": ("marketplaces", "cart", "TikTok Shop y Amazon", "Pedidos y fichas de marketplace bajo el mismo control.")},
        "en": {"crumb": "Shipping & returns", "service": "Shipping and returns logistics for ecommerce",
               "title": "Ecommerce Shipping & Returns Management | Grow Nest",
               "desc": "Rates, labels, daily tracking and return alerts so every parcel reaches its destination.",
               "label": "Shipping & returns", "h1": "Shipping and returns for ecommerce",
               "intro": "Our work doesn't stop at checkout. We set up rates, labels and tracking so every parcel arrives, and we warn you before one comes back.",
               "blocks": [{"h2": "What we do in logistics", "items": ["Carrier rates and weight-based shipping zones (FedEx, Correos)", "Shipping calculators and free-shipping bars by country", "Label generation and bulk shipping files", "Daily tracking of every order, with alerts for stuck parcels", "Reminders that get customers to collect parcels before they're returned", "A warehouse scanning app for outgoing and returned parcels"]},
                          {"h2": "Fewer returns, more delivered orders", "para": "Many parcels come back because the customer wasn't home or doesn't know the order is waiting at the post office. Our tracking spots these cases in time and sends the customer the pickup address."}],
               "faq": [("Which carriers do you work with?", "FedEx and Correos. If you use another one, tell us and we'll look at it."),
                       ("Does it work for marketplace orders too?", "Yes. Orders from Shopify, TikTok Shop and Amazon are tracked in the same system.")],
               "cta": "Get a shipping proposal", "related": ("marketplaces", "cart", "TikTok Shop & Amazon", "Marketplace orders and listings under the same control.")},
    },
    "marketplaces": {
        "shape": "cart",
        "es": {"crumb": "TikTok Shop y Amazon", "service": "Gestión de TikTok Shop y Amazon para marcas",
               "title": "Agencia TikTok Shop y Amazon para Marcas | Grow Nest",
               "desc": "Alta, fichas, pedidos y archivos de envío en TikTok Shop y Amazon, con el mismo control que tu propia tienda.",
               "label": "TikTok Shop y Amazon", "h1": "Agencia TikTok Shop y Amazon para marcas",
               "intro": "Gestionamos tus pedidos y tus fichas en TikTok Shop y Amazon con el mismo cuidado que tu propia tienda.",
               "blocks": [{"h2": "TikTok Shop", "items": ["Alta de la tienda, fichas de producto y procesamiento de pedidos", "Archivos de envío y subida del número de seguimiento", "Auditorías de ventas, afiliados y liquidaciones"]},
                          {"h2": "Amazon", "items": ["Fichas de producto: título, bullets, descripción y palabras clave, también para Amazon.es", "Archivos de envío y seguimiento"]},
                          {"h2": "Todo bajo el mismo control", "para": "Los pedidos de TikTok Shop y Amazon entran en el mismo sistema de seguimiento de envíos que tu tienda. Ves en un solo sitio qué está en camino, qué está parado y qué vuelve."}],
               "faq": [("¿Podéis adaptar mis fichas de Shopify a Amazon.es?", "Sí. Convertimos tus descripciones de Shopify en fichas de Amazon.es en español: título, bullets, descripción y palabras clave."),
                       ("¿Revisáis lo que me paga TikTok Shop?", "Sí. Cruzamos pedidos, comisiones de afiliados y liquidaciones para que sepas cuánto ganas de verdad.")],
               "cta": "Pide tu propuesta de marketplace", "related": ("envios", "truck", "Envíos y devoluciones", "Seguimiento diario y menos paquetes devueltos.")},
        "en": {"crumb": "TikTok Shop & Amazon", "service": "TikTok Shop and Amazon management for brands",
               "title": "TikTok Shop & Amazon Agency for Brands | Grow Nest",
               "desc": "Setup, listings, orders and shipping files on TikTok Shop and Amazon, with the same control as your own store.",
               "label": "TikTok Shop & Amazon", "h1": "TikTok Shop and Amazon agency for brands",
               "intro": "We manage your orders and listings on TikTok Shop and Amazon with the same care as your own store.",
               "blocks": [{"h2": "TikTok Shop", "items": ["Shop setup, product listings and order processing", "Shipping files and tracking number uploads", "Sales, affiliate and settlement audits"]},
                          {"h2": "Amazon", "items": ["Product listings: title, bullet points, description and keywords, including Amazon.es", "Shipping files and tracking"]},
                          {"h2": "Everything under one control", "para": "TikTok Shop and Amazon orders go into the same shipment-tracking system as your store. You see in one place what's on the way, what's stuck and what's coming back."}],
               "faq": [("Can you turn my Shopify listings into Amazon.es listings?", "Yes. We turn your Shopify descriptions into Spanish Amazon.es listings: title, bullet points, description and keywords."),
                       ("Do you check what TikTok Shop pays me?", "Yes. We match orders, affiliate commissions and settlements so you know what you really earn.")],
               "cta": "Get a marketplace proposal", "related": ("envios", "truck", "Shipping & returns", "Daily tracking and fewer returned parcels.")},
    },
    "apps": {
        "shape": "code",
        "es": {"crumb": "Apps a medida", "service": "Desarrollo de apps y dashboards a medida para ecommerce",
               "title": "Desarrollo de Apps a Medida para Ecommerce | Grow Nest",
               "desc": "Cuando ninguna app hace lo que necesitas, la creamos: apps web, integraciones y paneles para tu equipo.",
               "label": "Apps a medida", "h1": "Desarrollo de apps y dashboards a medida para ecommerce",
               "intro": "Cuando ninguna app hace lo que necesitas, la construimos. Apps web, herramientas internas y paneles conectados a tu tienda Shopify, tus marketplaces y tus transportistas.",
               "blocks": [{"h2": "Qué construimos", "items": ["Apps web con Next.js y Supabase", "Paneles de pedidos, ventas y devoluciones", "Herramientas de navegador que funcionan sin conexión, sin instalar nada", "Apps de facturación", "Integraciones por API entre Shopify, TikTok Shop, Amazon, transportistas y CRM"]},
                          {"h2": "Herramientas que ya hemos creado", "items": ["Un sistema que sigue cada envío a diario y avisa de los paquetes parados", "Una app de escaneo de etiquetas para el almacén", "Un convertidor de archivos de envío entre marketplaces", "Un panel de auditoría de ventas de TikTok Shop"]}],
               "faq": [("¿Cuánto tarda una herramienta a medida?", "Depende del alcance. Después de la auditoría te damos un plan por fases, con lo que entregamos en cada una."),
                       ("¿Se conecta con lo que ya uso?", "Sí. Trabajamos con las APIs de Shopify, marketplaces, transportistas y CRM.")],
               "cta": "Cuéntanos qué necesitas", "related": ("shopify", "bag", "Agencia Shopify", "Tiendas Shopify rápidas y venta B2B nativa.")},
        "en": {"crumb": "Custom apps", "service": "Custom apps and dashboards for ecommerce",
               "title": "Custom Apps & Dashboards for Ecommerce | Grow Nest",
               "desc": "When no app does what you need, we build it: web apps, integrations and dashboards for your team.",
               "label": "Custom apps", "h1": "Custom apps and dashboards for ecommerce",
               "intro": "When no app does what you need, we build it. Web apps, internal tools and dashboards connected to your Shopify store, your marketplaces and your carriers.",
               "blocks": [{"h2": "What we build", "items": ["Web apps with Next.js and Supabase", "Order, sales and returns dashboards", "Browser tools that work offline, with nothing to install", "Invoicing and billing apps", "API integrations between Shopify, TikTok Shop, Amazon, carriers and CRMs"]},
                          {"h2": "Tools we have already built", "items": ["A system that tracks every shipment daily and flags stuck parcels", "A label-scanning app for the warehouse", "A shipping-file converter between marketplaces", "A TikTok Shop sales audit dashboard"]}],
               "faq": [("How long does a custom tool take?", "It depends on the scope. After the audit we give you a phased plan with what we deliver in each phase."),
                       ("Will it connect to what I already use?", "Yes. We work with the APIs of Shopify, marketplaces, carriers and CRMs.")],
               "cta": "Tell us what you need", "related": ("shopify", "bag", "Shopify agency", "Fast Shopify stores and native B2B selling.")},
    },
}

def hero_inner(p, lang, show_cta=True):
    T = UI[lang]
    crumbs = f'<nav aria-label="{a(T["crumb_aria"])}"><ol class="crumbs"><li><a href="{url("home", lang)}">{e(T["home"])}</a></li><li aria-current="page">{e(p["crumb"])}</li></ol></nav>'
    acts = f"""<div class="actions">
        <a class="btn btn-primary" href="{url('contact', lang)}">{e(p.get('cta', T['cta']))} {icon('arrow')}</a>
        <a class="btn btn-light" href="{wa(lang)}" target="_blank" rel="noopener">{icon('chat')} WhatsApp</a>
      </div>""" if show_cta else ""
    return f"""<section class="hero inner" data-field-host aria-labelledby="h1">
  <div class="wrap">
    <div class="hero-copy">
      {crumbs}
      <p class="label">{e(p['label'])}</p>
      <h1 id="h1">{e(p['h1'])}</h1>
      <p class="lead">{e(p['intro'])}</p>
      {acts}
    </div>
    <div class="hero-visual"><canvas data-shapes="{p['shape']}" aria-hidden="true"></canvas></div>
  </div>
</section>"""

def block_html(b):
    if b.get("items"):
        inner = checks(b["items"], cols=len(b["items"]) > 3)
    elif b.get("flow"):
        inner = '<ol class="flow">' + "".join(f"<li><span>{e(x)}</span></li>" for x in b["flow"]) + "</ol>"
    else:
        inner = f'<p class="lead">{e(b["para"])}</p>'
    return f'<div class="block"><h2>{e(b["h2"])}</h2>{inner}</div>'

def build_service(key, lang):
    T = UI[lang]
    d = SERVICE_PAGES[key]
    p = dict(d[lang], key=key, path=url(key, lang), shape=d["shape"])
    rkey, ricon, rtitle, rdesc = p["related"]
    blocks = "".join(block_html(b) for b in p["blocks"])
    body = f"""{header(p, lang)}
<main id="main">
{hero_inner(p, lang)}
<section class="section content">
  <div class="wrap">
    {blocks}
    <div class="band" style="margin-top:64px">
      <div><h2>{e(p['cta'])}</h2><p>{e(T['band_p'])}</p></div>
      <div class="actions"><a class="btn btn-primary" href="{url('contact', lang)}">{e(T['cta'])}</a><a class="btn btn-light" href="{wa(lang)}" target="_blank" rel="noopener">WhatsApp</a></div>
    </div>
    <div class="related"><p class="label">{e(T['related'])}</p>
      <a class="card" href="{url(rkey, lang)}"><span class="ico">{icon(ricon)}</span><h3>{e(rtitle)}</h3><p>{e(rdesc)}</p><span class="go">{e(T['go'])} {icon('arrow')}</span></a>
    </div>
  </div>
</section>
{faq_html(p['faq'], T['faq_h2'], key, lang)}
</main>
{footer(lang)}"""
    return p, head(p, lang) + body

# ---------------------------------------------------------------- about, contact, privacy, 404
ABOUT = {
    "es": {"crumb": "Sobre nosotros", "pagetype": "AboutPage", "title": "Sobre Grow Nest: Agencia de Marketing para Ecommerce",
           "desc": "Agencia de performance marketing para ecommerce. De la web a las ventas: tienda, Meta Ads, Google Ads, optimización de páginas y envíos.",
           "label": "Sobre nosotros", "h1": "Sobre Grow Nest", "cta": "Pide tu propuesta",
           "intro": "Grow Nest es una agencia de performance marketing para ecommerce. Nos encargamos de todo, de la web a las ventas: creamos tu tienda, lanzamos Meta Ads y Google Ads, optimizamos las páginas y cuidamos los envíos.",
           "why_h2": "Por qué existimos",
           "quote": "Una marca online no debería necesitar cinco agencias para vender. Un solo equipo debería poder montar la tienda, lanzar los anuncios, automatizar los mensajes y llevar el paquete hasta la puerta. Ese es el equipo que hemos creado.",
           "by": "Ghulam Muhammad, fundador", "how_h2": "Cómo trabajamos",
           "values": [("Claridad.", "Informes que se entienden, sin jerga."), ("Honestidad.", "No prometemos ventas; te decimos qué funciona y qué no."), ("Tus cuentas son tuyas.", "Trabajamos con acceso de colaborador y de partner."), ("Constancia.", "Revisamos tus campañas cada semana.")],
           "where_h2": "Dónde trabajamos", "where": "Con marcas que venden en Europa, Reino Unido, Estados Unidos, el Golfo y Australia. Trabajamos en español y en inglés.",
           "band_h2": "¿Hablamos de tu tienda?", "band_p": "Cuéntanos qué vendes y qué quieres mejorar primero."},
    "en": {"crumb": "About", "pagetype": "AboutPage", "title": "About Grow Nest: Performance Marketing for Ecommerce",
           "desc": "Performance marketing agency for ecommerce. From website to sales: store, Meta Ads, Google Ads, page optimisation and shipping.",
           "label": "About us", "h1": "About Grow Nest", "cta": "Get a proposal",
           "intro": "Grow Nest is a performance marketing agency for ecommerce. We handle everything from website to sales: we build your store, run Meta Ads and Google Ads, optimise the pages and look after shipping.",
           "why_h2": "Why we exist",
           "quote": "An online brand shouldn't need five agencies to sell. One team should be able to build the store, run the ads, automate the messages and get the parcel to the door. That's the team we built.",
           "by": "Ghulam Muhammad, founder", "how_h2": "How we work",
           "values": [("Clarity.", "Reports you can understand, without jargon."), ("Honesty.", "We don't promise sales; we tell you what works and what doesn't."), ("Your accounts stay yours.", "We work through collaborator and partner access."), ("Consistency.", "We review your campaigns every week.")],
           "where_h2": "Where we work", "where": "With brands selling across Europe, the UK, the US, the Gulf and Australia. We work in Spanish and English.",
           "band_h2": "Shall we talk about your store?", "band_p": "Tell us what you sell and what you want to fix first."},
}
def build_about(lang):
    T = UI[lang]
    p = dict(ABOUT[lang], key="about", path=url("about", lang), shape="nest")
    vals = "".join(f"<li>{icon('check')}<span><strong>{e(t)}</strong> {e(d)}</span></li>" for t, d in p["values"])
    body = f"""{header(p, lang)}
<main id="main">
{hero_inner(p, lang)}
<section class="section content">
  <div class="wrap">
    <div class="block"><h2>{e(p['why_h2'])}</h2>
      <blockquote class="quote"><p>{e(p['quote'])}</p><footer>{e(p['by'])}</footer></blockquote>
    </div>
    <div class="block"><h2>{e(p['how_h2'])}</h2><ul class="checks cols">{vals}</ul></div>
    <div class="block"><h2>{e(p['where_h2'])}</h2><p class="lead">{e(p['where'])}</p></div>
    <div class="band" style="margin-top:64px">
      <div><h2>{e(p['band_h2'])}</h2><p>{e(p['band_p'])}</p></div>
      <div class="actions"><a class="btn btn-primary" href="{url('contact', lang)}">{e(T['cta'])}</a></div>
    </div>
  </div>
</section>
</main>
{footer(lang)}"""
    return p, head(p, lang) + body

CONTACT = {
    "es": {"crumb": "Contacto", "pagetype": "ContactPage", "title": "Contacto | Grow Nest",
           "desc": "Cuéntanos tu tienda y qué quieres mejorar primero. Respondemos por WhatsApp o email.",
           "label": "Contacto", "h1": "Contacta con Grow Nest", "intro": "Cuéntanos qué vendes y qué quieres mejorar primero. Respondemos por WhatsApp o por email."},
    "en": {"crumb": "Contact", "pagetype": "ContactPage", "title": "Contact | Grow Nest",
           "desc": "Tell us about your store and what you want to fix first. We reply on WhatsApp or by email.",
           "label": "Contact", "h1": "Contact Grow Nest", "intro": "Tell us what you sell and what you want to fix first. We reply on WhatsApp or by email."},
}
def build_contact(lang):
    T = UI[lang]
    p = dict(CONTACT[lang], key="contact", path=url("contact", lang), shape="bird")
    body = f"""{header(p, lang)}
<main id="main">
{hero_inner(p, lang, show_cta=False)}
<section class="section dark" id="form" aria-label="{a(T['form_aria'])}">
  <div class="wrap contact-grid">
    <div>{form('contact', lang)}</div>
    <aside aria-label="{a(T['direct_aria'])}">{reach(lang, with_address=True)}</aside>
  </div>
</section>
</main>
{footer(lang)}"""
    return p, head(p, lang) + body

PRIVACY = {
    "es": {"crumb": "Política de privacidad", "title": "Política de privacidad | Grow Nest", "desc": "Cómo tratamos los datos que nos envías a través del formulario de contacto de Grow Nest.",
           "h1": "Política de privacidad", "lead": "Esta página explica qué datos recogemos cuando nos escribes y para qué los usamos.",
           "blocks": [("Quién trata tus datos", f"Grow Nest. Contacto: {EMAIL}."),
                      ("Qué datos recogemos", "Los que escribes en el formulario de contacto: nombre, email, WhatsApp (opcional), web de tu tienda, servicios que te interesan y tu mensaje. Si nos escribes por WhatsApp o email, también tu número o tu dirección de correo."),
                      ("Para qué los usamos", "Solo para responder a tu solicitud y, si trabajamos juntos, para gestionar el servicio. No los vendemos ni los usamos para enviarte publicidad sin tu permiso."),
                      ("Quién más los ve", "El formulario se envía a nuestro correo a través del servicio FormSubmit. Nuestro correo funciona con Google."),
                      ("Cuánto tiempo los guardamos", "Mientras dure la conversación o el servicio, y después el tiempo que exija la ley."),
                      ("Tus derechos", f"Puedes pedir ver, corregir o borrar tus datos, o limitar su uso, escribiendo a {EMAIL}. También puedes reclamar ante la Agencia Española de Protección de Datos."),
                      ("Cookies", "Esta web no usa cookies propias de publicidad ni de analítica.")]},
    "en": {"crumb": "Privacy policy", "title": "Privacy policy | Grow Nest", "desc": "How we handle the details you send us through the Grow Nest contact form.",
           "h1": "Privacy policy", "lead": "This page explains what data we collect when you contact us and what we use it for.",
           "blocks": [("Who handles your data", f"Grow Nest. Contact: {EMAIL}."),
                      ("What we collect", "What you type into the contact form: name, email, WhatsApp (optional), your store's website, the services you're interested in and your message. If you write to us on WhatsApp or by email, also your number or email address."),
                      ("What we use it for", "Only to reply to your request and, if we work together, to run the service. We don't sell it or use it to send you advertising without your permission."),
                      ("Who else sees it", "The form is sent to our inbox through the FormSubmit service. Our email runs on Google."),
                      ("How long we keep it", "For as long as the conversation or the service lasts, and afterwards for as long as the law requires."),
                      ("Your rights", f"You can ask to see, correct or delete your data, or limit how it's used, by writing to {EMAIL}. You can also complain to the Spanish Data Protection Agency (AEPD)."),
                      ("Cookies", "This site uses no advertising or analytics cookies of its own.")]},
}
def build_privacy(lang):
    T = UI[lang]
    p = dict(PRIVACY[lang], key="privacy", path=url("privacy", lang), pagetype="WebPage", robots="noindex, follow")
    blocks = "".join(f'<div class="block"><h2>{e(h)}</h2><p>{e(t)}</p></div>' for h, t in p["blocks"])
    body = f"""{header(p, lang)}
<main id="main">
<section class="section content">
  <div class="wrap" style="max-width:820px">
    <nav aria-label="{a(T['crumb_aria'])}"><ol class="crumbs" style="color:var(--muted)"><li><a href="{url('home', lang)}" style="color:var(--muted)">{e(T['home'])}</a></li><li aria-current="page">{e(p['crumb'])}</li></ol></nav>
    <h1 style="font-size:clamp(2rem,1.4rem + 2vw,2.8rem)">{e(p['h1'])}</h1>
    <p class="lead">{e(p['lead'])}</p>
    {blocks}
  </div>
</section>
</main>
{footer(lang)}"""
    return p, head(p, lang) + body

def build_404():
    lang = "es"
    p = {"key": None, "path": "/404.html", "crumb": "404", "title": "Página no encontrada | Grow Nest", "desc": "Esta página no existe.", "robots": "noindex, follow"}
    body = f"""{header(dict(p, key='home'), lang)}
<main id="main">
<section class="section notfound">
  <div class="wrap">
    <p class="label">Error 404</p>
    <h1 style="font-size:clamp(2rem,1.4rem + 2vw,3rem)">Esta página no existe</h1>
    <p class="lead" style="margin:0 auto 24px">Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos. <span lang="en">This page doesn't exist: go to the <a href="/en/">English home page</a>.</span></p>
    <div class="actions" style="justify-content:center"><a class="btn btn-primary" href="/">Ir al inicio</a><a class="btn btn-ghost" href="/contacto/">Contacto</a></div>
  </div>
</section>
</main>
{footer(lang)}"""
    return head(p, lang) + body

# ---------------------------------------------------------------- write
def write(path, html):
    full = os.path.join(ROOT, path.lstrip("/"))
    if full.endswith("/") or full == ROOT:
        full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.relpath(full, ROOT)

def main():
    out, indexable = [], []
    for lang in ("es", "en"):
        out.append(write(url("home", lang), build_home(lang))); indexable.append("home")
        for key in SERVICE_PAGES:
            _, html = build_service(key, lang); out.append(write(url(key, lang), html))
        for fn in (build_about, build_contact, build_privacy):
            p, html = fn(lang); out.append(write(p["path"], html))
    out.append(write("/404.html", build_404()))
    keys = ["home"] + list(SERVICE_PAGES) + ["about", "contact"]
    rows = []
    for key in keys:
        es, en = BASE + url(key, "es"), BASE + url(key, "en")
        links = f'<xhtml:link rel="alternate" hreflang="es-ES" href="{es}"/><xhtml:link rel="alternate" hreflang="en" href="{en}"/><xhtml:link rel="alternate" hreflang="x-default" href="{es}"/>'
        rows.append(f"  <url><loc>{es}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if key == 'home' else '0.8'}</priority>{links}</url>")
        rows.append(f"  <url><loc>{en}</loc><lastmod>{TODAY}</lastmod><priority>0.5</priority>{links}</url>")
    write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    print("\n".join(out))

if __name__ == "__main__":
    main()
