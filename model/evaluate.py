import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.metrics import mean_absolute_error, mean_squared_error

# saúde do treinamento
def plot_learning_curves(history, model_name):
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Erro no Treino (Loss)')
    plt.plot(history.history['val_loss'], label='Erro na Validação (Val Loss)')
    plt.title('Curvas de Aprendizado (Saúde do Treinamento)')
    plt.xlabel('Épocas')
    plt.ylabel('Erro (MSE)')
    plt.legend()
    plt.grid(True)
    path = f'model\images\learning_curve_{model_name}.png'
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()

def evaluate_model(model, X_test, y_test, scaler):
    # Realizar previsões
    predictions = model.predict(X_test)
    
    # Inverter a escala (voltar para preço em R$)
    # y_test e predictions precisam estar em formato 2D para o scaler
    y_test_real = scaler.inverse_transform(y_test.reshape(-1, 1))
    predictions_real = scaler.inverse_transform(predictions)
    
    # Cálculo das métricas
    mae = mean_absolute_error(y_test_real, predictions_real)
    mse = mean_squared_error(y_test_real, predictions_real)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_test_real - predictions_real) / y_test_real)) * 100

    print(f"Resultados: ")
    print(f"MAE (Erro Médio Absoluto):  R$ {mae:.2f}")
    print(f"RMSE (Raiz do Erro Quadrático Médio): R$ {rmse:.2f}")
    print(f"MAPE (Erro Percentual Médio): {mape:.2f}%")
    
    return y_test_real, predictions_real

# y_real, y_pred = evaluate_model(model, X_test, y_test, scaler)

def plot_predictions(y_real, y_pred, model_name):
    plt.figure(figsize=(12, 6))
    plt.plot(y_real, color='blue', label='Preço Real')
    plt.plot(y_pred, color='red', label='Previsão do modelo')
    plt.title('Preço Real vs Previsão do Modelo')
    plt.xlabel('Tempo (Dias)')
    plt.ylabel('Preço da Ação (R$)')
    plt.legend()
    plt.grid(True)
    path = os.path.join(f'model\images\predictions_{model_name}.png')
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()

# plot_predictions(y_real, y_pred)