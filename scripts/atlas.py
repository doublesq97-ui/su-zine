"""图谱 (atlas) theme: reference-manual layout for su-zine.

Separate page builder so light/dark HTML stays byte-identical.
All article text is escaped; no HTML is passed through.
"""
import html

KINDS = {"flow", "stack", "tags", "papers", "steps", "table", "files", "cards", "callout"}
NEW_KINDS = {"steps", "table", "files", "cards", "callout"}
LAYOUTS = {"page", "cover", "end"}
STATES = {"", "pending", "done", "dropped"}


def _text(value, where):
    if not isinstance(value, str):
        raise ValueError(f"{where} must be a string")


def _strings(value, where):
    if not isinstance(value, list):
        raise ValueError(f"{where} must be an array")
    for item in value:
        _text(item, where)


def _index(value, where, limit):
    if type(value) is not int or not 0 <= value < max(limit, 1):
        raise ValueError(f"{where} must be a valid index")


def validate(data):
    """Extra checks for atlas-only fields; base validation runs first in build.py."""
    for n, page in enumerate(data["pages"], 1):
        if page.get("layout", "page") not in LAYOUTS:
            raise ValueError(f"page {n}.layout must be page, cover or end")
        if "toc" in page and not isinstance(page["toc"], bool):
            raise ValueError("toc must be true or false")
        if "short" in page:
            _text(page["short"], "short")
        for block in page["blocks"]:
            kind = block["kind"]
            if "num" in block:
                _text(block["num"], "num")
            if kind == "steps":
                n_items = len(block["items"])
                if not 2 <= n_items <= 6:
                    raise ValueError("steps needs 2-6 items")
                for key in ("actions", "back"):
                    if key in block:
                        _strings(block[key], key)
                        if len(block[key]) != n_items - 1:
                            raise ValueError(f"{key} must have one entry per gap")
            if kind == "table":
                _strings(block.get("head"), "head")
                if not 2 <= len(block["head"]) <= 4:
                    raise ValueError("table head needs 2-4 columns")
                rows = block.get("trows")
                if not isinstance(rows, list) or not rows:
                    raise ValueError("trows must be a nonempty array")
                for row in rows:
                    if not isinstance(row, dict):
                        raise ValueError("trows entries must be objects")
                    _strings(row.get("cells"), "cells")
                    if len(row["cells"]) != len(block["head"]):
                        raise ValueError("cells must match head")
                    if row.get("state", "") not in STATES:
                        raise ValueError("state must be pending, done, dropped or empty")
            if kind in ("files", "cards") and not block.get("rows"):
                raise ValueError(f"{kind} needs rows")
            if kind == "cards":
                if "highlight" in block:
                    _index(block["highlight"], "highlight", len(block["rows"]))
                for i in block.get("dropped", []):
                    _index(i, "dropped", len(block["rows"]))
            if kind == "callout" and block.get("tone", "fill") not in ("fill", "outline"):
                raise ValueError("tone must be fill or outline")
    return data


def esc(value):
    return html.escape(value, quote=True).replace("\n", "<br>")


def el(tag, value, cls):
    return f'<{tag} class="{cls}">{esc(value)}</{tag}>'


def _node(text):
    head, _, rest = text.partition("\n")
    sub = f'<span class="node-sub">{esc(rest)}</span>' if rest else ""
    return f'<div class="node"><b>{esc(head)}</b>{sub}</div>'


def steps(block):
    items, acts = block["items"], block.get("actions", [])
    back = block.get("back", [])
    gaps = len(items) - 1
    vertical = len(items) > 4 or block.get("orient") == "vertical"
    out = []
    counter = 0
    fwd_nums = []
    for i in range(gaps):
        if i < len(acts) and acts[i]:
            counter += 1
            fwd_nums.append(counter)
        else:
            fwd_nums.append(0)
    back_nums = [0] * gaps
    for i in reversed(range(gaps)):
        if i < len(back) and back[i]:
            counter += 1
            back_nums[i] = counter
    for i, item in enumerate(items):
        out.append(_node(item))
        if i < gaps:
            label = (f'<span class="act"><i>{fwd_nums[i]:02}</i>{esc(acts[i])}</span>'
                     if fwd_nums[i] else "")
            ret = ""
            if back_nums[i]:
                ret = (f'<div class="arrow back"><span class="line"></span>'
                       f'<span class="act"><i>{back_nums[i]:02}</i>{esc(back[i])}</span></div>')
            out.append(f'<div class="gap"><div class="arrow fwd">{label}<span class="line"></span></div>{ret}</div>')
    cls = "steps-v" if vertical else "steps-h"
    style = "" if vertical else f' style="grid-template-columns:{" 1fr ".join(["auto"] * len(items))}"'
    return f'<div class="{cls}"{style}>' + "".join(out) + "</div>"


