from GHOST.codigo.functions import *
Saudacao()
comandos = {
    "nex": {
        "palavras": ["nex","nexi","nexes","néquisis","ness","nexus"],
        "funcao": Nex
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
    },
    "terminal":{
        "palavras":["terminal","terminau","termi"],
        "funcao": terminal
    },
    "processos":{
        "palavras":["processo","processos"],
        "funcao": processos
    },
    "estudos":{
        "palavras":["estudo","estudos"],
        "funcao": estudos
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
