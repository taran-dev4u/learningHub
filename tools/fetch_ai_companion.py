"""Fetch the seven pinned public AI source snapshots for a reproducible rebuild.

Run from anywhere: python tools/fetch_ai_companion.py [--latest]
The default uses revisions already recorded in companion-data.json. --latest
refreshes to each repository's current default-branch head for a new review.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'AI_Engineering_Tutorial' / 'companion-data.json'
SCRATCH = ROOT / 'scratch'
ZIPS = SCRATCH / 'ai_source_zips'

def fetch(url: str) -> bytes:
    request = Request(url, headers={'User-Agent': 'LearningHub-source-audit',
                                    'Accept': 'application/vnd.github+json'})
    with urlopen(request, timeout=120) as response:
        return response.read()

def atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('wb', dir=path.parent, delete=False) as temp:
        temp.write(data)
        name = temp.name
    try:
        for attempt in range(4):
            try:
                os.replace(name, path)
                break
            except OSError:
                if attempt == 3: raise
                time.sleep(0.2 * (attempt + 1))
    finally:
        if os.path.exists(name): os.unlink(name)

def main() -> None:
    latest = '--latest' in sys.argv[1:]
    sources = json.loads(DATA.read_text(encoding='utf8'))['sources']
    if len(sources) != 7: raise SystemExit('Expected seven pinned sources')
    inventory = []
    for source in sources:
        repo = source['id']
        meta = json.loads(fetch('https://api.github.com/repos/' + repo))
        revision = source['revision']
        if latest:
            commit = json.loads(fetch('https://api.github.com/repos/' + repo + '/commits/' + meta['default_branch']))
            revision = commit['sha']
        tree = json.loads(fetch('https://api.github.com/repos/' + repo + '/git/trees/' + revision + '?recursive=1'))
        if tree.get('truncated'): raise SystemExit('GitHub tree was truncated: ' + repo)
        archive = fetch('https://codeload.github.com/' + repo + '/zip/' + revision)
        atomic_bytes(ZIPS / (repo.replace('/', '--') + '.zip'), archive)
        files = [entry for entry in tree['tree'] if entry['type'] == 'blob']
        inventory.append({'repo': repo, 'revision': revision,
                          'branch': meta['default_branch'],
                          'license': (meta.get('license') or {}).get('spdx_id'),
                          'truncated': False, 'files': files})
        print(repo, revision[:12], len(files), 'files', flush=True)
    atomic_bytes(SCRATCH / 'ai_sources_inventory.json',
                 json.dumps(inventory, ensure_ascii=False).encode('utf8'))

if __name__ == '__main__':
    main()
