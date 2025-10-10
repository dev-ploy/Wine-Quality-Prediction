# from mlProject.entity.config_entity import ModelTrainerConfig
from mlProject.components.model_trainer import ModelTrainer
from mlProject.config.configuration import ConfigurationManager

STAGE_NAME="Model Trainer Stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass
    def main(self):
        config=ConfigurationManager()
        model_trainer_config=config.get_model_trainer_config()
        model_trainer=ModelTrainer(config=model_trainer_config)
        model_trainer.train()