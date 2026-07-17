document.addEventListener('DOMContentLoaded', () => {
    const topicNav = document.getElementById('topic-nav');
    const markdownContent = document.getElementById('markdown-content');
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const themeToggle = document.getElementById('theme-toggle');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const markStudiedBtn = document.getElementById('mark-studied');
    const studyProgress = document.getElementById('study-progress');

    let topicsData = [];
    let flatConcepts = []; // We will flatten down to concepts for Prev/Next
    let currentConceptIndex = 0;
    let currentlyLoadedPageId = null;
    let hubTitleToCid = new Map();
    const DONE_KEY = 'hub_done_sd';
    let studied = readSet(DONE_KEY);

    function readSet(key) {
        if (window.LearningHubShared) return window.LearningHubShared.readSet(key);
        try { return new Set(JSON.parse(localStorage.getItem(key) || '[]')); } catch (_e) { return new Set(); }
    }

    function writeSet(key, set) {
        if (window.LearningHubShared) window.LearningHubShared.writeSet(key, set);
        else localStorage.setItem(key, JSON.stringify(Array.from(set)));
    }

    function normalizeTitle(value) {
        if (window.LearningHubShared) return window.LearningHubShared.normalizeTitle(value);
        return String(value || '').toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, ' ').replace(/\s+/g, ' ').trim();
    }

    function conceptStorageKey(concept) {
        const matched = hubTitleToCid.get(normalizeTitle(concept && concept.conceptTitle));
        return matched || `tutorial:${concept.pageId}/${concept.conceptId}`;
    }

    async function loadHubProgressMap() {
        try {
            const response = await fetch('../learning-hub-data.json', { cache: 'no-cache' });
            if (!response.ok) return;
            const data = await response.json();
            (data.items || []).forEach(item => {
                if (item.domain === 'sd') hubTitleToCid.set(normalizeTitle(item.title), item.key);
            });
        } catch (_error) {
            hubTitleToCid = new Map();
        }
    }

    // Configure marked.js to use highlight.js and inject IDs into headings
    const renderer = new marked.Renderer();
    renderer.heading = function(...args) {
        let textStr = '';
        let level = 1;

        if (args.length === 1 && typeof args[0] === 'object') {
            textStr = args[0].text || args[0].raw;
            level = args[0].depth;
        } else {
            textStr = args[0];
            level = args[1];
        }

        const id = String(textStr).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        return `<h${level} id="${id}">${textStr}</h${level}>`;
    };

    marked.setOptions({
        renderer: renderer,
        highlight: function(code, lang) {
            const language = hljs.getLanguage(lang) ? lang : 'plaintext';
            return hljs.highlight(code, { language }).value;
        },
        langPrefix: 'hljs language-'
    });

    // Theme handling
    const initTheme = () => {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
    };

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Mobile menu toggle
    mobileMenuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    if (markStudiedBtn) {
        markStudiedBtn.addEventListener('click', () => {
            const concept = flatConcepts[currentConceptIndex];
            if (!concept) return;
            const key = conceptStorageKey(concept);
            studied = readSet(DONE_KEY);
            if (studied.has(key)) studied.delete(key);
            else studied.add(key);
            writeSet(DONE_KEY, studied);
            updateStudyToolbar();
            renderStudiedMarkers();
        });
    }

    // Initialize Application
    const init = async () => {
        initTheme();
        try {
            topicsData = window.topicsData;
            await loadHubProgressMap();
            studied = readSet(DONE_KEY);

            // Flatten to concepts for pagination
            topicsData.forEach(section => {
                section.subsections.forEach(sub => {
                    sub.concepts.forEach(concept => {
                        flatConcepts.push({
                            pageId: sub.id,
                            pageTitle: sub.title,
                            file: sub.file,
                            conceptId: concept.anchor,
                            conceptTitle: concept.title
                        });
                    });
                });
            });

            renderSidebar();
            handleRouting();

            window.addEventListener('hashchange', handleRouting);
        } catch (error) {
            console.error('Error loading topics:', error);
            topicNav.innerHTML = '<div style="padding: 24px; color: red;">Failed to load curriculum.</div>';
        }
    };

    const renderSidebar = () => {
        topicNav.innerHTML = '';

        topicsData.forEach(section => {
            const sectionEl = document.createElement('div');
            sectionEl.className = 'topic-group';

            const titleEl = document.createElement('div');
            titleEl.className = 'topic-group-title';
            titleEl.innerText = section.section;
            sectionEl.appendChild(titleEl);

            const subListEl = document.createElement('div');
            subListEl.className = 'topic-list';

            section.subsections.forEach(sub => {
                const subTitleEl = document.createElement('div');
                subTitleEl.className = 'subsection-title';
                subTitleEl.innerText = sub.title;
                subTitleEl.style.fontWeight = '600';
                subTitleEl.style.marginTop = '10px';
                subTitleEl.style.marginBottom = '4px';
                subTitleEl.style.color = 'var(--text-primary)';
                subTitleEl.style.fontSize = '0.9rem';
                subListEl.appendChild(subTitleEl);

                sub.concepts.forEach(concept => {
                    const link = document.createElement('a');
                    link.href = `#${sub.id}/${concept.anchor}`;
                    link.className = 'topic-link';
                    link.innerText = concept.title;
                    link.dataset.pageId = sub.id;
                    link.dataset.conceptId = concept.anchor;

                    link.addEventListener('click', () => {
                        if (window.innerWidth <= 900) {
                            sidebar.classList.remove('open');
                        }
                    });

                    subListEl.appendChild(link);
                });
            });

            sectionEl.appendChild(subListEl);
            topicNav.appendChild(sectionEl);
        });
        renderStudiedMarkers();
    };

    const renderStudiedMarkers = () => {
        studied = readSet(DONE_KEY);
        document.querySelectorAll('.topic-link').forEach(link => {
            const concept = flatConcepts.find(c => c.pageId === link.dataset.pageId && c.conceptId === link.dataset.conceptId);
            link.classList.toggle('studied', concept ? studied.has(conceptStorageKey(concept)) : false);
        });
        if (studyProgress) {
            const total = flatConcepts.length;
            const done = flatConcepts.filter(c => studied.has(conceptStorageKey(c))).length;
            studyProgress.textContent = `${done} / ${total} studied`;
        }
    };

    const updateStudyToolbar = () => {
        const concept = flatConcepts[currentConceptIndex];
        if (!concept || !markStudiedBtn) return;
        studied = readSet(DONE_KEY);
        const isDone = studied.has(conceptStorageKey(concept));
        markStudiedBtn.classList.toggle('is-done', isDone);
        markStudiedBtn.textContent = isDone ? 'Studied' : 'Mark Studied';
        renderStudiedMarkers();
    };

    const handleRouting = async () => {
        const hash = window.location.hash.substring(1); // e.g. "requirements-scope/functional-requirements"
        let targetConcept = flatConcepts[0];

        if (hash) {
            const parts = hash.split('/');
            const pageId = parts[0];
            const conceptId = parts[1];

            const found = flatConcepts.find(c => c.pageId === pageId && c.conceptId === conceptId);
            if (found) {
                targetConcept = found;
            } else {
                // Try to just find by pageId
                const foundPage = flatConcepts.find(c => c.pageId === pageId);
                if (foundPage) targetConcept = foundPage;
            }
        } else {
            window.history.replaceState(null, null, `#${targetConcept.pageId}/${targetConcept.conceptId}`);
        }

        currentConceptIndex = flatConcepts.findIndex(c => c.pageId === targetConcept.pageId && c.conceptId === targetConcept.conceptId);

        updateSidebarHighlight(targetConcept.pageId, targetConcept.conceptId);
        updatePaginationButtons();
        updateStudyToolbar();

        await loadContent(targetConcept);
    };

    const updateSidebarHighlight = (pageId, conceptId) => {
        document.querySelectorAll('.topic-link').forEach(link => {
            if (link.dataset.pageId === pageId && link.dataset.conceptId === conceptId) {
                link.classList.add('active');
                link.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                link.classList.remove('active');
            }
        });
    };

    const updatePaginationButtons = () => {
        if (currentConceptIndex > 0) {
            btnPrev.disabled = false;
            const prev = flatConcepts[currentConceptIndex - 1];
            btnPrev.onclick = () => { window.location.hash = `${prev.pageId}/${prev.conceptId}`; };
        } else {
            btnPrev.disabled = true;
            btnPrev.onclick = null;
        }

        if (currentConceptIndex < flatConcepts.length - 1) {
            btnNext.disabled = false;
            btnNext.querySelector('span') ? null : btnNext.innerHTML = 'Next Topic <span class="arrow">→</span>';
            const next = flatConcepts[currentConceptIndex + 1];
            btnNext.onclick = () => { window.location.hash = `${next.pageId}/${next.conceptId}`; };
        } else {
            btnNext.disabled = true;
            btnNext.onclick = null;
        }
    };

    const loadContent = async (concept) => {
        // If we are already on the correct page, just scroll
        if (currentlyLoadedPageId === concept.pageId) {
            scrollToConcept(concept.conceptId);
            return;
        }

        markdownContent.innerHTML = '<div class="loading-spinner">Loading content...</div>';
        try {
            const markdownText = window.contentBundle[concept.file];
            if (!markdownText) throw new Error('Content not found');

            // Format raw math exponents like 2^10 or O(N^2) to HTML superscripts before parsing
            let processedText = markdownText.replace(/([A-Za-z0-9_]+)\^([A-Za-z0-9_]+)/g, '$1<sup>$2</sup>');

            let rawHtml = marked.parse(processedText);

            // Post-process blockquotes to alerts to preserve inner markdown formatting
            rawHtml = rawHtml.replace(/<blockquote>\s*<p>\[!(TIP|NOTE|WARNING|IMPORTANT|CAUTION)\]([\s\S]*?)<\/p>\s*<\/blockquote>/gi, (match, type, content) => {
                const alertType = type.toLowerCase();
                let icon = '💡';
                if (alertType === 'note') icon = 'ℹ️';
                if (alertType === 'warning') icon = '⚠️';
                if (alertType === 'important') icon = '🔥';
                if (alertType === 'caution') icon = '🛑';

                const cleanContent = content.replace(/^(?:<br\s*\/?>|\n|\s)+/, '');

                return `<div class="alert alert-${alertType}">
                    <div class="alert-header">
                        <span class="alert-icon">${icon}</span>
                        <span class="alert-title">${alertType.toUpperCase()}</span>
                    </div>
                    <div class="alert-content">${cleanContent}</div>
                </div>`;
            });

            const safeHtml = DOMPurify.sanitize(rawHtml, { ADD_ATTR: ['id'] }); // Allow id tags for scrolling

            markdownContent.innerHTML = safeHtml;
            markdownContent.classList.add('fade-in');

            currentlyLoadedPageId = concept.pageId;

            // Render Mermaid diagrams
            try {
                if (window.mermaid) {
                    const mermaidBlocks = document.querySelectorAll('#markdown-content code.language-mermaid');
                    if (mermaidBlocks.length > 0) {
                        mermaidBlocks.forEach((el) => {
                            const pre = el.parentElement;
                            if (pre && pre.tagName === 'PRE') {
                                const div = document.createElement('div');
                                div.className = 'mermaid';
                                div.style.textAlign = 'center';
                                div.style.margin = '2rem 0';
                                div.textContent = el.textContent; // Using textContent unescapes HTML entities if any
                                pre.replaceWith(div);
                            }
                        });
                        mermaid.run();
                    }
                }
            } catch (err) {
                console.error("Mermaid error:", err);
            }

            setTimeout(() => {
                markdownContent.classList.remove('fade-in');
            }, 400);

            scrollToConcept(concept.conceptId);

        } catch (error) {
            console.error('Error fetching content:', error);
            currentlyLoadedPageId = null;
            markdownContent.innerHTML = `
                <div style="text-align: center; padding: 40px;">
                    <h1>🚧 Error Loading Content</h1>
                    <p>The masterclass for <strong>${concept.pageTitle}</strong> failed to load.</p>
                    <pre style="text-align: left; background: #222; padding: 15px; margin-top: 20px; color: red; overflow-x: auto;">
${error.message}
${error.stack}
                    </pre>
                </div>
            `;
        }
    };

    const scrollToConcept = (conceptId) => {
        if (!conceptId) return;
        let el = document.getElementById(conceptId);

        if (!el) {
            // Fuzzy match: the sidebar anchor might not exactly match the markdown heading ID.
            const headers = Array.from(document.querySelectorAll('#markdown-content h1, #markdown-content h2, #markdown-content h3, #markdown-content h4'));
            const cleanConcept = conceptId.replace(/-/g, '');

            el = headers.find(h => {
                const cleanId = h.id.replace(/-/g, '');
                // Match if one is a substring of the other (e.g. "functional-requirements" vs "functional-requirements-checklist")
                return cleanId.length > 3 && (cleanConcept.includes(cleanId) || cleanId.includes(cleanConcept));
            });
        }

        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Add a slight highlight animation
            el.style.transition = 'color 0.4s ease';
            const originalColor = el.style.color;
            el.style.color = 'var(--accent-primary)';
            setTimeout(() => {
                el.style.color = originalColor || '';
            }, 1200);
        } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    };

    window.addEventListener('learning-hub-progress-external', (event) => {
        if (!event.detail || event.detail.key !== DONE_KEY) return;
        studied = readSet(DONE_KEY);
        updateStudyToolbar();
        renderStudiedMarkers();
    });

    // Boot
    init();
});
