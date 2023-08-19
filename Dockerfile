# Anahtar dosyanızın adı: Dockerfile

# Python 3.8 sürümünü kullanarak resmi bir temel görüntü kullanın
FROM python:3.9-slim-buster

# Çalışma dizinini ayarlayın
WORKDIR /usr/src/app

# Gerekli bağımlılıkları kurmak için requirements.txt dosyasını kopyalayın
RUN python3 -m pip install --upgrade pip

COPY requirements.txt ./

RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Uygulamanın geri kalan dosyalarını kopyalayın
COPY . .

# Uygulamanın çalıştırılacağı portu belirtin (örneğin: 8000)
EXPOSE 8000

# Uygulamanızı çalıştırmak için komutu belirtin
CMD ["python", "./main.py"]
