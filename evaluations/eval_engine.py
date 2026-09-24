import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-20b"

EVAL_DATASET = [
    {
        "question": "What is the capital of France?",
        "context": "France is a country in Europe. Its capital is Paris. Paris is known for the Eiffel Tower.",
        "answer": "The capital of France is Paris.",
    },
    {
        "question": "What is 2+2?",
        "context": "Basic arithmetic: 2+2 equals 4.",
        "answer": "2+2 equals 4.",
    },
    {
        "question": "Who wrote Hamlet?",
        "context": "Hamlet is a play by William Shakespeare, written around 1600.",
        "answer": "Hamlet was written by Charles Dickens.",
    },
]

def judge_faithfulness(question, context, answer):
    prompt = f"""You are an evaluation judge. Score the FAITHFULNESS of the answer on a scale of 0 to 1.
Faithfulness = is the answer derived ONLY from the given context? 1 = fully faithful, 0 = hallucinated.

Context: {context}
Answer: {answer}

Respond ONLY with a number between 0 and 1. Nothing else."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    try:
        return float(response.choices[0].message.content.strip())
    except:
        return 0.0

def judge_relevance(question, answer):
    prompt = f"""You are an evaluation judge. Score the RELEVANCE of the answer to the question on 0 to 1.
1 = directly answers the question, 0 = completely off-topic.

Question: {question}
Answer: {answer}

Respond ONLY with a number between 0 and 1. Nothing else."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    try:
        return float(response.choices[0].message.content.strip())
    except:
        return 0.0

def run_evaluation():
    results = []
    for row in EVAL_DATASET:
        faith = judge_faithfulness(row["question"], row["context"], row["answer"])
        rel = judge_relevance(row["question"], row["answer"])
        results.append({
            "question": row["question"],
            "answer": row["answer"],
            "faithfulness": faith,
            "answer_relevance": rel,
        })
    return results

if __name__ == "__main__":
    print(json.dumps(run_evaluation(), indent=2))
