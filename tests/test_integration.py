import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validators.validador import senha_valida


def sistema_completo(senha):
    return "Senha válida" if senha_valida(senha) else "Senha inválida"


def test_sistema_com_senha_valida():
    senha = "Segura1!"
    assert sistema_completo(senha) == "Senha válida"


def test_sistema_com_senha_invalida():
    senha = "fraca"
    assert sistema_completo(senha) == "Senha inválida"
