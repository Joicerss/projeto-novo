import importlib.util
from pathlib import Path


def load_pipeline_module():
    repo_root = Path(__file__).resolve().parents[1]
    mod_path = repo_root / 'starter_scripts' / '01_pipeline_responder_14_questoes.py'
    spec = importlib.util.spec_from_file_location('pipeline_module', str(mod_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_normalize_proc():
    mod = load_pipeline_module()
    sample = '0000000-00.0000.0.00.0000'
    out = mod.normalize_proc(sample)
    expected = ''.join([c for c in sample if c.isdigit()])
    assert out == expected


def test_text_has_any():
    mod = load_pipeline_module()
    assert mod.text_has_any('Itau Unibanco cobrança', mod.ITAU_PATTERNS)
    assert mod.text_has_any('Caminhão e carreta envolvidos', mod.VEIC_PATTERNS)
    assert not mod.text_has_any('texto sem correspondência', mod.ITAU_PATTERNS)
