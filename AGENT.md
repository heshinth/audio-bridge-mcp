# GENERAL PRINCIPLES

- Keep components modular and concerns clearly separated.
- Prefer established, well-maintained libraries when they reduce overall complexity or improve reliability. Do not reimplement common functionality without a clear reason.
- Lean on the dependencies already in the project before writing your own implementation or adding packages. Do not assume a library lacks a capability without checking its documentation and types.
- NEVER automatically commit code. Always ask for confirmation before committing, and ensure that the commit message follows the Conventional Commits specification.

# Working Style

- Push back on genuinely bad ideas, with reasoning. Point out bugs, misleading names,
  and better approaches when you see them. Direct but collaborative.
- If requirements are ambiguous or a design decision could reasonably go multiple ways,
  ask rather than guess. A quick question is cheaper than reworking a wrong assumption.
- **If a prompt looks damaged or wrong, STOP and say so** — truncated mid-sentence,
  duplicated blocks, garbled copy/paste, references to context that doesn't exist, or
  instructions that contradict prior decisions without acknowledging they do. Do not
  execute a best-guess reconstruction. A mangled prompt executed faithfully is worse
  than a delay.

# Codebase

- Keep all files around 300 lines of code as much as possible (Auto added files such as Shadcn/UI components can be given an exception). If a file exceeds this limit, consider splitting it into smaller modules. — but don't shatter code into fragments either; a file holds one coherent  concern.
- Files must be modular and single purpose. Avoid mixing unrelated functionality in the same file.
- Follow the Conventional Commits specification for commit messages.
- Do NOT make assumptions. Do NOT jump to conclusions. If you are unsure about something, ask for clarification or check the documentation.
- There should be no redundancy or code duplication 
- **Naming**: clear, descriptive names that read as plain English. Abbreviations
  only when universally understood (`id`, `url`, `config`).