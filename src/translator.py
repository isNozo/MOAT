from abc import ABC, abstractmethod

class Translator(ABC):
    @abstractmethod
    def translate(self, text: str) -> str:
        pass

def create_translator(kind: str) -> Translator:
    if kind == "argos":
        return ArgosTranslator()
    else:
        raise ValueError(f"Unknown translator type: {kind}")

class ArgosTranslator:
    def __init__(self):
        from argostranslate import package
        from argostranslate.translate import translate as argos_translate

        self._argos_translate = argos_translate
        self.from_code = "en"
        self.to_code = "ja"

        # Download and install Argos Translate package
        package.update_package_index()
        available_packages = package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == self.from_code and x.to_code == self.to_code, available_packages
            )
        )
        package.install_from_path(package_to_install.download())

    def translate(self, text):
        return self._argos_translate(text, self.from_code, self.to_code)
