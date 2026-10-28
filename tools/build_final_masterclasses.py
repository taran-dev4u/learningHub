import os
import sys
import tempfile
import time
import re
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def atomic_write(filepath, content):
    d = os.path.dirname(os.path.abspath(filepath))
    with tempfile.NamedTemporaryFile('w', dir=d, delete=False, encoding='utf-8') as tf:
        tf.write(content)
        temp_name = tf.name
    for attempt in range(4):
        try:
            os.replace(temp_name, filepath)
            break
        except OSError:
            if attempt == 3: raise
            time.sleep(0.1 * (attempt + 1))
    if os.path.exists(temp_name):
        try: os.unlink(temp_name)
        except OSError: pass

# Read base CSS from cloud_aws_azure.html
with open(os.path.join(ROOT, 'cloud_aws_azure.html'), 'r', encoding='utf-8') as f:
    cloud_html = f.read()

with open(os.path.join(ROOT, 'all_tech.html'), 'r', encoding='utf-8') as f:
    tech_html = f.read()

style_m = re.search(r'<style>([\s\S]*?)</style>', cloud_html)
base_css = style_m.group(1) if style_m else ""

soup_cloud = BeautifulSoup(cloud_html, 'html.parser')
soup_tech = BeautifulSoup(tech_html, 'html.parser')

sec_azure = soup_cloud.find('section', id='section-2')
sec_gcp = soup_cloud.find('section', id='section-3')
sec_spark = soup_tech.find('section', id='section-11')

STANDALONE_JS = """
(function() {
  const SLUG = window.SITE_SLUG || 'cloud';
  const KEY_DONE = 'hub_done_' + SLUG;
  const KEY_BM = 'hub_bm_' + SLUG;

  let doneSet = new Set();
  try {
    const raw = localStorage.getItem(KEY_DONE);
    if (raw) doneSet = new Set(JSON.parse(raw));
  } catch (e) {}

  let bmSet = new Set();
  try {
    const raw = localStorage.getItem(KEY_BM);
    if (raw) bmSet = new Set(JSON.parse(raw));
  } catch (e) {}

  function saveDone() {
    try { localStorage.setItem(KEY_DONE, JSON.stringify([...doneSet])); } catch (e) {}
  }
  function saveBm() {
    try { localStorage.setItem(KEY_BM, JSON.stringify([...bmSet])); } catch (e) {}
  }

  function updateProgress() {
    const all = document.querySelectorAll('li[data-cid]');
    const total = all.length;
    let done = 0;
    all.forEach(li => {
      const cid = li.getAttribute('data-cid');
      const isDone = doneSet.has(cid);
      li.classList.toggle('done', isDone);
      li.classList.toggle('is-done', isDone);
      const chk = li.querySelector('.done-check');
      if (chk) {
        chk.classList.toggle('checked', isDone);
        chk.innerHTML = isDone ? '✓' : '';
      }
      if (isDone) done++;
      const isBm = bmSet.has(cid);
      li.classList.toggle('is-bm', isBm);
      const star = li.querySelector('.bookmark-star');
      if (star) {
        star.classList.toggle('active', isBm);
        star.textContent = isBm ? '★' : '☆';
      }
    });
    const pct = total ? Math.round((done / total) * 100) : 0;
    const bar = document.getElementById('overall-bar');
    if (bar) bar.style.width = pct + '%';
    const txt = document.getElementById('overall-pct');
    if (txt) txt.textContent = done + ' / ' + total + ' (' + pct + '%)';
  }

  document.querySelectorAll('li[data-cid]').forEach(li => {
    const cid = li.getAttribute('data-cid');
    const chk = li.querySelector('.done-check');
    if (chk) {
      chk.addEventListener('click', (e) => {
        e.stopPropagation();
        if (doneSet.has(cid)) doneSet.delete(cid);
        else doneSet.add(cid);
        saveDone();
        updateProgress();
      });
    }
    const star = li.querySelector('.bookmark-star');
    if (star) {
      star.addEventListener('click', (e) => {
        e.stopPropagation();
        if (bmSet.has(cid)) bmSet.delete(cid);
        else bmSet.add(cid);
        saveBm();
        updateProgress();
      });
    }
  });

  let activeFilter = null;
  document.querySelectorAll('.filter-btn[data-filter]').forEach(b => {
    b.addEventListener('click', () => {
      const val = b.getAttribute('data-val');
      if (activeFilter === val) {
        activeFilter = null;
        b.classList.remove('active');
      } else {
        document.querySelectorAll('.filter-btn[data-filter]').forEach(x => x.classList.remove('active'));
        activeFilter = val;
        b.classList.add('active');
      }
      applyFilters();
    });
  });

  const sInput = document.getElementById('search-input');
  if (sInput) sInput.addEventListener('input', applyFilters);

  const clearBtn = document.getElementById('clear-filters');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      activeFilter = null;
      document.querySelectorAll('.filter-btn').forEach(x => x.classList.remove('active'));
      if (sInput) sInput.value = '';
      applyFilters();
    });
  }

  function applyFilters() {
    const q = (sInput ? sInput.value : '').toLowerCase().trim();
    document.querySelectorAll('li[data-cid]').forEach(li => {
      const cid = li.getAttribute('data-cid');
      const text = (li.getAttribute('data-name') || li.textContent).toLowerCase();
      let match = true;
      if (activeFilter === 'done' && !doneSet.has(cid)) match = false;
      if (activeFilter === 'undone' && doneSet.has(cid)) match = false;
      if (activeFilter === 'bookmarked' && !bmSet.has(cid)) match = false;
      if (q && !text.includes(q)) match = false;
      li.style.display = match ? '' : 'none';
    });
  }

  const randBtn = document.getElementById('random-btn');
  if (randBtn) {
    randBtn.addEventListener('click', () => {
      const all = Array.from(document.querySelectorAll('li[data-cid]')).filter(li => li.style.display !== 'none');
      if (!all.length) return;
      const pick = all[Math.floor(Math.random() * all.length)];
      pick.scrollIntoView({ behavior: 'smooth', block: 'center' });
      pick.style.outline = '3px solid var(--accent)';
      setTimeout(() => { pick.style.outline = ''; }, 2000);
    });
  }

  updateProgress();
})();
"""

