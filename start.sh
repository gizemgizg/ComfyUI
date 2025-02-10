#!/bin/bash

# ComfyUI'yi arka planda başlat
python main.py --listen 0.0.0.0 --port 8188 &

# API'yi başlat
python app.py 
