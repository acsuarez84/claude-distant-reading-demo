/**
 * Distant Reading Visualization Application
 * Interactive analysis of LLM outputs through rhetorical frameworks
 */

// Global state
const state = {
    data: null,
    currentView: 'text',
    selectedLLM: 'poe_chatbot',
    selectedSegment: 0,
    selectedParameter: 'full',
    wordcloudParameter: 'context',
    compareLLMs: ['poe_chatbot', 'chatgpt'],
    chartType: 'radar',
    compareTheory: 'all',
    compareParameter: 'all'
};

// ============================================================================
// Data Loading
// ============================================================================
async function loadData() {
    try {
        const response = await fetch('analysis_results.json');
        const data = await response.json();
        state.data = data;
        console.log('Data loaded:', data);
        return data;
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Error loading analysis data. Please ensure analysis_results.json exists.');
        return null;
    }
}

// ============================================================================
// Initialization
// ============================================================================
async function init() {
    console.log('Initializing application...');

    // Load data
    const data = await loadData();
    if (!data) return;

    // Set up event listeners
    setupNavigation();
    setupTextView();
    setupWordCloudView();
    setupConceptMapView();
    setupCompareView();

    // Initialize first view
    showView('text');
    updateTextView();
}

// ============================================================================
// Navigation
// ============================================================================
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            showView(view);
        });
    });
}

function showView(viewName) {
    state.currentView = viewName;

    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === viewName);
    });

    // Update views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });

    document.getElementById(`${viewName}-view`).classList.add('active');

    // Update view content
    switch (viewName) {
        case 'text':
            updateTextView();
            break;
        case 'wordclouds':
            updateWordCloudView();
            break;
        case 'conceptmap':
            updateConceptMapView();
            break;
        case 'compare':
            updateCompareView();
            break;
    }
}

// ============================================================================
// Text Navigation View
// ============================================================================
function setupTextView() {
    const llmSelect = document.getElementById('llm-select');
    const segmentSelect = document.getElementById('segment-select');
    const parameterSelect = document.getElementById('parameter-select');

    llmSelect.addEventListener('change', (e) => {
        state.selectedLLM = e.target.value;
        populateSegmentSelect();
        updateTextView();
    });

    segmentSelect.addEventListener('change', (e) => {
        state.selectedSegment = parseInt(e.target.value);
        updateTextView();
    });

    parameterSelect.addEventListener('change', (e) => {
        state.selectedParameter = e.target.value;
        updateTextView();
    });

    populateSegmentSelect();
}

function populateSegmentSelect() {
    const segmentSelect = document.getElementById('segment-select');
    const llmData = state.data.llms[state.selectedLLM];

    segmentSelect.innerHTML = '';

    llmData.image_responses.forEach((response, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `Segment ${response.segment_id}: ${response.prompt_type}`;
        segmentSelect.appendChild(option);
    });
}

function updateTextView() {
    const llmData = state.data.llms[state.selectedLLM];
    const response = llmData.image_responses[state.selectedSegment];

    if (!response) return;

    const textContent = document.getElementById('text-content');
    const textMetrics = document.getElementById('text-metrics');

    // Get text based on parameter selection
    let displayText = '';
    let metrics = null;

    if (state.selectedParameter === 'full') {
        displayText = response.full_response;
        metrics = response.overall_sentiment;
    } else if (response.parameters[state.selectedParameter]) {
        const param = response.parameters[state.selectedParameter];
        displayText = param.text;
        metrics = param.sentiment;
    }

    // Highlight code-switching
    const highlightedText = highlightCodeSwitching(displayText);

    textContent.innerHTML = `
        <h2>${response.prompt_type} Prompt</h2>
        <p class="prompt"><em>${response.prompt}</em></p>
        <hr style="margin: 1rem 0; border: none; border-top: 2px solid #E0E0E0;">
        <div>${highlightedText}</div>
    `;

    // Display metrics
    if (metrics) {
        textMetrics.innerHTML = `
            <h3>Sentiment Analysis</h3>
            <div class="metric-item">
                <div class="metric-label">Polarity</div>
                <div class="metric-value" style="color: ${getPolarityColor(metrics.polarity)}">${metrics.polarity.toFixed(2)}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Subjectivity</div>
                <div class="metric-value">${metrics.subjectivity.toFixed(2)}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Emotion</div>
                <div class="metric-value">${capitalizeFirst(metrics.emotion)}</div>
            </div>
        `;

        // Add parameter-specific metrics
        if (state.selectedParameter !== 'full' && response.parameters[state.selectedParameter]) {
            const param = response.parameters[state.selectedParameter];
            const themes = param.themes.slice(0, 5);

            textMetrics.innerHTML += `
                <h3 style="margin-top: 1.5rem;">Top Themes</h3>
                ${themes.map(theme => `
                    <div class="metric-item">
                        <div class="metric-label">${theme.word}</div>
                        <div class="metric-value">${theme.count}</div>
                    </div>
                `).join('')}
            `;
        }
    }
}

