.. financial-modelling documentation master file, created by
   sphinx-quickstart on Fri Jan 26 22:59:54 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to financial-modelling's documentation!
===============================================

.. image:: ../images/project_banner.jpeg

Overview
--------

The Stock History Analysis project aims to determine the preferred portfolio composition from constituents within the S&P 500 index. This is achieved by analyzing historical stock data using various technical analysis models. The project is currently in its initial iteration and is a work in progress.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Overview
--------

The Stock History Analysis project aims to determine the preferred portfolio composition from constituents within the S&P 500 index. This is achieved by analyzing historical stock data using various technical analysis models. The project is currently in its initial iteration and is a work in progress.

Objectives
----------

The primary objectives of the financial-modelling project are:

- Retrieve and clean historical stock data for analysis.
- Calculate key financial metrics that will serve as inputs for technical analysis models.
- Store historical stock price data with a suitable schema in Google Firestore document database.
- Prepare the groundwork for integrating various technical analysis models in future iterations.

Key Components
--------------

The key implementation and rationale of the financial-modelling project are:

- Data Retrieval from stock data source: The `get_stock_data` function fetches historical stock data for a given ticker and period using the `OpenBB` library from `yfinance` data source.
- Data Retrieval from Firestore document database: Determine the most recent stock price data stored in database, to update with up to date data from stock data source.
- Firestore document database schema: Each ticker symbols is stored in a separate Firestore collection. Each collection contains documents of stock price data, with ISO 8601 date string as document id and fields storing stock price data.
- Data Processing: The retrieved data is cleaned and processed to calculate various metrics like closing price, percentage change, holding period yield, holding period return, and portfolio value assuming an initial investment of $1000.
- Main Execution: The main block of the notebook orchestrates the reading of ticker symbols and the retrieval of stock data for each symbol. The results are then appended to a list and printed in JSON format.

CI/CD Overview
==============

This project retrieves, cleans, and analyzes historical stock data. The project adopts the following CI/CD features to ensure code and documentation quality and reliability:

- **Static code analysis with Qodana by JetBrains**: This tool checks and improves the code that performs the data retrieval, processing, and analysis of stock data. This includes suggestions to improve upon code quality, security, and duplication issues. The project follows strict type annotations and PEP 8 coding style conventions.
- **Project and source code documentation with Sphinx and numpy style docstrings**: This documentation explains the purpose, logic, and implementation of data handling and analysis in various modules. It uses Sphinx to generate HTML documentation from docstrings in a standard format for scientific and numerical projects.
- **Sphinx build hosting with GitHub Pages and Cloudflare CDN**: This feature makes the documentation accessible and available for users and developers who want to learn more about this project and its results. It hosts static websites from this GitHub repository and uses a custom domain: `https://model.calvin.sg` to deliver web content faster and more securely.
- **Workflow automation and configuration management with GitHub Actions and Infrastructure as Code**: This feature manages and automates the CI/CD workflows and ensures that the code and documentation are always in sync with the latest changes. It uses GitHub Actions to run the static code analysis tool and deploy the Sphinx build onto GitHub Pages.


Getting started
---------------

To use this project, you can install it using the following steps:

1. Clone the repository:

   .. code-block:: shell

      git clone https://github.com/calvindotsg/financial-modelling.git
      cd financial-modelling

2. Create a Python virtual environment for this project and and activate it:

   .. code-block:: shell

      python -m venv venv
      source venv/bin/activate

3. Provide environment variables in the ./.env file in your project directory. You can use the ./.env.example file as a template. Make sure to include Firebase service account key file in the ./env folder

4. Install the required dependencies:

   .. code-block:: shell

      pip install -r requirements.txt

5. To run the project, execute the main script `app.py`, in the following path `src/main/app.py`

   .. code-block:: shell

      python app.py

   This will initiate the analysis and provide insights into the preferred portfolio composition based on historical stock data.

