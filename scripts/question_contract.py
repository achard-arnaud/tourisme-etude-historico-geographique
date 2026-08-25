#!/usr/bin/env python3
import json
from pathlib import Path

VALID_KINDS = {'causal','metric','epistemic','comparative','counterfactual','method'}
VALID_STATUSES = {'open','answered','refuted','bounded','abandoned','pending_external'}
REQUIRED = {'id','question','kind','status','discriminating_test','falsifier','priority'}


def _load_register(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, list):
        raise ValueError('expected JSON list')
    return data


def validate_question_registers(root):
    root = Path(root)
    errors = []
    warnings = []
    records = []
    seen = set()
    register_paths = sorted((root / '08_questions').glob('question_register*.json')) if (root / '08_questions').exists() else []

    for path in register_paths:
        try:
            items = _load_register(path)
        except Exception as exc:
            errors.append(f'invalid question register: {path}: {exc}')
            continue
        for index, q in enumerate(items, 1):
            where = f'{path.name}#{index}'
            if not isinstance(q, dict):
                errors.append(f'question record is not an object: {where}')
                continue
            records.append(q)
            missing = [field for field in sorted(REQUIRED) if q.get(field) in (None, '', [])]
            for field in missing:
                errors.append(f'question missing {field}: {q.get("id") or where}')
            qid = q.get('id')
            if qid:
                if qid in seen:
                    errors.append(f'duplicate question id: {qid}')
                seen.add(qid)
            if q.get('kind') not in VALID_KINDS:
                errors.append(f'invalid question kind: {qid or where}')
            if q.get('status') not in VALID_STATUSES:
                errors.append(f'invalid question status: {qid or where}')
            if not isinstance(q.get('priority'), int) or q.get('priority', 0) < 1:
                errors.append(f'invalid question priority: {qid or where}')
            if isinstance(q.get('question'), str) and not q['question'].strip().endswith('?'):
                warnings.append(f'question is not interrogative: {qid or where}')
            gate = q.get('gate')
            if gate and gate == qid:
                errors.append(f'question self-gate: {qid}')
            for child in q.get('is_gate_for') or []:
                if child == qid:
                    errors.append(f'question self gate target: {qid}')

    ids = {q.get('id') for q in records if q.get('id')}
    for q in records:
        qid = q.get('id')
        gate = q.get('gate')
        if gate and gate not in ids:
            errors.append(f'unknown question gate {gate} referenced by {qid}')
        for child in q.get('is_gate_for') or []:
            if child not in ids:
                errors.append(f'unknown gated question {child} referenced by {qid}')

    return errors, warnings, len(records)


def main():
    import sys
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    errors, warnings, count = validate_question_registers(root)
    for msg in errors:
        print('ERROR:', msg, file=sys.stderr)
    for msg in warnings:
        print('WARN:', msg, file=sys.stderr)
    if errors:
        return 1
    print(f'QUESTION QA OK: {count} structured records, {len(warnings)} warnings')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
