import os
import yaml
import json
import pandas as pd
from dotenv import load_dotenv
from together import Together

# Load API key from .env
load_dotenv()


class ratings:
    def __init__(self, initial_rating: int, models: list, save_file: str = "llm_comparison.json"):
        self.file_name = save_file
        self.elo = self._load_ratings(initial_rating, models)

    def _load_ratings(self, default_rating: int, models: list)-> dict:
        if os.path.exists(self.file_name) and os.stat(self.file_name).st_size > 0:
            with open(self.file_name, 'r') as f:
                saved = json.load(f)
                return { model : saved.get(model, default_rating) for model in models}
        else:
            return {model : default_rating for model in models}

    def save(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.elo, f, indent=2)
    
    def set_rating(self,model_name: str, rating: int):
        self.elo[model_name] = rating
        self.save()

    def get_rating(self, which_model):
        return self.elo[which_model]
    

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

df = pd.read_csv("questions.csv")
sample = df.sample(1).reset_index(drop=True)

models = load_models("models.yaml")
first_model_name = models[0]
second_model_name = models[1]

def getAnswers(sample):
    row = sample.iloc[0]

    question = row['question']
    options = f"A) {row['A']}\nB) {row['B']}\nC) {row['C']}\nD) {row['D']}"

    prompt = f"Question: {question}\n\n{options}\n\nWhich option (A/B/C/D) is correct?"
    first_response = call_together_api(prompt, first_model_name)
    second_response = call_together_api(prompt, second_model_name)

    return [first_response, second_response]

def preference(response_list):
    print(f"**{first_model_name}**\n{response_list[0]}\n\n**{second_model_name}**\n{response_list[1]}\n\n")

    answer = input(f"if you like {first_model_name} answer enter 1\nif you like {second_model_name} answer enter 0\n enter 0.5 otherwise")

    return float(answer)

llm_comparison = ratings(1000, models)

response_list = getAnswers(sample)

select_model = preference(response_list)

def computeElo(first_model_name, second_model_name, select_model, k=32):
    expected_first = 1/(1 + 10** ((llm_comparison.get_rating(first_model_name)-llm_comparison.get_rating(second_model_name))/400))
    expected_second = 1 - expected_first

    new_rating_first = llm_comparison.get_rating(first_model_name) + k * (select_model - expected_first)
    new_rating_second = llm_comparison.get_rating(second_model_name) + k * ((1-select_model) - expected_second)

    llm_comparison.set_rating(first_model_name, new_rating_first)
    llm_comparison.set_rating(second_model_name, new_rating_second)

computeElo(first_model_name, second_model_name, select_model)
