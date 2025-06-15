# 🔐 Validador de Senhas com Testes Automatizados

Este projeto implementa uma função de validação de senhas com base em critérios de segurança, e utiliza **pytest** para testes automatizados — tanto para casos válidos quanto inválidos.

---

## 🚀 Funcionalidade

A função `senha_valida` verifica se uma senha atende aos seguintes critérios:

- ✅ Pelo menos 8 caracteres  
- ✅ Pelo menos uma letra maiúscula  
- ✅ Pelo menos uma letra minúscula  
- ✅ Pelo menos um número  
- ✅ Pelo menos um caractere especial (`@`, `#`, `$`, `%`, etc.)

---

## 📁 Estrutura do Projeto

```
Projeto-pytest-main/
├── validador.py           # Função principal de validação
├── test_validador.py      # Testes com pytest
├── .github/
│   └── workflows/
│       └── pytest.yml     # Pipeline de CI com GitHub Actions
└── README.md              # Este arquivo
```

---

## 🧪 Executando os Testes

### 🔧 Localmente

1. Crie um ambiente virtual (opcional):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instale as dependências:

```bash
pip install pytest
```

3. Execute os testes:

```bash
pytest
```

---

### ☁️ Via GitHub Actions

Este projeto possui um pipeline de **Integração Contínua (CI)** com GitHub Actions:

- Executa testes automaticamente em cada `push` ou `pull request` para a branch `main`.
- Gera dois relatórios:
  - `report.xml` (formato JUnit)
  - `result.txt` (saída legível do pytest)
- Os relatórios podem ser baixados como artefatos na aba **Actions** do GitHub.

---

## 🧠 Exemplos de Testes

```python
senha_valida("Senha@123")      # ✅ True
senha_valida("abc")            # ❌ False
senha_valida(123456)           # ❌ TypeError esperado
```

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT]

---

## 💡 Autor

Desenvolvido por Paulo Vicente de Carvalho Porto.