function highlightCodeSwitching(text) {
    const spanishPatterns = [
        /\b(mija|aquí|verdad|pero|sí|cómo|qué|ves|mira|ahh|ese|eso|todo|tanto|también|océano|cielo|mar|entiendes|ni|allá)\b/gi,
        /¿[^?]+\?/g
    ];

    let highlighted = text;

    spanishPatterns.forEach(pattern => {
        highlighted = highlighted.replace(pattern, '<span class="code-switch">$&</span>');
    });

    return highlighted;
}

function getPolarityColor(polarity) {
    if (polarity > 0.3) return '#2D7D2D';
    if (polarity < -0.3) return '#CC0000';
    return '#6C757D';
}

// ============================================================================
// Word Cloud View
// ============================================================================
function setupWordCloudView() {
    const tabs = document.querySelectorAll('.tab-btn');
    const filters = document.querySelectorAll('.wordcloud-filters input[type="checkbox"]');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            state.wordcloudParameter = tab.dataset.param;
            updateWordCloudView();
        });
    });

    filters.forEach(filter => {
        filter.addEventListener('change', () => {
            updateWordCloudView();
        });
    });
}

function updateWordCloudView() {
    const container = document.getElementById('wordcloud-container');
    const parameter = state.wordcloudParameter;

    // Get selected LLMs
    const selectedLLMs = Array.from(document.querySelectorAll('.wordcloud-filters input:checked'))
        .map(cb => cb.value);

    // Collect themes from selected LLMs
    const themes = collectThemesForWordCloud(parameter, selectedLLMs);

    // Clear container
    container.innerHTML = '';

    if (themes.length === 0) {
        container.innerHTML = '<div class="loading">No data available for selected filters</div>';
        return;
    }

    // Create word cloud data
    const wordCloudData = themes.map(([word, weight]) => [word, weight * 10]);

    // Render word cloud
    try {
        WordCloud(container, {
            list: wordCloudData,
            gridSize: 10,
            weightFactor: 8,
            fontFamily: 'Arial, sans-serif',
            color: function() {
                const colors = ['#0066CC', '#2D7D2D', '#D4A017', '#9B59B6', '#FF6B35'];
                return colors[Math.floor(Math.random() * colors.length)];
            },
            rotateRatio: 0.3,
            backgroundColor: 'white',
            click: function(item) {
                showWordDetails(item[0], parameter);
            }
        });
    } catch (error) {
        console.error('WordCloud error:', error);
        container.innerHTML = '<div class="loading">Error rendering word cloud</div>';
    }
}

function collectThemesForWordCloud(parameter, selectedLLMs) {
    const themeCounts = {};

    selectedLLMs.forEach(llmName => {
        const llmData = state.data.llms[llmName];

        llmData.image_responses.forEach(response => {
            if (response.parameters[parameter]) {
                const themes = response.parameters[parameter].themes;
                themes.forEach(theme => {
                    themeCounts[theme.word] = (themeCounts[theme.word] || 0) + theme.count;
                });
            }
        });
    });

    return Object.entries(themeCounts).sort((a, b) => b[1] - a[1]).slice(0, 50);
}

