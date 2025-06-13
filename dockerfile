# Gunakan base image resmi dari Python
FROM python:3.11-slim

# Tetapkan direktori kerja di dalam container
WORKDIR /app

# Salin file requirements dan instal dependensi
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua sisa kode aplikasi Anda
COPY . .

# Buka port yang akan digunakan oleh aplikasi
EXPOSE 7860 

# Perintah untuk menjalankan aplikasi menggunakan Gunicorn
# Server production yang direkomendasikan untuk Flask
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "app:app"]