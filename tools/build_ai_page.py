"""Generate both AI curriculum entry pages from the imported source catalogue."""
import json
import hashlib
import re
from pathlib import Path
from import_ai_curriculum import atomic

ROOT = Path(__file__).resolve().parent.parent
catalog = json.loads((ROOT / 'AI_Engineering_Tutorial/catalog.json').read_text(encoding='utf-8'))
c = catalog['counts']
revision = hashlib.sha256((ROOT / 'assets/ai-curriculum.js').read_bytes() + (ROOT / 'assets/ai-curriculum.css').read_bytes() + (ROOT / 'AI_Engineering_Tutorial/catalog.json').read_bytes()).hexdigest()[:12]
template = '''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
__BASE__
<title>AI Engineering · Complete Curriculum · Learning Hub</title>
<meta name="description" content="Complete source curriculum: __PHASES__ phases, __LESSONS__ lessons, manuals, projects, practice, certifications, learning paths, cheat sheets and glossary.">
<link rel="stylesheet" href="assets/learning-hub-shared.css">
<script src="assets/learning-hub-shared.js"></script>
<link rel="stylesheet" href="assets/ai-curriculum.css?v=__REV__">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github-dark.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
</head><body data-ai-curriculum>
<main id="ai-curriculum"><h1>AI Engineering from Scratch</h1><p>Loading the complete curriculum…</p></main>
<noscript>This curriculum needs JavaScript. The full source is available at <a href="https://github.com/rohitg00/ai-engineering-from-scratch">AI Engineering from Scratch</a>.</noscript>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<script src="assets/ai-curriculum.js?v=__REV__"></script>
</body></html>
'''
template = template.replace('__PHASES__', str(c['phases'])).replace('__LESSONS__', str(c['phase'])).replace('__REV__', revision)
atomic(ROOT / 'ai_engineering.html', template.replace('__BASE__', ''))
atomic(ROOT / 'AI_Engineering_Tutorial/index.html', template.replace('__BASE__', '').replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/'))
guide = ROOT / 'AI_Engineering_Tutorial/concept-guide.html'
if guide.exists() and '<base href="../">' in guide.read_text(encoding='utf-8'):
    guide_html = guide.read_text(encoding='utf-8').replace('<base href="../">', '')
    def relative_link(match):
        value = match[2]
        if value.startswith(('#', '/', 'data:', 'mailto:', 'javascript:')) or re.match(r'^https?://', value): return match[0]
        return match[1] + '../' + value + match[3]
    guide_html = re.sub(r'((?:href|src)=["\'])([^"\']+)(["\'])', relative_link, guide_html)
    atomic(guide, guide_html)
old_topics_text = (ROOT / 'AI_Engineering_Tutorial/topics.js').read_text(encoding='utf-8')
old_topics = json.JSONDecoder().raw_decode(old_topics_text.split('window.topicsData =', 1)[1].lstrip())[0]
def normalized(value): return re.sub(r'[^a-z0-9]+', '', value.lower())
legacy_routes = {}
by_title = {}
for entry in catalog['entries']: by_title.setdefault(normalized(entry['title']), []).append(entry)
for section in old_topics:
    for sub in section['subsections']:
        for topic in sub['concepts']:
            short = re.split(r'\s+[—–]\s+', topic['title'])[0]
            matches = by_title.get(normalized(short), [])
            phase_matches = [e for e in matches if e['group'] == sub['id']]
            if phase_matches or matches:
                legacy_routes[sub['id'] + '/' + topic['anchor']] = (phase_matches or matches)[0]['contentPath']
atomic(ROOT / 'AI_Engineering_Tutorial/legacy-routes.json', json.dumps(legacy_routes, ensure_ascii=False, separators=(',', ':')))
print('Built both AI entry pages from source revision', catalog['source']['revision'][:12], 'with asset release', revision)
