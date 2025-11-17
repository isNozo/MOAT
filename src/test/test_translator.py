from ..translator import create_translator

if __name__ == "__main__":
    translator = create_translator("argos")

    print(translator.translate("Hello, world! This is a test of the Argos translation system."))
