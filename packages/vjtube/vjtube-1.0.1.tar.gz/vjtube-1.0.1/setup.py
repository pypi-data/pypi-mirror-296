from setuptools import setup, find_packages

# Lê o conteúdo do README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vjtube",  # Nome do pacote no PyPI
    version="1.0.1",  # Versão do seu pacote
    author="Felipe Fioruci",
    author_email="felipe.fioruci@vjbots.com.br",
    description="Uma biblioteca para realizar scraping de vídeos do YouTube procurando usos indevidos de sua música.",
    long_description=long_description,  # Usa o conteúdo do README.md
    long_description_content_type="text/markdown",  # Define o formato do README
    url="https://github.com/Fioruci/vjtube",  # URL do repositório do projeto
    packages=find_packages(),  # Encontrará automaticamente os pacotes no diretório
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Requerimentos de versão do Python
    install_requires=[
        "playwright",  # Dependências necessárias
        # Adicione outras dependências necessárias
    ],
)