SISTER_CARDS_HTML = """
  <div class="sister-guides-card">
    <div class="sister-title">🚀 Complete Engineering &amp; Cloud Masterclasses</div>
    <div class="sister-grid">
      <a class="sister-link" href="tech_aws.html">☁️ AWS Cloud</a>
      <a class="sister-link" href="tech_azure.html">🔷 Microsoft Azure</a>
      <a class="sister-link" href="tech_gcp.html">🌐 Google Cloud Platform</a>
      <a class="sister-link" href="tech_linux.html">🐧 Linux &amp; CLI</a>
      <a class="sister-link" href="tech_git.html">🌿 Git &amp; GitHub</a>
      <a class="sister-link" href="tech_docker_k8s.html">🐳 Docker &amp; Kubernetes</a>
      <a class="sister-link" href="tech_cicd.html">🚀 CI/CD Pipelines</a>
      <a class="sister-link" href="tech_terraform.html">🏗️ Terraform IaC</a>
      <a class="sister-link" href="tech_kafka.html">⚡ Apache Kafka</a>
      <a class="sister-link" href="tech_spark.html">📊 Apache Spark</a>
      <a class="sister-link" href="tech_postgres.html">🐘 PostgreSQL</a>
      <a class="sister-link" href="tech_redis.html">🔴 Redis Caching</a>
      <a class="sister-link" href="tech_java.html">☕ Java &amp; Spring Boot</a>
      <a class="sister-link" href="tech_fastapi.html">🐍 Python &amp; FastAPI</a>
      <a class="sister-link" href="tech_apis.html">🔌 Production APIs</a>
      <a class="sister-link active-hub" href="cloud_aws_azure.html">☁️ Cloud Platforms Hub &rarr;</a>
      <a class="sister-link active-hub" href="all_tech.html">🌐 All-in-One Tech Portal &rarr;</a>
    </div>
  </div>
"""

