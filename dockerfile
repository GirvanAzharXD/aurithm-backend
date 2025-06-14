# Gunakan base image resmi dari Python
FROM python:3.11-slim

# Tetapkan direktori kerja di dalam container
WORKDIR /app

# Salin file requirements dan instal dependensi
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua sisa kode aplikasi Anda
COPY . .

# Perintah untuk menjalankan aplikasi
# Fly.io akan secara otomatis mendeteksi port internal 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "app:app"]