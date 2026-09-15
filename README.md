# Yang Zhou — academic homepage

Live at **<https://yangzhou-whu.github.io/>** (GitHub Pages, organisation `yangzhou-whu`, branch
`main`, root). Plain static files: one stylesheet per page, ~20 lines of JavaScript (email
obfuscation only), no build step, no Jekyll (`.nojekyll`). Nothing loads from a CDN, so the pages
render identically inside and outside China.

```
index.html                     the homepage
vega/research-guide.html       VEGA Lab 本科生科研入门指南 (linked from the nav and Openings)
vega/references.bib            the guide's 21 references, downloadable from the page
404.html
assets/css/style.css           shared styling; colour variables are the :root block near the top
assets/css/research-guide.css  reading layout for the guide, on top of style.css
assets/fonts/                  DM Sans woff2 (self-hosted, SIL OFL — see OFL.txt)
assets/img/portrait.jpg        560×560, cropped from the headshot
assets/favicon.svg
ZY_CV_short.pdf                linked from the header
```

`ChatGPT_ZY_Skin_Smoothing.png` (the 1.8 MB original headshot) is git-ignored and not referenced by
either page; it stays out of the published site.

Layout follows **maureenzou.github.io**: a 980 px shell split into a 212 px identity rail and a
fluid content column, white cards on a light grey ground, soft shadows, a compact type scale. The
bio follows **haipinglu.github.io**. DM Sans ships as the roman only; the few italic venue names are
browser-slanted, which halves the font payload.

## Editing the homepage

To add a paper, copy one `.pub` block in `index.html`:

```html
<div class="pub">
  <div class="t">Title of the paper</div>
  <div class="au"><b>Yang Zhou</b><sup>*</sup>, A. N. Other, et al.</div>
  <div class="vn"><span class="lk"><a href="…" rel="noopener"><!-- icon svg -->Paper</a></span><span><em>NeurIPS</em>, 2027</span></div>
</div>
```

`<b>` marks your name, `<sup>*</sup>` co-first, `<sup>#</sup>` corresponding, `.award` renders in
red. Accepted-but-unpublished work is written `<em>Journal</em> (Accepted), year`. Copy an existing
`<svg class="icon">` for link icons (paper, code, model, mail, scholar, github, cv, and the section
icons).

Appointments, education, funding and awards come from `ZY_CV_short.pdf` and are deliberately not
itemised; the key parts sit in the third bio paragraph.

## Editing the research guide

`vega/research-guide.html` is Chinese-language, one `<section class="card">` per chapter, with a
sticky table of contents in the rail. Citations in the text are `<a class="citation" href="#ref-n">[n]</a>`;
references are numbered in order of first citation, and `vega/references.bib` lists the same
entries in the same order, so `[n]` in the page is the n-th BibTeX entry.

Reference format (keep every entry to it):

- **Title** links to the version of record (`https://doi.org/…`) when a DOI exists, otherwise to the
  open full text (arXiv abstract page or proceedings PDF).
- **Authors**: all when four or fewer, otherwise the first three and “et al.”; Yang Zhou in `<b>`.
- **Venue**: `<em>Journal</em>, volume(issue):pages, year.` · `<em>MICCAI</em>, pp. a–b, year.` ·
  `arXiv:id, year.` · accepted work: `<em>Journal</em> (Accepted), year.`
- **Links line** (optional): short name when it is not in the title (`<span class="reference-tag">`),
  then `arXiv`/`PDF` for open full text, `代码`, `模型权重`, separated by ` · `.
- **BibTeX**: key `firstauthorYEARshortname`, authors `Family, Given` with the full list where the
  source gives one, titles double-braced, `doi` plus `url` for open full text, `note = {Accepted}`
  for accepted work. Volume, issue and pages were checked against Crossref on 2026-09-15.

## Email obfuscation

No address appears in the HTML source. Elements carry the parts:

```html
<a href="#contact" data-u="zhou_yang" data-d="whu.edu.cn">Email</a>
```

The inline script at the bottom of `index.html` joins them into a `mailto:` on load. This stops
naive harvesters, not a determined one.

## Preview and deploy

```sh
python3 -m http.server 8000     # http://localhost:8000 and /vega/research-guide.html
git add -A && git commit -m "…" && git push   # live in under a minute
```

Do **not** rename the `yangzhou12` GitHub account: `BenchX`, `NCRL`, `BTRTF` and others are cited
in papers and linked from this page, and GitHub lets anyone claim a released name.

### Custom domain (when one is bought)

Checked 2026-09-08 with `dig NS`, no delegation: `vega-lab.org`, `vega-lab.ai`, `vega-lab.dev`,
`vega-lab.net`, `zhouyang.ai`, `yangzhou.wiki`. Taken: `yangzhou.ai`, `vegalab.ai`, `vegalab.org`,
`yangzhou.dev`, `zhouyang.dev`, `vegalab.dev`, `vegalab.net`, `yangzhou.info`.

1. `echo 'vega-lab.org' > CNAME && git add CNAME && git commit -m "Add custom domain" && git push`
2. At the DNS provider (GitHub's Pages addresses as of 2026-09-07; re-check `https://api.github.com/meta`):

   | Record | Name | Value |
   |---|---|---|
   | A | `@` | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
   | AAAA | `@` | `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153` |
   | CNAME | `www` | `yangzhou-whu.github.io.` |

3. Once DNS has propagated:
   `gh api -X PUT repos/yangzhou-whu/yangzhou-whu.github.io/pages -f cname='vega-lab.org'`, then
   `-F https_enforced=true` after the Let's Encrypt certificate issues (minutes to an hour).

GitHub Pages is hosted outside mainland China, so no ICP filing is needed regardless of TLD; a
`.cn` domain does require real-name verification at the registrar.
