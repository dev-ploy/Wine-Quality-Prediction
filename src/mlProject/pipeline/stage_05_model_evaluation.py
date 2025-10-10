from mlProject.config.configuration import ConfigurationManager
from mlProject.components.model_evaluation import ModelEvaluation
from mlProject import logger
STAGET_NAME="Model Evaluation stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass
    def main(self):
            config=ConfigurationManager()
            model_evaluation_config=config.get_model_evaluation_config()
            model_evaluation=ModelEvaluation(config=model_evaluation_config)
            model_evaluation.save_results()