To access accompanying Jupyter Notebook in this project, follow these steps:

1. Ensure you have Jupyter Notebook or JupyterLab installed.
2. Clone the repository and navigate to the project directory.
3. Open the `notebooks/stock-history.ipynb` notebook.
4. Run the cells in sequence to perform the analysis.

Future Work
-----------
The next steps for this project include:

- Integration of technical analysis models to evaluate stock performance.
- Optimization of portfolio composition based on historical performance and technical indicators.
- Development of a user interface to interact with the analysis results.
- Expansion of the dataset to include additional financial metrics and a broader range of stocks.

Project Structure Summary
-------------------------

This repository follows a well-organized structure to enhance maintainability, modularity, and ease of collaboration. The key components include:

Source Code (`src/`)
~~~~~~~~~~~~~~~~~~~~

- `main/`: Contains the main application logic.
- `data_models/`: Houses Pydantic data models.
- `helpers/`: Stores helper functions.
- `tests/`: TODO: Includes unit tests for application logic, data models, and helper functions.

Configuration (`config/`)
~~~~~~~~~~~~~~~~~~~~~~~~~

- `app_config.py`: Centralized configuration file for application settings.

Documentation (`docs/`)
~~~~~~~~~~~~~~~~~~~~~~~

- `conf.py`: Sphinx configuration file.
- `index.rst`: Main documentation file.

Images (`images/`)
~~~~~~~~~~~~~~~~~~

- Stores images used in documentation.

Notebooks (`notebooks/`)
~~~~~~~~~~~~~~~~~~~~~~~~

- Contains Jupyter notebooks for analysis or experimentation.

Data (`data/`)
~~~~~~~~~~~~~~

- Houses data sources, such as CSV files.

Tests (`tests/`)
~~~~~~~~~~~~~~~~

- `test_integration.py`: Integration tests.
- Other test files organized by functionality.

Requirements (`requirements.txt`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Lists project dependencies.

Environment files (`env/`)
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Service account credential JSON files

Attribution and Citation
------------------------

How to cite, bibtex example:

.. code-block:: bibtex

   @misc{Loh_Zeyrek_2024,
     title={calvindotsg/Financial-modelling: Determine the preferred portfolio composition from constituents within the S&P 500 index},
     author={Loh, Calvin and Zeyrek, Genevieve},
     year={2024},
     url={https://github.com/calvindotsg/financial-modelling/},
   }

License
-------

This project is available under the `CC-BY-SA-4.0 License <https://github.com/calvindotsg/financial-modelling/blob/main/LICENSE>`_. This license enables reusers to distribute, remix, adapt, and build upon the material in any medium or format, so long as attribution is given to the creator. The license allows for commercial use. If you remix, adapt, or build upon the material, you must license the modified material under identical terms.

Contributing
------------

If you'd like to contribute to the project, please follow the guidelines in the `CONTRIBUTING.md` file.

Contact
-------

For any queries or discussions regarding the project, please open an issue in the repository.


Acknowledgments
---------------

- Data provided by `Yahoo Finance <https://finance.yahoo.com/>`_ via the `OpenBB platform` library with `yfinance` extension, `OpenBB Platform documentation <https://docs.openbb.co/platform>`_.
- S&P 500 company list sourced from the publicly available dataset on GitHub, provided by Rufus Pollock and the Open Knowledge Foundation, `GitHub repository: datasets/s-and-p-500-companies <https://github.com/datasets/s-and-p-500-companies/>`_.

Disclaimer
----------

This project is in the early stages of development and is subject to significant changes. The current functionality is limited to data retrieval and preliminary processing. Users should be aware that the analysis models are not yet implemented, and the results should not be used for actual trading or investment decisions.

Project links
-------------

- `GitHub Project Repository: financial-modelling <https://github.com/calvindotsg/financial-modelling>`_
- `GitHub Issue Tracker <https://github.com/calvindotsg/financial-modelling/issues>`_