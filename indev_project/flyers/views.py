from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .serializers import GenerateFlyerSerializer
from .services import generate_flyer_image_via_api
from .models import Flyer 

class GenerateFlyerView(APIView):
    """
    POST /flyers/generate/
    {
      "prompt": "떡볶이 전단지",
      "negative_prompt": "blurry, low quality",
      "width": 512,
      "height": 512,
      "steps": 20,
      "guidance_scale": 7.0,
      "seed": 1234
    }
    """

    def post(self, request):
        ser = GenerateFlyerSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        try:
            # ✅ AI 서버 호출
            ai_result = generate_flyer_image_via_api(data)

            # DB 저장
            flyer = Flyer.objects.create(
                prompt=data["prompt"],
                negative_prompt=data.get("negative_prompt", ""),
                width=ai_result.get("width", data.get("width", 768)),
                height=ai_result.get("height", data.get("height", 1024)),
                steps=ai_result.get("steps", data.get("steps", 30)),
                guidance_scale=ai_result.get("guidance_scale", data.get("guidance_scale", 7.5)),
                seed=ai_result.get("seed", data.get("seed") or 0),
                image=ai_result["file"],  # AI 서버가 반환한 경로/파일명
            )

            file_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{flyer.image.name}")

            return Response(
                {
                    "ok": True,
                    "id": flyer.id,
                    "file": flyer.image.name,
                    "url": file_url,
                    "meta": {
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

        except request.exceptions.RequestException as e:
            return Response({"ok": False, "error": f"AI 서버 연결 실패: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            return Response({"ok": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
