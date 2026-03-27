FROM python:3.11-slim

# System deps for GDAL, WeasyPrint, psycopg2
RUN apt-get update && apt-get install -y \
    gdal-bin libgdal-dev \
    libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
    libcairo2 libgdk-pixbuf2.0-0 libffi-dev \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

ENV GDAL_VERSION=3.6.0
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
