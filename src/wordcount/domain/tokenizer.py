"""Tokenizer and linguistic extraction domain service.

Provides robust, Unicode-aware text segmentation, sentence detection,
paragraph extraction, and syllable approximation.
"""

from __future__ import annotations
import re
from typing import List

WORD_REGEX = re.compile(r"\b[\w]+(?:['’\-][\w]+)*\b", re.UNICODE)

# Honorific titles that almost never end a sentence
TITLES = {
    "dr.", "mr.", "mrs.", "ms.", "prof.", "sr.", "jr.", "rev.", "gen.", "col.", "sen.", "rep."
}

# Latin abbreviations typically followed by non-sentence words
INLINE_ABBREVIATIONS = {
    "e.g.", "i.e.", "vs.", "etc.", "fig.", "dept.", "inc.", "ltd."
}


class Tokenizer:
    """Domain service responsible for tokenizing raw text into domain primitives."""

    @staticmethod
    def extract_words(text: str) -> List[str]:
        """Extract clean words from raw text, filtering out standalone numbers and punctuation."""
        if not text:
            return []
        tokens = WORD_REGEX.findall(text)
        return [tok for tok in tokens if any(c.isalpha() for c in tok)]

    @staticmethod
    def extract_sentences(text: str) -> List[str]:
        """Split text into sentences while respecting titles and abbreviations."""
        trimmed = text.strip()
        if not trimmed:
            return []

        # Split on sentence terminals (. ! ?) followed by whitespace
        raw_chunks = re.split(r'(?<=[.!?])\s+', trimmed)
        sentences: List[str] = []

        buffer = ""
        for i, chunk in enumerate(raw_chunks):
            if not chunk:
                continue
            if buffer:
                buffer += " " + chunk
            else:
                buffer = chunk

            words = buffer.strip().split()
            last_token = words[-1].lower() if words else ""

            # Check if last token is an honorific title or single initial (e.g., "Dr.", "A.")
            is_title = last_token in TITLES or bool(re.match(r'^[a-z]\.$', last_token))
            # Check if last token is internal acronym like "d.c."
            is_acronym = bool(re.match(r'^([a-z]\.)+[a-z]?$', last_token)) and last_token not in {"p.m.", "a.m."}

            if is_title or is_acronym:
                continue

            sentences.append(buffer.strip())
            buffer = ""

        if buffer:
            sentences.append(buffer.strip())

        return [s for s in sentences if s and any(c.isalnum() for c in s)]

    @staticmethod
    def extract_paragraphs(text: str) -> List[str]:
        """Split text into logical paragraphs (separated by blank lines)."""
        if not text.strip():
            return []
        paragraphs = re.split(r'\n\s*\n', text.strip())
        return [p.strip() for p in paragraphs if p.strip()]

    @staticmethod
    def count_syllables_in_word(word: str) -> int:
        """Estimate syllable count for a given word using standard linguistic heuristics."""
        clean = word.lower().strip(".:;?!'\"()[]{}")
        if not clean:
            return 0
        if len(clean) <= 3:
            return 1

        vowels = "aeiouy"
        count = len(re.findall(r'[aeiouy]+', clean))

        if clean.endswith('e') and not clean.endswith('le') and count > 1:
            count -= 1
        elif clean.endswith('ed') and not clean.endswith('ted') and not clean.endswith('ded') and count > 1:
            count -= 1

        return max(1, count)
