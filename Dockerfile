# 1. Base Image
FROM python:3.10-slim

# 2. Set Directory
WORKDIR /app

# 3. Install Dependencies First (Caching Layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Code
COPY . .

# 5. Setup Streamlit Config (The Reliable Way)
# We place the config file exactly where Streamlit looks for it
RUN mkdir -p /root/.streamlit
COPY streamlit_config.toml /root/.streamlit/config.toml

# 6. Setup Entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 7. Expose Ports
EXPOSE 8000
EXPOSE 8501

# 8. Run
CMD ["/app/entrypoint.sh"]