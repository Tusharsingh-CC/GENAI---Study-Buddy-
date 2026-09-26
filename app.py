"""
app.py
Main entry point for the AI Study Assistant.

This file only handles the USER INTERFACE (Gradio). All the actual logic
lives in separate files:
    - summarizer.py           -> summarize()
    - flashcard_generator.py  -> generate_flashcards()
    - quiz_generator.py       -> generate_quiz()

Run this file to start the app:  python app.py
"""

import gradio as gr

from summarizer import summarize
from flashcard_generator import generate_flashcards
from quiz_generator import generate_quiz


# ---------------------------------------------------------------------
# "Adapter" functions: these connect our plain-Python logic functions
# to what Gradio needs (they format the output nicely as Markdown/text).
# ---------------------------------------------------------------------

def run_summary(study_text: str, num_sentences: int) -> str:
    return summarize(study_text, num_sentences=int(num_sentences))


def run_flashcards(study_text: str, num_cards: int) -> str:
    cards = generate_flashcards(study_text, num_cards=int(num_cards))
    if not cards:
        return "Couldn't generate flashcards. Try pasting a longer piece of text (at least a few full sentences)."

    lines = []
    for i, (question, answer) in enumerate(cards, 1):
        lines.append(f"**Card {i}**")
        lines.append(f"Q: {question}")
        lines.append(f"A: {answer}")
        lines.append("")
    return "\n".join(lines)


def run_quiz(study_text: str, num_questions: int) -> str:
    quiz = generate_quiz(study_text, num_questions=int(num_questions))
    if not quiz:
        return ("Couldn't generate a quiz. Try pasting a longer piece of text "
                 "(the quiz needs enough different important words to create answer choices).")

    lines = []
    letters = ["A", "B", "C", "D"]
    for i, item in enumerate(quiz, 1):
        lines.append(f"**Q{i}. {item['question']}**")
        for letter, option in zip(letters, item["options"]):
            lines.append(f"   {letter}) {option}")
        lines.append(f"*Answer: {item['answer']}*")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------
# UI layout
# ---------------------------------------------------------------------

with gr.Blocks(title="AI Study Assistant") as demo:
    gr.Markdown("# 📚 AI Study Assistant")
    gr.Markdown(
        "Paste your notes or textbook paragraph below, then use the tabs to "
        "generate a summary, flashcards, or a quiz from it."
    )

    study_input = gr.Textbox(
        label="Your Study Text",
        placeholder="Paste your notes, article, or textbook paragraph here...",
        lines=10,
    )

    with gr.Tab("📝 Summary"):
        summary_slider = gr.Slider(1, 10, value=3, step=1, label="Number of sentences in summary")
        summary_btn = gr.Button("Generate Summary", variant="primary")
        summary_output = gr.Textbox(label="Summary", lines=6)
        summary_btn.click(fn=run_summary, inputs=[study_input, summary_slider], outputs=summary_output)

    with gr.Tab("🗂️ Flashcards"):
        flashcard_slider = gr.Slider(1, 10, value=5, step=1, label="Number of flashcards")
        flashcard_btn = gr.Button("Generate Flashcards", variant="primary")
        flashcard_output = gr.Markdown(label="Flashcards")
        flashcard_btn.click(fn=run_flashcards, inputs=[study_input, flashcard_slider], outputs=flashcard_output)

    with gr.Tab("❓ Quiz"):
        quiz_slider = gr.Slider(1, 10, value=4, step=1, label="Number of quiz questions")
        quiz_btn = gr.Button("Generate Quiz", variant="primary")
        quiz_output = gr.Markdown(label="Quiz")
        quiz_btn.click(fn=run_quiz, inputs=[study_input, quiz_slider], outputs=quiz_output)


if __name__ == "__main__":
    demo.launch()
