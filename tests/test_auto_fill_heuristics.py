"""
Unit tests for auto_fill_pilot_advanced.py heuristics.

Tests cover:
- Regex patterns (CNPJ, CPF, dates, years, monetary values)
- Keyword detection functions
- Scoring functions
- Main fill_advanced function
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.auto_fill_pilot_advanced import (
    RE_CNPJ, RE_CPF, RE_DATE, RE_YEAR, RE_VALOR,
    extract_first, contains_any, score_matches, fill_advanced,
    KEYS_SENTENCA, KEYS_INDEMN, KEYS_ACIDENTE, KEYS_VITIMA, KEYS_EXEC
)


class TestRegexPatterns(unittest.TestCase):
    """Test regex pattern matching for various document formats"""
    
    def test_cnpj_formatted(self):
        """Test CNPJ detection with formatting"""
        text = "CNPJ: 12.345.678/0001-90"
        match = RE_CNPJ.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), "12.345.678/0001-90")
    
    def test_cnpj_unformatted(self):
        """Test CNPJ detection without formatting"""
        text = "CNPJ: 12345678000190"
        match = RE_CNPJ.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), "12345678000190")
    
    def test_cpf_formatted(self):
        """Test CPF detection with formatting"""
        text = "CPF: 123.456.789-10"
        match = RE_CPF.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), "123.456.789-10")
    
    def test_cpf_unformatted(self):
        """Test CPF detection without formatting"""
        text = "CPF: 12345678910"
        match = RE_CPF.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), "12345678910")
    
    def test_date_formatted(self):
        """Test date detection in dd/mm/yyyy format"""
        text = "Data do evento: 15/03/2020"
        match = RE_DATE.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), "15/03/2020")
    
    def test_year_detection(self):
        """Test year detection"""
        text = "Ano: 2020"
        match = RE_YEAR.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), "2020")
    
    def test_year_detection_1900s(self):
        """Test year detection for 1900s"""
        text = "Ano: 1995"
        match = RE_YEAR.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), "1995")
    
    def test_valor_simple(self):
        """Test monetary value detection - simple"""
        text = "R$ 500"
        match = RE_VALOR.search(text)
        self.assertIsNotNone(match)
    
    def test_valor_with_cents(self):
        """Test monetary value detection with cents"""
        text = "R$ 1.000,50"
        match = RE_VALOR.search(text)
        self.assertIsNotNone(match)
    
    def test_valor_no_space(self):
        """Test monetary value detection without space"""
        text = "R$500"
        match = RE_VALOR.search(text)
        self.assertIsNotNone(match)
    
    def test_valor_large_amount(self):
        """Test monetary value detection for large amounts"""
        text = "R$ 1.000.000,00"
        match = RE_VALOR.search(text)
        self.assertIsNotNone(match)
    
    def test_valor_multiple_separators(self):
        """Test monetary value with multiple thousand separators"""
        text = "Indenização de R$ 250.000,00"
        match = RE_VALOR.search(text)
        self.assertIsNotNone(match)


class TestExtractFunctions(unittest.TestCase):
    """Test extraction helper functions"""
    
    def test_extract_first_with_match(self):
        """Test extract_first when pattern matches"""
        text = "Data: 01/01/2020 e também 31/12/2021"
        result = extract_first(RE_DATE, text)
        self.assertEqual(result, "01/01/2020")
    
    def test_extract_first_no_match(self):
        """Test extract_first when pattern doesn't match"""
        text = "Texto sem data"
        result = extract_first(RE_DATE, text)
        self.assertEqual(result, "")
    
    def test_contains_any_true(self):
        """Test contains_any when keywords are present"""
        text = "A sentença foi proferida pelo juiz"
        result = contains_any(text, KEYS_SENTENCA)
        self.assertTrue(result)
    
    def test_contains_any_false(self):
        """Test contains_any when keywords are absent"""
        text = "Processo em andamento"
        result = contains_any(text, KEYS_SENTENCA)
        self.assertFalse(result)
    
    def test_contains_any_case_insensitive(self):
        """Test contains_any is case insensitive"""
        text = "A SENTENÇA foi proferida"
        result = contains_any(text, KEYS_SENTENCA)
        self.assertTrue(result)
    
    def test_contains_any_partial_match(self):
        """Test contains_any with partial word match"""
        text = "Processo julgado procedente"
        result = contains_any(text, KEYS_SENTENCA)
        self.assertTrue(result)


class TestScoreMatches(unittest.TestCase):
    """Test scoring function"""
    
    def test_score_all_true(self):
        """Test score when all matches are True"""
        matches = [True, True, True, True]
        score = score_matches(matches)
        self.assertEqual(score, 1.0)
    
    def test_score_all_false(self):
        """Test score when all matches are False"""
        matches = [False, False, False, False]
        score = score_matches(matches)
        self.assertEqual(score, 0.0)
    
    def test_score_half(self):
        """Test score with half matches"""
        matches = [True, False, True, False]
        score = score_matches(matches)
        self.assertEqual(score, 0.5)
    
    def test_score_empty_list(self):
        """Test score with empty list"""
        matches = []
        score = score_matches(matches)
        self.assertEqual(score, 0.0)


