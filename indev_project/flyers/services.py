# flyers/services.py
from __future__ import annotations

import random, uuid, math
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline
from django.conf import settings
from .translate import ko_to_en, contains_korean

# 디바이스/DTYPE: CUDA > MPS(MAC의 경우에만 해당함) > CPU
_device = (
    "cuda" if torch.cuda.is_available()
    else ("mps" if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()
          else "cpu")
)
_dtype = torch.float16 if _device in "cuda" else torch.float32

_MODEL_ID = "runwayml/stable-diffusion-v1-5"

# 전단지 조건: 1. 하나의 전단지만이 들어와있어야함. 2. 손가락, 물건 등등 불필요한 요소 제거
# 긍정 프롬프트 힌트(단일 전단지, 중앙배치, 정면, 무배경, 여백, 이외 모형 금지)
_COMPOSITION_HINT = (
  ", textless full-bleed A4 poster, pure white background, one large centered icon of the key product from the description (e.g., burger), straight-on not overhead, minimal flat vector, clear silhouette, high contrast, professional flyer, not a mockup, no collage, panels, scene, or props"
)


# 부정 프롬프트(중복, 모형, 사람, 손, 프레임, 콜라주, 텍스트 잡음 ... 제거)
_BASE_NEG = (
  "TEXT, text, letters, words, numbers, logo, watermark, QR code, barcode, collage, panels, multi-page, mockup, frame, border, scene, room, props, overhead, flat lay, perspective, photo, photorealistic, texture, gradient, vignette, heavy shadow, people, hands, low quality, blurry, noise"
)




# 파이프라인 (최초 1회만 로드됨)
pipe: StableDiffusionPipeline | None = None
def _init_pipe() -> StableDiffusionPipeline:
    global pipe
    if pipe is not None:
        return pipe

    pipe = StableDiffusionPipeline.from_pretrained(
        _MODEL_ID,
        torch_dtype=_dtype,
        safety_checker=None,          # ← 안전 필터 해제
        requires_safety_checker=False # ← 안전필터 해제 경고 제거
    ).to(_device)

    # 메모리 최적화
    pipe.enable_attention_slicing()
    try:
        pipe.enable_vae_tiling()
    except Exception:
        pass
    if _device == "cuda":
        try:
            pipe.enable_xformers_memory_efficient_attention()
        except Exception:
            pass
    pipe.set_progress_bar_config(disable=True)
    return pipe

# 입력 검증/정규화
_MIN_SIZE, _MAX_SIZE = 256, 1536
_MIN_STEPS, _MAX_STEPS = 5, 75
_MIN_CFG, _MAX_CFG   = 0.0, 20.0
_MAX_PIXELS          = 1536 * 1024  # 필요시 조정

def _snap64(x: int) -> int:
    return max(_MIN_SIZE, min(_MAX_SIZE, int(round(x / 64) * 64)))

def _normalize(width: int, height: int, steps: int, cfg: float):
    width, height = _snap64(width), _snap64(height)
    if width * height > _MAX_PIXELS:
        scale = ( _MAX_PIXELS / (width * height) ) ** 0.5
        width, height = _snap64(int(width * scale)), _snap64(int(height * scale))
    steps = max(_MIN_STEPS, min(_MAX_STEPS, int(steps)))
    cfg   = max(_MIN_CFG,   min(_MAX_CFG,   float(cfg)))
    return width, height, steps, cfg

# 전단지 생성 함수
def generate_flyer_image(
    prompt: str,
    negative_prompt: str = "",
    width: int = 768,
    height: int = 1024,
    steps: int = 30,
    guidance_scale: float = 7.5,
    seed: int | None = None,
    auto_translate: bool = True,
) -> str:
    """
    이미지를 생성하고 MEDIA_ROOT/flyers/에 저장한 뒤 'flyers/파일명'을 반환.
    """
    p = _init_pipe()

    # 입력 정규화
    width, height, steps, guidance_scale = _normalize(width, height, steps, guidance_scale)

    # 한국어 -> 영어 번역
    if auto_translate and contains_korean(prompt):
        prompt_en = ko_to_en(prompt)
    else:
        prompt_en = prompt

    if auto_translate and negative_prompt and contains_korean(negative_prompt):
        user_neg = ko_to_en(negative_prompt)
    else:
        user_neg = negative_prompt

    # 기본 설정 프롬프트 + 입력 프롬프트 합치기
    full_prompt = f"{prompt_en}{_COMPOSITION_HINT}"
    merged_negative = ", ".join([_BASE_NEG] + ([user_neg] if user_neg else []))

    # 시드 고정
    if seed is None:
        seed = random.randint(0, 2**31 - 1)
    gen_device = "cuda" if _device == "cuda" else "cpu"  # MPS 제너레이터 이슈 회피
    generator = torch.Generator(device=gen_device).manual_seed(seed)


    with torch.inference_mode():
        img = p(
            prompt=full_prompt,
            negative_prompt=merged_negative,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images[0]  # PIL.Image

    # 저장
    subdir = Path(settings.MEDIA_ROOT) / "flyers"
    subdir.mkdir(parents=True, exist_ok=True)
    fname = f"flyer_{uuid.uuid4().hex}.png"
    img.save(str(subdir / fname), format="PNG")

    return f"flyers/{fname}"
