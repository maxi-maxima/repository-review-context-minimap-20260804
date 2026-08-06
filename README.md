# repository-review-context-minimap-20260804

Large pull requests overwhelm reviewers and AI agents with too much context; teams need a tiny map of touched areas, risky files, and likely owners before opening a full review.

## Why now

Local-first code intelligence and context reduction are trending because coding agents need fewer tokens and humans need faster review entry points.

## Install and run

No third-party dependencies are required. Use Python 3.10+.

```bash
python src/repository_review_context_minimap.py --help
python src/repository_review_context_minimap.py examples/changed-files.txt
git diff --name-only main...HEAD > changed-files.txt
git diff main...HEAD > changes.diff && python src/repository_review_context_minimap.py changes.diff --diff
python tests/test_cli.py
```

## Example

Sample input lives in `examples/`. Example command:

```bash
python src/repository_review_context_minimap.py examples/changed-files.txt
```

## Roadmap

- CODEOWNERS integration
- Token budget estimates per area

## License

MIT