class TestFillAdvanced(unittest.TestCase):
    """Test the main fill_advanced function"""
    
    def test_fill_with_itau_flag(self):
        """Test filling when itau_flag is true"""
        row = {
            'itau_flag': 'true',
            'veiculos_flag': 'false',
            'sample_text': 'Processo sem conteúdo relevante'
        }
        result = fill_advanced(row)
        self.assertEqual(result['pergunta_1'], 'sim')
        self.assertEqual(result['pergunta_2'], 'nao')
    
    def test_fill_with_veiculos_flag(self):
        """Test filling when veiculos_flag is true"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'true',
            'sample_text': 'Processo sem conteúdo relevante'
        }
        result = fill_advanced(row)
        self.assertEqual(result['pergunta_1'], 'nao')
        self.assertEqual(result['pergunta_2'], 'sim')
    
    def test_fill_with_sentenca(self):
        """Test pergunta_3 detection for sentence"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'A sentença foi proferida pelo juiz'
        }
        result = fill_advanced(row)
        self.assertEqual(result['pergunta_3'], 'sim')
    
    def test_fill_with_valor(self):
        """Test pergunta_4 detection for monetary value"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'Indenização de R$ 10.000,00'
        }
        result = fill_advanced(row)
        self.assertEqual(result['pergunta_4'], 'sim')
    
    def test_fill_without_valor(self):
        """Test pergunta_4 when no monetary value present"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'Processo de indenização moral'
        }
        result = fill_advanced(row)
        self.assertEqual(result['pergunta_4'], 'nao')
    
    def test_fill_with_cnpj(self):
        """Test pergunta_5 extraction of CNPJ"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'Empresa réu CNPJ 12.345.678/0001-90'
        }
        result = fill_advanced(row)
        self.assertIn('12.345.678/0001-90', result['pergunta_5'])
    
    def test_fill_with_date(self):
        """Test pergunta_6 extraction of date"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'Data do acidente: 15/03/2020'
        }
        result = fill_advanced(row)
        self.assertIn('15/03/2020', result['pergunta_6'])
    
    def test_fill_with_acidente(self):
        """Test pergunta_7 detection for accident"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'Acidente de trânsito com danos'
        }
        result = fill_advanced(row)
        self.assertEqual(result['pergunta_7'], 'sim')
    
    def test_fill_with_vitima(self):
        """Test pergunta_8 detection for victim"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'A vítima sofreu ferimentos graves'
        }
        result = fill_advanced(row)
        self.assertEqual(result['pergunta_8'], 'sim')
    
    def test_fill_with_execucao(self):
        """Test pergunta_9 detection for execution"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'Processo de execução com penhora'
        }
        result = fill_advanced(row)
        self.assertEqual(result['pergunta_9'], 'sim')
    
    def test_fill_perguntas_10_14_empty(self):
        """Test that perguntas 10-14 remain empty"""
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'Texto qualquer'
        }
        result = fill_advanced(row)
        for i in range(10, 15):
            self.assertEqual(result[f'pergunta_{i}'], '')
    
    def test_fill_evidencias_truncated(self):
        """Test that evidencias are truncated at 800 chars"""
        long_text = 'x' * 1000
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': long_text
        }
        result = fill_advanced(row)
        self.assertEqual(len(result['evidencias']), 803)  # 800 + '...'
        self.assertTrue(result['evidencias'].endswith('...'))
    
    def test_fill_evidencias_not_truncated(self):
        """Test that short evidencias are not truncated"""
        short_text = 'Texto curto'
        row = {
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': short_text
        }
        result = fill_advanced(row)
        self.assertEqual(result['evidencias'], short_text)
    
    def test_fill_confidence_calculation(self):
        """Test confidence score calculation"""
        row = {
            'itau_flag': 'true',
            'veiculos_flag': 'true',
            'sample_text': 'A sentença de R$ 10.000,00 foi proferida em 01/01/2020 no acidente com vítima CPF 123.456.789-10'
        }
        result = fill_advanced(row)
        # All 9 criteria should match
        self.assertGreater(result['confidence'], 0.8)
    
    def test_fill_numero_processo(self):
        """Test numero_processo extraction"""
        row = {
            'numero_processo': '1234567-89.2020.8.26.0100',
            'itau_flag': 'false',
            'veiculos_flag': 'false',
            'sample_text': 'Texto'
        }
        result = fill_advanced(row)
        self.assertEqual(result['numero_processo'], '1234567-89.2020.8.26.0100')


class TestKeywordLists(unittest.TestCase):
    """Test that keyword lists are comprehensive"""
    
    def test_keys_sentenca_not_empty(self):
        """Test KEYS_SENTENCA is not empty"""
        self.assertGreater(len(KEYS_SENTENCA), 0)
    
    def test_keys_indemn_not_empty(self):
        """Test KEYS_INDEMN is not empty"""
        self.assertGreater(len(KEYS_INDEMN), 0)
    
    def test_keys_acidente_not_empty(self):
        """Test KEYS_ACIDENTE is not empty"""
        self.assertGreater(len(KEYS_ACIDENTE), 0)
    
    def test_keys_vitima_not_empty(self):
        """Test KEYS_VITIMA is not empty"""
        self.assertGreater(len(KEYS_VITIMA), 0)
    
    def test_keys_exec_not_empty(self):
        """Test KEYS_EXEC is not empty"""
        self.assertGreater(len(KEYS_EXEC), 0)


if __name__ == '__main__':
    unittest.main()
