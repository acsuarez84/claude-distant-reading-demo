#!/usr/bin/env python3
"""
Extract and parse the Word document containing LLM outputs.
This script identifies segment boundaries and structures the data.
"""

import zipfile
import xml.etree.ElementTree as ET
import json
import re
from typing import List, Dict, Any


def extract_text_from_docx(docx_path: str) -> str:
    """Extract raw text from Word document."""
    with zipfile.ZipFile(docx_path) as docx:
        xml_content = docx.read('word/document.xml')
        tree = ET.fromstring(xml_content)

        texts = []
        for elem in tree.iter():
            if elem.tag.endswith('}t'):
                if elem.text:
                    texts.append(elem.text)

        return ''.join(texts)


def identify_segment_boundaries(text: str) -> List[Dict[str, Any]]:
    """
    Identify potential segment boundaries in the document.
    Returns a list of segments with metadata for user confirmation.
    """
    segments = []

    # Patterns that might indicate segment boundaries
    patterns = {
        'llm_header': r'(Poe\.com Chatbot|Chat GPT|ChatGPT|Claude\.AI)',
        'prompt_marker': r'(IMAGE PROMPT|AD-HOC|Can you describe)',
        'context_marker': r'Context:',
        'abstraction_marker': r'Abstraction:',
        'concept_marker': r'Concept:',
        'section_break': r'\n\n\n+',  # Multiple newlines
    }

    # Split text into potential segments
    # Look for patterns that indicate new prompts or responses
    lines = text.split('\n')

    current_segment = {
        'start_line': 0,
        'text': '',
        'markers': [],
        'llm': None,
        'prompt_type': None,
    }

    segment_id = 0

    for i, line in enumerate(lines):
        # Check for LLM identifiers
        llm_match = re.search(patterns['llm_header'], line, re.IGNORECASE)
        if llm_match:
            # Save previous segment if it has content
            if current_segment['text'].strip():
                current_segment['end_line'] = i
                current_segment['segment_id'] = segment_id
                segments.append(current_segment.copy())
                segment_id += 1

            # Start new segment
            current_segment = {
                'start_line': i,
                'text': line + '\n',
                'markers': ['llm_header'],
                'llm': llm_match.group(1),
                'prompt_type': None,
            }
            continue

        # Check for prompt markers
        prompt_match = re.search(patterns['prompt_marker'], line, re.IGNORECASE)
        if prompt_match:
            current_segment['markers'].append('prompt_marker')
            current_segment['prompt_type'] = prompt_match.group(1)

        # Add line to current segment
        current_segment['text'] += line + '\n'

    # Add final segment
    if current_segment['text'].strip():
        current_segment['end_line'] = len(lines)
        current_segment['segment_id'] = segment_id
        segments.append(current_segment)

    return segments


def parse_response_structure(text: str) -> Dict[str, str]:
    """
    Parse a response into Context, Abstraction, and Concept sections.
    """
    sections = {
        'context': '',
        'abstraction': '',
        'concept': '',
        'full_text': text
    }

    # Find section markers
    context_match = re.search(r'Context:(.*?)(?=Abstraction:|Concept:|$)', text, re.DOTALL | re.IGNORECASE)
    abstraction_match = re.search(r'Abstraction:(.*?)(?=Concept:|$)', text, re.DOTALL | re.IGNORECASE)
    concept_match = re.search(r'Concept:(.*?)$', text, re.DOTALL | re.IGNORECASE)

    if context_match:
        sections['context'] = context_match.group(1).strip()
    if abstraction_match:
        sections['abstraction'] = abstraction_match.group(1).strip()
    if concept_match:
        sections['concept'] = concept_match.group(1).strip()

    return sections


def display_segments_for_confirmation(segments: List[Dict[str, Any]]) -> None:
    """Display segments for user confirmation."""
    print("\n" + "="*80)
    print("SEGMENT BOUNDARY DETECTION")
    print("="*80)
    print(f"\nFound {len(segments)} potential segments\n")

    for seg in segments:
        print(f"\n{'─'*80}")
        print(f"Segment ID: {seg['segment_id']}")
        print(f"Lines: {seg['start_line']} - {seg['end_line']}")
        print(f"LLM: {seg['llm'] or 'Unknown'}")
        print(f"Prompt Type: {seg['prompt_type'] or 'Unknown'}")
        print(f"Markers: {', '.join(seg['markers'])}")
        print(f"\nPreview (first 200 chars):")
        print(seg['text'][:200].replace('\n', ' '))
        print("...")


if __name__ == '__main__':
    # Extract text
    print("Extracting text from Word document...")
    text = extract_text_from_docx('ENC 5930-Thinking Text Project-LLM Outputs.docx')

    print(f"\nExtracted {len(text)} characters")
    print(f"Approximate word count: {len(text.split())}")

    # Identify segments
    print("\nIdentifying segment boundaries...")
    segments = identify_segment_boundaries(text)

    # Display for confirmation
    display_segments_for_confirmation(segments)

    # Save raw segments for review
    with open('segments_raw.json', 'w', encoding='utf-8') as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)

    print(f"\n\n{'='*80}")
    print("Raw segments saved to: segments_raw.json")
    print("="*80)
