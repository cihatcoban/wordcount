"""Unit tests for Domain models and value objects."""

import unittest
from wordcount.domain.models import (
    KeywordFrequency,
    ReadabilityScore,
    ReadingTime,
    TextMetrics
)


class TestDomainModels(unittest.TestCase):

    def test_keyword_frequency_valid(self):
        kf = KeywordFrequency(word="architecture", count=5, density_percent=12.5)
        self.assertEqual(kf.word, "architecture")
        self.assertEqual(kf.count, 5)
        self.assertEqual(kf.density_percent, 12.5)

    def test_keyword_frequency_invalid_count(self):
        with self.assertRaises(ValueError):
            KeywordFrequency(word="test", count=-1, density_percent=10.0)

    def test_keyword_frequency_invalid_density(self):
        with self.assertRaises(ValueError):
            KeywordFrequency(word="test", count=2, density_percent=150.0)

    def test_text_metrics_empty_factory(self):
        metrics = TextMetrics.empty()
        self.assertEqual(metrics.words_total, 0)
        self.assertEqual(metrics.characters_total, 0)
        self.assertEqual(metrics.sentences_total, 0)
        self.assertEqual(metrics.paragraphs_total, 0)
        self.assertEqual(len(metrics.top_keywords), 0)
        self.assertEqual(metrics.reading_time.reading_minutes, 0.0)


if __name__ == "__main__":
    unittest.main()
