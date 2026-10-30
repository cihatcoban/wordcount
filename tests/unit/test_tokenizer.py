"""Unit tests for Tokenizer service."""

import unittest
from wordcount.domain.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):

    def test_extract_words_basic(self):
        text = "Hello world! This is a test."
        words = Tokenizer.extract_words(text)
        self.assertEqual(words, ["Hello", "world", "This", "is", "a", "test"])

    def test_extract_words_contractions_and_hyphens(self):
        text = "Don't stop, it's state-of-the-art technology."
        words = Tokenizer.extract_words(text)
        self.assertIn("Don't", words)
        self.assertIn("it's", words)
        self.assertIn("state-of-the-art", words)

    def test_extract_words_unicode_turkish(self):
        text = "Çok yaşa, ılık süt iç, şifalı olsun."
        words = Tokenizer.extract_words(text)
        self.assertEqual(words, ["Çok", "yaşa", "ılık", "süt", "iç", "şifalı", "olsun"])

    def test_extract_words_ignores_pure_numbers_and_punctuation(self):
        text = "123 456 ... --- !!! $$$"
        words = Tokenizer.extract_words(text)
        self.assertEqual(words, [])

    def test_extract_sentences_abbreviations(self):
        text = "Dr. Smith went to Washington D.C. yesterday. He met Mr. Jones at 5 p.m. It was great!"
        sentences = Tokenizer.extract_sentences(text)
        # Should correctly identify 3 sentences:
        # 1. "Dr. Smith went to Washington D.C. yesterday."
        # 2. "He met Mr. Jones at 5 p.m."
        # 3. "It was great!"
        self.assertEqual(len(sentences), 3)
        self.assertTrue(sentences[0].startswith("Dr. Smith"))
        self.assertTrue(sentences[1].startswith("He met Mr. Jones"))
        self.assertTrue(sentences[2].startswith("It was great"))

    def test_extract_paragraphs(self):
        text = "First paragraph here.\n\nSecond paragraph here with more lines.\n\nThird paragraph."
        paragraphs = Tokenizer.extract_paragraphs(text)
        self.assertEqual(len(paragraphs), 3)

    def test_syllables_counting(self):
        self.assertEqual(Tokenizer.count_syllables_in_word("cat"), 1)
        self.assertEqual(Tokenizer.count_syllables_in_word("hello"), 2)
        self.assertEqual(Tokenizer.count_syllables_in_word("beautiful"), 3)
        self.assertEqual(Tokenizer.count_syllables_in_word("architecture"), 4)


if __name__ == "__main__":
    unittest.main()
