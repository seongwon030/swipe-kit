# Spec format and slide types

```json
{
  "brand": {"name": "Orbit", "handle": "@orbit.money", "color": "#5B3DF5", "accent": "#D4FF3A"},
  "lang": "en",
  "slides": [ { "type": "...", ... } ],
  "caption": "Instagram caption",
  "hashtags": ["tag1", "tag2"]
}
```

**brand.color** fills the cover and CTA. Any color works: text on it switches between white and near-black automatically, and the light slide background and badge tint are derived from it. **brand.accent** should contrast strongly with brand (lime on violet, pink on tomato, neon on black); it fills stickers, highlights, callouts and the `point` slide. **brand.name** is the wordmark (top-left on every slide) and gets highlighted in the `problem` answer. **brand.handle** sits bottom-left; omit it to leave that corner empty. `lang` is optional (auto-detected).

In every text field `\n` is a line break and `*word*` is emphasis. Limits below are characters per line, "aim / max" — beyond max the renderer shrinks text or warns. Korean runs about 60% of the English character count for the same width.

---

### cover — brand surface
```json
{"type": "cover", "kicker": "Introducing Orbit", "title": "Know where\nyour money\n*actually* goes.", "subtitle": "Every account, every subscription,\none calm dashboard.", "sticker": "Free for 30 days"}
```
- `title`: 2–4 lines, 12 / 14 chars per line (KO 6 / 8). Bottom-anchored, so short titles are fine.
- `kicker` (optional): outlined pill above, 24 chars, rendered uppercase.
- `subtitle` (optional): 1–2 lines, 38 chars each.
- `sticker` (optional): scalloped badge, top-right. Max ~16 chars, the offer or hook ("Free for 30 days", "New", "8 weeks"). Only real offers.

### problem — dark surface
```json
{"type": "problem", "title": "Sound\n*familiar?*",
 "notes": [{"label": "Netflix renewed", "sub": "$15.49 charged to Visa", "time": "now"}],
 "answer": "Orbit catches it before your bank does."}
```
- `title`: 2 lines, 14 chars each.
- `notes`: 2–3 notification cards showing today's pain as phone alerts. `label` 22 chars, `sub` 32 chars, `time` (optional) like "now", "2h", "7:02".
- `answer`: 1–2 lines, 40 chars total. The brand name's first mention is highlighted.

### feature — light surface + phone
```json
{"type": "feature", "title": "All your\nsubscriptions,\n*one list.*", "subtitle": "Spot the ones you forgot about.", "callout": "Cancel in one tap",
 "screen": {"search": "Search subscriptions", "chips": ["Active", "Trials"],
            "items": [{"name": "Netflix", "meta": "Renews Nov 14", "badge": "$15.49", "color": "#FF7A59"}]}}
```
- `title`: 2–3 lines, 14 chars each. `subtitle`: one line, 40 chars.
- `callout` (optional): accent tag with an arrow pointing at the phone, one line, 18 chars.
- Prefer a real screenshot: `"screenshot": "path.png"` (relative to the spec file) replaces `screen`. Portrait captures work best; it is cropped from the top.
- Mockup: 3–5 `items`, 2–4 `chips` (first is selected). Use names the real product would show.

### steps — light surface, numbered editorial list
```json
{"type": "steps", "title": "Set up in\n*two minutes.*",
 "steps": [{"title": "Connect your accounts", "desc": "Bank-level encryption, read-only access"}]}
```
- Only for actual sequences (it prints 01, 02, 03). Unordered features belong in `feature` or `point`.
- 2–4 steps. `title` 26 chars, `desc` 44 chars.

### point — accent surface, statement
```json
{"type": "point", "title": "Budgeting that\ndoesn't feel\nlike homework.", "body": "No spreadsheets, no categories to babysit."}
```
- A belief, principle or differentiator, set like a pull quote. `title` 2–3 lines, 16 chars each. `body` up to 100 chars.

### cta — brand surface
```json
{"type": "cta", "title": "Take back\nyour *month.*", "subtitle": "Try Orbit free for 30 days.", "button": "Link in bio →", "sticker": "Free shipping"}
```
- `title`: 2–3 lines, 12 chars each, ending on the action.
- `button`: default "Link in bio →" (KO "프로필 링크에서 →"). 22 chars max.
- `subtitle`, `sticker` optional (sticker sits bottom-right; skip it if the cover already used the same offer).
