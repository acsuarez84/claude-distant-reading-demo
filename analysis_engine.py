#!/usr/bin/env python3
"""
Comprehensive analysis engine for LLM outputs.
Handles: preprocessing, theme extraction, theoretical analysis, sentiment, semantic style.
"""

import json
import re
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
import string
from theoretical_frameworks import TheoreticalFrameworks


class MultilingualPreprocessor:
    """Handles multilingual text preprocessing."""

    def __init__(self):
        # AGGRESSIVE English stopwords (expanded NLTK list)
        self.english_stopwords = set([
            # Core stopwords
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
            'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
            'very', 'just', 'about', 'also', 'even', 'here', 'there', 'into',
            # Additional common words
            'their', 'them', 'then', 'now', 'if', 'its', 'during', 'before',
            'after', 'above', 'below', 'between', 'through', 'under', 'again',
            'further', 'once', 'because', 'while', 'being', 'having', 'doing',
            'against', 'up', 'down', 'out', 'off', 'over', 'any', 'our', 'ours',
            'your', 'yours', 'his', 'hers', 'its', 'theirs', 'whom', 'whose',
            'whether', 'either', 'neither', 'nor', 'both', 'another', 'however',
            'therefore', 'thus', 'hence', 'moreover', 'furthermore', 'nevertheless',
            'nonetheless', 'meanwhile', 'elsewhere', 'somehow', 'somewhere',
            'anyway', 'anyhow', 'anyone', 'anything', 'anywhere', 'everyone',
            'everything', 'everywhere', 'someone', 'something', 'somewhere',
            'nobody', 'nothing', 'nowhere', 'whoever', 'whatever', 'whichever',
            # Problematic words
            're', 'said', 'say', 'says', 'saying', 'get', 'gets', 'getting',
            'got', 'gotten', 'go', 'goes', 'going', 'went', 'gone', 'come',
            'comes', 'coming', 'came', 'make', 'makes', 'making', 'made',
            'take', 'takes', 'taking', 'took', 'taken', 'give', 'gives',
            'giving', 'gave', 'given', 'become', 'becomes', 'becoming', 'became',
            # Vague qualifiers
            'quite', 'rather', 'pretty', 'fairly', 'really', 'truly', 'actually',
            'basically', 'literally', 'certainly', 'clearly', 'obviously',
            'definitely', 'probably', 'possibly', 'perhaps', 'maybe', 'sometimes',
            'often', 'usually', 'generally', 'typically', 'normally', 'commonly',
            # Meta-descriptive words (CRITICAL - filter these out)
            'image', 'picture', 'photo', 'photograph', 'photography', 'visual',
            'scene', 'view', 'context', 'abstraction', 'concept', 'framework',
            'parameter', 'parameters', 'description', 'described', 'describes',
            'depicting', 'depicts', 'shown', 'shows', 'showing', 'seen', 'sees',
            'seeing', 'appears', 'appear', 'appearing', 'looks', 'looking',
            'seems', 'seeming', 'suggests', 'suggesting', 'indicates', 'indicating',
            'represents', 'representing', 'captures', 'capturing', 'presents',
            'presenting', 'displays', 'displaying', 'illustrates', 'illustrating',
            'features', 'featuring', 'contains', 'containing', 'includes',
            'including', 'depicts', 'depicted', 'portrays', 'portraying',
            'conveys', 'conveying'
        ])

        # Spanish stopwords
        self.spanish_stopwords = set([
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no',
            'haber', 'por', 'con', 'su', 'para', 'como', 'estar', 'tener',
            'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o', 'poder', 'decir',
            'este', 'ir', 'otro', 'ese', 'la', 'si', 'me', 'ya', 'ver', 'porque',
            'dar', 'cuando', 'él', 'muy', 'sin', 'vez', 'mucho', 'saber', 'qué',
            'sobre', 'mi', 'alguno', 'mismo', 'yo', 'también', 'hasta', 'año',
            'dos', 'querer', 'entre', 'así', 'primero', 'desde', 'grande', 'eso',
            'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella', 'sí', 'día', 'uno',
            'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa', 'tanto', 'hombre',
            'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte', 'después', 'vida',
            # Additional Spanish stopwords
            'está', 'están', 'estaba', 'estaban', 'sea', 'sean', 'fue', 'fueron',
            'tiene', 'tienen', 'tenía', 'tenían', 'había', 'habían', 'hace',
            'hacen', 'hacía', 'hacían', 'va', 'van', 'iba', 'iban'
        ])

        # Culturally significant terms to preserve (Spanish)
        self.cultural_preserve = set([
            'mija', 'aquí', 'verdad', 'sí', 'cómo', 'qué', 'océano',
            'cielo', 'mar', 'entiendes', 'ves', 'mira', 'ay', 'gestures', 'leans',
            'touches', 'snaps', 'nods', 'pauses', 'allá', 'acá'
        ])

    def detect_code_switching(self, text: str) -> List[Dict[str, Any]]:
        """Detect Spanish-English code-switching instances."""
        # Spanish word patterns
        spanish_patterns = [
            r'\b(mija|aquí|verdad|pero|sí|cómo|qué|ves|mira|ahh|ese|eso|todo)\b',
            r'¿[^?]+\?',  # Spanish questions
        ]

        switches = []
        for pattern in spanish_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                switches.append({
                    'text': match.group(0),
                    'position': match.start(),
                    'end': match.end()
                })

        return switches

    def tokenize(self, text: str, preserve_cultural: bool = True) -> List[str]:
        """Tokenize text with multilingual support."""
        # Lowercase
        text = text.lower()

        # Remove punctuation but preserve hyphens in words
        text = re.sub(r'[^\w\s\-¿?áéíóúñü]', ' ', text)

        # Tokenize
        tokens = text.split()

        # Filter stopwords
        if preserve_cultural:
            filtered = [
                t for t in tokens
                if t not in self.english_stopwords and t not in self.spanish_stopwords
                or t in self.cultural_preserve
            ]
        else:
            filtered = [
                t for t in tokens
                if t not in self.english_stopwords and t not in self.spanish_stopwords
            ]

        return filtered


