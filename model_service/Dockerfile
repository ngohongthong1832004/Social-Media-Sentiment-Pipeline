FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc libffi-dev libssl-dev curl

WORKDIR /app
COPY requirements.txt .

# Sử dụng PyTorch mirror + tăng timeout
RUN pip install --default-timeout=100 --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
