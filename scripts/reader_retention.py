"""Dependency-free retention gates shared by reader renderers and CI tests."""

from pathlib import Path


def enforce_advanced_retention(project: Path, text: str, allow_abridged: bool = False) -> None:
    baseline = project / "09_output" / "report_v1_full.md"
    if not baseline.exists() or allow_abridged:
        return
    candidate_words = len(text.split())
    baseline_words = len(baseline.read_text(encoding="utf-8").split())
    if candidate_words < baseline_words:
        raise RuntimeError(
            "Refusing silent advanced-reader compression: report.md contains "
            f"{candidate_words} words but the complete V1 baseline contains "
            f"{baseline_words}. Use render_full_reader_v3.py, or explicitly pass "
            "--allow-abridged for a labelled derivative."
        )
