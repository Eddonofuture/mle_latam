from sklearn.utils import resample
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
import mlflow
import numpy as np
from aux import temporada_alta, dif_min, get_periodo_dia
mlflow.sklearn.autolog()


df = pd.read_csv('dataset_SCL.csv')

# Transformaciones
df['temporada_alta'] = df['Fecha-I'].apply(temporada_alta)
df['temporada_alta'].value_counts()
df['dif_min'] = df.apply(dif_min, axis=1)
df['atraso_15'] = np.where(df['dif_min'] > 15, 1, 0)
df['periodo_dia'] = df['Fecha-I'].apply(get_periodo_dia)


data = shuffle(df[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM',
                   'atraso_15']], random_state=111)


data_no_retraso = data[data['atraso_15'] == 0]
data_atraso = data[data['atraso_15'] == 1]

data_atraso_upsampled = resample(data_atraso,
                                 replace=True,
                                 n_samples=55592,  # Equilibrio del 50% en predicciones
                                 random_state=42)

data_upsampled = pd.concat([data_no_retraso, data_atraso_upsampled])

features_upsampled = pd.concat([pd.get_dummies(data_upsampled['OPERA'], prefix='OPERA'), pd.get_dummies(
    data_upsampled['TIPOVUELO'], prefix='TIPOVUELO'), pd.get_dummies(data_upsampled['MES'], prefix='MES')], axis=1)
label_upsampled = data_upsampled['atraso_15']

x_upsampled_train, x_upsampled_test, y_upsampled_train, y_upsampled_test = train_test_split(
    features_upsampled, label_upsampled, test_size=0.8, random_state=42)

modelxgb = xgb.XGBClassifier(nthread=4, seed=42)
parameters = {
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [10, 50, 100, 150, 200],
    'subsample': [0.5, 0.9],
    'max_depth': [6, 8, 10]
}

grid_search = GridSearchCV(modelxgb, param_grid=parameters, scoring='roc_auc',
                           cv=10, n_jobs=-10, verbose=1).fit(x_upsampled_train, y_upsampled_train)
y_predxgb_grid = grid_search.predict(x_upsampled_test)

#y_upsampled_predxgb = modelxgb.predict(x_upsampled_test)
mlflow.log_params("report", classification_report(
    y_upsampled_test, x_upsampled_test))
print(classification_report(y_upsampled_test, y_predxgb_grid))
