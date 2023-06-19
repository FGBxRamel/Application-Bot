import json
import os


class Translator():
    def __init__(self):
        self._load_translations()

    def _load_translations(self) -> None:
        self._translations = {}
        for file in os.listdir("translations"):
            with open(f"translations/{file}", "r") as f:
                self._translations[file.split(".")[0]] = json.load(f)

    def translate(self, lang: str, key: str) -> str:
        if not lang in self._translations:
            lang = "en"
        if not key in self._translations[lang]:
            return key
        return self._translations[lang][key]
