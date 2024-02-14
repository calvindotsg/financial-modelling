<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h1 align="center">Stock History Analysis</h1>
</p>
<!-- PROJECT LOGO -->

[![GitHub stars](https://img.shields.io/github/stars/calvindotsg/financial-modelling)](./financial-modelling/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/calvindotsg/financial-modelling)](./financial-modelling/network)
[![GitHub issues](https://img.shields.io/github/issues/calvindotsg/financial-modelling)](./financial-modelling/issues)
[![GitHub license](https://img.shields.io/github/license/calvindotsg/financial-modelling)](./financial-modelling/blob/master/LICENSE)

![Project banner](images/project_banner.jpeg)

## Overview
The Stock History Analysis project aims to determine the preferred portfolio composition from constituents within the S&P 500 index. This is achieved by analyzing historical stock data using various technical analysis models. The project is currently in its initial iteration and is a work in progress.

### Key Components
- **Library Imports**: Essential libraries such as `yfinance`, `pandas`, and `json` are imported to handle data retrieval, manipulation, and storage.
- **Data Retrieval**: The `get_stock_data` function fetches historical stock data for a given ticker and period using the `yfinance` library.
- **Data Processing**: The retrieved data is cleaned and processed to calculate various metrics like closing price, percentage change, holding period yield, holding period return, and portfolio value assuming an initial investment of $1000.
- **Ticker Symbol Reading**: The `read_ticker_symbols` function reads ticker symbols from a CSV file, which allows for batch processing of multiple stocks.
- **Main Execution**: The main block of the notebook orchestrates the reading of ticker symbols and the retrieval of stock data for each symbol. The results are then appended to a list and printed in JSON format.

## Objectives
The primary objective of this iteration is to:
- Retrieve and clean historical stock data for analysis.
- Calculate key financial metrics that will serve as inputs for technical analysis models.
- Prepare the groundwork for integrating various technical analysis models in future iterations.

## Getting started
To use this project, follow these steps:
1. Ensure you have Jupyter Notebook or JupyterLab installed.
2. Clone the repository and navigate to the project directory.
3. Open the `notebooks/stock-history.ipynb` notebook.
4. Run the cells in sequence to perform the analysis.

## Future Work
The next steps for this project include:
- Integration of technical analysis models to evaluate stock performance.
- Optimization of portfolio composition based on historical performance and technical indicators.
- Development of a user interface to interact with the analysis results.
- Expansion of the dataset to include additional financial metrics and a broader range of stocks.

## Project Structure Summary

This repository follows a well-organized structure to enhance maintainability, modularity, and ease of collaboration. The key components include:

### 1. Source Code (`src/`)

- `main/`: Contains the main application logic.
- `data_models/`: Houses Pydantic data models.
- `helpers/`: Stores helper functions.
- `tests/`: TODO: Includes unit tests for application logic, data models, and helper functions.

### 2. Configuration (`config/`)

- `app_config.py`: TODO: Centralized configuration file for application settings.

### 3. Documentation (`docs/`)

- `conf.py`: Sphinx configuration file.
- `index.rst`: Main documentation file.
- `_static/`: Folder for static files used in documentation.
- `_templates/`: Folder for custom templates if needed.

### 4. Images (`images/`)

- Stores images used in documentation.

### 5. Notebooks (`notebooks/`)

- Contains Jupyter notebooks for analysis or experimentation.

### 6. Data (`data/`)

- Houses data sources, such as CSV files.

### 7. Tests (`tests/`)

- `test_integration.py`: TODO: Integration tests.
- Other test files organized by functionality.

### 8. Requirements (`requirements.txt`)

- Lists project dependencies.

## Attribution and Citation

```bibtex
@misc{Loh_Zhang_2024,
  title={calvindotsg/Financial-modelling: Determine the preferred portfolio composition from constituents within the S&P 500 index},
  author={Loh, Calvin and Zhang, Genevieve},
  year={2024},
  url={https://github.com/calvindotsg/financial-modelling/},
}
```

## License
This project is available under the [CC-BY-SA-4.0 License](LICENSE.md). This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. If you remix, adapt, or build upon the material, you must license the modified material under identical terms.

## Contributions
Contributions are welcome. If you would like to contribute to the project, please fork the repository and submit a pull request with your proposed changes.

## Contact
For any queries or discussions regarding the project, please open an issue in the repository.

## Acknowledgments
- Data provided by [Yahoo Finance](https://finance.yahoo.com/) via the `yfinance` library ([GitHub Repo](https://github.com/ranaroussi/yfinance)).
- S&P 500 company list sourced from the publicly available dataset on GitHub, provided by Rufus Pollock and the Open Knowledge Foundation ([GitHub Repo](https://github.com/datasets/s-and-p-500-companies/)).

---

**Note**: This project is in the early stages of development and is subject to significant changes. The current functionality is limited to data retrieval and preliminary processing. Users should be aware that the analysis models are not yet implemented, and the results should not be used for actual trading or investment decisions.
