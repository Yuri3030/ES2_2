FROM python:3.11

# Pasta de trabalho dentro do container
WORKDIR /app

# Copia as dependências primeiro (para cachear melhor)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY ./app ./app

# Comando padrão ao rodar o container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
