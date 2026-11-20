# Image-generation tool adapters

The Skill is tool-agnostic at the instruction level. It requires an actual image-generation capability.

## ChatGPT

Use the available ImageGen capability to generate the background. If the generated image is available as a file and Python execution is available, run `scripts/render_poster.py` to add exact text.

## Codex / Claude Code / Pi / OpenCode

Use the image-generation tool or provider configured in that agent environment. The tool must return an image file that can be passed to the local typesetting script for the preferred workflow.

If the agent has no image-generation tool or configured image API, do not pretend to have generated an image. Explain that an image-generation capability must be connected. Do not silently substitute an SVG, ASCII mockup, or prompt-only response.

## Local rendering dependency

The exact-typesetting path requires Python 3, Pillow, and a CJK font installed on the machine. See `requirements.txt` and `scripts/render_poster.py`.
