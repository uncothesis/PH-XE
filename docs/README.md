# PH-50E (enhanced)

PH-50E (read PH-50 enhanced) evaluates LLMs and humans through dual modes: a basic accuracy check (5-question sampling with correctness metrics) and an advanced ELO-based evaluation system. The latter incorporates human-expert assessments of reasoning quality in pairwise model comparisons, dynamically updates skill ratings stored in JSON, and calculates percentile rankings relative to participant groups (LLMs/humans) and the full cohort. It combines simple performance tracking with nuanced competitive benchmarking.

---

## Features

(in addition to the ones mentioned in PH-50)
- **Dynamic ELO Rankings:** Models/humans gain skill-based scores updated through competitive comparisons (works similar to chess)
- **Percentile Positioning:** Shows performance relative to specific groups (LLMs/humans) and all participants
- **Rating Storage:** Maintains ratings in `llm_comparison.json` between sessions, auto-initializes new entrants
- **Reasoning-Focused Evaluation:** Humans judge response quality (not just accuracy) via side-by-side comparisons
- **Dual Analysis Mode:** Supports both quick accuracy checks (original 5Q test) and deep ELO-based evaluation
- **Cross-Type Benchmarking:** Compare LLMs against humans, other LLMs or both using unified metrics
---
## File structure

```
PH-50E/
	|- new.py                    # Main benchmarking script (evaluates accuracy and reasoning quality)
	|- test.py                   # to test the code without the API keys
	|- perEval                   # contains the Evaluate class which calculates the percentile for a given score
	|- questions.csv             # Input question dataset
	|- models.yaml               # YAML config with list of model names(also humans) and their types
	|- llm_comparison.json       # stores the model names and their respective ratings 
	|- .env                      # Stores TOGETHER_API_KEY
	|- original_files_by_jordan_taylor/
		|- main.py               # Main benchmarking script
		|- questions.csv         # Input questions dataset (unchanged)  
		|- models.yaml           # YAML config with list of model names
		|- exploratory.py.       # to directly access questions.csv
```

---
## Setup

1. Install dependencies
`pip install pandas python-dotenv tqdm together scipy`

2. Create `.env`
`TOGETHER_API_KEY=your_api_key_here`

3. Add `models.yaml`
```
models:
  - name: meta-llama/Llama-3.3-70B-Instruct-Turbo-Free
    type: llm
  - name: meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8
    type: llm
  - name: deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free
    type: llm
  - name: subject-1
    type: human
```

4. Prepare `questions.csv`
`id,correct_answer,question,A,B,C,D`

---
## Limitations

- **Statistical Assumptions**: Percentile calculations assume perfect normal distribution (gives ballpark estimates rather than exact values)  
- **Manual Model Selection**: Requires manual configuration for pairwise comparisons (no automatic matchmaking, will be improved in the future)  
- **Human Evaluation Bottleneck**: Dependent on manual input for reasoning quality assessment  
- **Cold Start Problem**: Elo ratings require significant comparisons to stabilize  
- **Simplified Scoring**: Basic evaluation only checks for answer substring matches 
- **Dataset Scope**: Limited to ~50 maritime questions (per current implementation)  