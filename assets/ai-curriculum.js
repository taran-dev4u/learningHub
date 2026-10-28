/* Full MIT curriculum snapshot: lazy content packs, syllabus and source reader. */
(function () {
  'use strict';
  var script = document.currentScript;
  var base = new URL('../', script.src).href;
  var root, catalog, sourceIndex, entries, groups, packs = new Map(), filePromise;
  var query = '', kind = '', pageNumber = 0, selected = 'overview', routeToken = 0;
  var DONE_KEY = 'hub_done_ai_source_v1';
  function doneSet() { try { return new Set(JSON.parse(localStorage.getItem(DONE_KEY) || '[]')); } catch (_) { return new Set(); } }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function route(path, section) { return '#read=' + encodeURIComponent(path) + (section ? '&section=' + encodeURIComponent(section) : ''); }
  function sourceUrl(path) { return catalog.source.repository + '/blob/' + catalog.source.revision + '/' + path.split('/').map(encodeURIComponent).join('/'); }
  function formatBytes(n) { return n > 1e6 ? (n / 1e6).toFixed(1) + ' MB' : n > 1000 ? Math.round(n / 1000) + ' KB' : n + ' B'; }
  function button(label, href, extra) { return '<a class="aic-button' + (extra || '') + '" href="' + esc(href) + '">' + esc(label) + '</a>'; }
  function slug(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'section'; }
  async function files() {
    if (!filePromise) filePromise = fetch(base + 'AI_Engineering_Tutorial/source/index.json').then(function (r) { if (!r.ok) throw Error('Source index could not load'); return r.json(); }).then(function (d) { sourceIndex = d; return d; });
    return filePromise;
  }
  async function content(path) {
    var index = await files(), record = index.files[path];
    if (!record) throw Error('This source file is not in the imported snapshot: ' + path);
    if (!packs.has(record.pack)) packs.set(record.pack, fetch(base + 'AI_Engineering_Tutorial/' + record.pack).then(async function (r) {
      if (!r.ok) throw Error('Source content could not load');
      var bytes = new Uint8Array(await r.arrayBuffer());
      if (bytes[0] === 31 && bytes[1] === 139) {
        var stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
        return JSON.parse(await new Response(stream).text());
      }
      return JSON.parse(new TextDecoder().decode(bytes));
    }));
    var pack = await packs.get(record.pack), data = pack[record.hash];
    if (!data) throw Error('Source pack is missing a file');
    return { record: record, data: data };
  }
  function bytesOf(data) { return data.encoding === 'base64' ? Uint8Array.from(atob(data.content), function (c) { return c.charCodeAt(0); }) : new TextEncoder().encode(data.content); }
  function hero() {
    var c = catalog.counts;
    return '<header class="aic-hero"><span class="aic-eyebrow">Learning Hub · complete source curriculum</span><h1>AI Engineering from Scratch</h1>' +
      '<p>Learn from the original lessons, every topic and subtopic, code, quizzes, manuals and practice files. Follow the phases in order or choose a focused learning path.</p>' +
      '<div class="aic-links">' + button('Roadmap', '#group=overview') + button('All topics', '#group=all') + button('Source files', '#files=') +
      button('Concept guide', base + 'AI_Engineering_Tutorial/concept-guide.html') + button('Original website ↗', catalog.source.website) + '</div>' +
      '<div class="aic-stats">' + [[c.phases,'phases'],[c.phase,'core lessons'],[c.subtopics,'subtopics / headings'],[c.manuals,'manuals'],[c.practice,'practice labs'],[c.sourceFiles,'source files']].map(function (x) { return '<div class="aic-stat"><b>' + x[0].toLocaleString() + '</b><span>' + x[1] + '</span></div>'; }).join('') + '</div></header>';
  }
  function navigation() {
    var last = '';
    return '<nav class="aic-nav" aria-label="AI syllabus"><a href="#group=overview"' + (selected === 'overview' ? ' class="active"' : '') + '>Curriculum roadmap</a><a href="#group=all">Every study item <small>' + catalog.counts.entries + '</small></a>' + catalog.groups.map(function (g) {
      var label = '';
      if (last !== g.kind) { last = g.kind; label = '<h2>' + esc(g.kind) + '</h2>'; }
      return label + '<a href="#group=' + encodeURIComponent(g.id) + '"' + (selected === g.id ? ' class="active"' : '') + '><span>' + esc(g.title) + '</span><small>' + g.entries.length + '</small></a>';
    }).join('') + '<h2>Repository</h2><a href="#files=">Browse every source file</a></nav>';
  }
  function shell() {
    root.innerHTML = hero() + '<div class="aic-layout">' + navigation() + '<div class="aic-main" id="aic-main"></div></div>' +
      '<footer class="aic-footer">Adapted from <a href="' + esc(catalog.source.repository) + '">Rohit Ghumare and contributors’ AI Engineering from Scratch</a>, MIT licensed. ' +
      'Source snapshot <a href="' + esc(catalog.source.repository + '/tree/' + catalog.source.revision) + '">' + catalog.source.revision.slice(0,12) + '</a>. ' +
      '<a href="' + base + 'AI_Engineering_Tutorial/SOURCE_LICENSE.txt">Copyright and license</a> · <a href="' + base + 'AI_Engineering_Tutorial/coverage.json">Import coverage</a></footer>';
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
  function card(e, done) {
    var hs = e.headings.filter(function (h) { return h.level > 1; });
    return '<article class="aic-card' + (done.has(e.id) ? ' done' : '') + '"><div class="aic-card-head"><input type="checkbox" data-done="' + esc(e.id) + '" aria-label="Complete ' + esc(e.title) + '"' + (done.has(e.id) ? ' checked' : '') + '><div>' +
      '<span class="aic-badge">' + esc(e.kind + ' · ' + e.status) + '</span><h3><a href="' + route(e.contentPath) + '">' + esc(e.title) + '</a></h3><p>' + esc(e.summary) + '</p>' +
      '<div class="aic-actions">' + button('Read', route(e.contentPath)) + button('Code & files', route(e.contentPath) + '&tab=files') + (e.videos.length ? '<button class="aic-button" data-watch="' + esc(e.id) + '">Watch ' + e.videos.length + '</button>' : '') + '</div></div></div>' +
      (hs.length ? '<details><summary>Full syllabus · ' + hs.length + ' subtopics</summary><ol class="aic-syllabus">' + hs.map(function (h) { return '<li style="--level:' + (h.level - 2) + '"><a href="' + route(e.contentPath,h.anchor) + '">' + esc(h.title) + '</a></li>'; }).join('') + '</ol></details>' : '') + '</article>';
  }
  function bindCards() {
    root.querySelectorAll('[data-done]').forEach(function (input) { input.onchange = function () { var d=doneSet(); if(input.checked)d.add(input.dataset.done);else d.delete(input.dataset.done);localStorage.setItem(DONE_KEY,JSON.stringify(Array.from(d)));input.closest('.aic-card').classList.toggle('done',input.checked); }; });
    root.querySelectorAll('[data-watch]').forEach(function (button) { button.onclick = function () { var e=entries.get(button.dataset.watch); if(window.VideoPanel)window.VideoPanel.open({title:e.title,query:e.title+' AI engineering',videos:e.videos,docs:[],originEl:button}); }; });
  }
  function renderItems() {
    var q=query.toLowerCase(), ids=groups.get(selected), done=doneSet();
    var list = catalog.entries.filter(function (e) {
      return (!kind || e.kind===kind) && (q || selected==='all' || !ids || ids.entries.indexOf(e.id)!==-1) &&
        (!q || (e.title+' '+e.summary+' '+e.headings.map(function(h){return h.title;}).join(' ')).toLowerCase().includes(q));
    });
    document.getElementById('aic-results').innerHTML = '<p class="aic-description">' + list.length.toLocaleString() + ' study items' + (q ? ' matching this search across the full curriculum' : '') + '</p><div class="aic-list">' + list.slice(pageNumber*40,(pageNumber+1)*40).map(function(e){return card(e,done);}).join('') + '</div>' + pagination(list.length,40);
    bindCards();bindPagination(renderItems);
  }
  function overview() {
    document.getElementById('aic-main').innerHTML = toolbar(false);
    function render() {
      if(query || kind){renderItems();return;}
      document.getElementById('aic-results').innerHTML = '<h2 class="aic-section-title">Your complete learning roadmap</h2><p class="aic-description">Start with the twenty phases, then use the manuals, labs, projects and focused paths. Every lesson opens its original complete content.</p><div class="aic-grid">' + catalog.groups.map(function(g){return '<article class="aic-group"><span class="aic-badge">'+esc(g.kind)+' · '+g.entries.length+' items</span><h3><a href="#group='+encodeURIComponent(g.id)+'">'+esc(g.title)+'</a></h3><p>'+esc(g.description||'Complete topics, subtopics and source material.')+'</p>'+button('Explore','#group='+encodeURIComponent(g.id))+'</article>';}).join('')+'</div>';
    }
    bindToolbar(render);render();
  }
  async function fileBrowser(prefix) {
    await files();document.getElementById('aic-main').innerHTML='<h2 class="aic-section-title">Source files</h2><p class="aic-description">Every tracked file from the pinned repository is preserved locally. Code and HTML are displayed as source.</p>'+toolbar(true);
    function render(){
      var q=query.toLowerCase(), list=Object.keys(sourceIndex.files).filter(function(p){return !p.startsWith('@generated/')&&(!prefix||p.startsWith(prefix))&&p.toLowerCase().includes(q);}).sort();
      document.getElementById('aic-results').innerHTML='<p class="aic-description">'+list.length.toLocaleString()+' files'+(prefix?' in '+esc(prefix):'')+'</p><div class="aic-card">'+list.slice(pageNumber*100,(pageNumber+1)*100).map(function(p){return '<div class="aic-file"><a href="'+route(p)+'">'+esc(p)+'</a><small>'+formatBytes(sourceIndex.files[p].size)+'</small></div>';}).join('')+'</div>'+pagination(list.length,100);bindPagination(render);
    }bindToolbar(render);render();
  }
  function resolveSource(href,path){
    if(!href||/^(?:https?:|mailto:|data:|blob:|#)/i.test(href))return null;
    var u=new URL(href,'https://source.invalid/'+path);
    return {path:decodeURIComponent(u.pathname.slice(1)),hash:decodeURIComponent(u.hash.slice(1))};
  }
  async function reader(path, params, token) {
    var main=document.getElementById('aic-main'), e=entries.get(path), origin=e?e.path:path;
    var g=e&&groups.get(e.group), prefix=origin.includes('/docs/')?origin.split('/docs/')[0]+'/':origin.slice(0,origin.lastIndexOf('/')+1);
    main.innerHTML='<p class="aic-description">Loading complete source…</p>';
    var loaded=await content(path);if(token!==routeToken)return;
    var sourceLink=sourceUrl(origin), displayTitle=e?e.title:path;
    main.innerHTML='<div class="aic-actions">'+button('← '+(g?g.title:'Source files'),g?'#group='+encodeURIComponent(g.id):'#files=')+button('GitHub source ↗',sourceLink)+'<button class="aic-button" id="aic-download">Download file</button>'+button('Files & code','#files='+encodeURIComponent(prefix))+'</div><h2 class="aic-section-title" style="margin-top:18px">'+esc(displayTitle)+'</h2>'+
      (e&&e.status==='planned'?'<p class="aic-note">This is planned upstream material. The source has no completed lesson or implementation yet.</p>':'')+
      '<p class="aic-description">'+esc(origin)+'</p><div class="aic-reading"><article class="aic-article" id="aic-article"></article><nav class="aic-toc" aria-label="Lesson sections" id="aic-toc"></nav></div>';
    document.getElementById('aic-download').onclick=function(){var blob=new Blob([bytesOf(loaded.data)],{type:loaded.record.mime});var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=path.split('/').pop();a.click();setTimeout(function(){URL.revokeObjectURL(a.href);},1000);};
    var article=document.getElementById('aic-article');
    if(loaded.data.encoding==='base64'){
      if(loaded.record.mime.startsWith('image/')){var img=document.createElement('img');img.alt=displayTitle;img.src=URL.createObjectURL(new Blob([bytesOf(loaded.data)],{type:loaded.record.mime}));article.appendChild(img);}
      else article.innerHTML='<p>This binary source file is preserved in the snapshot. Use Download file to save it.</p>';
    }else if(/\.md$/i.test(path)){
      article.innerHTML=DOMPurify.sanitize(marked.parse(loaded.data.content));
      var seen={};article.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(function(h){var s=slug(h.textContent);seen[s]=(seen[s]||0)+1;h.id='aic-'+s+(seen[s]>1?'-'+seen[s]:'');});
      article.querySelectorAll('a[href]').forEach(function(a){var href=a.getAttribute('href'), resolved=resolveSource(href,origin);if(resolved&&sourceIndex.files[resolved.path])a.href=route(resolved.path,resolved.hash);else if(resolved)a.href=new URL(href,catalog.source.website).href;else if(href&&href[0]==='#')a.href=route(path,href.slice(1));else {a.target='_blank';a.rel='noopener noreferrer';}});
      article.querySelectorAll('img[src]').forEach(async function(img){var r=resolveSource(img.getAttribute('src'),origin);if(r&&sourceIndex.files[r.path]){var v=await content(r.path);img.src=URL.createObjectURL(new Blob([bytesOf(v.data)],{type:v.record.mime}));}});
      article.querySelectorAll('pre code.language-figure').forEach(function(code){var note=document.createElement('p');note.className='aic-note';note.innerHTML='Interactive figure: '+esc(code.textContent.trim())+'. '+button('Open the original interactive lesson ↗',catalog.source.website+'lesson?path='+encodeURIComponent(origin.replace(/\/docs\/en\.md$/,'')));code.closest('pre').replaceWith(note);});
      if(window.hljs)article.querySelectorAll('pre code:not(.language-mermaid)').forEach(function(code){hljs.highlightElement(code);});
      if(window.renderMathInElement)renderMathInElement(article,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false},{left:'$',right:'$',display:false}],throwOnError:false});
      var hs=Array.from(article.querySelectorAll('h2,h3,h4,h5,h6'));document.getElementById('aic-toc').innerHTML='<span class="aic-eyebrow">In this lesson</span>'+hs.map(function(h){return '<a href="'+route(path,h.id.slice(4))+'">'+esc(h.textContent)+'</a>';}).join('');
    }else{
      var pre=document.createElement('pre'), code=document.createElement('code');code.textContent=loaded.data.content;pre.appendChild(code);article.appendChild(pre);if(window.hljs)hljs.highlightElement(code);
    }
    if(params.get('tab')==='files'){location.hash='files='+encodeURIComponent(prefix);return;}
    var section=params.get('section');if(section){var target=document.getElementById('aic-'+section);if(target)target.scrollIntoView({block:'start'});}
    else main.scrollIntoView({block:'start'});
  }
  async function navigate(){
    var token=++routeToken, params=new URLSearchParams(location.hash.slice(1));query='';pageNumber=0;kind='';selected=params.get('group')||'overview';shell();
    try{
      if(params.has('read'))await reader(params.get('read'),params,token);
      else if(params.has('files'))await fileBrowser(params.get('files'));
      else if(selected==='overview')overview();
      else{var g=groups.get(selected);document.getElementById('aic-main').innerHTML='<h2 class="aic-section-title">'+esc(g?g.title:'Every study item')+'</h2><p class="aic-description">'+esc(g&&g.description||'Search and study the complete imported curriculum.')+'</p>'+toolbar(false);bindToolbar(renderItems);renderItems();}
    }catch(error){document.getElementById('aic-main').innerHTML='<div class="aic-note">'+esc(error.message)+'</div>';}
  }
  async function init(){root=document.getElementById('ai-curriculum');try{var response=await fetch(base+'AI_Engineering_Tutorial/catalog.json');if(!response.ok)throw Error('Curriculum catalogue could not load');catalog=await response.json();entries=new Map(catalog.entries.map(function(e){return[e.contentPath,e];}));groups=new Map(catalog.groups.map(function(g){return[g.id,g];}));window.addEventListener('hashchange',navigate);await navigate();}catch(error){root.innerHTML='<h1>AI Engineering</h1><p>'+esc(error.message)+'</p>';}}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
}());
