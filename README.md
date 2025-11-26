# Distant Reading Analysis: LLM Rhetorical Interpretation

A comprehensive computational analysis system for studying how different Large Language Models interpret visual imagery through the lens of **Context, Abstraction, and Concept** in Latino Women Rhetorics.

## Project Overview

This project analyzes responses from three AI systems:
- **Poe.com Chatbot** (ad-hoc, conversational responses with code-switching)
- **ChatGPT** (generative, formal analytical approach)
- **Claude.AI** (agentic, structured interpretation)

Using seven theoretical frameworks:
1. Students' Rights to Their Own Language (SRTOL)
2. Multiliteracies
3. Multimodality
4. Rhetorical Listening
5. Code-Meshing
6. Big Data / Computational Analysis
7. Composing with AI

## Features

### Analysis Pipeline
- **Multilingual Preprocessing**: English/Spanish tokenization with cultural term preservation
- **Theme Extraction**: TF-IDF-based bag-of-themes for Context, Abstraction, Concept
- **Theoretical Analysis**: Quantitative (consistency/alignment scores) + qualitative observations
- **Sentiment Analysis**: Polarity, subjectivity, emotion labels (overall, per-image, per-parameter)
- **Semantic Style**: Cultural markers, sentence complexity, rhetorical devices, code-switching patterns

### Interactive Visualization
- **Responsive Design**: 1-inch margins, 20px base font, mobile/tablet/desktop support
- **High Contrast**: WCAG AAA compliant color scheme
- **Four Interactive Views**:
  1. **Text Navigation** - Browse responses with code-switching highlighting
  2. **Word Clouds** - Parameter-specific clouds with LLM filtering
  3. **Concept Map** - Force-directed graph with draggable nodes (LLMs, theories, themes)
  4. **Compare LLMs** - Side-by-side text, metrics charts, key differentiators

## Quick Start

### 1. Run the Analysis

```bash
# Extract and parse the Word document
python3 extract_document.py
python3 detailed_parser.py

# Run comprehensive analysis (generates analysis_results.json)
python3 analysis_engine.py
```

### 2. View the Visualization

Simply open `index.html` in a web browser:

```bash
# Using Python's built-in server
python3 -m http.server 8000

# Then navigate to: http://localhost:8000
```

Or use any other local web server (Live Server extension in VS Code, etc.)

## File Structure

```
├── ENC 5930-Thinking Text Project-LLM Outputs.docx  # Original data
├── CLAUDE.md                                         # Project documentation
├── README.md                                         # This file
│
├── Analysis Pipeline
│   ├── extract_document.py        # Extract text from Word doc
│   ├── parse_segments.py          # Initial segmentation
│   ├── detailed_parser.py         # LLM response extraction
│   ├── analysis_engine.py         # Comprehensive analysis
│   └── requirements.txt           # Python dependencies
│
├── Generated Data
│   ├── full_text.txt             # Extracted plain text
│   ├── segments_parsed.json      # Initial segments
│   ├── structured_data.json      # Parsed LLM responses
│   └── analysis_results.json     # Complete analysis (382KB)
│
└── Visualization
    ├── index.html                # Main page
    ├── styles.css                # Responsive styles
    └── app.js                    # Interactive functionality
```

## Visualization Guide

### Text Navigation
- **Select LLM**: Choose which AI system to view
- **Select Image**: Pick from 7 different image prompts (AD-HOC, ZERO-SHOT, FEW-SHOT)
- **Select Parameter**: View full response or specific parameter (Context/Abstraction/Concept)
- **Features**:
  - Spanish phrases highlighted in gold
  - Sentiment metrics in side panel
  - Top themes display

### Word Clouds
- **Tabs**: Switch between Context, Abstraction, Concept
- **Filters**: Check/uncheck LLMs to include
- **Interaction**: Click words to see all contexts where they appear across LLMs

### Concept Map
- **Node Types**:
  - 🔵 Blue circles = LLM nodes (larger)
  - 🟢 Green circles = Theory nodes (medium)
  - 🟡 Gold circles = Theme nodes (size varies by frequency)
- **Edge Types**:
  - Green = Theoretical alignment
  - Blue = Shared themes
  - Purple = Sentiment similarity
  - Red = Tensions/contradictions
- **Interactions**:
  - **Hover** node → See tooltip
  - **Click** node → View detailed metrics in side panel
  - **Drag** node → Reposition (stays fixed after dragging)
  - **Zoom/Pan** → Use mouse wheel and drag background
  - **Filter** → Toggle edge types on/off

### Compare LLMs
- **Select 2-3 LLMs** to compare
- **Filter by Theory** or **Parameter**
- **Three panels**:
  1. **Side-by-Side Text**: Synchronized text comparison
  2. **Metric Comparison**: Switch between Radar, Bar, or Line charts
  3. **Key Differentiators**: Highlighted differences in code-switching, sentiment, theoretical strengths

## Analysis Insights

### Quantitative Metrics
Each theoretical framework provides:
- **Consistency Score** (0-1): How reliably the LLM applies this framework
- **Alignment Score** (0-1): How well the output matches theoretical principles

### Qualitative Observations
- Code-switching patterns and placement (beginning/middle/end)
- Cultural markers and linguistic ownership
- Rhetorical devices (metaphor, simile, personification)
- Grammatical structures (active/passive voice)
- Multimodal integration strategies

## Dependencies

### Python (Analysis)
```
spacy>=3.7.0
nltk>=3.8.0
textblob>=0.17.0
transformers>=4.35.0
torch>=2.1.0
scikit-learn>=1.3.0
numpy>=1.24.0
pandas>=2.1.0
```

Install with:
```bash
pip install -r requirements.txt
```

### JavaScript (Visualization)
All libraries loaded via CDN:
- D3.js v7 (concept map)
- Chart.js v4 (metric comparisons)
- WordCloud2.js (word clouds)

## Research Context

This project is part of **ENC 5930** research analyzing:
- How different AI architectures (ad-hoc, generative, agentic) construct rhetorical responses
- The role of code-meshing and multilingual expression in AI-generated text
- Distant reading methodologies for computational rhetoric analysis
- Intersection of visual imagery interpretation and cultural/linguistic positioning

## Academic Frameworks

### Students' Rights to Their Own Language (SRTOL)
Examines linguistic ownership, dialect preservation, and cultural authenticity in AI responses.

### Multiliteracies
Analyzes how LLMs reference multiple modes of meaning-making (visual, spatial, gestural).

### Multimodality
Studies visual-textual relationships and sensory description integration.

### Rhetorical Listening
Identifies empathetic positioning, cultural acknowledgment, and perspective-taking.

### Code-Meshing
Maps Spanish-English integration patterns and grammatical blending.

### Big Data
Meta-analyzes pattern recognition, generalization vs. specificity, abstraction levels.

### Composing with AI
Examines self-referential positioning, agency markers, human-AI relationship framing.

## Future Development

Potential extensions:
- Additional image datasets
- More LLM comparisons (GPT-4, Gemini, Llama, etc.)
- Temporal analysis (how responses change over time)
- Cross-cultural comparison (other language pairs)
- Machine learning classification of rhetorical strategies

## License

Academic research project - ENC 5930

## Citation

If using this methodology or tool, please cite:
```
Distant Reading Analysis: LLM Rhetorical Interpretation
ENC 5930 - Context, Abstraction, and Concept in Latino Women Rhetorics
[Year]
```

## Contact

For questions about the analysis methodology or theoretical frameworks, refer to the course materials for ENC 5930.
