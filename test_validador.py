
from validador import senha_valida
import pytest


def test_senha_valida():
    assert senha_valida("Senha@123") is True
    assert senha_valida("Abcdef@1") is True
    assert senha_valida("Xpto$2024") is True


def test_senha_curta():
    assert senha_valida("Abc@1") is False
    assert senha_valida("S@1a") is False


def test_sem_maiuscula():
    assert senha_valida("senha@123") is False


def test_sem_minuscula():
    assert senha_valida("SENHA@123") is False


def test_sem_numero():
    assert senha_valida("Senha@abc") is False


def test_sem_caractere_especial():
    assert senha_valida("Senha1234") is False


def test_tudo_invalido():
    assert senha_valida("abc") is False
    assert senha_valida("") is False


def test_tipo_invalido():
    import pytest
    with pytest.raises(TypeError):
        senha_valida(12345678)

    with pytest.raises(TypeError):
        senha_valida(None)

    with pytest.raises(TypeError):
        senha_valida(["Senha@123"])
