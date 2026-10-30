"""Core Text Analyzer Domain Service.

Executes unified analysis pipelines against raw text to construct comprehensive
TextMetrics aggregate entities.
"""

from __future__ import annotations
from collections import Counter
import re
from typing import List, Optional

from wordcount.domain.models import (
    KeywordFrequency,
    TextMetrics
)
from wordcount.domain.tokenizer import Tokenizer
from wordcount.domain.readability import ReadabilityCalculator

# Common stopwords to optionally filter in frequency analysis if desired
DEFAULT_STOPWORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
    "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    # Turkish common stopwords
    "ve", "bir", "bu", "da", "de", "ile", "için", "ne", "o", "kadar",
    "gibi", "çok", "daha", "ama", "en", "var", "yok", "olan", "olarak"
}


class TextAnalyzer:
    """Domain service that computes comprehensive text metrics."""

    def __init__(self, tokenizer: Optional[Tokenizer] = None):
        self.tokenizer = tokenizer or Tokenizer()

    def analyze(
        self,
        text: str,
        top_n_keywords: int = 10,
        filter_stopwords: bool = False
    ) -> TextMetrics:
        """Analyze text and produce a TextMetrics domain aggregate."""
        if not text or not text.strip():
            return TextMetrics.empty()

        # 1. Basic Character Metrics
        total_chars = len(text)
        chars_no_spaces = len(re.sub(r'\s', '', text))

        # 2. Tokenization
        words = self.tokenizer.extract_words(text)
        sentences = self.tokenizer.extract_sentences(text)
        paragraphs = self.tokenizer.extract_paragraphs(text)

        total_words = len(words)
        if total_words == 0:
            return TextMetrics.empty()

        # 3. Word & Vocabulary Metrics
        lower_words = [w.lower() for w in words]
        word_counter = Counter(lower_words)
        unique_words = len(word_counter)
        vocabulary_density = round((unique_words / total_words) * 100, 2)

        total_word_chars = sum(len(w) for w in words)
        avg_word_length = round(total_word_chars / total_words, 2)
        longest_word = max(words, key=len) if words else ""

        # 4. Sentence & Paragraph Metrics
        total_sentences = max(1, len(sentences))
        total_paragraphs = max(1, len(paragraphs))
        avg_sentence_len = round(total_words / total_sentences, 2)

        # 5. Syllable & Readability Calculations
        total_syllables = sum(
            self.tokenizer.count_syllables_in_word(w) for w in words
        )
        readability = ReadabilityCalculator.calculate_readability(
            total_words=total_words,
            total_sentences=total_sentences,
            total_syllables=total_syllables
        )
        reading_time = ReadabilityCalculator.estimate_time(total_words=total_words)

        # 6. Keyword Frequencies
        keywords_pool = lower_words
        if filter_stopwords:
            keywords_pool = [w for w in keywords_pool if w not in DEFAULT_STOPWORDS]

        filtered_counter = Counter(keywords_pool) if keywords_pool else word_counter
        most_common = filtered_counter.most_common(top_n_keywords)

        top_keywords = [
            KeywordFrequency(
                word=word,
                count=count,
                density_percent=round((count / total_words) * 100, 2)
            )
            for word, count in most_common
        ]

        return TextMetrics(
            characters_total=total_chars,
            characters_no_spaces=chars_no_spaces,
            words_total=total_words,
            words_unique=unique_words,
            vocabulary_density=vocabulary_density,
            sentences_total=len(sentences),
            paragraphs_total=len(paragraphs),
            avg_word_length=avg_word_length,
            avg_sentence_length=avg_sentence_len,
            longest_word=longest_word,
            reading_time=reading_time,
            readability=readability,
            top_keywords=top_keywords
        )
