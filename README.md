# Projeto de Testes com pytest e HTTPX

Este projeto utiliza o `pytest` para testar funcionalidades de uma aplicação, com o uso de **HTTPX** para interagir com APIs e **pytest-html** para gerar relatórios de testes em HTML. Abaixo, explicamos o processo de instalação das dependências e como rodar os testes.

## Pré-requisitos

Antes de começar, você precisará ter o **Python** instalado em sua máquina. A versão recomendada do Python é 3.7 ou superior.

### 1. Instalar o Python

Se você ainda não tem o Python instalado, você pode baixá-lo e instalá-lo a partir do [site oficial do Python](https://www.python.org/downloads/).

### 2. Verificar a versão do Python

Após a instalação, você pode verificar se o Python está instalado corretamente rodando o seguinte comando no terminal ou prompt de comando:

```bash
 python --version
```

### 3. Instalar o PYTEST para os testes
```bash
pip install pytest
```

### 4. Instalar o HTTPX para os testes de API
```bash
pip install httpx
```

### 5. Instalar o pytest-html para gerar os relatórios
```bash
pip install pytest-html
```

## Como gerar os relatórios?
```bash
python -m pytest teste_api.py --html=relatorio.html --template=template.html --css=assets/style.css
```
