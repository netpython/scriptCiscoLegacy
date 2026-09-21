#!/usr/bin/env python3
"""Détermine la version majoritaire par modèle et classe les écarts logiciels."""
from __future__ import annotations
import re, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from common import devices, parallel, parser, run, write_csv, setup
log = setup('software_compliance')
args = parser('Conformité versions IOS').parse_args()

def collect(d):
    name = d.get('name', d['host'])
    data = run(d, 'show version', True)
    if isinstance(data, list) and data:
        data = data[0]
    if isinstance(data, dict):
        model = str(data.get('hardware') or data.get('platform') or 'UNKNOWN')
        version = str(data.get('version') or 'UNKNOWN')
    else:
        text = str(data)
        model = re.search('[Cc]isco\\s+(\\S+)\\s+.*processor', text) or re.search('Model [Nn]umber\\s*:\\s*(\\S+)', text)
        version = re.search('Version\\s+([^,\\s]+)', text)
        model = model.group(1) if model else 'UNKNOWN'
        version = version.group(1) if version else 'UNKNOWN'
    major = '.'.join(version.split('.')[:2])
    return {'device': name, 'host': d['host'], 'model': model, 'version': version, 'major': major, 'reachable': True}
rows = parallel(devices(args.inventory), collect, args.workers)
standards = {}
for model in {r.get('model') for r in rows if r.get('reachable')}:
    standards[model] = Counter((r['major'] for r in rows if r.get('model') == model)).most_common(1)[0][0]
for r in rows:
    expected = standards.get(r.get('model'), '')
    r['expected_major'] = expected
    r['result'] = 'OK' if r.get('major') == expected else 'WARN_VERSION_MISMATCH' if r.get('reachable') else 'KO_UNREACHABLE'
log.info('Rapport: %s', write_csv('software_standard_compliance', rows))