def table(block):
    head = "".join(el("th", h, "") for h in block["head"])
    rows = []
    for row in block["trows"]:
        cells = "".join(el("td", c, "") for c in row["cells"])
        rows.append(f'<tr class="{row.get("state", "") or "plain"}">{cells}</tr>')
    return f'<table class="tbl"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


def files(block):
    rows = "".join('<div class="file">' + el("code", a, "fname") + el("div", b, "fnote") + "</div>"
                   for a, b in block["rows"])
    return f'<div class="files">{rows}</div>'


def cards(block):
    hi, dropped = block.get("highlight", -1), set(block.get("dropped", []))
    out = []
    for i, (a, b) in enumerate(block["rows"]):
        cls = "card" + (" hi" if i == hi else "") + (" dropped" if i in dropped else "")
        out.append(f'<div class="{cls}">' + el("div", a, "card-h") + el("div", b, "card-b") + "</div>")
    cols = 3 if len(out) in (3, 6) else 2
    return f'<div class="cards cols{cols}">' + "".join(out) + "</div>"


def callout(block):
    pts = "".join(el("li", t, "") for t in block["items"])
    return f'<ul class="points">{pts}</ul>'


def legacy(block):
    kind = block["kind"]
    items = "".join(f'<div class="litem"><i>{i:02}</i>{esc(t)}</div>'
                    for i, t in enumerate(block["items"], 1))
    return f'<div class="legacy {kind}">{items}</div>'


RENDER = {"steps": steps, "table": table, "files": files, "cards": cards, "callout": callout}


def block_html(block, n):
    kind = block["kind"]
    num = block.get("num", f"{n:02}")
    note = el("span", block["label"], "note") if block.get("label") else ""
    head = (f'<div class="mod-head"><span class="dot">{esc(num)}</span>' +
            el("h2", block["title"], "mod-title") + note + "</div>")
    prose = "".join(el("p", p, "para") for p in block["paras"])
    graphic = RENDER.get(kind, legacy)(block)
    extra = ""
    if block.get("rows") and kind not in ("files", "cards"):
        extra = files(block)
    panel = el("div", block["panel"], "panel") if block.get("panel") else ""
    cap = el("div", block["caption"], "caption") if block["caption"] else ""
    tone = f' tone-{block.get("tone", "fill")}' if kind == "callout" else ""
    return (f'<section class="mod k-{kind}">{head}{prose}'
            f'<div class="board{tone}">{panel}{graphic}{extra}</div>{cap}</section>')


def toc(data, number):
    rows = []
    for i, page in enumerate(data["pages"], 1):
        if i == number:
            continue
        label = page.get("short") or page.get("sub") or page["title"].split("\n")[0]
        rows.append(f'<div class="toc-row"><i>{i:02}</i>{esc(label)}</div>')
    return '<nav class="toc"><div class="toc-h">本组目录</div>' + "".join(rows) + "</nav>"


def page_html(data, page, number):
    layout = page.get("layout", "page")
    blocks = "".join(block_html(b, i) for i, b in enumerate(page["blocks"], 1))
    checks = "".join("<div>" + el("div", a, "check-label") + el("div", b, "check-body") + "</div>"
                     for a, b in page.get("checks", []))
    checklist = el("h2", page["checktitle"], "checktitle") if page.get("checktitle") else ""
    if checks:
        checklist += f'<div class="checks">{checks}</div>'
    tag = el("div", page["sub"], "tag") if page.get("sub") else ""
    closing = el("div", page["closing"], "closing") if page.get("closing") else ""
    nav = toc(data, number) if page.get("toc") else ""
    total = len(data["pages"])
    body = (f'<main class="sheet atlas layout-{layout}"><header class="mast">' +
            el("span", data["series"], "series") + el("span", data["brand"], "brand") +
            "</header>" + tag + el("h1", page["title"], "title") + el("div", page["intro"], "intro") +
            nav + blocks + checklist + closing +
            '<footer class="footer"><div class="src"><span class="src-k">SOURCE</span>' +
            el("span", page["source"], "source") + "</div>" +
            f'<div class="sign">{esc(data["brand"])}<span class="num">{number:02} / {total:02}</span></div>'
            "</footer></main>")
    return ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(page["title"])}</title><link rel="stylesheet" href="style.css">'
            "</head><body>" + body + "</body></html>")
