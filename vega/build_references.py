#!/usr/bin/env python3
"""Regenerate vega/references.bib and the reference block of vega/research-guide.html
from the ONE list of entries below, so the page and the BibTeX never drift.

    python3 vega/build_references.py

Author lists live in references-authors.json next to this file (fetched from Crossref and
arXiv on 2026-09-15). To add a reference: append an entry to R, add its author list to the
JSON under the same key (Family / Given pairs), cite it in the page as
<a class="citation" href="#ref-n">[n]</a>, and run this script. Entries are numbered in
order of first citation, so keep R in that order.

Display rules (HTML):
  title       links to the version of record (doi.org) when a DOI exists, else the open full text
  authors     all when <= 4, otherwise first three + "et al."; Yang Zhou in bold
  venue       <em>Journal</em>, vol(issue):pages, year. | <em>Conf</em>, pp. a-b, year. | arXiv:id, year.
              accepted work: <em>Journal</em> (Accepted), year.
  links line  short name when it is not in the title · arXiv/PDF (open full text) · 代码 · 模型权重
BibTeX rules:
  key firstauthorYEARshortname; fields in a fixed order; titles double-braced; authors
  "Family, Given" with the full list where the source gives one; doi plus url for open full text;
  note = {Accepted} for accepted work.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.join(HERE, "research-guide.html")
BIB = os.path.join(HERE, "references.bib")
AUTHORS = json.load(open(os.path.join(HERE, "references-authors.json"), encoding="utf-8"))["authors"]


def au(key):
    """Author list for an entry as (family, given) tuples; corporate authors have given == ''."""
    return [(a["family"], a.get("given", "")) for a in AUTHORS[key]]


# ---- the references, in citation order ---------------------------------------------------------
R = [
 dict(key="zhou2026mermedfm", type="article",
      title="MerMED-FM: Multimodal, Multi-Disease Medical Imaging Foundation Model",
      journal="The Lancet Digital Health", volume="8", number="7", pages="101007", year="2026",
      doi="10.1016/j.landig.2026.101007", arxiv="2507.00185",
      code="https://github.com/yangzhou12/MerMED", weights="https://huggingface.co/youngzhou12/MerMED"),
 dict(key="yu2024urfound", type="inproceedings",
      title="UrFound: Towards Universal Retinal Foundation Models via Knowledge-Guided Masked Modeling",
      booktitle="Medical Image Computing and Computer Assisted Intervention (MICCAI)", conf="MICCAI",
      pages="753--762", year="2024", doi="10.1007/978-3-031-72390-2_70",
      pdf="https://papers.miccai.org/miccai-2024/paper/1942_paper.pdf",
      code="https://github.com/yukkai/UrFound", weights="https://huggingface.co/yyyyk/UrFound"),
 dict(key="zhou2023retfound", short="RETFound", type="article",
      title="A foundation model for generalizable disease detection from retinal images",
      journal="Nature", volume="622", number="7981", pages="156--163", year="2023",
      doi="10.1038/s41586-023-06555-x", code="https://github.com/rmaphoh/RETFound"),
 dict(key="ma2025arkplus", short="Ark+", type="article",
      title="A fully open AI foundation model applied to chest radiography",
      journal="Nature", volume="643", number="8071", pages="488--498", year="2025",
      doi="10.1038/s41586-025-09079-8", pdf="https://rdcu.be/eqx2i", code="https://github.com/jlianglab/Ark"),
 dict(key="yan2025panderm", short="PanDerm", type="article",
      title="A multimodal vision foundation model for clinical dermatology",
      journal="Nature Medicine", volume="31", number="8", pages="2691--2702", year="2025",
      doi="10.1038/s41591-025-03747-y", code="https://github.com/SiyuanYan1/PanDerm"),
 dict(key="blankemeier2026merlin", type="article",
      title="Merlin: a computed tomography vision-language foundation model and dataset",
      journal="Nature", volume="652", number="8112", pages="1318--1328", year="2026",
      doi="10.1038/s41586-026-10181-8", arxiv="2406.06512", code="https://github.com/StanfordMIMI/Merlin"),
 dict(key="chen2023medrpg", short="MedRPG", type="inproceedings",
      title="Medical Phrase Grounding with Region-Phrase Context Contrastive Alignment",
      booktitle="Medical Image Computing and Computer Assisted Intervention (MICCAI)", conf="MICCAI",
      pages="371--381", year="2023", doi="10.1007/978-3-031-43990-2_35",
      arxiv="2303.07618", code="https://github.com/eraserNut/MedRPG"),
 dict(key="bai2026evlffm", type="article",
      title="EVLF-FM: Explainable Vision Language Foundation Model for Medicine",
      journal="Nature Medicine", status="Accepted", year="2026", arxiv="2509.24231"),
 dict(key="ma2024medsam", short="MedSAM", type="article",
      title="Segment anything in medical images",
      journal="Nature Communications", volume="15", number="1", pages="654", year="2024",
      doi="10.1038/s41467-024-44824-z", code="https://github.com/bowang-lab/MedSAM"),
 dict(key="wu2026unibiomed", short="UniBiomed", type="article",
      title="A universal foundation model for grounded biomedical image interpretation",
      journal="Nature Communications", volume="17", number="1", pages="7173", year="2026",
      doi="10.1038/s41467-026-73986-1", code="https://github.com/Luffy03/UniBiomed"),
 dict(key="zhang2026medsegx", short="MedSegX", type="article",
      title="A generalist foundation model and database for open-world medical image segmentation",
      journal="Nature Biomedical Engineering", volume="10", number="5", pages="1026--1041", year="2026",
      doi="10.1038/s41551-025-01497-3", note="Published online 5 September 2025"),
 dict(key="zhao2025teaser", short="Teaser", type="article",
      title="Topicwise Separable Sentence Retrieval for Medical Report Generation",
      journal="IEEE Transactions on Medical Imaging", volume="44", number="3", pages="1505--1517", year="2025",
      doi="10.1109/TMI.2024.3507076", arxiv="2405.04175", code="https://github.com/CindyZJT/Teaser"),
 dict(key="zhou2026note2chat", type="inproceedings",
      title="Note2Chat: Improving LLMs for Multi-Turn Clinical History Taking Using Medical Notes",
      booktitle="Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)", conf="AAAI",
      volume="40", number="41", pages="35149--35157", year="2026", doi="10.1609/aaai.v40i41.40821",
      arxiv="2601.21551", code="https://github.com/zhentingsheng/Note2Chat"),
 dict(key="lievin2026amie", short="AMIE", type="article",
      title="Towards conversational artificial intelligence for disease management",
      journal="Nature", volume="655", number="8125", pages="1292--1299", year="2026",
      doi="10.1038/s41586-026-10764-5"),
 dict(key="zhao2026deeprare", short="DeepRare", type="article",
      title="An agentic system for rare disease diagnosis with traceable reasoning",
      journal="Nature", volume="651", number="8106", pages="775--784", year="2026",
      doi="10.1038/s41586-025-10097-9", code="https://github.com/MAGIC-AI4Med/DeepRare"),
 dict(key="ding2026combodied", type="misc",
      title="ComBodied Agents: a New Paradigm of Human-Centric Agentic AI",
      year="2026", arxiv="2608.10915v2"),
 dict(key="huang2026biomni", short="Biomni", type="article",
      title="Autonomous biomedical research with an artificial intelligence agent",
      journal="Science", volume="393", number="6813", pages="eadz4351", year="2026",
      doi="10.1126/science.adz4351", pdf="https://www.biorxiv.org/content/10.1101/2025.05.30.656746v1.full.pdf",
      code="https://github.com/snap-stanford/Biomni"),
 dict(key="thapa2026sleepfm", short="SleepFM", type="article",
      title="A multimodal sleep foundation model for disease prediction",
      journal="Nature Medicine", volume="32", number="2", pages="752--762", year="2026",
      doi="10.1038/s41591-025-04133-4", code="https://github.com/rthapa84/sleepfm-codebase"),
 dict(key="he2025lucaone", short="LucaOne", type="article",
      title="Generalized biological foundation model with unified nucleic acid and protein language",
      journal="Nature Machine Intelligence", volume="7", number="6", pages="942--953", year="2025",
      doi="10.1038/s42256-025-01044-4", code="https://github.com/LucaOne/LucaOne"),
 dict(key="zhou2024benchx", type="inproceedings",
      title="BenchX: A Unified Benchmark Framework for Medical Vision-Language Pretraining on Chest X-Rays",
      booktitle="Advances in Neural Information Processing Systems (NeurIPS)", conf="NeurIPS",
      volume="37", year="2024",
      pdf="https://proceedings.neurips.cc/paper_files/paper/2024/file/0cb35e10bf7bb73d10c12414edbd63fd-Paper-Datasets_and_Benchmarks_Track.pdf",
      code="https://github.com/yangzhou12/BenchX"),
 dict(key="leng2025cmm", short="CMM", type="inproceedings",
      title="The Curse of Multi-Modalities: Evaluating Hallucinations of Large Multimodal Models across Language, Visual, and Audio",
      booktitle="Advances in Neural Information Processing Systems (NeurIPS)", conf="NeurIPS",
      volume="38", year="2025", doi="10.52202/085713-3601", arxiv="2410.12787",
      code="https://github.com/DAMO-NLP-SG/CMM"),
]
for r in R:
    r["authors"] = au(r["key"])


# ---- HTML ---------------------------------------------------------------------------------------
def display_name(fam, giv):
    return f"{giv} {fam}".strip() if giv else fam


def html_authors(auths):
    names = [display_name(f, g) for f, g in auths]
    if len(names) > 4:
        names = names[:3] + ["et al."]
    return ", ".join("<b>Yang Zhou</b>" if n == "Yang Zhou" else html.escape(n) for n in names)


def dash(p):
    return p.replace("--", "–")


def html_venue(r):
    if r["type"] == "misc":
        return f"arXiv:{r['arxiv']}, {r['year']}."
    if r["type"] == "article":
        s = f"<em>{html.escape(r['journal'])}</em>"
        if r.get("status"):
            return f"{s} ({r['status']}), {r['year']}."
        vol = r.get("volume", "") + (f"({r['number']})" if r.get("number") else "")
        return f"{s}, {vol}:{dash(r['pages'])}, {r['year']}."
    s = f"<em>{html.escape(r['conf'])}</em>"
    if r.get("pages") and r.get("volume"):
        return f"{s}, {r['volume']}({r['number']}):{dash(r['pages'])}, {r['year']}."
    if r.get("pages"):
        return f"{s}, pp. {dash(r['pages'])}, {r['year']}."
    return f"{s}, {r['year']}."


def title_href(r):
    if r.get("doi"):
        return "https://doi.org/" + r["doi"]
    if r.get("arxiv"):
        return "https://arxiv.org/abs/" + r["arxiv"]
    return r["pdf"]


def html_links(r):
    parts = []
    if r.get("short"):
        parts.append(f'<span class="reference-tag">{html.escape(r["short"])}</span>')
    if r.get("doi") and r.get("arxiv"):
        parts.append(f'<a href="https://arxiv.org/abs/{r["arxiv"]}">arXiv</a>')
    if r.get("doi") and r.get("pdf"):
        parts.append(f'<a href="{r["pdf"]}">PDF</a>')
    if r.get("code"):
        parts.append(f'<a href="{r["code"]}">代码</a>')
    if r.get("weights"):
        parts.append(f'<a href="{r["weights"]}">模型权重</a>')
    return " · ".join(parts)


def html_ref(i, r):
    body = [f'<p class="reference-title"><a href="{title_href(r)}">{html.escape(r["title"])}</a></p>',
            f'<p class="reference-authors">{html_authors(r["authors"])}</p>',
            f'<p class="reference-venue">{html_venue(r)}</p>']
    if html_links(r):
        body.append(f'<p class="reference-links">{html_links(r)}</p>')
    return (f'<article class="reference" id="ref-{i}"><span class="reference-number">[{i}]</span><div>'
            + "".join(body) + "</div></article>")


# ---- BibTeX -------------------------------------------------------------------------------------
def bib_author(auths):
    return " and ".join(f"{f}, {g}" if g else "{" + f.replace("&", r"\&") + "}" for f, g in auths)


def bib(r):
    f = [("author", bib_author(r["authors"])), ("title", "{" + r["title"] + "}")]
    if r["type"] == "article":
        f.append(("journal", r["journal"]))
    elif r["type"] == "inproceedings":
        f.append(("booktitle", r["booktitle"]))
    for k in ("volume", "number", "pages", "year"):
        if r.get(k):
            f.append((k, r[k]))
    if r["type"] == "misc":
        f += [("eprint", r["arxiv"]), ("archiveprefix", "arXiv"), ("url", "https://arxiv.org/abs/" + r["arxiv"])]
    if r.get("doi"):
        f.append(("doi", r["doi"]))
    if r.get("arxiv") and r["type"] != "misc":
        f.append(("url", "https://arxiv.org/abs/" + r["arxiv"]))
    elif r.get("pdf"):
        f.append(("url", r["pdf"]))
    if r.get("status"):
        f.append(("note", r["status"]))
    elif r.get("note"):
        f.append(("note", r["note"]))
    w = max(len(k) for k, _ in f)
    return f"@{r['type']}{{{r['key']},\n" + ",\n".join(f"  {k:<{w}} = {{{v}}}" for k, v in f) + "\n}\n"


# ---- write --------------------------------------------------------------------------------------
if __name__ == "__main__":
    with open(BIB, "w", encoding="utf-8") as fh:
        fh.write("% References of the VEGA Lab research guide (vega/research-guide.html), in citation order.\n"
                 "% Numbering [n] in the page equals the order here. Generated by build_references.py.\n\n"
                 + "\n".join(bib(r) for r in R))
    block = ('<p class="bib-download"><a href="references.bib" download>下载 BibTeX 参考文献</a></p>'
             + "\n".join(html_ref(i + 1, r) for i, r in enumerate(R)))
    src = open(GUIDE, encoding="utf-8").read()
    new, n = re.subn(r'<p class="bib-download">.*?(?=</section>\n</main>)', lambda m: block, src, flags=re.S)
    assert n == 1, "reference block not found in research-guide.html"
    cited = sorted({int(x) for x in re.findall(r'href="#ref-(\d+)"', new)})
    assert cited == list(range(1, len(R) + 1)), f"citations {cited} do not match {len(R)} entries"
    open(GUIDE, "w", encoding="utf-8").write(new)
    print(f"{len(R)} references written to {os.path.relpath(BIB)} and {os.path.relpath(GUIDE)}")
