import detectlanguage
import cattr
import json

from dataclasses import dataclass

SUPORTED_LANGUAGES_JSON_FILE = r".\data\supported_languages.json"

@dataclass
class Language:
    code: str
    name: str

@dataclass
class LanguagePair:
    src: Language
    dst: Language

@dataclass
class LanguageDetection:
    isReliable: bool
    confidence: float
    language: str

class Languages:
    def __init__(self):
        pass

    @staticmethod
    def set_api_key(key: str):
        detectlanguage.configuration.api_key = key

    @staticmethod
    def detect(text: str):
        converter = cattr.Converter()
        return [converter.structure(item, LanguageDetection) for item in detectlanguage.detect(text)]

    @staticmethod
    def load_supported():
        with open(SUPORTED_LANGUAGES_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            converter = cattr.Converter()
            return [converter.structure(item, Language) for item in data]
