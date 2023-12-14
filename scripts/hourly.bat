@echo off

:: Create virtual environment
if not exist .venv\ (
	python -m venv .venv
)

:: Activate virtual environment
call .venv\Scripts\activate

:: Update virtual environment
python -m pip install pip setuptools wheel --upgrade

:: Install dependencies
pip install -r requirements.txt --upgrade

:: Talent
talent esi jita_orders
talent esi vale_orders
talent etl orders
talent docs build
