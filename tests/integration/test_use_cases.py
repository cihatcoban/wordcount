"""Integration tests for application Use Cases."""

import unittest
from wordcount.application.dtos import AnalyzeTextCommand
from wordcount.application.use_cases import AnalyzeTextUseCase


class TestAnalyzeTextUseCase(unittest.TestCase):

    def setUp(self):
        self.use_case = AnalyzeTextUseCase(max_text_length=1000)

    def test_execute_success(self):
        command = AnalyzeTextCommand(
            text="Domain-Driven Design and Clean Architecture provide high cohesion and loose coupling.",
            top_n_keywords=3
        )
        result = self.use_case.execute(command)

        self.assertGreater(result.words_total, 5)
        self.assertGreater(result.characters_total, 20)
        self.assertGreater(result.execution_time_ms, 0.0)
        self.assertIsInstance(result.to_dict(), dict)

    def test_execute_exceeds_max_length(self):
        command = AnalyzeTextCommand(text="A" * 1500)
        with self.assertRaises(ValueError) as ctx:
            self.use_case.execute(command)
        self.assertIn("exceeds maximum allowed length", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
