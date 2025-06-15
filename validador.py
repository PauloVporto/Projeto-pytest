
import re

def senha_valida(senha):
    if not isinstance(senha, str):
        raise TypeError("Senha deve ser uma string")

    if len(senha) < 8:
        return False
    if not re.search(r"[A-Z]", senha):
        return False
    if not re.search(r"[a-z]", senha):
        return False
    if not re.search(r"\d", senha):
        return False
    if not re.search(r"[!@#$%^&*()\-_=+{}\[\]:;,.<>?/]", senha):
        return False

    return True
