from setuptools import setup, find_packages

# Leitura do README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Leitura do requirements.txt
with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setup(
    name="ozzy_image_processing",  # nome do pacote
    version="0.0.3",  # versão do pacote
    author="Ozzy Azevedo",
    author_email="ozzysp@icloud.com",
    description="Package to process images using Python",
    long_description=long_description,  # conteúdo do README
    long_description_content_type="text/markdown",  # formato do README
    url="https://github.com/ozzysp/image-processing-package",  # link do projeto
    packages=find_packages(),  # localizar pacotes no projeto
    install_requires=requirements,  # instalar as dependências
    python_requires='>=3.8',  # versão mínima do Python
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
)
