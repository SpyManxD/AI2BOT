# 4MachineLearningModel.py

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from kerastuner import Hyperband

import mlflow

# Configuration
N_STEPS = 50
N_FEATURES = 5

# Load dataset
X_train, y_train, X_test, y_test = load_data()

# Build model
inputs = tf.keras.Input(shape=(N_STEPS, N_FEATURES))
x = LSTM(128, return_sequences=True)(inputs)
x = LSTM(64)(x)
x = layers.Dense(64, activation='relu')(x)
outputs = layers.Dense(1, activation='sigmoid')(x)
model = keras.Model(inputs=inputs, outputs=outputs)

# Compile and train
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

tuner = Hyperband(model, objective='val_accuracy')
tuner.search(X_train, y_train, epochs=100, validation_data=(X_test, y_test))

best_model = tuner.get_best_models(1)[0]

# Track with MLflow
mlflow.log_param('model', best_model.to_json())
mlflow.log_metric('val_accuracy', best_model.evaluate(X_test, y_test)[1])