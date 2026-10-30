/**
 * WordCount Pro - Reactive Client Application
 * Zero external library dependencies. Fast, robust, and accessible.
 */

(function () {
    'use strict';

    // DOM Elements
    const textInput = document.getElementById('textInput');
    const liveWords = document.getElementById('liveWords');
    const liveChars = document.getElementById('liveChars');
    const liveSentences = document.getElementById('liveSentences');
    const charCount = document.getElementById('charCount');
    const liveStatus = document.getElementById('liveStatus');

    // KPI Elements
    const kpiWords = document.getElementById('kpiWords');
    const kpiUnique = document.getElementById('kpiUnique');
    const kpiChars = document.getElementById('kpiChars');
    const kpiCharsNoSpace = document.getElementById('kpiCharsNoSpace');
    const kpiReadTime = document.getElementById('kpiReadTime');
    const kpiSpeakTime = document.getElementById('kpiSpeakTime');
    const kpiFlesch = document.getElementById('kpiFlesch');
    const kpiGrade = document.getElementById('kpiGrade');

    // Detail Elements
    const statSentences = document.getElementById('statSentences');
    const statParagraphs = document.getElementById('statParagraphs');
    const statAvgSentence = document.getElementById('statAvgSentence');
    const statAvgWord = document.getElementById('statAvgWord');
    const statLongest = document.getElementById('statLongest');
    const statLevel = document.getElementById('statLevel');
    const statNotes = document.getElementById('statNotes');
    const statLatency = document.getElementById('statLatency');
    const keywordsList = document.getElementById('keywordsList');
    const keywordsCountBadge = document.getElementById('keywordsCountBadge');

    // Controls
    const analyzeBtn = document.getElementById('analyzeBtn');
    const clearBtn = document.getElementById('clearBtn');
    const fileUpload = document.getElementById('fileUpload');
    const filterStopwords = document.getElementById('filterStopwords');
    const topKeywordsCount = document.getElementById('topKeywordsCount');
    const copyJsonBtn = document.getElementById('copyJsonBtn');
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const samplesBtn = document.getElementById('samplesBtn');
    const samplesMenu = document.getElementById('samplesMenu');
    const toast = document.getElementById('toast');

    let lastAnalysisResult = null;
    let debounceTimer = null;

    // Sample Texts
    const SAMPLES = {
        tech: "Clean Architecture and Domain-Driven Design establish clear boundaries between high-level policy and low-level details. By decoupling domain logic from delivery frameworks like web servers or databases, systems become testable, resilient, and adaptable to technological evolution. A senior software engineer treats frameworks as implementation details rather than core dependencies.",
        classic: "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune, or to take arms against a sea of troubles and by opposing end them. To die—to sleep, no more; and by a sleep to say we end the heart-ache and the thousand natural shocks that flesh is heir to.",
        tr: "Keystone yazılım mimarisi, modülerlik ve sorumlulukların ayrıştırılması ilkelerine dayanır. Öğrencilik yıllarında yazılmış basit betikler, endüstri standartlarında katmanlı bir mimariye dönüştürüldüğünde; birim testler, veri transfer nesneleri (DTO) ve tip güvenliği projenin sürdürülebilirliğini garanti altına alır."
    };

    // Initialize Theme
    function initTheme() {
        const savedTheme = localStorage.getItem('wc_theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        themeIcon.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    }

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', nextTheme);
        localStorage.setItem('wc_theme', nextTheme);
        themeIcon.textContent = nextTheme === 'dark' ? '☀️' : '🌙';
    });

    // Toast Notification Helper
    function showToast(message, duration = 3000) {
        toast.textContent = message;
        toast.classList.remove('hidden');
        setTimeout(() => {
            toast.classList.add('hidden');
        }, duration);
    }

    // Client-side quick metrics
    function calculateInstantStats(text) {
        charCount.textContent = text.length.toLocaleString();
        liveChars.textContent = text.length.toLocaleString();

        const trimmed = text.trim();
        if (!trimmed) {
            liveWords.textContent = '0';
            liveSentences.textContent = '0';
            liveStatus.textContent = 'Ready';
            liveStatus.style.borderColor = 'var(--border-color)';
            return;
        }

        // Live approximate word count
        const words = trimmed.match(/\b[\w]+(?:['’\-][\w]+)*\b/gu) || [];
        liveWords.textContent = words.length.toLocaleString();

        // Live approximate sentence count
        const sentences = trimmed.split(/[.!?]+\s+/g).filter(s => s.trim().length > 0);
        liveSentences.textContent = sentences.length.toLocaleString();

        liveStatus.textContent = 'Typing...';
    }

    // Server API Deep Analysis
    async function executeDeepAnalysis() {
        const text = textInput.value;
        if (!text.trim()) {
            resetDashboard();
            showToast('Please enter text to analyze.');
            return;
        }

        liveStatus.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;

        try {
            const payload = {
                text: text,
                top_n_keywords: parseInt(topKeywordsCount.value, 10),
                filter_stopwords: filterStopwords.checked
            };

            const response = await fetch('/api/v1/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Analysis failed' }));
                throw new Error(errorData.detail || `Server returned ${response.status}`);
            }

            const data = await response.json();
            lastAnalysisResult = data;
            renderDashboard(data);
            liveStatus.textContent = 'Analyzed';
        } catch (err) {
            console.error('Deep Analysis Error:', err);
            showToast(`Analysis Error: ${err.message}`);
            liveStatus.textContent = 'Error';
        } finally {
            analyzeBtn.disabled = false;
        }
    }

    function renderDashboard(data) {
        // KPI Cards
        kpiWords.textContent = data.words_total.toLocaleString();
        kpiUnique.textContent = `${data.words_unique.toLocaleString()} unique (${data.vocabulary_density}% density)`;
        kpiChars.textContent = data.characters_total.toLocaleString();
        kpiCharsNoSpace.textContent = `${data.characters_no_spaces.toLocaleString()} non-whitespace`;

        kpiReadTime.textContent = data.reading_time.reading_time_formatted;
        kpiSpeakTime.textContent = `Speaking: ${data.reading_time.speaking_time_formatted}`;

        kpiFlesch.textContent = `${data.readability.flesch_reading_ease} / 100`;
        kpiGrade.textContent = `Grade Level: ${data.readability.flesch_kincaid_grade}`;

        // Detailed Stats
        statSentences.textContent = data.sentences_total.toLocaleString();
        statParagraphs.textContent = data.paragraphs_total.toLocaleString();
        statAvgSentence.textContent = `${data.avg_sentence_length} words`;
        statAvgWord.textContent = `${data.avg_word_length} chars`;
        statLongest.textContent = data.longest_word || '-';
        statLevel.textContent = data.readability.reading_level;
        statNotes.textContent = data.readability.notes;
        statLatency.textContent = `${data.execution_time_ms} ms`;

        // Render Keywords
        renderKeywords(data.top_keywords);
    }

    function renderKeywords(keywords) {
        keywordsList.innerHTML = '';
        if (!keywords || keywords.length === 0) {
            keywordsList.innerHTML = '<p class="empty-hint">No significant keywords identified.</p>';
            keywordsCountBadge.textContent = '0 found';
            return;
        }

        keywordsCountBadge.textContent = `${keywords.length} found`;
        const maxDensity = Math.max(...keywords.map(k => k.density_percent), 1);

        keywords.forEach(kw => {
            const row = document.createElement('div');
            row.className = 'keyword-row';

            const relWidth = Math.min(100, Math.round((kw.density_percent / maxDensity) * 100));

            row.innerHTML = `
                <div class="keyword-header">
                    <span class="keyword-word">${escapeHtml(kw.word)}</span>
                    <span class="keyword-metrics">${kw.count} times (${kw.density_percent}%)</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: ${relWidth}%;"></div>
                </div>
            `;
            keywordsList.appendChild(row);
        });
    }

    function resetDashboard() {
        kpiWords.textContent = '0';
        kpiUnique.textContent = '0 unique (0% density)';
        kpiChars.textContent = '0';
        kpiCharsNoSpace.textContent = '0 non-whitespace';
        kpiReadTime.textContent = '0 sec';
        kpiSpeakTime.textContent = 'Speaking: 0 sec';
        kpiFlesch.textContent = '-';
        kpiGrade.textContent = 'Grade: -';

        statSentences.textContent = '0';
        statParagraphs.textContent = '0';
        statAvgSentence.textContent = '0 words';
        statAvgWord.textContent = '0 chars';
        statLongest.textContent = '-';
        statLevel.textContent = '-';
        statNotes.textContent = '-';
        statLatency.textContent = '0 ms';

        keywordsList.innerHTML = '<p class="empty-hint">Enter or paste text to inspect keyword distribution.</p>';
        keywordsCountBadge.textContent = '0 found';
        lastAnalysisResult = null;
    }

    function escapeHtml(str) {
        return str.replace(/[&<>'"]/g, tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag));
    }

    // Event Listeners
    textInput.addEventListener('input', () => {
        calculateInstantStats(textInput.value);
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            if (textInput.value.trim().length > 0) {
                executeDeepAnalysis();
            } else {
                resetDashboard();
            }
        }, 600);
    });

    analyzeBtn.addEventListener('click', executeDeepAnalysis);
    filterStopwords.addEventListener('change', executeDeepAnalysis);
    topKeywordsCount.addEventListener('change', executeDeepAnalysis);

    clearBtn.addEventListener('click', () => {
        textInput.value = '';
        calculateInstantStats('');
        resetDashboard();
        textInput.focus();
        showToast('Text cleared.');
    });

    // File Upload
    fileUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            textInput.value = event.target.result;
            calculateInstantStats(textInput.value);
            executeDeepAnalysis();
            showToast(`Loaded "${file.name}" (${file.size.toLocaleString()} bytes)`);
        };
        reader.onerror = () => {
            showToast('Failed to read file.');
        };
        reader.readAsText(file);
        fileUpload.value = '';
    });

    // Sample Picker
    samplesBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        samplesMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', () => {
        if (!samplesMenu.classList.contains('hidden')) {
            samplesMenu.classList.add('hidden');
        }
    });

    samplesMenu.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', () => {
            const sampleKey = item.getAttribute('data-sample');
            if (SAMPLES[sampleKey]) {
                textInput.value = SAMPLES[sampleKey];
                calculateInstantStats(textInput.value);
                executeDeepAnalysis();
                showToast(`Loaded sample: ${item.textContent}`);
            }
        });
    });

    // Copy JSON Report
    copyJsonBtn.addEventListener('click', async () => {
        if (!lastAnalysisResult) {
            showToast('No analysis data available to copy.');
            return;
        }

        try {
            await navigator.clipboard.writeText(JSON.stringify(lastAnalysisResult, null, 2));
            showToast('Full JSON report copied to clipboard!');
        } catch {
            showToast('Failed to copy to clipboard.');
        }
    });

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            executeDeepAnalysis();
        } else if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            clearBtn.click();
        }
    });

    // Boot
    initTheme();
    calculateInstantStats(textInput.value);
    if (textInput.value.trim().length > 0) {
        executeDeepAnalysis();
    }
})();
