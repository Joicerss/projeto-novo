# Projeto Novo - Jurimetria Case

A jurimetrics analysis and reporting tool for legal data visualization and statistical analysis.

## Overview

This repository contains tools and results for jurimetric analysis, including:
- Statistical analysis of legal case data
- Survival analysis (Kaplan-Meier curves)
- Logistic regression and Cox proportional hazards models
- Automated HTML report generation

## Project Structure

```
.
├── generate_report_complete.py    # Main report generation script
├── requirements.txt               # Python dependencies
├── pyproject.toml                # Python package configuration
├── README.md                     # This file
├── .github/workflows/            # CI/CD workflows
│   └── python-publish.yml        # PyPI publishing workflow
└── Data files:
    ├── *.png                     # Visualization plots
    ├── *.csv                     # Analysis results
    └── *.html                    # Generated reports
```

## Data Files

- `distribuicao_tempo_tramitacao.png` — Histogram of case processing time
- `resultado_por_juiz.png` — Results count by judge
- `boxplot_valor_causa.png` — Boxplot of case value by outcome
- `kaplan_meier_survival.png` — Kaplan-Meier survival curve
- `quebra_estrutural_detectada.png` — Structural break detection (simulated)
- `resultados_regressao_logistica.csv` — Logistic regression odds ratios
- `hazard_ratios_cox.csv` — Cox proportional hazards model summary
- `classification_report.txt` — Classification report for test set
- `confusion_matrix.csv` — Confusion matrix
- `cv_scores.csv` — Cross-validation accuracy scores
- `report_complete.html` — Complete HTML report with figures and tables

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Joicerss/projeto-novo.git
cd projeto-novo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install the package in development mode:
```bash
pip install -e .
```

## Usage

### Generate HTML Report

Run the report generation script:

```bash
python generate_report_complete.py
```

Or if installed as a package:
```bash
generate-report
```

The script will generate `report_complete.html` in the current directory, combining:
- All visualization plots (PNG files)
- Statistical analysis results (CSV tables)

### View the Report

Open `report_complete.html` in a web browser to view the complete analysis report.

## Development

### Running Tests

```bash
pytest
```

### Building the Package

```bash
python -m build
```

## CI/CD

This repository includes a GitHub Actions workflow that automatically publishes the package to PyPI when a release is created.

## Notes

- The data used in this project is simulated for demonstration purposes
- All generated reports and visualizations are reproducible from the source data
- The HTML reports are self-contained and can be shared independently

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is available for educational and research purposes.
