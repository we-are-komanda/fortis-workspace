"""Validate this spec bundle and synthetic arithmetic, not the Fortis application."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json
import re

root = Path(__file__).resolve().parent
index = json.loads((root / 'task-index.json').read_text(encoding='utf-8'))
tasks = index['tasks']
ids = {t['id'] for t in tasks}
assert len(tasks) == 15 and len(ids) == 15
required = ['README.md','00_SHARED_CONTRACTS.md','SOURCES.md','ACCEPTANCE_MATRIX.md',
            'CODER_PROMPT.md','RELEASE_GATE.md','contracts/release-contracts.ts','fixtures/finance-v1.json']
for name in required:
    assert (root / name).is_file(), name
for t in tasks:
    assert (root / t['file']).is_file(), t['file']
    assert set(t['deps']).issubset(ids), t['id']
    content = (root / t['file']).read_text(encoding='utf-8')
    for section in ['## 1.', '## 2.', '## 3.', '## 4.', '## 5.', '## 6.', '## 7.', '## 8.']:
        assert section in content, (t['id'], section)
    for dep in t['deps']:
        assert dep in content.split('**Цель:**')[0], (t['id'], dep)

pending = {t['id']: set(t['deps']) for t in tasks}
visited = set()
waves = []
while pending:
    ready = sorted(k for k, v in pending.items() if v <= visited)
    assert ready, ('cyclic_dependencies', pending)
    waves.append(ready)
    for k in ready:
        visited.add(k)
        del pending[k]

f = json.loads((root / 'fixtures/finance-v1.json').read_text(encoding='utf-8'))
prices = {a['id']: int(a['unitPriceMinor']) for a in f['assets']}
for name in ['variantA','variantB']:
    v = f[name]
    groups = {}
    for obj in v['objects']:
        unit = int(obj.get('customPriceMinor', prices[obj['assetId']]))
        groups[obj['layerId']] = groups.get(obj['layerId'], 0) + unit * obj['quantity']
    assert sum(groups.values()) == int(v['expectedTotalMinor'])
    assert groups == {k:int(x) for k,x in v['expectedByLayer'].items()}
    if v['budget']['mode'] == 'limited':
        assert int(v['budget']['limitMinor']) - sum(groups.values()) == int(v['budget']['expectedRemainingMinor'])
A, B = [int(f[n]['expectedTotalMinor']) for n in ['variantA','variantB']]
assert B - A == int(f['comparison']['expectedDifferenceMinor'])
pct = (Decimal(B-A) / Decimal(A) * 100).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
assert str(pct) == f['comparison']['expectedDifferencePercentRounded2']
c = f['compound']
unit = sum(int(x['unitPriceMinor']) * x['quantity'] for x in c['components'])
assert unit == int(c['expectedUnitMinor']) and unit * c['quantity'] == int(c['expectedTotalMinor'])
for b in f['boundaryTests']:
    if 'allowed' in b:
        assert (int(b['baseMinor']) + int(b['addMinor']) <= int(b['limitMinor'])) == b['allowed']
    if b['id'] == 'ZERO-OVERRIDE':
        assert int(b['overrideMinor']) * b['quantity'] == int(b['expectedMinor'])
    if b['id'] == 'UNKNOWN-PRICE':
        assert b['priceMinor'] is None and b['expectedTotalMinor'] is None and b['isComplete'] is False
    if 'priceMlnText' in b:
        value = (Decimal(b['priceMlnText']) * 100_000_000).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        assert str(value) == b['expectedUnitMinor']

acceptance_ids = []
for t in tasks:
    text = (root / t['file']).read_text(encoding='utf-8')
    acceptance_ids += re.findall(r'^\| ([A-Z]+-\d+) \|', text, re.M)
assert len(acceptance_ids) == len(set(acceptance_ids)), 'duplicate acceptance IDs'
for md in root.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    assert text.count('```') % 2 == 0, ('unbalanced fences', md.name)
    for url in re.findall(r'\]\(([^)]+)\)', text):
        if '://' not in url and not url.startswith('#'):
            assert (md.parent / url.split('#')[0]).exists(), ('broken local link', md.name, url)

print('PASS: 15 specifications; complete sections and valid dependency DAG.')
print(f'PASS: {len(acceptance_ids)} unique acceptance scenarios.')
print('PASS: financial fixture, grouped totals, override, compound, delta, budget boundary, rounding.')
print('PASS: local links and Markdown code fences.')
print('Topological waves: ' + ' -> '.join('/'.join(w) for w in waves))
print('NOT EXECUTED: Fortis build, unit, integration, browser E2E, production checks.')
