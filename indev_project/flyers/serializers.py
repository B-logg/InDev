from rest_framework import serializers


BAN_WORDS = {
    "nsfw","nude","naked","porn","explicit","sex","gore","blood","violent",
    # 원하는대로 수정 가능
}

class GenerateFlyerSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    negative_prompt = serializers.CharField(required=False, allow_blank=True, default="")
    width = serializers.IntegerField(required=False, default=768, min_value=256, max_value=1536)
    height = serializers.IntegerField(required=False, default=1024, min_value=256, max_value=1536)
    steps = serializers.IntegerField(required=False, default=30, min_value=5, max_value=75)
    guidance_scale = serializers.FloatField(required=False, default=7.5, min_value=0.0, max_value=20.0)
    seed = serializers.IntegerField(required=False)
    auto_translate = serializers.BooleanField(required=False, default=True)

    # (필수)prompt: 무엇을 만들지에 대한 긍정 프롬프트. 이미지의 주제, 스타일, 색감, 구도 등을 자연어로 제시
    # (선택)negative_prompt: 피하고 싶은 요소를 적는 프롬프트. 품질을 해치는 요소를 배제.
    # (선택)width/height: 생성되는 이미지의 출력 해상도(픽셀). 
    # (선택)steps: 샘플링 횟수, 클수록 품질이 오르지만 시간이 선형 증가
    # (선택)guidance_scale: CFG 스케일(프롬프트를 얼마나 강하게 믿을지)
    # (선택)seed: 난수 시드(같은 모델/프롬프트/파라미터라면 같은 시드 = 동일 결과)
    # 다른 결과를 보고 싶으면 시드를 바꾸거나 비우기

    def validate_prompt(self, v):
        low = v.lower()
        if any(w in low for w in BAN_WORDS):
            raise serializers.ValidationError("허용되지 않은 내용이 포함되어있습니다. 프롬프트를 수정하세요!")
        return v