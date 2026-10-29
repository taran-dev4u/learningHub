"""Build a pinned, searchable companion index for the requested AI repos.

Inputs are complete GitHub tree inventories and codeload ZIP snapshots kept in
ignored scratch/. The output contains metadata and topic/question titles, not
copies of upstream lessons. Run after refreshing the pinned snapshots.
"""
from __future__ import annotations

import json
import gzip
import hashlib
import os
import re
import sys
import tempfile
import time
import zipfile
from pathlib import Path

from import_ai_curriculum import atomic

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = ROOT / 'scratch'
INVENTORY = SCRATCH / 'ai_sources_inventory.json'
ZIPS = SCRATCH / 'ai_source_zips'
OUTPUT = ROOT / 'AI_Engineering_Tutorial' / 'companion-data.json'
LICENSES = ROOT / 'AI_Engineering_Tutorial' / 'companion-licenses'
CONTENT = ROOT / 'AI_Engineering_Tutorial' / 'companion-content'

DESCRIPTIONS = {
    'alirezadir/AIMLInterviews': 'ML coding, fundamentals, system design cases and interview practice. Much of the current source text is Chinese; English readers can use the mapped topic names and code exercises.',
    'pallavi-shekhar/ai-engineering-interview-questions-company-wise': 'Company wise AI engineering interview questions, grouped by role and technical area. Treat reported company processes as examples, not guarantees.',
    'calmrocks/ai-engineer-notebooks': 'Runnable, framework light notebooks for model APIs, RAG, evals, agents, serving, security and customer discovery.',
    'amitshekhariitbhu/ai-engineering-course': 'A broad AI engineering syllabus, including a detailed inference engineering sequence.',
    'amitshekhariitbhu/ai-system-design': 'AI system design concepts, capacity estimation, serving, RAG, agents, operations and case studies.',
    'owainlewis/youtube-tutorials': 'Practical tutorial lessons and code for RAG, agents, development workflows and deployment. The repository does not publish direct video IDs for these lessons.',
    'louisfb01/ai-engineering-cheatsheets': 'Decision oriented AI engineering playbook. Headings are indexed; original decision tables in the Learning Hub companion guides are independently written.',
    'aishwaryanr/awesome-generative-ai-guide': 'Main generative AI resource: learning journeys, topic guides, courses, interview roles and cases, research updates, notebooks, and video notes.',
}

COURSE_MODULES = {0: 0, 1: 2, 2: 3, 3: 7, 4: 10, 5: 10, 6: 10,
                  7: 10, 8: 11, 9: 11, 10: 14, 11: 14, 12: 17,
                  13: 17, 14: 18, 15: 12, 16: 17, 17: 6, 18: 6,
                  19: 10, 20: 19}
FOLDER_PHASES = {
    '00-setup': 0, '01-model-apis': 11, '02-evals-basics': 11,
    '03-rag': 11, '04-evals': 11, '05-agents': 14,
    '06-adaptation': 10, '07-security': 18, '08-operations': 17,
    '09-serving-inference': 17, '10-ml-system-design': 17,
    '11-customer-craft': 14, '12-case-studies-and-capstone': 19,
}

def clean(text: str) -> str:
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'!?(?:\[([^]]+)\])\([^)]*\)', r'\1', text)
    text = re.sub(r'[`*_#]', '', text).replace('\\.', '.')
    return re.sub(r'\s+', ' ', text).strip()

