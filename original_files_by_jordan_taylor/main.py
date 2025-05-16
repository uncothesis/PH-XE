# 3.12

import os
import time
import yaml
import pandas as pd
from dotenv import load_dotenv
from together import Together
from tqdm import tqdm

# Load API key from .env
load_dotenv()

def load_models(yaml_path="models.yaml"):
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return [model["name"] for model in data.get("models", [])]

def call_together_api(prompt, model_name):
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Load data
df = pd.read_csv("questions.csv")
sample = df.sample(5).reset_index(drop=True)

models = load_models("models.yaml")
model_name = models[0]

# Run questions
results = []
for _, row in tqdm(sample.iterrows(), total=len(sample), desc="Evaluating"):
    question = row['question']
    options = f"A) {row['A']}\nB) {row['B']}\nC) {row['C']}\nD) {row['D']}"
    correct = row['correct_answer']

    prompt = f"Question: {question}\n\n{options}\n\nWhich option (A/B/C/D) is correct?"
    response = call_together_api(prompt, model_name)
    match = correct.lower() in response.lower()

    results.append({
        "question": question,
        "correct": correct,
        "response": response,
        "is_correct": match
    })

    time.sleep(1)

# Summary
num_correct = sum(r['is_correct'] for r in results)
print(f"\nModel Accuracy: {num_correct} / {len(results)} correct")

# Show only incorrects
incorrect = [r for r in results if not r['is_correct']]
if incorrect:
    print("\nIncorrect Responses:")
    for r in incorrect:
        print(f"\nQ: {r['question']}\nExpected: {r['correct']}\nModel said: {r['response']}")