import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
import warnings
warnings.filterwarnings('ignore')
from statsmodels.tsa.stattools import adfuller
import pmdarima as pm
from pmdarima import auto_arima
import statsmodels.api as sm
from datetime import datetime
import requests
import json
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


#Appd Configuration and parsing the data
def appD(appUrl,auth):
    try:
        url=appUrl+ "525600&output=json&rollup=false"
        headers = {'Authorization': 'Basic '+auth}
        r = requests.get(url,headers=headers,verify=false)
        y = json.dumps(json.loads(r.text)[0])
        str = json.loads(y)
        json_array  = str["metricValues"]
        df=pd.DataFrame(json_array)
        df['Date']=pd.to_datetime(df['startTimeInMillis'],unit='ms').dt.date
        return predict_forecast(df)
    except:
            return pd.DataFrame()
#forecasting by applying the model

# Load data
def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['Date'], index_col='Date')
    # df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
    return df

# Preprocessing
def preprocess_data(df):
    df = df.fillna(method='ffill')
    return df

def detect_data_length(df):
   # Detect if the data is less than one year or more
   # df.reset_index(inplace=True)
   # df.rename(columns={'index': 'ds', 'Value': 'y'}, inplace=True)
   df['Date'] = pd.to_datetime(df['Date'])
   data_length = (df['Date'].max() - df['Date'].min()).days
   return data_length < 364

# Split data into train and test
def train_test_split_data(df, test_size=0.2):
    train_size = int(len(df) * (1 - test_size))
    train, test = df[:train_size], df[train_size:]
    return train, test

# Dynamic ARIMA model using auto_arima
def arima_forecast(train, test):
    model = auto_arima(train, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True)
    model_fit = model.fit(train)
    predictions = model_fit.predict(n_periods=len(test))
    return predictions, model

# Dynamic SARIMA model using auto_arima for seasonal order
def sarima_forecast(train, test):
    model = auto_arima(train, seasonal=True, m=12, trace=True, error_action='ignore', suppress_warnings=True)
    model_fit = SARIMAX(train, order=model.order, seasonal_order=model.seasonal_order).fit()
    predictions = model_fit.forecast(steps=len(test))
    return predictions, model

# Prophet model
def prophet_forecast(train, test,yearly_seasonality=False):
    # train.reset_index(inplace=True)
    train = train.reset_index().rename(columns={'Date': 'ds', 'Value': 'y'})
    # train.columns = ['ds', 'y']
    model = Prophet(weekly_seasonality=True, yearly_seasonality=yearly_seasonality)
    model.fit(train)
    future = model.make_future_dataframe(periods=len(test))
    forecast = model.predict(future)
    return forecast['yhat'][-len(test):]

# Random Forest model
def random_forest_forecast(train, test):
    X_train = np.array(range(len(train))).reshape(-1, 1)
    y_train = train.values
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)

    X_test = np.array(range(len(train), len(train) + len(test))).reshape(-1, 1)
    predictions = model.predict(X_test)
    return predictions

# Calculate error
def calculate_error(test, predictions):
    return np.sqrt(mean_squared_error(test, predictions))

# Model Selection
def select_best_model(train, test,yearly_seasonality):
    try:
        models = ['ARIMA', 'SARIMA', 'Prophet', 'RandomForest']
        errors = {}

        # ARIMA
        arima_preds, arima_model = arima_forecast(train, test)
        errors['ARIMA'] = calculate_error(test, arima_preds)

         # Prophet
        prophet_preds = prophet_forecast(train, test,yearly_seasonality)
        errors['Prophet'] = calculate_error(test, prophet_preds)

        # SARIMA
        sarima_preds, sarima_model = sarima_forecast(train, test)
        errors['SARIMA'] = calculate_error(test, sarima_preds)


        # # Random Forest
        rf_preds = random_forest_forecast(train, test)
        errors['RandomForest'] = calculate_error(test, rf_preds)

        # Select the best model
        best_model = min(errors, key=errors.get)

        # Return the models and their auto_arima results
        return best_model, errors, arima_model, sarima_model
    except:
        return{'something went wrong'}

