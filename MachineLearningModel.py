from tensorflow.keras.layers import LSTM
from tensorflow.keras import layers
from tensorflow import keras
from kerastuner.tuners import Hyperband
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import tensorflow as tf
import mlflow

def create_sequences(data, time_steps, features):
    sequences = []
    target = []

    for i in range(len(data) - time_steps):
        sequences.append(data[i:i + time_steps, :features])
        target.append(data[i + time_steps, -1])

    return np.array(sequences), np.array(target)

def load_data(N_STEPS, N_FEATURES):
    data_file_path = "path_to_your_data.csv"
    raw_data = pd.read_csv(data_file_path)

    processed_data = raw_data.fillna(method='ffill')
    features = processed_data[['feature1', 'feature2', 'feature3', 'feature4']]
    target = processed_data['target']
    data_with_target = features.copy()
    data_with_target['target'] = target

    X, y = create_sequences(data_with_target.values, N_STEPS, N_FEATURES)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, y_train, X_test, y_test

N_STEPS = 50
N_FEATURES = 5

X_train, y_train, X_test, y_test = load_data(N_STEPS, N_FEATURES)

inputs = tf.keras.Input(shape=(N_STEPS, N_FEATURES))
x = LSTM(128, return_sequences=True)(inputs)
x = LSTM(64)(x)
x = layers.Dense(64, activation='relu')(x)
outputs = layers.Dense(1, activation='sigmoid')(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

tuner = Hyperband(model,
                  objective='val_accuracy',
                  max_epochs=30,
                  factor=3,
                  directory='output',
                  project_name='hyperband_tuning')

tuner.search(X_train, y_train, epochs=100, validation_data=(X_test, y_test))

best_model = tuner.get_best_models(1)[0]

mlflow.start_run()
mlflow.log_param('model', best_model.to_json())
mlflow.log_metric('val_accuracy', best_model.evaluate(X_test, y_test)[1])
mlflow.end_run()
