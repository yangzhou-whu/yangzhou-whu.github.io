# Deploying this site

Plain static files. No build step, no Jekyll (`.nojekyll` tells GitHub Pages to serve them
verbatim). The repo is already initialised on `main` with everything committed — nothing has been
pushed yet.

## 1. Pick where it lives

`marswhu.github.io` (Mang Ye's group) is a **second GitHub account** named after the lab. GitHub's
terms allow only one free *personal* account, so the sanctioned equivalent is a free
**Organization** — same `<name>.github.io` URL, and you can add students to it later.

Available as of 2026-09-07: `vega-whu`, `whu-vega`, `vegalab-whu`, `yangzhou-whu`.
Taken: `vega-lab`, `vegalab`, `VEGA-Lab`.

Do **not** rename the `yangzhou12` account. `BenchX`, `NCRL`, `BTRTF` and others are cited in
papers and linked from this page; GitHub redirects the old name but then lets anyone else claim it.

## 2. Push

Personal account — serves at `https://yangzhou12.github.io/`:

```sh
cd /home/zhouyang/OpenEye/personal_website
gh repo create yangzhou12.github.io --public --source=. --remote=origin --push
```

Lab organization — serves at `https://vega-whu.github.io/`:

```sh
cd /home/zhouyang/OpenEye/personal_website
gh api -X POST /user/orgs -f login=vega-whu          # or create it at github.com/organizations/new
gh repo create vega-whu/vega-whu.github.io --public --source=. --remote=origin --push
```

For a repo named `<owner>.github.io`, Pages turns itself on from `main` at root. To confirm or force
it:

```sh
gh api -X POST repos/<owner>/<owner>.github.io/pages \
  -f 'source[branch]=main' -f 'source[path]=/'       # 409 just means it is already on
gh api repos/<owner>/<owner>.github.io/pages --jq '.html_url, .status'
```

Later edits: `git add -A && git commit -m "…" && git push`. Live in under a minute.

## 3. Custom domain (do this whenever the domain is bought)

Any repo can serve a custom domain at its root, so the repo name stops mattering once this is set.

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
| CNAME | `www` | `<owner>.github.io.` |

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
