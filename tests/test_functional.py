import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validators.validador import senha_valida


def test_senha_valida_com_senha_forte():
    senha = "Abcdef1!"
    assert senha_valida(senha) == True


def test_senha_valida_sem_maiuscula():
    senha = "abcdef1!"
    assert senha_valida(senha) == False


def test_senha_valida_sem_minuscula():
    senha = "ABCDEF1!"
    assert senha_valida(senha) == False


def test_senha_valida_sem_numero():
    senha = "Abcdefgh!"
    assert senha_valida(senha) == False


def test_senha_valida_sem_caractere_especial():
    senha = "Abcdef12"
    assert senha_valida(senha) == False
