#!/usr/bin/env python3
"""
Generate Markdown Reports from Analysis Results

Creates two markdown files:
1. analysis_summary.md - Detailed analysis for each LLM
2. comparative_analysis.md - Cross-LLM theoretical comparison
"""

import json
from typing import Dict, Any


def load_analysis_results():
    """Load the analysis results JSON."""
    with open('analysis_results.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_llm_section(llm_name: str, llm_data: Dict[str, Any]) -> str:
    """Generate markdown section for a single LLM."""
    display_name = llm_name.replace('_', ' ').title()

    md = f"\n## {display_name}\n\n"

    # Overall stats
    stats = llm_data.get('overall_stats', {})
    md += f"**Total Responses:** {stats.get('total_responses', 0)}  \n"
    md += f"**Total Words:** {stats.get('total_words', 0)}  \n"

    # Sentiment
    sentiment = llm_data.get('sentiment', {})
    md += f"**Average Sentiment:** {sentiment.get('average_polarity', 0):.2f} ({sentiment.get('overall_emotion', 'neutral')})  \n"
    md += f"**Subjectivity:** {sentiment.get('average_subjectivity', 0):.2f}  \n\n"

    # Theoretical analysis summary
    md += "### Theoretical Framework Scores\n\n"
    theoretical = llm_data.get('theoretical_analysis', {})

    for theory, scores in theoretical.items():
        theory_display = theory.replace('_', ' ').title()
        consistency = scores.get('avg_consistency', 0)
        alignment = scores.get('avg_alignment', 0)
        md += f"- **{theory_display}**: Consistency: {consistency:.2f} | Alignment: {alignment:.2f}\n"

    md += "\n"

    # Sample detailed analysis
    md += "### Sample Theoretical Analysis\n\n"
    md += "_Analysis from first image response (Context parameter):_\n\n"

    if llm_data.get('image_responses') and len(llm_data['image_responses']) > 0:
        first_response = llm_data['image_responses'][0]
        param_data = first_response.get('parameters', {}).get('context')

        if param_data and param_data.get('theoretical_analysis'):
            for theory_key, theory_data in param_data['theoretical_analysis'].items():
                if theory_data.get('analysis'):
                    analysis = theory_data['analysis']
                    theory_display = theory_key.replace('_', ' ').title()

                    md += f"#### {theory_display}\n\n"

                    md += f"**Pattern Description:**  \n{analysis.get('pattern_description', '')} \n\n"

                    md += f"**Rhetorical Interpretation:**  \n{analysis.get('rhetorical_interpretation', '')} \n\n"

                    md += f"**Cultural/Political Implications:**  \n{analysis.get('cultural_political_implications', '')} \n\n"

                    if analysis.get('key_examples'):
                        md += "**Examples:**\n"
                        for example in analysis['key_examples'][:3]:
                            md += f"- {example}\n"
                        md += "\n"

                    if analysis.get('theorists_cited'):
                        md += f"**Key Theorists:** {', '.join(analysis['theorists_cited'])}\n\n"

                    md += "---\n\n"

    return md


def generate_analysis_summary(data: Dict[str, Any]) -> str:
    """Generate the main analysis summary markdown."""
    md = "# Distant Reading Analysis: LLM Rhetorical Interpretation\n\n"
    md += "## Summary Report\n\n"
    md += "_This report presents detailed theoretical analysis of how three LLM systems "
    md += "(Poe.com Chatbot, ChatGPT, Claude.AI) interpret visual imagery through the "
    md += "analytical frameworks of Context, Abstraction, and Concept in Latino Women Rhetorics._\n\n"

    md += "---\n\n"

    # Generate section for each LLM
    llms = data.get('llms', {})
    for llm_name in ['poe_chatbot', 'chatgpt', 'claude_ai']:
        if llm_name in llms:
            md += generate_llm_section(llm_name, llms[llm_name])

    # Comparative themes
    md += "\n## Comparative Theme Analysis\n\n"
    comparative = data.get('comparative_analysis', {}).get('themes', {})

    if comparative.get('context_themes'):
        md += "### Top Context Themes\n\n"
        for theme in comparative['context_themes'][:10]:
            md += f"- **{theme['word']}**: {theme['count']} occurrences\n"
        md += "\n"

    if comparative.get('abstraction_themes'):
        md += "### Top Abstraction Themes\n\n"
        for theme in comparative['abstraction_themes'][:10]:
            md += f"- **{theme['word']}**: {theme['count']} occurrences\n"
        md += "\n"

    if comparative.get('concept_themes'):
        md += "### Top Concept Themes\n\n"
        for theme in comparative['concept_themes'][:10]:
            md += f"- **{theme['word']}**: {theme['count']} occurrences\n"
        md += "\n"

    return md


def generate_comparative_analysis(data: Dict[str, Any]) -> str:
    """Generate cross-LLM comparative analysis markdown."""
    md = "# Comparative Theoretical Analysis Across LLMs\n\n"
    md += "_Cross-system comparison of rhetorical strategies and theoretical alignment._\n\n"

    md += "---\n\n"

    # Theory-by-theory comparison
    theories = [
        ('srtol', "Students' Rights to Their Own Language"),
        ('multiliteracies', 'Multiliteracies'),
        ('multimodality', 'Multimodality'),
        ('rhetorical_listening', 'Rhetorical Listening'),
        ('code_meshing', 'Code-Meshing'),
        ('big_data', 'Big Data / Computational Analysis'),
        ('composing_with_ai', 'Composing with AI')
    ]

    llms = data.get('llms', {})

    for theory_key, theory_name in theories:
        md += f"## {theory_name}\n\n"

        # Scores comparison table
        md += "### Alignment Scores\n\n"
        md += "| LLM | Consistency | Alignment |\n"
        md += "|-----|-------------|----------|\n"

        for llm_name in ['poe_chatbot', 'chatgpt', 'claude_ai']:
            if llm_name in llms:
                display_name = llm_name.replace('_', ' ').title()
                theoretical = llms[llm_name].get('theoretical_analysis', {})
                scores = theoretical.get(theory_key, {})
                consistency = scores.get('avg_consistency', 0)
                alignment = scores.get('avg_alignment', 0)
                md += f"| {display_name} | {consistency:.2f} | {alignment:.2f} |\n"

        md += "\n"

        # Comparative analysis
        md += "### How Each LLM Applies This Framework\n\n"

        for llm_name in ['poe_chatbot', 'chatgpt', 'claude_ai']:
            if llm_name in llms:
                display_name = llm_name.replace('_', ' ').title()
                llm_data = llms[llm_name]

                # Get sample analysis
                if llm_data.get('image_responses') and len(llm_data['image_responses']) > 0:
                    first_response = llm_data['image_responses'][0]
                    param_data = first_response.get('parameters', {}).get('context')

                    if param_data and param_data.get('theoretical_analysis'):
                        theory_data = param_data['theoretical_analysis'].get(theory_key)

                        if theory_data and theory_data.get('analysis'):
                            analysis = theory_data['analysis']

                            md += f"#### {display_name}\n\n"
                            md += f"**Pattern:** {analysis.get('pattern_description', '')} \n\n"

                            # Just first sentence of interpretation
                            interpretation = analysis.get('rhetorical_interpretation', '')
                            first_sentence = interpretation.split('.')[0] + '.'
                            md += f"**Interpretation:** {first_sentence}\n\n"

        md += "---\n\n"

    # Overall comparison
    md += "## Overall Comparative Insights\n\n"

    md += "### Code-Switching and Linguistic Diversity\n\n"
    md += "Comparing how each LLM handles multilingual expression:\n\n"

    for llm_name in ['poe_chatbot', 'chatgpt', 'claude_ai']:
        if llm_name in llms:
            display_name = llm_name.replace('_', ' ').title()
            theoretical = llms[llm_name].get('theoretical_analysis', {})

            srtol = theoretical.get('srtol', {})
            code_meshing = theoretical.get('code_meshing', {})

            md += f"- **{display_name}**: SRTOL Alignment: {srtol.get('avg_alignment', 0):.2f} | "
            md += f"Code-Meshing Consistency: {code_meshing.get('avg_consistency', 0):.2f}\n"

    md += "\n### Multimodal Engagement\n\n"
    md += "Comparing how each LLM integrates multiple meaning-making modes:\n\n"

    for llm_name in ['poe_chatbot', 'chatgpt', 'claude_ai']:
        if llm_name in llms:
            display_name = llm_name.replace('_', ' ').title()
            theoretical = llms[llm_name].get('theoretical_analysis', {})

            multiliteracies = theoretical.get('multiliteracies', {})
            multimodality = theoretical.get('multimodality', {})

            md += f"- **{display_name}**: Multiliteracies: {multiliteracies.get('avg_alignment', 0):.2f} | "
            md += f"Multimodality: {multimodality.get('avg_alignment', 0):.2f}\n"

    md += "\n### AI Self-Positioning\n\n"
    md += "How each LLM positions itself rhetorically:\n\n"

    for llm_name in ['poe_chatbot', 'chatgpt', 'claude_ai']:
        if llm_name in llms:
            display_name = llm_name.replace('_', ' ').title()
            theoretical = llms[llm_name].get('theoretical_analysis', {})

            ai_composing = theoretical.get('composing_with_ai', {})

            md += f"- **{display_name}**: Consistency: {ai_composing.get('avg_consistency', 0):.2f} | "
            md += f"Alignment: {ai_composing.get('avg_alignment', 0):.2f}\n"

    md += "\n"

    return md


def main():
    """Generate both markdown reports."""
    print("Loading analysis results...")
    data = load_analysis_results()

    print("Generating analysis_summary.md...")
    summary = generate_analysis_summary(data)
    with open('analysis_summary.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"  ✓ Saved analysis_summary.md ({len(summary)} characters)")

    print("Generating comparative_analysis.md...")
    comparative = generate_comparative_analysis(data)
    with open('comparative_analysis.md', 'w', encoding='utf-8') as f:
        f.write(comparative)
    print(f"  ✓ Saved comparative_analysis.md ({len(comparative)} characters)")

    print("\n" + "="*80)
    print("MARKDOWN REPORTS GENERATED SUCCESSFULLY!")
    print("="*80)


if __name__ == '__main__':
    main()
