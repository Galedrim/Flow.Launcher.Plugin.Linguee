import os

ICONS_DIR = r".\images\flags"

class Icon:
    @staticmethod
    def get_icon(language: str):
        found_file = None

        for files in os.listdir(ICONS_DIR):
            if language.lower() in files.lower():
                found_file = os.path.join(ICONS_DIR, files)
                break
        return found_file
