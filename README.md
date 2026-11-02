# BO Wenqu — Back-to-School Campaign Landing Page

Conversion landing page for BO Wenqu's back-to-school stationery campaign.
Single self-contained `index.html` — no build step, no dependencies, no external assets.

## Open it

Just open `index.html` in a browser. If the `.srt`-style fetches or module scripts ever get added,
serve it instead:

```bash
python3 -m http.server 8000
```

## What's in the repo

| File | What it is |
|---|---|
| `index.html` | The landing page — 42 KB, single file, zero external requests |
| `BOWenqu_BackToSchool_CopyPack.md` | Full multi-channel copy pack this page was built from |

## Page structure

Ordered as a conversion funnel rather than a transcription of the copy deck:

| Section | Job |
|---|---|
| Sticky nav | Anchor jumps + persistent CTA |
| Hero | Gradient headline, price card, **live countdown**, three trust badges |
| Trust bar | Certification / 100gsm paper / warranty / 48h dispatch |
| Pain-point split | "Three shops vs one box" side-by-side |
| Bundle contents | 6 cards, inline SVG icons + piece counts |
| Dual-audience split | Parent (mint) on the left, kid (pink) on the right |
| Spec table | 6 rows that remove purchase friction |
| Three offers | Early bird / bundle price / gift-with-purchase, middle card emphasised |
| FAQ | Accordion, 5 entries |
| Final CTA | Gradient block + two buttons |
| Mobile sticky bar | Price + CTA pinned to the bottom on narrow screens |

## Implementation notes

- **No product photography exists**, so all 14 icons are hand-written inline SVG `<symbol>`s
  (notebook, pen, eraser, ruler, pencil case, labels, unicorn, dinosaur…). Nothing to load,
  nothing to break, and every colour is a CSS variable. Swapping in real photography means
  replacing a handful of `<use>` nodes.
- **The countdown persists** to `localStorage`. First visit locks the deadline to 7 days out, so
  refreshing never restarts the clock — a countdown that resets every reload breaks the urgency it
  is supposed to create.
- **The dual-audience strategy is visual, not just verbal:** parent side is mint with a shield
  icon, kid side is pink with a star icon. You can tell who is being addressed at a glance.
- Responsive breakpoints at 980px and 620px. All animation is disabled under
  `prefers-reduced-motion`.

## ⚠️ Before you publish

Every price, discount, certification name and date in this page is a **placeholder default** from
section 10 of the copy pack. Replace them with real, substantiated values:

- Early-bird discount, bundle price / original price, gift-with-purchase threshold
- Certification names (currently EN71 & ASTM D-4236), paper weight (100gsm), warranty term
- Campaign end date and dispatch promise

The same list lives in a comment at the top of `index.html`.

## Working in Bolt.new

Static single file — import and open. Good next prompts:

- "Build a second Hero variant that uses a checklist visual instead of the price card"
- "Add real image slots with captions and swap instructions"
- "Move the three offers into a JSON config so the ops team can edit numbers without touching HTML"
- "Add a variant switcher to A/B test both hero versions"

## Related

`BOWenqu_BackToSchool_CopyPack.md` holds the source copy for every channel — poster, Instagram
feed ×4, Stories 5-frame sequence, 30-second TikTok/Reels script, Pinterest, PDP, three-email EDM
sequence, SMS ×3, and a five-layer hashtag library.