function showWordDetails(word, parameter) {
    const detailsPanel = document.getElementById('wordcloud-details');

    // Find contexts where this word appears
    const contexts = [];

    Object.entries(state.data.llms).forEach(([llmName, llmData]) => {
        llmData.image_responses.forEach(response => {
            if (response.parameters[parameter]) {
                const text = response.parameters[parameter].text;
                if (text.toLowerCase().includes(word.toLowerCase())) {
                    const sentences = text.split(/[.!?]+/);
                    sentences.forEach(sentence => {
                        if (sentence.toLowerCase().includes(word.toLowerCase())) {
                            contexts.push({
                                llm: llmName,
                                segment: response.segment_id,
                                text: sentence.trim()
                            });
                        }
                    });
                }
            }
        });
    });

    detailsPanel.innerHTML = `
        <h3>Word: "${word}"</h3>
        <p><strong>Appears in ${contexts.length} contexts</strong></p>
        <div style="max-height: 400px; overflow-y: auto;">
            ${contexts.slice(0, 10).map(ctx => `
                <div class="metric-item">
                    <div class="metric-label">${getLLMDisplayName(ctx.llm)} - Segment ${ctx.segment}</div>
                    <p style="margin-top: 0.5rem; font-size: 0.9rem;">${ctx.text}</p>
                </div>
            `).join('')}
        </div>
    `;
}

// ============================================================================
// Concept Map View
// ============================================================================
function setupConceptMapView() {
    const edgeFilters = document.querySelectorAll('.edge-filter');

    edgeFilters.forEach(filter => {
        filter.addEventListener('change', () => {
            updateConceptMapView();
        });
    });
}

function updateConceptMapView() {
    const container = document.getElementById('concept-map-container');

    // Clear existing
    container.innerHTML = '';

    // Build graph data
    const graphData = buildConceptMapData();

    // Render D3 force-directed graph
    renderConceptMap(container, graphData);
}

