# Security and data handling

- The maintained package receives the Meta access token from `META_ACCESS_TOKEN` at runtime. It is not stored in source code or example configuration. Keep `.env` out of Git and do not print tokens or token-bearing request URLs.
- Instagram sample CSVs include public post identifiers, captions, engagement metrics and historical media URLs. Avoid assuming these are anonymized or safe for new publication. Confirm ownership and redistribution rights before reuse.
- The large historical notebook and archived workbooks were preserved without content changes. The notebook could not be fully inspected through the available file interface; do not interpret this review as a comprehensive secrets or personal-data audit of those artifacts.
- The original repository contains only one visible commit from November 2022. Moving or deleting files on the current branch does not erase them from the public Git history. If a real credential is discovered in history, revoke it immediately and plan a coordinated history rewrite separately.
- No live website calls are made during tests. Use only accounts and sources you are authorized to access, follow terms and rate limits, and use a limited-scope token where practical.
- The bundled historical drivers were removed from the current tree rather than executed. Historical downloaded binaries are not trusted application dependencies.
