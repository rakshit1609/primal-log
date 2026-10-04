# primal-log

Generate a Markdown changelog from your git history, grouped by [Conventional Commit](https://www.conventionalcommits.org) type.

```bash
pip install primal-log
primal-log                         # run inside a git repo, prints to stdout
primal-log --repo ../other-repo
primal-log --output CHANGELOG.md
```

**Example**
```
## Features
- feat: login (fd9db33)
## Fixes
- fix: redirect bug (c555b9a)
## Docs
- docs: api ref (fb22476)
## Other
- chore: deps (ed066c6)
```

## Limitations (v1)
- Groups `feat`, `fix` and `docs`; everything else goes under "Other"
- The "Breaking Changes" section is not populated yet (`!` / `BREAKING CHANGE:` are not parsed)
- Whole history only: no version/tag ranges yet

MIT licensed.