function buildConceptMapData() {
    const nodes = [];
    const links = [];
    let nodeId = 0;

    // Add LLM nodes
    const llmNames = ['poe_chatbot', 'chatgpt', 'claude_ai'];
    const llmNodes = {};

    llmNames.forEach(llmName => {
        const node = {
            id: nodeId++,
            name: getLLMDisplayName(llmName),
            type: 'llm',
            llmKey: llmName,
            data: state.data.llms[llmName]
        };
        nodes.push(node);
        llmNodes[llmName] = node;
    });

    // Add theory nodes
    const theories = [
        { key: 'srtol', name: "Students' Rights to Their Own Language" },
        { key: 'multiliteracies', name: 'Multiliteracies' },
        { key: 'multimodality', name: 'Multimodality' },
        { key: 'rhetorical_listening', name: 'Rhetorical Listening' },
        { key: 'code_meshing', name: 'Code-Meshing' },
        { key: 'big_data', name: 'Big Data' },
        { key: 'composing_with_ai', name: 'Composing with AI' }
    ];

    const theoryNodes = {};

    theories.forEach(theory => {
        const node = {
            id: nodeId++,
            name: theory.name,
            type: 'theory',
            theoryKey: theory.key
        };
        nodes.push(node);
        theoryNodes[theory.key] = node;
    });

    // Add top theme nodes
    const topThemes = state.data.comparative_analysis.themes.unified_themes || [];
    const themeNodes = {};

    topThemes.slice(0, 10).forEach(theme => {
        const node = {
            id: nodeId++,
            name: theme.word,
            type: 'theme',
            count: theme.count
        };
        nodes.push(node);
        themeNodes[theme.word] = node;
    });

    // Create links

    // 1. LLM to Theory links (based on alignment scores)
    llmNames.forEach(llmName => {
        const llmData = state.data.llms[llmName];
        const theoreticalAnalysis = llmData.theoretical_analysis;

        if (theoreticalAnalysis) {
            Object.entries(theoreticalAnalysis).forEach(([theoryKey, scores]) => {
                if (theoryNodes[theoryKey] && scores.avg_alignment > 0.3) {
                    links.push({
                        source: llmNodes[llmName].id,
                        target: theoryNodes[theoryKey].id,
                        type: 'alignment',
                        strength: scores.avg_alignment,
                        value: scores.avg_alignment * 10
                    });
                }

                // Add tension links for low alignment
                if (theoryNodes[theoryKey] && scores.avg_alignment < 0.2) {
                    links.push({
                        source: llmNodes[llmName].id,
                        target: theoryNodes[theoryKey].id,
                        type: 'tension',
                        strength: 1 - scores.avg_alignment,
                        value: 5
                    });
                }
            });
        }
    });

    // 2. Shared theme links between LLMs
    const llmThemes = {};
    llmNames.forEach(llmName => {
        llmThemes[llmName] = new Set();
        const llmData = state.data.llms[llmName];
        llmData.image_responses.forEach(response => {
            Object.values(response.parameters).forEach(param => {
                if (param.themes) {
                    param.themes.forEach(theme => {
                        llmThemes[llmName].add(theme.word);
                    });
                }
            });
        });
    });

    // Find shared themes
    for (let i = 0; i < llmNames.length; i++) {
        for (let j = i + 1; j < llmNames.length; j++) {
            const llm1 = llmNames[i];
            const llm2 = llmNames[j];
            const shared = [...llmThemes[llm1]].filter(t => llmThemes[llm2].has(t));

            if (shared.length > 3) {
                links.push({
                    source: llmNodes[llm1].id,
                    target: llmNodes[llm2].id,
                    type: 'shared-theme',
                    strength: shared.length / 10,
                    value: shared.length
                });
            }
        }
    }

    // 3. LLM to theme links
    Object.entries(themeNodes).forEach(([themeName, themeNode]) => {
        llmNames.forEach(llmName => {
            if (llmThemes[llmName].has(themeName)) {
                links.push({
                    source: llmNodes[llmName].id,
                    target: themeNode.id,
                    type: 'shared-theme',
                    strength: 0.5,
                    value: 3
                });
            }
        });
    });

    // 4. Sentiment-based links
    llmNames.forEach(llmName => {
        const llmData = state.data.llms[llmName];
        const sentiment = llmData.sentiment;

        if (sentiment) {
            llmNames.forEach(otherLLM => {
                if (otherLLM !== llmName) {
                    const otherSentiment = state.data.llms[otherLLM].sentiment;
                    if (otherSentiment) {
                        const polarityDiff = Math.abs(sentiment.average_polarity - otherSentiment.average_polarity);

                        if (polarityDiff < 0.2) {
                            links.push({
                                source: llmNodes[llmName].id,
                                target: llmNodes[otherLLM].id,
                                type: 'sentiment',
                                strength: 1 - polarityDiff,
                                value: 5
                            });
                        }
                    }
                }
            });
        }
    });

    return { nodes, links };
}

