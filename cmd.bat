@echo off
REM Create a virtual environment named venv
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install pandas
pip install pandas

REM Run the detector script
python detector.py

REM Deactivate the virtual environment
deactivate

@echo Script execution completed.
