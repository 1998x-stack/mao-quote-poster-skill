# Usage examples

When the Skill is active, each of the following should trigger one poster without further design questions.

## Example 1

Input:

```text
星星之火，可以燎原。
```

Expected behavior:
- Generate one vertical crimson poster.
- Typeset the exact quotation.
- Add the `毛泽东` attribution.
- Do not add an anniversary footer.

## Example 2

Input:

```text
世上无难事，只要肯登攀。
```

Expected behavior:
- Keep the full wording and punctuation.
- Use the same visual identity.
- Generate one image only.

## Example 3: long quotation

Input:

```text
没有调查，没有发言权。
```

Expected behavior:
- Preserve every character.
- Adjust line breaks and font size for legibility.
- Never truncate the quotation.
