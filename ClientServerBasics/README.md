# ClientServerBasics — servidor de processamento de texto

Extensão do código base cliente/servidor com sockets TCP (Cap. 2, Fig. 2.3). O servidor deixou de apenas devolver a mensagem com `*` e passou a oferecer várias operações de processamento de texto que o cliente pode chamar remotamente.

## O que foi acrescentado

1. **Processamento no servidor:** cada requisição é interpretada e as operações pedidas são executadas sobre o texto enviado.
2. **Mais de uma funcionalidade por requisição:** o cliente envia uma lista de operações em uma única requisição e recebe todos os resultados em uma única resposta.

## Arquivos

| Arquivo | Função |
|---|---|
| `constCS.py` | `HOST` e `PORT` usados por cliente e servidor |
| `server.py` | servidor: recebe requisições, executa as operações e responde |
| `client.py` | cliente: monta a requisição, envia e imprime os resultados |

## Operações oferecidas

| Operação | Resultado |
|---|---|
| `upper` / `lower` | texto em maiúsculas / minúsculas |
| `reverse` | texto invertido |
| `length` | número de caracteres |
| `words` | número de palavras |
| `vowels` | número de vogais |
| `palindrome` | `true`/`false` (ignora espaços, pontuação e maiúsculas) |
| `sha256` | hash SHA-256 do texto |

## Protocolo

Mensagens em JSON, uma por linha (`\n`), o que evita problemas de fronteira de mensagem no TCP.

```json
// requisição
{"text": "Hello World", "ops": ["upper", "reverse", "words"]}

// resposta
{"results": {"upper": "HELLO WORLD", "reverse": "dlroW olleH", "words": 2}, "errors": {}}
```

Operações desconhecidas não derrubam a requisição: aparecem em `errors`, e as demais são executadas normalmente. Requisições mal formadas recebem uma resposta de erro.

## Como executar

Requer Python 3. Em um terminal:

```bash
python server.py
```

Em outro terminal:

```bash
python client.py "Hello World" upper reverse words
python client.py                      # exemplo padrão
```

Exemplo de saída:

```
Texto enviado: "Hello World"
  upper       -> HELLO WORLD
  reverse     -> dlroW olleH
  words       -> 2
```

Por padrão `constCS.py` usa `127.0.0.1` (teste na mesma máquina). Para rodar em máquinas diferentes, coloque no `HOST` o IP da máquina do servidor, nos dois lados, e libere a porta `5678`.

## Observações

- O servidor atende um cliente por vez, como no código base, mas aceita várias requisições na mesma conexão.
