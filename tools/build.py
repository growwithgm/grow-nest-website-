#!/usr/bin/env python3
"""Builds the static Grow Nest site (Spanish, es-ES) into the repo root.

Run:  python3 tools/build.py
Every page gets its own title, meta description, canonical URL, Open Graph tags
and JSON-LD (Organization, WebSite, WebPage, Service, FAQPage, BreadcrumbList).
"""
import json, os, time
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.grownest.pro"
V = time.strftime("%Y%m%d%H%M")
TODAY = time.strftime("%Y-%m-%d")
WA_NUMBER = "447429917026"
WA = "https://wa.me/" + WA_NUMBER + "?text=" + "Hola%20Grow%20Nest%2C%20me%20gustar%C3%ADa%20recibir%20una%20propuesta."
PHONE = "+44 7429 917026"
EMAIL = "connect.grownest@gmail.com"
MARKETS = ["España", "Reino Unido", "Alemania", "Francia", "Países Bajos", "Estados Unidos", "Emiratos Árabes", "Australia"]
AREA = ["ES", "GB", "DE", "FR", "NL", "IT", "PT", "US", "AE", "SA", "AU"]

def e(s):
    return escape(s, quote=False)

def a(s):
    return escape(s, quote=True)

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
    "card": '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M7 15h4"/>',
}

def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

# ---------------------------------------------------------------- services
SERVICES = [
    {"key": "google", "name": "Google Ads y Shopping", "short": "Google Ads", "url": "/agencia-google-ads/", "icon": "search", "card": "Tus productos en Google justo cuando alguien los busca."},
    {"key": "shopify", "name": "Tiendas Shopify y B2B", "short": "Shopify", "url": "/agencia-shopify/", "icon": "bag", "card": "Tiendas rápidas, páginas optimizadas para convertir y venta B2B."},
    {"key": "whatsapp", "name": "WhatsApp marketing", "short": "WhatsApp marketing", "url": "/whatsapp-marketing/", "icon": "chat", "card": "Carritos recuperados y avisos de pedido que sí se leen."},
    {"key": "email", "name": "Email marketing con Klaviyo", "short": "Email marketing", "url": "/email-marketing-ecommerce/", "icon": "mail", "card": "Flujos que siguen vendiendo después del primer pedido."},
    {"key": "envios", "name": "Envíos y devoluciones", "short": "Envíos y devoluciones", "url": "/logistica-ecommerce/", "icon": "truck", "card": "Seguimiento diario y menos paquetes devueltos."},
    {"key": "marketplaces", "name": "TikTok Shop y Amazon", "short": "TikTok Shop y Amazon", "url": "/tiktok-shop-amazon/", "icon": "cart", "card": "Los pedidos de marketplace, con el mismo control que tu tienda."},
    {"key": "apps", "name": "Apps y dashboards a medida", "short": "Apps a medida", "url": "/desarrollo-a-medida/", "icon": "code", "card": "Si ninguna app lo resuelve, la creamos."},
    {"key": "creative", "name": "Creatividades y vídeos de producto", "short": "Creatividades", "url": None, "icon": "play", "card": "Anuncios que frenan el scroll. Incluido en la gestión de Meta Ads."},
]
FORM_OPTIONS = ["Meta Ads", "Google Ads", "Shopify", "WhatsApp", "Email marketing", "Envíos y devoluciones", "TikTok Shop / Amazon", "Apps a medida", "Creatividades"]

# ---------------------------------------------------------------- shared parts
def head(p):
    url = BASE + p["path"]
    title, desc = p["title"], p["desc"]
    return f"""<!doctype html>
<html lang="es-ES">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{a(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="es-ES" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="robots" content="{p.get('robots', 'index, follow, max-image-preview:large')}">
<meta name="theme-color" content="#08121D">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Grow Nest">
<meta property="og:title" content="{a(title)}">
<meta property="og:description" content="{a(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Grow Nest, agencia de Facebook y Meta Ads para ecommerce">
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
<script type="application/ld+json">{json.dumps(jsonld(p), ensure_ascii=False, separators=(',', ':'))}</script>
<script src="/assets/js/site.js?v={V}" defer></script>
<script type="module" src="/assets/js/hero.js?v={V}"></script>
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
"""

def header(p):
    nav = [("Meta Ads", "/#meta-ads"), ("Servicios", "/#servicios"), ("Cómo trabajamos", "/#como-trabajamos"), ("Sobre nosotros", "/sobre-nosotros/"), ("Contacto", "/contacto/")]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == p["path"] else ""}>{e(t)}</a>' for t, h in nav)
    mob = [("Agencia Meta Ads", "/")] + [(s["short"], s["url"]) for s in SERVICES if s["url"]] + [("Sobre nosotros", "/sobre-nosotros/"), ("Contacto", "/contacto/")]
    mlinks = "".join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in mob)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Grow Nest, inicio"><img src="/assets/img/logo-wordmark-light.png" alt="Grow Nest" width="81" height="40"></a>
    <nav class="nav" aria-label="Principal">{links}</nav>
    <a class="btn btn-primary btn-sm header-cta" href="/contacto/">Pide tu propuesta</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Abrir menú">{icon('menu')}</button>
  </div>
</header>
<nav id="mobile-menu" class="mobile-menu" aria-label="Menú móvil" hidden>
  <ul>{mlinks}</ul>
  <a class="btn btn-primary" href="/contacto/">Pide tu propuesta</a>
