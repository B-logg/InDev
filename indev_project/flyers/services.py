import requests
from django.conf import settings

# AI 서버 주소
AI_SERVER_URL = "http://<AI_SERVER_IP>/generate"

def generate_flyer_image_via_api(data: dict) -> dict:
    # AI 서버에 요청을 보내고 결과(JSON)를 반환
    
    res = requests.post(AI_SERVER_URL, json=data, timeout=300)
    res.raise_for_status()
    return res.json()
