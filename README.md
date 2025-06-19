# Projeto de Testes com pytest

Este projeto utiliza o `pytest` para testar funcionalidades de uma aplicação, com o uso de **HTTPX** para interagir com APIs, **pytest-reporter-html** para gerar relatórios de testes em HTML e **Selenium** para interagir com interfaces. Abaixo, explicamos o processo de instalação das dependências e como rodar os testes.

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

### 5. Instalar o selenium para os testes de UI
```bash
pip install selenium
```

### 6. Instalar o pytest-reporter-html para gerar os relatórios
```bash
pip install pytest-reporter-html
```
### 7. Instalar o pytest-metadata para auxiliar nos dados do relatório
```bash
pip install pytest-metadata
```
### 8. Instalar o pytest-metadata para auxiliar nos dados do relatório
```bash
pip install pytest-metadata
```

## Como rodar os testes?
```bash
pytest Testes_Pytest.py
```
Os relatórios são gerados automaticamente após os testes finalizarem
