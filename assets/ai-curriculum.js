/* Full MIT curriculum snapshot: lazy content packs, syllabus and source reader. */
(function () {
  'use strict';
  var script = document.currentScript;
  var base = new URL('../', script.src).href;
  var release = new URL(script.src).searchParams.get('v') || '1';
  var root, catalog, sourceIndex, entries, groups, packs = new Map(), filePromise;
  var panelMode=window.self!==window.top && new URLSearchParams(location.search).has('panel');
  var query = '', kind = '', pageNumber = 0, selected = 'overview', routeToken = 0;
  var NAV_KEY = 'hub_ai_nav_closed_v1', TOC_KEY = 'hub_ai_toc_closed_v1';
  function closed(key) { return localStorage.getItem(key) === '1'; }
  var DONE_KEY = 'hub_done_ai_source_v1';
  var BOOKMARK_KEY = 'hub_bm_ai_source_v1';
  function doneSet() { try { return new Set(JSON.parse(localStorage.getItem(DONE_KEY) || '[]')); } catch (_) { return new Set(); } }
  function bookmarks() { try { return new Set(JSON.parse(localStorage.getItem(BOOKMARK_KEY) || '[]')); } catch (_) { return new Set(); } }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function route(path, section) { return '#read=' + encodeURIComponent(path) + (section ? '&section=' + encodeURIComponent(section) : ''); }
  function sourceUrl(path) { return catalog.source.repository + '/blob/' + catalog.source.revision + '/' + path.split('/').map(encodeURIComponent).join('/'); }
  function formatBytes(n) { return n > 1e6 ? (n / 1e6).toFixed(1) + ' MB' : n > 1000 ? Math.round(n / 1000) + ' KB' : n + ' B'; }
  function button(label, href, extra) { return '<a class="aic-button' + (extra || '') + '" href="' + esc(href) + '">' + esc(label) + '</a>'; }
  function slug(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'section'; }
  async function files() {
    if (!filePromise) filePromise = fetch(base + 'AI_Engineering_Tutorial/source/index.json?v=' + release).then(function (r) { if (!r.ok) throw Error('Source index could not load'); return r.json(); }).then(function (d) { sourceIndex = d; return d; });
    return filePromise;
  }
  async function content(path) {
    var index = await files(), record = index.files[path];
    if (!record) throw Error('This source file is not in the imported snapshot: ' + path);
    if (!packs.has(record.pack)) packs.set(record.pack, fetch(base + 'AI_Engineering_Tutorial/' + record.pack + '?v=' + release).then(async function (r) {
      if (!r.ok) throw Error('Source content could not load');
      var bytes = new Uint8Array(await r.arrayBuffer());
      if (bytes[0] === 31 && bytes[1] === 139) {
        var stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
        return JSON.parse(await new Response(stream).text());
      }
      return JSON.parse(new TextDecoder().decode(bytes));
    }));
    var pack;
    try{pack=await packs.get(record.pack);}catch(error){packs.delete(record.pack);throw error;}
    var data = pack[record.hash];
    if (!data) throw Error('Source pack is missing a file');
    return { record: record, data: data };
  }
  function bytesOf(data) { return data.encoding === 'base64' ? Uint8Array.from(atob(data.content), function (c) { return c.charCodeAt(0); }) : new TextEncoder().encode(data.content); }
  // Each link below was matched to the named lesson and checked against the creator's video page.
  var CURATED_VIDEO = {
    'phases/01-math-foundations/01-linear-algebra-intuition/docs/en.md': ['Vectors | Essence of linear algebra', '3Blue1Brown', 'fNk_zzaMoSs'],
    'phases/01-math-foundations/02-vectors-matrices-operations/docs/en.md': ['Vectors | Essence of linear algebra', '3Blue1Brown', 'fNk_zzaMoSs'],
    'phases/08-generative-ai/03-gans-generator-discriminator/docs/en.md': ['Generative Adversarial Networks (GANs)', 'Computerphile', 'Sw9r8CL98N0'],
    'phases/05-nlp-foundations-to-advanced/19-subword-tokenization/docs/en.md': ["Let's build the GPT Tokenizer", 'Andrej Karpathy', 'zduSFxRajkE']
  };
  function lessonVideo(e) { var v=e&&CURATED_VIDEO[e.path]; return v ? '<a class="aic-button" target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/watch?v='+v[2]+'">▶ '+esc(v[0])+' · '+esc(v[1])+' ↗</a>' : ''; }
  function hero() {
    var c = catalog.counts;
    return '<header class="aic-hero">' +
      '<div style="margin-bottom:12px"><a href="' + base + 'ai_data.html" style="display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:700;color:var(--aic-accent,#7c3aed);text-decoration:none;padding:5px 12px;border-radius:6px;background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2)">← AI &amp; Data Hub</a></div>' +
      '<span class="aic-eyebrow">Learning Hub · AI engineering lessons</span><h1>AI Engineering from Scratch</h1>' +
      '<p>Read explanations and worked examples here, then practise with code and exercises. Follow the phases in order. Reference files and project plans are listed separately from lessons.</p>' +
      '<div class="aic-links">' + button('Roadmap', '#group=overview') + button('All topics', '#group=all') + button('Source files', '#files=') +
      button('Concept guide', base + 'AI_Engineering_Tutorial/concept-guide.html') + button('Original website ↗', catalog.source.website) + '</div>' +
      '<div class="aic-stats">' + [[c.phases,'phases'],[c.phase,'core lessons'],[c.subtopics,'indexed section headings'],[c.manuals,'manuals'],[c.practice,'practice labs'],[c.sourceFiles,'source files']].map(function (x) { return '<div class="aic-stat"><b>' + x[0].toLocaleString() + '</b><span>' + x[1] + '</span></div>'; }).join('') + '</div></header>';
  }
  function navigation() {
    var last = '';
    return '<nav class="aic-nav" id="aic-nav" aria-label="AI syllabus">&nbsp;<span class="aic-eyebrow">All phases</span><a href="#group=overview"' + (selected === 'overview' ? ' class="active"' : '') + '>Curriculum roadmap</a><a href="#group=all">Every study item <small>' + catalog.counts.entries + '</small></a>' + catalog.groups.map(function (g) {
      var label = '';
      if (last !== g.kind) { last = g.kind; label = '<h2>' + esc(g.kind) + '</h2>'; }
      return label + '<a href="#group=' + encodeURIComponent(g.id) + '"' + (selected === g.id ? ' class="active"' : '') + '><span>' + esc(g.title) + '</span><small>' + g.entries.length + '</small></a>';
    }).join('') + '<h2>Repository</h2><a href="#files=">Browse every source file</a></nav>';
  }
  function shell() {
    root.innerHTML = hero() + '<div class="aic-layout" id="aic-layout"><div class="aic-nav-wrap"><button class="aic-toggle" id="aic-nav-toggle" type="button" aria-controls="aic-nav"></button>' + navigation() + '</div>' + '<div class="aic-main" id="aic-main"></div></div>' +
      '<footer class="aic-footer">Adapted from <a href="' + esc(catalog.source.repository) + '">Rohit Ghumare and contributors’ AI Engineering from Scratch</a>, MIT licensed. ' +
      'Source snapshot <a href="' + esc(catalog.source.repository + '/tree/' + catalog.source.revision) + '">' + catalog.source.revision.slice(0,12) + '</a>. ' +
      '<a href="' + base + 'AI_Engineering_Tutorial/SOURCE_LICENSE.txt">Copyright and license</a> · <a href="' + base + 'AI_Engineering_Tutorial/coverage.json">Import coverage</a></footer>';
    var layout=document.getElementById('aic-layout'),nav=document.getElementById('aic-nav'),toggle=document.getElementById('aic-nav-toggle');
    function sync(){var value=closed(NAV_KEY);layout.classList.toggle('nav-closed',value);nav.hidden=value;toggle.textContent=value?'›':'‹';toggle.setAttribute('aria-label',value?'Show roadmap':'Hide roadmap');toggle.title=value?'Show roadmap':'Hide roadmap';toggle.setAttribute('aria-expanded',String(!value));}
    toggle.onclick=function(){localStorage.setItem(NAV_KEY,closed(NAV_KEY)?'0':'1');sync();};sync();
  }
  function toolbar(fileMode) {
    return '<div class="aic-toolbar"><input id="aic-search" type="search" aria-label="Search the complete syllabus" placeholder="' + (fileMode ? 'Search every source filename…' : 'Search every topic and subtopic…') + '" value="' + esc(query) + '">' +
      (!fileMode ? '<select id="aic-kind" aria-label="Filter material type"><option value="">All material</option>' + Array.from(new Set(catalog.groups.map(function (g) { return g.kind; }))).map(function (k) { return '<option' + (kind === k ? ' selected' : '') + '>' + k + '</option>'; }).join('') + '</select>' : '') + '</div><div id="aic-results"></div>';
  }
  function bindToolbar(render) {
    document.getElementById('aic-search').addEventListener('input', function (e) { query = e.target.value; pageNumber = 0; render(); });
    var select = document.getElementById('aic-kind');
    if (select) select.addEventListener('change', function (e) { kind = e.target.value; pageNumber = 0; render(); });
  }
  function pagination(count, size) {
    if (count <= size) return '';
    return '<div class="aic-pagination"><button class="aic-button" data-page="-1"' + (pageNumber === 0 ? ' disabled' : '') + '>Previous</button><span>' + (pageNumber + 1) + ' / ' + Math.ceil(count / size) + '</span><button class="aic-button" data-page="1"' + ((pageNumber + 1) * size >= count ? ' disabled' : '') + '>Next</button></div>';
  }
  function bindPagination(render) {
    root.querySelectorAll('[data-page]').forEach(function (b) { b.onclick = function () { pageNumber += Number(b.dataset.page); render(); document.getElementById('aic-main').scrollIntoView({block:'start'}); }; });
  }
  function card(e, done, saved) {
    var hs = e.headings.filter(function (h) { return h.level > 1; });
    return '<article class="aic-card' + (done.has(e.id) ? ' done' : '') + '"><div class="aic-card-head"><input type="checkbox" data-done="' + esc(e.id) + '" aria-label="Complete ' + esc(e.title) + '"' + (done.has(e.id) ? ' checked' : '') + '><div>' +
      '<span class="aic-badge">' + esc(e.kind + ' · ' + e.status) + '</span><h3><a href="' + route(e.contentPath) + '">' + esc(e.title) + '</a></h3><p>' + esc(e.summary) + '</p>' +
      '<div class="aic-actions">' + button(e.status==='planned'?'Read plan':'Open lesson', route(e.contentPath)) + (e.status==='planned'?'':button('Code & files', route(e.contentPath) + '&tab=files')) + (CURATED_VIDEO[e.path] ? lessonVideo(e) : e.videos.length ? '<button class="aic-button" data-watch="' + esc(e.id) + '">Watch ' + e.videos.length + '</button>' : '') + '<button class="aic-button" data-bookmark="'+esc(e.id)+'" aria-pressed="'+saved.has(e.id)+'">'+(saved.has(e.id)?'★ Saved':'☆ Save')+'</button></div></div></div>' +
      (e.kind==='phase' ? '<details class="aic-inline-lesson" data-inline-lesson="'+esc(e.contentPath)+'"><summary>Read explanation, worked examples & exercises here</summary><div class="aic-inline-body"></div></details>' : '') +
      (hs.length ? '<details><summary>Full syllabus · ' + hs.length + ' subtopics</summary><ol class="aic-syllabus">' + hs.map(function (h) { return '<li style="--level:' + (h.level - 2) + '"><a href="' + route(e.contentPath,h.anchor) + '">' + esc(h.title) + '</a></li>'; }).join('') + '</ol></details>' : '') + '</article>';
  }
  function bindCards() {
    root.querySelectorAll('[data-inline-lesson]').forEach(function(details){
      details.addEventListener('toggle',async function(){
        if(!details.open||details.dataset.loaded==='1')return;
        var host=details.querySelector('.aic-inline-body'),path=details.dataset.inlineLesson,e=entries.get(path);
        details.dataset.loaded='1';host.innerHTML='<p role="status">Loading lesson explanations…</p>';
        try{
          var loaded=await content(path);host.innerHTML='<article class="aic-article"></article>';
          renderMarkdown(host.querySelector('article'),loaded.data.content,path,e.path,e,'inline-'+Array.from(entries.keys()).indexOf(path)+'-');
        }catch(error){details.dataset.loaded='0';host.innerHTML='<p role="alert">'+esc(error.message)+'. Close and reopen this lesson to retry.</p>';}
      });
    });
    root.querySelectorAll('[data-done]').forEach(function (input) { input.onchange = function () { var d=doneSet(); if(input.checked)d.add(input.dataset.done);else d.delete(input.dataset.done);localStorage.setItem(DONE_KEY,JSON.stringify(Array.from(d)));input.closest('.aic-card').classList.toggle('done',input.checked); }; });
    root.querySelectorAll('[data-watch]').forEach(function (button) { button.onclick = function () { var e=entries.get(button.dataset.watch); if(window.VideoPanel)window.VideoPanel.open({title:e.title,query:e.title+' AI engineering',videos:e.videos,docs:[],originEl:button}); }; });
    root.querySelectorAll('[data-bookmark]').forEach(function(button){button.onclick=function(){var saved=bookmarks(),id=button.dataset.bookmark;if(saved.has(id))saved.delete(id);else saved.add(id);localStorage.setItem(BOOKMARK_KEY,JSON.stringify(Array.from(saved)));button.textContent=saved.has(id)?'★ Saved':'☆ Save';button.setAttribute('aria-pressed',String(saved.has(id)));};});
  }
  function renderItems() {
    var q=query.toLowerCase(), ids=groups.get(selected), done=doneSet(), saved=bookmarks();
    var list = catalog.entries.filter(function (e) {
      return (!kind || e.kind===kind) && (q || selected==='all' || !ids || ids.entries.indexOf(e.id)!==-1) &&
        (!q || (e.title+' '+e.summary+' '+e.headings.map(function(h){return h.title;}).join(' ')).toLowerCase().includes(q));
    });
    document.getElementById('aic-results').innerHTML = '<p class="aic-description">' + list.length.toLocaleString() + ' study items' + (q ? ' matching this search across the full curriculum' : '') + '</p><div class="aic-list">' + list.slice(pageNumber*40,(pageNumber+1)*40).map(function(e){return card(e,done,saved);}).join('') + '</div>' + pagination(list.length,40);
    bindCards();bindPagination(renderItems);
  }
  function overview() {
    document.getElementById('aic-main').innerHTML = toolbar(false);
    function render() {
      if(query || kind){renderItems();return;}
      document.getElementById('aic-results').innerHTML = '<section class="aic-start aic-card"><span class="aic-eyebrow">Start studying</span><h2>Explanations, examples and exercises</h2><p>Open a phase and expand a lesson to read it directly in the roadmap. The full lesson reader also includes a section-by-section contents list.</p>'+button('Begin the first lesson',route(catalog.entries.find(function(e){return e.kind==='phase';}).contentPath),' primary')+'</section><section class="aic-start aic-card"><span class="aic-eyebrow">Recommended additions</span><h2>Production evaluation topics to study next</h2><p>The source has related lessons, but no dedicated core lesson on experiment design or label leakage. Study controlled experiments, safe train/validation/test splitting, leakage checks, and feedback loops using the official course modules below.</p><div class="aic-actions"><a class="aic-button" href="https://developers.google.com/machine-learning/crash-course/production-ml-systems" target="_blank" rel="noopener noreferrer">Google: Production ML systems ↗</a><a class="aic-button" href="https://developers.google.com/machine-learning/crash-course/overfitting" target="_blank" rel="noopener noreferrer">Google: Generalization &amp; overfitting ↗</a></div></section><h2 class="aic-section-title">Learning roadmap</h2><p class="aic-description">Start with the twenty phases, then use the manuals, labs, projects and focused paths. Expand a core lesson to read its explanations, worked code and exercises without leaving this page.</p><div class="aic-grid">' + catalog.groups.map(function(g){return '<article class="aic-group"><span class="aic-badge">'+esc(g.kind)+' · '+g.entries.length+' items</span><h3><a href="#group='+encodeURIComponent(g.id)+'">'+esc(g.title)+'</a></h3><p>'+esc(g.description||'Complete topics, subtopics and source material.')+'</p>'+button('Explore','#group='+encodeURIComponent(g.id))+'</article>';}).join('')+'</div>';
    }
    bindToolbar(render);render();
  }
  async function fileBrowser(prefix, from) {
    await files();if(panelMode)window.parent.postMessage({type:'ai-reader-title',title:'Code & files'},location.origin);document.getElementById('aic-main').innerHTML=(from?'<div class="aic-actions">'+button('← Back to lesson',route(from))+'</div>':'')+'<h2 class="aic-section-title">Source files</h2><p class="aic-description">Every tracked file from the pinned repository is preserved locally. Code and HTML are displayed as source.</p>'+toolbar(true);
    function render(){
      var q=query.toLowerCase(), list=Object.keys(sourceIndex.files).filter(function(p){return !p.startsWith('@generated/')&&(!prefix||p.startsWith(prefix))&&p.toLowerCase().includes(q);}).sort();
      document.getElementById('aic-results').innerHTML='<p class="aic-description">'+list.length.toLocaleString()+' files'+(prefix?' in '+esc(prefix):'')+'</p><div class="aic-card">'+list.slice(pageNumber*100,(pageNumber+1)*100).map(function(p){return '<div class="aic-file"><a href="'+route(p)+(from?'&from='+encodeURIComponent(from):'')+'">'+esc(p)+'</a><small>'+formatBytes(sourceIndex.files[p].size)+'</small></div>';}).join('')+'</div>'+pagination(list.length,100);bindPagination(render);
    }bindToolbar(render);render();
  }
  function resolveSource(href,path){
    if(!href||/^(?:https?:|mailto:|data:|blob:|#)/i.test(href))return null;
    var u=new URL(href,'https://source.invalid/'+path);
    return {path:decodeURIComponent(u.pathname.slice(1)),hash:decodeURIComponent(u.hash.slice(1))};
  }
  function renderMarkdown(article,text,path,origin,e,idPrefix){
      article.innerHTML=DOMPurify.sanitize(marked.parse(text),{FORBID_TAGS:['script','style','form','input','button','iframe']});
      var seen={}, renderedHeads=article.querySelectorAll('h1,h2,h3,h4,h5,h6');renderedHeads.forEach(function(h,i){var s=slug(h.textContent);seen[s]=(seen[s]||0)+1;h.id=idPrefix+(e&&e.headings.length===renderedHeads.length?e.headings[i].anchor:s+(seen[s]>1?'-'+seen[s]:''));});
      article.querySelectorAll('a[href]').forEach(function(a){var href=a.getAttribute('href'), resolved=resolveSource(href,origin);if(resolved&&sourceIndex.files[resolved.path])a.href=route(resolved.path,resolved.hash);else if(resolved)a.href=new URL(href,catalog.source.website).href;else if(href&&href[0]==='#')a.href=route(path,href.slice(1));else {a.target='_blank';a.rel='noopener noreferrer';}});
      article.querySelectorAll('img[src]').forEach(async function(img){var r=resolveSource(img.getAttribute('src'),origin);if(r&&sourceIndex.files[r.path]){var v=await content(r.path);img.src=URL.createObjectURL(new Blob([bytesOf(v.data)],{type:v.record.mime}));}});
      article.querySelectorAll('pre code.language-figure').forEach(function(code){var note=document.createElement('p');note.className='aic-note';note.innerHTML='Interactive figure: '+esc(code.textContent.trim())+'. '+button('Open the original interactive lesson ↗',catalog.source.website+'lesson?path='+encodeURIComponent(origin.replace(/\/docs\/en\.md$/,'')));code.closest('pre').replaceWith(note);});
      article.querySelectorAll('pre code.language-math, pre code.language-latex, pre code.language-tex, pre code.language-katex').forEach(function(code){
        if(!window.katex)return;
        var equation=document.createElement('div');equation.className='aic-equation';equation.setAttribute('role','math');
        try{katex.render(code.textContent.trim(),equation,{displayMode:true,throwOnError:true,output:'htmlAndMathml'});code.closest('pre').replaceWith(equation);}
        catch(error){code.closest('pre').classList.add('aic-equation-source');}
      });
      if(window.hljs)article.querySelectorAll('pre code:not(.language-mermaid)').forEach(function(code){hljs.highlightElement(code);});
      if(window.renderMathInElement)renderMathInElement(article,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false},{left:'$',right:'$',display:false}],throwOnError:false});
  }
  function renderQuiz(article,data){
    article.innerHTML=data.questions.map(function(q,i){var multiple=Array.isArray(q.correct)&&q.correct.length>1;return '<section class="aic-card"><span class="aic-badge">Question '+(i+1)+(q.stage?' · '+esc(q.stage):'')+'</span><h3>'+esc(q.question||q.prompt||'Question')+'</h3><fieldset style="border:0;padding:0">'+(q.options||[]).map(function(option,j){return '<label style="display:block;padding:8px 0;cursor:pointer"><input type="'+(multiple?'checkbox':'radio')+'" name="quiz-'+i+'" value="'+j+'"> '+esc(typeof option==='string'?option:JSON.stringify(option))+'</label>';}).join('')+'</fieldset><button class="aic-button" data-check-question="'+i+'">Check answer</button><div data-question-answer="'+i+'" hidden class="aic-note"></div></section>';}).join('');
    article.querySelectorAll('[data-check-question]').forEach(function(button){button.onclick=function(){var i=Number(button.dataset.checkQuestion),q=data.questions[i],selected=Array.from(article.querySelectorAll('input[name="quiz-'+i+'"]:checked')).map(function(input){return Number(input.value);}),correct=Array.isArray(q.correct)?q.correct:[q.correct],ok=selected.length===correct.length&&selected.every(function(value){return correct.includes(value);}),answer=article.querySelector('[data-question-answer="'+i+'"]');answer.hidden=false;answer.innerHTML='<b>'+(ok?'Correct.':'Review the answer.')+'</b><p>'+esc(q.explanation||'')+'</p><p>Source answer: '+correct.map(function(n){return esc((q.options||[])[n]||n);}).join('; ')+'</p>';};});
  }
  async function reader(path, params, token) {
    var main=document.getElementById('aic-main'), e=entries.get(path), origin=e?e.path:path, context=entries.get(params.get('from'))||e;
    var g=context&&groups.get(context.group), prefix=origin.includes('/docs/')?origin.split('/docs/')[0]+'/':origin.slice(0,origin.lastIndexOf('/')+1);
    main.innerHTML='<p class="aic-description" role="status">Loading lesson explanations and examples…</p>';
    var loaded=await content(path);if(token!==routeToken)return;
    var sourceLink=sourceUrl(origin), displayTitle=e?e.title:path;
    var lessonNav='';
    if(context&&context.kind==='phase'&&g){
      var phaseEntries=g.entries, position=phaseEntries.indexOf(context.id), previous=position>0?entries.get(phaseEntries[position-1]):null, next=position<phaseEntries.length-1?entries.get(phaseEntries[position+1]):null;
      lessonNav='<section class="aic-phase-guide" aria-label="Lessons in this phase"><div class="aic-phase-heading"><span class="aic-eyebrow">'+esc(g.title)+'</span><span>Lesson '+(position+1)+' of '+phaseEntries.length+'</span></div><div class="aic-phase-step">'+(previous?button('← '+previous.title,route(previous.contentPath)):'<span>First lesson</span>')+(next?button(next.title+' →',route(next.contentPath),' primary'):'<span>Last lesson</span>')+'</div><details class="aic-phase-list" open><summary>All '+phaseEntries.length+' lessons in this phase</summary><ol>'+phaseEntries.map(function(id,i){var item=entries.get(id);return '<li'+(id===context.id?' class="current" aria-current="step"':'')+'><a href="'+route(item.contentPath)+'">'+(i+1)+'. '+esc(item.title)+'</a></li>';}).join('')+'</ol></details></section>';
    }
    main.innerHTML=lessonNav+'<div class="aic-actions">'+(params.get('from')&&params.get('from')!==path?button('← Back to lesson',route(params.get('from')))+button('← Files','#files='+encodeURIComponent(prefix)+'&from='+encodeURIComponent(params.get('from'))):button('← '+(g?g.title:'Source files'),g?'#group='+encodeURIComponent(g.id):'#files='))+button('GitHub source ↗',sourceUrl(origin))+(e&&e.originalSite?button('Original interactive guide ↗',e.originalSite):'')+lessonVideo(e)+'<button class="aic-button" id="aic-download">Download file</button>'+button('Files & code','#files='+encodeURIComponent(prefix)+'&from='+encodeURIComponent(params.get('from')||path))+'</div><h2 class="aic-section-title" style="margin-top:18px">'+esc(e?e.title:path)+'</h2>'+
      (e&&e.status==='planned'?'<p class="aic-note">This is planned upstream material. The source has no completed lesson or implementation yet.</p>':'')+
      '<p class="aic-description">'+esc(origin)+'</p><div class="aic-reading" id="aic-reading"><article class="aic-article" id="aic-article"></article><aside class="aic-toc-wrap"><button class="aic-toggle" id="aic-toc-toggle" type="button" aria-controls="aic-toc"></button><nav class="aic-toc" aria-label="Lesson sections" id="aic-toc"></nav></aside></div>';
    if(panelMode){var phaseList=main.querySelector('.aic-phase-list');if(phaseList)phaseList.open=false;}
    var reading=document.getElementById('aic-reading'),toc=document.getElementById('aic-toc'),tocToggle=document.getElementById('aic-toc-toggle');
    function syncToc(){var value=closed(TOC_KEY);reading.classList.toggle('toc-closed',value);toc.hidden=value;tocToggle.textContent=value?'‹':'›';tocToggle.setAttribute('aria-label',value?'Show lesson contents':'Hide lesson contents');tocToggle.title=value?'Show lesson contents':'Hide lesson contents';tocToggle.setAttribute('aria-expanded',String(!value));}
    tocToggle.onclick=function(){localStorage.setItem(TOC_KEY,closed(TOC_KEY)?'0':'1');syncToc();};syncToc();
    document.getElementById('aic-download').onclick=function(){var blob=new Blob([bytesOf(loaded.data)],{type:loaded.record.mime});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=path.split('/').pop();a.click();setTimeout(function(){URL.revokeObjectURL(a.href);},1000);};
    var article=document.getElementById('aic-article');
    var quiz=null;if(/\.json$/i.test(path)&&loaded.data.encoding==='utf8'){try{quiz=JSON.parse(loaded.data.content);}catch(_){/* Invalid fixtures remain readable as source. */}}
    if(loaded.data.encoding==='base64'){
      if(loaded.record.mime.startsWith('image/')){var img=document.createElement('img');img.alt=displayTitle;img.src=URL.createObjectURL(new Blob([bytesOf(loaded.data)],{type:loaded.record.mime}));article.appendChild(img);}
      else article.innerHTML='<p>This binary source file is preserved in the snapshot. Use Download file to save it.</p>';
    }else if(/\.md$/i.test(path)){
      renderMarkdown(article,loaded.data.content,path,origin,e,'aic-');
      var hs=Array.from(article.querySelectorAll('h2,h3,h4,h5,h6'));document.getElementById('aic-toc').innerHTML='<span class="aic-eyebrow">In this lesson</span>'+hs.map(function(h){return '<a href="'+route(path,h.id.slice(4))+'">'+esc(h.textContent)+'</a>';}).join('');
    }else if(quiz&&Array.isArray(quiz.questions)&&quiz.questions.length&&quiz.questions.every(function(q){return Array.isArray(q.options)&&q.correct!=null;})){
      renderQuiz(article,quiz);
    }else{
      var pre=document.createElement('pre'), code=document.createElement('code');code.textContent=loaded.data.content;pre.appendChild(code);article.appendChild(pre);if(window.hljs)hljs.highlightElement(code);
    }
    if(panelMode)window.parent.postMessage({type:'ai-reader-title',title:displayTitle},location.origin);
    if(params.get('tab')==='files'){location.hash='files='+encodeURIComponent(prefix)+'&from='+encodeURIComponent(path);return;}
    var section=params.get('section');if(section){var target=document.getElementById('aic-'+section);if(target)target.scrollIntoView({block:'start'});}
    else main.scrollIntoView({block:'start'});
  }
  async function navigate(){
    var raw=location.hash.slice(1);
    if(raw&&!/^(?:read|group|files)=/.test(raw)){
      var old=await fetch(base+'AI_Engineering_Tutorial/legacy-routes.json?v='+release).then(function(r){return r.json();});
      if(old[raw]){location.replace(route(old[raw]));return;}
      var phase=raw.match(/^phase-\d+/);if(phase){location.replace('#group='+phase[0]);return;}
    }
    var token=++routeToken, params=new URLSearchParams(location.hash.slice(1));query='';pageNumber=0;kind='';selected=params.get('group')||'overview';if(params.has('read')&&entries.has(params.get('read')))selected=entries.get(params.get('read')).group;shell();
    try{
      if(params.has('read'))await reader(params.get('read'),params,token);
      else if(params.has('files'))await fileBrowser(params.get('files'),params.get('from'));
      else if(selected==='overview')overview();
      else{var g=groups.get(selected);document.getElementById('aic-main').innerHTML='<h2 class="aic-section-title">'+esc(g?g.title:'Every study item')+'</h2><p class="aic-description">'+esc(g&&g.description||'Search and study the complete imported curriculum.')+'</p>'+toolbar(false);bindToolbar(renderItems);renderItems();}
    }catch(error){document.getElementById('aic-main').innerHTML='<div class="aic-note">'+esc(error.message)+'</div>';}
  }
  function setupReaderPanel(){
    if(panelMode)return;
    var pane=document.createElement('section');pane.className='aic-reader-panel';pane.id='aic-reader-panel';pane.hidden=true;
    pane.innerHTML='<header class="aic-reader-bar"><strong id="aic-reader-title">Lesson</strong><div class="aic-reader-tools"><label class="aic-reader-width">Width <input id="aic-reader-width" type="range" min="40" max="90" value="60" aria-label="Reader panel width"></label><button type="button" id="aic-site-theme" aria-label="Change site theme">Site: Light</button><button type="button" id="aic-reader-theme" aria-label="Change reader theme">Reader: Light</button><button type="button" id="aic-reader-dock" aria-label="Move reader to left" title="Move reader to left">⇄</button><button type="button" id="aic-reader-expand" aria-label="Expand reader" title="Expand reader">⛶</button><button type="button" id="aic-reader-minimize" aria-label="Minimize reader" title="Minimize reader">›</button><button type="button" id="aic-reader-close" aria-label="Close reader" title="Close reader">×</button></div></header><iframe id="aic-reader-frame" title="AI lesson reader"></iframe>';
    document.body.appendChild(pane);
    var frame=pane.querySelector('iframe'),lastFocus=null,themeOrder=['light','dark','black'],readerThemeKey='hub_ai_reader_theme_v1';
    function readerTheme(){var value=localStorage.getItem(readerThemeKey);return themeOrder.includes(value)?value:(document.documentElement.getAttribute('data-theme')||'light');}
    function applyReaderTheme(){
      var value=readerTheme();pane.setAttribute('data-reader-theme',value);pane.querySelector('#aic-reader-theme').textContent='Reader: '+value[0].toUpperCase()+value.slice(1);
      if(!frame.contentDocument||frame.contentWindow.location.href==='about:blank')return;
      var root=frame.contentDocument.documentElement;
      root.classList.toggle('light',value==='light');root.classList.toggle('dark',value!=='light');root.classList.toggle('black',value==='black');root.setAttribute('data-theme',value);
    }
    function syncSiteTheme(){var value=document.documentElement.getAttribute('data-theme')||'light';pane.querySelector('#aic-site-theme').textContent='Site: '+value[0].toUpperCase()+value.slice(1);}
    var savedWidth=Number(localStorage.getItem('hub_ai_reader_width_v1'));
    if(savedWidth>=40&&savedWidth<=90)pane.querySelector('#aic-reader-width').value=String(savedWidth);
    function syncLayout(){
      var width=pane.querySelector('#aic-reader-width').value+'vw';
      document.body.style.setProperty('--aic-reader-width',width);
      document.body.classList.toggle('aic-reader-minimized',!pane.hidden&&pane.classList.contains('minimized'));
      document.body.classList.toggle('aic-reader-expanded',!pane.hidden&&pane.classList.contains('expanded'));
      document.body.classList.toggle('aic-reader-dock-left',!pane.hidden&&pane.classList.contains('dock-left'));
    }
    syncLayout();
    frame.addEventListener('load',applyReaderTheme);
    window.addEventListener('learning-hub-theme',syncSiteTheme);syncSiteTheme();
    function close(){pane.hidden=true;frame.src='about:blank';document.body.classList.remove('aic-reader-open');syncLayout();if(lastFocus&&lastFocus.isConnected)lastFocus.focus();}
    pane.querySelector('#aic-reader-close').onclick=close;
    pane.querySelector('#aic-site-theme').onclick=function(){var button=document.querySelector('.hub-nav [data-hub-theme]');if(button)button.click();syncSiteTheme();};
    pane.querySelector('#aic-reader-theme').onclick=function(){var value=readerTheme();localStorage.setItem(readerThemeKey,themeOrder[(themeOrder.indexOf(value)+1)%themeOrder.length]);applyReaderTheme();};
    pane.querySelector('#aic-reader-width').oninput=function(){localStorage.setItem('hub_ai_reader_width_v1',this.value);pane.classList.remove('expanded','minimized');syncLayout();};
    pane.querySelector('#aic-reader-dock').onclick=function(){pane.classList.toggle('dock-left');syncLayout();this.setAttribute('aria-label',pane.classList.contains('dock-left')?'Move reader to right':'Move reader to left');};
    pane.querySelector('#aic-reader-expand').onclick=function(){pane.classList.remove('minimized');pane.classList.toggle('expanded');syncLayout();this.setAttribute('aria-label',pane.classList.contains('expanded')?'Restore reader width':'Expand reader');};
    pane.querySelector('#aic-reader-minimize').onclick=function(){pane.classList.toggle('minimized');var value=pane.classList.contains('minimized');syncLayout();this.textContent=value?(pane.classList.contains('dock-left')?'›':'‹'):'›';this.setAttribute('aria-label',value?'Restore reader':'Minimize reader');this.title=value?'Restore reader':'Minimize reader';};
    window.addEventListener('message',function(e){if(e.origin===location.origin&&e.source===frame.contentWindow&&e.data&&e.data.type==='ai-reader-title')pane.querySelector('#aic-reader-title').textContent=e.data.title;});
    root.addEventListener('click',function(e){var a=e.target.closest('a[href]');if(!a)return;var href=a.getAttribute('href');if(!href||!/^#(?:read|files)=/.test(href))return;e.preventDefault();lastFocus=a;pane.hidden=false;pane.classList.remove('minimized');document.body.classList.add('aic-reader-open');syncLayout();pane.querySelector('#aic-reader-title').textContent='Loading lesson…';frame.src=base+'AI_Engineering_Tutorial/reader.html?panel=1&v='+release+href;});
  }
  async function init(){root=document.getElementById('ai-curriculum');try{var response=await fetch(base+'AI_Engineering_Tutorial/catalog.json?v='+release);if(!response.ok)throw Error('Curriculum catalogue could not load');catalog=await response.json();entries=new Map(catalog.entries.map(function(e){return[e.contentPath,e];}));groups=new Map(catalog.groups.map(function(g){return[g.id,g];}));window.addEventListener('hashchange',navigate);setupReaderPanel();await navigate();}catch(error){root.innerHTML='<h1>AI Engineering</h1><p>'+esc(error.message)+'</p>';}}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
}());
