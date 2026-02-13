FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Кэширование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install allure-pytest==2.13.2

COPY . .

# Команда по умолчанию
CMD ["pytest", "tests", "-v", "--junitxml=test-results.xml", "--alluredir=allure-results"]