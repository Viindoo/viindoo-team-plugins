#!/usr/bin/env python3
"""Build a bilingual viindoo.com blog post from a JSON spec.

Usage: build_post.py spec.json [out_dir]   (out_dir defaults to the spec's directory)

Spec format (every text is a pair [en, vi]; inline <strong>/<em>/<a> allowed, nothing else):
{
  "slug": "post2",                                   # prefix for output files
  "create": {"blog_id": 12, "website_id": 1, "author_id": 541},
  "meta": {"name": [en, vi], "subtitle": [en, vi], "website_meta_title": [en, vi],
           "website_meta_description": [en, vi], "website_meta_keywords": [en, vi],
           "seo_name": [en, vi]},
  "blocks": [
    {"p": [en, vi]}, {"h2": [en, vi]}, {"h3": [en, vi]}, {"quote": [en, vi]},
    {"ul": [[en, vi], ...]}, {"ol": [[en, vi], ...]},
    {"table": {"rows": [[[en, vi], ...], ...], "right_cols": [1, 2]}},   # first row = header
    {"figure": {"src": "/web/image/..", "src_vi": "/web/image/.. (optional)",
                "alt": [en, vi], "caption": [en, vi]}},
    {"cards": {"cols": 2|3, "items": [{"title": [en, vi], "text": [en, vi]}, ...]}},  # s_three_columns
    {"steps": [{"icon": "fa-eye", "title": [en, vi], "text": [en, vi] (optional)}, ...]},  # s_process_steps
    {"alert": [en, vi]} or {"alert": {"tone": "info|warning|success", "text": [en, vi]}},  # s_alert
    {"faq": [{"q": [en, vi], "a": [en, vi]}, ...]}                                   # s_faq_collapse
  ],
  "separators": true,   # s_hr line between h2 sections (default true)
  "related": [{"url": "/blog/..", "en": "title", "vi": "tiêu đề"}],      # optional
  "cta": true                                                             # site CTA snippet
}

Outputs in out_dir:
  <slug>_content_en.html     EN source HTML (what gets created)
  <slug>_content_vi.html     VI HTML for human review only
  <slug>_vi_map.json         {"terms": [[en_html, vi_html], ...], "src_map": {src_en: src_vi}}
  <slug>_meta.json           {field: [en, vi]}
  <slug>_create_values.json  values for blog.post.create (EN, is_published False)
Prints word counts, meta lengths and any long dash (U+2012..U+2015) found.
"""
import html
import json
import pathlib
import re
import sys

CTA = '''<section class="s_text_image o_colored_level pt0 pb0 bg-800 s_custom_snippet" data-snippet="s_image_text" style="background-image: none;" data-name="CTA Blogs - Transform your business ">
        <div class="container">
            <div class="row o_grid_mode" data-row-count="6" style="--grid-item-padding-y: 0px; --grid-item-padding-x: 0px;">
                <div class="o_colored_level o_grid_item g-col-lg-6 o_grid_item_image g-height-6 col-lg-6" style="grid-area: 1 / 1 / 7 / 7; z-index: 1;"><img src="/web/image/6521075-43f92e7b/PAC07190%20sua%202%20%281%29.jpg" alt="Start your digital transformation with Viindoo" class="img img-fluid mx-auto o_we_custom_image o_we_image_cropped" data-original-id="6427746" data-original-src="/web/image/6427746-0a26a54a/PAC07190%20sua%202%20%281%29.jpg" data-mimetype="image/jpeg" data-x="297.9310344827586" data-y="157.24137931034483" data-width="1622.0689655172414" data-height="969.655172413793" data-scale-x="1" data-scale-y="1" data-aspect-ratio="0/0" loading="lazy"></div>
                <div class="o_colored_level o_grid_item g-height-5 g-col-lg-4 col-lg-4" style="grid-area: 2 / 8 / 7 / 12; z-index: 2;">
                    <h2>Start to transform your business&nbsp;</h2><p><br></p><p><a href="/services/express-packs" class="btn btn-primary">Start now</a>&nbsp; &nbsp;<a href="/appointment/a-solution-consultation-1" class="btn btn-secondary">Schedule a meeting</a><br></p>
                </div>
            </div>
        </div>
    </section>'''
CTA_TERMS = [["Start to transform your business", "Bắt đầu chuyển đổi doanh nghiệp của bạn"],
             ["Start now", "Bắt đầu ngay"], ["Schedule a meeting", "Đặt lịch tư vấn"],
             ["Start your digital transformation with Viindoo", "Bắt đầu chuyển đổi số cùng Viindoo"]]
ALLOWED_TAGS = ("strong", "em", "b", "a")


def esc(text):
    """Escape text but keep the few inline tags authors are allowed to use."""
    out = html.escape(text, quote=False)
    for tag in ALLOWED_TAGS:
        out = re.sub(rf"&lt;({tag}(?: [^&]*?)?)&gt;", lambda m: "<" + html.unescape(m.group(1)) + ">", out)
        out = out.replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return out


