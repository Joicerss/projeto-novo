"""
Unit tests for generate_modelo_respostas.py

Tests the template generation functionality.
"""
import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
import pandas as pd

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_modelo_respostas import generate


class TestGenerateModeloRespostas(unittest.TestCase):
    """Test template generation"""
    
    def setUp(self):
        """Create a temporary directory for test outputs"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)
    
    def test_generate_creates_file(self):
        """Test that generate creates the output file"""
        output_path = os.path.join(self.test_dir, "test_modelo.xlsx")
        generate(output_path)
        self.assertTrue(os.path.exists(output_path))
    
    def test_generate_has_correct_columns(self):
        """Test that generated file has all required columns"""
        output_path = os.path.join(self.test_dir, "test_modelo.xlsx")
        generate(output_path)
        
        df = pd.read_excel(output_path)
        expected_cols = [
            "numero_processo",
            "pergunta_1",
            "pergunta_2",
            "pergunta_3",
            "pergunta_4",
            "pergunta_5",
            "pergunta_6",
            "pergunta_7",
            "pergunta_8",
            "pergunta_9",
            "pergunta_10",
            "pergunta_11",
            "pergunta_12",
            "pergunta_13",
            "pergunta_14",
            "evidencias"
        ]
        self.assertEqual(list(df.columns), expected_cols)
    
    def test_generate_empty_dataframe(self):
        """Test that generated file contains no rows"""
        output_path = os.path.join(self.test_dir, "test_modelo.xlsx")
        generate(output_path)
        
        df = pd.read_excel(output_path)
        self.assertEqual(len(df), 0)
    
    def test_generate_creates_parent_directory(self):
        """Test that generate creates parent directory if it doesn't exist"""
        nested_path = os.path.join(self.test_dir, "nested", "dir", "test_modelo.xlsx")
        generate(nested_path)
        self.assertTrue(os.path.exists(nested_path))


if __name__ == '__main__':
    unittest.main()
