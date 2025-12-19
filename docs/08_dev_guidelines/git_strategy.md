# Git Strategy

SFS uses a structured Git workflow.

---

## Branching Model

- main: stable, production-ready
- develop: integration branch
- feature/*: feature development
- fix/*: bug fixes
- docs/*: documentation updates

---

## Commit Rules

- One logical change per commit
- Descriptive commit messages

Format:
<type>: <short description>

[type] ∈ {feat, fix, refactor, docs, test, chore}


---

## Pull Requests

A PR must:
- Reference an issue or requirement
- Pass all tests
- Pass architecture checks
- Update documentation if behavior changes

---

## Forbidden

- Direct commits to main
- Mixing refactor and feature in one commit
- Large unreviewable PRs
