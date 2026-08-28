"""Dependency-free retention gates shared by reader renderers and CI tests."""

from pathlib import Path

from output_state import resolve_state_path


def _baseline_path(project: Path) -> Path | None:
    """Resolve the configured retention baseline, with legacy fallback for fixtures."""
    try:
        return resolve_state_path(project, "baseline_markdown")
    except (FileNotFoundError, ValueError):
        legacy = project / "09_output" / "report_v1_full.md"
        return legacy if legacy.exists() else None


def enforce_advanced_retention(project: Path, text: str, allow_abridged: bool = False) -> None:
    baseline = _baseline_path(project)
    if baseline is None or allow_abridged:
        return
    candidate_words = len(text.split())
    baseline_words = len(baseline.read_text(encoding="utf-8").split())
    if candidate_words < baseline_words:
        raise RuntimeError(
            "Refusing silent advanced-reader compression: candidate contains "
            f"{candidate_words} words but the configured baseline contains "
            f"{baseline_words}. Use the full reader pipeline, or explicitly pass "
            "--allow-abridged for a labelled derivative."
        )
