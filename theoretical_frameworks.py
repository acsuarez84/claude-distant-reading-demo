#!/usr/bin/env python3
"""
Theoretical Analysis Templates with Citations to Key Scholars

This module provides sophisticated rhetorical analysis grounded in seven
theoretical frameworks. Each template includes:
- Pattern description (what the data shows)
- Rhetorical interpretation (what it means for meaning-making)
- Cultural/political implications (what ideological work it does)
- Textual evidence (specific examples)
- Theorist citations (key scholars)
"""

import re
from typing import Dict, List, Any


def extract_examples(text: str, pattern: str, limit: int = 3) -> List[str]:
    """Extract example quotes matching a pattern."""
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches[:limit] if matches else []


def extract_code_switch_examples(text: str, limit: int = 3) -> List[str]:
    """Extract code-switching examples from text."""
    # Find sentences with Spanish words
    spanish_pattern = r'[^.!?]*\b(mija|aquí|verdad|pero|sí|cómo|qué|ves|mira|océano|cielo|mar|entiendes|allá|acá|ni|tanto|también|ese|eso)[^.!?]*[.!?]'
    return extract_examples(text, spanish_pattern, limit)


def extract_gestures(text: str) -> List[str]:
    """Extract gesture descriptions."""
    gesture_pattern = r'(leans? in|touches?|snaps?|waves?|taps?|nods?|pauses?|gestures?)[^.!?]{0,50}'
    return extract_examples(text, gesture_pattern, limit=5)


def extract_multimodal_refs(text: str) -> List[str]:
    """Extract multimodal references."""
    patterns = [
        r'[^.!?]*(visual|spatial|gestural|embodied)[^.!?]*[.!?]',
        r'[^.!?]*(composition|horizon|silhouette|shape|form)[^.!?]*[.!?]'
    ]
    examples = []
    for pattern in patterns:
        examples.extend(extract_examples(text, pattern, limit=2))
    return examples[:3]


