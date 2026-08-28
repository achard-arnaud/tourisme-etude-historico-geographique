# Run33 crystal — functional reader baseline

This directory freezes the exact Markdown source of the Run33 readers that were functionally validated before any later side-story or technical refactor pass.

The Markdown is stored as gzip-compressed base64 shards because the connected repository writer accepts UTF-8 text but not local binary uploads. The DOCX/PDF binaries remain externally delivered artifacts; their exact SHA-256 hashes are recorded in `docs/RUN33_CRYSTAL_MANIFEST.json`.

## Reconstruct the exact Markdown

```bash
cat docs/run33_crystal/pre_1948/part-*.b64 | base64 -d | gzip -d > Sri_Lanka_pre_1948_RUN33_storytelling_final.md
cat docs/run33_crystal/post_1948/part-*.b64 | base64 -d | gzip -d > Sri_Lanka_1948_2026_RUN33_storytelling_final.md
sha256sum Sri_Lanka_*_RUN33_storytelling_final.md
```

Expected hashes:

- pre-1948: `0d168868600af10aae84f95cdaf639ca608c36b1bfef50f6d9d511eba8a170ed`
- 1948–2026: `21f83c12aa83d12b4a783ce835de226665e189dd386c8ca540d997fc33c1c0ae`

## Editorial status

Run33 is a **functional baseline**, not a pipeline refactor. It preserves the Run32 reader scaffold while removing production/meta prose and restoring richer narrative material from fragments and source lineage. Claims remain backstage. A later functional pass may add or reposition side stories, but must use this crystal as its iterative baseline and must not silently rewrite it as if it were generated from scratch.
