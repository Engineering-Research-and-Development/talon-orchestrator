FROM python:3.9.15-slim 

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install streamlit
RUN pip install -r requirements.txt

# Your python scripts and others dependencies
ADD ./src /src

COPY .streamlit/config.toml /root/.streamlit/config.toml

WORKDIR /src
# Run your main script
# ENTRYPOINT ["python", "main.py"]

ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]