</nav>
"""

def footer():
    svc = "".join(f'<li><a href="{s["url"]}">{e(s["short"])}</a></li>' for s in SERVICES if s["url"])
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="logo" src="/assets/img/logo-light.png" alt="Grow Nest. Where Digital Growth Takes Flight" width="180" height="97">
        <p>Agencia de performance marketing para ecommerce. De la web a las ventas: tienda, Meta Ads, Google Ads, optimización y envíos en un solo equipo.</p>
      </div>
      <div>
        <h2>Servicios</h2>
        <ul><li><a href="/">Agencia Meta Ads</a></li>{svc}</ul>
      </div>
      <div>
        <h2>Grow Nest</h2>
        <ul>
          <li><a href="/sobre-nosotros/">Sobre nosotros</a></li>
          <li><a href="/#como-trabajamos">Cómo trabajamos</a></li>
          <li><a href="/#faq">Preguntas frecuentes</a></li>
          <li><a href="/contacto/">Contacto</a></li>
          <li><a href="/politica-de-privacidad/">Política de privacidad</a></li>
        </ul>
      </div>
      <div>
        <h2>Contacto</h2>
        <ul>
          <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp: {PHONE}</a></li>
          <li>{EMAIL}</li>
          <li>Campañas en Europa, Reino Unido, Estados Unidos, el Golfo y Australia</li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 Grow Nest. Todos los derechos reservados.</span>
      <span>Donde el crecimiento digital despega.</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{icon('chat')}<span>WhatsApp</span></a>
</body>
</html>
"""

def form(pid):
    opts = "".join(f'<label><input type="checkbox" name="servicio" value="{a(o)}"> {e(o)}</label>' for o in FORM_OPTIONS)
    return f"""<form class="form" data-contact novalidate>
  <div class="row">
    <label class="field" for="{pid}-nombre"><span>Nombre</span><input id="{pid}-nombre" name="nombre" type="text" autocomplete="name" required></label>
    <label class="field" for="{pid}-email"><span>Email</span><input id="{pid}-email" name="email" type="email" autocomplete="email" required></label>
  </div>
  <div class="row">
    <label class="field" for="{pid}-whatsapp"><span>WhatsApp <small>(opcional)</small></span><input id="{pid}-whatsapp" name="whatsapp" type="tel" autocomplete="tel"></label>
    <label class="field" for="{pid}-web"><span>Web de tu tienda</span><input id="{pid}-web" name="web" type="text" inputmode="url" placeholder="tutienda.com"></label>
  </div>
  <fieldset>
    <legend>¿Qué necesitas?</legend>
    <div class="opts">{opts}</div>
  </fieldset>
  <label class="field" for="{pid}-mensaje"><span>Mensaje</span><textarea id="{pid}-mensaje" name="mensaje" required placeholder="Qué vendes, en qué países y qué quieres mejorar primero."></textarea></label>
  <div class="hp" aria-hidden="true"><label>No rellenar <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
  <button class="btn btn-primary" type="submit">Enviar mensaje {icon('arrow')}</button>
  <p class="form-status" role="status" aria-live="polite"></p>
  <p class="form-note">Usamos tus datos solo para responderte. Más información en la <a href="/politica-de-privacidad/">política de privacidad</a>.</p>
</form>"""

def reach(with_address=False):
    addr = f"""<div class="item"><small>Dirección</small><span>18 Albert Road, Ilford IG1 1HN, Reino Unido</span></div>""" if with_address else ""
    return f"""<div class="reach">
  <a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener">{icon('chat')} Escríbenos por WhatsApp</a>
  <div class="item"><small>WhatsApp / teléfono</small><span id="tel-{'a' if with_address else 'b'}">{PHONE}</span><button class="copy" type="button" data-copy="+{WA_NUMBER}" aria-controls="tel-{'a' if with_address else 'b'}">Copiar</button></div>
  <div class="item"><small>Email</small><span id="mail-{'a' if with_address else 'b'}">{EMAIL}</span><button class="copy" type="button" data-copy="{EMAIL}" aria-controls="mail-{'a' if with_address else 'b'}">Copiar</button></div>
  {addr}
</div>"""

def contact_section(pid, h2="Haz despegar tu marca", sid="contacto"):
    return f"""<section class="section dark" id="{sid}" aria-labelledby="{pid}-title">
  <div class="wrap contact-grid">
    <div>
      <p class="label">Contacto</p>
      <h2 id="{pid}-title">{e(h2)}</h2>
      <p class="lead">Cuéntanos qué vendes y qué quieres mejorar primero. Respondemos por WhatsApp o por email.</p>
      <div style="margin-top:28px">{form(pid)}</div>
    </div>
    <aside aria-label="Contacto directo" style="padding-top:8px">{reach()}</aside>
  </div>
</section>"""

def faq_html(items, h2, pid):
    qs = "".join(f"<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>" for q, ans in items)
    return f"""<section class="section" id="faq" aria-labelledby="{pid}-faq">
  <div class="wrap">
    <div class="section-head"><p class="label">Preguntas frecuentes</p><h2 id="{pid}-faq">{e(h2)}</h2></div>
    <div class="faq">{qs}</div>
  </div>
</section>"""

def checks(items, cols=False):
    lis = "".join(f"<li>{icon('check')}<span>{e(i)}</span></li>" for i in items)
    return f'<ul class="checks{" cols" if cols else ""}">{lis}</ul>'

def card(s):
    if s["url"]:
        return f'<a class="card" href="{s["url"]}"><span class="ico">{icon(s["icon"])}</span><h3>{e(s["name"])}</h3><p>{e(s["card"])}</p><span class="go">Ver servicio {icon("arrow")}</span></a>'
    return f'<div class="card"><span class="ico">{icon(s["icon"])}</span><h3>{e(s["name"])}</h3><p>{e(s["card"])}</p></div>'