def generate_masterclass_page(filename, title, subtitle, badge, parent_hub_url, parent_hub_label, sec_soup):
    subs = sec_soup.find_all('div', class_='subsection')
    concepts = sec_soup.find_all('li', attrs={'data-cid': True})
    total_subs = len(subs)
    total_concepts = len(concepts)

    # Clean up section soup for standalone page
    sec_html = str(sec_soup)
    # Remove any focus bar from inside the section
    sec_html = re.sub(r'<div class="domain-focus-bar">[\s\S]*?</div>\s*', '', sec_html)

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title} | Learning Hub</title>
<link href="assets/learning-hub-shared.css" rel="stylesheet"/>
<script src="assets/learning-hub-shared.js"></script>
<style>
{base_css}
</style>
</head>
<body data-site="cloud">
<div class="wrap">
  <div class="tech-breadcrumb">
    <a class="tech-bc-home" href="{parent_hub_url}">← {parent_hub_label}</a>
    <span class="tech-bc-sep">/</span>
    <span class="tech-bc-curr">{title}</span>
  </div>

  <div class="hero">
    <div class="edition">{badge} · {total_subs} Subsections · {total_concepts} Concepts</div>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">{total_subs}</div><div class="l">Subsections</div></div>
    <div class="stat"><div class="n">{total_concepts}</div><div class="l">Concepts</div></div>
    <div class="stat"><div class="n">100%</div><div class="l">Curated</div></div>
    <div class="stat"><div class="n">15+</div><div class="l">Verified Docs &amp; Labs</div></div>
  </div>

  <div class="overall-progress">
    <span class="lbl">Masterclass Progress</span>
    <div class="bar-track"><div class="bar-fill" id="overall-bar"></div></div>
    <span class="pct" id="overall-pct">0 / {total_concepts}</span>
  </div>

  <div class="controls">
    <div class="controls-row">
      <span class="label">Filter:</span>
      <button class="filter-btn status-done" data-filter="status" data-val="done">Done</button>
      <button class="filter-btn" data-filter="status" data-val="undone">Not Done</button>
      <button class="filter-btn status-bookmarked" data-filter="status" data-val="bookmarked">★ Bookmarked</button>
      <span class="sep"></span>
      <div class="search"><input id="search-input" placeholder="Search {total_concepts} concepts…" type="search"/></div>
      <button class="icon-btn" id="random-btn" title="Random concept">🎲</button>
      <button class="icon-btn" id="theme-toggle" title="Toggle theme">🌓</button>
      <button class="icon-btn" onclick="window.print()" title="Print">🖨️</button>
      <button class="filter-btn" id="clear-filters">Clear</button>
    </div>
  </div>

  {sec_html}

  {SISTER_CARDS_HTML}
</div>

