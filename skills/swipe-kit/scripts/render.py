#!/usr/bin/env python3
"""swipe-kit renderer: spec.json -> 01.png ... + preview.png + caption.txt

Usage:  python3 render.py spec.json out_dir
Needs:  playwright (chromium), Pillow
"""
import base64, colorsys, html, json, math, mimetypes, re, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"
W, H = 1080, 1350
ICON_COLORS = ["#FF7A59", "#3DD68C", "#4C8DFF", "#FFC233", "#B57CFF", "#FF5C8A"]
NOTIF_POS = [(72, 540, -2), (228, 700, 1.5), (110, 860, -1)]  # left, top, rotate


# ── text helpers ─────────────────────────────────────────────
def esc(s):
    """escape, \\n -> <br>, *word* -> serif italic emphasis"""
    t = html.escape(str(s or ""))
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t.replace("\n", "<br>")


def mark(s, word):
    t = esc(s)
    w = html.escape(word or "")
    return t.replace(w, f"<mark>{w}</mark>", 1) if w else t


# ── color helpers ────────────────────────────────────────────
def rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hexc(c):
    return "#" + "".join(f"{round(max(0, min(1, v)) * 255):02X}" for v in c)


def lum(h):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in rgb(h)); return 0.2126 * r + 0.7152 * g + 0.0722 * b


def on(h):  # readable text color for a background
    return "#111111" if lum(h) > 0.36 else "#FFFFFF"


def tokens(brand, accent):
    r, g, b = rgb(brand)
    mix = lambda t: hexc(tuple(v + (1 - v) * t for v in (r, g, b)))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    light = mix(0.93) if s > 0.15 else "#F4F4F2"
    return {"brand": brand, "on-brand": on(brand), "accent": accent, "on-accent": on(accent),
            "light": light, "tint": mix(0.86) if s > 0.15 else "#E8E8E6"}


def scallop(n=18, depth=0.09):  # clip-path polygon for a scalloped sticker
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = 0.5 if i % 2 == 0 else 0.5 - depth
        pts.append(f"{50 + rr * 100 * math.cos(a):.2f}% {50 + rr * 100 * math.sin(a):.2f}%")
    return "polygon(" + ",".join(pts) + ")"


STICKER_CLIP = scallop()


def sticker(text):
    return f'<div class="sticker" style="clip-path:{STICKER_CLIP}">{esc(text)}</div>' if text else ""


def img_uri(path, base):
    p = Path(path)
    if not p.is_absolute():
        p = (base / p).resolve()
    mt = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mt};base64," + base64.b64encode(p.read_bytes()).decode()


# ── slide builders ───────────────────────────────────────────
def chrome(ctx, i):
    b = ctx["brand"]; n = ctx["n"]
    swipe = '<span class="swipe">Swipe →</span>' if i < n - 1 else "<span></span>"
    if ctx["lang"] == "ko" and i < n - 1:
        swipe = '<span class="swipe">넘겨보기 →</span>'
    handle = esc(b.get("handle") or "")
    return (f'<div class="chrome top"><span class="wordmark">{esc(b["name"])}</span>'
            f'<span class="count">{i + 1:02d} / {n:02d}</span></div>'
            f'<div class="chrome bot"><span>{handle}</span>{swipe}</div>')


def s_cover(d, ctx, i):
    kicker = f'<span class="pill kicker">{esc(d["kicker"])}</span>' if d.get("kicker") else ""
    sub = f'<p class="sub" data-fit>{esc(d.get("subtitle"))}</p>' if d.get("subtitle") else ""
    return f'''<div class="slide s-brand cover">{chrome(ctx, i)}{kicker}{sticker(d.get("sticker"))}
<div class="region"><h1 class="disp" data-fit>{esc(d["title"])}</h1>{sub}</div></div>'''


def s_problem(d, ctx, i):
    notes = d.get("notes", [])[:3]
    if len(notes) < 2:
        raise ValueError("problem: needs 2-3 notes")
    out = ""
    for k, (n, (x, y, r)) in enumerate(zip(notes, NOTIF_POS)):
        sub = f'<small>{esc(n.get("sub"))}</small>' if n.get("sub") else ""
        t = f'<span class="t">{esc(n.get("time"))}</span>' if n.get("time") else ""
        out += (f'<div class="notif" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">'
                f'<div class="ico" style="background:{ICON_COLORS[k]}"></div><div><b>{esc(n["label"])}</b>{sub}</div>{t}</div>')
    return f'''<div class="slide s-dark problem">{chrome(ctx, i)}
<div class="region top"><h2 class="disp" data-fit>{esc(d["title"])}</h2></div>{out}
<div class="region bottom"><p class="disp answer" data-fit>{mark(d.get("answer"), ctx["brand"]["name"])}</p></div></div>'''


