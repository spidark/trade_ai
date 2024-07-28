import logging
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, silhouette_score
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

def train_random_forest_model(data, target_column):
    logging.info("Training Random Forest model")
    try:
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        logging.info(f"Random Forest model trained with MSE: {mse}")
        return model, mse, X_test, y_test, y_pred
    except Exception as e:
        logging.error(f"Error training Random Forest model: {e}")
        return None, None, None, None, None

def train_regression_model(data, target_column):
    logging.info("Training regression model")
    try:
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        logging.info(f"Regression model trained with MSE: {mse}")
        return model, mse, X_test, y_test, y_pred
    except Exception as e:
        logging.error(f"Error training regression model: {e}")
        return None, None, None, None, None

def predict_price(model, data):
    logging.info("Predicting prices")
    try:
        predictions = model.predict(data)
        logging.info(f"Predictions: {predictions}")
        return predictions
    except Exception as e:
        logging.error(f"Error predicting prices: {e}")
        return None

def train_clustering_model(data, n_clusters):
    logging.info("Training clustering model")
    try:
        model = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = model.fit_predict(data)
        silhouette_avg = silhouette_score(data, clusters)
        logging.info(f"Clustering model trained with silhouette score: {silhouette_avg}")
        return model, silhouette_avg, clusters
    except Exception as e:
        logging.error(f"Error training clustering model: {e}")
        return None, None, None

def cluster_data(model, data):
    logging.info("Clustering data")
    try:
        clusters = model.predict(data)
        logging.info(f"Data clustered into: {clusters}")
        return clusters
    except Exception as e:
        logging.error(f"Error clustering data: {e}")
        return None

def plot_regression_results(X_test, y_test, y_pred, output_dir):
    plt.figure(figsize=(10, 6))
    plt.scatter(X_test.index, y_test, color='blue', label='Actual')
    plt.scatter(X_test.index, y_pred, color='red', label='Predicted')
    plt.xlabel('Index')
    plt.ylabel('Price')
    plt.title('Regression Model Results')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'regression_results.png'))
    plt.close()

def plot_clustering_results(data, clusters, output_dir):
    plt.figure(figsize=(10, 6))
    plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=clusters, cmap='viridis', marker='o')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Clustering Results')
    plt.savefig(os.path.join(output_dir, 'clustering_results.png'))
    plt.close()
