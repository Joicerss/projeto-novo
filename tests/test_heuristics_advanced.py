import importlib.util
from pathlib import Path


def load_advanced_module():
    repo_root = Path(__file__).resolve().parents[1]
    mod_path = repo_root / 'scripts' / 'auto_fill_pilot_advanced.py'
    spec = importlib.util.spec_from_file_location('adv_mod', str(mod_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_extract_cnpj_and_cpf():
    mod = load_advanced_module()
    txt = 'Empresa X CNPJ 12.345.678/0001-90 e CPF 123.456.789-09 registrado.'
    cnpj = mod.extract_first(mod.RE_CNPJ, txt)
    cpf = mod.extract_first(mod.RE_CPF, txt)
    assert '12.345.678/0001-90' in cnpj
    assert '123.456.789-09' in cpf


def test_extract_date_year_and_valor():
    mod = load_advanced_module()
    txt = 'Pagamento realizado em 05/06/2021 no valor de R$ 1.234,56. Ano referenciado 2020.'
    date = mod.extract_first(mod.RE_DATE, txt)
    valor = mod.extract_first(mod.RE_VALOR, txt)
    year = mod.extract_first(mod.RE_YEAR, txt)
    assert date == '05/06/2021'
    assert 'R$' in valor
    assert year == '2021' or year == '2020'


def test_contains_keywords():
    mod = load_advanced_module()
    # use spelling that matches keywords defined in heuristics
    txt = 'Houve uma sentença favorável e indenização por acidente com vítima.'
    assert mod.contains_any(txt, mod.KEYS_SENTENCA)
    assert mod.contains_any(txt, mod.KEYS_INDEMN)
    assert mod.contains_any(txt, mod.KEYS_ACIDENTE)
    assert mod.contains_any(txt, mod.KEYS_VITIMA)


def test_indenizacao_mode_strict_lenient(tmp_path, monkeypatch):
    # create a temp pilot file with text mentioning 'indenização' but no R$
    pilot = tmp_path / 'pilot.csv'
    pilot.write_text('numero_processo,sample_text\n1,"Pedido de indenização por danos"\n')

    # strict mode: should NOT mark pergunta_4
    monkeypatch.setenv('HEURISTICS_MODE', 'strict')
    spec = importlib.util.spec_from_file_location('adv_mod_s', str(Path(__file__).resolve().parents[1] / 'scripts' / 'auto_fill_pilot_advanced.py'))
    mod_s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod_s)
    # simulate reading the pilot row
    row = {'sample_text': 'Pedido de indenização por danos', 'numero_processo': '1'}
    out_s = mod_s.fill_advanced(row)
    assert out_s['pergunta_4'] == 'nao'

    # lenient mode: should mark pergunta_4 because keyword present
    monkeypatch.setenv('HEURISTICS_MODE', 'lenient')
    spec2 = importlib.util.spec_from_file_location('adv_mod_l', str(Path(__file__).resolve().parents[1] / 'scripts' / 'auto_fill_pilot_advanced.py'))
    mod_l = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(mod_l)
    row2 = {'sample_text': 'Pedido de indenização por danos', 'numero_processo': '1'}
    out_l = mod_l.fill_advanced(row2)
    assert out_l['pergunta_4'] == 'sim'
