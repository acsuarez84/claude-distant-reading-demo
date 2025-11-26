# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project for ENC 5930 analyzing how different Large Language Models (LLMs) interpret visual imagery through the analytical framework of **Context, Abstraction, and Concept**, with a focus on **Latino Women Rhetorics**.

The project compares rhetorical strategies across three AI systems:
- **Poe.com Chatbot** (ad-hoc responses)
- **ChatGPT** (generative approach)
- **Claude.AI** (agentic approach)

The repository name "claude-distant-reading-demo" indicates the eventual goal is to apply computational distant reading methodologies to analyze patterns across LLM-generated responses.

## Current State

The repository currently contains:
- `ENC 5930-Thinking Text Project-LLM Outputs.docx` - A Word document containing image prompts and LLM responses (~39,000 characters, ~5,900 words)

This is a research data document containing multiple image analysis responses from different AI systems, each structured around the three analytical parameters (Context, Abstraction, Concept).

## Expected Development Direction

Based on the project's focus on distant reading, future development will likely involve:

1. **Data Extraction & Processing**
   - Converting the Word document into structured data formats (JSON, CSV, or similar)
   - Parsing and separating responses by AI system and analytical framework
   - Extracting metadata (image identifiers, AI system, response type)

2. **Text Analysis Tools**
   - Computational analysis of rhetorical patterns across different LLM responses
   - Comparative analysis tools for Context vs. Abstraction vs. Concept interpretations
   - Identification of language patterns specific to each AI system

3. **Distant Reading Methodologies**
   - Text mining and natural language processing
   - Pattern recognition across multiple image-response pairs
   - Comparative rhetorical analysis tools

## Working with the Data

### Extracting Text from the Word Document

Use Python's `zipfile` and `xml.etree.ElementTree` to extract text:

```python
import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('ENC 5930-Thinking Text Project-LLM Outputs.docx') as docx:
    xml_content = docx.read('word/document.xml')
    tree = ET.fromstring(xml_content)

    texts = []
    for elem in tree.iter():
        if elem.tag.endswith('}t'):
            if elem.text:
                texts.append(elem.text)

    full_text = ''.join(texts)
```

Alternatively, use `python-docx` library if available:
```bash
pip install python-docx
```

## Academic Context

This is an academic research project focused on:
- **Distant Reading**: Computational analysis of large-scale textual data
- **Rhetoric and Composition**: How different AI systems construct rhetorical responses
- **Latino Women Rhetorics**: Cultural and linguistic dimensions in AI-generated text
- **Multimodal Analysis**: Intersection of visual imagery and textual interpretation

## Key Considerations

When developing tools for this project:

1. **Preserve Cultural Context**: The responses include code-switching between English and Spanish, and cultural references that are central to the analysis
2. **Maintain Response Integrity**: Each AI system's response should be analyzed as a complete rhetorical artifact
3. **Structured Analysis**: Keep the three-part framework (Context, Abstraction, Concept) as the organizing principle
4. **Comparative Framework**: Design tools to facilitate comparison across AI systems while respecting their different rhetorical approaches
