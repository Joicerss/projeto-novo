#!/usr/bin/env python3
"""
Example script demonstrating how to use the judicial data collector
This script shows basic usage patterns and can be customized
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from coleta_judicial import JudicialDataCollector, TJSPScraper, DataExporter


def example_basic_collection():
    """Example 1: Basic complete collection"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Collection")
    print("=" * 60)
    
    collector = JudicialDataCollector()
    collector.run()


def example_tjsp_only():
    """Example 2: Collect only from TJSP"""
    print("\n" + "=" * 60)
    print("Example 2: TJSP Only Collection")
    print("=" * 60)
    
    scraper = TJSPScraper(
        search_url="https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do",
        timeout=30
    )
    
    try:
        results = scraper.search_processes(
            keywords=["recuperação judicial", "Itaú", "veículos pesados"],
            date_start="01/01/2023",
            date_end="31/12/2025",
            max_results=50
        )
        
        print(f"Found {len(results)} processes")
        
        # Export results
        if results:
            exporter = DataExporter(output_dir="resultados_tjsp")
            exporter.export_to_csv(results, "processos_tjsp.csv")
            exporter.export_to_json(results, "processos_tjsp.json")
            print("Results exported successfully")
        
    finally:
        scraper.close()


def example_custom_search():
    """Example 3: Custom search with specific parameters"""
    print("\n" + "=" * 60)
    print("Example 3: Custom Search")
    print("=" * 60)
    
    # Customize search parameters
    custom_keywords = [
        "recuperação judicial",
        "Itaú Unibanco",
        "caminhão",
        "transporte rodoviário"
    ]
    
    scraper = TJSPScraper(
        search_url="https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do"
    )
    
    try:
        results = scraper.search_processes(
            keywords=custom_keywords,
            date_start="01/06/2023",
            date_end="30/06/2024",
            max_results=100
        )
        
        print(f"Custom search found {len(results)} processes")
        
        # Filter results (example)
        filtered = [r for r in results if 'Itaú' in str(r)]
        print(f"After filtering: {len(filtered)} processes")
        
    finally:
        scraper.close()


def example_export_formats():
    """Example 4: Export data in different formats"""
    print("\n" + "=" * 60)
    print("Example 4: Multiple Export Formats")
    print("=" * 60)
    
    # Sample data for demonstration
    sample_data = [
        {
            'tribunal': 'TJSP',
            'numero_processo': '1234567-89.2023.8.26.0100',
            'classe': 'Recuperação Judicial',
            'assunto': 'Recuperação Judicial',
            'data_distribuicao': '15/03/2023',
            'valor_causa': 'R$ 5.000.000,00',
            'partes': [
                {'tipo': 'Requerente', 'nome': 'Empresa X Transportes Ltda'},
                {'tipo': 'Credor', 'nome': 'Itaú Unibanco S.A.'}
            ]
        },
        {
            'tribunal': 'TJSP',
            'numero_processo': '9876543-21.2023.8.26.0100',
            'classe': 'Recuperação Judicial',
            'assunto': 'Recuperação Judicial',
            'data_distribuicao': '20/05/2023',
            'valor_causa': 'R$ 3.500.000,00',
            'partes': [
                {'tipo': 'Requerente', 'nome': 'Transportadora Y S.A.'},
                {'tipo': 'Credor', 'nome': 'Banco Itaú S.A.'}
            ]
        }
    ]
    
    exporter = DataExporter(output_dir="exemplos_export")
    
    # Export in all formats
    exporter.export_to_csv(sample_data, "exemplo.csv")
    print("✓ CSV exported")
    
    exporter.export_to_json(sample_data, "exemplo.json")
    print("✓ JSON exported")
    
    exporter.export_to_excel(sample_data, "exemplo.xlsx")
    print("✓ Excel exported")
    
    exporter.export_summary(sample_data, "resumo.txt")
    print("✓ Summary exported")
    
    print(f"\nAll files saved to: exemplos_export/")


def main():
    """Main function to run examples"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║         Examples - Judicial Data Collector               ║
╚═══════════════════════════════════════════════════════════╝

Choose an example to run:
1. Basic complete collection
2. TJSP only collection
3. Custom search parameters
4. Export in different formats
0. Exit
""")
    
    try:
        choice = input("Enter your choice (0-4): ").strip()
        
        if choice == '1':
            example_basic_collection()
        elif choice == '2':
            example_tjsp_only()
        elif choice == '3':
            example_custom_search()
        elif choice == '4':
            example_export_formats()
        elif choice == '0':
            print("Exiting...")
            return
        else:
            print("Invalid choice. Please run again and select 0-4.")
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
