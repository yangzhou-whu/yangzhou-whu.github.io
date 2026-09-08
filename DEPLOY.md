# Deploying this site

Plain static files. No build step, no Jekyll (`.nojekyll` tells GitHub Pages to serve them
verbatim). The repo is already initialised on `main` with everything committed — nothing has been
pushed yet.

## 1. Where it lives

The site is going to **`https://yangzhou-whu.github.io/`**.

`marswhu.github.io` (Mang Ye's group) is a second GitHub account named for the lab rather than the
person's handle. GitHub's terms allow only one free *personal* account, so the sanctioned equivalent
is a free **Organization** — same `<name>.github.io` URL, and you can add students to it later.

Every plain form of the name is taken (`yangzhou`, `zhouyang`, `yang-zhou`, `yangzhou-ai`).
Checked free on 2026-09-08: `yangzhou-whu`, `zhouyang-whu`, `yzhou-whu`, `vega-whu`, `whu-vega`,
`vegalab-whu`, `vega-lab-whu`, `yangzhoulab`, `vegalab-ai`.

Do **not** rename the `yangzhou12` account. `BenchX`, `NCRL`, `BTRTF` and others are cited in papers
and linked from this page; GitHub redirects the old name but then lets anyone else claim it.

## 2. Push

**Step 1 — create the organization (you, in a browser).** There is no API for this: `POST /user/orgs`
returns 404, and `gh` cannot do it either. Go to <https://github.com/organizations/new>, choose the
**Free** plan, and set the organization name to `yangzhou-whu`.

**Step 2 — create the repo and push (one command).**

```sh
cd /home/zhouyang/OpenEye/homepage_zy
gh repo create yangzhou-whu/yangzhou-whu.github.io --public --source=. --remote=origin --push
```

For a repo named `<owner>.github.io`, Pages turns itself on from `main` at root. To confirm, or to
force it:

```sh
gh api -X POST repos/yangzhou-whu/yangzhou-whu.github.io/pages \
  -f 'source[branch]=main' -f 'source[path]=/'      # 409 just means it is already on
gh api repos/yangzhou-whu/yangzhou-whu.github.io/pages --jq '.html_url, .status'
```

Later edits: `git add -A && git commit -m "…" && git push`. Live in under a minute.

**Staying on the personal account instead.** If you would rather skip the organization, this also
works with no new account, at `https://yangzhou12.github.io/`:

```sh
gh repo create yangzhou12.github.io --public --source=. --remote=origin --push
```

## 3. Custom domain (do this whenever the domain is bought)

Any repo can serve a custom domain at its root, so the repo name stops mattering once this is set.

Any repo can serve a custom domain at its root, so the repo name stops mattering once this is set —
you can publish under the GitHub name today and attach a domain later without breaking anything.

Checked on 2026-09-08 with `dig NS`, no DNS delegation (very likely unregistered — confirm at a
registrar): `vega-lab.org`, `vega-lab.ai`, `vega-lab.dev`, `vega-lab.net`, `zhouyang.ai`,
`yangzhou.wiki`. Already taken: `yangzhou.ai`, `vegalab.ai`, `vegalab.org`, `yangzhou.dev`,
`zhouyang.dev`, `vegalab.dev`, `vegalab.net`, `yangzhou.info`.

**In the repo** — one line, no scheme, no trailing slash:

```sh
echo 'vega-lab.org' > CNAME          # or www.vega-lab.org
git add CNAME && git commit -m "Add custom domain" && git push
```

**At the DNS provider.** These are GitHub's current Pages addresses, read from
`https://api.github.com/meta` on 2026-09-07 — re-check that endpoint rather than copying stale
values from a blog post:

| Record | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153` |
| CNAME | `www` | `yangzhou-whu.github.io.` |

If you prefer `www.` as the primary, put `www.vega-lab.org` in `CNAME` and keep the apex A records
so the bare domain redirects to it.

**Then**, once DNS has propagated, set it in the repo and turn on HTTPS:

```sh
gh api -X PUT repos/<owner>/<repo>/pages -f cname='vega-lab.org'
gh api -X PUT repos/<owner>/<repo>/pages -F https_enforced=true   # only after the cert issues
```

The certificate is issued by Let's Encrypt automatically and usually takes a few minutes to an hour.

**On China:** GitHub Pages is hosted outside the mainland, so no ICP filing is required regardless
of the TLD. A `.cn` domain does require real-name verification at the registrar. Access from the
mainland is usually fine but occasionally slow — which is exactly why this site self-hosts its
fonts and loads nothing from a CDN.
