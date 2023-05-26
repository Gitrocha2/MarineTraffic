import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from tensorflow.keras.models import load_model

# Load the saved model
loaded_model = load_model('./models/gru_model.h5')

print("Model loaded successfully!")

# Load new data for prediction
new_data = np.array([[10, 24, 2, 'PORTOVELHO', 'RJ', 15, 9, '2023', 'Wednesday', 10]])
scaler = MinMaxScaler()
label_encoders = {}

# Perform necessary transformations on new data
num_features = ['WaitOp', 'OpTime', 'Queue2', 'Day', 'Month', 'Hour']
new_data[:, :6] = scaler.fit_transform(new_data[:, :6])

# Encode categorical features
cat_features = ['Port', 'UF', 'Weekday']
for feature in cat_features:
    label_encoders[feature] = LabelEncoder()
    new_data[:, cat_features.index(feature)] = label_encoders[feature].fit_transform(new_data[:, cat_features.index(feature)])

# Ordinal Encode numerical feature "Year"
label_encoders['Year'] = LabelEncoder()
new_data[:, cat_features.index('Year')] = label_encoders['Year'].transform(new_data[:, cat_features.index('Year')])

# Predict the queue time using the loaded model
predicted_queue_time = loaded_model.predict(new_data)
print('Predicted Queue Time:', predicted_queue_time)