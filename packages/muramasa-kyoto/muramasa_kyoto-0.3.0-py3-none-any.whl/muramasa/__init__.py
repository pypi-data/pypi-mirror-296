from .feature_extraction import extract_features, create_feature_file
from .anomaly_detection import AnomalyDetector
from .utils import load_data, preprocess_data
import os

__all__ = ['extract_features', 'create_feature_file', 'AnomalyDetector', 'load_data', 'preprocess_data']

__version__ = '0.3.0'

# Load the pre-trained model
model_path = os.path.join(os.path.dirname(__file__), 'trained_model.joblib')
pre_trained_model = AnomalyDetector.load_model(model_path)