"""
quiz_generator.py
Builds multiple-choice quiz questions on top of the same "blank the
keyword" idea used in flashcard_generator.py.

Steps (easy to explain in a viva):
1. Reuse flashcard generation to get (question_with_blank, correct_answer) pairs.
2. For each question, pick 3 random WRONG answers ("distractors") from
   other important words found in the text.
3. Shuffle the 4 options (1 correct + 3 wrong) so the correct answer
   isn't always in the same position.
"""

import random
from flashcard_generator import generate_flashcards
from text_utils import word_frequencies


def generate_quiz(text: str, num_questions: int = 4) -> list:
    """Return a list of dicts, each shaped like:
    {
        "question": "The _____ produces energy for the cell.",
        "options": ["mitochondria", "nucleus", "ribosome", "protein"],
        "answer": "mitochondria"
    }
    """
    if not text or not text.strip():
        return []

    # Step 1: reuse the flashcard logic to get question/answer pairs
    cards = generate_flashcards(text, num_cards=num_questions)
    if not cards:
        return []

    # Step 2: build a pool of possible "wrong answer" words from the whole text
    freqs = word_frequencies(text)
    all_keywords = list(freqs.keys())

    quiz = []
    for question, correct_answer in cards:
        # Pick distractor words: important words that are NOT the correct answer
        distractor_pool = [w for w in all_keywords if w != correct_answer]
        random.shuffle(distractor_pool)
        distractors = distractor_pool[:3]

        # If the text is too short to find 3 distractors, skip this question
        if len(distractors) < 3:
            continue

        options = distractors + [correct_answer]
        random.shuffle(options)

        quiz.append({
            "question": question,
            "options": options,
            "answer": correct_answer,
        })

    return quiz
