import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Embedding


#Define the number of epochs
EPOCH_NUM = 1

# Load the dataset from CSV
dataset = pd.read_csv('./data/grutrain.csv', sep=';')

# Encode categorical features
cat_features = ['Port', 'UF', 'Weekday', 'Year', 'Month', 'Day', 'Hour']
label_encoders = {}
for feature in cat_features:
    label_encoders[feature] = LabelEncoder()
    dataset[feature] = label_encoders[feature].fit_transform(dataset[feature])

# Split the dataset into input features and target variable
X = dataset.drop('Queue', axis=1).values
y = dataset['Queue'].values

# Scale numerical features
num_features = ['WaitOp', 'OpTime', 'Queue2']
scaler = MinMaxScaler()
X[:, :3] = scaler.fit_transform(X[:, :3])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape the input data
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Build the GRU model
model = Sequential()
model.add(GRU(64, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=EPOCH_NUM, batch_size=32)

# Save the trained model
model.save('./models/gru_model.h5')

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print('Loss:', loss)


"""
# Predict the queue time for new input data
new_data = np.array([[[10, 24, 2, 'PORTOVELHO', 15, 9, 2023, 10, 'Monday', 'RJ']]])
new_data[:, :7] = scaler.transform(new_data[:, :7])
new_data[:, 3] = label_encoders['Port'].transform(new_data[:, 3])
new_data[:, 3] = label_encoders['Weekday'].transform(new_data[:, 8])
new_data[:, 9] = label_encoders['UF'].transform(new_data[:, 9])
predicted_queue_time = model.predict(new_data)
print('Predicted Queue Time:', predicted_queue_time)
"""
