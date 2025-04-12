FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /notice_server

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Запускаем приложение
CMD ["python", "main.py"]

