import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import tensorflow as tf
import joblib

# Load the CSV data into a pandas DataFrame
data = pd.read_csv('./data/train_full_wdnum.csv', sep=';')

data = data[['Queue', 'WaitOp', 'OpTime', 'Queue2', 'Day', 'Month', 'Year', 'Weekday', 'Hour']]

print(data.head(3))

# Split the data into features (X) and target variable (y)
X = data.drop('Queue', axis=1)
y = data['Queue']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the model architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X_train_scaled, y_train, epochs=1, batch_size=32)

# Evaluate the model on the test set
loss = model.evaluate(X_test_scaled, y_test)
print('Mean Squared Error on test set:', loss)

# Save the trained model
model.save('queue_prediction_model.h5')
print('Model saved.')

# Save the scaler
joblib.dump(scaler, 'scaler.pkl')
print('Scaler saved.')


# Load the saved model
loaded_model = tf.keras.models.load_model('queue_prediction_model.h5')
print('Model loaded.')

# Load the scaler
loaded_scaler = joblib.load('scaler.pkl')
print('Scaler loaded.')

# Create a dictionary input for prediction
input_dict = {
    'WaitOp': 0.5,
    'OpTime': 1.2,
    'Queue2': 3.0,
    'Day': 1,
    'Month': 5,
    'Year': 2023,
    'Weekday': 1,
    'Hour': 10,
}

# Scale the input using the loaded scaler
input_scaled = loaded_scaler.transform(pd.DataFrame([input_dict], columns=['WaitOp', 'OpTime', 'Queue2', 'Day', 'Month',
                                                                           'Year', 'Weekday', 'Hour']))

# Predict the Queue value using the loaded model
prediction = loaded_model.predict(input_scaled)[0][0]
print('Predicted Queue value:', prediction)
