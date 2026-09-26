Notes to Flashcards & Quiz Generator
Python | Gradio | NLP
- Built an offline web application in Python and Gradio that converts pasted study notes into a condensed summary, fill-in-the-blank flashcards, and a multiple-choice quiz.
- Implemented extractive summarisation using word-frequency scoring to rank sentences by term importance — requiring no external AI model, API key, or internet connection.
- Generated flashcards and MCQs by extracting the top-scoring keyword from each sentence as the answer, with shuffled distractors drawn from the notes.
- Designed the pipeline around transparent, deterministic logic, making every step reproducible and easy to run, test, and explain.
