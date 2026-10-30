"""Application Use Cases.

Coordinates domain services, handles execution tracing, input validation,
and converts domain entities to transport-safe DTOs.
"""

from __future__ import annotations
import time
from typing import Optional

from wordcount.application.dtos import (
    AnalyzeTextCommand,
    TextAnalysisResultDTO
)
from wordcount.domain.analyzer import TextAnalyzer


class AnalyzeTextUseCase:
    """Primary application use case for processing and analyzing text bodies."""

    def __init__(
        self,
        analyzer: Optional[TextAnalyzer] = None,
        max_text_length: int = 2_000_000
    ):
        self.analyzer = analyzer or TextAnalyzer()
        self.max_text_length = max_text_length

    def execute(self, command: AnalyzeTextCommand) -> TextAnalysisResultDTO:
        """Execute text analysis with constraint validation and performance tracking."""
        command.validate(max_length=self.max_text_length)

        start_time = time.perf_counter()

        metrics = self.analyzer.analyze(
            text=command.text,
            top_n_keywords=command.top_n_keywords,
            filter_stopwords=command.filter_stopwords
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return TextAnalysisResultDTO.from_domain(
            metrics=metrics,
            execution_time_ms=elapsed_ms
        )
