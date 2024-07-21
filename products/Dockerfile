# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libdbus-1-3 \
    libxtst6 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libatspi2.0-0 \
    libxrandr2 \
    fonts-liberation \
    libasound2 \
    libcurl4 \
    libdrm2 \
    libgbm1 \
    libu2f-udev \
    libvulkan1 \
    xdg-utils \
    gnupg curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get -fy install \
    && rm google-chrome-stable_current_amd64.deb

# Устанавливаем ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.182/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver-linux64.zip

# Копируем зависимости и устанавливаем
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем код приложения
COPY . .

# Запускаем приложение
CMD ["python", "app.py", "--cfg=config.yml"]