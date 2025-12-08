# MOAT - Mouse OCR & AI Translator

MOATは以下の特徴を持つOCR翻訳ツールです。

- 任意のアプリケーションの画面をリアルタイムにキャプチャしてテキストを抽出
- テキストにマウスをホバーすると単語の意味をポップアップで表示

以下の環境で動作することを確認しています。

- Windows11
- NVIDIA GeForce RTX 4060 Ti (16GB)

# 使用方法
## ステップ１
ツール本体を以下からダウンロードしてください。

## ステップ２
翻訳にローカルLLMを利用します。以下のサイトからollamaをインストールしてください。

https://ollama.com/

## ステップ３

ollamaを実行した状態でMOATを実行してください。ドロップダウンからキャプチャするウィンドウを選択し、再生ボタンでキャプチャ開始します。

※最初の実行だけMOATを管理者権限で実行する必要あり（Win11に標準インストールされているSnippingToolのOCRライブラリをコピーするため）

# 開発者向け環境構築方法

以下のパッケージをインストールしてください。
```
> pip install Pyside6 pywin32 windows_capture oneocr ollama pyinstaller
```

ollamaを実行した状態で以下を実行してください。

```
> python.exe .\src\main.py
```

以下のコマンドでdistディレクトリに配布用の実行ファイルが生成されます。

```
> pyinstaller.exe --clean .\src\main.py
```