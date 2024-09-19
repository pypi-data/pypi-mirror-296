# Intrusion Detection Package

This package provides a CNN-LSTM-based intrusion detection model that can be used to classify network traffic as benign or malicious.

## Installation

You can install the package using pip:

pip install network_intrusion_detection


## Usage

To use the model, follow these steps:

1. Load your pre-trained model (.h5 file).
2. Preprocess your network traffic data (CSV format).
3. Make predictions on the data.

Example:

```python
import network_intrusion_detection
from network_intrusion_detection.model import load_model, preprocess_data, predict_traffic

# Load the pre-trained model
model = load_model('path/to/model.h5')

# Preprocess the data
data = preprocess_data('path/to/network_data.csv')

# Make predictions
predictions = predict_traffic(model, data)

# Output predictions
print(predictions)
