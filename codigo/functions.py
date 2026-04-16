import speech_recognition as recon
from piper import PiperVoice #classe que controla a voz
import numpy as np # mais low level para converter bytes
import threading
import datetime
import subprocess
import psutil
import time
import os

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "pt_BR-cadu-medium.onnx")

voice = PiperVoice.load(MODEL_PATH)

micro = recon.Recognizer()

espera_de_fala = threading.Lock()


#controle de escuta evitando o bug de ficar ouvindo e executando varias vezes

falando = False

# captura de audio
def capture_audio():
    # inicia a escuta

    with recon.Microphone() as mic:
        micro.adjust_for_ambient_noise(mic, duration=0.5)
        print("Aguardando sua fala... ")

        try:
            audio = micro.listen(mic,timeout=5,phrase_time_limit=6)
            comando = micro.recognize_google(audio,language='pt-BR')
            return comando.lower().strip()
        except recon.WaitTimeoutError:
            return None
        except recon.UnknownValueError:
            return None
        except recon.RequestError as e:
            print(f"Erro interno {e}")
            return None

def escutar(max_tentativas=3):
    global falando
    if falando:
        return None

    for _ in range(max_tentativas):
        comando = normalizar(capture_audio())

        if comando:
            return comando.lower().strip()

        fala("Não entendi, pode repetir?")

    fala("Não consegui ouvir você.")
    return None

def escutar_passivo():
    # escuta quieto, sem ficar falando para repetir -_-
    global falando
    if falando:
        return None
    return normalizar(capture_audio())

def normalizar(texto):
    if not texto:
        return None
    return texto.lower().strip().lstrip(".")

# converte o texto para fala
def fala(texto):
    global falando
    with espera_de_fala:
        falando = True
        try:
            som = subprocess.Popen(["aplay", "-f", "S16_LE", "-r", "22050", "-c", "1"], stdin=subprocess.PIPE)
            for pedaco in voice.synthesize(texto):
                # converte float → int16 → bytes
                audio = (pedaco.audio_float_array * 32767).astype(np.int16)
                som.stdin.write(audio.tobytes())

            som.stdin.close()
            som.wait()
        finally:
            falando = False

def Saudacao():
    horario = datetime.datetime.now().hour
    if 6 <= horario < 12:
        print("Bom dia retr0, seja bem vindo!")
        fala('Bom dia retrô, Como você ta?, acordou cedo hoje ')
    elif 12 <= horario < 18:
        print("Boa tarde retr0, Como voce está?")
        fala("Boa tarde retrô, como voce tá?, Vamos fazer o que hoje?")
    else:
        print("Boa noite retr0, como ce ta?")
        fala("Boa noite retrô, como voçê está?, no que te ajudo hoje?")

def resposta_desconhecida(comando):
    print("Não conheço esse comando ou instrução")
    fala("Não reconheço este comando, veja se voçê falou certo, ou se não adiciona no meu script...")

def Nex():
    print("Sou a ouvido...")
    fala("Estou lhe ouvindo, o que voçê manda..")

def Horas():
    data = datetime.datetime.now().strftime("%H:%M")
    print(f"Agora são {data}")
    fala(f"Agora são {data} !")

def data():
    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    atual = datetime.datetime.now()
    ano = atual.year
    mes = meses[atual.month - 1]
    dia = atual.day
    print(f"Hoje é {dia} do {mes} de {ano}")
    fala(f"hoje é dia {dia} de {mes} de {ano}")

def abrirYoutube():
    fala("Claro,Me fale, o que você deseja pesquisar no youtube?")
    query = escutar()
    if not query:
        return

    fala("Entendi Senhor.")
    subprocess.Popen(["brave-browser",f"https://youtube.com/results?search_query={query.replace(' ','+')}"])

def Pesquisa():
    fala("Claro, só me diga, o que voçê quer pesquisar?")
    query = escutar()
    if not query:
        return
    if "não" in query or  "nao" in query:
        print("retornando..")
        fala("Ok retrô, Retornando..")
        return
    fala("Entendido retrõ.")
    subprocess.Popen(["brave-browser", f"https://www.google.com/search?q={query.replace(' ', '+')}"])

def quem_sou():
    fala("Bom, me chamo Nex, fui criado pelo retrô com código puro, sem Inteligencia Artificial. Fui criado para ter controle total do sistema, e executar ações a partir das ordens me passada. Ainda sou um protótipo, mas estou em desenvolvimento.")

def desligar():
    fala("Confirma desligamento do sistema? ")
    escolha = escutar()

    if not escolha:
        fala("Cancelando desligamento.")
        return

    if escolha in ["sim", "s", "claro", "pode", "ok","desligar","pode desligar","confirmo","comfirmo"]:
        fala("Entendido, desligando em 3 segundos")
        time.sleep(3)
        subprocess.run(["systemctl", "poweroff"])

def terminal():
    print("Abrindo Terminal....")
    fala("Entendido, abrindo Terminal")
    subprocess.Popen("konsole")

def processos():
    fala("Claro, mostrarei os processos do seu sistema agora")
    subprocess.Popen(["konsole", "-e", "htop"])

def estudos():
    print("ATIVANDO MODO ESTUDOS!")
    fala("Entendido, ativando o modo estudo agora !")
    subprocess.Popen(["brave-browser",f"https://youtube.com/results?search_query=blues"])
    time.sleep(2)
    subprocess.Popen(["brave-browser", 'https://app.hackingclub.com/dashboard'])
    time.sleep(2)
    subprocess.Popen("konsole")

def estadoAtual():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    print(f"CPU: {cpu}%")
    print(f"RAM:{ram.percent}")
    fala(f"Bom retrô, Sua máquina agora está com {cpu} por cento da CPU em uso. Sua memória Ram está em {ram.percent} por cento")
    fala("pode ficar tranquilo, estou monitorando o sistema e avisarei se algum componente se sobrecarregar.")

def Timer():
    def extrair_segundos(texto):
        texto = texto.lower()

        if "segundo" in texto:
            numero = ''.join(filter(str.isdigit, texto))
            return int(numero) if numero else None

        if "minuto" in texto or "min" in texto:
            numero = ''.join(filter(str.isdigit, texto))
            return (int(numero) * 60) if numero else None

        return None

    def contar_timer(seg):
        if seg > 60:
            minutos = seg // 60
            fala(f"Ok, Iniciando contagem de {minutos} minutos conforme você pediu, avisarei assim que terminar..")
        else:
            fala(f"Ok, Iniciando contagem de {seg} segundos conforme você pediu, avisarei assim que terminar..")
        time.sleep(seg)
        fala("retrô o taime que você pediu acabou de expirar")
        print(f"Time expirado !!")
    texto = escutar()
    if not texto:
        fala("Não entendi retrô")
        return
    seg = extrair_segundos(texto)
    if not seg:
        fala("Não consegui entender a tempo, desculpe")
        return
    threading.Thread(target=contar_timer, args=(seg,)).start()

def monitoramento():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    if cpu >= 85.0:
        print(f"CPU:{cpu}%")
        fala(f"Retrô, sua CPU está Bem alta, Com {cpu} por cento!!. Isso vai travar seu sistema.")
    if ram > 88:
        fala(f"retrô Sua Memória RAM está com {ram} por cento.")
