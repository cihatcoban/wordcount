"""Domain models for Text Analysis.

Pure Python dataclasses with zero framework dependencies.
Representing core business entities, value objects, and domain invariants.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class KeywordFrequency:
    """Value object representing frequency and relative density of a keyword."""
    word: str
    count: int
    density_percent: float

    def __post_init__(self) -> None:
        if self.count < 0:
            raise ValueError(f"count cannot be negative, got {self.count}")
        if not (0.0 <= self.density_percent <= 100.0):
            raise ValueError(f"density_percent must be between 0 and 100, got {self.density_percent}")


@dataclass(frozen=True)
class ReadabilityScore:
    """Value object capturing readability and comprehension metrics."""
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    reading_level: str
    notes: str


@dataclass(frozen=True)
class ReadingTime:
    """Estimated reading and speaking time in minutes and formatted strings."""
    reading_minutes: float
    reading_time_formatted: str
    speaking_minutes: float
    speaking_time_formatted: str


@dataclass(frozen=True)
class TextMetrics:
    """Aggregate entity representing all computed metrics for a given text body."""
    characters_total: int
    characters_no_spaces: int
    words_total: int
    words_unique: int
    vocabulary_density: float
    sentences_total: int
    paragraphs_total: int
    avg_word_length: float
    avg_sentence_length: float
    longest_word: str
    reading_time: ReadingTime
    readability: ReadabilityScore
    top_keywords: List[KeywordFrequency] = field(default_factory=list)

    @classmethod
    def empty(cls) -> TextMetrics:
        """Factory for empty text metrics."""
        return cls(
            characters_total=0,
            characters_no_spaces=0,
            words_total=0,
            words_unique=0,
            vocabulary_density=0.0,
            sentences_total=0,
            paragraphs_total=0,
            avg_word_length=0.0,
            avg_sentence_length=0.0,
            longest_word="",
            reading_time=ReadingTime(
                reading_minutes=0.0,
                reading_time_formatted="0 sec",
                speaking_minutes=0.0,
                speaking_time_formatted="0 sec"
            ),
            readability=ReadabilityScore(
                flesch_reading_ease=100.0,
                flesch_kincaid_grade=0.0,
                reading_level="N/A",
                notes="Text is empty."
            ),
            top_keywords=[]
        )
