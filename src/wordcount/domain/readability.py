"""Readability and estimation domain service.

Calculates Flesch Reading Ease, Flesch-Kincaid Grade level,
and estimated reading / speaking times.
"""

from __future__ import annotations
import math
from wordcount.domain.models import ReadabilityScore, ReadingTime


class ReadabilityCalculator:
    """Domain service for calculating reading complexity and timing estimates."""

    AVERAGE_READING_WPM = 225.0
    AVERAGE_SPEAKING_WPM = 135.0

    @classmethod
    def calculate_readability(
        cls,
        total_words: int,
        total_sentences: int,
        total_syllables: int
    ) -> ReadabilityScore:
        """Compute Flesch Reading Ease and Flesch-Kincaid Grade Level."""
        if total_words == 0 or total_sentences == 0:
            return ReadabilityScore(
                flesch_reading_ease=100.0,
                flesch_kincaid_grade=0.0,
                reading_level="N/A",
                notes="Insufficient text for score calculation."
            )

        asl = total_words / total_sentences  # Average Sentence Length
        asw = total_syllables / total_words  # Average Syllables per Word

        # Flesch Reading Ease formula
        fre = 206.835 - (1.015 * asl) - (84.6 * asw)
        fre = max(0.0, min(100.0, fre))

        # Flesch-Kincaid Grade Level formula
        fkg = (0.39 * asl) + (11.8 * asw) - 15.59
        fkg = max(0.0, fkg)

        # Categorize reading level based on Flesch score
        if fre >= 90:
            level = "Very Easy (5th Grade)"
            notes = "Easily understood by an average 11-year-old student."
        elif fre >= 80:
            level = "Easy (6th Grade)"
            notes = "Conversational English for consumers."
        elif fre >= 70:
            level = "Fairly Easy (7th Grade)"
            notes = "Accessible reading for most adults."
        elif fre >= 60:
            level = "Standard (8th-9th Grade)"
            notes = "Plain English; suitable for newspapers and public articles."
        elif fre >= 50:
            level = "Fairly Difficult (10th-12th Grade)"
            notes = "High school level; suitable for technical blogs or essays."
        elif fre >= 30:
            level = "Difficult (College)"
            notes = "Academic articles and business reports."
        else:
            level = "Very Difficult (Graduate Level)"
            notes = "Scientific, legal, or dense scholarly text."

        return ReadabilityScore(
            flesch_reading_ease=round(fre, 1),
            flesch_kincaid_grade=round(fkg, 1),
            reading_level=level,
            notes=notes
        )

    @classmethod
    def estimate_time(cls, total_words: int) -> ReadingTime:
        """Calculate estimated silent reading time and spoken presentation time."""
        if total_words <= 0:
            return ReadingTime(
                reading_minutes=0.0,
                reading_time_formatted="0 sec",
                speaking_minutes=0.0,
                speaking_time_formatted="0 sec"
            )

        read_mins = total_words / cls.AVERAGE_READING_WPM
        speak_mins = total_words / cls.AVERAGE_SPEAKING_WPM

        return ReadingTime(
            reading_minutes=round(read_mins, 2),
            reading_time_formatted=cls._format_duration(read_mins),
            speaking_minutes=round(speak_mins, 2),
            speaking_time_formatted=cls._format_duration(speak_mins)
        )

    @staticmethod
    def _format_duration(minutes: float) -> str:
        total_seconds = math.ceil(minutes * 60)
        if total_seconds < 60:
            return f"{total_seconds} sec"
        mins = total_seconds // 60
        secs = total_seconds % 60
        if secs == 0:
            return f"{mins} min"
        return f"{mins} min {secs} sec"
