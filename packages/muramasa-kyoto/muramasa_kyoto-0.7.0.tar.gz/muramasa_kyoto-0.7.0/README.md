# Muramasa Kyoto

Muramasa Kyoto is a Python package for detecting anomalies in plasmid DNA sequences using K-means clustering and Mahalanobis distance.

## Installation

You can install Muramasa Kyoto using pip:pip install muramasa_kyoto

## Usage

Here's a basic example of how to use Muramasa Kyoto:

```python
from muramasa_kyoto import feature_extraction, anomaly_detection

# Extract features from your plasmid sequences
feature_extraction.create_feature_file('input.csv', 'features.csv')

# Load the features
import pandas as pd
features = pd.read_csv('features.csv')

# Create and train the anomaly detector
detector = anomaly_detection.AnomalyDetector()
detector.fit(features)

# Predict anomalies
predictions = detector.predict(features)

# Get feature contributions for anomalies
contributions = detector.get_feature_contributions(features[predictions['is_anomaly']])