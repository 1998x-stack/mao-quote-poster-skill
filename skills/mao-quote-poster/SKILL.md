---
name: mao-quote-poster
description: Turn a user-provided Mao Zedong quotation into exactly one polished vertical red commemorative poster. When this skill is active, a quotation alone is sufficient input; do not ask the user to restate the visual style.
---

# Mao Quote Poster

## Purpose

Create **one finished poster image** from the Mao Zedong quotation supplied by the user. The user should only need to send the quotation. Use the default visual identity below without asking for design preferences.

## Default behavior

- Output: exactly **one image**.
- Canvas: vertical **9:16** poster.
- Visual identity: deep crimson red, fabric/flag-like folds, subtle film grain, a vertical warm spotlight, large warm ivory/yellow Chinese typography with a restrained glow.
- Main text: the user's quotation, visually dominant and centered.
- Attribution: `毛泽东`, placed below or to the lower-right of the quotation in a restrained calligraphic/signature treatment.
- Lower composition: a subtle dark-red historical silhouette or abstract profile blended into the background; it must not compete with the quotation.
- No extra slogan, date, memorial anniversary, publisher mark, brand logo, QR code, or watermark.
- Do not add `纪念毛泽东同志逝世50周年` or any other event-specific footer unless the user explicitly asks for it.

## Input contract

1. Treat the user's supplied quotation as the exact text to typeset.
2. Preserve its wording, character order, punctuation, and simplified/traditional form. Do not paraphrase, shorten, modernize, or silently correct it.
3. Trim only accidental whitespace at the beginning or end. Preserve intentional line breaks.
4. If the user sends only a quotation, proceed immediately. Do not ask for a style, aspect ratio, color, or layout.
5. If no quotation text is present, ask one concise question requesting the quotation.
6. Do not perform external attribution research unless the user explicitly asks to verify the quotation. The image is based on the user's supplied attribution/context.

## Production workflow

### Preferred workflow: generated background + exact typesetting

1. Use the available image-generation tool to create a **background only**. The background must contain no text or lettering.
2. If the runtime can save the generated background to a local file and run Python, use `scripts/render_poster.py` to typeset the exact quotation and attribution. This is the preferred path because it avoids image-model Chinese-character errors.
3. If local image post-processing is unavailable, ask the image-generation tool to render the quotation exactly as supplied. Inspect the result. If a character is visibly wrong or missing, regenerate once with larger, simpler typography and fewer line breaks.
4. Return the single finished image. Do not return only a prompt or design description.

### Background-generation prompt

Adapt the following prompt only to accommodate the quotation's eventual text area. Do not ask the image model to draw any words:

> Create a vertical 9:16 Chinese historical commemorative poster BACKGROUND ONLY, with absolutely no text, no letters, no numbers, no calligraphy, no logos, no symbols, and no watermark. Deep saturated crimson and vermilion red fabric or flag-like folds sweep vertically along the sides. A warm, slightly brighter vertical beam of light runs through the central area, leaving a calm, uncluttered central field for later typography. Add subtle vintage film grain, tactile paper/fabric texture, restrained red-on-red tonal depth, and a solemn, powerful atmosphere. In the lower third, blend in a subtle dark-maroon abstract historical side-profile silhouette, low contrast and secondary to the future text. Keep the central text-safe area visually calm and high-contrast. No recognizable organization insignia and no extra decorative lettering. High-quality editorial poster design.

### Exact typesetting

When `scripts/render_poster.py` is available:

```bash
python3 scripts/render_poster.py \
  --background /path/to/background.png \
  --quote "用户提供的完整名言" \
  --output /path/to/output.png
```

- The script uses a locally installed CJK font; it never rewrites the quotation.
- If the font cannot be found, stop and report the missing font rather than generating boxes or substituting Latin glyphs.
- If Pillow is missing, install the package in `requirements.txt` in the active project environment, or use the image-generation-only fallback.

## Composition rules

- Keep the quotation as the visual focus. Use balanced line breaks; do not break a Chinese punctuation mark onto the beginning of a new line.
- Short quotations: use two or three bold lines with generous negative space.
- Medium quotations: use three to five lines and reduce the type size only as much as needed.
- Long quotations: preserve every character; use smaller but still legible type and a taller text block. Never truncate or replace text with ellipses.
- Use warm pale-gold/ivory text, a soft outer glow, and a subtle dark shadow for legibility.
- Keep attribution visually secondary and separated from the quote.
- Keep the lower silhouette understated. Never let it overlap the quotation.
- Do not invent a source title, speech date, publication, event, or historical claim.

## Quality gate

Before returning the image, verify:

- There is exactly one image.
- The full quotation appears, in order, with no missing, duplicated, or substituted characters.
- Punctuation and line breaks are acceptable.
- `毛泽东` attribution is present unless the user explicitly requests no attribution.
- The image is vertical 9:16 or as close as the available image tool permits.
- No unintended words, dates, logos, watermarks, or random pseudo-Chinese glyphs appear.

If the image-generation tool cannot reliably render Chinese text, prefer the generated-background + local-typesetting workflow. Never claim the text is exact if it has not been checked.

## User-facing response

After successful generation, keep the response brief. The image itself is the deliverable. Do not repeat the quotation in a long explanation or offer multiple versions unless requested.
