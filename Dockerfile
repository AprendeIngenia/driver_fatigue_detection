FROM python:3.10

# install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

# path to work
WORKDIR /app

# requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# app port
EXPOSE 8000

# eject app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]