def phase_for(repo: str, path: str, title: str, current: int | None = None) -> int:
    low = (path + ' ' + title).lower()
    subject = title.lower()
    # A specific subject can be studied in a different phase from its source
    # chapter. These overrides keep foundational topics visible where learned.
    if any(x in subject for x in ('vision-language', 'multimodal', 'audio-language')): return 12
    if any(x in subject for x in ('linear algebra', 'matrix multiplication', 'probability', 'statistics', 'calculus', 'bayes theorem')): return 1
    if any(x in subject for x in ('computer vision', 'image classification', 'object detection', 'deepfake image', 'convolutional neural', 'convolution from scratch')): return 4
    if any(x in subject for x in ('tokenization', 'tokenizer', 'tf-idf', 'word2vec', 'text classification', 'named entity recognition')): return 5
    if any(x in subject for x in ('diffusion model', 'generative image', 'generative model', 'generative adversarial', 'stylegan')): return 8
    if any(x in subject for x in ('reinforcement learning', 'policy gradient', 'q-learning', 'reward modeling')): return 9
    if any(x in subject for x in ('autonomous agent', 'background agent', 'long-running agent', 'scheduled agent')): return 15
    if repo.endswith('/awesome-generative-ai-guide'):
        if path.startswith('interview_prep/'):
            if '/system-design/' in path: return 17
            if '/roles/' in path: return 19
            return 19
        if path.startswith('research_updates/'): return 19
        if path.startswith('topics/'):
            return {'foundations': 10, 'prompting': 11, 'rag': 11,
                    'fine-tuning': 10, 'agents': 14, 'evaluation': 11,
                    'multimodal': 12, 'production': 17,
                    'safety-security': 18}.get(Path(path).stem, 11)
        if path.startswith('journeys/') or path.startswith('paths/'): return 0
        if any(x in low for x in ('security', 'safety', 'red-team', 'guardrail')): return 18
        if any(x in low for x in ('rag', 'retrieval', 'vector', 'embedding', 'prompt', 'eval')): return 11
        if any(x in low for x in ('agent', 'mcp', 'tool use', 'harness')): return 14
        if any(x in low for x in ('inference', 'serving', 'llmops', 'production')): return 17
        if any(x in low for x in ('multimodal', 'vision', 'audio', 'voice')): return 12
        if any(x in low for x in ('fine-tun', 'lora', 'peft')): return 10
        return 11
    if repo.endswith('/ai-engineering-course'):
        m = re.search(r'\bmodule\s+(\d+)\b', title, re.I)
        if m: return COURSE_MODULES.get(int(m.group(1)), 19)
        m = re.match(r'\s*(\d+)\.', title)
        if m: return COURSE_MODULES.get(int(m.group(1)), 19)
        return current if current is not None else 19
    if repo.endswith('/ai-engineer-notebooks'):
        return next((v for k, v in FOLDER_PHASES.items() if path.startswith(k)), 19)
    if repo.endswith('/AIMLInterviews'):
        if '/MLC/' in path: return 2
        if '/MLSD/' in path: return 17
        if 'behavior' in low or 'companies' in low: return 19
        if 'genai' in low: return 11
        return 2
    if repo.endswith('/youtube-tutorials'):
        if any(x in low for x in ('gcp', 'deploy', 'postgresql', 'database')): return 17
        if any(x in low for x in ('rag', 'retrieval', 'classification')): return 11
        if any(x in low for x in ('multi-agent', 'agent-teams', 'subagent')): return 16
        if any(x in low for x in ('mcp', 'skills')): return 13
        if any(x in low for x in ('git-workflow', 'software-engineering')): return 0
        return 14
    if repo.endswith('/ai-system-design'):
        if any(x in low for x in ('rag', 'retrieval', 'embedding', 'vector database', 'chunking', 'rerank', 'context window')): return 11
        if any(x in low for x in ('agent', 'tool calling', 'mcp', 'skill', 'memory')): return 14
        if any(x in low for x in ('guardrail', 'safety', 'privacy', 'compliance', 'injection')): return 18
        if any(x in low for x in ('multimodal', 'voice', 'audio')): return 12
        return current if current is not None else 17
    if repo.endswith('/ai-engineering-cheatsheets'):
        if any(x in low for x in ('agent', 'workflow', 'multi-agent', 'memory')): return 14
        if any(x in low for x in ('cache', 'cost', 'quantiz', 'production', 'observability')): return 17
        if 'security' in low: return 18
        return current if current is not None else 11
    if repo.endswith('/ai-engineering-interview-questions-company-wise'):
        if 'llm internals' in low: return 7
        if 'ml and dl fundamentals' in low: return 2
        if any(x in low for x in ('inference', 'serving', 'gpu', 'system design')): return 17
        if any(x in low for x in ('agent', 'tool use')): return 14
        if any(x in low for x in ('rag', 'retrieval', 'evaluation', 'observability')): return 11
        if any(x in low for x in ('fine-tuning', 'post-training', 'alignment')): return 10
        if any(x in low for x in ('safety', 'security', 'responsible')): return 18
        if any(x in low for x in ('multimodal', 'speech', 'voice')): return 12
        if any(x in low for x in ('coding', 'data structures')): return 2
        return 19
    return 19