function renderConceptMap(container, graphData) {
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Create SVG
    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // Add zoom behavior
    const g = svg.append('g');

    svg.call(d3.zoom()
        .scaleExtent([0.5, 3])
        .on('zoom', (event) => {
            g.attr('transform', event.transform);
        }));

    // Get enabled edge types
    const enabledEdges = Array.from(document.querySelectorAll('.edge-filter:checked'))
        .map(cb => cb.value);

    // Filter links
    const filteredLinks = graphData.links.filter(link => enabledEdges.includes(link.type));

    // Create force simulation
    const simulation = d3.forceSimulation(graphData.nodes)
        .force('link', d3.forceLink(filteredLinks).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(40));

    // Draw links
    const link = g.append('g')
        .selectAll('line')
        .data(filteredLinks)
        .enter().append('line')
        .attr('class', d => `edge ${d.type}`)
        .style('stroke', d => getEdgeColor(d.type))
        .style('stroke-width', d => Math.max(2, d.value / 2))
        .style('stroke-opacity', 0.6);

    // Draw nodes
    const node = g.append('g')
        .selectAll('circle')
        .data(graphData.nodes)
        .enter().append('circle')
        .attr('r', d => getNodeSize(d))
        .attr('fill', d => getNodeColor(d.type))
        .attr('stroke', '#1A1A1A')
        .attr('stroke-width', 3)
        .style('cursor', 'pointer')
        .call(drag(simulation))
        .on('click', (event, d) => showNodeDetails(d))
        .on('mouseover', function(event, d) {
            d3.select(this)
                .transition()
                .duration(200)
                .attr('r', getNodeSize(d) * 1.3);

            showTooltip(event, d);
        })
        .on('mouseout', function(event, d) {
            d3.select(this)
                .transition()
                .duration(200)
                .attr('r', getNodeSize(d));

            hideTooltip();
        });

    // Add labels
    const label = g.append('g')
        .selectAll('text')
        .data(graphData.nodes)
        .enter().append('text')
        .text(d => d.name.length > 20 ? d.name.substring(0, 20) + '...' : d.name)
        .attr('font-size', 12)
        .attr('font-weight', 'bold')
        .attr('text-anchor', 'middle')
        .attr('dy', d => getNodeSize(d) + 20)
        .style('pointer-events', 'none')
        .style('user-select', 'none');

    // Update positions
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);

        label
            .attr('x', d => d.x)
            .attr('y', d => d.y);
    });
}

function drag(simulation) {
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        // Keep node fixed after dragging
        // Uncomment below to allow nodes to float again
        // d.fx = null;
        // d.fy = null;
    }

    return d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);
}

function getNodeSize(node) {
    switch (node.type) {
        case 'llm': return 25;
        case 'theory': return 20;
        case 'theme': return 15 + (node.count || 0) / 2;
        default: return 15;
    }
}

function getNodeColor(type) {
    const colors = {
        'llm': '#0066CC',
        'theory': '#2D7D2D',
        'theme': '#D4A017'
    };
    return colors[type] || '#6C757D';
}

function getEdgeColor(type) {
    const colors = {
        'alignment': '#2D7D2D',
        'shared-theme': '#0066CC',
        'sentiment': '#9B59B6',
        'tension': '#CC0000'
    };
    return colors[type] || '#6C757D';
}

function showNodeDetails(node) {
    const detailsPanel = document.getElementById('concept-map-details');

    let content = `<h3>${node.name}</h3>`;

    if (node.type === 'llm') {
        const llmData = node.data;
        content += `
            <p><strong>Type:</strong> LLM Node</p>
            <p><strong>Total Responses:</strong> ${llmData.overall_stats.total_responses}</p>
            <p><strong>Total Words:</strong> ${llmData.overall_stats.total_words}</p>
            <p><strong>Average Sentiment:</strong> ${llmData.sentiment.average_polarity.toFixed(2)} (${llmData.sentiment.overall_emotion})</p>

            <div class="detail-tabs" style="margin-top: 1rem;">
                <button class="detail-tab active" onclick="showDetailTab(event, 'scores-${node.id}')">Scores</button>
                <button class="detail-tab" onclick="showDetailTab(event, 'analysis-${node.id}')">Detailed Analysis</button>
            </div>

            <div id="scores-${node.id}" class="detail-tab-content active">
                <h4>Theoretical Alignment Scores</h4>
                ${Object.entries(llmData.theoretical_analysis || {}).map(([theory, scores]) => `
                    <div class="metric-item">
                        <div class="metric-label">${theory}</div>
                        <div class="metric-value">
                            Consistency: ${scores.avg_consistency.toFixed(2)} |
                            Alignment: ${scores.avg_alignment.toFixed(2)}
                        </div>
                    </div>
                `).join('')}
            </div>

            <div id="analysis-${node.id}" class="detail-tab-content" style="display: none;">
                <div style="max-height: 500px; overflow-y: auto;">
                    ${generateLLMAnalysisSummary(llmData)}
                </div>
            </div>
        `;
    } else if (node.type === 'theory') {
        content += `
            <p><strong>Type:</strong> Theoretical Framework</p>
            <p><strong>Key:</strong> ${node.theoryKey}</p>
            <div style="margin-top: 1rem;">
                ${generateTheoryAnalysisSummary(node.theoryKey)}
            </div>
        `;
    } else if (node.type === 'theme') {
        content += `
            <p><strong>Type:</strong> Theme Node</p>
            <p><strong>Frequency:</strong> ${node.count}</p>
        `;
    }

    detailsPanel.innerHTML = content;
}

