from abc import ABC, abstractmethod

class Translator(ABC):
    @abstractmethod
    def translate(self, text: str) -> str:
        pass

def create_translator(kind: str) -> Translator:
    if kind == "ollama":
        return OllamaTranslator()
    else:
        raise ValueError(f"Unknown translator type: {kind}")

class OllamaTranslator(Translator):
    def __init__(self, model: str = "gemma3:12b"):
        import ollama

        self.ollama = ollama
        self.model = model

        self.prompt_template = (
            "[{word}]という単語の意味を文脈から推論し、次の形式で回答してください。形式以外の文字は出力しないでください。\n"
            "[{word}]: 単語の意味\n\n"
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