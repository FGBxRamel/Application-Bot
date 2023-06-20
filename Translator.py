import json


class Translator():
    def __init__(self, lang: str = "en"):
        self._lang = lang
        self._load_translation()

    def _load_translation(self) -> None:
        self._translations = {}
        with open(f"translations/{self._lang}.json", "r", encoding="utf8") as f:
            self._translations = json.load(f)

    def translate(self, key: str) -> str:
        if not key in self._translations:
            return key
        return self._translations[key]
