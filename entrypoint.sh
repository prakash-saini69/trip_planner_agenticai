#!/bin/bash
# 1. Unset AWS variables that might conflict
unset STREAMLIT_SERVER_ENABLE_CORS
unset STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION

# 2. Start the Backend (Uvicorn) in the background
echo "Starting Backend..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# 3. Start the Frontend (Streamlit)
echo "Starting Frontend..."
streamlit run streamlit_app.py