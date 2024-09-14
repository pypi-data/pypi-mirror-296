# Muramasa

Muramasa is a Python package for detecting anomalies in plasmid DNA sequences using K-means clustering and Mahalanobis distance.

## Installation

You can install Muramasa using pip:
pip install muramasa

## Usage

Here's a basic example of how to use Muramasa:

```python
from muramasa import feature_extraction, anomaly_detection

# Extract features from your plasmid sequences
feature_extraction.create_feature_file('input.csv', 'features.csv')

# Load the features
features = pd.read_csv('features.csv')

# Create and train the anomaly detector
detector = anomaly_detection.AnomalyDetector()
detector.fit(features)

# Predict anomalies
predictions = detector.predict(features)

# Get feature contributions for anomalies
contributions = detector.get_feature_contributions(features[predictions['is_anomaly']])