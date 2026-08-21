# Output Risk Profile

Skill: `us-overnight-a-stock-mapping`

## Why This Exists

Generated skills often fail in small output details: generic headings, cluttered citations, fragile screenshots, weak Markdown rendering, or missing execution assumptions. This profile predicts the most likely output mistakes before the skill is used heavily.

## Matched Risk Families

### Citation and footnote clutter
- Matched keywords: source, research, reference, 来源
- Score: `4`

### Markdown readability
- Matched keywords: md, 报告
- Score: `2`

### Code and command safety
- Matched keywords: script
- Score: `1`

## Likely Output Mistakes

- Footnote markers or dense citation notes can interrupt the reading flow.
- Evidence can be over-attached to obvious statements and under-attached to risky claims.
- Tables can render as dense grids with weak hierarchy or poor mobile readability.
- Long bullets can make the output look complete while hiding the actual decision logic.
- Commands can omit environment assumptions, working directory, or rollback notes.
- Code snippets can look runnable while missing required inputs.

## Output Constraints To Apply

- Attach citations only to claims that need evidence, not to every sentence.
- Group source notes at the end of a section when inline markers would hurt readability.
- Use tables only when comparison is the main job; otherwise prefer compact cards or grouped bullets.
- Keep table cells short and move explanations below the table.
- Name the working directory, required inputs, and expected output for each command.
- Mark destructive or external side-effect operations explicitly.

## Self-Repair Checks

- Remove decorative citations that do not support a material claim.
- Move repeated source explanations into one compact source note.
- Preview whether each table still reads well when columns are narrow.
- Convert any table with paragraph-length cells into bullets or cards.
- Scan each command for cwd, input, output, and side-effect assumptions.
- Remove speculative error handling that is not tied to a real failure mode.

## Reviewer Note

Use this report before deepening the package and again before approving example outputs.
