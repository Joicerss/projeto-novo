"""
Judicial Data Collection Package
Automation scripts for collecting judicial process data from Brazilian courts
"""

__version__ = "1.0.0"
__author__ = "Projeto Jurimetria"

from .base_scraper import BaseJudicialScraper
from .tjsp_scraper import TJSPScraper
from .data_exporter import DataExporter
from .main_collector import JudicialDataCollector

__all__ = [
    'BaseJudicialScraper',
    'TJSPScraper',
    'DataExporter',
    'JudicialDataCollector',
]
