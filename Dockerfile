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

# 6. Create the config.toml file
# This file is correct, but we need to make sure Streamlit actually uses it!
RUN bash -c 'echo -e "[server]\nport = 8501\naddress = \"0.0.0.0\"\nheadless = true\nenableCORS = false\nenableXsrfProtection = false\n" > /root/.streamlit/config.toml'

# 7. Create startup script
# UPDATE: We 'unset' the AWS variables so they don't override our config
RUN echo '#!/bin/bash\n\
unset STREAMLIT_SERVER_ENABLE_CORS\n\
unset STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION\n\
uvicorn main:app --host 0.0.0.0 --port 8000 & \n\
streamlit run streamlit_app.py\n\
wait' > /app/start.sh

# 8. Permissions and CMD
RUN chmod +x /app/start.sh
EXPOSE 8000
EXPOSE 8501
CMD ["/app/start.sh"]