def file_kind(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == '.ipynb': return 'notebook'
    if suffix == '.md': return 'lesson' if path.endswith('/LESSON.md') else 'reading'
    if suffix in ('.py', '.ts', '.js', '.go', '.sql', '.sh'): return 'code'
    if suffix in ('.png', '.jpg', '.jpeg', '.svg', '.pdf'): return 'media'
    return 'file'

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

def build() -> None:
    if not INVENTORY.exists(): raise SystemExit('Missing complete tree inventory: ' + str(INVENTORY))
    raw = json.loads(INVENTORY.read_text(encoding='utf8'))
    if len(raw) != 8 or any(x['truncated'] for x in raw):
        raise SystemExit('Expected eight complete, non-truncated GitHub trees')
    result = {'sources': [], 'files': [], 'topics': [], 'questions': []}
    attributions = ['# AI Engineering companion sources', '',
                    'The Learning Hub explanations and decision tables are original. This index links eight pinned public repositories and reproduces short topic titles and Apache-licensed interview practice prompts. See each source for its full material and current updates.', '']
    for item in raw:
        repo, revision = item['repo'], item['revision']
        archive = ZIPS / (repo.replace('/', '--') + '.zip')
        if not archive.exists(): raise SystemExit('Missing archive: ' + str(archive))
        expected = {f['path']: f for f in item['files']}
        with zipfile.ZipFile(archive) as zip_file:
            members = {p.split('/', 1)[1]: p for p in zip_file.namelist() if '/' in p and not p.endswith('/')}
            if set(members) != set(expected):
                raise SystemExit('Archive and Git tree differ: ' + repo)
            pack_name = 'companion-content/' + repo.replace('/', '--') + '.json.gz' if item['license'] else None
            source = {'id': repo, 'revision': revision, 'license': item['license'] or 'No license declared',
                      'description': DESCRIPTIONS[repo], 'files': len(expected),
                      'url': 'https://github.com/' + repo + '/tree/' + revision,
                      'pack': pack_name}
            result['sources'].append(source)
            pack = {}
            license_path = next((p for p in ('LICENSE', 'LICENSE.md', 'LICENSE.txt') if p in members), None)
            if license_path:
                LICENSES.mkdir(exist_ok=True)
                local_license = LICENSES / (repo.replace('/', '--') + '.txt')
                atomic(local_license, zip_file.read(members[license_path]).decode('utf8', 'replace'))
            attributions.extend(['## ' + repo, '', '- Pinned revision: `' + revision + '`',
                                 '- Source: https://github.com/' + repo + '/tree/' + revision,
                                 '- Declared license: ' + source['license'],
                                 '- Local license copy: ' + (local_license.relative_to(ROOT).as_posix() if license_path else 'none declared upstream'), ''])
            for path, record in sorted(expected.items()):
                raw_bytes = zip_file.read(members[path])
                blob = hashlib.sha1(b'blob ' + str(len(raw_bytes)).encode() + b'\0' + raw_bytes).hexdigest()
                if blob != record['sha']:
                    raise SystemExit('Git blob mismatch: ' + repo + '/' + path)
                title = clean(Path(path).stem.replace('-', ' ').replace('_', ' '))
                phase = phase_for(repo, path, title)
                inline = False
                if pack_name and 0 < record.get('size', 0) <= 1_000_000 and file_kind(path) != 'media':
                    try:
                        raw_text = raw_bytes.decode('utf8')
                        if '\x00' not in raw_text:
                            pack[path] = raw_text
                            inline = True
                    except UnicodeDecodeError:
                        pass
                result['files'].append({'source': repo, 'path': path, 'kind': file_kind(path),
                                        'size': record.get('size', 0), 'phase': phase, 'inline': inline})
                if not path.lower().endswith(('.md', '.ipynb')) or record.get('size', 0) == 0:
                    continue
                # Chinese and Persian translations remain in the complete file list.
                if path.startswith(('cn/', 'fa/')): continue
                try:
                    if path.endswith('.ipynb'):
                        notebook = json.loads(raw_bytes)
                        text = '\n'.join(''.join(cell.get('source', [])) for cell in notebook.get('cells', []) if cell.get('cell_type') == 'markdown')
                    else: text = raw_bytes.decode('utf8', 'replace')
                except (ValueError, UnicodeError): continue
                current_phase = phase
                company = ''
                section = ''
                top_section = ''
                for line in text.splitlines():
                    heading = re.match(r'^(#{1,5})\s+(.+?)\s*$', line)
                    if heading:
                        level, heading_title = len(heading.group(1)), clean(heading.group(2))
                        if not heading_title: continue
                        if repo.endswith('/ai-engineering-course'):
                            current_phase = phase_for(repo, path, heading_title, current_phase)
                        elif repo.endswith('/ai-engineering-interview-questions-company-wise'):
                            if level == 2:
                                top_section = heading_title
                                company = ''
                                section = ''
                            elif level == 3:
                                if top_section == 'Common Questions Asked Across Companies':
                                    company, section = 'Across companies', heading_title
                                else:
                                    company, section = heading_title, ''
                            elif level == 4: section = heading_title
                            current_phase = phase_for(repo, path, section or heading_title, current_phase)
                        else: current_phase = phase_for(repo, path, heading_title, current_phase if level > 2 else None)
                        result['topics'].append({'source': repo, 'path': path, 'title': heading_title,
                                                 'level': level, 'phase': current_phase})
                        continue
                    if repo.endswith('/ai-engineering-interview-questions-company-wise'):
                        question = re.match(r'^-\s+(.+)', line)
                        if question and company and section:
                            wording = clean(question.group(1))
                            if wording and not wording.startswith(('Answer:', 'See ')):
                                result['questions'].append({'company': company, 'area': section,
                                                            'question': wording, 'phase': phase_for(repo, path, section),
                                                            'source': repo})
            if pack_name:
                source['inlineFiles'] = len(pack)
                payload = json.dumps(pack, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                atomic_bytes(ROOT / 'AI_Engineering_Tutorial' / pack_name, gzip.compress(payload, compresslevel=9, mtime=0))
            else:
                source['inlineFiles'] = 0
    counts = {key: len(result[key]) for key in ('sources', 'files', 'topics', 'questions')}
    counts['inlineFiles'] = sum(source['inlineFiles'] for source in result['sources'])
    result['counts'] = counts
    atomic(OUTPUT, json.dumps(result, ensure_ascii=False, separators=(',', ':')))
    atomic(ROOT / 'AI_Engineering_Tutorial' / 'COMPANION_ATTRIBUTION.md', '\n'.join(attributions) + '\n')
    print('Companion index:', counts, 'bytes', OUTPUT.stat().st_size)

if __name__ == '__main__':
    build()
