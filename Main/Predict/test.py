import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import GRU, Dense
from keras.optimizers import Adam

# Load the CSV dataset
dataset = pd.read_csv('.AIDatabase/queue_data.csv')

# Extract relevant columns
X = dataset[['Operationtime', 'Port', 'ArrivalDate', 'OperationType', 'State']]
y = dataset['QueueTime']

# Encode categorical features
encoder = LabelEncoder()
X['Port'] = encoder.fit_transform(X['Port'])
X['OperationType'] = encoder.fit_transform(X['OperationType'])
X['State'] = encoder.fit_transform(X['State'])

# Scale numerical features
scaler = MinMaxScaler()
X['Operationtime'] = scaler.fit_transform(X['Operationtime'].values.reshape(-1, 1))
X['ArrivalDate'] = scaler.fit_transform(X['ArrivalDate'].values.reshape(-1, 1))

# Define the GRU model
model = Sequential()
model.add(GRU(units=64, input_shape=(1, X.shape[1])))
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer=Adam(), loss='mean_squared_error')

# Train the model
model.fit(X.values.reshape((X.shape[0], 1, X.shape[1])), y, epochs=50, batch_size=32, verbose=1)

# Save the trained model
model.save('queue_time_model.h5')

# Load the saved model
loaded_model = load_model('queue_time_model.h5')

# Example future time data
future_time = pd.DataFrame({
    'Operationtime': [10],  # Replace with the operation time for the future time
    'Port': ['PortA'],  # Replace with the port for the future time
    'ArrivalDate': ['2023-06-01'],  # Replace with the arrival date for the future time
    'OperationType': ['TypeA'],  # Replace with the operation type for the future time
    'State': ['StateX']  # Replace with the state for the future time
})

# Preprocess the future time data
future_time['Port'] = encoder.transform(future_time['Port'])
future_time['OperationType'] = encoder.transform(future_time['OperationType'])
future_time['State'] = encoder.transform(future_time['State'])
future_time['Operationtime'] = scaler.transform(future_time['Operationtime'].values.reshape(-1, 1))
future_time['ArrivalDate'] = scaler.transform(future_time['ArrivalDate'].values.reshape(-1, 1))

# Reshape the input data for GRU (samples, timesteps, features)
future_time = np.reshape(future_time.values, (future_time.shape[0], 1, future_time.shape[1]))

# Make prediction for the future time using the loaded model
prediction = loaded_model.predict(future_time)

# Perform any additional processing or analysis with the prediction
print(f'Predicted Queue Time: {prediction[0][0]}')