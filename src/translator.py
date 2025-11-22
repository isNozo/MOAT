from abc import ABC, abstractmethod

class Translator(ABC):
    @abstractmethod
    def translate(self, text: str) -> str:
        pass

def create_translator(kind: str) -> Translator:
    if kind == "argos":
        return ArgosTranslator()
    elif kind == "ollama":
        return OllamaTranslator()
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

class OllamaTranslator(Translator):
    def __init__(self, model: str = "gemma3:12b"):
        import ollama

        self.ollama = ollama
        self.model = model

        self.prompt_template = (
            "[{word}]というテキストの意味を推論し、次の形式で回答してください。形式以外の文字は出力しないでください。\n"
            "{word}:<意味>\n\n"
            "ちなみに、[{word}]は文章全体の中で以下のように使われています。\n"
            "{full_text}"
        )

    def translate(self, word: str, full_text: str) -> str:
        prompt = self.prompt_template.format(
            word=word,
            full_text=full_text
        )

        response = self.ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "あなたは翻訳エンジンです。"},
                {"role": "user", "content": prompt},
            ],
            options={
                "temperature": 0.0,
            }
        )

        return response["message"]["content"].strip()