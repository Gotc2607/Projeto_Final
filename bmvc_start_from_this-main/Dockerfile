# Usar uma imagem Python leve
FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar apenas o arquivo de dependências para otimizar cache
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# copiar todo o código da aplicação
COPY . .

# Expor a porta do aplicativo
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["python", "route.py"]
