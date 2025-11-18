from ..translator import create_translator

if __name__ == "__main__":
    argos_translator = create_translator("argos")
    print(argos_translator.translate("Hello, world! This is a test of the Argos translation system."))

    ollama_translator = create_translator("ollama")
    print(ollama_translator.translate("Hello, world! This is a test of the Ollama translation system."))
