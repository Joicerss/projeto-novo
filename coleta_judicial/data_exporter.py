"""
Data export module for judicial process data
Supports multiple output formats (CSV, JSON, Excel)
"""

import json
import logging
from pathlib import Path
from typing import List, Dict
import pandas as pd

logger = logging.getLogger(__name__)


class DataExporter:
    """Handles exporting collected data to various formats"""
    
    def __init__(self, output_dir: str = "resultados_coleta"):
        """
        Initialize exporter
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_to_csv(self, data: List[Dict], filename: str = "processos.csv") -> bool:
        """
        Export data to CSV format
        
        Args:
            data: List of process dictionaries
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = self.output_dir / filename
            
            if not data:
                logger.warning("No data to export")
                return False
            
            # Flatten nested structures for CSV
            flattened_data = self._flatten_data(data)
            
            df = pd.DataFrame(flattened_data)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            logger.info(f"Data exported to CSV: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return False
    
    def export_to_json(self, data: List[Dict], filename: str = "processos.json") -> bool:
        """
        Export data to JSON format
        
        Args:
            data: List of process dictionaries
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = self.output_dir / filename
            
            if not data:
                logger.warning("No data to export")
                return False
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data exported to JSON: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return False
    
    def export_to_excel(self, data: List[Dict], filename: str = "processos.xlsx") -> bool:
        """
        Export data to Excel format
        
        Args:
            data: List of process dictionaries
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = self.output_dir / filename
            
            if not data:
                logger.warning("No data to export")
                return False
            
            # Flatten nested structures for Excel
            flattened_data = self._flatten_data(data)
            
            df = pd.DataFrame(flattened_data)
            
            # Create Excel writer with formatting
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Processos', index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Processos']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"Data exported to Excel: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            return False
    
    def _flatten_data(self, data: List[Dict]) -> List[Dict]:
        """
        Flatten nested structures in data
        
        Args:
            data: List of dictionaries with potentially nested structures
            
        Returns:
            List of flattened dictionaries
        """
        flattened = []
        
        for item in data:
            flat_item = {}
            for key, value in item.items():
                if isinstance(value, list):
                    # Convert lists to strings
                    if value and isinstance(value[0], dict):
                        # List of dicts - join with semicolon
                        flat_item[key] = "; ".join([
                            ", ".join([f"{k}:{v}" for k, v in d.items()])
                            for d in value
                        ])
                    else:
                        # Simple list
                        flat_item[key] = "; ".join(map(str, value))
                elif isinstance(value, dict):
                    # Flatten dict
                    for subkey, subvalue in value.items():
                        flat_item[f"{key}_{subkey}"] = subvalue
                else:
                    flat_item[key] = value
            
            flattened.append(flat_item)
        
        return flattened
    
    def export(self, data: List[Dict], format: str = 'csv', 
               filename: str = None) -> bool:
        """
        Export data in specified format
        
        Args:
            data: List of process dictionaries
            format: Output format (csv, json, xlsx)
            filename: Optional custom filename
            
        Returns:
            True if successful, False otherwise
        """
        if not filename:
            filename = f"processos.{format}"
        
        format = format.lower()
        
        if format == 'csv':
            return self.export_to_csv(data, filename)
        elif format == 'json':
            return self.export_to_json(data, filename)
        elif format in ['xlsx', 'excel']:
            return self.export_to_excel(data, filename)
        else:
            logger.error(f"Unsupported format: {format}")
            return False
    
    def export_summary(self, data: List[Dict], 
                      filename: str = "resumo_coleta.txt") -> bool:
        """
        Export a text summary of the collection
        
        Args:
            data: List of process dictionaries
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = self.output_dir / filename
            
            total_processes = len(data)
            tribunals = {}
            
            for item in data:
                tribunal = item.get('tribunal', 'Desconhecido')
                tribunals[tribunal] = tribunals.get(tribunal, 0) + 1
            
            summary = f"""
RESUMO DA COLETA DE DADOS JUDICIAIS
=====================================

Total de processos coletados: {total_processes}

Distribuição por Tribunal:
"""
            for tribunal, count in tribunals.items():
                summary += f"  - {tribunal}: {count} processos\n"
            
            summary += f"\nArquivos gerados nesta pasta:\n"
            summary += f"  - Dados completos disponíveis nos arquivos CSV/JSON/Excel\n"
            summary += f"  - Consulte a documentação para análise dos dados\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            logger.info(f"Summary exported: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting summary: {e}")
            return False