def s_feature(d, ctx, i):
    sub = f'<p class="sub" data-fit>{esc(d.get("subtitle"))}</p>' if d.get("subtitle") else ""
    if d.get("screenshot"):
        phone = f'<div class="phone shot"><img src="{img_uri(d["screenshot"], ctx["base"])}"></div>'
    else:
        sc = d.get("screen", {})
        chips = "".join(f'<span class="chip{" on" if k == 0 else ""}">{esc(c)}</span>' for k, c in enumerate(sc.get("chips", [])[:4]))
        items = ""
        for k, it in enumerate(sc.get("items", [])[:5]):
            badge = f'<span class="badge">{esc(it.get("badge"))}</span>' if it.get("badge") else ""
            color = it.get("color") or ICON_COLORS[k % len(ICON_COLORS)]
            items += f'<div class="item"><div class="logo" style="background:{color}"></div><div><b>{esc(it.get("name"))}</b><small>{esc(it.get("meta"))}</small></div>{badge}</div>'
        search = f'<div class="search">{esc(sc["search"])}</div>' if sc.get("search") else ""
        phone = f'<div class="phone">{search}<div class="chips">{chips}</div>{items}</div>'
    call = f'<div class="callout">{esc(d["callout"])}</div>' if d.get("callout") else ""
    return f'''<div class="slide s-light feature">{chrome(ctx, i)}
<div class="region"><h2 class="disp" data-fit>{esc(d["title"])}</h2>{sub}</div>{phone}{call}</div>'''


def s_steps(d, ctx, i):
    steps = d.get("steps", [])
    if not 2 <= len(steps) <= 4:
        raise ValueError("steps: needs 2-4 steps (split longer sequences across slides with \"start\")")
    n0 = int(d.get("start", 1))
    lst = "".join(f'<div class="step"><div class="n">{k + n0:02d}</div><div><b data-fit>{esc(s["title"])}</b>'
                  f'<span data-fit>{esc(s.get("desc"))}</span></div></div>' for k, s in enumerate(steps))
    return f'''<div class="slide s-light steps">{chrome(ctx, i)}
<div class="region top"><h2 class="disp" data-fit>{esc(d["title"])}</h2></div>
<div class="region list">{lst}</div></div>'''


def s_list(d, ctx, i):
    items = d.get("items", [])
    if not 2 <= len(items) <= 5:
        raise ValueError("list: needs 2-5 items (split longer lists across slides)")
    lst = ""
    for it in items:
        desc = f'<span data-fit>{esc(it.get("desc"))}</span>' if it.get("desc") else ""
        val = f'<div class="v" data-fit>{esc(it.get("value"))}</div>' if it.get("value") else ""
        lst += f'<div class="row"><div><b data-fit>{esc(it["title"])}</b>{desc}</div>{val}</div>'
    return f'''<div class="slide s-light list">{chrome(ctx, i)}
<div class="region top"><h2 class="disp" data-fit>{esc(d["title"])}</h2></div>
<div class="region rows">{lst}</div></div>'''


def s_photo(d, ctx, i):
    sub = f'<p class="sub" data-fit>{esc(d.get("subtitle"))}</p>' if d.get("subtitle") else ""
    return f'''<div class="slide s-light photo">{chrome(ctx, i)}
<div class="region"><h2 class="disp" data-fit>{esc(d["title"])}</h2>{sub}</div>
<div class="frame"><img src="{img_uri(d["image"], ctx["base"])}"></div></div>'''


def s_point(d, ctx, i):
    body = f'<p class="body" data-fit>{esc(d.get("body"))}</p>' if d.get("body") else ""
    q = '<div class="q">“</div>' if d.get("quote") else ""
    return f'''<div class="slide s-accent point">{chrome(ctx, i)}
<div class="region">{q}<h2 class="disp" data-fit>{esc(d["title"])}</h2>{body}</div></div>'''


def s_cta(d, ctx, i):
    sub = f'<p class="sub" data-fit>{esc(d.get("subtitle"))}</p>' if d.get("subtitle") else ""
    btn = d.get("button") or ("프로필 링크에서 →" if ctx["lang"] == "ko" else "Link in bio →")
    return f'''<div class="slide s-brand cta">{chrome(ctx, i)}
<div class="region"><h1 class="disp" data-fit>{esc(d["title"])}</h1>{sub}</div>
<div class="btn">{esc(btn)}</div>{sticker(d.get("sticker"))}</div>'''


