# Grow Nest website (grownest.pro)

Spanish (es-ES) site for Grow Nest, built to rank in Spain for Facebook and Meta Ads agency searches and to turn visitors into enquiries.

## Pages

| URL | Main keyword |
| --- | --- |
| `/` | agencia de facebook y meta ads para ecommerce |
| `/agencia-google-ads/` | agencia google ads ecommerce |
| `/agencia-shopify/` | agencia shopify españa |
| `/whatsapp-marketing/` | agencia whatsapp marketing |
| `/email-marketing-ecommerce/` | agencia email marketing ecommerce |
| `/logistica-ecommerce/` | envíos y devoluciones ecommerce |
| `/tiktok-shop-amazon/` | agencia tiktok shop |
| `/desarrollo-a-medida/` | desarrollo apps shopify a medida |
| `/sobre-nosotros/` | brand page |
| `/contacto/` | contact page |

## How it is built

- Static HTML, no framework and no build step on the server. Vercel serves the repo root.
- All copy lives in `tools/build.py`. Edit it, then run `python3 tools/build.py` to regenerate every page, `sitemap.xml` and `robots.txt`.
- Each page has its own title, meta description, canonical URL, Open Graph tags and JSON-LD (Organization, WebSite, WebPage, Service, FAQPage, BreadcrumbList).
- `assets/js/hero.js` draws the dot animation in each hero (WebGL, Canvas 2D fallback, paused off screen, static with reduced motion).
- `assets/js/site.js` runs the menu, the copy buttons and the contact form. The form posts to FormSubmit, which emails `connect.grownest@gmail.com`.

## Run locally

```
python3 -m http.server 8080
```

Then open http://localhost:8080.
