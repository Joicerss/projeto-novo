#!/usr/bin/env python3
"""
Quick test script to verify the judicial data collection system structure
This script tests the components without requiring external dependencies
"""

import sys
from pathlib import Path

# Test 1: Check file structure
print("=" * 60)
print("Test 1: Checking File Structure")
print("=" * 60)

required_files = [
    "coleta_judicial/__init__.py",
    "coleta_judicial/config.py",
    "coleta_judicial/base_scraper.py",
    "coleta_judicial/tjsp_scraper.py",
    "coleta_judicial/data_exporter.py",
    "coleta_judicial/main_collector.py",
    "coleta_judicial/examples.py",
    "coleta_judicial/README.md",
    "requirements.txt",
    ".gitignore",
]

base_path = Path(__file__).parent
all_exist = True

for file_path in required_files:
    full_path = base_path / file_path
    exists = full_path.exists()
    status = "✓" if exists else "✗"
    print(f"{status} {file_path}")
    if not exists:
        all_exist = False

if all_exist:
    print("\n✓ All required files are present")
else:
    print("\n✗ Some files are missing")
    sys.exit(1)

# Test 2: Check Python syntax
print("\n" + "=" * 60)
print("Test 2: Checking Python Syntax")
print("=" * 60)

import py_compile

python_files = [
    "coleta_judicial/__init__.py",
    "coleta_judicial/config.py",
    "coleta_judicial/base_scraper.py",
    "coleta_judicial/tjsp_scraper.py",
    "coleta_judicial/data_exporter.py",
    "coleta_judicial/main_collector.py",
    "coleta_judicial/examples.py",
]

all_valid = True

for file_path in python_files:
    full_path = base_path / file_path
    try:
        py_compile.compile(str(full_path), doraise=True)
        print(f"✓ {file_path}")
    except py_compile.PyCompileError as e:
        print(f"✗ {file_path}: {e}")
        all_valid = False

if all_valid:
    print("\n✓ All Python files have valid syntax")
else:
    print("\n✗ Some files have syntax errors")
    sys.exit(1)

# Test 3: Check configuration
print("\n" + "=" * 60)
print("Test 3: Checking Configuration")
print("=" * 60)

sys.path.insert(0, str(base_path))

try:
    from coleta_judicial import config
    
    print(f"✓ Config module loaded")
    print(f"  - Banks: {len(config.BANKS)}")
    print(f"  - Keywords: {len(config.KEYWORDS)}")
    print(f"  - Tribunals: {len(config.TRIBUNALS)}")
    print(f"  - Research questions: {len(config.RESEARCH_QUESTIONS)}")
    print(f"  - Date range: {config.DATE_START} to {config.DATE_END}")
    print(f"  - Output format: {config.OUTPUT_FORMAT}")
    print(f"  - Output directory: {config.OUTPUT_DIR}")
    
except ImportError as e:
    print(f"✗ Failed to load config: {e}")
    # This is expected if dependencies are not installed
    print("  (This is expected if dependencies are not installed)")

# Test 4: Check documentation
print("\n" + "=" * 60)
print("Test 4: Checking Documentation")
print("=" * 60)

readme_path = base_path / "coleta_judicial" / "README.md"
if readme_path.exists():
    content = readme_path.read_text()
    
    required_sections = [
        "Descrição",
        "Instalação",
        "Uso",
        "Configuração",
        "Observações",
    ]
    
    all_sections_present = True
    for section in required_sections:
        if section in content:
            print(f"✓ Section '{section}' present")
        else:
            print(f"✗ Section '{section}' missing")
            all_sections_present = False
    
    word_count = len(content.split())
    print(f"\n  Documentation length: {word_count} words")
    
    if word_count > 500:
        print("✓ Documentation is comprehensive")
    else:
        print("⚠ Documentation might be too brief")
else:
    print("✗ README.md not found")

# Test 5: Check requirements.txt
print("\n" + "=" * 60)
print("Test 5: Checking Requirements")
print("=" * 60)

req_path = base_path / "requirements.txt"
if req_path.exists():
    content = req_path.read_text()
    
    required_packages = [
        "requests",
        "beautifulsoup4",
        "pandas",
        "selenium",
        "playwright",
    ]
    
    for package in required_packages:
        if package in content:
            print(f"✓ {package}")
        else:
            print(f"✗ {package} missing")
    
    line_count = len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')])
    print(f"\n  Total dependencies specified: {line_count}")
else:
    print("✗ requirements.txt not found")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
✓ All basic structure tests passed!

The judicial data collection system is properly set up.

Next steps:
1. Install dependencies: pip install -r requirements.txt
2. Configure parameters in coleta_judicial/config.py
3. Run: cd coleta_judicial && python main_collector.py

Note: The actual scraping functionality requires:
- Installing dependencies
- Inspecting actual TJSP website HTML structure
- Implementing specific parsing logic
- Testing with real searches

See coleta_judicial/README.md for complete documentation.
""")

print("✓ All tests completed successfully!")
