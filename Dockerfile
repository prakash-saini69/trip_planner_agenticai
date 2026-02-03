# 1. Use an official Python runtime
FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy files
COPY . /app

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Create the .streamlit directory
RUN mkdir -p /root/.streamlit

# 6. Create the config.toml file to FORCE disable CORS/XSRF
# This is the "Nuclear Option" that overrides AWS variables
RUN bash -c 'echo -e "[server]\nport = 8501\naddress = \"0.0.0.0\"\nheadless = true\nenableCORS = false\nenableXsrfProtection = false\n" > /root/.streamlit/config.toml'

# 7. Create startup script (Updated with = signs for safety)
RUN echo '#!/bin/bash\nuvicorn main:app --host 0.0.0.0 --port 8000 & \nstreamlit run streamlit_app.py\nwait' > /app/start.sh

# 8. Permissions and CMD
RUN chmod +x /app/start.sh
EXPOSE 8000
EXPOSE 8501
CMD ["/app/start.sh"]