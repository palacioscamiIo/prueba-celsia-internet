# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto 5000 para acceder a la aplicación Flask
EXPOSE 5000

# Establece el comando por defecto para ejecutar la aplicación
CMD ["python", "app/main.py"]
