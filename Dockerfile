# 1. Use an official Python runtime
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your specific files (Code + Configs)
COPY . /app

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Open the ports for API (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# 6. Create a startup script to run BOTH apps at once
# FIX: Added --server.enableCORS false and --server.enableXsrfProtection false
RUN echo '#!/bin/bash\nuvicorn main:app --host 0.0.0.0 --port 8000 & \nstreamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false\nwait' > /app/start.sh

# 7. Make the script executable
RUN chmod +x /app/start.sh

# 8. Run the script when container starts
CMD ["/app/start.sh"]