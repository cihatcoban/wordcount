"""Command-line presentation adapter for WordCount.

Allows running analysis directly in the terminal, piped from files or stdin.
Example:
    python -m wordcount.presentation.cli "Hello world! This is a test."
    cat my_essay.md | python -m wordcount.presentation.cli -
"""

from __future__ import annotations
import argparse
import json
import sys

from wordcount.application.dtos import AnalyzeTextCommand
from wordcount.application.use_cases import AnalyzeTextUseCase


def main() -> None:
    """CLI Entry point."""
    parser = argparse.ArgumentParser(
        description="WordCount Pro - Industrial Text & Readability Analyzer"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Input text string or '-' to read from standard input"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of formatted text"
    )
    parser.add_argument(
        "--stopwords",
        action="store_true",
        help="Filter out common stopwords from keyword density analysis"
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top keywords to display (default: 10)"
    )

    args = parser.parse_args()

    if args.input == "-":
        if sys.stdin.isatty():
            print("Enter text (press Ctrl+D on Unix or Ctrl+Z on Windows to analyze):")
        text = sys.stdin.read()
    else:
        text = args.input

    if not text.strip():
        print("Error: Empty input provided.", file=sys.stderr)
        sys.exit(1)

    use_case = AnalyzeTextUseCase()
    command = AnalyzeTextCommand(
        text=text,
        top_n_keywords=args.top,
        filter_stopwords=args.stopwords
    )

    try:
        result = use_case.execute(command)
    except Exception as e:
        print(f"Error analyzing text: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        return

    # Formatted terminal output
    print("\n" + "=" * 50)
    print("        WORDCOUNT PRO - TEXT ANALYSIS REPORT")
    print("=" * 50)
    print(f"  Total Words:          {result.words_total:,}")
    print(f"  Unique Words:         {result.words_unique:,} ({result.vocabulary_density}% density)")
    print(f"  Total Characters:     {result.characters_total:,} ({result.characters_no_spaces:,} non-space)")
    print(f"  Sentences:            {result.sentences_total:,}")
    print(f"  Paragraphs:           {result.paragraphs_total:,}")
    print(f"  Avg Word Length:      {result.avg_word_length} chars")
    print(f"  Avg Sentence Length:  {result.avg_sentence_length} words")
    print(f"  Longest Word:         {result.longest_word}")
    print("-" * 50)
    print("READABILITY & SPEED:")
    print(f"  Flesch Reading Ease:  {result.readability.flesch_reading_ease}/100 ({result.readability.reading_level})")
    print(f"  Flesch-Kincaid Grade: {result.readability.flesch_kincaid_grade}")
    print(f"  Reading Time:         {result.reading_time.reading_time_formatted}")
    print(f"  Speaking Time:        {result.reading_time.speaking_time_formatted}")
    print("-" * 50)
    print(f"TOP {len(result.top_keywords)} KEYWORDS:")
    for kw in result.top_keywords:
        print(f"  - {kw.word:<18} count: {kw.count:<4} ({kw.density_percent}%)")
    print("=" * 50)
    print(f"Execution took: {result.execution_time_ms} ms\n")


if __name__ == "__main__":
    main()
