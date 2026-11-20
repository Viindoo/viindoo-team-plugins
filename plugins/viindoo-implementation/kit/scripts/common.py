# -*- coding: utf-8 -*-
"""Shared helpers for the viindoo-implementation kit.

- Locates the project data folder (one folder per customer) and the output folder.
- Loads the customer data modules from that folder (project.py, handbook.py, setup_tasks.py).
- Locates the viindoo-presales plugin, whose brand (brand.yaml, logos, vdoc) is reused by reference.
- Renders the shared report shell (brand CSS + logo) used by every HTML output of the kit.

Nothing here hardcodes a machine path: everything comes from arguments, environment variables
or paths relative to this plugin.
"""
import argparse
import glob
import html
import importlib.util
import os
import pathlib
import re
import sys

sys.dont_write_bytecode = True   # không để __pycache__ trong thư mục dữ liệu của khách

SCRIPTS = pathlib.Path(__file__).resolve().parent
KIT = SCRIPTS.parent
PLUGIN = KIT.parent
ASSETS = KIT / "assets"
FONT_DIR = ASSETS / "fonts"
EXAMPLE = KIT / "examples" / "sample"

ENV_DATA = "VIINDOO_PROJECT_DATA"
ENV_OUT = "VIINDOO_PROJECT_OUT"
ENV_PRESALES = "VIINDOO_PRESALES_ROOT"

BANNED_DASH = re.compile("[\u2012\u2013\u2014\u2015]")


# ------------------------------------------------------------------ arguments and folders
def cli(description, extra=None, argv=None):
    """Parse --data / --out (plus extra arguments) and export them as environment variables,
    so engine modules imported afterwards find the same folders."""
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--data", help=f"thư mục dữ liệu dự án (mặc định ${ENV_DATA})")
    p.add_argument("--out", help=f"thư mục ra (mặc định ${ENV_OUT}, hoặc '<data>/../Triển khai')")
    if extra:
        extra(p)
    a = p.parse_args(argv)
    if a.data:
        os.environ[ENV_DATA] = str(pathlib.Path(a.data).expanduser().resolve())
    if a.out:
        os.environ[ENV_OUT] = str(pathlib.Path(a.out).expanduser().resolve())
    data_dir()   # fail early with a clear message
    return a


def data_dir():
    d = os.environ.get(ENV_DATA)
    if not d:
        raise SystemExit(f"Chưa chỉ thư mục dữ liệu dự án: chạy với --data <thư mục> hoặc đặt ${ENV_DATA}")
    p = pathlib.Path(d).expanduser().resolve()
    if not p.is_dir():
        raise SystemExit(f"Không thấy thư mục dữ liệu dự án: {p}")
    return p


def out_dir(sub=""):
    o = os.environ.get(ENV_OUT)
    p = pathlib.Path(o).expanduser().resolve() if o else data_dir().parent / "Triển khai"
    if sub:
        p = p / sub
    p.mkdir(parents=True, exist_ok=True)
    return p


def internal_dir():
    """Internal documents never go to the customer: they live in a separate sub-folder."""
    return out_dir("Nội bộ")


def work_dir():
    """Scratch for intermediate files (diagram images, font logs): beside the data, never in the customer folder."""
    p = data_dir() / "_tam"
    p.mkdir(parents=True, exist_ok=True)
    return p


# ------------------------------------------------------------------ customer data modules
def load(name, required=True):
    """Import <data>/<name>.py once and register it under its plain name."""
    if name in sys.modules:
        return sys.modules[name]
    path = data_dir() / f"{name}.py"
    if not path.exists():
        if required:
            raise SystemExit(f"Thiếu tệp dữ liệu {path} - xem mẫu trong {EXAMPLE}")
        return None
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def data_file(name):
    return data_dir() / name


# ------------------------------------------------------------------ viindoo-presales (brand, kit)
def presales_root():
    """viindoo-presales holds the Viindoo brand (brand.yaml, logos) and the document kit (vdoc).
    Order: $VIINDOO_PRESALES_ROOT, the sibling folder in the same repo checkout, the newest copy in
    the Claude Code plugin cache."""
    cands = []
    if os.environ.get(ENV_PRESALES):
        cands.append(pathlib.Path(os.environ[ENV_PRESALES]).expanduser())
    cands.append(PLUGIN.parent / "viindoo-presales")
    cands += [pathlib.Path(p) for p in sorted(glob.glob(os.path.expanduser("~/.claude/plugins/cache/*/viindoo-presales/*")), reverse=True)]
    for c in cands:
        if (c / "brand" / "brand.yaml").exists() and (c / "kit" / "lib" / "vdoc.py").exists():
            return c
    raise SystemExit("Không tìm thấy plugin viindoo-presales (brand, kit). Cài plugin viindoo-presales "
                     f"hoặc đặt ${ENV_PRESALES} trỏ vào thư mục plugin đó.")


def brand_yaml():
    return presales_root() / "brand" / "brand.yaml"


def vdoc():
    lib = str(presales_root() / "kit" / "lib")
    if lib not in sys.path:
        sys.path.insert(0, lib)
    import vdoc as _v  # noqa: E402
    return _v


# ------------------------------------------------------------------ small text helpers
def e(s):
    return html.escape(str(s), quote=False)


def hours(x):
    """Hours in Vietnamese notation: 1.5 -> '1,5'."""
    return f"{x:g}".replace(".", ",") if x is not None else ""


def ul(items, cls="kv"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"


def report_css():
    return (ASSETS / "report.css").read_text(encoding="utf-8")


def page(title, h1, sub, body, css_extra="", toc="", intro=""):
    """Shared report shell: brand CSS, color logo on white, title block, optional table of contents."""
    logo = vdoc().logo_svg(nen_toi=False)
    nav = f'<nav class="toc"><b>Nội dung</b><ul>{toc}</ul></nav>' if toc else ""
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&amp;family=Roboto:wght@400;500;700&amp;display=swap" rel="stylesheet">
<style>{report_css()}
{css_extra}
</style></head><body>
<header class="top"><div class="wrap">
<div><h1>{e(h1)}</h1><div class="sub">{sub}</div></div>
{logo}
</div></header>
<main class="wrap">
{intro}
{nav}
{body}
</main></body></html>"""


def check_text(doc, where, ban_words=()):
    """Every artifact: ASCII hyphen only; customer documents also must not leak banned words."""
    errors = []
    if BANNED_DASH.search(doc):
        errors.append(f"{where}: có gạch ngang dài (en/em dash)")
    plain = re.sub(r"<[^>]+>", " ", doc)
    for w in ban_words:
        if re.search(rf"\b{re.escape(w)}\b", plain):
            errors.append(f"{where}: có từ '{w}' trong bản gửi khách")
    return errors


def write(path, text):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path
