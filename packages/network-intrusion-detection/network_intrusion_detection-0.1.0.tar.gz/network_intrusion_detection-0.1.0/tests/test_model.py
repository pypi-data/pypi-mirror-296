import unittest
from intrusion_detection.model import load_model, preprocess_data, predict_traffic
import numpy as np

class TestIntrusionDetection(unittest.TestCase):

    def test_load_model(self):
        model = load_model('path/to/valid/model.h5')
        self.assertIsNotNone(model)
    
    def test_preprocess_data(self):
        data = preprocess_data('path/to/valid/data.csv')
        self.assertIsInstance(data, np.ndarray)
    
    def test_predict_traffic(self):
        model = load_model('path/to/valid/model.h5')
        data = preprocess_data('path/to/valid/data.csv')
        predictions = predict_traffic(model, data)
        self.assertEqual(predictions.shape[0], data.shape[0])

if __name__ == "__main__":
    unittest.main()
