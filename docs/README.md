# PH-50E (enhanced)

A lightweight benchmarking tool for evaluating Large Language Models (LLMs) on maritime domain knowledge. Evaluates basic multiple-choice question accuracy, compares model reasoning capabilities through Elo ratings, and provides statistical performance analysis.


## Features

(in addition to the ones mentioned in PH-50)
- **Dual Evaluation Modes**:  
  - Basic accuracy testing (5-question samples)
  - Reasoning comparison via Elo rating system  
- **Human-in-the-Loop Assessment**: Expert preference evaluation for model-vs-model reasoning outputs  
- **Statistical Analysis**:  
  - Normal distribution-based percentile rankings  
  - Separate scoring for human-aligned vs general model types  
- **Configurable Setup**: Model management through YAML configuration  

PH-50E/
- new.py                    # Main benchmarking script (evaluates accuracy and reasoning quality)
- test.py                   # to test the code without the API keys
- perEval                   # contains the Evaluate class which calculates the percentile for a give score
- questions.csv             # Input question dataset
- models.yaml               # YAML config with list of model names and their types
- llm_comparison.json       # stores the model names and their respective ratings 
- .env                      # Stores TOGETHER_API_KEY


## Limitations

- **Statistical Assumptions**: Percentile calculations assume perfect normal distribution (ballpark estimates rather than exact values)  
- **Manual Model Selection**: Requires manual configuration for pairwise comparisons (no automatic matchmaking)  
- **Human Evaluation Bottleneck**: Dependent on manual input for reasoning quality assessment  
- **Cold Start Problem**: Elo ratings require significant comparisons to stabilize  
- **Simplified Scoring**: Basic evaluation only checks for answer substring matches  
- **Dataset Scope**: Limited to ~50 maritime questions (per current implementation)  

## Usage

1. Configure models in `models.yaml`  
2. Set API key in `.env`  
3. Run main.py for either:  
   - Basic accuracy test (`basicEval()`)  
   - Comparative Elo evaluation  
4. Review results in console and generated JSON files  

