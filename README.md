# Grow Nest website (grownest.pro)

Site for Grow Nest, built to rank in Spain for Facebook and Meta Ads agency searches and to turn visitors into enquiries.

Spanish (es-ES) is the main version at the root. A full English version lives under `/en/`. The ES | EN switcher in the header links each page to its pair, and every page carries hreflang links (es-ES, en, and x-default pointing to Spanish).

## Pages

| Spanish URL | English URL | Main keyword (Spanish) |
| --- | --- | --- |
| `/` | `/en/` | agencia de facebook y meta ads para ecommerce |
| `/agencia-google-ads/` | `/en/google-ads-agency/` | agencia google ads ecommerce |
| `/agencia-shopify/` | `/en/shopify-agency/` | agencia shopify españa |
| `/whatsapp-marketing/` | `/en/whatsapp-marketing/` | agencia whatsapp marketing |
| `/email-marketing-ecommerce/` | `/en/email-marketing/` | agencia email marketing ecommerce |
| `/logistica-ecommerce/` | `/en/shipping-and-returns/` | envíos y devoluciones ecommerce |
| `/tiktok-shop-amazon/` | `/en/tiktok-shop-amazon/` | agencia tiktok shop |
| `/desarrollo-a-medida/` | `/en/custom-apps/` | desarrollo apps shopify a medida |
| `/sobre-nosotros/` | `/en/about/` | brand page |
| `/contacto/` | `/en/contact/` | contact page |

## How it is built

- Static HTML, no framework and no build step on the server. Vercel serves the repo root.
- All copy lives in `tools/build.py`, in Spanish and English side by side. Edit it, then run `python3 tools/build.py` to regenerate every page in both languages, `sitemap.xml` (with hreflang alternates) and `robots.txt`.
- Each page has its own title, meta description, canonical URL, Open Graph tags and JSON-LD (Organization, WebSite, WebPage, Service, FAQPage, BreadcrumbList).
- `assets/js/hero.js` draws the dot animation in each hero (WebGL, Canvas 2D fallback, paused off screen, static with reduced motion).
- `assets/js/site.js` runs the menu, the copy buttons and the contact form, with messages in the page's language. The form posts to FormSubmit, which emails `connect.grownest@gmail.com`.

## Run locally

```
python3 -m http.server 8080
```

Then open http://localhost:8080.
