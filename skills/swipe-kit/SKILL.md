---
name: swipe-kit
description: Turn a product, app, project or event into an Instagram carousel (card news, 1080×1350, 4:5) using a fixed marketing design system, exported as PNGs plus a caption. Use whenever someone wants an Instagram post, carousel, card news (카드뉴스), promo slides or social graphics to introduce or promote something, even if they never say "carousel". Writes copy in the language of the request (English or Korean). 서비스·앱·프로젝트 홍보용 인스타 카드뉴스, 캐러셀, 피드 이미지를 만들 때 사용한다.
---

# swipe-kit

Builds marketing carousels in the style of modern product brands on Instagram: big tight display type with a serif-italic accent word, color-blocked slides, a scalloped sticker, notification cards, a device mockup, and the usual carousel chrome (wordmark, `01 / 06` counter, handle, `Swipe →`).

The design is fixed in `assets/template.css`. Your job is **planning the deck, writing the copy and filling a JSON spec**. Do not redesign per request: a consistent feed sells better than one flashy slide, and the template has already solved spacing and hierarchy.

## Workflow

### 1. Gather material
Needed: product name, one-line description, audience, a concrete pain the audience has today, 2–3 key features, where the call to action points (link in bio, DM, a URL). Nice to have: brand color, Instagram handle, app screenshots.

If it is already in the conversation or attached, do not ask again. Ask only for things you must not invent (the pain, the features, any offer like "free for 30 days"). Without a brand color, use the default (violet `#5B3DF5` + lime `#D4FF3A`) and say so.

### 2. Plan the deck
Default flow, 5–7 slides:

1. `cover` — the hook
2. `problem` — "sound familiar?" moment, answered by the product
3. `feature` ×1–2 — what it does, shown on a phone
4. `steps` or `point` — `steps` only for real sequences; `point` for a belief, principle or differentiator
5. `cta` — one clear action

Surfaces alternate automatically by type (brand → dark → light → light → accent → brand). Avoid three light slides in a row; drop in a `point` or `problem` to break it up. Never exceed 10 slides.

### 3. Write the copy
Read `references/slide-types.md` for every field and its length limit. Principles:

- **One idea per slide.** Two ideas means two slides.
- **Cut 30%** from your first draft. Carousels fail on word count far more than on design.
- **Benefits, not features.** "See every renewal before it hits your card", not "Subscription tracking".
- **Break headlines by hand** with `\n` at natural phrase boundaries.
- **Emphasis:** wrap one word or short phrase per headline in `*asterisks*`. In English it becomes serif italic; in Korean, a marker underline. Use it on the word that carries the feeling, at most once per headline, not on every slide.
- **English:** sentence case, contractions welcome, short words. Avoid "revolutionary", "seamless", "unlock", "elevate", "game-changer", "next-level".
- **Korean:** 해요체, write from the user's side, never strand a single particle on its own line.
- **Never:** emoji, exclamation-mark stacks, invented numbers (user counts, ratings, savings) the user did not give you.
- Caption: 3–5 lines — relatable hook, what the product does, the action. 4–8 hashtags.

Set `"lang"` in the spec only if auto-detection would be wrong (it detects Hangul in the slide text).

### 4. Render

```bash
python3 <skill>/scripts/render.py spec.json out_dir
```

Outputs `01.png`… (1080×1350 each), `preview.png` (contact sheet) and `caption.txt`. Needs `playwright` (chromium) and `Pillow`; if missing: `pip install playwright pillow --break-system-packages && playwright install chromium`. Fonts are bundled, so no network is required.

`assets/example.json` is a complete deck; copying it is the fastest start.

### 5. Review and fix
Open `preview.png` and look at it. Then check the renderer warnings:

- `[shrunk] … below 85%`, `[overflow]`, `[clipped]` → cut the copy and render again. A shrunk headline breaks the type scale across the deck.
- Awkward headline breaks or a line with one short word → move the `\n`.
- Uneven copy length between slides → even it out.

Repeat until clean, then deliver.

### 6. Deliver
Zip the PNGs, and put the zip, `preview.png` and `caption.txt` in the output folder. Paste the full caption in your reply so it can be copied directly.

## Changing the design

Solve requests through the spec first (copy, slide order, brand color, accent, screenshots, sticker text). Edit `assets/template.css` or `render.py` only when the user explicitly wants a template change. Even then:

- Colors come from `brand`, `accent` and the values derived from them. No new hues.
- Accent appears once or twice per slide (sticker, highlight, callout). More and it stops meaning anything.
- Type stays Bricolage Grotesque (display) + Instrument Serif Italic (accent) + Inter (text), with Pretendard as the Hangul fallback.
- No gradients, glassmorphism, drop-shadow stacks or emoji decoration.
