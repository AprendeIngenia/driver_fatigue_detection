FROM python:3.10-slim

# install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

# path to work
WORKDIR /app

# requirements
COPY app.py requirements.txt /app/
COPY drowsiness_processor /app/drowsiness_processor

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# app port
EXPOSE 8000

# eject app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]