# MOAT - Mouse OCR & AI Translator

## Installation
Requirements:
- Ollama 0.12.11

Run the following commands:
```
> pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
> pip install Pyside6 pywin32 windows_capture setuptools paddleocr==3.3.1
```

Note: The paddlepaddle-gpu version must match your CUDA version. Please refer to the [official installation guide](https://www.paddlepaddle.org.cn/en/install/quick?docurl=/documentation/docs/en/develop/install/pip/windows-pip_en.html).

```
> ollama run llama3
> python .\src\main.py
```