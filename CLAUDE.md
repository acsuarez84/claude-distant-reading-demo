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
python3 extract_document.py           # Extract text from Word document
python3 detailed_parser.py            # Parse into structured segments
python3 analysis_engine.py            # Run comprehensive analysis (generates analysis_results.json)
python3 generate_markdown_reports.py  # Generate human-readable markdown reports (optional)

# Quick re-run (if structured_data.json exists)
python3 analysis_engine.py            # Only regenerate analysis_results.json
python3 generate_markdown_reports.py  # Only regenerate markdown reports
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
Complete Analysis (analysis_results.json - 602KB)
    - Theme extraction
    - Sentiment analysis (multilingual)
    - Semantic style analysis
    - 7 theoretical framework scores + detailed analysis
    ↓ app.js loads / generate_markdown_reports.py
Interactive Visualization (index.html) + Markdown Reports
```

### Analysis Engine Architecture

The `analysis_engine.py` contains five major analyzers, with theoretical analysis templates in `theoretical_frameworks.py`:

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
     - `analyze_srtol()` - Students' Rights to Their Own Language (CCCC 1974, Smitherman 1977, Young 2009-2011)
     - `analyze_multiliteracies()` - Multiple meaning-making modes (New London Group 1996, Cope & Kalantzis)
     - `analyze_multimodality()` - Visual-textual relationships (Kress & van Leeuwen 1996-2006, Shipka 2011)
     - `analyze_rhetorical_listening()` - Empathy and cultural positioning (Ratcliffe 2005, Glenn 2004, Glenn & Ratcliffe 2011)
     - `analyze_code_meshing()` - Spanish-English integration patterns (Canagarajah 2006-2013, Young 2004-2011)
     - `analyze_big_data()` - Pattern recognition and abstraction (Moretti 2005-2013, Hayles 2012)
     - `analyze_composing_with_ai()` - Self-referential positioning (Vee 2017, Hayles 2005-2012, Boyle 2018)
   - Each returns:
     - `qualitative`: Observations, counts, categorizations
     - `quantitative`: Consistency score (0-1), alignment score (0-1), marker_words list
     - `analysis`: Pattern description, rhetorical interpretation, cultural/political implications, key examples, theorists cited

4. **TheoreticalFrameworks** (`theoretical_frameworks.py`)
   - Pre-written analysis templates grounded in academic theory
   - Each framework generates:
     - `pattern_description`: What the data shows
     - `rhetorical_interpretation`: What it means for meaning-making (with direct quotes from theorists)
     - `cultural_political_implications`: What ideological work it does
     - `key_examples`: Textual evidence from the response
     - `theorists_cited`: List of key scholars cited
   - Example concepts integrated:
     - Glenn's "productive silence" vs "silencing"
     - Ratcliffe's "standing under" and "rhetorical eavesdropping"
     - Young's "code-meshing" vs "code-switching"
     - Smitherman's "linguistic push-pull"

5. **SentimentAnalyzer**
   - Simple word-based sentiment (positive/negative/neutral word lists)
   - Calculates polarity (-1 to 1), subjectivity (0 to 1), emotion label
   - Runs at three levels: overall, per-image, per-parameter

6. **SemanticStyleAnalyzer**
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
   - Click node → detailed panel with tabs:
     - **Scores tab**: Consistency/alignment metrics
     - **Detailed Analysis tab**: Full theoretical analysis (pattern description, rhetorical interpretation, cultural/political implications, examples, theorists)
   - Hover → tooltip

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
                "srtol": {
                  qualitative,
                  quantitative,
                  analysis: {
                    pattern_description,
                    rhetorical_interpretation,
                    cultural_political_implications,
                    key_examples,
                    theorists_cited
                  }
                },
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

1. Add analysis template to `TheoreticalFrameworks` class in `theoretical_frameworks.py`:
   ```python
   @staticmethod
   def new_framework_analysis(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
       """
       New Framework

       Key Theorists:
       - Author (Year) - Work Title

       Focus: What this framework analyzes
       """
       qual = metrics['qualitative']
       # Extract relevant metrics

       # Pattern Description
       pattern = f"""The response demonstrates..."""

       # Rhetorical Interpretation (cite theorists)
       interpretation = f"""This aligns with Author's (Year) concept of..."""

       # Cultural/Political Implications
       implications = f"""The political stakes are..."""

       return {
           'pattern_description': pattern.strip(),
           'rhetorical_interpretation': interpretation.strip(),
           'cultural_political_implications': implications.strip(),
           'key_examples': [],
           'theorists_cited': ['Author (Year)']
       }
   ```

2. Add analyzer method to `TheoreticalAnalyzer` class in `analysis_engine.py`:
   ```python
   def analyze_new_framework(self, text: str) -> Dict[str, Any]:
       # Count relevant markers
       markers = len(re.findall(r'pattern', text))
       marker_words = [...]  # Extract specific words

       consistency = min(1.0, markers / threshold)
       alignment = calculate_alignment(text)

       qualitative = { /* observations */ }
       quantitative = {
           'consistency_score': round(consistency, 3),
           'alignment_score': round(alignment, 3),
           'marker_words': marker_words
       }

       # Generate theoretical analysis
       analysis = self.frameworks.new_framework_analysis(
           metrics={'qualitative': qualitative, 'quantitative': quantitative},
           text=text
       )

       return {
           'qualitative': qualitative,
           'quantitative': quantitative,
           'analysis': analysis
       }
   ```

3. Call it in `main()` within the theories dict:
   ```python
   theories = {
       'srtol': theoretical_analyzer.analyze_srtol(param_text),
       # ... existing theories
       'new_framework': theoretical_analyzer.analyze_new_framework(param_text)
   }
   ```

4. Add to visualization comparison options in `index.html`:
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

## Output Files

The analysis pipeline generates multiple output files:

1. **analysis_results.json (602KB)**: Complete machine-readable analysis with theoretical interpretations
2. **analysis_summary.md (~30KB)**: Human-readable detailed analysis for each LLM with sample theoretical interpretations
3. **comparative_analysis.md (~10KB)**: Cross-LLM comparison organized by theoretical framework

## Performance Considerations

- `analysis_results.json` is 602KB - loads quickly
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
