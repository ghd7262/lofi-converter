FROM python:3.12-slim
WORKDIR /app
# Pedalboard's native module links against libatomic, which slim images leave out.
RUN apt-get update && apt-get install -y --no-install-recommends libatomic1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
COPY tests tests
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
