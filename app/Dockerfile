# Usar a imagem oficial do Python
FROM python:3.10

# Instalar dependências essenciais
RUN apt-get update && apt-get install -y bash

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar todos os arquivos do projeto, incluindo a venv existente
COPY . .

# Atualizar dependências do ambiente virtual já existente
RUN /bin/bash -c "source /app/Scripts/activate && pip install --upgrade pip && pip install -r requirements.txt"

# Definir comando padrão ao iniciar o container
CMD ["/bin/bash", "-c", "source /app/Scripts/activate && python main.py"]
