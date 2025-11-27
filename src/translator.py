from ollama import chat
from PySide6.QtCore import QRunnable, QThreadPool

class TranslateWorkerManager():
    def __init__(self):
        self.pool = QThreadPool()
        self.prev_worker = None
    
    def translate(self, word, full_text, on_progress):
        if self.prev_worker:
            self.prev_worker.is_cancelled = True
        
        worker = TranslateWorker(word, full_text, on_progress)
        self.prev_worker = worker
        self.pool.start(worker)        

class TranslateWorker(QRunnable):
    def __init__(self, word, full_text, on_progress):
        super().__init__()
        self.word = word
        self.full_text = full_text
        self.on_progress = on_progress
        self.is_cancelled = False

    def run(self):
        prompt_template = (
            "[{word}]という単語の意味を文脈から推論し、次の形式で回答してください。形式以外の文字は出力しないでください。\n"
            "[{word}]: 単語の意味\n\n"
            "ちなみに、[{word}]は文章全体の中で以下のように使われています。\n"
            "{full_text}"
        )
        prompt = prompt_template.format(
            word=self.word,
            full_text=self.full_text
        )

        response = chat(
            model="gemma3:12b",
            messages=[
                {"role": "system", "content": "あなたは翻訳エンジンです。"},
                {"role": "user", "content": prompt},
            ],
            options={
                "temperature": 0.0,
            },
            stream=True
        )

        result = ""
        for chunk in response:
            if self.is_cancelled:
                break
            result += chunk["message"]["content"]
            self.on_progress(result)