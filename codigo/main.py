from functions import *
Saudacao()
comandos = {
    "nex": {
        "palavras": ["nex","nexi","nexes","néquisis","ness","nexus","fala"],
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
        "palavras":["quem","você é"],
        "funcao":quem_sou
    },
    "desligar":{
        "palavras":["desligar","desliga"],
        "funcao": desligar
    },
    "terminal":{
        "palavras":["terminal"],
        "funcao": terminal
    },
    "processos":{
        "palavras":["processo","processos"],
        "funcao": processos
    },
    "estudos":{
        "palavras":["estudo","estudos"],
        "funcao": estudos
    },
    "time":{
        "palavras":["taime","time","taimi","cronômetro"],
        "funcao": Timer
    },
    "estado":{
        "palavras":["estado","maquina","estado"],
        "funcao": estadoAtual
    }
}
timeout = 20 # tempo que ele fica aguardando comandos
ativamento = ["nex","nexi","néquisis","ness","nexus","fala nex"]
ativo = False # entra em estado de escuta de comandos
tempo_ativo = 0 # tempo em que está escutando comando que se renova a cada comando executado

while True:
    monitoramento()
    comando = escutar_passivo()

    if not comando or not comando.strip():
        if ativo and (time.time() - tempo_ativo > timeout):
            ativo = False
            print("[*] Modo de escuta [*]")
            fala("Voltando ao modo de escuta retrô.")
        continue

    comando = comando.lower()
    # modo de escuta passiva, sem execução
    if not ativo:
        if any(palavra in comando for palavra in ativamento):
            ativo = True
            tempo_ativo = time.time()
            Nex()
        continue # ignora quando não tiver as palavras do ativamento

    # Modo de ativo
    if time.time() - tempo_ativo > timeout:
        ativo = False
        print("[*] Modo de escuta [*]")
        continue

    tempo_ativo = time.time()

    # executa os comandos
    executado = False
    for item in comandos.values():
        if any(palavra in comando for palavra in item["palavras"]):
            item["funcao"]()
            executado = True
            break

    if not executado:
        resposta_desconhecida(comando)
