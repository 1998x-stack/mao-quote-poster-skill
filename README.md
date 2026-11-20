# Mao Quote Poster Skill

A reusable Agent Skill that turns one user-provided Mao Zedong quotation into **one vertical 9:16 red commemorative poster**.

The default style follows the supplied visual reference: crimson fabric-like folds, warm central light, glowing ivory/yellow Chinese typography, a subtle lower silhouette, and a small `毛泽东` attribution.

## The intended interaction

Once installed and activated, the user only needs to send:

```text
星星之火，可以燎原。
```

The agent generates one finished image. It does not ask the user to repeat the style instructions.

## Features

- Exact quote preservation: no paraphrasing, shortening, or silent correction.
- One image per request, vertical 9:16 by default.
- Stable visual identity across different quotations.
- Background generation separated from text typesetting.
- Local Pillow renderer for precise Chinese typography.
- No event-specific footer, invented date, logo, or watermark.
- Skill source is agent-agnostic, with an installer for Codex, Claude Code, Pi, OpenCode, and `.agents` projects.

## Directory structure

```text
mao-quote-poster-skill/
├── README.md
├── skills/
│   └── mao-quote-poster/
│       ├── SKILL.md
│       ├── references/
│       │   ├── design-system.md
│       │   └── tool-adapters.md
│       ├── scripts/
│       │   └── render_poster.py
│       ├── examples/
│       │   └── usage.md
│       ├── tests/
│       │   └── test_render_poster.py
│       └── requirements.txt
└── scripts/
    └── install_skill.py
```

## Install

Install to all supported project-local directories:

```bash
python3 scripts/install_skill.py \
  --project /path/to/your/project \
  --targets agents,codex,claude,pi,opencode
```

Install to only Pi and Codex:

```bash
python3 scripts/install_skill.py \
  --project /path/to/your/project \
  --targets pi,codex
```

To replace existing copies, add `--force`.

## Exact Chinese typesetting

The preferred production workflow is:

1. Generate a red poster background with an image-generation tool, without any text.
2. Overlay the quote and attribution with the included Pillow script.
3. Inspect the final image and return one image.

Install the renderer dependency:

```bash
python3 -m pip install -r skills/mao-quote-poster/requirements.txt
```

Render:

```bash
python3 skills/mao-quote-poster/scripts/render_poster.py \
  --background background.png \
  --quote "星星之火，可以燎原。" \
  --output mao-quote-poster.png
```

The machine must have a CJK font installed. The script searches common macOS, Linux, and Windows font locations. If necessary, pass an explicit font:

```bash
python3 skills/mao-quote-poster/scripts/render_poster.py \
  --background background.png \
  --quote "星星之火，可以燎原。" \
  --output mao-quote-poster.png \
  --font "/path/to/NotoSansCJK-Regular.ttc"
```

## Important runtime requirement

The Skill needs an actual image-generation capability in the agent environment. The included renderer handles exact text composition; it does not generate the background by itself. If the agent has no image-generation tool or configured image API, it must say so rather than pretending an image was created.

## Quality principles

- The user's quote is the source of truth for the text.
- The image must not contain additional slogans or invented historical details.
- The default footer is intentionally empty; no anniversary date or publisher logo is added.
- Do not claim exact text rendering until the final image has been inspected.
