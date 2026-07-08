---
description: Bump version, tag, and push a new release
---

Read `taskwatch/__init__.py` to get the current version string (e.g. `"0.2.9"`).
Parse it as `major.minor.patch`. Compute the next version:

1. Increment patch by 1.
2. If patch reaches 10: set patch to 0 and increment minor by 1.
3. If minor reaches 10: set minor to 0 and increment major by 1.

Update the version in both `taskwatch/__init__.py` and `pyproject.toml`.

Then execute:

```
git add -A
git commit -m "Bump version to <new-version>"
git tag v<new-version>
git push origin master
git push origin v<new-version>
```

Print the old and new versions at the end.
