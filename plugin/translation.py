import requests
import cattr

from languages import LanguagePair
from dataclasses import dataclass, field
from typing import List

@dataclass
class Example:
    src: str
    dst: str

@dataclass
class Translation:
    featured: bool
    text: str
    pos: str
    examples: List[Example] = field(default_factory=list)

@dataclass
class Word:
    featured: bool
    text: str
    pos: str
    forms: List[str] = field(default_factory=list)
    translations: List[Translation] = field(default_factory=list)

@dataclass
class ErrorResponse:
    message: str

class Translations:
    def __init__(self):
        pass

    @staticmethod
    def load(word: str, languagePair: LanguagePair) -> List[Word]:
        api_root = "https://linguee-api.fly.dev/api/v2"
        resp = requests.get(f"{api_root}/translations", params={"query": word, "src": languagePair.src.code, "dst": languagePair.dst.code})
        converter = cattr.Converter()
        if 'message' in resp.json():
            return converter.structure(resp.json(), ErrorResponse)
        else:
            return [converter.structure(item, Word) for item in resp.json()]