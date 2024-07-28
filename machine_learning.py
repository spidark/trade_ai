import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import logging

def prepare_data(data):
    data = data.dropna()
    X = data[['Open', 'High', 'Low', 'Volume']].values
    y = data['Close'].values
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_regression_model(data):
    logging.info("Training regression model")
    X_train, X_test, y_train, y_test = prepare_data(data)
    model = LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    logging.info(f"Regression model trained with score: {score}")
    return model

def predict_price(model, data):
    X = data[['Open', 'High', 'Low', 'Volume']].values
    predictions = model.predict(X)
    return predictions

def train_clustering_model(data):
    logging.info("Training clustering model")
    X = data[['Open', 'High', 'Low', 'Close', 'Volume']].values
    model = KMeans(n_clusters=3)
    model.fit(X)
    return model

def cluster_data(model, data):
    X = data[['Open', 'High', 'Low', 'Close', 'Volume']].values
    clusters = model.predict(X)
    return clusters
