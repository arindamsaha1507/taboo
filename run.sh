#!/bin/bash
# Run the Taboo game Streamlit app

# Activate virtual environment and run the app
source .venv/bin/activate
streamlit run app.py > logs/log.txt 2> logs/err.txt