TEAL = "rgb(0, 184, 204)"
CARD_BG = "rgba(0, 184, 204, 0.08)"


def build(spec, i):
    """Render one language. Layout follows the snippets used by the best posts on viindoo.com:
    every h2 opens its own text section, sections are separated by an s_hr line, and rich
    blocks (cards, steps, alert, faq) are emitted as their own website snippets."""
    sections, cur, terms, src_map = [], [], [], {}
    toc = 0
    uid = [0]

    def nid():
        uid[0] += 1
        return f"{spec.get('slug', 'post')}{uid[0]}"

    def flush():
        if cur:
            sections.append('<section class="s_text_block o_colored_level pt32 pb16" data-snippet="s_text_block" '
                            'data-name="Text" style="background-image: none;">\n<div class="container s_allow_columns">\n'
                            + "\n".join(cur) + "\n</div></section>")
            cur.clear()

    def t(pair):
        terms.append(pair)
        return esc(pair[i])

    blocks = list(spec["blocks"])
    if spec.get("related"):
        blocks.append({"h2": ["Related articles", "Bài viết liên quan"]})
        blocks.append({"ul": [[f'<a href="{r["url"]}">{r["en"]}</a>', f'<a href="{r["url"]}">{r["vi"]}</a>']
                              for r in spec["related"]]})
    first_h2 = True
    for b in blocks:
        (kind, val), = b.items()
        if kind == "h2":
            flush()
            if not first_h2 and spec.get("separators", True):
                sections.append('<div class="s_hr text-start pt16 pb16" data-snippet="s_hr" data-name="Separator">'
                                '<hr class="w-100 mx-auto" style="border-top-width: 1px; border-top-style: solid;"></div>')
            first_h2 = False
            toc += 1
            cur.append(f'<h2 id="vtoc_{toc}"><b>{t(val)}</b></h2>')
        elif kind == "h3":
            cur.append(f"<h3>{t(val)}</h3>")
        elif kind == "p":
            cur.append(f'<p style="text-align: justify;">{t(val)}</p>')
        elif kind == "quote":
            cur.append('<blockquote class="s_blockquote s_blockquote_classic w-100 mx-auto o_animable blockquote" '
                       'data-snippet="s_blockquote" data-name="Blockquote"><i class="s_blockquote_icon fa fa-1x fa-quote-left '
                       'bg-o-color-2 rounded"></i><div class="s_blockquote_content bg-100">'
                       f'<p><strong>{t(val)}</strong></p></div></blockquote>')
        elif kind == "alert":
            tone = val.get("tone", "info") if isinstance(val, dict) else "info"
            text = val["text"] if isinstance(val, dict) else val
            icon = {"info": "fa-info-circle", "warning": "fa-exclamation-triangle", "success": "fa-check-circle"}[tone]
            cur.append(f'<div class="s_alert s_alert_md alert-{tone} w-100 clearfix" data-snippet="s_alert" data-name="Alert">'
                       f'<i class="fa s_alert_icon {icon}"></i><div class="s_alert_content"><p>{t(text)}</p></div></div>')
        elif kind in ("ul", "ol"):
            cur.append(f'<{kind} style="text-align: justify;">' + "".join(f"<li>{t(item)}</li>" for item in val) + f"</{kind}>")
        elif kind == "table":
            right = set(val.get("right_cols", []))
            rows = []
            for r, row in enumerate(val["rows"]):
                tag = "th" if r == 0 else "td"
                rows.append("<tr>" + "".join(f'<{tag}{" style=\"text-align: right;\"" if c in right else ""}>{t(cell)}</{tag}>'
                                             for c, cell in enumerate(row)) + "</tr>")
            cur.append('<table class="table table-bordered"><tbody>' + "".join(rows) + "</tbody></table>")
        elif kind == "figure":
            src = val["src"] if i == 0 or not val.get("src_vi") else val["src_vi"]
            if val.get("src_vi"):
                src_map[val["src"]] = val["src_vi"]
            terms.append(val["alt"])
            alt = html.escape(val["alt"][i], quote=True)
            cur.append(f'<div style="text-align: center; margin: 24px 0;"><img src="{src}" alt="{alt}" title="{alt}" '
                       f'class="img img-fluid mx-auto" loading="lazy"><p style="text-align: center;"><em>{t(val["caption"])}</em></p></div>')
        elif kind == "cards":
            flush()
            items = val["items"]
            width = {1: 12, 2: 6, 3: 4, 4: 6}.get(val.get("cols", 0), 6 if len(items) in (2, 4) else 4)
            cols = []
            for it in items:
                body = f'<p class="card-title" style="font-size: 1.125rem;"><strong>{t(it["title"])}</strong></p>'
                if it.get("text"):
                    body += f'<p class="card-text">{t(it["text"])}</p>'
                cols.append(f'<div class="s_col_no_bgcolor pt16 pb16 col-lg-{width}"><div class="card text-bg-white h-100" '
                            f'style="background-color: {CARD_BG}; border-color: {TEAL};"><div class="card-body">{body}</div></div></div>')
            sections.append('<section class="s_three_columns o_colored_level pt0 pb24" data-vcss="001" data-snippet="s_three_columns" '
                            'data-name="Columns" style="background-image: none;"><div class="container"><div class="row d-flex align-items-stretch">'
                            + "".join(cols) + "</div></div></section>")
        elif kind == "steps":
            flush()
            n = len(val)
            width = max(2, 12 // n) if n <= 6 else 2
            offset = (12 - width * n) // 2
            steps = []
            for k, st in enumerate(val):
                conn = ('' if k == n - 1 else
                        '<svg class="s_process_step_connector" viewBox="0 0 100 80" preserveAspectRatio="none" '
                        'style="left: calc(50% + 40px); height: 80px; width: calc(100% - 80px);"><path d="M 0 40 L 100 40" '
                        f'vector-effect="non-scaling-stroke" style="stroke: {TEAL};"></path></svg>')
                off = f" offset-lg-{offset}" if k == 0 and offset else ""
                text = f'<p style="text-align: center;">{t(st["text"])}</p>' if st.get("text") else ""
                steps.append(f'<div class="s_process_step pt24 pb24 o_colored_level col-lg-{width}{off}">{conn}'
                             f'<div class="s_process_step_icon"><i class="fa {st.get("icon", "fa-circle")} mx-auto fa-3x" '
                             f'style="color: {TEAL};"></i></div><div class="s_process_step_content">'
                             f'<p style="text-align: center;"><strong>{t(st["title"])}</strong></p>{text}</div></div>')
            sections.append('<section class="s_process_steps o_colored_level s_process_steps_connector_line pt24 pb24" data-vcss="001" '
                            'data-snippet="s_process_steps" data-name="Steps" style="background-image: none;"><div class="container">'
                            '<div class="row g-0">' + "".join(steps) + "</div></div></section>")
        elif kind == "faq":
            flush()
            acc = nid()
            items = []
            for k, qa in enumerate(val):
                tab = f"{acc}t{k}"
                items.append(f'<div class="card bg-100" data-name="Item"><a href="#" role="tab" aria-expanded="false" '
                             f'class="card-header collapsed" data-bs-toggle="collapse" data-bs-target="#{tab}" aria-controls="{tab}">'
                             f'{t(qa["q"])}</a><div class="collapse" role="tabpanel" id="{tab}" data-bs-parent="#{acc}">'
                             f'<div class="card-body"><p class="card-text" style="text-align: justify;">{t(qa["a"])}</p></div></div></div>')
            sections.append('<section class="s_faq_collapse o_colored_level pt8 pb32 s_faq_collapse_boxed" data-snippet="s_faq_collapse" '
                            f'data-name="FAQ" style="background-image: none;"><div class="container"><div id="{acc}" class="accordion" role="tablist">'
                            + "".join(items) + "</div></div></section>")
        else:
            raise ValueError(f"unknown block kind: {kind}")
    flush()
    page = "\n".join(sections)
    if spec.get("cta", True):
        page += "\n\n" + CTA
        terms.extend(CTA_TERMS)
    return page, terms, src_map


def main():
    spec_path = pathlib.Path(sys.argv[1])
    out_dir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else spec_path.parent
    spec = json.loads(spec_path.read_text())
    slug = spec.get("slug", spec_path.stem)
    en_html, terms, src_map = build(spec, 0)
    vi_html, _, _ = build(spec, 1)
    meta = spec["meta"]
    (out_dir / f"{slug}_content_en.html").write_text(en_html)
    (out_dir / f"{slug}_content_vi.html").write_text(vi_html)
    (out_dir / f"{slug}_vi_map.json").write_text(json.dumps({"terms": terms, "src_map": src_map}, ensure_ascii=False))
    (out_dir / f"{slug}_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    values = {**spec["create"], "is_published": False, **{k: v[0] for k, v in meta.items()}, "content": en_html}
    (out_dir / f"{slug}_create_values.json").write_text(json.dumps(values, ensure_ascii=False))

    strip = lambda s: re.sub("<[^>]+>", "", s)
    blob = json.dumps(spec, ensure_ascii=False)
    print(f"terms={len(terms)} en_words={sum(len(strip(e).split()) for e, _ in terms)} "
          f"vi_words={sum(len(strip(v).split()) for _, v in terms)} images_per_lang={len(src_map)}")
    dashes = re.findall("[‒–—―]", blob)
    print("long_dashes:", len(dashes), "(must be 0)")
    limits = {"website_meta_title": 60, "website_meta_description": 160}
    for k, (e, v) in meta.items():
        flag = "  <-- too long" if k in limits and max(len(e), len(v)) > limits[k] else ""
        print(f"{k}: en={len(e)} vi={len(v)}{flag}")
    print("outputs in", out_dir)


if __name__ == "__main__":
    main()