class TheoreticalFrameworks:
    """
    Pre-written analysis templates for each theoretical framework.
    All templates cite key theorists and include textual evidence.
    """

    @staticmethod
    def srtol_analysis(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        Students' Rights to Their Own Language (SRTOL)

        Key Theorists:
        - CCCC (1974) - Foundational resolution on linguistic rights
        - Geneva Smitherman (1977) - Talkin and Testifyin
        - Vershawn Young (2009, 2011) - Code-meshing critique
        - Victor Villanueva - Language diversity and rhetoric

        Focus: Linguistic ownership, vernacular authority, code-meshing
        """
        qual = metrics['qualitative']
        code_switches = qual.get('code_switching_instances', 0)
        vernacular = qual.get('vernacular_markers', 0)
        gestures = qual.get('gesture_descriptions', 0)

        examples = extract_code_switch_examples(text, limit=3)
        gesture_examples = extract_gestures(text)

        # Pattern Description
        if code_switches > 5:
            pattern = f"""The LLM employs {code_switches} instances of code-switching and {vernacular} vernacular markers, demonstrating linguistic pluralism consistent with the 1974 CCCC Students' Right to Their Own Language resolution, which asserts that students' right to their own patterns of language "includes the right to their own dialects." """
        elif code_switches > 0:
            pattern = f"""With {code_switches} code-switching instances, the response shows moderate engagement with linguistic diversity, though not to the extent advocated by SRTOL proponents."""
        else:
            pattern = f"""The response contains no code-switching, adhering exclusively to academic Standard English—what Vershawn Young (2009) critiques as enforcing linguistic assimilation rather than embracing students' full linguistic repertoires."""

        # Rhetorical Interpretation
        if code_switches > 5:
            interpretation = f"""This frequent code-switching enacts what Geneva Smitherman (1977) describes as "linguistic push-pull"—the strategic deployment of home language alongside dominant discourse. Examples include: "{examples[0] if len(examples) > 0 else 'N/A'}" and "{examples[1] if len(examples) > 1 else 'N/A'}". Rather than treating Spanish as deficit or "interference," the LLM positions it as co-constitutive of meaning-making, challenging monolingual ideologies that frame multilingualism as problem rather than resource. This exemplifies Young's (2011) concept of code-meshing: blending languages seamlessly rather than code-switching (separating them into distinct contexts)."""
        elif code_switches > 0:
            interpretation = f"""The moderate code-switching suggests awareness of linguistic diversity but stops short of full code-meshing. This mirrors what Young calls "code-switching" ideology—compartmentalizing languages rather than blending them organically."""
        else:
            interpretation = f"""The absence of code-switching enforces what Victor Villanueva terms "linguistic homogeneity"—the erasure of cultural-linguistic identity in favor of assimilation to academic norms. This contradicts SRTOL's core premise that linguistic diversity enriches rather than detracts from rhetorical effectiveness."""

        # Cultural/Political Implications
        if gestures > 3:
            implications = f"""The {gestures} gesture descriptions ({', '.join(gesture_examples[:3])}) signal embodied rhetoric—language as performed, not just written. This challenges print-centric academic discourse by foregrounding orality and physical presence, echoing Smitherman's argument that African American and Latinx rhetorics privilege embodiment over abstract textuality. Such gestural markers resist the disembodied "voice from nowhere" that characterizes dominant academic writing, instead positioning knowledge as situated, performed, and culturally specific. This enacts what SRTOL calls "the right to their own patterns of language"—not merely lexical choice but rhetorical stance, embodiment, and cultural positioning."""
        else:
            implications = f"""The limited gestural markers suggest conformity to print-based academic conventions that devalue embodied, oral, and performative dimensions of language. This aligns with critiques that mainstream composition pedagogy privileges written over spoken discourse, marginalizing rhetorical traditions rooted in oral culture."""

        return {
            'pattern_description': pattern.strip(),
            'rhetorical_interpretation': interpretation.strip(),
            'cultural_political_implications': implications.strip(),
            'key_examples': examples[:3],
            'gesture_examples': gesture_examples[:3],
            'theorists_cited': ['CCCC (1974)', 'Smitherman (1977)', 'Young (2009, 2011)', 'Villanueva']
        }

    @staticmethod
    def multiliteracies_analysis(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        Multiliteracies

        Key Theorists:
        - New London Group (1996) - Foundational multiliteracies manifesto
        - Cope & Kalantzis (2000, 2009) - Multiliteracies pedagogy
        - Gunther Kress (2003, 2010) - Multimodality theory

        Focus: Multiple modes of meaning-making, design across semiotic systems
        """
        qual = metrics['qualitative']
        visual_refs = qual.get('visual_literacy_refs', 0)
        spatial_refs = qual.get('spatial_literacy_refs', 0)
        gestural_refs = qual.get('gestural_literacy_refs', 0)
        total_multimodal = visual_refs + spatial_refs + gestural_refs

        examples = extract_multimodal_refs(text)

        # Pattern Description
        pattern = f"""The response demonstrates multimodal meaning-making across {visual_refs} visual, {spatial_refs} spatial, and {gestural_refs} gestural literacy references, totaling {total_multimodal} multimodal engagements with the image."""

        # Rhetorical Interpretation
        if total_multimodal > 10:
            interpretation = f"""This extensive multimodal engagement aligns with the New London Group's (1996) multiliteracies framework, which argues that meaning is made through "Design"—the deliberate orchestration of multiple semiotic modes. The LLM moves beyond monomodal linguistic literacy to integrate visual literacy (composition, contrast, tonal range), spatial literacy (horizon, distance, foreground/background relationships), and embodied/gestural literacy (posture, gaze, physical positioning). Examples include: {examples[0] if len(examples) > 0 else 'N/A'}. This demonstrates what Cope & Kalantzis (2009) term "multimodal meaning"—the recognition that contemporary communication requires navigating and integrating diverse semiotic resources, not privileging linguistic text over other modes."""
        else:
            interpretation = f"""With {total_multimodal} multimodal references, the response shows limited engagement with multiliteracies. This suggests adherence to traditional monomodal literacy focused primarily on linguistic description, what Kress (2003) critiques as "the dominance of writing" over other meaning-making modes."""

        # Cultural/Political Implications
        implications = f"""By integrating multiple modes, the LLM enacts what the New London Group calls recognition of "increasing multiplicity and integration of significant modes of meaning-making." This challenges composition pedagogy's historical privileging of alphabetic text, acknowledging that meaning-making in digital/visual age requires multimodal competencies. However, as Kress (2010) notes, true multimodal literacy requires not just describing visual elements linguistically, but understanding how each mode has distinct affordances and limitations—and this response {('demonstrates' if total_multimodal > 10 else 'struggles with')} such modal awareness."""

        return {
            'pattern_description': pattern.strip(),
            'rhetorical_interpretation': interpretation.strip(),
            'cultural_political_implications': implications.strip(),
            'key_examples': examples[:3],
            'theorists_cited': ['New London Group (1996)', 'Cope & Kalantzis (2000, 2009)', 'Kress (2003, 2010)']
        }

    @staticmethod
    def multimodality_analysis(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        Multimodality

        Key Theorists:
        - Gunther Kress & Theo van Leeuwen (1996, 2006) - Reading Images
        - Carey Jewitt (2009) - Multimodal approaches
        - Jody Shipka (2011) - Multimodal composition

        Focus: Visual-textual relationships, modal affordances
        """
        qual = metrics['qualitative']
        visual_desc = qual.get('visual_descriptions', 0)
        spatial_desc = qual.get('spatial_descriptions', 0)
        interpretation_markers = qual.get('interpretation_integration', 0)

        # Pattern Description
        pattern = f"""The response employs {visual_desc} visual descriptions, {spatial_desc} spatial descriptions, and {interpretation_markers} interpretive integrations of image and meaning."""

        # Rhetorical Interpretation
        interpretation = f"""This pattern demonstrates engagement with what Kress & van Leeuwen (2006) call "visual grammar"—the systematic ways visual elements create meaning parallel to linguistic grammar. The integration of visual description with interpretation ('{interpretation_markers}' instances) shows awareness that images are not merely illustrative but constitutive of meaning. However, as Shipka (2011) notes, true multimodal composition requires recognizing that each mode has distinct affordances: images can show simultaneity and spatial relationships that linear text cannot, while text can articulate abstract concepts and temporal sequences unavailable to static images."""

        # Cultural/Political Implications
        implications = f"""By treating visual and textual modes as co-constitutive, the response challenges logocentric academic traditions that subordinate image to word. Kress (2003) argues this hierarchy reflects print culture's dominance, but digital rhetorics demand recognition that "the world told is a different world to the world shown." The LLM's multimodal approach acknowledges this, though {('fully embracing' if interpretation_markers > 5 else 'still defaulting to')} {('visual-textual integration' if interpretation_markers > 5 else 'linguistic description of visual content')}."""

        return {
            'pattern_description': pattern.strip(),
            'rhetorical_interpretation': interpretation.strip(),
            'cultural_political_implications': implications.strip(),
            'theorists_cited': ['Kress & van Leeuwen (1996, 2006)', 'Jewitt (2009)', 'Shipka (2011)', 'Kress (2003)']
        }

    @staticmethod
    def rhetorical_listening_analysis(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        Rhetorical Listening

        Key Theorists:
        - Krista Ratcliffe (2005) - Rhetorical Listening: Identification, Gender, Whiteness
        - Cheryl Glenn (2004) - Unspoken: A Rhetoric of Silence
        - Glenn & Ratcliffe (2011) - Silence and Listening as Rhetorical Arts
        - Jacqueline Jones Royster (1996) - When the First Voice You Hear

        Focus: Empathy, cultural acknowledgment, accountability, silence as rhetoric
        """
        qual = metrics['qualitative']
        empathy = qual.get('empathy_markers', 0)
        cultural = qual.get('cultural_acknowledgment', 0)
        perspective = qual.get('perspective_taking', 0)
        questions = qual.get('questioning_engagement', 0)

        # Pattern Description
        pattern = f"""The response demonstrates {empathy} empathetic positioning markers, {cultural} cultural acknowledgments, {perspective} instances of perspective-taking ("you", "we", "our"), and {questions} questions or invitations for engagement."""

        # Rhetorical Interpretation
        if empathy + cultural > 5:
            interpretation = f"""This pattern exemplifies Ratcliffe's (2005) concept of rhetorical listening as "a trope for interpretive invention and more specifically as a code of cross-cultural conduct." The LLM demonstrates what Ratcliffe calls "standing under"—occupying a space of receptivity rather than mastery. By foregrounding empathy and cultural acknowledgment, the response enacts listening as accountability, recognizing (as Royster 1996 argues) that interpretation is always situated, never neutral. The {questions} questions suggest what Glenn (2004) identifies as productive silence—leaving space for others' voices rather than filling all interpretive gaps. This aligns with Glenn & Ratcliffe's (2011) argument that "listening, like silence, is not passive; it is a rhetorical art" requiring active, intentional cultivation."""
        else:
            interpretation = f"""Limited empathetic engagement suggests rhetorical stance-taking rather than genuine listening. Ratcliffe distinguishes between hearing (registering sound) and listening (seeking understanding across difference), and this response demonstrates more hearing than listening. Glenn (2004) warns against what she calls "silencing"—imposing interpretations that foreclose others' meaning-making—and this response risks such foreclosure by prioritizing assertion over receptivity."""

        # Cultural/Political Implications
        implications = f"""Rhetorical listening carries profound political stakes: it requires, as Royster (1996) argues, acknowledging "the right of the people in question to name their own experience." The LLM's {('strong' if empathy + cultural > 5 else 'limited')} engagement with cultural positioning suggests {('accountability to' if empathy + cultural > 5 else 'distance from')} the subject's cultural situatedness. Glenn & Ratcliffe (2011) theorize listening as resistance to what Glenn calls "compulsory hearing"—the demand that marginalized groups speak on dominant terms. Instead, rhetorical listening creates space for "unheard stories" (Royster) and validates silence as meaningful. The presence of {questions} questions {('demonstrates' if questions > 2 else 'suggests limited') if questions > 0 else 'suggests absence of'} what Ratcliffe terms "rhetorical eavesdropping"—listening to what is not explicitly stated, attending to cultural logics beyond surface meaning."""

        return {
            'pattern_description': pattern.strip(),
            'rhetorical_interpretation': interpretation.strip(),
            'cultural_political_implications': implications.strip(),
            'key_examples': [],  # Add for consistency
            'theorists_cited': ['Ratcliffe (2005)', 'Glenn (2004)', 'Glenn & Ratcliffe (2011)', 'Royster (1996)']
        }

    @staticmethod
    def code_meshing_analysis(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        Code-Meshing

        Key Theorists:
        - Suresh Canagarajah (2006, 2011, 2013) - Translanguaging, code-meshing
        - Vershawn Young (2004, 2009, 2011) - Code-meshing vs code-switching
        - Ofelia García & Li Wei (2014) - Translanguaging practices

        Focus: Language blending, translingual practice
        """
        qual = metrics['qualitative']
        total_switches = qual.get('total_code_switches', 0)
        beginning = qual.get('beginning_switches', 0)
        middle = qual.get('middle_switches', 0)
        end_switches = qual.get('end_switches', 0)
        seamless = qual.get('seamless_integration', 0)
        marked = qual.get('marked_switches', 0)

        examples = extract_code_switch_examples(text, limit=4)

        # Pattern Description
        pattern = f"""The response employs {total_switches} code-meshing instances: {beginning} in opening sections, {middle} in middle sections, {end_switches} in concluding sections. Of these, {seamless} integrate seamlessly while {marked} are marked/explained."""

        # Rhetorical Interpretation
        if total_switches > 8 and seamless > marked:
            interpretation = f"""This extensive seamless code-meshing enacts what Canagarajah (2011, 2013) terms "translingual practice"—the deployment of full linguistic repertoires without apology or translation. Examples include: "{examples[0] if len(examples) > 0 else 'N/A'}", "{examples[1] if len(examples) > 1 else 'N/A'}". The concentration in {('beginning' if beginning == max([beginning, middle, end_switches]) else 'middle' if middle == max([beginning, middle, end_switches]) else 'ending')} sections suggests strategic placement: code-meshing functions as {('cultural grounding/frame-setting' if beginning == max([beginning, middle, end_switches]) else 'affective intensification' if middle == max([beginning, middle, end_switches]) else 'concluding emphasis')}. Young (2011) distinguishes code-meshing (blending) from code-switching (separating), and this response demonstrates the former—languages coexist rather than alternate."""
        elif total_switches > 0:
            interpretation = f"""Moderate code-meshing with {marked} marked instances suggests what García & Li Wei (2014) call "translanguaging awareness"—conscious navigation of linguistic boundaries rather than seamless blending. This performs code-switching (compartmentalized languages) more than code-meshing (integrated repertoire)."""
        else:
            interpretation = f"""Absence of code-meshing enforces monolingual norms. Canagarajah (2013) argues this reflects "monolingual ideologies" that construct multilingualism as deviant rather than normative."""

        # Cultural/Political Implications
        implications = f"""Code-meshing carries political stakes: Young argues it resists assimilationist pressures to "leave your language at the door," instead asserting that full linguistic selfhood belongs in academic discourse. Canagarajah positions translingualism as decolonial practice, challenging English linguistic imperialism. This response's {('extensive' if total_switches > 8 else 'limited' if total_switches > 0 else 'absent')} code-meshing {('enacts such resistance' if total_switches > 8 else 'gestures toward but does not fully embrace translingual practice' if total_switches > 0 else 'capitulates to English monolingualism')}."""

        return {
            'pattern_description': pattern.strip(),
            'rhetorical_interpretation': interpretation.strip(),
            'cultural_political_implications': implications.strip(),
            'key_examples': examples[:4],
            'theorists_cited': ['Canagarajah (2006, 2011, 2013)', 'Young (2004, 2009, 2011)', 'García & Li Wei (2014)']
        }

    @staticmethod
    def big_data_analysis(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        Big Data / Computational Analysis

        Key Theorists:
        - Franco Moretti (2005, 2013) - Distant reading
        - N. Katherine Hayles (2012) - How We Think
        - Lisa Nakamura & Peter Chow-White (2012) - Race After the Internet

        Focus: Pattern recognition, abstraction, computational rhetoric
        """
        qual = metrics['qualitative']
        patterns = qual.get('pattern_recognition', 0)
        generalizations = qual.get('generalizations', 0)
        specifics = qual.get('specific_details', 0)
        abstractions = qual.get('abstraction_markers', 0)

        # Pattern Description
        pattern = f"""The response employs {patterns} pattern recognition markers, {generalizations} generalizations, {specifics} specific details, and {abstractions} abstraction markers."""

        # Rhetorical Interpretation
        interpretation = f"""This analytical approach reflects what Moretti (2005, 2013) calls "distant reading"—identifying patterns across large datasets rather than close reading individual texts. The ratio of generalizations ({generalizations}) to specifics ({specifics}) suggests {('pattern-focused' if generalizations > specifics else 'detail-focused' if specifics > generalizations else 'balanced')} approach. Hayles (2012) distinguishes "close reading" (attention to textual particularity) from "hyper reading" (filtering for patterns), and this LLM demonstrates {('hyper reading tendencies' if generalizations > specifics else 'close reading orientation' if specifics > generalizations else 'integration of both modes')}."""

        # Cultural/Political Implications
        implications = f"""Computational approaches to text carry epistemological implications. Moretti argues distant reading reveals structures invisible to close reading, but critics note it risks flattening cultural specificity into aggregated patterns. As Nakamura & Chow-White (2012) caution, big data analytics can reproduce racial and cultural biases when pattern-recognition effaces situated knowledge. This response's {('high' if abstractions > 5 else 'moderate' if abstractions > 2 else 'low')} abstraction level suggests {('comfort with computational generalization' if abstractions > 5 else 'negotiation between pattern and particularity' if abstractions > 2 else 'resistance to reductive categorization')}."""

        return {
            'pattern_description': pattern.strip(),
            'rhetorical_interpretation': interpretation.strip(),
            'cultural_political_implications': implications.strip(),
            'theorists_cited': ['Moretti (2005, 2013)', 'Hayles (2012)', 'Nakamura & Chow-White (2012)']
        }

    @staticmethod
    def composing_with_ai_analysis(metrics: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        Composing with AI

        Key Theorists:
        - Annette Vee (2017) - Coding Literacy
        - Casey Boyle (2018) - Rhetoric and Posthumanism
        - N. Katherine Hayles (2005, 2012) - Posthuman, computational media
        - James J. Brown Jr. (2015) - Ethical Programs

        Focus: AI agency, human-machine collaboration, algorithmic rhetoric
        """
        qual = metrics['qualitative']
        active_voice = qual.get('active_voice_instances', 0)
        passive_voice = qual.get('passive_voice_instances', 0)
        definitive = qual.get('definitive_statements', 0)
        tentative = qual.get('tentative_statements', 0)

        # Pattern Description
        pattern = f"""The response employs {active_voice} active voice constructions, {passive_voice} passive voice, {definitive} definitive statements, and {tentative} tentative/modal statements."""

        # Rhetorical Interpretation
        interpretation = f"""This rhetorical positioning reflects what Hayles (2005, 2012) calls the "posthuman" condition—recognition that agency is distributed between human and nonhuman actors. The ratio of active to passive voice ({active_voice}:{passive_voice}) and definitive to tentative statements ({definitive}:{tentative}) signals the LLM's stance toward interpretive authority. Vee (2017) argues that computational authorship requires new literacy frameworks acknowledging that code, algorithms, and data structures "write" alongside human authors. The LLM's {('authoritative' if definitive > tentative else 'tentative' if tentative > definitive else 'balanced')} positioning {('asserts' if definitive > tentative else 'hedges' if tentative > definitive else 'negotiates')} its own agency in meaning-making."""

        # Cultural/Political Implications
        implications = f"""AI authorship raises questions of accountability. Brown (2015) argues that algorithms are "ethical programs" that encode values, and Boyle (2018) notes that posthuman rhetoric distributes agency beyond human intention. This LLM's {('assertive' if active_voice > passive_voice else 'deferential')} voice and {('confident' if definitive > tentative else 'uncertain')} modal positioning suggest {('comfort with distributed agency' if active_voice > passive_voice and definitive > tentative else 'anxiety about autonomous interpretation' if passive_voice > active_voice or tentative > definitive else 'negotiated stance toward human-AI collaboration')}. As composition increasingly involves AI collaboration, these rhetorical choices signal how nonhuman actors position themselves in knowledge-making."""

        return {
            'pattern_description': pattern.strip(),
            'rhetorical_interpretation': interpretation.strip(),
            'cultural_political_implications': implications.strip(),
            'theorists_cited': ['Vee (2017)', 'Hayles (2005, 2012)', 'Boyle (2018)', 'Brown (2015)']
        }


def generate_comparative_analysis(llm_analyses: Dict[str, Dict[str, Any]], theory_key: str) -> Dict[str, Any]:
    """
    Generate comparative analysis across LLMs for a specific theory.

    Args:
        llm_analyses: Dict mapping LLM names to their theoretical analyses
        theory_key: Which theory to compare (e.g., 'srtol', 'code_meshing')

    Returns:
        Comparative analysis with description, interpretation, implications
    """
    # Extract metrics for comparison
    llm_metrics = {}
    for llm_name, analyses in llm_analyses.items():
        if theory_key in analyses:
            llm_metrics[llm_name] = analyses[theory_key]

    if not llm_metrics:
        return {
            'description': f'No data available for {theory_key} comparison.',
            'interpretation': '',
            'implications': ''
        }

    # Generate comparison based on theory
    if theory_key == 'code_meshing':
        poe_switches = llm_metrics.get('poe_chatbot', {}).get('qualitative', {}).get('total_code_switches', 0)
        chatgpt_switches = llm_metrics.get('chatgpt', {}).get('qualitative', {}).get('total_code_switches', 0)
        claude_switches = llm_metrics.get('claude_ai', {}).get('qualitative', {}).get('total_code_switches', 0)

        description = f"""Code-meshing frequency varies dramatically: Poe ({poe_switches} switches), ChatGPT ({chatgpt_switches} switches), Claude ({claude_switches} switches)."""

        interpretation = f"""This divergence reflects architectural and training differences. Poe's extensive code-meshing suggests training data including vernacular, conversational text, while ChatGPT's formal monolingualism indicates optimization for academic Standard English. As Canagarajah (2013) notes, AI language models reproduce the linguistic ideologies embedded in their training corpora—monolingual datasets produce monolingual outputs."""

        implications = f"""These differences reveal that "AI" is not monolithic: different architectures encode different linguistic politics. The LLM that code-meshes enacts translingual practice; the one that doesn't enforces linguistic assimilation. This demonstrates what Vee calls "computational literacy"—recognizing that algorithms make rhetorical choices."""

    else:
        # Generic comparative template
        description = f"Comparative analysis of {theory_key} across LLMs shows varied engagement with this theoretical framework."
        interpretation = f"These variations reflect different rhetorical affordances and constraints built into each LLM's architecture."
        implications = f"The divergence demonstrates that AI systems are not neutral but encode specific epistemological and cultural assumptions."

    return {
        'description': description,
        'interpretation': interpretation,
        'implications': implications
    }