<script>
window.SITE_SLUG = "cloud";
</script>
<script>
{STANDALONE_JS}
</script>
</body>
</html>
"""
    dest = os.path.join(ROOT, filename)
    atomic_write(dest, page_html)
    print(f"Generated masterclass: {filename} ({total_subs} subs, {total_concepts} concepts).")

def main():
    # 1. Generate tech_azure.html
    generate_masterclass_page(
        "tech_azure.html",
        "Microsoft Azure Cloud Architecture Masterclass",
        "Enterprise Microsoft Azure architecture: Entra ID identity governance, Virtual Machines & App Service runtimes, VNet secure topologies, Cosmos DB globally distributed multi-model databases, Azure SQL, and AKS container microservices.",
        "Enterprise Identity, Microservices & Data · Masterclass",
        "cloud_aws_azure.html",
        "Cloud Platforms Hub",
        sec_azure
    )

    # 2. Generate tech_gcp.html
    generate_masterclass_page(
        "tech_gcp.html",
        "Google Cloud Platform (GCP) Architecture Masterclass",
        "Production Google Cloud engineering: Google Kubernetes Engine (GKE) enterprise clusters, Cloud Run serverless scale-to-zero microservices, BigQuery petabyte analytical data warehousing, Cloud Spanner horizontally scalable relational databases, and global VPC networking.",
        "Containers, Serverless, Big Data & Analytics · Masterclass",
        "cloud_aws_azure.html",
        "Cloud Platforms Hub",
        sec_gcp
    )

    # 3. Generate tech_spark.html
    generate_masterclass_page(
        "tech_spark.html",
        "Apache Spark Big Data Processing Masterclass",
        "High-performance distributed cluster computing: RDD core primitives, DataFrame/Dataset APIs, Catalyst query optimization, Tungsten off-heap memory management, wide vs narrow shuffle stages, Spark SQL, and Structured Streaming.",
        "Distributed In-Memory Cluster Computing · Masterclass",
        "all_tech.html",
        "All-in-One Tech Portal",
        sec_spark
    )

    # 4. Update cloud_aws_azure.html to link Azure and GCP to their masterclasses
    with open(os.path.join(ROOT, 'cloud_aws_azure.html'), 'r', encoding='utf-8') as f:
        c_content = f.read()

    # Update Azure card in cloud_aws_azure.html
    if 'id="card-azure"' in c_content:
        # Check if masterclass button exists for azure
        if 'href="tech_azure.html"' not in c_content:
            c_content = re.sub(
                r'(<div class="domain-card"[^>]*id="card-azure"[^>]*>[\s\S]*?<div class="domain-card-actions">\s*<button class="domain-btn-view"[^>]*>[^<]*</button>)\s*</div>',
                r'\1\n<a class="domain-btn-masterclass" href="tech_azure.html">Dedicated Masterclass ↗</a>\n</div>',
                c_content
            )

    # Update GCP card in cloud_aws_azure.html
    if 'id="card-gcp"' in c_content:
        if 'href="tech_gcp.html"' not in c_content:
            c_content = re.sub(
                r'(<div class="domain-card"[^>]*id="card-gcp"[^>]*>[\s\S]*?<div class="domain-card-actions">\s*<button class="domain-btn-view"[^>]*>[^<]*</button>)\s*</div>',
                r'\1\n<a class="domain-btn-masterclass" href="tech_gcp.html">Dedicated Masterclass ↗</a>\n</div>',
                c_content
            )

    # Update focus bars in cloud_aws_azure.html for Azure and GCP
    if 'href="tech_azure.html"' not in c_content:
        c_content = re.sub(
            r'(<section class="section domain-section" id="section-2"[\s\S]*?<div class="domain-focus-nav">\s*<button class="domain-focus-btn"[^>]*>← Prev Domain</button>\s*<button class="domain-focus-btn"[^>]*>View All \(3\)</button>\s*<button class="domain-focus-btn"[^>]*>Next Domain →</button>)\s*</div>',
            r'\1\n<a class="domain-focus-link" href="tech_azure.html">Open Full Azure Masterclass ↗</a>\n</div>',
            c_content
        )
    if 'href="tech_gcp.html"' not in c_content:
        c_content = re.sub(
            r'(<section class="section domain-section" id="section-3"[\s\S]*?<div class="domain-focus-nav">\s*<button class="domain-focus-btn"[^>]*>← Prev Domain</button>\s*<button class="domain-focus-btn"[^>]*>View All \(3\)</button>\s*<button class="domain-focus-btn"[^>]*>Next Domain →</button>)\s*</div>',
            r'\1\n<a class="domain-focus-link" href="tech_gcp.html">Open Full GCP Masterclass ↗</a>\n</div>',
            c_content
        )

    atomic_write(os.path.join(ROOT, 'cloud_aws_azure.html'), c_content)
    print("Updated cloud_aws_azure.html with Azure & GCP masterclass links.")

    # 5. Update all_tech.html to link Spark to tech_spark.html
    with open(os.path.join(ROOT, 'all_tech.html'), 'r', encoding='utf-8') as f:
        t_content = f.read()

    if 'id="card-spark"' in t_content:
        if 'href="tech_spark.html"' not in t_content:
            t_content = re.sub(
                r'(<div class="domain-card"[^>]*id="card-spark"[^>]*>[\s\S]*?<div class="domain-card-actions">\s*<button class="domain-btn-view"[^>]*>[^<]*</button>)\s*</div>',
                r'\1\n<a class="domain-btn-masterclass" href="tech_spark.html">Dedicated Masterclass ↗</a>\n</div>',
                t_content
            )

    if 'href="tech_spark.html"' not in t_content:
        t_content = re.sub(
            r'(<section class="section domain-section" id="section-11"[\s\S]*?<div class="domain-focus-nav">\s*<button class="domain-focus-btn"[^>]*>← Prev Domain</button>\s*<button class="domain-focus-btn"[^>]*>View All \(13\)</button>\s*<button class="domain-focus-btn"[^>]*>Next Domain →</button>)\s*</div>',
            r'\1\n<a class="domain-focus-link" href="tech_spark.html">Open Full Spark Masterclass ↗</a>\n</div>',
            t_content
        )

    atomic_write(os.path.join(ROOT, 'all_tech.html'), t_content)
    print("Updated all_tech.html with Spark masterclass links.")

if __name__ == '__main__':
    main()