function showDetailTab(event, tabId) {
    // Get all tabs and content in the clicked tab's container
    const button = event.target;
    const container = button.closest('.detail-tabs').parentElement;

    // Hide all tab content
    const tabContents = container.querySelectorAll('.detail-tab-content');
    tabContents.forEach(tc => tc.style.display = 'none');

    // Remove active class from all tabs
    const tabs = container.querySelectorAll('.detail-tab');
    tabs.forEach(t => t.classList.remove('active'));

    // Show selected tab and mark button active
    document.getElementById(tabId).style.display = 'block';
    button.classList.add('active');
}

function generateLLMAnalysisSummary(llmData) {
    // Get first response as sample for detailed analysis
    if (!llmData.image_responses || llmData.image_responses.length === 0) {
        return '<p>No analysis available</p>';
    }

    const firstResponse = llmData.image_responses[0];
    const paramData = firstResponse.parameters.context || firstResponse.parameters.abstraction || firstResponse.parameters.concept;

    if (!paramData || !paramData.theoretical_analysis) {
        return '<p>No theoretical analysis available</p>';
    }

    let html = '<p style="font-size: 0.9em; color: #666; margin-bottom: 1rem;">Sample analysis from first response (Context parameter):</p>';

    Object.entries(paramData.theoretical_analysis).forEach(([theory, data]) => {
        if (data.analysis) {
            const theoryName = theory.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            html += `
                <div class="theory-analysis-block" style="margin-bottom: 1.5rem; padding: 1rem; background: #f8f9fa; border-left: 4px solid #0066CC;">
                    <h5 style="margin-top: 0; color: #0066CC;">${theoryName}</h5>

                    <p><strong>Pattern Description:</strong><br>
                    ${data.analysis.pattern_description}</p>

                    <p><strong>Rhetorical Interpretation:</strong><br>
                    ${data.analysis.rhetorical_interpretation}</p>

                    <p><strong>Cultural/Political Implications:</strong><br>
                    ${data.analysis.cultural_political_implications}</p>

                    ${data.analysis.key_examples && data.analysis.key_examples.length > 0 ? `
                        <p><strong>Examples:</strong><br>
                        ${data.analysis.key_examples.map(ex => `• ${ex}`).join('<br>')}</p>
                    ` : ''}

                    <p style="font-size: 0.85em; color: #666;"><strong>Theorists:</strong> ${data.analysis.theorists_cited.join(', ')}</p>
                </div>
            `;
        }
    });

    return html;
}

function generateTheoryAnalysisSummary(theoryKey) {
    // Show how this theory is applied across all LLMs
    let html = '<p style="font-size: 0.9em; color: #666;">How this theory manifests across LLMs:</p>';

    Object.entries(window.analysisData.llms).forEach(([llmName, llmData]) => {
        if (llmData.image_responses && llmData.image_responses.length > 0) {
            const firstResponse = llmData.image_responses[0];
            const paramData = firstResponse.parameters.context;

            if (paramData && paramData.theoretical_analysis && paramData.theoretical_analysis[theoryKey]) {
                const analysis = paramData.theoretical_analysis[theoryKey].analysis;
                if (analysis) {
                    html += `
                        <div class="llm-theory-block" style="margin-bottom: 1rem; padding: 0.75rem; background: #f8f9fa; border-left: 3px solid #28a745;">
                            <h6 style="margin-top: 0; color: #28a745;">${llmName.replace(/_/g, ' ').toUpperCase()}</h6>
                            <p style="font-size: 0.9em;">${analysis.pattern_description}</p>
                            <p style="font-size: 0.85em; color: #666; font-style: italic;">${analysis.rhetorical_interpretation.substring(0, 200)}...</p>
                        </div>
                    `;
                }
            }
        }
    });

    return html;
}

