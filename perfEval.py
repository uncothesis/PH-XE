import json
import yaml
import statistics
from scipy.stats import norm

class Evaluate:
    def __init__(self,data: str = "llm_comparison.json"):
        self.data = data
        with open(self.data,'r') as f:
           self.loaded_elo = json.load(f)
        self.models = self.load_models()

    def load_models(self, yaml_path="models.yaml") -> list[dict]:
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
            return data["models"]

    def analyse(self, score: int,desired_type: str="human"):
        filtered_elo = []
        for model in self.models:
            if model['type'] == desired_type and model['name'] in self.loaded_elo:
                filtered_elo.append(self.loaded_elo[model['name']])
        mean = statistics.mean(filtered_elo)
        sd = statistics.stdev(filtered_elo)
        data_list = list(self.loaded_elo.values())

        overall_mean = statistics.mean(data_list)
        overall_sd = statistics.stdev(data_list)

        return [norm.cdf(score , loc=mean, scale = sd)*100, norm.cdf(score, loc=overall_mean, scale = overall_sd)*100]
