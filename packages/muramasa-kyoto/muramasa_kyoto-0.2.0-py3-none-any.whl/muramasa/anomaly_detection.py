import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from scipy.spatial.distance import mahalanobis

class AnomalyDetector:
    def __init__(self, n_clusters=7, random_state=0):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = None
        self.centers = None
        self.covs = None
        self.threshold = 4.1476920323417  # Fixed threshold as per requirement

    def fit(self, X):
        """
        Fit the anomaly detector to the data.
        
        Args:
        X (pd.DataFrame): Training data
        """
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state, n_init=10).fit(X)
        self.centers = self.kmeans.cluster_centers_

        # Calculate covariance matrices for each cluster
        self.covs = []
        for i in range(self.n_clusters):
            cluster_data = X[self.kmeans.labels_ == i]
            cov = np.cov(cluster_data.T, bias=True)
            cov += np.eye(cov.shape[0]) * 1e-6  # Add small regularization
            self.covs.append(cov)

    def calculate_anomaly_score(self, X):
        """
        Calculate anomaly scores for data points.
        
        Args:
        X (pd.DataFrame): Data to calculate anomaly scores for
        
        Returns:
        np.array: Anomaly scores
        """
        labels = self.kmeans.predict(X)
        scores = []
        for i, x in enumerate(X.values):
            label = labels[i]
            score = mahalanobis(x, self.centers[label], np.linalg.inv(self.covs[label]))
            scores.append(score)
        return np.array(scores)

    def predict(self, X):
        """
        Predict anomalies in the data.
        
        Args:
        X (pd.DataFrame): Data to predict anomalies for
        
        Returns:
        pd.DataFrame: Predictions with anomaly scores and labels
        """
        scores = self.calculate_anomaly_score(X)
        predictions = pd.DataFrame({
            'anomaly_score': scores,
            'is_anomaly': scores > self.threshold
        })
        return predictions

    def get_feature_contributions(self, X):
        """
        Calculate feature contributions to anomaly scores.
        
        Args:
        X (pd.DataFrame): Data to calculate feature contributions for
        
        Returns:
        pd.DataFrame: Feature contributions
        """
        labels = self.kmeans.predict(X)
        contributions = []
        for i, x in enumerate(X.values):
            label = labels[i]
            diff = x - self.centers[label]
            inv_cov = np.linalg.inv(self.covs[label])
            contrib = np.abs(np.dot(inv_cov, diff.T).T * diff)
            contributions.append(contrib)
        return pd.DataFrame(contributions, columns=X.columns)