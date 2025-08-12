# flyers/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .serializers import GenerateFlyerSerializer
from .services import generate_flyer_image
from .models import Flyer 

class GenerateFlyerView(APIView):
    """
    POST flyers/generate/
    {
      "prompt": "떡이 쫄깃하고, 매콤달콤한 원조 떡볶이 가게 전단지",
      "negative_prompt": "blurry, low quality, watermark, text artifacts",
      "width": 768,
      "height": 1024,
      "steps": 28,
      "guidance_scale": 7.0,
      "seed": 1234
    }
    """

    def post(self, request):
        ser = GenerateFlyerSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        try:
            # 이미지 생성 (services.py가 파일명을 반환)
            filename = generate_flyer_image(**data)

            # --- (선택) DB에 생성 이력 저장 ---
            flyer = Flyer.objects.create(
                prompt=data["prompt"],
                negative_prompt=data.get("negative_prompt", ""),
                width=data.get("width", 768),
                height=data.get("height", 1024),
                steps=data.get("steps", 30),
                guidance_scale=data.get("guidance_scale", 7.5),
                seed=(data.get("seed") or 0),  # services에서 랜덤 시드 썼다면 여기엔 0 저장
                image=filename,  # ImageField: MEDIA_ROOT 기준 상대 경로/파일명
            )

            # 절대 URL을 만들어서 프론트가 바로 사용할 수 있도록함
            file_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{flyer.image.name}")

            return Response(
                {
                    "ok": True,
                    "id": flyer.id,
                    "file": flyer.image.name,
                    "url": file_url,
                    "meta": {
                        "model": "Stable Diffusion v1.5",
                        "width": flyer.width,
                        "height": flyer.height,
                        "steps": flyer.steps,
                        "guidance_scale": flyer.guidance_scale,
                        "seed": flyer.seed,
                        "created_at": flyer.created_at,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        # services.py에서 입력 값 검증에 실패하면 ValueError를 던지도록 했다면 400으로 내려줌
        # 또는 NSFW 플래그 검사를 통한 안전 필터(세이프티 체크)에 걸러진 것.(노출/음란/민감 등의 이미지 반환 막기)
        except ValueError as e:
            return Response({"ok": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"ok": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
