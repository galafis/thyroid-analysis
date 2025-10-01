
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Adicionar o diretório src ao PATH para que o script possa ser importado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from update_graph_colors import (
    gerar_grafico_comparacao_algoritmos,
    gerar_grafico_interpretabilidade,
    gerar_grafico_visualizacao_ml,
    PALETA_ALGORITMOS,
    SHAP_COLORS,
    CORES_GERAIS
)

class TestUpdateGraphColors(unittest.TestCase):

    def setUp(self):
        self.output_dir = 'test_output_images'
        os.makedirs(self.output_dir, exist_ok=True)

        # Mock plt.savefig to record calls and simulate file creation
        self.saved_files = []
        def mock_savefig_side_effect(filename, **kwargs):
            full_path = os.path.join(self.output_dir, os.path.basename(filename))
            self.saved_files.append(full_path)
            # Simulate file creation for os.path.exists
            with open(full_path, 'w') as f:
                f.write('mock content')

        self.patcher_savefig = patch('matplotlib.pyplot.savefig', side_effect=mock_savefig_side_effect)
        self.mock_savefig = self.patcher_savefig.start()

    def tearDown(self):
        self.patcher_savefig.stop()
        for f in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, f))
        os.rmdir(self.output_dir)

    def test_gerar_grafico_comparacao_algoritmos(self):
        gerar_grafico_comparacao_algoritmos()
        expected_path = os.path.join(self.output_dir, 'ml_algorithms_comparison_new.png')
        self.assertIn(expected_path, self.saved_files)
        self.assertTrue(os.path.exists(expected_path))

    def test_gerar_grafico_interpretabilidade(self):
        gerar_grafico_interpretabilidade()
        expected_path = os.path.join(self.output_dir, 'model_interpretability_new.png')
        self.assertIn(expected_path, self.saved_files)
        self.assertTrue(os.path.exists(expected_path))

    def test_gerar_grafico_visualizacao_ml(self):
        gerar_grafico_visualizacao_ml()
        expected_path = os.path.join(self.output_dir, 'thyroid_ml_visualization_new.png')
        self.assertIn(expected_path, self.saved_files)
        self.assertTrue(os.path.exists(expected_path))

    def test_palette_definitions(self):
        self.assertIsInstance(PALETA_ALGORITMOS, dict)
        self.assertGreater(len(PALETA_ALGORITMOS), 0)
        self.assertIsInstance(SHAP_COLORS, list)
        self.assertGreater(len(SHAP_COLORS), 0)
        self.assertIsInstance(CORES_GERAIS, list)
        self.assertGreater(len(CORES_GERAIS), 0)

if __name__ == '__main__':
    unittest.main()

