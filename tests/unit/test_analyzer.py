"""Unit tests for TextAnalyzer domain service."""

import unittest
from wordcount.domain.analyzer import TextAnalyzer


class TestTextAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = TextAnalyzer()

    def test_analyze_empty_string(self):
        metrics = self.analyzer.analyze("")
        self.assertEqual(metrics.words_total, 0)
        self.assertEqual(metrics.characters_total, 0)
        self.assertEqual(len(metrics.top_keywords), 0)

    def test_analyze_whitespace_only(self):
        metrics = self.analyzer.analyze("   \n\t  ")
        self.assertEqual(metrics.words_total, 0)

    def test_analyze_simple_text(self):
        text = "Keystone is an architectural framework. Keystone makes code clean."
        metrics = self.analyzer.analyze(text, top_n_keywords=5)

        self.assertEqual(metrics.words_total, 9)
        self.assertEqual(metrics.words_unique, 8)
        self.assertEqual(metrics.sentences_total, 2)
        self.assertEqual(metrics.paragraphs_total, 1)
        self.assertGreater(metrics.characters_total, 0)
        self.assertGreater(metrics.characters_no_spaces, 0)
        self.assertEqual(metrics.top_keywords[0].word, "keystone")
        self.assertEqual(metrics.top_keywords[0].count, 2)

    def test_analyze_with_stopwords_filter(self):
        text = "the quick brown fox jumps over the lazy dog"
        metrics = self.analyzer.analyze(text, top_n_keywords=5, filter_stopwords=True)
        # 'the' is a stopword and should be excluded from top keywords
        keyword_words = [kw.word for kw in metrics.top_keywords]
        self.assertNotIn("the", keyword_words)


if __name__ == "__main__":
    unittest.main()
