from __future__ import annotations
import re
from typing import Optional
from transformers import MarianMTModel, MarianTokenizer
import torch

_HANGUL_RE = re.compile(r'[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7A3]')

_trans_tok: Optional[MarianTokenizer] = None
_trans_mod: Optional[MarianMTModel] = None
_MODEL_NAME = "Helsinki-NLP/opus-mt-ko-en"

def _init_translator():
    global _trans_tok, _trans_mod
    if _trans_tok and _trans_mod:
        return
    _trans_tok = MarianTokenizer.from_pretrained(_MODEL_NAME)
    _trans_mod = MarianMTModel.from_pretrained(_MODEL_NAME)

def contains_korean(text: str) -> bool: # 한글 포함 유무 판독
    return bool(text and _HANGUL_RE.search(text))

def ko_to_en(text: str) -> str:
    if not text or not contains_korean(text):
        return text
    _init_translator()

    inputs = _trans_tok([text], return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        gen = _trans_mod.generate(**inputs, max_length=512, num_beams=4)
    return _trans_tok.decode(gen[0], skip_special_tokens=True)
