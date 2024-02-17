<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h1 align="center">Stock History Analysis</h1>
</p>
<!-- PROJECT LOGO -->

[![GitHub Repo stars](https://img.shields.io/github/stars/calvindotsg/financial-modelling)](https://github.com/calvindotsg/financial-modelling/stargazers)
[![GitHub license](https://img.shields.io/github/license/calvindotsg/financial-modelling)](./LICENSE)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/calvindotsg/financial-modelling/documentation.yml)](https://github.com/calvindotsg/financial-modelling/actions/workflows/documentation.yml)
[![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/calvindotsg/financial-modelling/main)](https://github.com/calvindotsg/financial-modelling/commits/main/)
[![GitHub forks](https://img.shields.io/github/forks/calvindotsg/financial-modelling)](https://github.com/calvindotsg/financial-modelling/forks)


[![Project banner](images/project_banner.jpeg)](https://model.calvin.sg)

## Overview
Project documentation: https://model.calvin.sg

The Stock History Analysis project aims to determine the preferred portfolio composition from constituents within the S&P 500 index. This is achieved by analyzing historical stock data using various technical analysis models. The project is currently in its initial iteration and is a work in progress.

## Objectives
The primary objective of this iteration is to:
- Retrieve and clean historical stock data for analysis.
- Calculate key financial metrics that will serve as inputs for technical analysis models.
- Store historical stock price data with a suitable schema in Google Firestore document database.
- Prepare the groundwork for integrating various technical analysis models in future iterations.

### Key Components
The key implementation and rationale of the financial-modelling project are:
- **Data Retrieval from stock data source**: The `get_stock_data` function fetches historical stock data for a given ticker and period using the `OpenBB` library from `yfinance` data source.
- **Data Retrieval from Firestore document database**: Determine the most recent stock price data stored in database, to update with up to date data from stock data source.
- **Firestore document database schema**: Each ticker symbols is stored in a separate Firestore collection. Each collection contains documents of stock price data, with ISO 8601 date string as document id and fields storing stock price data.
- **Data Processing**: The retrieved data is cleaned and processed to calculate various metrics like closing price, percentage change, holding period yield, holding period return, and portfolio value assuming an initial investment of $1000.
- **Main Execution**: The main block of the notebook orchestrates the reading of ticker symbols and the retrieval of stock data for each symbol. The results are then appended to a list and printed in JSON format.

## Getting started
To use this project, follow these steps:
1. Clone the GitHub repository to your local machine using `git clone https://github.com/calvindotsg/financial-modelling.git`.
2. Create a Python virtual environment for this project using `python -m venv venv` and activate it using `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).
3. Provide environment variables in the `./.env` file in your project directory. You can use the `./.env.example` file as a template. Make sure to include Firebase service account key file in the `./env` folder.
4. Install the required dependencies as per the `requirements.txt` file using `pip install -r requirements.txt`.
5. To run the project, execute the main script `python app.py`, in the following path `src/main/app.py`. This will initiate the analysis and provide insights into the preferred portfolio composition based on historical stock data.

To access accompanying Jupyter Notebook in this project, follow these steps:
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

- `app_config.py`: Centralized configuration file for application settings.

### 3. Documentation (`docs/`)

- `conf.py`: Sphinx configuration file.
- `index.rst`: Main documentation file.

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

### 9. Environment files (`env/`)

- Service account credential JSON files

## Attribution and Citation
How to cite, bibtex example:
```bibtex
@misc{Loh_Zeyrek_2024,
  title={calvindotsg/Financial-modelling: Determine the preferred portfolio composition from constituents within the S&P 500 index},
  author={Loh, Calvin and Zeyrek, Genevieve},
  year={2024},
  url={https://github.com/calvindotsg/financial-modelling/},
}
```

## License
This project is available under the [CC-BY-SA-4.0 License](LICENSE.md). This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. If you remix, adapt, or build upon the material, you must license the modified material under identical terms.

## Contributing
Contributions are welcome. If you would like to contribute to the project, please fork the repository and submit a pull request with your proposed changes.

## Contact
For any queries or discussions regarding the project, please open an issue in the repository.

## Acknowledgments
- Data provided by [Yahoo Finance](https://finance.yahoo.com/) via the `OpenBB platform` library with `yfinance` extension, ([OpenBB Platform documentation](https://docs.openbb.co/platform)).
- S&P 500 company list sourced from the publicly available dataset on GitHub, provided by Rufus Pollock and the Open Knowledge Foundation, ([GitHub Repo](https://github.com/datasets/s-and-p-500-companies/)).

---

**Disclaimer**: This project is in the early stages of development and is subject to significant changes. The current functionality is limited to data retrieval and preliminary processing. Users should be aware that the analysis models are not yet implemented, and the results should not be used for actual trading or investment decisions.
