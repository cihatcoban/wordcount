"""Application Data Transfer Objects (DTOs).

Defines strongly-typed input commands and output representations
decoupling the domain layer from web/API transports.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from wordcount.domain.models import TextMetrics


@dataclass(frozen=True)
class AnalyzeTextCommand:
    """Input command for analyzing text."""
    text: str
    top_n_keywords: int = 10
    filter_stopwords: bool = False
    source_name: Optional[str] = None

    def validate(self, max_length: int = 2_000_000) -> None:
        """Validate command constraints to prevent DoS and malicious payloads."""
        if len(self.text) > max_length:
            raise ValueError(
                f"Input text exceeds maximum allowed length of {max_length} characters (got {len(self.text)})."
            )
        if self.top_n_keywords < 1 or self.top_n_keywords > 100:
            raise ValueError(
                f"top_n_keywords must be between 1 and 100, got {self.top_n_keywords}."
            )


@dataclass(frozen=True)
class KeywordItemDTO:
    word: str
    count: int
    density_percent: float


@dataclass(frozen=True)
class ReadabilityDTO:
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    reading_level: str
    notes: str


@dataclass(frozen=True)
class ReadingTimeDTO:
    reading_minutes: float
    reading_time_formatted: str
    speaking_minutes: float
    speaking_time_formatted: str


@dataclass(frozen=True)
class TextAnalysisResultDTO:
    """Standardized output DTO containing full analytics."""
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
    reading_time: ReadingTimeDTO
    readability: ReadabilityDTO
    top_keywords: List[KeywordItemDTO]
    execution_time_ms: float

    @classmethod
    def from_domain(cls, metrics: TextMetrics, execution_time_ms: float = 0.0) -> TextAnalysisResultDTO:
        return cls(
            characters_total=metrics.characters_total,
            characters_no_spaces=metrics.characters_no_spaces,
            words_total=metrics.words_total,
            words_unique=metrics.words_unique,
            vocabulary_density=metrics.vocabulary_density,
            sentences_total=metrics.sentences_total,
            paragraphs_total=metrics.paragraphs_total,
            avg_word_length=metrics.avg_word_length,
            avg_sentence_length=metrics.avg_sentence_length,
            longest_word=metrics.longest_word,
            reading_time=ReadingTimeDTO(
                reading_minutes=metrics.reading_time.reading_minutes,
                reading_time_formatted=metrics.reading_time.reading_time_formatted,
                speaking_minutes=metrics.reading_time.speaking_minutes,
                speaking_time_formatted=metrics.reading_time.speaking_time_formatted
            ),
            readability=ReadabilityDTO(
                flesch_reading_ease=metrics.readability.flesch_reading_ease,
                flesch_kincaid_grade=metrics.readability.flesch_kincaid_grade,
                reading_level=metrics.readability.reading_level,
                notes=metrics.readability.notes
            ),
            top_keywords=[
                KeywordItemDTO(
                    word=k.word,
                    count=k.count,
                    density_percent=k.density_percent
                )
                for k in metrics.top_keywords
            ],
            execution_time_ms=round(execution_time_ms, 2)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary representation."""
        return asdict(self)