function showTooltip(event, d) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.innerHTML = `<strong>${d.name}</strong><br>Type: ${d.type}`;
    tooltip.style.left = event.pageX + 10 + 'px';
    tooltip.style.top = event.pageY - 10 + 'px';
    document.body.appendChild(tooltip);
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// ============================================================================
// Compare View
// ============================================================================
function setupCompareView() {
    const compareLLMs = document.querySelectorAll('.compare-llm');
    const compareTheory = document.getElementById('compare-theory');
    const compareParameter = document.getElementById('compare-parameter');
    const chartTypeBtns = document.querySelectorAll('.chart-type-btn');

    compareLLMs.forEach(cb => {
        cb.addEventListener('change', () => {
            state.compareLLMs = Array.from(document.querySelectorAll('.compare-llm:checked'))
                .map(c => c.value);
            updateCompareView();
        });
    });

    compareTheory.addEventListener('change', (e) => {
        state.compareTheory = e.target.value;
        updateCompareView();
    });

    compareParameter.addEventListener('change', (e) => {
        state.compareParameter = e.target.value;
        updateCompareView();
    });

    chartTypeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            chartTypeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.chartType = btn.dataset.chart;
            updateComparisonChart();
        });
    });
}

function updateCompareView() {
    updateTextComparison();
    updateComparisonChart();
    updateDifferences();
}

function updateTextComparison() {
    const container = document.getElementById('text-comparison-container');

    if (state.compareLLMs.length === 0) {
        container.innerHTML = '<div class="loading">Please select at least one LLM to compare</div>';
        return;
    }

    container.innerHTML = state.compareLLMs.map(llmName => {
        const llmData = state.data.llms[llmName];
        const response = llmData.image_responses[0]; // First segment for now

        if (!response) return '';

        let text = response.full_response;

        if (state.compareParameter !== 'all' && response.parameters[state.compareParameter]) {
            text = response.parameters[state.compareParameter].text;
        }

        return `
            <div class="llm-text-panel ${llmName.split('_')[0]}">
                <h3>${getLLMDisplayName(llmName)}</h3>
                <div style="max-height: 500px; overflow-y: auto; font-size: 0.95rem; line-height: 1.8;">
                    ${highlightCodeSwitching(text.substring(0, 1000))}${text.length > 1000 ? '...' : ''}
                </div>
            </div>
        `;
    }).join('');
}

function updateComparisonChart() {
    const canvas = document.getElementById('comparison-chart');
    const ctx = canvas.getContext('2d');

    // Clear existing chart
    if (window.comparisonChart) {
        window.comparisonChart.destroy();
    }

    // Build chart data
    const chartData = buildChartData();

    if (!chartData) return;

    // Create chart based on type
    const config = {
        type: state.chartType,
        data: chartData,
        options: getChartOptions()
    };

    window.comparisonChart = new Chart(ctx, config);
}

function buildChartData() {
    if (state.compareLLMs.length === 0) return null;

    const theories = [
        'srtol',
        'multiliteracies',
        'multimodality',
        'rhetorical_listening',
        'code_meshing',
        'big_data',
        'composing_with_ai'
    ];

    const datasets = state.compareLLMs.map((llmName, index) => {
        const llmData = state.data.llms[llmName];
        const theoreticalAnalysis = llmData.theoretical_analysis || {};

        const data = theories.map(theory => {
            if (state.compareTheory !== 'all' && state.compareTheory !== theory) {
                return null;
            }
            return theoreticalAnalysis[theory]?.avg_alignment || 0;
        });

        const colors = {
            'poe_chatbot': '#9B59B6',
            'chatgpt': '#16A085',
            'claude_ai': '#E74C3C'
        };

        return {
            label: getLLMDisplayName(llmName),
            data: data,
            backgroundColor: colors[llmName] + '40',
            borderColor: colors[llmName],
            borderWidth: 2,
            pointBackgroundColor: colors[llmName],
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: colors[llmName]
        };
    });

    const labels = theories.map(t => t.replace(/_/g, ' ').toUpperCase());

    return {
        labels: state.compareTheory !== 'all' ? [state.compareTheory.toUpperCase()] : labels,
        datasets: datasets
    };
}