# ---------------------------------------------------------------- JSON-LD
ORG = {
    "@type": "Organization", "@id": BASE + "/#org", "name": "Grow Nest", "url": BASE + "/",
    "logo": BASE + "/assets/img/grownest-logo.png", "email": EMAIL, "telephone": "+447429917026",
    "slogan": "Donde el crecimiento digital despega", "description": "Agencia de performance marketing para ecommerce: Meta Ads, Google Ads, Shopify, WhatsApp, email y envíos en un solo equipo.", "founder": {"@type": "Person", "name": "Ghulam Muhammad"},
    "address": {"@type": "PostalAddress", "streetAddress": "18 Albert Road", "addressLocality": "Ilford", "postalCode": "IG1 1HN", "addressCountry": "GB"},
    "areaServed": AREA, "knowsLanguage": ["es", "en"],
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+447429917026", "email": EMAIL, "availableLanguage": ["es", "en"]},
}
WEBSITE = {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Grow Nest", "inLanguage": "es-ES", "publisher": {"@id": BASE + "/#org"}}

def jsonld(p):
    url = BASE + p["path"]
    graph = [ORG, WEBSITE]
    page = {"@type": p.get("pagetype", "WebPage"), "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": "es-ES", "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#org"}}
    if p["path"] != "/":
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url}]
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": crumbs})
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
    graph.append(page)
    if p.get("service"):
        graph.append({"@type": "Service", "@id": url + "#service", "name": p["service"], "serviceType": p["service"], "description": p["desc"], "url": url, "provider": {"@id": BASE + "/#org"}, "areaServed": AREA, "availableLanguage": ["es", "en"]})
    if p.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in p["faq"]]})
    return {"@context": "https://schema.org", "@graph": graph}

# ---------------------------------------------------------------- home
HOME_FAQ = [
    ("¿Qué hace una agencia de Facebook Ads?", "Planifica, crea y optimiza tus anuncios de Facebook e Instagram para vender más con el mismo presupuesto. En Grow Nest también configuramos la medición, el catálogo y las creatividades."),
    ("¿Solo gestionáis los anuncios?", "No. Nos encargamos de todo, de la web a las ventas: creamos o mejoramos tu tienda, lanzamos Meta Ads y Google Ads, optimizamos las páginas, configuramos la medición y cuidamos los mensajes y los envíos."),
    ("¿Facebook Ads y Meta Ads son lo mismo?", "Sí. Meta Ads es el nombre actual de la plataforma que publica tus anuncios en Facebook, Instagram, Messenger y el resto de apps de Meta."),
    ("¿Cuánto cuesta anunciarse en Facebook e Instagram?", "Meta no tiene una tarifa fija. Tú decides el presupuesto diario y Meta cobra por impresiones o clics. En la auditoría te recomendamos un presupuesto según tu margen y tus objetivos."),
    ("¿Cuánto cobra Grow Nest por gestionar Meta Ads?", "Depende de los mercados, las campañas y las creatividades que necesites. Te damos un precio cerrado después de la auditoría."),
    ("¿Cuánto tardan en verse los resultados?", "Los primeros datos llegan en 7 a 14 días. Hacia los 30 días ya se ve con claridad qué funciona."),
    ("¿Trabajáis solo con tiendas de España?", "No. Gestionamos campañas en Europa, Reino Unido, Estados Unidos, el Golfo, Australia y otros mercados."),
    ("¿Hay permanencia?", "No. Después de la puesta en marcha, el servicio es mes a mes."),
    ("¿Garantizáis ventas?", "No. La publicidad es probar y aprender. Garantizamos el trabajo, informes claros y consejos honestos sobre lo que funciona y lo que no."),
]
HOME = {
    "path": "/", "file": "index.html",
    "title": "Agencia Facebook y Meta Ads para Ecommerce | Grow Nest",
    "desc": "Agencia de Facebook y Meta Ads para ecommerce. De la web a las ventas: tienda, Meta Ads, Google Ads, optimización de páginas y envíos en un solo equipo.",
    "service": "Gestión de publicidad en Facebook e Instagram (Meta Ads) para ecommerce",
    "faq": HOME_FAQ,
}

