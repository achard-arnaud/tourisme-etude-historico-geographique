#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

HILS = [
    'HIL-01_institutions-chronology',
    'HIL-02_geography-environment',
    'HIL-03_economy-infrastructure',
    'HIL-04_society-demography',
    'HIL-05_religion-culture-legitimacy',
    'HIL-06_security-coercion',
    'HIL-07_regional-global-system',
    'HIL-08_historiography-bias',
]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-') or 'arc'


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument('--id', required=True)
    parser.add_argument('--title', required=True)
    args = parser.parse_args()

    project = Path(args.project)
    arc_name = f"{args.id}_{slugify(args.title)}"
    arc = project / '01_arcs' / arc_name
    (arc / 'claims').mkdir(parents=True, exist_ok=True)
    (arc / 'evidence').mkdir(parents=True, exist_ok=True)
    for hil in HILS:
        for zoom in range(5):
            (arc / 'hil' / hil / f'Z{zoom}').mkdir(parents=True, exist_ok=True)

    (project / '07_drifts').mkdir(parents=True, exist_ok=True)
    (arc / 'ARC.md').write_text(
        f"# {args.id} — {args.title}\n\n"
        "## Entry rupture\n\n"
        "## Causal question\n\n"
        "## TL;DR\n\n"
        "## Drivers / amplifiers / consequences / non-causes\n\n"
        "## What changes the optimum?\n\n"
        "## Exit rupture / bridge forward\n",
        encoding='utf-8',
    )
    (project / '07_drifts' / f'{arc_name}.md').write_text(
        f'# Drift audit — {args.id}\n', encoding='utf-8'
    )
    print(arc)


if __name__ == '__main__':
    main()
