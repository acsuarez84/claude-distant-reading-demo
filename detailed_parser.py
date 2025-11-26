#!/usr/bin/env python3
"""
Detailed parser to extract individual LLM responses with Context, Abstraction, Concept sections.
"""

import json
import re
from typing import List, Dict, Any, Tuple


def load_segments() -> List[Dict[str, Any]]:
    """Load parsed segments."""
    with open('segments_parsed.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_prompt(text: str) -> str:
    """Extract the image prompt/question from segment text."""
    # Common prompt patterns
    patterns = [
        r'(Can you .*?\?)',
        r'(Given this actual .*?\?)',
        r'(What is .*?\?)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            prompt = match.group(1)
            # Clean up
            prompt = re.sub(r'\s+', ' ', prompt).strip()
            if len(prompt) < 500:  # Reasonable prompt length
                return prompt

    return "Unknown prompt"


def split_by_llm(text: str) -> Tuple[str, str, str]:
    """
    Split segment text into three LLM responses.
    Returns: (poe_text, chatgpt_text, claude_text)
    """

    # Poe.com Chatbot typically starts with gestures/actions in italics
    # Example: "leans in, looking at the photo carefully"

    # ChatGPT typically starts with formal phrases
    # Example: "Here is a description", "Given the actual context"

    # Claude.AI typically starts with analytical phrases
    # Example: "Looking at this image", "Expanded Context"

    # Find potential split points
    # Look for patterns that indicate start of each LLM

    poe_start_patterns = [
        r'(leans in[^\.]{0,100}\.)',
        r'(pauses[^\.]{0,100}\.)',
        r'(nods slowly[^\.]{0,100}\.)',
        r'(settles back[^\.]{0,100}\.)',
        r'(shifts posture[^\.]{0,100}\.)',
        r'(takes a breath[^\.]{0,100}\.)',
        r'(Ay, okay, mira)',
        r'(Ahh[^\.]{0,100}\.)',
    ]

    chatgpt_start_patterns = [
        r'(Here is a description)',
        r'(Below is an updated)',
        r'(Given the actual context)',
        r'(Here are the additional)',
        r'(Abstraction \(Based on)',
        r'(Abstraction \(Given)',
    ]

    claude_start_patterns = [
        r'(Looking at this image through)',
        r'(Expanded Context:)',
        r'(Expanded Breakdown)',
        r'(Given the Full Context)',
        r'(Context \(Inferred)',
    ]

    # Find all matches
    poe_matches = []
    for pattern in poe_start_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            poe_matches.append(match.start())

    chatgpt_matches = []
    for pattern in chatgpt_start_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            chatgpt_matches.append(match.start())

    claude_matches = []
    for pattern in claude_start_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            claude_matches.append(match.start())

    # Get first match for each
    poe_start = min(poe_matches) if poe_matches else 0
    chatgpt_start = min(chatgpt_matches) if chatgpt_matches else len(text)
    claude_start = min(claude_matches) if claude_matches else len(text)

    # Sort the positions
    positions = sorted([
        (poe_start, 'poe'),
        (chatgpt_start, 'chatgpt'),
        (claude_start, 'claude')
    ])

    # Extract text for each LLM based on positions
    llm_texts = {'poe': '', 'chatgpt': '', 'claude': ''}

    for i, (pos, llm) in enumerate(positions):
        if i < len(positions) - 1:
            next_pos = positions[i + 1][0]
            llm_texts[llm] = text[pos:next_pos].strip()
        else:
            llm_texts[llm] = text[pos:].strip()

    return llm_texts['poe'], llm_texts['chatgpt'], llm_texts['claude']


def extract_parameters(text: str) -> Dict[str, str]:
    """
    Extract Context, Abstraction, and Concept sections from LLM response.
    """
    parameters = {
        'context': '',
        'abstraction': '',
        'concept': '',
        'full_text': text
    }

    # Look for explicit markers
    # Context: ... Abstraction: ... Concept: ...

    # Try to find these sections
    context_pattern = r'Context:?\s*(.*?)(?=Abstraction:|Concept:|$)'
    abstraction_pattern = r'Abstraction:?\s*(.*?)(?=Concept:|$)'
    concept_pattern = r'Concept:?\s*(.*?)$'

    context_match = re.search(context_pattern, text, re.DOTALL | re.IGNORECASE)
    abstraction_match = re.search(abstraction_pattern, text, re.DOTALL | re.IGNORECASE)
    concept_match = re.search(concept_pattern, text, re.DOTALL | re.IGNORECASE)

    if context_match:
        parameters['context'] = context_match.group(1).strip()
    if abstraction_match:
        parameters['abstraction'] = abstraction_match.group(1).strip()
    if concept_match:
        parameters['concept'] = concept_match.group(1).strip()

    # If no explicit sections found, use full text as context
    if not any([parameters['context'], parameters['abstraction'], parameters['concept']]):
        parameters['context'] = text

    return parameters


def parse_all_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Parse all segments into structured data."""
    parsed_data = []

    for i, segment in enumerate(segments):
        print(f"\nProcessing Segment {i + 1} ({segment['prompt_type']})...")

        text = segment['text']

        # Extract prompt
        prompt = extract_prompt(text)
        print(f"  Prompt: {prompt[:80]}...")

        # Split by LLM
        poe_text, chatgpt_text, claude_text = split_by_llm(text)

        print(f"  Poe text: {len(poe_text)} chars")
        print(f"  ChatGPT text: {len(chatgpt_text)} chars")
        print(f"  Claude text: {len(claude_text)} chars")

        # Extract parameters from each
        poe_params = extract_parameters(poe_text)
        chatgpt_params = extract_parameters(chatgpt_text)
        claude_params = extract_parameters(claude_text)

        # Build structured segment
        parsed_segment = {
            'segment_id': i + 1,
            'prompt_type': segment['prompt_type'],
            'prompt': prompt,
            'llm_responses': {
                'poe_chatbot': poe_params,
                'chatgpt': chatgpt_params,
                'claude_ai': claude_params
            }
        }

        parsed_data.append(parsed_segment)

    return parsed_data


def display_for_confirmation(parsed_data: List[Dict[str, Any]]) -> None:
    """Display parsed data for user confirmation."""
    print("\n\n" + "="*80)
    print("PARSED DATA - CONFIRMATION REQUIRED")
    print("="*80)

    for segment in parsed_data:
        print(f"\n{'═'*80}")
        print(f"SEGMENT {segment['segment_id']}: {segment['prompt_type']}")
        print(f"{'═'*80}")
        print(f"\nPrompt: {segment['prompt']}")

        for llm_name, params in segment['llm_responses'].items():
            print(f"\n  ┌─ {llm_name.upper().replace('_', ' ')} ─")
            print(f"  │ Full text length: {len(params['full_text'])} chars")
            print(f"  │ Context: {len(params['context'])} chars")
            print(f"  │ Abstraction: {len(params['abstraction'])} chars")
            print(f"  │ Concept: {len(params['concept'])} chars")

            if params['context']:
                print(f"  │ Context preview: {params['context'][:100]}...")
            if params['abstraction']:
                print(f"  │ Abstraction preview: {params['abstraction'][:100]}...")
            if params['concept']:
                print(f"  │ Concept preview: {params['concept'][:100]}...")

            print("  └─")

    print("\n" + "="*80)
    response = input("\nDoes this structure look correct? (y/n): ").strip().lower()

    if response == 'y':
        print("✓ Structure confirmed!")
        return True
    else:
        print("❌ Structure needs adjustment")
        return False


if __name__ == '__main__':
    print("Loading segments...")
    segments = load_segments()

    print(f"Loaded {len(segments)} segments")

    # Parse all segments
    parsed_data = parse_all_segments(segments)

    # Display for confirmation
    confirmed = display_for_confirmation(parsed_data)

    # Save parsed data
    with open('structured_data.json', 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)

    print(f"\nStructured data saved to: structured_data.json")
