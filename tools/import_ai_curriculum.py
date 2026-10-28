"""Import the complete, pinned MIT source as data; never execute upstream code.

Usage: python tools/import_ai_curriculum.py /path/to/upstream scratch/ai-source-tree.json
Every tracked file is content-addressed and preserved in deterministic gzip
packs. The study catalogue uses the actual Markdown, not generated summaries.
"""
import base64
import collections
import gzip
import hashlib
import html
import json
import mimetypes
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import urllib.parse
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'AI_Engineering_Tutorial'
MARKDOWN = MarkdownIt('commonmark')


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str): data = data.encode('utf-8')
    if path.exists() and path.read_bytes() == data: return
    fd, temp = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream: stream.write(data)
        for attempt in range(5):
            try:
                os.replace(temp, path)
                break
            except OSError:
                if attempt == 4: raise
                time.sleep(.2 * (attempt + 1))
    finally:
        if os.path.exists(temp): os.unlink(temp)


def dump(data): return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
def plain(text):
    text = re.sub(r'!?\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]*>|[*`]', '', text)
    return html.unescape(re.sub(r'(?<!\w)_+|_+(?!\w)', '', text)).strip()
def slug(text): return re.sub(r'[^a-z0-9]+', '-', plain(text).lower()).strip('-') or 'section'


def headings(text):
    result, counts = [], collections.Counter()
    tokens = MARKDOWN.parse(text)
    def add(level, title):
        key = slug(title); counts[key] += 1
        result.append({'level': level, 'title': title, 'anchor': key + (f'-{counts[key]}' if counts[key] > 1 else '')})
    for i, token in enumerate(tokens):
        if token.type == 'html_block' and re.search(r'<h[1-6]\b', token.content, re.I):
            from bs4 import BeautifulSoup
            for tag in BeautifulSoup(token.content, 'html.parser').find_all(re.compile('^h[1-6]$')):
                add(int(tag.name[1:]), tag.get_text())
        if token.type != 'heading_open': continue
        inline = tokens[i + 1]
        title = ''.join(t.content if t.type in ['text', 'code_inline', 'image'] else ' ' if t.type in ['softbreak', 'hardbreak'] else '' for t in (inline.children or []))
        level = int(token.tag[1:])
        add(level, title)
    return result


