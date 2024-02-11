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

Objectives
----------

The primary objectives of the financial-modelling project are:

- Retrieve and clean historical stock data for analysis.
- Calculate key financial metrics that will serve as inputs for technical analysis models.
- Prepare the groundwork for integrating various technical analysis models in future iterations.

Installation
------------

To use this project, you can install it using the following steps:

1. Clone the repository:

   .. code-block:: shell

      git clone https://github.com/your-username/financial-modelling.git
      cd financial-modelling

2. Install the required dependencies:

   .. code-block:: shell

      pip install -r requirements.txt

Getting started
---------------

To run the project, execute the main script `stock-history.py` located in the project root directory:

.. code-block:: shell

   python stock-history.py

This will initiate the analysis and provide insights into the preferred portfolio composition based on historical stock data.

Project Structure Summary
-------------------------

This repository follows a well-organized structure to enhance maintainability, modularity, and ease of collaboration. The key components include:

Source Code (`src/`)
~~~~~~~~~~~~~~~~~~~~

- `main/`: Contains the main application logic.
- `data_models/`: Houses Pydantic data models.
- `helpers/`: Stores helper functions.
- `tests/`: Includes unit tests for application logic, data models, and helper functions.

Configuration (`config/`)
~~~~~~~~~~~~~~~~~~~~~~~~~

- `app_config.py`: Centralized configuration file for application settings.

Documentation (`docs/`)
~~~~~~~~~~~~~~~~~~~~~~~

- `conf.py`: Sphinx configuration file.
- `index.rst`: Main documentation file.
- `_static/`: Folder for static files used in documentation.
- `_templates/`: Folder for custom templates if needed.

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

Contributing
------------

If you'd like to contribute to the project, please follow the guidelines in the `CONTRIBUTING.md` file.

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.

References
----------

- `Project Repository <https://github.com/your-username/financial-modelling>`_
- `Issue Tracker <https://github.com/your-username/financial-modelling/issues>`_