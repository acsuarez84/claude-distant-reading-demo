# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project for ENC 5930 analyzing how different Large Language Models (LLMs) interpret visual imagery through the analytical framework of **Context, Abstraction, and Concept**, with a focus on **Latino Women Rhetorics**.

The project compares rhetorical strategies across three AI systems:
- **Poe.com Chatbot** (ad-hoc responses with heavy code-switching)
- **ChatGPT** (generative, formal analytical approach)
- **Claude.AI** (agentic, structured interpretation)

The system performs distant reading analysis using 7 theoretical frameworks and provides an interactive web-based visualization.

## Common Commands

### Running the Analysis Pipeline

```bash
# Full pipeline (from Word doc to analysis results)
python3 extract_document.py      # Extract text from Word document
python3 detailed_parser.py       # Parse into structured segments
python3 analysis_engine.py       # Run comprehensive analysis

# Quick re-run (if structured_data.json exists)
python3 analysis_engine.py       # Only regenerate analysis_results.json
```

### Viewing the Visualization

```bash
# Start local web server
python3 -m http.server 8000

# Then open: http://localhost:8000
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Note: The visualization has no build step - it's vanilla HTML/CSS/JS with CDN-loaded libraries (D3.js, Chart.js, WordCloud2.js).

## Architecture Overview

### Two-Part System

1. **Analysis Pipeline** (Python) - Processes Word document → Generates JSON analysis
2. **Visualization Interface** (HTML/CSS/JS) - Loads JSON → Interactive exploration

### Data Flow

```
Word Document (39K chars, 7 image prompts)
    ↓ extract_document.py
Plain Text (full_text.txt)
    ↓ parse_segments.py / detailed_parser.py
Structured JSON (structured_data.json)
    - Segments by prompt type (AD-HOC, ZERO-SHOT, FEW-SHOT)
    - LLM responses (poe_chatbot, chatgpt, claude_ai)
    - Parameters (context, abstraction, concept)
    ↓ analysis_engine.py
Complete Analysis (analysis_results.json - 382KB)
    - Theme extraction
    - Sentiment analysis (multilingual)
    - Semantic style analysis
    - 7 theoretical framework scores
    ↓ app.js loads
Interactive Visualization (index.html)
```

### Analysis Engine Architecture

The `analysis_engine.py` contains five major analyzers:

1. **MultilingualPreprocessor**
   - Tokenizes English and Spanish text
   - Detects code-switching instances (Spanish words, ¿?questions)
   - Preserves culturally significant terms (mija, aquí, ves, etc.)
   - Filters stopwords while keeping cultural markers

2. **ThemeExtractor**
   - TF-IDF-based theme extraction
   - Generates separate bags for Context/Abstraction/Concept + unified
   - Outputs top N themes with frequency counts

3. **TheoreticalAnalyzer**
   - 7 analysis methods (one per framework):
     - `analyze_srtol()` - Students' Rights to Their Own Language
     - `analyze_multiliteracies()` - Multiple meaning-making modes
     - `analyze_multimodality()` - Visual-textual relationships
     - `analyze_rhetorical_listening()` - Empathy and cultural positioning
     - `analyze_code_meshing()` - Spanish-English integration patterns
     - `analyze_big_data()` - Pattern recognition and abstraction
     - `analyze_composing_with_ai()` - Self-referential positioning
   - Each returns:
     - `qualitative`: Observations, counts, categorizations
     - `quantitative`: Consistency score (0-1), alignment score (0-1)

4. **SentimentAnalyzer**
   - Simple word-based sentiment (positive/negative/neutral word lists)
   - Calculates polarity (-1 to 1), subjectivity (0 to 1), emotion label
   - Runs at three levels: overall, per-image, per-parameter

5. **SemanticStyleAnalyzer**
   - Cultural markers (Spanish terms, gestures, references)
   - Sentence complexity (avg length, max/min)
   - Word choices (emotional vs neutral, concrete vs abstract)
   - Grammatical structures (active/passive voice, questions)
   - Rhetorical devices (metaphor, simile, personification, repetition)
   - Code-switching implications per parameter

### Visualization Architecture

**Single-page application** with 4 views (no routing):

- **State management**: Global `state` object in `app.js`
- **View switching**: CSS class toggling (`.view.active`)
- **Data loading**: Fetch `analysis_results.json` on init

**Four views:**

1. **Text Navigation** (`#text-view`)
   - Dropdowns control display (LLM, segment, parameter)
   - Code-switching highlighting with regex replacement
   - Side panel shows sentiment metrics

2. **Word Clouds** (`#wordclouds-view`)
   - Tabs for Context/Abstraction/Concept
   - WordCloud2.js renders on canvas
   - Click word → show contexts across LLMs

3. **Concept Map** (`#conceptmap-view`)
   - D3.js v7 force-directed graph
   - Three node types: LLMs (blue), theories (green), themes (gold)
   - Four edge types: alignment, shared-theme, sentiment, tension
   - Drag handler keeps nodes fixed after dragging
   - Click node → detailed panel, hover → tooltip

4. **Compare LLMs** (`#compare-view`)
   - Three panels: text comparison, Chart.js charts, differences list
   - Radar/bar/line chart switching
   - Calculates differentiators dynamically

### JSON Output Structure

