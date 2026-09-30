FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Generar iconos y base inicial
RUN python generate_icons.py
RUN python seed_data.py

# Exponer puerto
ENV PORT=8000
EXPOSE 8000

# Comando de inicio
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
