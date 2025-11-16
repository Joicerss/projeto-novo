"""
Main orchestrator script for judicial data collection
Coordinates search, extraction, and export of judicial process data
"""

import logging
import time
from datetime import datetime
from typing import List, Dict
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    BANKS, KEYWORDS, TRIBUNALS, DATE_START, DATE_END,
    OUTPUT_FORMAT, OUTPUT_DIR, TIMEOUT, DELAY_BETWEEN_REQUESTS,
    RESEARCH_QUESTIONS
)
from tjsp_scraper import TJSPScraper
from data_exporter import DataExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('coleta_judicial.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class JudicialDataCollector:
    """Main coordinator for judicial data collection"""
    
    def __init__(self):
        """Initialize the collector"""
        self.scrapers = {}
        self.all_results = []
        self.exporter = DataExporter(output_dir=OUTPUT_DIR)
        
    def initialize_scrapers(self):
        """Initialize scrapers for configured tribunals"""
        logger.info("Initializing scrapers...")
        
        for code, config in TRIBUNALS.items():
            try:
                if code == 'TJSP':
                    scraper = TJSPScraper(
                        search_url=config['search_url'],
                        timeout=TIMEOUT
                    )
                    self.scrapers[code] = scraper
                    logger.info(f"Initialized scraper for {config['name']}")
                else:
                    logger.warning(f"Scraper not implemented for {code}")
            except Exception as e:
                logger.error(f"Failed to initialize scraper for {code}: {e}")
    
    def build_search_terms(self) -> List[str]:
        """
        Build search term combinations
        
        Returns:
            List of search term strings
        """
        search_terms = []
        
        # Combine banks with keywords
        for bank in BANKS:
            for keyword in KEYWORDS:
                term = f"{bank} {keyword}"
                search_terms.append(term)
        
        # Also add just the main keywords
        search_terms.extend(KEYWORDS)
        
        return search_terms
    
    def collect_data(self):
        """Execute the data collection process"""
        logger.info("=" * 60)
        logger.info("Starting judicial data collection")
        logger.info("=" * 60)
        
        # Print research questions
        logger.info("\nResearch Questions:")
        for question in RESEARCH_QUESTIONS:
            logger.info(f"  {question}")
        
        logger.info(f"\nSearch Period: {DATE_START} to {DATE_END}")
        logger.info(f"Output Format: {OUTPUT_FORMAT}")
        logger.info(f"Output Directory: {OUTPUT_DIR}\n")
        
        # Initialize scrapers
        self.initialize_scrapers()
        
        if not self.scrapers:
            logger.error("No scrapers initialized. Exiting.")
            return
        
        # Build search terms
        search_terms = self.build_search_terms()
        logger.info(f"Prepared {len(search_terms)} search term combinations")
        
        # Collect from each tribunal
        for code, scraper in self.scrapers.items():
            logger.info(f"\n{'=' * 60}")
            logger.info(f"Collecting from {code}")
            logger.info(f"{'=' * 60}")
            
            try:
                # Search with all keywords
                results = scraper.search_processes(
                    keywords=KEYWORDS + BANKS,
                    date_start=DATE_START,
                    date_end=DATE_END
                )
                
                logger.info(f"Found {len(results)} processes in {code}")
                
                # Add results to collection
                self.all_results.extend(results)
                
                # Delay between tribunals
                if len(self.scrapers) > 1:
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                
            except Exception as e:
                logger.error(f"Error collecting from {code}: {e}")
                continue
        
        # Summary
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Collection Summary")
        logger.info(f"{'=' * 60}")
        logger.info(f"Total processes collected: {len(self.all_results)}")
        
        # Export results
        self.export_results()
        
        # Cleanup
        self.cleanup()
    
    def export_results(self):
        """Export collected results"""
        if not self.all_results:
            logger.warning("No results to export")
            return
        
        logger.info("\nExporting results...")
        
        # Export in configured format
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"processos_{timestamp}"
        
        success = self.exporter.export(
            data=self.all_results,
            format=OUTPUT_FORMAT,
            filename=f"{filename}.{OUTPUT_FORMAT}"
        )
        
        if success:
            # Also export as JSON for backup
            if OUTPUT_FORMAT != 'json':
                self.exporter.export_to_json(
                    self.all_results,
                    f"{filename}.json"
                )
            
            # Export summary
            self.exporter.export_summary(self.all_results)
            
            logger.info(f"\nResults exported successfully to {OUTPUT_DIR}/")
        else:
            logger.error("Failed to export results")
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("\nCleaning up...")
        for code, scraper in self.scrapers.items():
            try:
                scraper.close()
            except Exception as e:
                logger.error(f"Error closing scraper {code}: {e}")
    
    def run(self):
        """Run the complete collection process"""
        start_time = time.time()
        
        try:
            self.collect_data()
        except KeyboardInterrupt:
            logger.info("\n\nCollection interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            elapsed = time.time() - start_time
            logger.info(f"\nTotal execution time: {elapsed:.2f} seconds")


def main():
    """Main entry point"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║     Coletor de Dados de Processos Judiciais              ║
║     Recuperação Judicial - Itaú e Veículos Pesados       ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    collector = JudicialDataCollector()
    collector.run()
    
    print("\n✓ Collection completed. Check the logs and output directory.")


if __name__ == "__main__":
    main()
