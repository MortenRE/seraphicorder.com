# Seraphic Order — Digital Creations

The website of Seraphic Order, published at **https://seraphicorder.com**.

*Ancient atmosphere. Modern creation.*

## What this is

A hand-built static site: one HTML page, one stylesheet, one script, and a set of
self-drawn SVG assets. There is no framework, no build step, no backend, no
analytics and no third-party request of any kind. The fonts are self-hosted.

```
index.html          the page
styles.css          all styling (design tokens at the top)
main.js             ambient behaviour: reveals, parallax, rain, active chapter
404.html            "not recorded in the archive"
assets/img/         emblem, seal, favicon and celestial diagram (SVG)
assets/fonts/       Cormorant Garamond + EB Garamond (variable WOFF2, OFL)
favicon.*, og.jpg   generated raster icons and the social preview image
CNAME               custom domain for GitHub Pages
.github/workflows   deployment to GitHub Pages
```

## Adding a creation

Creations live in the ordered list `ol.plates` in `index.html`. Each entry is a
"plate". Replace one of the pending plates, or append a new `<li>`:

```html
<li class="plate" data-state="published">
  <a class="plate__link" href="https://example.com">
    <span class="plate__num">Plate I</span>
    <div class="plate__figure" aria-hidden="true">
      <!-- an inline SVG, or <img src="assets/img/work.jpg" alt=""> -->
    </div>
    <h3 class="plate__title">Name of the work</h3>
    <p class="plate__desc">One quiet sentence about it.</p>
  </a>
</li>
```

Keep the roman numerals in the order of making. The grid handles one to three
plates per row and wraps beyond that.

## Working locally

Open `index.html` directly, or serve the folder:

```
python -m http.server 8000
```

## Regenerating the emblem and icons

`tools/emblem.py` (Python 3, no dependencies) draws the seal, the mark, the
favicon and the celestial diagram into `assets/img/`, and inlines the emblem
symbols into `index.html` between the `<!-- emblem:start -->` and
`<!-- emblem:end -->` markers so that the ring text can use the page's web font.

```
python tools/emblem.py
```

The raster files (`favicon.ico`, `apple-touch-icon.png`, `icon-*.png`, `og.jpg`)
were rendered from those SVGs with a headless browser and Pillow. If the emblem
changes, re-render them from `favicon.svg` and `assets/img/seal.svg`.

## Deployment

Pushing to `main` runs `.github/workflows/deploy.yml`, which uploads the
repository root as a Pages artifact and deploys it. In the repository settings
under **Pages**, the source must be set to **GitHub Actions** and the custom
domain to `seraphicorder.com` (with "Enforce HTTPS" once the certificate is
issued).

## Licences

Site content and design © Seraphic Order. Fonts are licensed under the SIL Open
Font License; see `assets/fonts/LICENSE.txt`.
