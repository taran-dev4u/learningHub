"""Generate both AI curriculum entry pages from the imported source catalogue."""
import json
from pathlib import Path
from import_ai_curriculum import atomic

ROOT = Path(__file__).resolve().parent.parent
catalog = json.loads((ROOT / 'AI_Engineering_Tutorial/catalog.json').read_text(encoding='utf-8'))
c = catalog['counts']; revision = catalog['source']['revision'][:12]
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
atomic(ROOT / 'AI_Engineering_Tutorial/index.html', template.replace('__BASE__', '<base href="../">'))
print('Built both AI entry pages from source revision', revision)