function getChartOptions() {
    const baseOptions = {
        responsive: false,  // Fixed size: 400×300
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: {
                    font: {
                        size: 14
                    }
                }
            }
        }
    };

    if (state.chartType === 'radar') {
        return {
            ...baseOptions,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        stepSize: 0.2
                    }
                }
            }
        };
    }

    return {
        ...baseOptions,
        scales: {
            y: {
                beginAtZero: true,
                max: 1
            }
        }
    };
}

function updateDifferences() {
    const container = document.getElementById('differences-list');

    if (state.compareLLMs.length < 2) {
        container.innerHTML = '<div class="loading">Please select at least 2 LLMs to compare differences</div>';
        return;
    }

    const differences = calculateDifferences();

    container.innerHTML = differences.map(diff => `
        <div class="difference-item">
            <h4>${diff.title}</h4>
            <p>${diff.description}</p>
        </div>
    `).join('');
}

function calculateDifferences() {
    const differences = [];

    // Compare code-switching frequency
    const codeSwitchingCounts = {};
    state.compareLLMs.forEach(llmName => {
        const llmData = state.data.llms[llmName];
        let total = 0;

        llmData.image_responses.forEach(response => {
            Object.values(response.parameters).forEach(param => {
                if (param.semantic_style?.cultural_markers) {
                    total += param.semantic_style.cultural_markers.spanish_terms || 0;
                }
            });
        });

        codeSwitchingCounts[llmName] = total;
    });

    const maxCS = Math.max(...Object.values(codeSwitchingCounts));
    const minCS = Math.min(...Object.values(codeSwitchingCounts));

    differences.push({
        title: 'Code-Switching Frequency',
        description: `${getLLMDisplayName(Object.keys(codeSwitchingCounts).find(k => codeSwitchingCounts[k] === maxCS))} uses the most code-switching (${maxCS} instances), while ${getLLMDisplayName(Object.keys(codeSwitchingCounts).find(k => codeSwitchingCounts[k] === minCS))} uses the least (${minCS} instances).`
    });

    // Compare sentiment
    const sentiments = {};
    state.compareLLMs.forEach(llmName => {
        const llmData = state.data.llms[llmName];
        sentiments[llmName] = llmData.sentiment?.average_polarity || 0;
    });

    differences.push({
        title: 'Sentiment Polarity',
        description: `Sentiment ranges from ${Math.min(...Object.values(sentiments)).toFixed(2)} to ${Math.max(...Object.values(sentiments)).toFixed(2)}, showing ${Math.max(...Object.values(sentiments)) - Math.min(...Object.values(sentiments)) > 0.5 ? 'significant' : 'moderate'} variation in emotional tone.`
    });

    // Compare theoretical strengths
    state.compareLLMs.forEach(llmName => {
        const llmData = state.data.llms[llmName];
        const theoreticalAnalysis = llmData.theoretical_analysis || {};

        const strongest = Object.entries(theoreticalAnalysis)
            .sort((a, b) => b[1].avg_alignment - a[1].avg_alignment)[0];

        if (strongest) {
            differences.push({
                title: `${getLLMDisplayName(llmName)} Theoretical Strength`,
                description: `Shows highest alignment with ${strongest[0].replace(/_/g, ' ')} (${strongest[1].avg_alignment.toFixed(2)}).`
            });
        }
    });

    return differences;
}

// ============================================================================
// Utility Functions
// ============================================================================
function getLLMDisplayName(llmKey) {
    const names = {
        'poe_chatbot': 'Poe.com Chatbot',
        'chatgpt': 'ChatGPT',
        'claude_ai': 'Claude.AI'
    };
    return names[llmKey] || llmKey;
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// ============================================================================
// Start Application
// ============================================================================
document.addEventListener('DOMContentLoaded', init);
