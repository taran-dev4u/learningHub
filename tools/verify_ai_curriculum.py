"""Verify every imported source byte and every declared curriculum destination."""
import base64
import collections
import gzip
import hashlib
import json
from pathlib import Path
import re
from import_ai_curriculum import headings

ROOT = Path(__file__).resolve().parent.parent / 'AI_Engineering_Tutorial'
catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
index = json.loads((ROOT / 'source/index.json').read_text(encoding='utf-8'))
inventory = json.loads((ROOT / 'source/inventory.json').read_text(encoding='utf-8'))
expected = {r['path']: r for r in inventory['files']}
actual = {p for p in index['files'] if not p.startswith('@generated/')}
assert actual == set(expected), ('Missing or extra source files', set(expected) - actual, actual - set(expected))
payload = {}
for pack in index['packs']:
    data = (ROOT / pack['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == pack['sha256'], pack['path']
    records = json.loads(gzip.decompress(data))
    assert len(records) == pack['records'], pack['path']
    payload.update(records)
text = {}
for path, record in index['files'].items():
    data = payload[record['hash']]
    raw = base64.b64decode(data['content']) if data['encoding'] == 'base64' else data['content'].encode('utf-8')
    assert hashlib.sha256(raw).hexdigest() == record['hash'], path
    assert len(raw) == record['size'], path
    if path in expected:
        git_hash = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert git_hash == expected[path]['sha'] == record['gitBlob'], path
    if data['encoding'] == 'utf8': text[path] = data['content']
entries = {e['id']: e for e in catalog['entries']}
assert len(entries) == len(catalog['entries']), 'Duplicate curriculum routes'
paths = {e['path'] for e in entries.values()}
for group in catalog['groups']:
    assert group['entries'], group['id']
    assert all(e in entries for e in group['entries']), group['id']
for entry in entries.values():
    assert entry['contentPath'] in index['files'], entry['contentPath']
    assert entry['path'] in actual, entry['path']
    assert entry['headings'] == headings(text.get(entry['contentPath'], '')), entry['id']
    if entry['kind'] == 'phase':
        assert entry['contentPath'] == entry['path'], 'Core lesson replaced by a summary'
for pattern in [r'^phases/[^/]+/[^/]+/docs/en\.md$', r'^certifications/[^/]+/lessons/[^/]+/docs/en\.md$',
                r'^manuals/[^/]+/(?:sections/[^/]+|front)\.md$', r'^practice/[^/]+/problem\.md$', r'^cheatsheets/[^/]+\.md$']:
    required = {p for p in actual if re.match(pattern, p)}
    assert required <= paths, ('Unlisted study source', required - paths)
assert {a['file'] for a in catalog['artifacts']} <= paths, 'Missing artifact destinations'
quizzes = {}
for path in actual:
    if not path.endswith('.json') or not path.startswith(('phases/', 'certifications/')): continue
    try: data = json.loads(text.get(path, ''))
    except (ValueError, TypeError): continue
    if isinstance(data, dict) and isinstance(data.get('questions'), list) and data['questions']: quizzes[path] = len(data['questions'])
assert set(quizzes) == {e['path'] for e in entries.values() if e['kind'] == 'quiz'}, 'Missing quiz/assessment'
assert sum(quizzes.values()) == catalog['counts']['quizQuestions'], 'Question count drift'
counts = collections.Counter(e['kind'] for e in entries.values())
for kind, number in counts.items(): assert catalog['counts'][kind] == number, kind
assert catalog['counts']['sourceFiles'] == len(actual)
assert catalog['counts']['entries'] == len(entries)
assert catalog['counts']['subtopics'] == sum(sum(h['level'] > 1 for h in e['headings']) for e in entries.values())
assert (ROOT / 'SOURCE_LICENSE.txt').read_text(encoding='utf-8') == text['LICENSE']
print(f"Verified {len(actual):,} source files byte-for-byte against Git blobs at {catalog['source']['revision']}.")
print(f"Verified {len(entries):,} study entries and {catalog['counts']['subtopics']:,} syllabus headings; zero missing destinations.")