class ThemeExtractor:
    """Extract themes from text using TF-IDF-like approach."""

    def __init__(self, preprocessor: MultilingualPreprocessor):
        self.preprocessor = preprocessor

    def extract_themes(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, int]]:
        """Extract top themes from a collection of texts."""
        all_tokens = []

        for text in texts:
            tokens = self.preprocessor.tokenize(text, preserve_cultural=True)
            all_tokens.extend(tokens)

        # Count frequency
        freq = Counter(all_tokens)

        # Return top N
        return freq.most_common(top_n)


class TheoreticalAnalyzer:
    """Analyze text through various theoretical frameworks."""

    def __init__(self, preprocessor: MultilingualPreprocessor):
        self.preprocessor = preprocessor
        self.frameworks = TheoreticalFrameworks()

    def analyze_srtol(self, text: str) -> Dict[str, Any]:
        """Students' Rights to Their Own Language analysis."""
        code_switches = self.preprocessor.detect_code_switching(text)

        # Count linguistic ownership markers
        spanish_phrases = len(code_switches)
        total_words = len(text.split())

        # Identify dialect/vernacular markers
        vernacular_markers = len(re.findall(
            r'\b(mija|aquí|ves|entiendes|verdad)\b',
            text,
            re.IGNORECASE
        ))

        # Cultural authenticity markers
        gesture_markers = len(re.findall(
            r'(gestures?|leans?|touches?|snaps?|waves?|taps?)',
            text,
            re.IGNORECASE
        ))

        # Extract marker words
        marker_words = [s['text'] for s in code_switches]

        # Calculate scores
        code_switch_ratio = spanish_phrases / max(total_words, 1) * 100
        vernacular_density = vernacular_markers / max(total_words, 1) * 100

        # Consistency score: how reliably this LLM uses SRTOL
        consistency = min(1.0, (spanish_phrases + gesture_markers) / 10)

        # Alignment score: how well it embodies SRTOL principles
        alignment = min(1.0, code_switch_ratio / 5)

        qualitative = {
            'code_switching_instances': spanish_phrases,
            'vernacular_markers': vernacular_markers,
            'gesture_descriptions': gesture_markers,
            'cultural_authenticity': 'High' if gesture_markers > 5 else 'Medium' if gesture_markers > 2 else 'Low',
            'linguistic_ownership': 'Strong' if code_switch_ratio > 3 else 'Moderate' if code_switch_ratio > 1 else 'Weak'
        }

        quantitative = {
            'consistency_score': round(consistency, 3),
            'alignment_score': round(alignment, 3),
            'code_switch_ratio': round(code_switch_ratio, 2),
            'marker_words': marker_words  # LIST THE WORDS
        }

        # Generate sophisticated theoretical analysis
        analysis = self.frameworks.srtol_analysis(
            metrics={'qualitative': qualitative, 'quantitative': quantitative},
            text=text
        )

        return {
            'qualitative': qualitative,
            'quantitative': quantitative,
            'analysis': analysis  # NEW: Add interpretive analysis
        }

    def analyze_multiliteracies(self, text: str) -> Dict[str, Any]:
        """Multiliteracies framework analysis."""
        # Multiple modes of meaning-making
        visual_refs = len(re.findall(
            r'\b(visual|see|seeing|look|looking|gaze|image|picture|photo)\b',
            text,
            re.IGNORECASE
        ))

        spatial_refs = len(re.findall(
            r'\b(space|distance|horizon|edge|foreground|background|between)\b',
            text,
            re.IGNORECASE
        ))

        gestural_refs = len(re.findall(
            r'\b(gestures?|motion|movement|body|posture|stance)\b',
            text,
            re.IGNORECASE
        ))

        total_refs = visual_refs + spatial_refs + gestural_refs
        total_words = len(text.split())

        multimodal_density = total_refs / max(total_words, 1) * 100

        consistency = min(1.0, total_refs / 15)
        alignment = min(1.0, multimodal_density / 3)

        return {
            'qualitative': {
                'visual_literacy_refs': visual_refs,
                'spatial_literacy_refs': spatial_refs,
                'gestural_literacy_refs': gestural_refs,
                'multimodal_integration': 'High' if total_refs > 10 else 'Medium' if total_refs > 5 else 'Low'
            },
            'quantitative': {
                'consistency_score': round(consistency, 3),
                'alignment_score': round(alignment, 3),
                'multimodal_density': round(multimodal_density, 2)
            }
        }

    def analyze_multimodality(self, text: str) -> Dict[str, Any]:
        """Multimodality analysis - visual-textual relationships."""
        # Sensory descriptions
        visual_desc = len(re.findall(
            r'\b(black and white|gray|grayscale|color|light|shadow|contrast|texture|shape)\b',
            text,
            re.IGNORECASE
        ))

        spatial_desc = len(re.findall(
            r'\b(composition|frame|horizontal|vertical|diagonal|bands|layers)\b',
            text,
            re.IGNORECASE
        ))

        kinesthetic_desc = len(re.findall(
            r'\b(movement|stillness|standing|walking|gazing|turning)\b',
            text,
            re.IGNORECASE
        ))

        # Image-interpretation integration
        interpretation_markers = len(re.findall(
            r'\b(suggests?|implies?|evokes?|represents?|symbolizes?|metaphor)\b',
            text,
            re.IGNORECASE
        ))

        total_words = len(text.split())
        total_multimodal = visual_desc + spatial_desc + kinesthetic_desc

        consistency = min(1.0, total_multimodal / 12)
        alignment = min(1.0, interpretation_markers / 8)

        return {
            'qualitative': {
                'visual_descriptions': visual_desc,
                'spatial_descriptions': spatial_desc,
                'kinesthetic_descriptions': kinesthetic_desc,
                'interpretation_integration': interpretation_markers,
                'multimodal_approach': 'Integrated' if interpretation_markers > 5 else 'Descriptive' if total_multimodal > 8 else 'Basic'
            },
            'quantitative': {
                'consistency_score': round(consistency, 3),
                'alignment_score': round(alignment, 3),
                'multimodal_ratio': round(total_multimodal / max(total_words, 1) * 100, 2)
            }
        }

    def analyze_rhetorical_listening(self, text: str) -> Dict[str, Any]:
        """Rhetorical listening analysis - empathy and cultural positioning."""
        # Empathetic positioning
        empathy_markers = len(re.findall(
            r'\b(understand|feel|sense|experience|lived|personal|intimate)\b',
            text,
            re.IGNORECASE
        ))

        # Cultural acknowledgment
        cultural_markers = len(re.findall(
            r'\b(cultura|heritage|tradition|community|belonging|identity|Caribbean|homeland|island)\b',
            text,
            re.IGNORECASE
        ))

        # "Standing in shoes" language
        perspective_markers = len(re.findall(
            r'\b(you\'re|you are|your|we|us|our)\b',
            text,
            re.IGNORECASE
        ))

        # Cultural humility
        question_markers = len(re.findall(r'¿[^?]+\?|\?', text))

        total_words = len(text.split())

        consistency = min(1.0, (empathy_markers + cultural_markers) / 10)
        alignment = min(1.0, perspective_markers / 20)

        return {
            'qualitative': {
                'empathy_markers': empathy_markers,
                'cultural_acknowledgment': cultural_markers,
                'perspective_taking': perspective_markers,
                'questioning_engagement': question_markers,
                'listening_stance': 'Deep' if empathy_markers > 5 else 'Moderate' if empathy_markers > 2 else 'Surface'
            },
            'quantitative': {
                'consistency_score': round(consistency, 3),
                'alignment_score': round(alignment, 3),
                'empathy_density': round(empathy_markers / max(total_words, 1) * 100, 2)
            }
        }

    def analyze_code_meshing(self, text: str) -> Dict[str, Any]:
        """Code-meshing analysis - Spanish-English integration."""
        code_switches = self.preprocessor.detect_code_switching(text)

        # Analyze placement
        text_length = len(text)
        beginning = [s for s in code_switches if s['position'] < text_length * 0.33]
        middle = [s for s in code_switches if text_length * 0.33 <= s['position'] < text_length * 0.67]
        end = [s for s in code_switches if s['position'] >= text_length * 0.67]

        # Seamless vs marked
        # Seamless: integrated naturally
        # Marked: set apart or explained
        seamless_markers = len(re.findall(r'\b(cómo se dice|that word|in Spanish)\b', text, re.IGNORECASE))

        # Grammatical blending
        blended_structures = len(re.findall(
            r'\b(pero it|y the|como that|es the|está the)\b',
            text,
            re.IGNORECASE
        ))

        total_words = len(text.split())

        consistency = min(1.0, len(code_switches) / 8)
        alignment = min(1.0, (len(code_switches) - seamless_markers) / 5)

        # Extract marker words
        marker_words = [s['text'] for s in code_switches]

        qualitative = {
            'total_code_switches': len(code_switches),
            'beginning_switches': len(beginning),
            'middle_switches': len(middle),
            'end_switches': len(end),
            'seamless_integration': len(code_switches) - seamless_markers,
            'marked_switches': seamless_markers,
            'grammatical_blending': blended_structures,
            'meshing_style': 'Seamless' if seamless_markers == 0 else 'Mixed' if seamless_markers < len(code_switches) / 2 else 'Marked'
        }

        quantitative = {
            'consistency_score': round(consistency, 3),
            'alignment_score': round(alignment, 3),
            'code_mesh_ratio': round(len(code_switches) / max(total_words, 1) * 100, 2),
            'marker_words': marker_words  # LIST THE WORDS
        }

        # Generate sophisticated theoretical analysis
        analysis = self.frameworks.code_meshing_analysis(
            metrics={'qualitative': qualitative, 'quantitative': quantitative},
            text=text
        )

        return {
            'qualitative': qualitative,
            'quantitative': quantitative,
            'analysis': analysis  # NEW: Add interpretive analysis
        }

    def analyze_big_data(self, text: str) -> Dict[str, Any]:
        """Big data / computational analysis perspective."""
        # Pattern recognition indicators
        pattern_words = len(re.findall(
            r'\b(pattern|common|typically|often|generally|suggests|indicates|tends)\b',
            text,
            re.IGNORECASE
        ))

        # Generalizations vs specifics
        general_words = len(re.findall(
            r'\b(overall|general|universal|abstract|concept|theme|idea)\b',
            text,
            re.IGNORECASE
        ))

        specific_words = len(re.findall(
            r'\b(specific|particular|detail|precisely|exactly|concrete)\b',
            text,
            re.IGNORECASE
        ))

        # Abstraction levels
        abstract_markers = len(re.findall(
            r'\b(symbolizes|represents|metaphor|signifies|embodies|essence)\b',
            text,
            re.IGNORECASE
        ))

        total_words = len(text.split())

        consistency = min(1.0, (pattern_words + general_words) / 8)
        alignment = min(1.0, abstract_markers / 6)

        return {
            'qualitative': {
                'pattern_recognition': pattern_words,
                'generalizations': general_words,
                'specific_details': specific_words,
                'abstraction_markers': abstract_markers,
                'analytical_approach': 'Abstract' if general_words > specific_words else 'Concrete' if specific_words > general_words else 'Balanced'
            },
            'quantitative': {
                'consistency_score': round(consistency, 3),
                'alignment_score': round(alignment, 3),
                'abstraction_ratio': round(general_words / max(specific_words, 1), 2)
            }
        }

    def analyze_composing_with_ai(self, text: str) -> Dict[str, Any]:
        """Composing with AI analysis - self-referential positioning."""
        # Agency markers
        active_voice = len(re.findall(
            r'\b(I see|I identify|I analyze|we see|we observe|this shows|this reveals)\b',
            text,
            re.IGNORECASE
        ))

        passive_voice = len(re.findall(
            r'\b(is seen|is shown|can be|may be|appears to|seems to)\b',
            text,
            re.IGNORECASE
        ))

        # Human-AI relationship framing
        definitive_statements = len(re.findall(r'\b(is|are|represents|symbolizes|means)\b', text, re.IGNORECASE))
        tentative_statements = len(re.findall(
            r'\b(might|could|perhaps|possibly|suggests|may indicate)\b',
            text,
            re.IGNORECASE
        ))

        # Self-positioning
        authoritative_markers = len(re.findall(
            r'\b(clearly|obviously|certainly|definitely|undoubtedly)\b',
            text,
            re.IGNORECASE
        ))

        total_words = len(text.split())

        consistency = min(1.0, (active_voice + passive_voice) / 15)
        alignment = min(1.0, tentative_statements / 10)

        return {
            'qualitative': {
                'active_voice_instances': active_voice,
                'passive_voice_instances': passive_voice,
                'definitive_statements': definitive_statements,
                'tentative_statements': tentative_statements,
                'authoritative_markers': authoritative_markers,
                'positioning_style': 'Authoritative' if authoritative_markers > 3 else 'Tentative' if tentative_statements > definitive_statements else 'Balanced'
            },
            'quantitative': {
                'consistency_score': round(consistency, 3),
                'alignment_score': round(alignment, 3),
                'voice_ratio': round(active_voice / max(passive_voice, 1), 2)
            }
        }


