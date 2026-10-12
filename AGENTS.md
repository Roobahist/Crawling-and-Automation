# Repository maintenance notes

- This repository combines educational legacy exercises with a maintained `src/` Python package. Preserve archived datasets, images and the large notebook unless there is explicit authorization to remove them.
- Python >=3.11. Install with `python -m pip install -e '.[dev]'` and verify with `python -m unittest discover -s tests -v` and the commands in README.md.
- Keep all network calls in adapters/entry points. Parsing and price calculations should remain side-effect free; use injected HTTP sessions and explicit validated settings.
- Never commit API tokens or browser cookies. Do not log full URLs that contain tokens. CI must never require real credentials.
- Do not silently invent brand translations, modify scraped prices, discard malformed source rows or assume legacy site selectors still work.
- Make changes to `legacy/` only with clear compatibility and data-preservation justification. Prefer extending tested `src/` functionality over patching historical one-off scripts.
- Test new behavior with fixtures and fake sessions. External APIs can change; distinguish verified compatibility from historical assumptions.
- Keep docs and any architecture diagrams aligned with the implemented package. Do not add Docker or deployments without a real use case.
