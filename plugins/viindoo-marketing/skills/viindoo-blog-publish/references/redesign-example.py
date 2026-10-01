"""Turn the flat article-4 spec into the sectioned snippet layout (text unchanged, only presentation)."""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).parent
spec = json.loads((HERE / "bai4_spec.json").read_text())
B = spec["blocks"]


def idx_h2(prefix):
    return next(k for k, b in enumerate(B) if "h2" in b and b["h2"][0].startswith(prefix))


def next_h2(k):
    return next((j for j in range(k + 1, len(B)) if "h2" in B[j]), len(B))


def split_strong(pair):
    """'<strong>Title</strong> rest' -> (title_pair, text_pair)."""
    out_t, out_x = [], []
    for s in pair:
        m = re.match(r"^<strong>(.*?)</strong>\s*(.*)$", s, re.S)
        out_t.append(m.group(1).rstrip(":") if m else s)
        x = m.group(2) if m else ""
        out_x.append(x[:1].upper() + x[1:])
    return out_t, out_x


# 1. three activity groups: h3 + p pairs -> cards
k = idx_h2("Kaizen does not mean cutting every step")
end = next_h2(k)
seg = B[k + 1:end]
intro = [b for b in seg if "p" in b][:1]
pairs, items = [b for b in seg if "h3" in b or "p" in b][1:], []
for j in range(0, len(pairs), 2):
    items.append({"title": pairs[j]["h3"], "text": pairs[j + 1]["p"]})
B[k + 1:end] = intro + [{"cards": {"cols": 3, "items": items}}]

# 2. four questions (ol) -> 2x2 cards
k = idx_h2("Data entry should only happen")
end = next_h2(k)
for j in range(k, end):
    if "ol" in B[j]:
        its = []
        for pair in B[j]["ol"]:
            title, text = split_strong(pair)
            its.append({"title": title, "text": text})
        B[j] = {"cards": {"cols": 2, "items": its}}
        break

# 3. three levels: h3 + p -> cards, figure moved after the cards
k = idx_h2("Three levels of data")
end = next_h2(k)
seg = B[k + 1:end]
figs = [b for b in seg if "figure" in b]
paras = [b for b in seg if "p" in b]
lvl, j = [], 0
rest = [b for b in seg if "h3" in b or ("p" in b and b is not paras[0])]
for j in range(0, len(rest), 2):
    lvl.append({"title": rest[j]["h3"], "text": rest[j + 1]["p"]})
B[k + 1:end] = [paras[0], {"cards": {"cols": 3, "items": lvl}}] + figs

# 4. what gets reused (ul of 5) -> cards
k = idx_h2("Viindoo's role")
end = next_h2(k)
for j in range(k, end):
    if "ul" in B[j]:
        its = []
        for pair in B[j]["ul"]:
            title, text = split_strong(pair)
            its.append({"title": title, "text": text})
        B[j] = {"cards": {"cols": 3, "items": its}}
        break

# 5. the loop quote -> process steps with icons
k = idx_h2("A good ERP should reduce tasks over time")
end = next_h2(k)
icons = ["fa-pencil-square-o", "fa-bar-chart", "fa-lightbulb-o", "fa-list-alt", "fa-cogs", "fa-compress"]
for j in range(k, end):
    if "quote" in B[j] and "→" in B[j]["quote"][0]:
        en = [x.strip() for x in B[j]["quote"][0].split("→")]
        vi = [x.strip() for x in B[j]["quote"][1].split("→")]
        B[j] = {"steps": [{"icon": ic, "title": [e, v]} for ic, e, v in zip(icons, en, vi)]}
        break

# 6. "wrong digitalization" closing quote -> warning alert
k = idx_h2("Wrong digitalization")
end = next_h2(k)
for j in range(k, end):
    if "quote" in B[j]:
        B[j] = {"alert": {"tone": "warning", "text": B[j]["quote"]}}
        break

# 7. FAQ h3 + p -> accordion
k = idx_h2("Frequently asked questions")
end = next_h2(k)
seg = B[k + 1:end]
qa = [{"q": seg[j]["h3"], "a": seg[j + 1]["p"]} for j in range(0, len(seg), 2)]
B[k + 1:end] = [{"faq": qa}]

# 8. next-article teaser -> info alert
k = idx_h2("Next in the series")
B[k + 1] = {"alert": {"tone": "info", "text": B[k + 1]["p"]}}

spec["separators"] = True
(HERE / "bai4_spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print("kinds:", [list(b)[0] for b in B])
