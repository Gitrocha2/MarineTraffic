import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

# Load the CSV data
data = pd.read_csv('./data/TF_train_full.csv', sep=';')

# Split the data into features (X) and target variable (y)
X = data.drop('Queue', axis=1)
y = data['Queue']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the numerical features using StandardScaler
numeric_features = ['WaitOp', 'OpTime', 'Queue2', 'Day', 'Month', 'Year', 'Hour']
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[numeric_features])
X_test_scaled = scaler.transform(X_test[numeric_features])

# Encode the text column "UF" using LabelEncoder
label_encoder = LabelEncoder()
X_train_encoded = X_train['UF'].astype(str)
X_test_encoded = X_test['UF'].astype(str)
label_encoder.fit(X_train_encoded)
X_train_encoded = label_encoder.transform(X_train_encoded)
X_test_encoded = label_encoder.transform(X_test_encoded)

# Concatenate the scaled numerical features and encoded "UF" column
X_train_final = tf.keras.utils.normalize(tf.concat([X_train_scaled, X_train_encoded.reshape(-1, 1)], axis=1))
X_test_final = tf.keras.utils.normalize(tf.concat([X_test_scaled, X_test_encoded.reshape(-1, 1)], axis=1))

# Define the model architecture
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train_final.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X_train_final, y_train, epochs=1, batch_size=32)

# Evaluate the model on the test set
loss = model.evaluate(X_test_final, y_test)
print('Mean Squared Error on test set:', loss)

# Save the trained model
model.save('queue_prediction_model2.h5')
print('Model saved.')

# Save the scalers
joblib.dump(scaler, 'scaler2.pkl')
joblib.dump(label_encoder, 'label_encoder2.pkl')
print('Scalers saved.')

# Load the saved model
loaded_model = tf.keras.models.load_model('queue_prediction_model2.h5')
print('Model loaded.')

# Load the scalers
loaded_scaler = joblib.load('scaler2.pkl')
loaded_label_encoder = joblib.load('label_encoder2.pkl')
print('Scalers loaded.')

# Create a dictionary input for prediction
input_dict = {
    'WaitOp': 0.5,
    'OpTime': 1.2,
    'Queue2': 3.0,
    'Day': 1,
    'Month': 5,
    'Year': 2023,
    'Hour': 10,
    'UF': 'RJ'  # Provide the actual text value here
}

# Scale the numerical features using the loaded scaler
input_scaled = loaded_scaler.transform(pd.DataFrame([input_dict], columns=numeric_features))

# Encode the "UF" column using the loaded label encoder
input_encoded = loaded_label_encoder.transform([input_dict['UF']])

# Concatenate the scaled numerical features and encoded "UF" column
input_final = tf.keras.utils.normalize(tf.concat([input_scaled, input_encoded.reshape(-1, 1)], axis=1))

# Predict the Queue value using the loaded model
prediction = loaded_model.predict(input_final)[0][0]
print('Predicted Queue value:', prediction)