def build_home():
    p = HOME
    cards = "".join(card(s) for s in SERVICES)
    steps = [("Auditoría", "Revisamos tu cuenta publicitaria, tu medición y tu tienda. Te decimos qué falla y qué falta."),
             ("Plan", "Recibes por escrito qué haremos, en qué orden y qué necesitamos de ti."),
             ("Lanzamiento", "Montamos campañas, creatividades y medición, y lo revisamos todo antes de publicar."),
             ("Optimización", "Revisión semanal, avisos por WhatsApp e informe mensual. Escalamos lo que funciona.")]
    steps_html = "".join(f'<li><span class="n">0{i}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(steps, 1))
    why = [("team", "De la web a las ventas", "Tienda, Meta Ads, Google Ads, optimización de páginas y envíos en el mismo equipo. Nada se pierde entre agencias."),
           ("tool", "Construimos, no solo aconsejamos", "Si falta una herramienta, la programamos."),
           ("chart", "Datos en los que confiar", "Primero arreglamos la medición. Después leemos los resultados en los pedidos de tu tienda."),
           ("lock", "Tus cuentas son tuyas", "Trabajamos con acceso de colaborador y de partner.")]
    why_html = "".join(f'<li>{icon(i)}<div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, t, d in why)
    meta_items = ["Estrategia por país, producto y margen", "Campañas de captación, catálogo dinámico y retargeting", "Creatividades: imágenes y vídeos cortos de producto", "Píxel de Meta y API de Conversiones bien configurados", "Catálogo de productos sincronizado con tu tienda", "Pruebas A/B de anuncios y audiencias", "Informe mensual claro y avisos por WhatsApp"]
    jsteps = [("bag", "Web y tienda", "Creamos o mejoramos tu tienda Shopify para que venda en el móvil."),
              ("megaphone", "Meta Ads", "Campañas en Facebook e Instagram que crean demanda."),
              ("search", "Google Ads", "Google Shopping y Búsqueda para quien ya busca tu producto."),
              ("tool", "Optimización de páginas", "Fichas, landing pages y checkout que convierten más visitas en pedidos."),
              ("chart", "Medición", "Píxel, API de Conversiones y GA4 que cuentan las ventas reales."),
              ("chat", "Venta y recompra", "WhatsApp, email y envíos para que el pedido llegue y el cliente vuelva.")]
    journey_html = "".join(f'<li><span class="ico">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, t, d in jsteps)
    platforms = ["Meta Ads", "Google Ads", "Shopify", "Klaviyo", "WhatsApp Business API", "TikTok Shop", "Amazon", "GA4"]
    chips = "".join(f"<li>{e(m)}</li>" for m in MARKETS)
    body = f"""{header(p)}
<main id="main">
<section class="hero" data-field-host aria-labelledby="h1">
  <div class="wrap">
    <div class="hero-copy">
      <p class="label">Performance marketing · Ecommerce</p>
      <h1 id="h1">Agencia de Facebook y Meta Ads <span class="grad-text">para ecommerce</span></h1>
      <p class="lead">De la web a las ventas, nos encargamos de todo: creamos tu tienda, lanzamos Meta Ads y Google Ads, optimizamos cada página y cuidamos lo que pasa después del clic.</p>
      <div class="actions">
        <a class="btn btn-primary" href="#contacto">Pide tu propuesta {icon('arrow')}</a>
        <a class="btn btn-light" href="{WA}" target="_blank" rel="noopener">{icon('chat')} Escríbenos por WhatsApp</a>
      </div>
      <p class="trust">{icon('globe')}Gestionamos campañas en Europa, Reino Unido, Estados Unidos, el Golfo y Australia.</p>
    </div>
    <div class="hero-visual"><canvas data-shapes="growth,phone,bag" aria-hidden="true"></canvas></div>
  </div>
</section>
<section class="platforms" aria-label="Plataformas">
  <div class="wrap"><p>Plataformas con las que trabajamos a diario</p><ul>{''.join(f'<li>{e(x)}</li>' for x in platforms)}</ul></div>
</section>
<section class="section soft" id="performance" aria-labelledby="perf-title">
  <div class="wrap">
    <div class="section-head"><p class="label">Performance marketing</p><h2 id="perf-title">De la web a las ventas, nos encargamos de todo</h2><p class="lead">No solo lanzamos anuncios. Creamos tu tienda, le llevamos tráfico con Meta Ads y Google Ads, optimizamos cada página y cuidamos lo que pasa después de la compra. Un solo equipo, de principio a fin.</p></div>
    <ol class="journey">{journey_html}</ol>
  </div>
</section>
<section class="section" id="meta-ads" aria-labelledby="meta-title">
  <div class="wrap split">
    <div>
      <p class="label">Meta Ads</p>
      <h2 id="meta-title">Facebook e Instagram Ads que venden</h2>
      <p class="lead">Somos una agencia de Meta Ads especializada en tiendas online. Creamos, lanzamos y optimizamos tus campañas de Facebook e Instagram cada semana. Medimos cada euro con los pedidos de tu tienda, no con las estimaciones de la plataforma. Y si lo que frena las ventas no es el anuncio sino la página, el checkout o el envío, también lo arreglamos.</p>
      <h3 style="margin-top:28px">Qué incluye la gestión de Meta Ads</h3>
      {checks(meta_items)}
      <a class="more-link" href="#contacto">Pide tu propuesta de Meta Ads {icon('arrow')}</a>
    </div>
    <div class="phone-wrap" aria-hidden="true">
      <div class="phone"><div class="screen">
        <div class="ad-top"><i></i><div><b>Tu marca</b><small>Publicidad</small></div></div>
        <div class="ad-img"></div>
        <div class="ad-row">Nueva colección<span>Comprar</span></div>
        <div class="ad-lines"><i></i><i></i></div>
      </div></div>
      <div class="toast">{icon('check')}<div>Pedido confirmado<small>Medido en tu tienda, no en la plataforma</small></div></div>
    </div>
  </div>
</section>
<section class="section soft" id="como-trabajamos" aria-labelledby="proc-title">
  <div class="wrap">
    <div class="section-head"><p class="label">Cómo trabajamos</p><h2 id="proc-title">De la auditoría a las ventas</h2></div>
    <ol class="steps">{steps_html}</ol>
  </div>
</section>
<section class="section" id="servicios" aria-labelledby="svc-title">
  <div class="wrap">
    <div class="section-head"><p class="label">Servicios</p><h2 id="svc-title">Todo lo que tu tienda online necesita para vender más</h2><p class="lead">Las campañas funcionan mejor cuando la tienda, los mensajes y los envíos también funcionan. Por eso lo hacemos todo en el mismo equipo.</p></div>
    <div class="cards">{cards}</div>
    <div class="band" style="margin-top:44px">
      <div><h2>¿No sabes por dónde empezar?</h2><p>Revisamos tu cuenta y tu tienda, y te decimos qué arreglar primero.</p></div>
      <div class="actions"><a class="btn btn-primary" href="#contacto">Pide tu propuesta</a></div>
    </div>
  </div>
</section>
<section class="section soft" aria-labelledby="why-title">
  <div class="wrap">
    <div class="section-head"><p class="label">Por qué Grow Nest</p><h2 id="why-title">Por qué trabajar con Grow Nest</h2></div>
    <ul class="why">{why_html}</ul>
  </div>
</section>
<section class="section dark" data-field-host aria-labelledby="mk-title">
  <div class="wrap split">
    <div>
      <p class="label">Mercados</p>
      <h2 id="mk-title">Campañas en cualquier mercado</h2>
      <p class="lead">Tanto si vendes solo en España como en veinte países, lanzamos tus campañas en Europa, Reino Unido, Estados Unidos, el Golfo y donde quieras crecer, en el idioma y la moneda de cada mercado. Trabajamos en español y en inglés.</p>
      <ul class="chips">{chips}</ul>
    </div>
    <div class="globe-box"><canvas data-shapes="globe" data-count="1500" aria-hidden="true"></canvas></div>
  </div>
</section>
{faq_html(HOME_FAQ, "Preguntas frecuentes sobre Facebook y Meta Ads", "home")}
{contact_section("home")}
</main>
{footer()}"""
    return head(p) + body

# ---------------------------------------------------------------- service pages
PAGES = [
    {
        "path": "/agencia-google-ads/", "crumb": "Agencia Google Ads", "shape": "search", "service": "Gestión de Google Ads y Google Shopping para ecommerce",
        "title": "Agencia Google Ads y Shopping para Ecommerce | Grow Nest",
        "desc": "Campañas de Google Shopping y Búsqueda para tiendas online, con medición limpia y limpieza de búsquedas cada semana.",
        "label": "Google Ads", "h1": "Agencia Google Ads para ecommerce",
        "intro": "Llevamos tus productos a Google Shopping y a la Búsqueda justo cuando alguien los está buscando. Gestionamos campañas de Google Ads para tiendas online en varios países, con medición limpia y revisión semanal.",
        "blocks": [
            {"h2": "Qué incluye nuestra gestión de Google Ads", "items": ["Campañas de Google Shopping, Búsqueda, Display y YouTube", "Alta y revisión de Google Merchant Center y del feed de productos", "Campañas por país: Europa, Reino Unido, Estados Unidos y el Golfo", "Limpieza de términos de búsqueda y listas de palabras clave negativas", "GA4 y Google Tag Manager con las conversiones bien definidas", "Informe mensual con ventas reales, no solo clics"]},
            {"h2": "Resultados medidos en tu tienda", "para": "Google Ads cuenta las conversiones a su manera. Nosotros contrastamos cada campaña con los pedidos de tu tienda y las UTM, y decidimos el presupuesto con esos datos."},
        ],
        "faq": [("¿Qué es Google Shopping?", "Son los anuncios con foto, precio y nombre de la tienda que aparecen al buscar un producto. Salen del feed de productos de Merchant Center."),
                ("¿Google Ads o Meta Ads?", "Google llega a quien ya busca tu producto. Meta crea demanda en quien todavía no lo busca. La mayoría de tiendas necesita los dos."),
                ("¿Cuánto tarda Google Ads en dar resultados?", "Los primeros datos llegan en 7 a 14 días. Hacia los 30 días ya se ve qué campañas merecen más presupuesto.")],
        "cta": "Pide tu propuesta de Google Ads", "related": ("Agencia de Facebook y Meta Ads", "/", "megaphone", "Campañas en Facebook e Instagram medidas con tus pedidos reales."),
    },
    {
        "path": "/agencia-shopify/", "crumb": "Agencia Shopify", "shape": "bag", "service": "Desarrollo de tiendas Shopify y Shopify B2B",
        "title": "Agencia Shopify en España: Tiendas y B2B | Grow Nest",
        "desc": "Creamos tiendas Shopify rápidas, optimizamos cada página para convertir y montamos venta al por mayor con Shopify B2B nativo.",
        "label": "Shopify", "h1": "Agencia Shopify en España: tiendas y B2B",
        "intro": "Creamos y mejoramos tiendas Shopify rápidas que venden en el móvil. Y si vendes al por mayor, lo montamos con Shopify B2B nativo, en la misma tienda y sin apps extra.",
        "blocks": [
            {"h2": "Desarrollo de tiendas Shopify", "items": ["Tiendas nuevas y rediseños", "Temas y secciones a medida en Liquid", "Mercados, monedas, impuestos y zonas de envío", "Google Merchant Center y feeds de producto", "Shopify Flow, formularios y facturas con Order Printer", "Velocidad, móvil y checkout", "Optimización de fichas de producto y landing pages para convertir más visitas en pedidos"]},
            {"h2": "Shopify B2B para vender al por mayor", "items": ["Cuentas de empresa, listas de precios y precios por cantidad", "Productos solo para mayoristas y envíos B2B propios", "Landing de mayoristas que capta clientes profesionales", "CRM de leads con seguimiento por WhatsApp y email"]},
        ],
        "faq": [("¿Shopify sirve para vender al por mayor?", "Sí. Shopify B2B permite cuentas de empresa, precios propios y pedidos por volumen sin abrir una segunda tienda."),
                ("¿Podré editar la tienda yo mismo?", "Sí. Creamos secciones que se editan desde el editor de Shopify, sin tocar código."),
                ("¿Trabajáis con WooCommerce?", "Sí, si tu tienda ya funciona en WooCommerce. Para tiendas nuevas recomendamos Shopify.")],
        "cta": "Pide tu propuesta de Shopify", "related": ("Envíos y devoluciones", "/logistica-ecommerce/", "truck", "Tarifas, etiquetas y seguimiento para cada pedido."),
    },
    {
        "path": "/whatsapp-marketing/", "crumb": "WhatsApp marketing", "shape": "chat", "service": "WhatsApp marketing y WhatsApp Business API para ecommerce",
        "title": "Agencia WhatsApp Marketing para Ecommerce | Grow Nest",
        "desc": "WhatsApp Business API conectado a tu tienda: carritos recuperados, avisos de pedido y envío, y campañas que se leen.",
        "label": "WhatsApp marketing", "h1": "Agencia de WhatsApp marketing para ecommerce",
        "intro": "Conectamos la API de WhatsApp Business a tu tienda y automatizamos los mensajes que recuperan ventas y ahorran trabajo a tu equipo. Mensajes que tus clientes sí abren.",
        "blocks": [
            {"h2": "Qué automatizamos en WhatsApp", "items": ["Alta de WhatsApp Business API y aprobación de plantillas", "Recuperación de carritos y checkouts abandonados", "Confirmación de pedido, envío y entrega", "Avisos de vuelta al stock", "Campañas a listas grandes de clientes", "Bandeja compartida para tu equipo"]},
            {"h2": "Cómo recuperamos un carrito abandonado", "flow": ["El cliente deja productos en el carrito sin pagar.", "Recibe un WhatsApp con su carrito y un enlace directo para terminar la compra.", "Si no compra, le llega un segundo recordatorio más tarde."]},
        ],
        "faq": [("¿Qué es la API de WhatsApp Business?", "Es la versión oficial de WhatsApp para empresas. Permite enviar mensajes automáticos desde tu tienda con plantillas aprobadas por Meta."),
                ("¿Puedo escribir a todos mis clientes por WhatsApp?", "Solo a los que han dado su consentimiento. Te ayudamos a recogerlo en el checkout y en tus formularios."),
                ("¿Funciona con Shopify?", "Sí. Conectamos WhatsApp a los eventos de tu tienda: carrito, pedido, envío y entrega.")],
        "cta": "Pide tu propuesta de WhatsApp", "related": ("Email marketing para ecommerce", "/email-marketing-ecommerce/", "mail", "Flujos de Klaviyo que venden después del primer pedido."),
    },
    {
        "path": "/email-marketing-ecommerce/", "crumb": "Email marketing", "shape": "mail", "service": "Email marketing y Klaviyo para ecommerce",
        "title": "Agencia Email Marketing Ecommerce y Klaviyo | Grow Nest",
        "desc": "Flujos de Klaviyo que venden después del primer pedido, enviados desde un dominio que llega a la bandeja de entrada.",
        "label": "Email marketing", "h1": "Agencia de email marketing para ecommerce",
        "intro": "Creamos flujos y campañas en Klaviyo o Shopify Email que siguen vendiendo después del primer pedido. Enviados desde un dominio que llega a la bandeja de entrada, no a spam.",
        "blocks": [
            {"h2": "Flujos de email que montamos", "items": ["Bienvenida para nuevos suscriptores", "Carrito y checkout abandonado", "Productos vistos y no comprados", "Post-compra: gracias, reseña y siguiente compra", "Recuperación de clientes inactivos"]},
            {"h2": "Qué más incluye", "items": ["Formularios y popups de suscripción", "Segmentos y calendario de campañas", "Entregabilidad: SPF, DKIM, DMARC y dominio de envío propio"]},
        ],
        "faq": [("¿Klaviyo o Shopify Email?", "Shopify Email basta para empezar. Klaviyo es mejor cuando necesitas segmentos avanzados y flujos con varias ramas."),
                ("¿Por qué mis emails llegan a spam?", "Casi siempre es la configuración del dominio: SPF, DKIM o DMARC. Lo revisamos y lo corregimos.")],
        "cta": "Pide tu propuesta de email marketing", "related": ("WhatsApp marketing", "/whatsapp-marketing/", "chat", "Carritos recuperados y avisos de pedido por WhatsApp."),
    },
    {
        "path": "/logistica-ecommerce/", "crumb": "Envíos y devoluciones", "shape": "van", "service": "Logística de envíos y devoluciones para ecommerce",
        "title": "Envíos y Devoluciones para Ecommerce | Grow Nest",
        "desc": "Tarifas, etiquetas, seguimiento diario y alertas de devolución para que cada paquete llegue a su destino.",
        "label": "Envíos y devoluciones", "h1": "Envíos y devoluciones para ecommerce",
        "intro": "Nuestro trabajo no acaba en el checkout. Configuramos tarifas, etiquetas y seguimiento para que cada paquete llegue a su destino, y te avisamos antes de que vuelva.",
        "blocks": [
            {"h2": "Qué hacemos en logística", "items": ["Tarifas de transportistas y zonas de envío por peso (FedEx, Correos)", "Calculadoras de envío en la tienda y barras de envío gratis por país", "Generación de etiquetas y archivos de envío masivos", "Seguimiento diario de cada pedido, con alertas de paquetes parados", "Recordatorios al cliente para recoger su paquete antes de que se devuelva", "App de escaneo para paquetes de salida y devueltos en el almacén"]},
            {"h2": "Menos devoluciones, más pedidos entregados", "para": "Muchos paquetes vuelven porque el cliente no estaba en casa o no sabe que su pedido le espera en la oficina. Nuestro seguimiento detecta esos casos a tiempo y le envía al cliente la dirección de recogida."},
        ],
        "faq": [("¿Con qué transportistas trabajáis?", "FedEx y Correos. Si usas otro, cuéntanoslo y lo revisamos."),
                ("¿Sirve también para pedidos de marketplace?", "Sí. Los pedidos de Shopify, TikTok Shop y Amazon se siguen en el mismo sistema.")],
        "cta": "Pide tu propuesta de logística", "related": ("TikTok Shop y Amazon", "/tiktok-shop-amazon/", "cart", "Pedidos y fichas de marketplace bajo el mismo control."),
    },
    {
        "path": "/tiktok-shop-amazon/", "crumb": "TikTok Shop y Amazon", "shape": "cart", "service": "Gestión de TikTok Shop y Amazon para marcas",
        "title": "Agencia TikTok Shop y Amazon para Marcas | Grow Nest",
        "desc": "Alta, fichas, pedidos y archivos de envío en TikTok Shop y Amazon, con el mismo control que tu propia tienda.",
        "label": "TikTok Shop y Amazon", "h1": "Agencia TikTok Shop y Amazon para marcas",
        "intro": "Gestionamos tus pedidos y tus fichas en TikTok Shop y Amazon con el mismo cuidado que tu propia tienda.",
        "blocks": [
            {"h2": "TikTok Shop", "items": ["Alta de la tienda, fichas de producto y procesamiento de pedidos", "Archivos de envío y subida del número de seguimiento", "Auditorías de ventas, afiliados y liquidaciones"]},
            {"h2": "Amazon", "items": ["Fichas de producto: título, bullets, descripción y palabras clave, también para Amazon.es", "Archivos de envío y seguimiento"]},
            {"h2": "Todo bajo el mismo control", "para": "Los pedidos de TikTok Shop y Amazon entran en el mismo sistema de seguimiento de envíos que tu tienda. Ves en un solo sitio qué está en camino, qué está parado y qué vuelve."},
        ],
        "faq": [("¿Podéis adaptar mis fichas de Shopify a Amazon.es?", "Sí. Convertimos tus descripciones de Shopify en fichas de Amazon.es en español: título, bullets, descripción y palabras clave."),
                ("¿Revisáis lo que me paga TikTok Shop?", "Sí. Cruzamos pedidos, comisiones de afiliados y liquidaciones para que sepas cuánto ganas de verdad.")],
        "cta": "Pide tu propuesta de marketplace", "related": ("Envíos y devoluciones", "/logistica-ecommerce/", "truck", "Seguimiento diario y menos paquetes devueltos."),
    },
    {
        "path": "/desarrollo-a-medida/", "crumb": "Apps a medida", "shape": "code", "service": "Desarrollo de apps y dashboards a medida para ecommerce",
        "title": "Desarrollo de Apps a Medida para Ecommerce | Grow Nest",
        "desc": "Cuando ninguna app hace lo que necesitas, la creamos: apps web, integraciones y paneles para tu equipo.",
        "label": "Apps a medida", "h1": "Desarrollo de apps y dashboards a medida para ecommerce",
        "intro": "Cuando ninguna app hace lo que necesitas, la construimos. Apps web, herramientas internas y paneles conectados a tu tienda Shopify, tus marketplaces y tus transportistas.",
        "blocks": [
            {"h2": "Qué construimos", "items": ["Apps web con Next.js y Supabase", "Paneles de pedidos, ventas y devoluciones", "Herramientas de navegador que funcionan sin conexión, sin instalar nada", "Apps de facturación", "Integraciones por API entre Shopify, TikTok Shop, Amazon, transportistas y CRM"]},
            {"h2": "Herramientas que ya hemos creado", "items": ["Un sistema que sigue cada envío a diario y avisa de los paquetes parados", "Una app de escaneo de etiquetas para el almacén", "Un convertidor de archivos de envío entre marketplaces", "Un panel de auditoría de ventas de TikTok Shop"]},
        ],
        "faq": [("¿Cuánto tarda una herramienta a medida?", "Depende del alcance. Después de la auditoría te damos un plan por fases, con lo que entregamos en cada una."),
                ("¿Se conecta con lo que ya uso?", "Sí. Trabajamos con las APIs de Shopify, marketplaces, transportistas y CRM.")],
        "cta": "Cuéntanos qué necesitas", "related": ("Agencia Shopify", "/agencia-shopify/", "bag", "Tiendas Shopify rápidas y venta B2B nativa."),
    },
]

def hero_inner(p, crumb=True):
    crumbs = f'<ol class="crumbs"><li><a href="/">Inicio</a></li><li aria-current="page">{e(p["crumb"])}</li></ol>' if crumb else ""
    cta = p.get("hero_cta", True)
    acts = f"""<div class="actions">
        <a class="btn btn-primary" href="/contacto/">{e(p.get('cta', 'Pide tu propuesta'))} {icon('arrow')}</a>
        <a class="btn btn-light" href="{WA}" target="_blank" rel="noopener">{icon('chat')} WhatsApp</a>
      </div>""" if cta else ""
    return f"""<section class="hero inner" data-field-host aria-labelledby="h1">
  <div class="wrap">
    <div class="hero-copy">
      <nav aria-label="Ruta de navegación">{crumbs}</nav>
      <p class="label">{e(p['label'])}</p>
      <h1 id="h1">{e(p['h1'])}</h1>
      <p class="lead">{e(p['intro'])}</p>
      {acts}
    </div>
    <div class="hero-visual"><canvas data-shapes="{p['shape']}" aria-hidden="true"></canvas></div>
  </div>
</section>"""

def block_html(b):
    inner = ""
    if b.get("items"):
        inner = checks(b["items"], cols=len(b["items"]) > 3)
    elif b.get("flow"):
        inner = '<ol class="flow">' + "".join(f"<li><span>{e(x)}</span></li>" for x in b["flow"]) + "</ol>"
    elif b.get("para"):
        inner = f'<p class="lead">{e(b["para"])}</p>'
    return f'<div class="block"><h2>{e(b["h2"])}</h2>{inner}</div>'

def build_service(p):
    rel_t, rel_u, rel_i, rel_d = p["related"]
    blocks = "".join(block_html(b) for b in p["blocks"])
    body = f"""{header(p)}
<main id="main">
{hero_inner(p)}
<section class="section content">
  <div class="wrap">
    {blocks}
    <div class="band" style="margin-top:64px">
      <div><h2>{e(p['cta'])}</h2><p>Te respondemos por WhatsApp o por email con los siguientes pasos.</p></div>
      <div class="actions"><a class="btn btn-primary" href="/contacto/">Pide tu propuesta</a><a class="btn btn-light" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></div>
    </div>
    <div class="related"><p class="label">También te puede interesar</p>
      <a class="card" href="{rel_u}"><span class="ico">{icon(rel_i)}</span><h3>{e(rel_t)}</h3><p>{e(rel_d)}</p><span class="go">Ver servicio {icon('arrow')}</span></a>
    </div>
  </div>
</section>
{faq_html(p['faq'], 'Preguntas frecuentes', p['path'].strip('/').replace('/', '-'))}
</main>
{footer()}"""
    return head(p) + body

# ---------------------------------------------------------------- about, contact, privacy, 404
ABOUT = {
    "path": "/sobre-nosotros/", "crumb": "Sobre nosotros", "shape": "nest", "pagetype": "AboutPage",
    "title": "Sobre Grow Nest: Agencia de Marketing para Ecommerce",
    "desc": "Agencia de performance marketing para ecommerce. De la web a las ventas: tienda, Meta Ads, Google Ads, optimización de páginas y envíos.",
    "label": "Sobre nosotros", "h1": "Sobre Grow Nest",
    "intro": "Grow Nest es una agencia de performance marketing para ecommerce. Nos encargamos de todo, de la web a las ventas: creamos tu tienda, lanzamos Meta Ads y Google Ads, optimizamos las páginas y cuidamos los envíos.",
    "cta": "Pide tu propuesta",
}
def build_about():
    p = ABOUT
    values = [("Claridad.", "Informes que se entienden, sin jerga."), ("Honestidad.", "No prometemos ventas; te decimos qué funciona y qué no."), ("Tus cuentas son tuyas.", "Trabajamos con acceso de colaborador y de partner."), ("Constancia.", "Revisamos tus campañas cada semana.")]
    vals = "".join(f"<li>{icon('check')}<span><strong>{e(t)}</strong> {e(d)}</span></li>" for t, d in values)
    body = f"""{header(p)}
<main id="main">
{hero_inner(p)}
<section class="section content">
  <div class="wrap">
    <div class="block"><h2>Por qué existimos</h2>
      <blockquote class="quote"><p>Una marca online no debería necesitar cinco agencias para vender. Un solo equipo debería poder montar la tienda, lanzar los anuncios, automatizar los mensajes y llevar el paquete hasta la puerta. Ese es el equipo que hemos creado.</p><footer>Ghulam Muhammad, fundador</footer></blockquote>
    </div>
    <div class="block"><h2>Cómo trabajamos</h2><ul class="checks cols">{vals}</ul></div>
    <div class="block"><h2>Dónde trabajamos</h2><p class="lead">Con marcas que venden en Europa, Reino Unido, Estados Unidos, el Golfo y Australia. Trabajamos en español y en inglés.</p></div>
    <div class="band" style="margin-top:64px">
      <div><h2>¿Hablamos de tu tienda?</h2><p>Cuéntanos qué vendes y qué quieres mejorar primero.</p></div>
      <div class="actions"><a class="btn btn-primary" href="/contacto/">Pide tu propuesta</a></div>
    </div>
  </div>
</section>
</main>
{footer()}"""
    return head(p) + body

CONTACT = {
    "path": "/contacto/", "crumb": "Contacto", "shape": "bird", "pagetype": "ContactPage",
    "title": "Contacto | Grow Nest",
    "desc": "Cuéntanos tu tienda y qué quieres mejorar primero. Respondemos por WhatsApp o email.",
    "label": "Contacto", "h1": "Contacta con Grow Nest",
    "intro": "Cuéntanos qué vendes y qué quieres mejorar primero. Respondemos por WhatsApp o por email.",
    "hero_cta": False,
}
def build_contact():
    p = CONTACT
    body = f"""{header(p)}
<main id="main">
{hero_inner(p)}
<section class="section dark" id="contacto" aria-label="Formulario de contacto">
  <div class="wrap contact-grid">
    <div>{form('contact')}</div>
    <aside aria-label="Contacto directo">{reach(with_address=True)}</aside>
  </div>
</section>
</main>
{footer()}"""
    return head(p) + body

PRIVACY = {
    "path": "/politica-de-privacidad/", "crumb": "Política de privacidad", "pagetype": "WebPage",
    "title": "Política de privacidad | Grow Nest", "desc": "Cómo tratamos los datos que nos envías a través del formulario de contacto de Grow Nest.",
    "robots": "noindex, follow",
}
def build_privacy():
    p = PRIVACY
    body = f"""{header(p)}
<main id="main">
<section class="section content">
  <div class="wrap" style="max-width:820px">
    <nav aria-label="Ruta de navegación"><ol class="crumbs" style="color:var(--muted)"><li><a href="/" style="color:var(--muted)">Inicio</a></li><li aria-current="page">Política de privacidad</li></ol></nav>
    <h1 style="font-size:clamp(2rem,1.4rem + 2vw,2.8rem)">Política de privacidad</h1>
    <p class="lead">Esta página explica qué datos recogemos cuando nos escribes y para qué los usamos.</p>
    <div class="block"><h2>Quién trata tus datos</h2><p>Grow Nest. Contacto: {EMAIL}.</p></div>
    <div class="block"><h2>Qué datos recogemos</h2><p>Los que escribes en el formulario de contacto: nombre, email, WhatsApp (opcional), web de tu tienda, servicios que te interesan y tu mensaje. Si nos escribes por WhatsApp o email, también tu número o tu dirección de correo.</p></div>
    <div class="block"><h2>Para qué los usamos</h2><p>Solo para responder a tu solicitud y, si trabajamos juntos, para gestionar el servicio. No los vendemos ni los usamos para enviarte publicidad sin tu permiso.</p></div>
    <div class="block"><h2>Quién más los ve</h2><p>El formulario se envía a nuestro correo a través del servicio FormSubmit. Nuestro correo funciona con Google.</p></div>
    <div class="block"><h2>Cuánto tiempo los guardamos</h2><p>Mientras dure la conversación o el servicio, y después el tiempo que exija la ley.</p></div>
    <div class="block"><h2>Tus derechos</h2><p>Puedes pedir ver, corregir o borrar tus datos, o limitar su uso, escribiendo a {EMAIL}. También puedes reclamar ante la Agencia Española de Protección de Datos.</p></div>
    <div class="block"><h2>Cookies</h2><p>Esta web no usa cookies propias de publicidad ni de analítica.</p></div>
  </div>
</section>
</main>
{footer()}"""
    return head(p) + body

NOTFOUND = {"path": "/404.html", "crumb": "Página no encontrada", "title": "Página no encontrada | Grow Nest", "desc": "Esta página no existe.", "robots": "noindex, follow"}
def build_404():
    p = NOTFOUND
    body = f"""{header(p)}
<main id="main">
<section class="section notfound">
  <div class="wrap">
    <p class="label">Error 404</p>
    <h1 style="font-size:clamp(2rem,1.4rem + 2vw,3rem)">Esta página no existe</h1>
    <p class="lead" style="margin:0 auto 24px">Puede que el enlace haya cambiado. Vuelve al inicio o escríbenos.</p>
    <div class="actions" style="justify-content:center"><a class="btn btn-primary" href="/">Ir al inicio</a><a class="btn btn-ghost" href="/contacto/">Contacto</a></div>
  </div>
</section>
</main>
{footer()}"""
    return head(p) + body

# ---------------------------------------------------------------- write
def write(path, html):
    full = os.path.join(ROOT, path.lstrip("/"))
    if full.endswith("/"):
        full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return full

def main():
    out = [write("/index.html", build_home())]
    for p in PAGES:
        out.append(write(p["path"], build_service(p)))
    out.append(write(ABOUT["path"], build_about()))
    out.append(write(CONTACT["path"], build_contact()))
    out.append(write(PRIVACY["path"], build_privacy()))
    out.append(write("/404.html", build_404()))
    indexable = ["/"] + [p["path"] for p in PAGES] + [ABOUT["path"], CONTACT["path"]]
    pri = {"/": "1.0"}
    urls = "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pri.get(u, '0.8')}</priority></url>\n" for u in indexable)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    print("\n".join(os.path.relpath(x, ROOT) for x in out))

if __name__ == "__main__":
    main()
