import logging
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, silhouette_score
from sklearn.ensemble import RandomForestRegressor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Configuration de la journalisation
logging.basicConfig(filename='trade.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# Modèle de régression linéaire
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

# Modèle de forêt aléatoire
def train_random_forest_model(data, target_column):
    logging.info("Training random forest model")
    try:
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        logging.info(f"Random forest model trained with MSE: {mse}")
        return model, mse, X_test, y_test, y_pred
    except Exception as e:
        logging.error(f"Error training random forest model: {e}")
        return None, None, None, None, None

# Prédiction des prix
def predict_price(model, data):
    logging.info("Predicting prices")
    try:
        predictions = model.predict(data)
        logging.info(f"Predictions: {predictions}")
        return predictions
    except Exception as e:
        logging.error(f"Error predicting prices: {e}")
        return None

# Modèle de clustering
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

# Clustering des données
def cluster_data(model, data):
    logging.info("Clustering data")
    try:
        clusters = model.predict(data)
        logging.info(f"Data clustered into: {clusters}")
        return clusters
    except Exception as e:
        logging.error(f"Error clustering data: {e}")
        return None

# Visualisation des résultats de la régression
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

# Visualisation des résultats de clustering
def plot_clustering_results(data, clusters, output_dir):
    plt.figure(figsize=(10, 6))
    plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=clusters, cmap='viridis', marker='o')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Clustering Results')
    plt.savefig(os.path.join(output_dir, 'clustering_results.png'))
    plt.close()

# Analyse des sentiments
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)['compound']
    return sentiment_score

# Ajout des indicateurs techniques
def add_technical_indicators(data):
    data['SMA'] = data['Close'].rolling(window=20).mean()
    data['EMA'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['RSI'] = calculate_rsi(data['Close'])
    data['Upper_BB'], data['Lower_BB'] = calculate_bollinger_bands(data['Close'])
    data = add_multitemp_indicators(data)
    return data

def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(close, window=20):
    sma = close.rolling(window).mean()
    std = close.rolling(window).std()
    upper_bb = sma + (std * 2)
    lower_bb = sma - (std * 2)
    return upper_bb, lower_bb

def add_multitemp_indicators(data):
    windows = [5, 10, 20]  # Short, medium, long term windows
    for window in windows:
        data[f'SMA_{window}'] = calculate_moving_average(data, window)
        data[f'RSI_{window}'] = calculate_rsi(data['Close'], window)
    return data

def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemples de données
    data = pd.DataFrame({
        'Close': [150, 152, 153, 155, 154, 156],
        'Volume': [1000, 1100, 1200, 1300, 1400, 1500],
        'News': [
            "Company reports record profits!",
            "New product launch successful",
            "Market reacts to positive earnings",
            "Company stock rises",
            "Analysts upgrade stock rating",
            "Strong quarterly performance"
        ]
    })

    # Ajout des indicateurs techniques
    data = add_technical_indicators(data)
    data = add_multitemp_indicators(data)

    # Analyse des sentiments
    data['Sentiment'] = data['News'].apply(analyze_sentiment)

    # Entraînement des modèles
    target_column = 'Close'
    reg_model, reg_mse, X_test, y_test, y_pred = train_regression_model(data, target_column)
    rf_model, rf_mse, X_test, y_test, y_pred = train_random_forest_model(data, target_column)

    # Visualisation des résultats
    output_dir = "plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    plot_regression_results(X_test, y_test, y_pred, output_dir)

    # Clustering
    clustering_data = data[['Close', 'Volume']]
    cluster_model, silhouette_avg, clusters = train_clustering_model(clustering_data, n_clusters=3)
    plot_clustering_results(clustering_data, clusters, output_dir)
    
    print("Script completed successfully")
