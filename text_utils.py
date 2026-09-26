"""
text_utils.py
Small shared helper functions used by summarizer.py, flashcard_generator.py,
and quiz_generator.py.

Keeping these in one place avoids repeating the same code three times
(a good practice to mention in a viva: "DRY - Don't Repeat Yourself").
"""

import re
from collections import Counter

# A short manual list of common English "stopwords" - words that appear
# everywhere and carry very little meaning (the, is, and, etc).
# We exclude them so our summarizer/quiz focuses on IMPORTANT words instead.
STOPWORDS = set("""
a an the this that these those is are was were be been being
of in on at to for with from by as it its it's into over under
and or but if then so because than too very
i you he she we they them his her our your their
not no do does did doing have has had having
can could will would shall should may might must
about above after again all also am any been before below between
both down during each few further here how more most other own
same some such up while
through using use used uses called based found releasing
""".split())


def clean_and_tokenize(text: str) -> list:
    """Lowercase the text and split it into a list of words only
    (numbers/punctuation removed)."""
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return words


def split_sentences(text: str) -> list:
    """Split a block of text into a list of sentences.

    This is a SIMPLE rule-based splitter: it breaks the text wherever it
    sees '.', '!' or '?' followed by a space or end of text.
    It won't be perfect (e.g. 'Mr. Smith' would be split), but it's easy
    to understand and good enough for study notes.
    """
    text = text.strip()
    if not text:
        return []
    # Split on . ! ? followed by whitespace
    raw_sentences = re.split(r"(?<=[.!?])\s+", text)
    # Clean up and drop empty/very short fragments
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 0]
    return sentences


def word_frequencies(text: str) -> Counter:
    """Count how often each meaningful (non-stopword) word appears.

    Words that appear more often are treated as more 'important' -
    this is the core idea behind our simple summarizer and keyword picker.
    """
    words = clean_and_tokenize(text)
    significant_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return Counter(significant_words)


def score_sentence(sentence: str, freqs: Counter) -> float:
    """Give a sentence a numeric importance score: the sum of the
    frequency-scores of its significant words, divided by sentence length
    so that very long sentences don't win just by containing more words."""
    words = clean_and_tokenize(sentence)
    if not words:
        return 0.0
    total = sum(freqs.get(w, 0) for w in words)
    return total / len(words)
