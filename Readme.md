# 🛠️ ETL Data Validation Pipeline

This is a Python-based ETL (Extract, Transform, Load) pipeline designed to validate, clean, and load structured CSV data into a PostgreSQL database.

The project demonstrates integration of industry tools like **Pandas**, **Great Expectations**, and **Apache Airflow** to simulate real-world data workflows used in automation and QA environments.

---

## 🚀 Features

- ✅ Parses CSV input using **Pandas DataFrames**
- ✅ Validates schema and data types with **Great Expectations**
- ✅ Flags missing values or formatting errors
- ✅ Uses **Apache Airflow** to schedule ETL execution
- ✅ Pushes clean records to a **PostgreSQL** database

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core scripting language |
| Pandas | Data parsing and manipulation |
| Great Expectations | Data quality checks and validations |
| Apache Airflow | Scheduling and orchestration |
| PostgreSQL | Final data destination (SQL database) |

---

## 📂 Folder Structure

```
etl_project/
├── dags/
│   └── etl_dag.py          # Airflow DAG that orchestrates scheduling of the ETL workflow
├── scripts/
│   ├── etl_runner.py       # Main script that executes extract → validate → load
│   ├── extract.py          # Module for reading CSVs into Pandas DataFrames
│   ├── transform.py        # Module for applying validation and cleansing rules
│   └── load.py             # Module for pushing final data into PostgreSQL
├── expectations/
│   └── suites/             # Great Expectations configuration files and rule definitions
├── config/
│   ├── db_config.py        # Database connection settings (host, port, credentials)
│   └── settings.py         # General config (file paths, thresholds, etc.)
├── data/
│   └── sample_input.csv    # Example CSV input file used for testing
└── requirements.txt
```

---

## 🧩 Module Responsibilities

| Module / Folder        | Purpose / Responsibilities |
|------------------------|-----------------------------|
| **dags/etl_dag.py**     | Defines the Airflow DAG that triggers periodic ETL runs (scheduling, dependencies). |
| **scripts/etl_runner.py** | Orchestrates the ETL steps: calls extract, transform, validate, and load in order. |
| **scripts/extract.py**  | Reads CSV files into Pandas DataFrames; handles malformed file or header issues. |
| **scripts/transform.py**| Applies validation rules via *Great Expectations*, checks for missing values, type mismatches, schema adherence. |
| **scripts/load.py**     | Inserts cleaned and validated data into PostgreSQL, handling batch inserts or upserts. |
| **expectations/suites/**| Contains `.json` or `.yml` definition files for validation expectations (rules). |
| **config/db_config.py**  | Holds database credentials and connection parameters (e.g., user, password, host, port). |
| **config/settings.py**  | Defines constants such as input directory paths, filename patterns, validation thresholds. |
| **data/sample_input.csv**| A sample input dataset that matches expected schema for testing and demonstration. |
| **requirements.txt**     | Lists required Python libraries (pandas, sqlalchemy, airflow, great_expectations, etc.). |

---

## 🔄 Data Flow & Execution

1. **CSV Input** — The pipeline starts by reading CSV files placed in the configured input folder (e.g., `data/`).
2. **Extraction** — `extract.py` loads the file into a Pandas DataFrame, handling file-level sanity checks (headers, encoding, missing columns).
3. **Validation / Transformation** — `transform.py` invokes Great Expectations suites to:
   - Check schema (column names, types)  
   - Validate value ranges / patterns  
   - Detect missing or null values  
   - Mark or drop invalid rows  
4. **Loading** — Cleaned data is passed to `load.py`, which writes it into PostgreSQL (committing valid rows, logging or rejecting invalid ones).
5. **Scheduling** — The entire pipeline is automated by Airflow via `dags/etl_dag.py`, which triggers runs on the configured schedule (e.g., daily).
6. **Reporting & Logging** — Validation results generate expectation reports; logging captures successes, failures, and row-level errors.

---

## 🧾 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/marlono1/ETL_Project.git
cd ETL_Project
```

### 2. Set up a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure PostgreSQL connection  
Edit the config file under `config/db_config.py` with your database credentials.

### 4. Place a sample `.csv` file inside the `data/` folder  
Ensure it follows the expected schema. A sample is included.

### 5. Run the pipeline manually

```bash
python scripts/etl_runner.py
```

### 6. Or trigger via Airflow  
Once Airflow is configured, trigger the DAG from the UI or CLI.

---

## 📈 Future Improvements

- Add logging module and error tracking
- Implement unit tests for data transformation logic
- Enable email alerts for validation failures
- Support for additional input formats (e.g., JSON)

---

## 🙋‍♂️ About the Author

**Marlon Ortiz** – QA Engineer with 8+ years of experience in black box testing, data validation, and system integration. Actively expanding into SDET and data-focused automation roles.

GitHub: [@marlono1](https://github.com/marlono1)
