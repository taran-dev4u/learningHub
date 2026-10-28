"""Check companion provenance, phase coverage and index integrity."""
import json
import gzip
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'AI_Engineering_Tutorial'
data = json.loads((BASE / 'companion-data.json').read_text(encoding='utf8'))
guides = json.loads((BASE / 'companion-guides.json').read_text(encoding='utf8'))
playbook = json.loads((BASE / 'decision-playbook.json').read_text(encoding='utf8'))

assert len(data['sources']) == 7
assert set(guides) == {f'phase-{i:02d}' for i in range(20)}
for key in ('sources', 'files', 'topics', 'questions'):
    assert data['counts'][key] == len(data[key]), key
sources = {s['id']: s for s in data['sources']}
assert len(sources) == 7
files = {(f['source'], f['path']) for f in data['files']}
assert len(files) == len(data['files'])
for source in data['sources']:
    assert len(source['revision']) == 40
    assert source['files'] == sum(f['source'] == source['id'] for f in data['files'])
    assert source['url'].endswith(source['revision'])
    if source['license'] != 'No license declared':
        assert (BASE / 'companion-licenses' / (source['id'].replace('/', '--') + '.txt')).exists()
        pack = json.loads(gzip.decompress((BASE / source['pack']).read_bytes()))
        assert len(pack) == source['inlineFiles']
        assert set(pack) == {f['path'] for f in data['files'] if f['source'] == source['id'] and f['inline']}
    else:
        assert source['pack'] is None and source['inlineFiles'] == 0
for topic in data['topics']:
    assert (topic['source'], topic['path']) in files
    assert topic['title'] and 0 <= topic['phase'] < 20 and 1 <= topic['level'] <= 5
for question in data['questions']:
    assert (question['source'], 'README.md') in files
    assert question['company'] and question['area'] and question['question']
    assert 0 <= question['phase'] < 20
for phase, guide in guides.items():
    assert all(guide.get(key) for key in ('title', 'explanation', 'worked', 'practice'))
    assert guide['headers'] and guide['rows']
    assert all(len(row) == len(guide['headers']) for row in guide['rows'])
assert len(guides['phase-17']['deepDive']) == 18
assert len(playbook['sections']) == 7
assert len({section['id'] for section in playbook['sections']}) == 7
assert playbook['source'].startswith('https://github.com/louisfb01/ai-engineering-cheatsheets/')
for section in playbook['sections']:
    assert section['phase'] in guides
    assert all(section.get(key) for key in ('title', 'explanation', 'worked', 'exercise', 'headers', 'rows', 'subtopics'))
    assert all(len(row) == len(section['headers']) for row in section['rows'])
    assert all(len(topic) == 2 and all(topic) for topic in section['subtopics'])
assert data['counts']['inlineFiles'] == sum(f['inline'] for f in data['files'])
assert set(Counter(t['phase'] for t in data['topics'])) == set(range(20))
print('AI companion verified:', data['counts'], '20 phase guides, 18 inference topics, 7 decision areas')
