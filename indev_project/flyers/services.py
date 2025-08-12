# flyers/services.py
from __future__ import annotations

import random, uuid
from pathlib import Path
import math
import torch
from diffusers import StableDiffusionPipeline
from django.conf import settings

# --- 디바이스/DTYPE: CUDA > MPS(Apple) > CPU --- 
# 메모리 최적화 과정(MAC 기준)
_device = (
    "cuda" if torch.cuda.is_available()
    else ("mps" if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()
          else "cpu")
)
_dtype = torch.float16 if _device in ("cuda", "mps") else torch.float32

_MODEL_ID = "runwayml/stable-diffusion-v1-5"

# 최초 1회만 로드
pipe: StableDiffusionPipeline | None = None
def _init_pipe() -> StableDiffusionPipeline:
    global pipe
    if pipe is not None:
        return pipe

    pipe = StableDiffusionPipeline.from_pretrained(
        _MODEL_ID,
        torch_dtype=_dtype,
        safety_checker=None,  # 실서비스면 자체 콘텐츠 필터를 따로 두세요
    ).to(_device)

    # ---- 메모리 최적화 ----
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

# 입력 검증/정규화(width/height를 64의 배수로 되도록 검증 -> 모델 안정적이게됨)
_MIN_SIZE, _MAX_SIZE = 256, 1536
_MIN_STEPS, _MAX_STEPS = 5, 75
_MIN_CFG, _MAX_CFG = 0.0, 20.0
_MAX_PIXELS = 1536 * 1024  # 너무 큰 해상도 방지용(원하면 조정)

def _snap64(x: int) -> int:
    return max(_MIN_SIZE, min(_MAX_SIZE, int(round(x / 64) * 64)))

def _normalize(width: int, height: int, steps: int, cfg: float):
    # 64배수 스냅
    width, height = _snap64(width), _snap64(height)

    # 픽셀 수 과하면 자동 축소
    if width * height > _MAX_PIXELS:
        scale = math.sqrt(_MAX_PIXELS / (width * height))
        width, height = _snap64(int(width * scale)), _snap64(int(height * scale))

    steps = max(_MIN_STEPS, min(_MAX_STEPS, int(steps)))
    cfg   = max(_MIN_CFG,   min(_MAX_CFG,   float(cfg)))
    return width, height, steps, cfg

def generate_flyer_image(
    prompt: str,
    negative_prompt: str = "",
    width: int = 768,
    height: int = 1024,
    steps: int = 30,
    guidance_scale: float = 7.5,
    seed: int | None = None,
) -> str:
    """
    이미지를 생성하고 MEDIA_ROOT/flyers/에 저장한 뒤 'flyers/파일명'을 반환.
    """
    p = _init_pipe()

    # 입력 정규화
    width, height, steps, guidance_scale = _normalize(width, height, steps, guidance_scale)

    # 시드 고정 (재현성)
    if seed is None:
        seed = random.randint(0, 2**31 - 1)
    gen_device = "cuda" if _device == "cuda" else "cpu"  # MPS는 generator 이슈 회피
    generator = torch.Generator(device=gen_device).manual_seed(seed)

    flyer_hint = ", clean layout, poster, flyer, bold typography, high contrast, graphic design, vector elements"
    full_prompt = f"{prompt}{flyer_hint}"

    with torch.inference_mode():
        img = p(
            prompt=full_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images[0]

    subdir = Path(settings.MEDIA_ROOT) / "flyers"
    subdir.mkdir(parents=True, exist_ok=True)
    fname = f"flyer_{uuid.uuid4().hex}.png"
    img.save(str(subdir / fname), format="PNG")

    return f"flyers/{fname}"
