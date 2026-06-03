/**
 * Research Assistant — Frontend Logic
 * Handles form submission, agent pipeline animation, and report rendering.
 */

(function () {
    'use strict';

    // ── DOM References ──
    const searchForm = document.getElementById('search-form');
    const queryInput = document.getElementById('query-input');
    const searchBtn = document.getElementById('search-btn');
    const suggestions = document.getElementById('suggestions');
    const pipelineSection = document.getElementById('pipeline-section');
    const resultsSection = document.getElementById('results-section');
    const errorSection = document.getElementById('error-section');
    const reportContent = document.getElementById('report-content');
    const resultsTitle = document.getElementById('results-title');
    const copyBtn = document.getElementById('copy-btn');
    const newSearchBtn = document.getElementById('new-search-btn');
    const retryBtn = document.getElementById('retry-btn');
    const errorMessage = document.getElementById('error-message');
    const searchSection = document.getElementById('search-section');

    const AGENT_STEPS = ['planner', 'search', 'retriever', 'writer', 'critic'];
    const STEP_DURATIONS = [2000, 3000, 2500, 8000, 6000]; // Simulated timing

    let currentQuery = '';
    let rawReport = '';

    // ── Event Listeners ──

    searchForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (query) {
            startResearch(query);
        }
    });

    suggestions.addEventListener('click', function (e) {
        const chip = e.target.closest('.suggestion-chip');
        if (chip) {
            const query = chip.dataset.query;
            queryInput.value = query;
            startResearch(query);
        }
    });

    copyBtn.addEventListener('click', copyReport);
    newSearchBtn.addEventListener('click', resetToSearch);
    retryBtn.addEventListener('click', function () {
        if (currentQuery) {
            startResearch(currentQuery);
        }
    });

    // ── Core Functions ──

    async function startResearch(query) {
        currentQuery = query;
        rawReport = '';

        // UI State: Show pipeline, hide results/errors
        setSearchDisabled(true);
        pipelineSection.style.display = '';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
        suggestions.style.display = 'none';

        resetPipeline();

        // Animate agent steps while waiting for the API
        const pipelineAnimation = animatePipeline();

        try {
            const response = await fetch('/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}`);
            }

            const data = await response.json();

            // Complete all pipeline steps
            await pipelineAnimation.complete();

            // Show results
            rawReport = data.report || '';
            resultsTitle.textContent = `Research Report: ${query}`;
            reportContent.innerHTML = markdownToHTML(rawReport);
            resultsSection.style.display = '';

        } catch (err) {
            pipelineAnimation.cancel();
            errorMessage.textContent = err.message || 'An unexpected error occurred.';
            errorSection.style.display = '';
        } finally {
            setSearchDisabled(false);
        }
    }

    function animatePipeline() {
        let cancelled = false;
        let resolveComplete = null;
        let currentStepIndex = 0;

        const stepPromise = new Promise(function (resolve) {
            resolveComplete = resolve;
        });

        // Start animating steps with simulated timing
        async function run() {
            for (let i = 0; i < AGENT_STEPS.length; i++) {
                if (cancelled) return;
                currentStepIndex = i;
                activateStep(AGENT_STEPS[i]);

                // Activate connectors up to this point
                const connectors = document.querySelectorAll('.pipeline-connector');
                for (let j = 0; j < i; j++) {
                    if (connectors[j]) connectors[j].classList.add('active');
                }

                await sleep(STEP_DURATIONS[i]);
                if (cancelled) return;
            }
        }

        run();

        return {
            complete: async function () {
                cancelled = true;
                // Mark all steps as completed
                for (const step of AGENT_STEPS) {
                    completeStep(step);
                }
                const connectors = document.querySelectorAll('.pipeline-connector');
                connectors.forEach(function (c) { c.classList.add('active'); });
                await sleep(500); // Brief pause before showing results
            },
            cancel: function () {
                cancelled = true;
            }
        };
    }

    function activateStep(stepId) {
        const el = document.getElementById('step-' + stepId);
        if (el) {
            // Complete previous steps
            const idx = AGENT_STEPS.indexOf(stepId);
            for (let i = 0; i < idx; i++) {
                completeStep(AGENT_STEPS[i]);
            }
            el.classList.remove('completed');
            el.classList.add('active');
        }
    }

    function completeStep(stepId) {
        const el = document.getElementById('step-' + stepId);
        if (el) {
            el.classList.remove('active');
            el.classList.add('completed');
        }
    }

    function resetPipeline() {
        for (const step of AGENT_STEPS) {
            const el = document.getElementById('step-' + step);
            if (el) {
                el.classList.remove('active', 'completed');
            }
        }
        const connectors = document.querySelectorAll('.pipeline-connector');
        connectors.forEach(function (c) { c.classList.remove('active'); });
    }

    function setSearchDisabled(disabled) {
        searchBtn.disabled = disabled;
        queryInput.disabled = disabled;
        if (disabled) {
            searchBtn.querySelector('.btn-text').textContent = 'Researching…';
        } else {
            searchBtn.querySelector('.btn-text').textContent = 'Research';
        }
    }

    function resetToSearch() {
        pipelineSection.style.display = 'none';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
        suggestions.style.display = '';
        queryInput.value = '';
        queryInput.focus();
        resetPipeline();
    }

    async function copyReport() {
        try {
            await navigator.clipboard.writeText(rawReport);
            copyBtn.classList.add('copied');
            copyBtn.querySelector('span').textContent = 'Copied!';
            setTimeout(function () {
                copyBtn.classList.remove('copied');
                copyBtn.querySelector('span').textContent = 'Copy';
            }, 2000);
        } catch (err) {
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = rawReport;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
        }
    }

    // ── Markdown to HTML (lightweight) ──

    function markdownToHTML(md) {
        if (!md) return '<p>No content generated.</p>';

        let html = md;

        // Escape HTML entities
        html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

        // Headings (process from h4 to h1 to avoid ## matching before ####)
        html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

        // Bold and italic
        html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

        // Inline code
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Links (unescape the angle brackets for URLs)
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, function (match, text, url) {
            url = url.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
            return '<a href="' + url + '" target="_blank" rel="noopener noreferrer">' + text + '</a>';
        });

        // Bare URLs
        html = html.replace(/(https?:\/\/[^\s<]+)/g, function (url) {
            const cleanUrl = url.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
            return '<a href="' + cleanUrl + '" target="_blank" rel="noopener noreferrer">' + url + '</a>';
        });

        // Horizontal rules
        html = html.replace(/^---$/gm, '<hr>');

        // Blockquotes
        html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');

        // Unordered lists
        html = html.replace(/^[\-\*] (.+)$/gm, '<li>$1</li>');
        html = html.replace(/((?:<li>.+<\/li>\n?)+)/g, '<ul>$1</ul>');

        // Ordered lists
        html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

        // Paragraphs — wrap remaining text lines
        html = html.split('\n\n').map(function (block) {
            block = block.trim();
            if (!block) return '';
            // Don't wrap if it's already an HTML block element
            if (/^<(h[1-4]|ul|ol|li|blockquote|hr|p|div)/.test(block)) {
                return block;
            }
            return '<p>' + block.replace(/\n/g, '<br>') + '</p>';
        }).join('\n');

        return html;
    }

    // ── Utilities ──

    function sleep(ms) {
        return new Promise(function (resolve) { setTimeout(resolve, ms); });
    }

})();
