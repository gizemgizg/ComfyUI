# ComfyUI için temel imaj
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    python3-dev \
    build-essential \
    wget

# Çalışma dizinini oluştur
WORKDIR /app

# ComfyUI'yi klonla
RUN git clone https://github.com/gizemgizg/ComfyUI.git
WORKDIR /app/ComfyUI

# ComfyUI bağımlılıklarını yükle
RUN pip install -r requirements.txt

# Port'ları aç
EXPOSE 8000
EXPOSE 8188

# Başlangıç scripti
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Uygulamayı başlat
CMD ["/app/start.sh"] 
