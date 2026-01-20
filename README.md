### Treinamento e Validação do modelo

#### Primeiro passos:

Criar e ativar ambiente virtual:

``` python -m venv venv ```

``` .\venv\Scripts\activate ```

Instalar pacotes necessários:

``` pip install -r requirements.txt ```

Realizando treinamento:

O arquivo responsável está na pasta ``` models ```, no arquivo ``` training.py ```

Para executar corretamente é necessário configurar (por enquanto) as seguintes variáveis:

``` symbol='DIS' # representa qual a ação target ```

``` model_name='lstm_v1' # nome para o modelo ```

``` X_train, X_test, y_train, y_test, scaler = get_data(symbol) # prepara os dados da lib yfinance para treinamento ```

``` model, history = train_lstm(X_train, y_train, X_test, y_test) # treina o modelo ```

```model.save(f'model\models\{model_name}.keras') # salva o modelo na pasta models ```

``` joblib.dump(scaler, f'model\models\scaler_{model_name}.pkl') # salva o pickle do modelo ```

``` y_real, y_pred = evaluate_model(model, X_test, y_test, scaler) # resultados com métricas ```

``` plot_learning_curves(history, model_name) # saúde do treinamento ```

``` plot_predictions(y_real, y_pred, model_name) # gráfico das predições com a base de teste ```