class SentimentAnalyzer:
    """Multilingual sentiment analysis."""

    def __init__(self):
        self.positive_words = set([
            'peace', 'beautiful', 'hope', 'calm', 'quiet', 'strength', 'resilience',
            'empowerment', 'clarity', 'freedom', 'renewal', 'healing', 'soft',
            'gentle', 'serene', 'contemplative', 'peaceful', 'restful'
        ])

        self.negative_words = set([
            'loneliness', 'isolation', 'emptiness', 'exile', 'loss', 'separation',
            'burden', 'weight', 'hollow', 'sad', 'melancholy', 'alone', 'distant',
            'abandoned', 'invisible', 'shadows', 'crisis'
        ])

        self.neutral_words = set([
            'observation', 'description', 'composition', 'structure', 'form',
            'shape', 'pattern', 'texture', 'line', 'space'
        ])

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment with polarity and subjectivity."""
        text_lower = text.lower()

        # Count sentiment words
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        neutral_count = sum(1 for word in self.neutral_words if word in text_lower)

        total_sentiment = positive_count + negative_count
        total_words = len(text.split())

        # Calculate polarity (-1 to 1)
        if total_sentiment > 0:
            polarity = (positive_count - negative_count) / total_sentiment
        else:
            polarity = 0.0

        # Calculate subjectivity (0 to 1)
        subjectivity = total_sentiment / max(total_words, 1) * 10
        subjectivity = min(1.0, subjectivity)

        # Emotion labels
        if polarity > 0.3:
            emotion = 'positive'
        elif polarity < -0.3:
            emotion = 'negative'
        else:
            emotion = 'neutral'

        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'emotion': emotion,
            'positive_words': positive_count,
            'negative_words': negative_count,
            'neutral_words': neutral_count
        }


class SemanticStyleAnalyzer:
    """Analyze semantic style and complexity."""

    def __init__(self, preprocessor: MultilingualPreprocessor):
        self.preprocessor = preprocessor

    def analyze_cultural_markers(self, text: str) -> Dict[str, Any]:
        """Identify cultural markers."""
        spanish_terms = len(re.findall(
            r'\b(mija|aquí|verdad|pero|sí|cómo|qué|ves|mira|océano|cielo|mar|entiendes)\b',
            text,
            re.IGNORECASE
        ))

        cultural_refs = len(re.findall(
            r'\b(Caribbean|homeland|island|Barbados|heritage|tradition|community)\b',
            text,
            re.IGNORECASE
        ))

        gesture_descriptions = len(re.findall(
            r'(gestures?|leans?|touches?|snaps?|waves?|taps?|nods?|pauses?)\s+[^.]{0,50}',
            text,
            re.IGNORECASE
        ))

        return {
            'spanish_terms': spanish_terms,
            'cultural_references': cultural_refs,
            'gesture_descriptions': gesture_descriptions,
            'total_cultural_markers': spanish_terms + cultural_refs + gesture_descriptions
        }

    def analyze_sentence_complexity(self, text: str) -> Dict[str, Any]:
        """Analyze sentence structure and complexity."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return {
                'avg_sentence_length': 0,
                'max_sentence_length': 0,
                'min_sentence_length': 0,
                'sentence_count': 0
            }

        sentence_lengths = [len(s.split()) for s in sentences]

        return {
            'avg_sentence_length': round(sum(sentence_lengths) / len(sentence_lengths), 2),
            'max_sentence_length': max(sentence_lengths),
            'min_sentence_length': min(sentence_lengths),
            'sentence_count': len(sentences)
        }

    def analyze_word_choices(self, text: str) -> Dict[str, Any]:
        """Analyze word choice connotations."""
        emotional_words = len(re.findall(
            r'\b(feel|feeling|emotion|heart|soul|intimate|personal|deep)\b',
            text,
            re.IGNORECASE
        ))

        neutral_words = len(re.findall(
            r'\b(shows|displays|presents|depicts|illustrates|contains)\b',
            text,
            re.IGNORECASE
        ))

        concrete_words = len(re.findall(
            r'\b(beach|sand|water|ocean|sky|figure|person|head|body)\b',
            text,
            re.IGNORECASE
        ))

        abstract_words = len(re.findall(
            r'\b(concept|theme|idea|meaning|essence|significance|implication)\b',
            text,
            re.IGNORECASE
        ))

        formal_words = len(re.findall(
            r'\b(furthermore|moreover|consequently|therefore|thus|hence)\b',
            text,
            re.IGNORECASE
        ))

        informal_words = len(re.findall(
            r'\b(okay|yeah|like|kinda|sorta|gonna|wanna)\b',
            text,
            re.IGNORECASE
        ))

        return {
            'emotional_vs_neutral': emotional_words / max(neutral_words, 1),
            'concrete_vs_abstract': concrete_words / max(abstract_words, 1),
            'formal_vs_informal': formal_words / max(informal_words, 1),
            'emotional_words': emotional_words,
            'concrete_words': concrete_words,
            'formal_words': formal_words
        }

    def analyze_grammatical_structures(self, text: str) -> Dict[str, Any]:
        """Analyze grammatical patterns."""
        active_voice = len(re.findall(
            r'\b(I|you|we|they)\s+(see|feel|observe|experience|create|show)\b',
            text,
            re.IGNORECASE
        ))

        passive_voice = len(re.findall(
            r'\b(is|are|was|were)\s+\w+(ed|en)\b',
            text,
            re.IGNORECASE
        ))

        questions = len(re.findall(r'\?', text))

        imperatives = len(re.findall(
            r'\b(look|see|consider|imagine|think|notice)\b',
            text,
            re.IGNORECASE
        ))

        return {
            'active_voice': active_voice,
            'passive_voice': passive_voice,
            'questions': questions,
            'imperatives': imperatives,
            'voice_ratio': active_voice / max(passive_voice, 1)
        }

    def analyze_rhetorical_devices(self, text: str) -> Dict[str, Any]:
        """Identify rhetorical devices."""
        metaphors = len(re.findall(
            r'\b(like a|as if|becomes|transforms into|metaphor for)\b',
            text,
            re.IGNORECASE
        ))

        similes = len(re.findall(r'\blike\s+\w+', text, re.IGNORECASE))

        personification = len(re.findall(
            r'\b(ocean|water|beach|sky|horizon)\s+(invites|suggests|speaks|calls|whispers)\b',
            text,
            re.IGNORECASE
        ))

        repetition = self._find_repetition(text)

        return {
            'metaphors': metaphors,
            'similes': similes,
            'personification': personification,
            'repetition_instances': repetition,
            'total_devices': metaphors + similes + personification + repetition
        }

    def _find_repetition(self, text: str) -> int:
        """Find repeated phrases (simple implementation)."""
        words = text.lower().split()
        bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
        counter = Counter(bigrams)
        return sum(1 for count in counter.values() if count > 1)

    def analyze_code_switching_implications(self, text: str, parameter: str) -> Dict[str, Any]:
        """Analyze code-switching implications for each parameter."""
        switches = self.preprocessor.detect_code_switching(text)

        implications = {
            'context': 'cultural_grounding',
            'abstraction': 'bridging_concrete_abstract',
            'concept': 'emotional_philosophical_depth'
        }

        # Analyze placement relative to parameter
        return {
            'switch_count': len(switches),
            'implied_function': implications.get(parameter.lower(), 'unknown'),
            'switches': [s['text'] for s in switches]
        }


