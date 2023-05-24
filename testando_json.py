import json

with open('jogadores.json', 'r') as arquivo_json:
    texto = arquivo_json.read()

nome_jogador = "dib"

dicionario = json.loads(texto)

dicionario[nome_jogador] = 2

novo_json = json.dumps(dicionario)

with open('jogadores.json', 'w') as arquivo_json:
    arquivo_json.write(novo_json)