```javascript
{
  "llms": {
    "poe_chatbot": {
      "overall_stats": { total_responses, total_words },
      "sentiment": { average_polarity, average_subjectivity },
      "theoretical_analysis": { /* avg scores per theory */ },
      "image_responses": [
        {
          "segment_id": 1,
          "prompt_type": "AD-HOC",
          "prompt": "...",
          "full_response": "...",
          "overall_sentiment": { polarity, subjectivity, emotion },
          "parameters": {
            "context": {
              "text": "...",
              "themes": [{ word, count }],
              "sentiment": { ... },
              "semantic_style": { ... },
              "theoretical_analysis": {
                "srtol": { qualitative, quantitative },
                // ... 6 more theories
              }
            },
            "abstraction": { ... },
            "concept": { ... }
          }
        }
      ]
    },
    "chatgpt": { ... },
    "claude_ai": { ... }
  },
  "comparative_analysis": {
    "themes": {
      "context_themes": [{ word, count }],
      "abstraction_themes": [...],
      "concept_themes": [...],
      "unified_themes": [...]
    }
  }
}
```

## Key Design Decisions

### Multilingual Support
- Spanish stopwords excluded but culturally significant terms preserved
- Code-switching detection uses regex patterns for common Spanish words and ¿? syntax
- Sentiment analysis uses English word lists (limitation: doesn't handle Spanish sentiment separately)

### Theoretical Scoring
- **Consistency**: How reliably/frequently an LLM applies the framework
- **Alignment**: How well the output embodies the framework's principles
- Both scored 0-1, calculated from pattern frequencies normalized by text length

### Visualization Responsiveness
- CSS variables for theming (easy color scheme changes)
- Container margins: 6.25% (≈1 inch on standard screens)
- Breakpoints: 1024px (tablet), 768px (mobile)
- Base font: 20px desktop, 18px mobile
- High contrast: WCAG AAA (7:1 minimum ratio)

### D3 Force Simulation
- Nodes are draggable and stay fixed after release (not floating)
- Links filtered by checkbox selections (toggle edge types)
- Zoom/pan enabled on SVG
- Force parameters: charge -300, link distance 100, collision radius 40

## Important Patterns

### Adding a New Theoretical Framework

1. Add analyzer method to `TheoreticalAnalyzer` class:
   ```python
   def analyze_new_framework(self, text: str) -> Dict[str, Any]:
       # Count relevant markers
       markers = len(re.findall(r'pattern', text))
       consistency = min(1.0, markers / threshold)
       alignment = calculate_alignment(text)

       return {
           'qualitative': { /* observations */ },
           'quantitative': {
               'consistency_score': round(consistency, 3),
               'alignment_score': round(alignment, 3)
           }
       }
   ```

2. Call it in `main()` within the theories dict:
   ```python
   theories = {
       'srtol': theoretical_analyzer.analyze_srtol(param_text),
       # ... existing theories
       'new_framework': theoretical_analyzer.analyze_new_framework(param_text)
   }
   ```

3. Add to visualization comparison options in `index.html`:
   ```html
   <option value="new_framework">New Framework</option>
   ```

### Modifying the Concept Map

- Nodes added in `buildConceptMapData()` - push to `nodes` array
- Links added same function - push to `links` array with `type` property
- Node colors: update `getNodeColor(type)`
- Edge colors: update `getEdgeColor(type)`
- Edge filtering: add checkbox in HTML, update `enabledEdges` filter

### Debugging Analysis Issues

If analysis results look wrong:
1. Check `structured_data.json` - are responses parsed correctly?
2. Check `full_text.txt` - did Word extraction work?
3. Run individual analyzer methods in Python REPL with sample text
4. Check regex patterns - some special characters need escaping

## Cultural Context Preservation

**Critical**: This project analyzes Latino Women Rhetorics with code-meshing. When modifying analyzers:

1. **Never filter out Spanish terms** as "noise"
2. **Preserve code-switching patterns** - they're data, not errors
3. **Keep gesture descriptions** (leans, touches, snaps) - rhetorical markers for Poe responses
4. **Maintain distinction** between three LLM styles:
   - Poe: Intimate, code-meshed, gestural
   - ChatGPT: Formal, academic, structured
   - Claude: Analytical, comprehensive, neutral

## Testing Changes

No automated tests exist. Manual testing workflow:

1. **Analysis changes**:
   ```bash
   python3 analysis_engine.py
   # Check analysis_results.json size/structure
   # Verify key fields present
   ```

2. **Visualization changes**:
   - Open `index.html` in browser
   - Open DevTools console (check for JS errors)
   - Test all 4 views
   - Test responsive design (DevTools device emulation)
   - Verify accessibility (contrast, keyboard navigation)

3. **Data extraction changes**:
   ```bash
   python3 extract_document.py
   # Check full_text.txt looks correct
   python3 detailed_parser.py
   # Check structured_data.json has all segments
   ```

## Performance Considerations

- `analysis_results.json` is 382KB - loads quickly
- Word cloud rendering can lag with >100 words - limited to top 50
- Concept map force simulation starts hot (alpha 1.0) for fast initial layout
- D3 drag keeps nodes fixed (fx/fy set) to prevent re-simulation overhead
- Chart.js charts destroyed before recreation to prevent memory leaks

## Academic Context

This is research for ENC 5930 analyzing:
- How AI architectures (ad-hoc, generative, agentic) construct rhetorical responses
- Code-meshing and multilingual expression in AI text
- Distant reading methodologies for computational rhetoric
- Visual imagery interpretation through cultural/linguistic positioning

When making changes, preserve the academic integrity of the analysis frameworks.
