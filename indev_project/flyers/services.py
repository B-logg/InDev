# flyers/services.py
from __future__ import annotations

import random, uuid, math
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline
from django.conf import settings

# --- 디바이스/DTYPE: CUDA > MPS(Apple) > CPU ---
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

    # safety_checker=None 해제 -> 기본 안전 필터 ON(실서비스화를 위함)
    pipe = StableDiffusionPipeline.from_pretrained(
        _MODEL_ID,
        torch_dtype=_dtype,
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


# ---- 입력 검증/정규화 ----
_MIN_SIZE, _MAX_SIZE = 256, 1536
_MIN_STEPS, _MAX_STEPS = 5, 75
_MIN_CFG, _MAX_CFG = 0.0, 20.0
_MAX_PIXELS = 1536 * 1024  # 과도한 해상도 방지(필요시 조정)

def _snap64(x: int) -> int:
    return max(_MIN_SIZE, min(_MAX_SIZE, int(round(x / 64) * 64)))

def _normalize(width: int, height: int, steps: int, cfg: float):
    # 64배수 스냅
    width, height = _snap64(width), _snap64(height)

    # 픽셀 수 과하면 자동 축소
    if width * height > _MAX_PIXELS:
        scale = ( _MAX_PIXELS / (width * height) ) ** 0.5
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
    NSFW가 감지되면 ValueError를 발생시켜 호출 측(뷰)에서 400 처리하도록 함.
    """
    p = _init_pipe()

    # 입력 정규화
    width, height, steps, guidance_scale = _normalize(width, height, steps, guidance_scale)

    # 시드 고정 (재현성)
    if seed is None:
        seed = random.randint(0, 2**31 - 1)
    # MPS는 torch.Generator(device="mps") 이슈가 있어 CPU를 사용
    gen_device = "cuda" if _device == "cuda" else "cpu"
    generator = torch.Generator(device=gen_device).manual_seed(seed)

    flyer_hint = ", clean layout, poster, flyer, bold typography, high contrast, graphic design, vector elements"
    full_prompt = f"{prompt}{flyer_hint}"

    with torch.inference_mode():
        out = p(
            prompt=full_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            generator=generator,
            # output_type="pil"  # 기본 PIL, 명시해도 됨
        )
        # 안전 필터 결과 확인
        nsfw_flags = getattr(out, "nsfw_content_detected", None)
        if nsfw_flags and any(bool(f) for f in nsfw_flags):
            # 여기서 블러/대체 이미지 저장 대신 에러로 막음
            raise ValueError("NSFW content detected by safety checker")

        img = out.images[0]  # PIL.Image

    # 저장
    subdir = Path(settings.MEDIA_ROOT) / "flyers"
    subdir.mkdir(parents=True, exist_ok=True)
    fname = f"flyer_{uuid.uuid4().hex}.png"
    img.save(str(subdir / fname), format="PNG")

    return f"flyers/{fname}"