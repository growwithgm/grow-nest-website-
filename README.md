# Grow Nest website

The one-page site for **Grow Nest** ([grownest.pro](https://www.grownest.pro/)), an e-commerce growth studio.

The page is a scroll story. About 3,000 glowing dots live on a fixed canvas behind the content and morph into a new shape for each section: a nest with an egg, a shopping bag, cartons, a chart, a chat bubble, an envelope, a van, a cart, a browser window, a video frame, glowing clusters, a winding path, a hatching egg, a globe, a galaxy, a flying bird and finally the Grow Nest logo. The night sky turns to dawn near the end.

Plain HTML, CSS and JavaScript modules. No framework, no build step, no tracking.

## Run it locally

Serve the repo root with any static server, then open the printed address:

```sh
python3 -m http.server 8080
# or
npx serve .
```

Opening `index.html` straight from the disk (`file://`) will not work, because browsers block ES modules there.

## How it deploys

Every push to `main` runs `.github/workflows/pages.yml`, which publishes the repo root to GitHub Pages. One-time setup: **Settings → Pages → Source → GitHub Actions**.

Preview: https://growwithgm.github.io/grow-nest-website-/

All asset paths are relative, so the same files work on the Pages preview and on grownest.pro. There is no `CNAME` file yet; the domain moves over separately.

## Files

```
index.html                 the page and all copy
assets/css/main.css        design tokens, layout, phone layout
assets/js/main.js          scroll state, header counter, dawn, form, copy buttons
assets/js/field.js         dot engine: WebGL, with a Canvas 2D fallback
assets/js/shapes.js        every shape, one function each
assets/img/                logo, light logo versions, favicons, share image
tools/make-logos.py        makes the light logos and favicons from grownest-logo.png
reference/screens/         check screenshots (desktop 1440x900, phone 390x844)
```

### Dot scenes

Each `<section>` (and the footer) has `data-shape` (a function name in `shapes.js`) and a `--tint` colour. `data-layout="wide"` centres and dims the dots behind full-width content; `data-layout="footer"` places the logo above the footer.

The engine reads the scroll position, works out which two scenes the viewport centre sits between, and moves every dot from its point in one shape to its point in the next, with its own delay and a slight swirl. Dots follow their targets on springs, and the pointer pushes them aside. With `prefers-reduced-motion`, each scene shows its finished shape and switches halfway between sections.

### Logos

```sh
python3 tools/make-logos.py   # needs Pillow and NumPy
```

This reads `assets/img/grownest-logo.png` and writes `logo-light.png`, `logo-wordmark-light.png`, `favicon-32.png`, `apple-touch-icon.png` and `favicon.svg`.

### Contact form

The form posts JSON to FormSubmit (`https://formsubmit.co/ajax/connect.grownest@gmail.com`). The first real submission makes FormSubmit send an activation email to that address. Until the link in it is clicked, submissions are not delivered and the page shows its error message.
