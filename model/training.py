import yfinance as yf
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
from evaluate import evaluate_model, plot_learning_curves, plot_predictions
from datetime import datetime, timedelta

now = datetime.now()
days_ago = now - timedelta(days=120) # range de dias para treinamento do modelo
start_date = days_ago.strftime('%Y-%m-%d')
end_date = now.strftime('%Y-%m-%d')

def get_data(symbol, window_size=30):
    df = yf.download(symbol, start=start_date, end=end_date, progress=False)
    df = df.dropna()
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    features_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    data_features = df[features_cols].values
    data_target = df[['Close']].values
    
    scaler_features = MinMaxScaler(feature_range=(0, 1))
    scaled_features = scaler_features.fit_transform(data_features)
    
    scaler_target = MinMaxScaler(feature_range=(0, 1))
    scaled_target = scaler_target.fit_transform(data_target)
    
    X, y = [], []
    for i in range(window_size, len(scaled_features)):
        X.append(scaled_features[i-window_size:i, :])
        y.append(scaled_target[i, 0])
    
    X, y = np.array(X), np.array(y)
    
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    return X_train, X_test, y_train, y_test, scaler_target

def train_lstm(X_train, y_train, X_test, y_test):
    model = Sequential([
        LSTM(units=100, return_sequences=True, 
             input_shape=(X_train.shape[1], X_train.shape[2])),
        Dropout(0.2),
        
        LSTM(units=100, return_sequences=False),
        Dropout(0.2),
        
        Dense(units=1)
    ])

    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='mean_squared_error')

    # caso a curva de loss estabilize, encerra o treinamento para evitar overfitting
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[early_stop],
        verbose=1
    )
    
    return model, history

symbol='DIS'
model_name='lstm_v1'
X_train, X_test, y_train, y_test, scaler = get_data(symbol)
model, history = train_lstm(X_train, y_train, X_test, y_test)
model.save(f'model\models\{model_name}.keras')
joblib.dump(scaler, f'model\models\scaler_{model_name}.pkl')
y_real, y_pred = evaluate_model(model, X_test, y_test, scaler)
plot_learning_curves(history, model_name)
plot_predictions(y_real, y_pred, model_name)
