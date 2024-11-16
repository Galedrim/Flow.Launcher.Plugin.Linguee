
from flox import Flox
from typing import List

from languages import Languages, LanguagePair
from icons import Icon
from translation import Translations, Word, ErrorResponse

class Linguee(Flox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_key = self.settings.get('api_key')
        if self.api_key:
            Languages.set_api_key(self.api_key)

        first_setting = self.settings.get('main_language')
        second_setting = self.settings.get('secondary_language')

        self.first_lang= next((lang for lang in Languages.load_supported() if lang.name == first_setting))
        self.second_lang = next((lang for lang in Languages.load_supported() if lang.name == second_setting))

        self.show_less_common_translation = self.settings.get('show_less_common_translation')

    def results(self, query: str):
        if not self.api_key:
            self.key_missing_results()
            return self._results

        if not query:
            self.query_missing_results()
            return self._results

        data = []
        for lang in Languages.detect(query):
            data.append(lang)

        if not data:
            self.error_language_results()
            return self._results

        language_pair = None
        for lang in data:
            if lang.language == self.first_lang.code and lang.confidence > 3.0:
                language_pair = LanguagePair(self.first_lang, self.second_lang)
                break
            elif lang.language == self.second_lang.code and lang.confidence > 3.0:
                language_pair = LanguagePair(self.second_lang, self.first_lang)
                break

        if language_pair:
            results = Translations.load(query, language_pair)
            if isinstance(results, ErrorResponse):
                self.error_api_results(results.message)
            else:
                self.translation_results(results, language_pair)
        else:
            self.error_language_used_results()

        return self._results

    def key_missing_results(self):
        self.add_item(
            title="Please set detectlanguage API key in settings",
            subtitle="You can get a free API key from detectlanguage.com",
        )

    def query_missing_results(self):
        self.add_item(
            title="Please enter a word to translate with Linguee"
        )

    def error_language_results(self):
        self.add_item(
            title="The detection of the language has failed."
        )

    def error_language_used_results(self):
        self.add_item(
            title="The word could not be translated in the configured languages."
        )

    def error_api_results(self, message: str):
        self.add_item(
            title=message
        )

    def translation_results(self, words: List[Word], language_pair: LanguagePair):
        for word in words:
            self.add_item(
                title=f"{word.text} [{word.pos}]",
                icon=f"{Icon.get_icon(language_pair.src.name)}",
            )

            for translation in word.translations:
                if translation.featured or (not translation.featured and self.show_less_common_translation):
                    self.add_item(
                        title=f"--> {translation.text} [{translation.pos}]",
                        subtitle=f"{' / '.join([example.dst for example in translation.examples])}",
                        icon=f"{Icon.get_icon(language_pair.dst.name)}",
                    )

    def query(self, query: str):
        self.results(query)


