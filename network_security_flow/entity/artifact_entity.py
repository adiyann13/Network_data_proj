from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    training_file_path:str
    testing_file_path:str

@dataclass
class DataValidationAtrtifacts:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_path:str
    invalid_test_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass
class ClassificationMetricsArtifacts:
    f1_score:float
    precision:float
    recall:float

@dataclass
class ModelTrainerArtifcats:
    trained_model_file_path:str
    train_metric_artifact: ClassificationMetricsArtifacts
    test_metric_artifact: ClassificationMetricsArtifacts
