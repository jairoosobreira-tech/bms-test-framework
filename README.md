# BMS Test Framework

Python QA automation framework for Battery Management System validation.
Built with pytest, simulating real automotive testing scenarios (Voltage, Temperature, DTCs).

## Project Structure

- `bms.py` — BMSCell class with ISO 26262 safety logic
- `log_parser.py` — CAN/UDS log parser with DTC extraction
- `run_tests.py` — JSON-driven test runner with report generation
- `test_bms.py` — pytest suite for BMSCell (9 tests)
- `test_log_parser.py` — pytest suite for log parser (5 tests)

## Setup

python -m venv .venv
source .venv/bin/activate
pip install pytest

## Run Tests

pytest -v

## Run JSON-driven suite

python run_tests.py
