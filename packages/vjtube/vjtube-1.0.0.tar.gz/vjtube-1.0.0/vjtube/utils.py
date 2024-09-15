import re

def sanitize_filename(filename: str) -> str:
    """
    Remove caracteres inválidos para salvar arquivos.

    :param filename: Nome do arquivo a ser sanitizado.
    :return: Nome do arquivo sem caracteres inválidos.
    """
    return re.sub(r'[\\/*?:"<>|]', "", filename)