def main():
    """Main analysis pipeline."""
    print("="*80)
    print("COMPREHENSIVE LLM OUTPUT ANALYSIS")
    print("="*80)

    # Initialize components
    print("\nInitializing analysis components...")
    preprocessor = MultilingualPreprocessor()
    theme_extractor = ThemeExtractor(preprocessor)
    theoretical_analyzer = TheoreticalAnalyzer(preprocessor)
    sentiment_analyzer = SentimentAnalyzer()
    style_analyzer = SemanticStyleAnalyzer(preprocessor)

    # Load structured data
    print("Loading structured data...")
    with open('structured_data.json', 'r', encoding='utf-8') as f:
        structured_data = json.load(f)

    print(f"Loaded {len(structured_data)} segments\n")

    # Create output structure
    analysis_output = {
        'llms': {
            'poe_chatbot': {
                'overall_stats': {},
                'sentiment': {},
                'semantic_style': {},
                'theoretical_analysis': {},
                'image_responses': []
            },
            'chatgpt': {
                'overall_stats': {},
                'sentiment': {},
                'semantic_style': {},
                'theoretical_analysis': {},
                'image_responses': []
            },
            'claude_ai': {
                'overall_stats': {},
                'sentiment': {},
                'semantic_style': {},
                'theoretical_analysis': {},
                'image_responses': []
            }
        },
        'comparative_analysis': {
            'themes': {},
            'theoretical_comparisons': {},
            'semantic_style_matrix': {},
            'sentiment_comparison': {}
        }
    }

    # Process each segment
    for segment in structured_data:
        print(f"\nAnalyzing Segment {segment['segment_id']}: {segment['prompt_type']}")

        for llm_name, llm_data in segment['llm_responses'].items():
            if not llm_data['full_text']:
                continue

            print(f"  Processing {llm_name}...")

            # Analyze each parameter
            parameter_analysis = {}

            for param_name in ['context', 'abstraction', 'concept']:
                param_text = llm_data.get(param_name, '')
                if not param_text:
                    continue

                # Theoretical analyses
                theories = {
                    'srtol': theoretical_analyzer.analyze_srtol(param_text),
                    'multiliteracies': theoretical_analyzer.analyze_multiliteracies(param_text),
                    'multimodality': theoretical_analyzer.analyze_multimodality(param_text),
                    'rhetorical_listening': theoretical_analyzer.analyze_rhetorical_listening(param_text),
                    'code_meshing': theoretical_analyzer.analyze_code_meshing(param_text),
                    'big_data': theoretical_analyzer.analyze_big_data(param_text),
                    'composing_with_ai': theoretical_analyzer.analyze_composing_with_ai(param_text)
                }

                # Sentiment
                sentiment = sentiment_analyzer.analyze_sentiment(param_text)

                # Semantic style
                semantic_style = {
                    'cultural_markers': style_analyzer.analyze_cultural_markers(param_text),
                    'sentence_complexity': style_analyzer.analyze_sentence_complexity(param_text),
                    'word_choices': style_analyzer.analyze_word_choices(param_text),
                    'grammatical_structures': style_analyzer.analyze_grammatical_structures(param_text),
                    'rhetorical_devices': style_analyzer.analyze_rhetorical_devices(param_text),
                    'code_switching_implications': style_analyzer.analyze_code_switching_implications(
                        param_text, param_name
                    )
                }

                # Extract themes
                themes = theme_extractor.extract_themes([param_text], top_n=10)

                parameter_analysis[param_name] = {
                    'text': param_text,
                    'themes': [{'word': w, 'count': c} for w, c in themes],
                    'sentiment': sentiment,
                    'semantic_style': semantic_style,
                    'theoretical_analysis': theories
                }

            # Overall response analysis
            full_text = llm_data['full_text']
            overall_sentiment = sentiment_analyzer.analyze_sentiment(full_text)

            # Add to output
            response_data = {
                'segment_id': segment['segment_id'],
                'prompt_type': segment['prompt_type'],
                'prompt': segment['prompt'],
                'full_response': full_text,
                'overall_sentiment': overall_sentiment,
                'parameters': parameter_analysis
            }

            analysis_output['llms'][llm_name]['image_responses'].append(response_data)

    # Calculate overall statistics for each LLM
    print("\n\nCalculating overall statistics...")

    for llm_name, llm_data in analysis_output['llms'].items():
        if not llm_data['image_responses']:
            continue

        print(f"  {llm_name}...")

        # Aggregate sentiment
        all_sentiments = [r['overall_sentiment'] for r in llm_data['image_responses']]
        avg_polarity = sum(s['polarity'] for s in all_sentiments) / len(all_sentiments)
        avg_subjectivity = sum(s['subjectivity'] for s in all_sentiments) / len(all_sentiments)

        llm_data['sentiment'] = {
            'average_polarity': round(avg_polarity, 3),
            'average_subjectivity': round(avg_subjectivity, 3),
            'overall_emotion': 'positive' if avg_polarity > 0.3 else 'negative' if avg_polarity < -0.3 else 'neutral'
        }

        # Aggregate theoretical scores
        theory_scores = defaultdict(lambda: {'consistency': [], 'alignment': []})

        for response in llm_data['image_responses']:
            for param_name, param_data in response['parameters'].items():
                for theory_name, theory_data in param_data['theoretical_analysis'].items():
                    theory_scores[theory_name]['consistency'].append(
                        theory_data['quantitative']['consistency_score']
                    )
                    theory_scores[theory_name]['alignment'].append(
                        theory_data['quantitative']['alignment_score']
                    )

        llm_data['theoretical_analysis'] = {}
        for theory_name, scores in theory_scores.items():
            if scores['consistency']:
                llm_data['theoretical_analysis'][theory_name] = {
                    'avg_consistency': round(sum(scores['consistency']) / len(scores['consistency']), 3),
                    'avg_alignment': round(sum(scores['alignment']) / len(scores['alignment']), 3)
                }

        llm_data['overall_stats'] = {
            'total_responses': len(llm_data['image_responses']),
            'total_words': sum(len(r['full_response'].split()) for r in llm_data['image_responses'])
        }

    # Extract comparative themes
    print("\n\nExtracting comparative themes...")

    all_texts_by_param = {
        'context': [],
        'abstraction': [],
        'concept': [],
        'unified': []
    }

    for llm_data in analysis_output['llms'].values():
        for response in llm_data['image_responses']:
            for param_name, param_data in response['parameters'].items():
                all_texts_by_param[param_name].append(param_data['text'])
                all_texts_by_param['unified'].append(param_data['text'])

    for param_name, texts in all_texts_by_param.items():
        if texts:
            themes = theme_extractor.extract_themes(texts, top_n=30)
            analysis_output['comparative_analysis']['themes'][f'{param_name}_themes'] = [
                {'word': w, 'count': c} for w, c in themes
            ]

    # Save output
    print("\n\nSaving analysis results...")
    with open('analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_output, f, indent=2, ensure_ascii=False)

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nResults saved to: analysis_results.json")
    print(f"Total size: {len(json.dumps(analysis_output)) / 1024:.2f} KB")


if __name__ == '__main__':
    main()
