from setuptools import setup, find_packages

setup(
    name="meupacote_renato",  # Nome único do pacote no PyPI
    version="0.1.0",   # Versão inicial do pacote
    packages=find_packages(),  # Encontra automaticamente subpacotes
    install_requires=[
        "requests",         # Sempre instala a versão mais atual
        "numpy",            # Sempre instala a versão mais atual
        "pandas",           # Sempre instala a versão mais atual
        "scikit-learn",     # Sempre instala a versão mais atual
    ],
    author="renato_snp",
    author_email="renatoguitarblues@gmail.com",
    description="Uma descrição do seu pacote",
    long_description=open("README.md").read(),  # Carregar descrição do README
    long_description_content_type="text/markdown",  # Tipo de conteúdo
    url="https://github.com/seuusuario/meupacote",  # URL do projeto (GitHub, etc.)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Versão mínima do Python suportada
)
