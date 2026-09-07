# Yang Zhou — academic homepage

One page, one stylesheet, ~20 lines of JavaScript (email obfuscation only). No build step.
Layout follows **maureenzou.github.io**: a 980 px shell split into a 212 px identity rail and a
fluid content column, white cards on a light grey ground, soft shadows, and a compact type scale.
The bio follows **haipinglu.github.io**: a role paragraph, then a thesis line with three labelled
research threads, then the artifacts we release.

DM Sans is **self-hosted** in `assets/fonts/` (Google Fonts latin variable build, 61 KB, SIL OFL —
see `assets/fonts/OFL.txt`). Only the roman is shipped; the handful of italic venue names are
browser-slanted, which halves the font payload. Nothing loads from a CDN, so the page renders
identically inside and outside China.

```
index.html                the whole site
404.html
assets/css/style.css      all styling; colour variables are the :root block near the top
assets/fonts/             DM Sans woff2 + licence
assets/img/portrait.jpg   560×560, cropped from your headshot
assets/favicon.svg
ZY_CV_short.pdf           linked from the header
```

`ChatGPT_ZY_Skin_Smoothing.png` (the 1.8 MB original headshot) is still in the folder. It is not
referenced by the page — delete it before deploying if you would rather not publish it.

## Email obfuscation

No address appears in the HTML source. Elements carry the parts:

```html
<a href="#contact" data-u="zhou_yang" data-d="whu.edu.cn">Email</a>
<span data-u="zhou_yang" data-d="whu.edu.cn"><noscript>zhou_yang [at] whu.edu.cn</noscript></span>
```

The inline script at the bottom of `index.html` joins them into a `mailto:` on load. `<a>` elements
keep their own label; `<span>` elements are filled with the address as visible text. Without
JavaScript the `<noscript>` fallback shows a human-readable form. This stops naive harvesters, not a
determined one — do not treat it as security.

## Editing

To add a paper, copy one `.pub` block in `index.html`:

```html
<div class="pub">
  <div class="yr">2027</div>
  <div class="meta">
    <div class="t">Title of the paper</div>
    <div class="au"><b>Yang Zhou</b><sup>*</sup>, A. N. Other, et al.</div>
    <div class="vn"><em>NeurIPS</em>, 2027 <span class="award">· Oral</span></div>
    <div class="lk">
      <a href="https://arxiv.org/abs/…" rel="noopener"><!-- keep an icon svg here -->arXiv</a>
    </div>
  </div>
</div>
```

`<b>` marks your name, `<sup>*</sup>` co-first, `<sup>#</sup>` corresponding, `.award` renders in
red. Copy an existing `<svg class="icon">` for the link icons — the set in use is mail, scholar,
github, cv, arxiv, code, external-link, award, users, book, pin and target (the VEGA badge).

Every one of the ten papers links to arXiv, code and the publisher where those exist; all links were
checked and resolve.

## Content

Appointments, education, funding, awards and the publication list come from `ZY_CV_short.pdf`. The
appointment and education lists are deliberately **not** itemised — the key parts sit in the third
bio paragraph. Two corrections applied against the CV:

- The TPAMI paper's published title includes **Robust** (*Bayesian Low-Tubal-Rank **Robust** Tensor
  Factorization…*); the CV drops it.
- BenchX is the NeurIPS 2024 **Datasets & Benchmarks** track, now stated on the page.

The Shanghai Science and Technology Award was removed on request.

## Preview and deploy

```sh
python3 -m http.server 8000     # http://localhost:8000
```

- **Netlify** — drag the folder onto the dashboard, or connect the repo with an empty build command
  and publish directory `.`.
- **GitHub Pages** — Settings → Pages → deploy from branch, root.
- **University web space** — copy the folder as-is.