BUILDERS = {"cover": s_cover, "problem": s_problem, "feature": s_feature,
            "steps": s_steps, "list": s_list, "photo": s_photo, "point": s_point, "cta": s_cta}

# shrink [data-fit] text together until each .region fits (min 62%); report what happened
FIT_JS = """() => {
  // overflow = how far the content box (not glyph ink) sticks out of the region
  const over = rg => {
    const r = rg.getBoundingClientRect(), kids = [...rg.children];
    if (!kids.length) return 0;
    const top = Math.min(...kids.map(k => k.getBoundingClientRect().top));
    const bot = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
    return Math.max(r.top - top, bot - r.bottom, rg.scrollHeight - rg.clientHeight - 30);
  };
  const warns = [];
  document.querySelectorAll('.slide').forEach((sl, si) => {
    sl.querySelectorAll('.region').forEach(rg => {
      const els = [...rg.querySelectorAll('[data-fit]')];
      const base = els.map(e => parseFloat(getComputedStyle(e).fontSize));
      let s = 1;
      while (over(rg) > 2 && s > 0.62) {
        s -= 0.03; els.forEach((e, i) => e.style.fontSize = (base[i] * s) + 'px');
      }
      if (s < 0.97) warns.push({slide: si + 1, shrink: Math.round(s * 100)});
      if (over(rg) > 2) warns.push({slide: si + 1, overflow: true});
    });
    sl.querySelectorAll('h1, h2, .notif b, .step b').forEach(e => {
      if (e.scrollWidth > e.clientWidth + 2) warns.push({slide: si + 1, clipped: e.textContent.slice(0, 24)});
    });
    sl.querySelectorAll('.sticker, .btn').forEach(e => {
      if (e.scrollHeight > e.clientHeight + 2 || e.scrollWidth > e.clientWidth + 2) warns.push({slide: si + 1, clipped: e.textContent.slice(0, 24)});
    });
  });
  return warns;
}"""


def main(spec_path, out_dir):
    spec_path = Path(spec_path).resolve(); out = Path(out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    brand = {"name": "", "color": "#5B3DF5", "accent": "#D4FF3A", **spec.get("brand", {})}
    lang = spec.get("lang") or ("ko" if re.search(r"[가-힣]", json.dumps(spec["slides"], ensure_ascii=False)) else "en")
    tk = tokens(brand["color"], brand["accent"])
    root = ":root{" + ";".join(f"--{k}:{v}" for k, v in tk.items()) + "}"
    ctx = {"brand": brand, "n": len(spec["slides"]), "lang": lang, "base": spec_path.parent}
    slides = []
    for i, d in enumerate(spec["slides"]):
        t = d.get("type")
        if t not in BUILDERS:
            raise ValueError(f"slide {i + 1}: unknown type '{t}'")
        slides.append(BUILDERS[t](d, ctx, i))
    page = f'''<html lang="{lang}"><head><meta charset="utf-8"><link rel="stylesheet" href="{(ASSETS / "template.css").as_uri()}">
<style>{root}</style></head><body>{"".join(slides)}</body></html>'''
    html_path = out / "_deck.html"; html_path.write_text(page, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 2400, "height": 1500})
        pg.goto(html_path.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        warns = pg.evaluate(FIT_JS)
        files = []
        for i, el in enumerate(pg.query_selector_all(".slide")):
            f = out / f"{i + 1:02d}.png"; el.screenshot(path=str(f)); files.append(f)
        b.close()

    from PIL import Image
    g = 30; n = len(files); cols = min(n, 5); rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W + (cols + 1) * g, rows * H + (rows + 1) * g), "#E5E5E5")
    for i, f in enumerate(files):
        sheet.paste(Image.open(f), (g + (i % cols) * (W + g), g + (i // cols) * (H + g)))
    sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(out / "preview.png")

    cap = spec.get("caption", "").strip()
    tags = " ".join("#" + t.lstrip("#") for t in spec.get("hashtags", []))
    (out / "caption.txt").write_text((cap + ("\n\n" + tags if tags else "")).strip() + "\n", encoding="utf-8")
    html_path.unlink()

    print(f"Rendered {n} slides -> {out}")
    for w in warns:
        if w.get("overflow"):
            print(f"  [overflow] slide {w['slide']}: text does not fit even at minimum size. Cut the copy.")
        elif w.get("clipped"):
            print(f"  [clipped] slide {w['slide']}: '{w['clipped']}' is too wide for its box. Shorten it or add a line break.")
        else:
            print(f"  [shrunk] slide {w['slide']}: text scaled to {w['shrink']}%." + (" Consider cutting copy." if w["shrink"] < 85 else ""))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python3 render.py spec.json out_dir")
    main(*sys.argv[1:])
