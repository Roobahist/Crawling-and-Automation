# Historical code migration

| Old path | Preserved path | Maintained alternative |
| --- | --- | --- |
| `P1/` | `legacy/automotive/` | `crawling_automation.automotive` (price utilities and Bama parser) |
| `P2/` | `legacy/instagram/` | `crawling_automation.social.instagram` and `crawl-auto instagram-*` |
| `P3/` | `legacy/notebooks/` | BourseView financial-data notebook retained with cookie values redacted; not converted to maintained scripts. |

Most historical source and collected data are preserved in the current tree. The P3 notebook is a special case: six embedded BourseView authentication cookie literals were redacted, while its 90 cells and 37 saved outputs remain intact. The unredacted version persists in the original public Git commit; remove or rotate compromised sessions before publication. Three Windows ChromeDriver executables and four compiled Python cache files were deliberately removed from the maintained tree. They remain available in the original 2022 commit, because this modernization did not rewrite history.

The new package is not a drop-in replacement for every original Selenium script. The old scripts ran browser automation and had implicit side effects, hardcoded site selections and no tests. The modernized Bama parser specifically targets the old listing structure and must be adapted and verified before live use.

The new Instagram adapter requires token and API version to be supplied at runtime, explicitly supports page retrieval, and avoids using deprecated legacy metrics by default. The original `#$#` delimited exports are archived; new output uses conventional CSV quoting and delimiters.
