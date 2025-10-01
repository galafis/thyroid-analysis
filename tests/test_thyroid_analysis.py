
import unittest
import os
import sys
import pandas as pd
from unittest.mock import patch, MagicMock
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# Adicionar o diretório src ao PATH para que o script possa ser importado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/processing')))

from thyroid_analysis import load_data, preprocess_data, train_model, evaluate_model, save_artifacts, DATA_PATH, MODEL_PATH

class TestThyroidAnalysis(unittest.TestCase):

    def setUp(self):
        # Mock para pd.read_csv
        self.mock_df = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [6, 7, 8, 9, 10],
            'diagnosis': ['negative', 'positive', 'negative', 'positive', 'negative']
        })
        self.patcher_read_csv = patch('pandas.read_csv', return_value=self.mock_df)
        self.mock_read_csv = self.patcher_read_csv.start()

        # Mock para joblib.dump
        self.patcher_joblib_dump = patch('joblib.dump')
        self.mock_joblib_dump = self.patcher_joblib_dump.start()

        # Mock para os.makedirs
        self.patcher_makedirs = patch('os.makedirs')
        self.mock_makedirs = self.patcher_makedirs.start()

        # Mock para os.path.exists para simular a existência do arquivo de dados
        self.patcher_exists = patch('os.path.exists', return_value=True)
        self.mock_exists = self.patcher_exists.start()

    def tearDown(self):
        self.patcher_read_csv.stop()
        self.patcher_joblib_dump.stop()
        self.patcher_makedirs.stop()
        self.patcher_exists.stop()

    def test_load_data(self):
        df = load_data('test_data.csv')
        self.mock_read_csv.assert_called_once_with(os.path.join(DATA_PATH, 'test_data.csv'))
        pd.testing.assert_frame_equal(df, self.mock_df)

    def test_load_data_file_not_found(self):
        self.mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            load_data('non_existent_file.csv')

    def test_preprocess_data(self):
        X_scaled, y, label_encoder, scaler = preprocess_data(self.mock_df.copy())
        self.assertIsInstance(X_scaled, type(self.mock_df.values))
        self.assertIsInstance(y, pd.Series)
        self.assertIsInstance(label_encoder, LabelEncoder)
        self.assertIsInstance(scaler, StandardScaler)
        self.assertEqual(len(y.unique()), 2) # 'negative', 'positive'

    def test_train_model(self):
        X_scaled, y, _, _ = preprocess_data(self.mock_df.copy())
        model = train_model(X_scaled, y)
        self.assertIsInstance(model, RandomForestClassifier)

    def test_evaluate_model(self):
        X_scaled, y, label_encoder, _ = preprocess_data(self.mock_df.copy())
        # Para o propósito do teste unitário, vamos usar um split simples sem stratify para evitar erros com datasets pequenos.
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.4, random_state=42)


        model = train_model(X_train, y_train)
        
        with patch('builtins.print') as mock_print:
            accuracy, precision, recall, f1 = evaluate_model(model, X_test, y_test, label_encoder)
            self.assertIsInstance(accuracy, float)
            self.assertIsInstance(precision, float)
            self.assertIsInstance(recall, float)
            self.assertIsInstance(f1, float)
            mock_print.assert_called()

    def test_save_artifacts(self):
        model = MagicMock(spec=RandomForestClassifier)
        scaler = MagicMock(spec=StandardScaler)
        label_encoder = MagicMock(spec=LabelEncoder)
        
        save_artifacts(model, scaler, label_encoder)
        
        self.mock_makedirs.assert_called_once_with(MODEL_PATH, exist_ok=True)
        self.assertEqual(self.mock_joblib_dump.call_count, 3)
        self.mock_joblib_dump.assert_any_call(model, os.path.join(MODEL_PATH, 'random_forest_model.pkl'))
        self.mock_joblib_dump.assert_any_call(scaler, os.path.join(MODEL_PATH, 'scaler.pkl'))
        self.mock_joblib_dump.assert_any_call(label_encoder, os.path.join(MODEL_PATH, 'label_encoder.pkl'))

if __name__ == '__main__':
    unittest.main()