# Forecast for 1 year reusing the ARIMA and SARIMA orders
def forecast_next_year(df, best_model, arima_model, sarima_model, period,yearly_seasonality):
    try:
        if best_model == 'ARIMA':
            # Reuse ARIMA order
            model = auto_arima(df, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True, d=1, max_p=5, max_q=5)
            model_fit = model.fit(df)
            predictions = arima_model.predict(n_periods=period)

        elif best_model == 'SARIMA':
            # Reuse SARIMA order
            model_fit = SARIMAX(df, order=sarima_model.order, seasonal_order=sarima_model.seasonal_order).fit()
            predictions = model_fit.forecast(steps=period)

        elif best_model == 'Prophet':
            # df = pd.read_csv('/Users/546131/Downloads/sample3.csv', parse_dates=['Date'], index_col='Date')
            df = df.reset_index().rename(columns={'Date': 'ds', 'Value': 'y'})
            # model = Prophet()
            # model.fit(df)
            # future = model.make_future_dataframe(periods=365)
            # forecast = model.predict(future)
            # predictions = forecast['yhat'][-365:]
            model = Prophet(weekly_seasonality=True, yearly_seasonality=yearly_seasonality)
            model.fit(df)
            future = model.make_future_dataframe(periods=period)
            forecast = model.predict(future)
            # predictions = forecast[['ds', 'yhat']].tail(period)
            predictions = forecast['yhat'][-period:]

        elif best_model == 'RandomForest':
            X = np.array(range(len(df))).reshape(-1, 1)
            y = df.values
            model = RandomForestRegressor(n_estimators=100)
            model.fit(X, y)

            X_next = np.array(range(len(df), len(df) + period)).reshape(-1, 1)
            predictions = model.predict(X_next)

        return predictions
    except:
        return{'something went wrong'}
# Main function
def predict_forecast(filepath):
    try:
        # Load and preprocess data
        df = load_data(filepath)
        dp = pd.read_csv(filepath)
        dp['Date'] = pd.to_datetime(dp['Date'])
        data_length = (dp['Date'].max() - dp['Date'].min()).days
        # is_less_than_a_year = False
        df = preprocess_data(df)

        # Split into train and test
        train, test = train_test_split_data(df)

        # print(data_length)
        if data_length < 363:
            print('Less than 1 year data')
            best_model, errors, arima_model, sarima_model = select_best_model(train, test,yearly_seasonality=False)
        else:
            print('greater than 1 year data')
            best_model, errors, arima_model, sarima_model = select_best_model(train, test,yearly_seasonality=True)

        # Select the best model and get ARIMA/SARIMA models
        # best_model, errors, arima_model, sarima_model = select_best_model(train, test)
        print(f"Best model: {best_model}")
        print(f"Errors: {errors}")

        # # Plot historical data
        # plt.figure(figsize=(10, 6))
        # plt.plot(df.index, df.values, label='Historical Data')
        # plt.title('Historical Data')
        # plt.legend()
        # plt.show()

        # Forecast for the next year using the same ARIMA/SARIMA order
        if data_length < 363:
            # print('Less than 1 year data')
            forecast = forecast_next_year(df, best_model, arima_model, sarima_model,period=30,yearly_seasonality=False)
        else:
            forecast = forecast_next_year(df, best_model, arima_model, sarima_model,period=30,yearly_seasonality=True)

        max_value = forecast.max()
        mean_value = forecast.mean()
        print(f"Max value in the next 30 days: {max_value}")
        print(f"Mean value for the next 30 days: {mean_value}")

            # Ensure the index of the dataframe is of type DatetimeIndex
        df.index = pd.to_datetime(df.index, dayfirst=True)

        # Plot the forecast
        plt.figure(figsize=(10, 6))

        # Generate proper forecast dates starting from the day after the last date in df
        forecast_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=30, freq='D')

        # Plot historical data
        plt.plot(df.index, df.values, label='Historical Data')

        # Plot forecast data
        plt.plot(forecast_dates, forecast, label='Forecast', color='orange')

        plt.legend()
        plt.show()
        return {'Predicted Peak' : mean_value, 'Predicted Steady' : max_value}
    except:
        return{'something went wrong'}


