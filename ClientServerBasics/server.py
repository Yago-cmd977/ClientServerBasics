"""Servidor (código base ClientServerBasics, estendido).

1. Processa a requisição: executa operações sobre um texto recebido.
2. Aceita várias operações diferentes na mesma requisição.

Protocolo: uma requisição por linha, em JSON.
  Requisição: {"text": "Hello World", "ops": ["upper", "reverse", "words"]}
  Resposta:   {"results": {...}, "errors": {...}}
"""
import hashlib
import json
from socket import *
from constCS import *

VOGAIS = set("aeiouAEIOUáéíóúâêôãõàÁÉÍÓÚÂÊÔÃÕÀ")


def palindromo(t):
    limpo = [c.lower() for c in t if c.isalnum()]
    return limpo == limpo[::-1]


# Funcionalidades oferecidas aos clientes
OPERACOES = {
    "upper": lambda t: t.upper(),
    "lower": lambda t: t.lower(),
    "reverse": lambda t: t[::-1],
    "length": lambda t: len(t),
    "words": lambda t: len(t.split()),
    "vowels": lambda t: sum(1 for c in t if c in VOGAIS),
    "palindrome": palindromo,
    "sha256": lambda t: hashlib.sha256(t.encode()).hexdigest(),
}


def processar(linha):
    """Interpreta a requisição e executa cada operação pedida."""
    try:
        req = json.loads(linha.decode())
        texto, ops = req["text"], req["ops"]
        if not isinstance(texto, str) or not isinstance(ops, list):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        return {"results": {}, "errors": {"requisicao": 'formato esperado: {"text": str, "ops": [str, ...]}'}}

    resultados, erros = {}, {}
    for op in ops:
        if op in OPERACOES:
            resultados[op] = OPERACOES[op](texto)
        else:
            erros[op] = "operação desconhecida (disponíveis: " + ", ".join(OPERACOES) + ")"
    return {"results": resultados, "errors": erros}


s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
print(f"Servidor ouvindo em {HOST}:{PORT}")

while True:  # atende um cliente por vez
    (conn, addr) = s.accept()  # retorna novo socket e endereço do cliente
    print("Cliente conectado:", addr)
    with conn, conn.makefile("rb") as entrada:
        for linha in entrada:  # uma requisição por linha
            print("Requisição:", linha.decode().strip())
            resposta = processar(linha)  # processa a requisição
            conn.sendall((json.dumps(resposta, ensure_ascii=False) + "\n").encode())
    print("Cliente desconectado:", addr)
