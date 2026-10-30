"""Unit tests for ReadabilityCalculator."""

import unittest
from wordcount.domain.readability import ReadabilityCalculator


class TestReadabilityCalculator(unittest.TestCase):

    def test_calculate_readability_empty(self):
        score = ReadabilityCalculator.calculate_readability(0, 0, 0)
        self.assertEqual(score.flesch_reading_ease, 100.0)
        self.assertEqual(score.flesch_kincaid_grade, 0.0)
        self.assertEqual(score.reading_level, "N/A")

    def test_calculate_readability_simple(self):
        # 10 words, 1 sentence, 12 syllables
        score = ReadabilityCalculator.calculate_readability(10, 1, 12)
        self.assertGreater(score.flesch_reading_ease, 0.0)
        self.assertLessEqual(score.flesch_reading_ease, 100.0)
        self.assertIsInstance(score.reading_level, str)

    def test_estimate_time(self):
        time_est = ReadabilityCalculator.estimate_time(450)
        self.assertEqual(time_est.reading_minutes, 2.0)
        self.assertEqual(time_est.reading_time_formatted, "2 min")
        self.assertGreater(time_est.speaking_minutes, 3.0)


if __name__ == "__main__":
    unittest.main()
