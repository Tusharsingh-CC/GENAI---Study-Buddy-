"""
flashcard_generator.py
Generates simple "fill in the blank" flashcards from the study text.

The idea (easy to explain in a viva):
1. Find the most important (frequent, non-stopword) word in a sentence.
2. Replace that word with a blank "_____" to make the QUESTION.
3. The word we removed becomes the ANSWER.

Example:
  Sentence: "The mitochondria produces energy for the cell."
  Keyword:  "mitochondria" (an important, frequent word)
  Question: "The _____ produces energy for the cell."
  Answer:   "mitochondria"
"""

from text_utils import split_sentences, word_frequencies, clean_and_tokenize


def _find_keyword(sentence: str, freqs) -> str:
    """Find the most important word in this sentence, based on how often
    it appears in the whole text (using the frequencies we already counted)."""
    words = clean_and_tokenize(sentence)
    candidates = [w for w in words if w in freqs]
    if not candidates:
        return None
    # Pick the word with the highest overall frequency in the text
    best_word = max(candidates, key=lambda w: freqs[w])
    return best_word


def _make_blank(sentence: str, keyword: str) -> str:
    """Replace the keyword in the sentence with a blank, keeping the
    original capitalization of the rest of the sentence untouched."""
    # Replace whole-word matches only (case-insensitive), keep it simple
    import re
    pattern = re.compile(r"\b" + re.escape(keyword) + r"\b", re.IGNORECASE)
    return pattern.sub("_____", sentence, count=1)


def generate_flashcards(text: str, num_cards: int = 5) -> list:
    """Return a list of (question, answer) tuples."""
    if not text or not text.strip():
        return []

    sentences = split_sentences(text)
    freqs = word_frequencies(text)

    # Only use sentences of a reasonable length (not too short, not a wall of text)
    good_sentences = [s for s in sentences if 5 <= len(s.split()) <= 30]

    cards = []
    used_keywords = set()

    # Sort sentences so the ones with the most "important" content go first
    good_sentences.sort(
        key=lambda s: sum(freqs.get(w, 0) for w in clean_and_tokenize(s)),
        reverse=True,
    )

    for sentence in good_sentences:
        if len(cards) >= num_cards:
            break

        keyword = _find_keyword(sentence, freqs)
        if not keyword or keyword in used_keywords:
            continue  # skip if no keyword found, or we already used this keyword

        question = _make_blank(sentence, keyword)
        cards.append((question, keyword))
        used_keywords.add(keyword)

    return cards
