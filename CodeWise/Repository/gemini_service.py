from django.conf import settings
from google import genai
from google.genai import types
import json
client=genai.Client(api_key=settings.GEMINI_API_KEY)

def evaluate_answer(question,student_answer):
    prompt = f"""
    
    You ar2e an experienced Python programming instructor.

    Analyse the student's submitted answer based on the question.

    QUESTION:
    {question}

    STUDENT ANSWER:
    {student_answer}

    Return the evaluation in JSON format with exactly these keys:

    {{
        "correctness": "Explain whether the answer is correct.",
        "explanation": [
            "Step 1 explanation",
            "Step 2 explanation"
        ],
        "errors": "Mention errors or missing cases.",
        "improvements": [
            "Improvement suggestion 1",
            "Improvement suggestion 2"
        ],
        "overallfeedback": "Give encouraging feedback."
    }}

    Important:
    - Return valid JSON only.
    - Do not include Markdown code fences.
    - Do not add any text outside the JSON.
    - Use beginner-friendly language.
    """


    response=client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    feedback=json.loads(response.text)
    return feedback
