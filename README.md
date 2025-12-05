# MOAT - Mouse OCR & AI Translator

MOATは以下の特徴を持つOCR翻訳ツールです。

- 任意のアプリケーションの画面をリアルタイムにキャプチャしてテキストを抽出
- テキストにマウスをホバーすると単語の意味をポップアップで表示

以下の環境で動作することを確認しています。

- Windows11
- NVIDIA GeForce RTX 4060 Ti (16GB)

# 使用方法
## ステップ１
ツール本体を以下からダウンロードしてください。(OCRライブラリがでかいので展開すると5GBくらいになります)

https://drive.google.com/file/d/1JyMUxZPpJj_GVX6AT1lYLH9n7JDR3F87/view?usp=sharing

## ステップ２
翻訳にローカルLLMを利用します。以下のサイトからollamaをインストールしてください。

https://ollama.com/

## ステップ３

ollamaを実行した状態でMOATを実行してください。ドロップダウンからキャプチャするウィンドウを選択し、再生ボタンでキャプチャ開始します。

# 開発者向け環境構築方法

Run the following commands:
```
> pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
> pip install Pyside6 pywin32 windows_capture setuptools paddleocr==3.3.1 ollama
```

Note: The paddlepaddle-gpu version must match your CUDA version. Please refer to the [official installation guide](https://www.paddlepaddle.org.cn/en/install/quick?docurl=/documentation/docs/en/develop/install/pip/windows-pip_en.html).

```
> ollama run gemma3:12b
> python .\src\main.py
```