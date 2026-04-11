from GHOST.codigo.functions import *
Saudacao()
comandos = {
    "ghost": {
        "palavras": ["fala","mano","gosti","ghoste","goste","gousti","oste"],
        "funcao": ghost
    },
    "horas": {
        "palavras": ["hora","horas","horario"],
        "funcao": Horas
    },
    "dia": {
        "palavras":["dia","hoje","data"],
        "funcao": data
    },
    "youtube": {
        "palavras": ["youtube","youtubi","abrir youtube"],
        "funcao": abrirYoutube
    },
    "pesquisa":{
        "palavras":["pesquisar","pesquisa","google","internet","net"],
        "funcao": Pesquisa
    },
    "voce":{
        "palavras":["criou","crio"],
        "funcao":quem_sou
    },
    "desligar":{
        "palavras":["desligar","desliga"],
        "funcao": desligar
    }
}
while True:
    comando = normalizar(capture_audio())

    if not comando or not comando.strip():
        continue
    executado = False
    comando = comando.lower()
    for item in comandos.values():
        if any(palavra in comando for palavra in item["palavras"]):
            item["funcao"]()
            executado = True
            break
        if executado:
            break

    if not executado:
        resposta_desconhecida(comando)
