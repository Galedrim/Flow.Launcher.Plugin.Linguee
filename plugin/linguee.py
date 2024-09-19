
from flox import Flox
from typing import List

from languages import Languages, LanguagePair
from icons import Icon
from translation import Translations, Word

class Linguee(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        first_setting = self.settings.get('first_language')
        second_setting = self.settings.get('second_language')

        self.first_lang= next((lang for lang in Languages.load_supported() if lang.name == first_setting), None)
        self.second_lang = next((lang for lang in Languages.load_supported() if lang.name == second_setting), None)

        self.api_key = self.settings.get('api_key')
        if self.api_key:
            Languages.set_api_key(self.api_key)

        self.show_less_common = self.settings.get('show_less_common')

    def results(self, query: str):
        if not self.api_key:
            self.key_missing_results()
            return self._results

        if not query:
            self.query_missing_results()
            return self._results

        data = next((lang for lang in Languages.detect(query) if lang.isReliable), None)
        detected_lang = next((lang for lang in Languages.load_supported() if lang.code == data.language), None) if data else None
        if not data or not detected_lang:
            language_pair = LanguagePair(self.first_lang, self.second_lang)
        else:
            language_pair = LanguagePair(detected_lang, self.second_lang if detected_lang == self.first_lang else self.first_lang)

        words = Translations.load(query, language_pair)
        self.translation_results(words, language_pair)
        return self._results

    def key_missing_results(self):
        self.add_item(
            title="Please set detectlanguage API key in settings",
            subtitle="You can get a free API key from detectlanguage.com",
        )

    def query_missing_results(self):
        self.add_item(
            title="Please enter a word to translate"
        )

    def translation_results(self, words: List[Word], language_pair: LanguagePair):
        for word in words:
            self.add_item(
                title=f"{word.text} [{word.pos}]",
                icon=f"{Icon.get_icon(language_pair.src.name)}",
            )

            for translation in word.translations:
                if translation.featured or (not translation.featured and self.show_less_common):
                    self.add_item(
                        title=f"--> {translation.text} [{translation.pos}]",
                        subtitle=f"{' / '.join([example.dst for example in translation.examples])}",
                        icon=f"{Icon.get_icon(language_pair.dst.name)}",
                    )

    def query(self, query: str):
        self.results(query)


