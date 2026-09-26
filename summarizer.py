"""
summarizer.py
A simple EXTRACTIVE summarizer.

"Extractive" means we don't generate new sentences - we pick the most
important EXISTING sentences from the original text and return them
in their original order. This is simple, has no external AI model,
and is easy to explain in a viva:

1. Count how often each important word appears in the whole text.
2. Score every sentence by how many "important" words it contains.
3. Pick the top N highest-scoring sentences.
4. Put them back in their original order so the summary reads naturally.
"""

from text_utils import split_sentences, word_frequencies, score_sentence


def summarize(text: str, num_sentences: int = 3) -> str:
    """Return a short summary made of the top `num_sentences` sentences."""
    if not text or not text.strip():
        return "Please paste some study text first."

    sentences = split_sentences(text)

    if len(sentences) == 0:
        return "Please paste some study text first."

    if len(sentences) <= num_sentences:
        # Nothing to summarize - the text is already short.
        return text.strip()

    freqs = word_frequencies(text)

    # Score every sentence, keeping track of its original position (index)
    scored = [
        (i, sentence, score_sentence(sentence, freqs))
        for i, sentence in enumerate(sentences)
    ]

    # Sort by score (highest first) and take the top N
    top_sentences = sorted(scored, key=lambda item: item[2], reverse=True)[:num_sentences]

    # Sort the chosen sentences back into their ORIGINAL order
    top_sentences_in_order = sorted(top_sentences, key=lambda item: item[0])

    summary = " ".join(sentence for _, sentence, _ in top_sentences_in_order)
    return summary