def main():
    upstream = Path(sys.argv[1]).resolve()
    inventory = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    tracked = [x for x in inventory['tree'] if x['type'] == 'blob']
    revision = (upstream / '.git/refs/heads/main').read_text().strip()
    source_url = f'https://github.com/rohitg00/ai-engineering-from-scratch/tree/{revision}/'
    files, payload, payload_bytes, pack_number, text_files = {}, {}, 0, 0, {}
    hashes, packs = {}, []
    previous_path = OUT / 'source/index.json'
    if previous_path.exists():
        previous = json.loads(previous_path.read_text(encoding='utf-8'))
        if previous['source']['revision'] == revision and all((OUT / p['path']).exists() for p in previous['packs']):
            packs = previous['packs']
            hashes = {v['hash']: v['pack'] for v in previous['files'].values()}
            pack_number = len(packs)

    def flush():
        nonlocal payload, payload_bytes, pack_number
        if not payload: return
        name = f'source/packs/{pack_number:03d}.json.gz'
        encoded = dump(payload).encode('utf-8')
        compressed = gzip.compress(encoded, compresslevel=9, mtime=0)
        atomic(OUT / name, compressed)
        packs.append({'path': name, 'sha256': hashlib.sha256(compressed).hexdigest(), 'records': len(payload), 'bytes': len(compressed)})
        payload, payload_bytes, pack_number = {}, 0, pack_number + 1

    def store(path, raw, original_sha=None):
        nonlocal payload_bytes
        digest = hashlib.sha256(raw).hexdigest()
        try:
            content = raw.decode('utf-8'); encoding = 'utf8'
            if '\x00' in content: raise UnicodeError('binary')
            text_files[path] = content
        except UnicodeError:
            content, encoding = base64.b64encode(raw).decode('ascii'), 'base64'
        if digest not in hashes:
            if payload_bytes > 2_000_000: flush()
            hashes[digest] = f'source/packs/{pack_number:03d}.json.gz'
            payload[digest] = {'encoding': encoding, 'content': content}
            payload_bytes += len(content.encode('utf-8')) + 120
        files[path] = {'hash': digest, 'pack': hashes[digest], 'size': len(raw), 'encoding': encoding,
                       'mime': mimetypes.guess_type(path)[0] or 'text/plain', 'gitBlob': original_sha}

    for source_number, record in enumerate(tracked, 1):
        path = record['path']; raw = (upstream / path).read_bytes()
        def git_hash(data): return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if git_hash(raw) != record['sha']:
            normalized = raw.replace(b'\r\n', b'\n')
            if git_hash(normalized) != record['sha']: raise ValueError('Source revision/byte mismatch: ' + path)
            raw = normalized
        store(path, raw, record['sha'])
        if source_number % 2000 == 0: print(f'Verified source files: {source_number}/{len(tracked)}', flush=True)

    source_data = text_files['site/data.js']
    def constant(name):
        match = re.search(r'const ' + name + r'\s*=\s*', source_data)
        return json.JSONDecoder().raw_decode(source_data[match.end():])[0]
    phases, paths, glossary = constant('PHASES'), constant('LEARNING_PATHS'), constant('GLOSSARY')
    artifacts, prerequisites = constant('ARTIFACTS'), constant('ROADMAP_PREREQS')
    groups, entries, ids = [], [], set()
    # Keep existing verified videos by matching old tutorial titles/routes.
    def js_json(file, marker):
        text = file.read_text(encoding='utf-8')
        return json.JSONDecoder().raw_decode(text.split(marker, 1)[1].lstrip())[0]
    old_topics = js_json(OUT / 'topics.js', 'window.topicsData =')
    old_resources = js_json(OUT / 'resources.js', 'window.aiResources =')
    videos_by_title = {}
    for section in old_topics:
        for sub in section['subsections']:
            for topic in sub['concepts']:
                resource = old_resources.get('concepts', {}).get(sub['id'] + '/' + topic['anchor'], {})
                if resource.get('videos'):
                    videos_by_title[slug(re.split(r'\s+[—–]\s+', topic['title'])[0])] = resource['videos']

    def group(key, title, kind, **extra):
        value = {'id': key, 'title': title, 'kind': kind, 'entries': [], **extra}
        groups.append(value); return value

    def entry(g, path, title=None, summary='', status='published', content_path=None, **extra):
        key = content_path or path
        if key in ids:
            g['entries'].append(key); return
        ids.add(key)
        content = text_files.get(key, '')
        hs = headings(content)
        value = {'id': key, 'path': path, 'contentPath': key, 'group': g['id'], 'kind': g['kind'],
                 'title': title or (hs[0]['title'] if hs else Path(path).stem.replace('-', ' ').title()),
                 'summary': summary, 'status': status, 'headings': hs, **extra}
        value['videos'] = videos_by_title.get(slug(value['title']), [])
        entries.append(value); g['entries'].append(key)

    def virtual(path, text): store(path, text.encode('utf-8')); return path
    def structure(value, level=2):
        if isinstance(value, dict):
            return '\n\n'.join('#' * min(level, 6) + ' ' + re.sub(r'(?<!^)(?=[A-Z])', ' ', str(k)).replace('_', ' ').title() + '\n\n' + structure(v, level + 1) for k, v in value.items())
        if isinstance(value, list):
            return '\n\n'.join(structure(v, level) if isinstance(v, (dict, list)) else '- ' + str(v) for v in value)
        if isinstance(value, str):
            target = value.rstrip('/')
            if target + '/docs/en.md' in files: target += '/docs/en.md'
            if target in files: return '[' + value + '](/' + target + ')'
        return str(value)

    for phase in phases:
        g = group(f'phase-{phase["id"]:02}', f'Phase {phase["id"]:02} · {phase["name"]}', 'phase', description=phase['desc'], prerequisites=prerequisites.get(str(phase['id']), []))
        for lesson in phase['lessons']:
            path = lesson['url'].split('/tree/main/', 1)[1].rstrip('/') + '/docs/en.md'
            if path not in files: raise ValueError('Missing declared lesson: ' + path)
            entry(g, path, lesson['name'], lesson.get('summary', ''), lesson.get('status', 'published'), languages=lesson.get('lang', ''), lessonType=lesson.get('type', ''))

    for manifest in sorted(upstream.glob('manuals/*/manual.json')):
        data = json.loads(manifest.read_text(encoding='utf-8')); directory = manifest.parent.relative_to(upstream).as_posix()
        g = group('manual-' + data['id'], data['title'], 'manual', description=data.get('summary', ''), metadata=data)
        def declared(value):
            if isinstance(value, dict):
                for v in value.values(): yield from declared(v)
            elif isinstance(value, list):
                for v in value: yield from declared(v)
            elif isinstance(value, str) and value.endswith('.md') and directory + '/' + value in files: yield directory + '/' + value
        for path in dict.fromkeys(declared([data.get('front'), data.get('parts'), data.get('reference')])): entry(g, path)
        for path in sorted(files):
            if path.startswith(directory + '/sections/') and path.endswith('.md') and path not in ids: entry(g, path)

    practice_group = group('practice', 'Hands-on practice', 'practice')
    for meta in sorted(upstream.glob('practice/*/meta.json')):
        data = json.loads(meta.read_text(encoding='utf-8')); directory = meta.parent.relative_to(upstream).as_posix()
        entry(practice_group, directory + '/problem.md', data['title'], data.get('summary', ''), metadata=data)

    project_group = group('projects', 'Runnable projects', 'project')
    for meta in sorted(upstream.glob('projects/*/project.json')):
        data = json.loads(meta.read_text(encoding='utf-8')); directory = meta.parent.relative_to(upstream).as_posix()
        path = directory + '/README.md'
        if path not in files: path = directory + '/project.json'
        entry(project_group, path, data['title'], data.get('summary', ''), data.get('status', 'published'), metadata=data)
    planned = json.loads(text_files['projects/roadmap.json'])['planned']
    planned_group = group('planned-projects', 'Planned projects', 'planned', description='Upstream plans are preserved as plans; they do not have completed implementations.')
    for data in planned:
        path = virtual('@generated/planned/' + data['id'] + '.md', '# ' + data['title'] + '\n\n' + structure(data))
        entry(planned_group, 'projects/roadmap.json', data['title'], data.get('summary', ''), 'planned', path)

    for program in sorted(upstream.glob('certifications/*/program.json')):
        data = json.loads(program.read_text(encoding='utf-8')); base = program.parent.relative_to(upstream).as_posix()
        g = group('cert-' + program.parent.name, data.get('name', data['id']), 'certification', description=data.get('summary', ''), metadata=data)
        for path in sorted(files):
            if path.startswith(base + '/lessons/') and path.endswith('/docs/en.md'): entry(g, path)
        for track in sorted(program.parent.glob('tracks/*.json')):
            metadata = json.loads(track.read_text(encoding='utf-8'))
            path = virtual('@generated/certifications/' + metadata['id'] + '.md', '# ' + metadata['credential'] + '\n\n' + structure(metadata))
            entry(g, track.relative_to(upstream).as_posix(), metadata['credential'], metadata.get('summary', ''), content_path=path)

    cheatsheet_group = group('cheatsheets', 'Cheat sheets', 'cheatsheet')
    for path in sorted(files):
        if path.startswith('cheatsheets/') and path.endswith('.md'): entry(cheatsheet_group, path)
    path_group = group('learning-paths', 'Learning paths', 'path')
    # Read all path manifests from disk, including any not yet in built site data.
    for manifest in sorted(upstream.glob('learning-paths/*.json')):
        data = json.loads(manifest.read_text(encoding='utf-8'))
        path = virtual('@generated/paths/' + data['id'] + '.md', '# ' + data['title'] + '\n\n' + structure(data))
        entry(path_group, manifest.relative_to(upstream).as_posix(), data['title'], data.get('summary', ''), content_path=path, metadata=data)
    glossary_group = group('glossary', 'Glossary', 'glossary')
    for term in glossary:
        path = virtual('@generated/glossary/' + term['slug'] + '.md', '# ' + term['term'] + '\n\n' + structure(term))
        entry(glossary_group, 'glossary/terms.md', term['term'], term.get('means', ''), content_path=path)
    artifact_group = group('artifacts', 'Prompts, skills & lesson outputs', 'artifact')
    for artifact in artifacts:
        if artifact['file'] not in files: raise ValueError('Missing declared artifact: ' + artifact['file'])
        entry(artifact_group, artifact['file'], artifact['name'], artifact.get('description', ''), metadata=artifact)
    quiz_group = group('quizzes', 'Lesson quizzes & certification assessments', 'quiz')
    question_count = 0
    for path in sorted(actual for actual in files if actual.endswith('.json') and actual.startswith(('phases/', 'certifications/'))):
        try: data = json.loads(text_files.get(path, ''))
        except (ValueError, TypeError): continue
        if not isinstance(data, dict) or not isinstance(data.get('questions'), list) or not data['questions']: continue
        questions = data['questions']; question_count += len(questions)
        lesson_doc = path.rsplit('/', 1)[0] + '/docs/en.md'
        title = data.get('title') or ((headings(text_files[lesson_doc])[0]['title'] + ' · Quiz') if lesson_doc in text_files else Path(path).stem.replace('-', ' ').title())
        entry(quiz_group, path, title, f'{len(questions)} original source questions, with answers and explanations.', questionCount=len(questions))
    guides = group('guides', 'Course guides and roadmaps', 'guide')
    for path in ['README.md', 'ROADMAP.md', 'learning-paths/CAREER-PRACTICE.md', 'projects/README.md', 'projects/ROADMAP.md', 'projects/VALIDATION.md', 'glossary/myths.md', 'site/developer.md', 'site/skills.md']:
        if path in files: entry(guides, path)
    # Preserve the explanatory text from the website's visual guides as well
    # as their complete original HTML/JS in the source browser.
    from bs4 import BeautifulSoup
    from markdownify import markdownify
    visuals = group('visual-guides', 'Interactive visual guides', 'visual', description='Complete guide text and source; open the original for its live interactive simulation.')
    for name in ['inside-an-ai-agent', 'inside-a-decompiler', 'inside-an-llm-serving-gpu', 'how-to-learn', 'roadmap', 'learning-paths', 'catalog', 'developer', 'skills']:
        origin = 'site/' + name + '.html'
        if origin not in text_files: continue
        soup = BeautifulSoup(text_files[origin], 'html.parser')
        for tag in soup.select('script, style, nav, header, footer, svg, canvas'): tag.decompose()
        body = soup.find('main') or soup.body or soup
        converted = markdownify(str(body), heading_style='ATX')
        path = virtual('@generated/website/' + name + '.md', converted)
        entry(visuals if name.startswith('inside-') else guides, origin, content_path=path, originalSite='https://aiengineeringfromscratch.com/' + name)
    flush()

    counts = collections.Counter(entry['kind'] for entry in entries)
    counts.update({'phases': len(phases), 'manuals': sum(g['kind'] == 'manual' for g in groups), 'sourceFiles': len(tracked),
                   'subtopics': sum(sum(h['level'] > 1 for h in entry['headings']) for entry in entries),
                   'artifacts': len(artifacts), 'entries': len(entries), 'packs': len(packs)})
    counts['certificationLessons'] = sum(e['kind'] == 'certification' and e['path'].endswith('/docs/en.md') for e in entries)
    counts['certificationTracks'] = sum(e['kind'] == 'certification' and '/tracks/' in e['path'] for e in entries)
    counts['quizQuestions'] = question_count
    declared_phases = {e['path'] for e in entries if e['kind'] == 'phase'}
    actual_phases = {p for p in files if re.match(r'^phases/[^/]+/[^/]+/docs/en\.md$', p)}
    if declared_phases != actual_phases: raise ValueError('Phase syllabus does not cover every source lesson')
    source = {'repository': 'https://github.com/rohitg00/ai-engineering-from-scratch', 'website': 'https://aiengineeringfromscratch.com/',
              'revision': revision, 'tree': inventory['sha'], 'license': 'MIT', 'copyright': 'Copyright (c) 2026 Rohit Ghumare'}
    atomic(OUT / 'source/index.json', dump({'source': source, 'files': files, 'packs': packs}))
    atomic(OUT / 'source/inventory.json', dump({'source': source, 'files': [{k: r[k] for k in ['path', 'sha', 'size', 'mode']} for r in tracked]}))
    atomic(OUT / 'catalog.json', dump({'source': source, 'counts': dict(counts), 'groups': groups, 'entries': entries, 'artifacts': artifacts}))
    atomic(OUT / 'SOURCE_LICENSE.txt', text_files['LICENSE'])
    atomic(OUT / 'coverage.json', dump({'source': source, 'counts': dict(counts), 'missingSourceFiles': [], 'missingPhaseLessons': [],
            'trackedBytes': sum(files[x['path']]['size'] for x in tracked), 'packedBytes': sum(p['bytes'] for p in packs),
            'headingCount': sum(len(e['headings']) for e in entries), 'trackedFileHashesVerified': len(tracked)}))
    # Preserve the original 177-concept guide as a separate companion page.
    legacy = ROOT / 'ai_engineering.html'
    if 'data-ai-curriculum' not in legacy.read_text(encoding='utf-8'):
        atomic(OUT / 'concept-guide.html', legacy.read_text(encoding='utf-8').replace('<head>', '<head>\n<base href="../">', 1))
    print(json.dumps({'revision': revision, **dict(counts), 'packedMB': round(sum(p['bytes'] for p in packs) / 1e6, 2)}, indent=2))


if __name__ == '__main__': main()
