from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

setup(
    name="validador_docs",
    version="0.0.1",
    author='edmaker89',
    author_email="edmaker@gmail.com",
    description="Validators Brasilian documents",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edmaker89/validator_documents_package",
    packages=find_packages(),
    install_requires=[],  # Lista de dependências se necessário, aqui você pode remover o requirements.txt
    python_requires=">=3.12",
    setup_requires=['pytest-runner'],  # Opcional, se for usar pytest para testar
    tests_require=['pytest'],  # Se você for usar pytest
)
