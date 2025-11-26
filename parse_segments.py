#!/usr/bin/env python3
"""
Parse the LLM outputs document into structured segments.
This script identifies individual image prompts and separates responses by LLM.
"""

import json
import re
from typing import List, Dict, Any


def load_full_text() -> str:
    """Load the extracted full text."""
    with open('full_text.txt', 'r', encoding='utf-8') as f:
        return f.read()


def manual_segment_extraction(text: str) -> List[Dict[str, Any]]:
    """
    Manually extract segments based on the document structure.
    The document has: prompting type → prompt → Poe response → ChatGPT response → Claude response
    """

    # Define markers for different prompting types
    prompting_types = ['AD-HOC', 'FEW-SHOT', 'ZERO-SHOT']

    segments = []

    # Split by prompting type markers
    # Find all instances of prompting types
    current_pos = 0
    prompt_number = 1

    # Manual extraction based on visible patterns
    # Looking at the text, I can see:
    # 1. First image is AD-HOC with prompt "Can you describe this picture..."
    # 2. Then AD-HOC 2 with "Can you further breakdown..."
    # 3. Then ZERO-SHOT with "Given this actual context..."
    # 4. Then FEW-SHOT variations

    # Let me find all the major sections

    # Find all instances where responses start
    poe_pattern = r'(leans in|pauses|nods slowly|settles back|shifts posture|takes a breath)'
    chatgpt_pattern = r'Here is a description|Given the actual|Below is an updated|Abstraction \(Given'
    claude_pattern = r'Looking at this image through|Expanded Context|Given the Full Context'

    # Split by major prompt types
    parts = re.split(r'(AD-HOC|FEW-SHOT|ZERO-SHOT)', text)

    current_segment = None

    for i, part in enumerate(parts):
        if part in prompting_types:
            # New prompting method detected
            if current_segment:
                segments.append(current_segment)

            current_segment = {
                'prompt_type': part,
                'prompt_number': prompt_number,
                'text': '',
                'responses': {}
            }
            prompt_number += 1
        elif current_segment:
            current_segment['text'] += part

    if current_segment:
        segments.append(current_segment)

    return segments


def extract_llm_responses(segment_text: str) -> Dict[str, Dict[str, str]]:
    """
    Extract individual LLM responses from a segment.
    Each response should have Context, Abstraction, and Concept sections.
    """
    responses = {
        'poe_chatbot': {'full_text': '', 'context': '', 'abstraction': '', 'concept': ''},
        'chatgpt': {'full_text': '', 'context': '', 'abstraction': '', 'concept': ''},
        'claude_ai': {'full_text': '', 'context': '', 'abstraction': '', 'concept': ''}
    }

    # Poe.com Chatbot has distinctive markers: gesture descriptions, Spanish phrases
    # ChatGPT has formal structure: "Here is a description..."
    # Claude.AI has analytical structure: "Looking at this image..."

    # Try to split by identifying each LLM's characteristic opening

    # Poe typically starts with action: "leans in", "pauses", "nods slowly", etc.
    poe_markers = [
        'leans in, looking at the photo',
        'pauses, eyebrows raising',
        'nods slowly, understanding clicking',
        'settles back, looking at the image',
        'shifts posture, reconsidering',
        'takes a breath, recentering'
    ]

    # ChatGPT markers
    chatgpt_markers = [
        'Here is a description of the image',
        'Given the actual context',
        'Below is an updated interpretation',
        'Here are the additional contextual'
    ]

    # Claude markers
    claude_markers = [
        'Looking at this image through your three parameters:',
        'Expanded Context:',
        'Given the Full Context'
    ]

    # Extract prompt
    prompt_match = re.search(r'(Can you .*?\?|Given this actual .*?\?)', segment_text, re.DOTALL)
    prompt = prompt_match.group(1) if prompt_match else ''

    # This is complex - for now, let's return the structure
    return responses, prompt


def display_segments_for_confirmation(segments: List[Dict[str, Any]]) -> None:
    """Display parsed segments for user confirmation."""
    print("\n" + "="*80)
    print("SEGMENT DETECTION - CONFIRMATION NEEDED")
    print("="*80)
    print(f"\nDetected {len(segments)} segments\n")

    for i, seg in enumerate(segments):
        print(f"\n{'─'*80}")
        print(f"Segment {i + 1}")
        print(f"Prompting Type: {seg.get('prompt_type', 'Unknown')}")
        print(f"Prompt Number: {seg.get('prompt_number', 'Unknown')}")
        print(f"\nText Preview (first 300 chars):")
        print(seg['text'][:300].strip())
        print("\n...")
        print("\n" + "─"*80)

        # Ask for confirmation
        response = input(f"\nIs this a valid segment? (y/n/edit): ").strip().lower()

        if response == 'n':
            seg['valid'] = False
            print("❌ Segment marked as invalid")
        elif response == 'edit':
            print("\nSegment editing not yet implemented.")
            print("For now, marking as valid and continuing...")
            seg['valid'] = True
        else:
            seg['valid'] = True
            print("✓ Segment confirmed")

    # Filter valid segments
    valid_segments = [s for s in segments if s.get('valid', True)]
    print(f"\n\n{'='*80}")
    print(f"Total valid segments: {len(valid_segments)}")
    print("="*80)

    return valid_segments


if __name__ == '__main__':
    print("Loading extracted text...")
    text = load_full_text()

    print("Parsing segments...")
    segments = manual_segment_extraction(text)

    print(f"\nFound {len(segments)} potential segments")

    # Display for confirmation
    # valid_segments = display_segments_for_confirmation(segments)

    # For now, just save all segments
    with open('segments_parsed.json', 'w', encoding='utf-8') as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)

    print(f"\nParsed segments saved to: segments_parsed.json")

    # Display summary
    print("\n" + "="*80)
    print("SEGMENT SUMMARY")
    print("="*80)
    for i, seg in enumerate(segments):
        print(f"\nSegment {i + 1}: {seg.get('prompt_type', 'Unknown')} (Prompt #{seg.get('prompt_number', '?')})")
        print(f"  Text length: {len(seg['text'])} characters")
