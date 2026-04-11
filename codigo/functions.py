import speech_recognition as recon
from piper import PiperVoice #classe que controla a voz
import numpy as np # mais low level para converter bytes
import datetime
import subprocess
from time import sleep
import os

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(BASE_DIR, "pt_BR-cadu-medium.onnx")

voice = PiperVoice.load(MODEL_PATH)

micro = recon.Recognizer()


def escutar(max_tentativas=3):
    for _ in range(max_tentativas):
        comando = normalizar(capture_audio())

        if comando:
            return comando.lower().strip()

        fala("Não entendi, pode repetir?")

    fala("Não consegui ouvir você.")
    return None

def normalizar(texto):
    if not texto:
        return None
    return texto.lower().strip()
# converte o texto para fala
def fala(texto):
    som = subprocess.Popen(["aplay", "-f", "S16_LE", "-r", "22050", "-c", "1"], stdin=subprocess.PIPE)
    for pedaco in voice.synthesize(texto):
        # converte float → int16 → bytes
        audio = (pedaco.audio_float_array * 32767).astype(np.int16)
        som.stdin.write(audio.tobytes())

    som.stdin.close()
    som.wait()

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

def Saudacao():
    horario = datetime.datetime.now().hour
    if 6 <= horario < 12:
        print("Bom dia retr0, seja bem vindo!")
        fala('Bom dia retrô, Como voce ta?, acordou cedo hoje ')
    elif 12 <= horario < 18:
        print("Boa tarde retr0, Como voce está?")
        fala("Boa tarde retrô, como se tá mano?, Vamos fazer o que hoje?")
    else:
        print("Boa noite retr0, como ce ta?")
        fala("Boa noite retrô, como voçê tá mano?, no que te ajudo hoje?")

def resposta_desconhecida(comando):
    print("Não conheço esse comando ou instrução")
    fala("Mano não conheço esse comando, veja se voçê falou certo, ou se não adiciona no meu script fechou")

def ghost():
    print("Sou a ouvidos mano..")
    fala("Fala mano, o que voçê manda..")

def Horas():
    data = datetime.datetime.now().strftime("%H:%M")
    print(f"Agora são {data}")
    fala(f"Agora são {data} meu mano")

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
    fala(f"Mano hoje é dia {dia} de {mes} de {ano}")

def abrirYoutube():
    fala("Beleza agora me fala, o que voçê quer pesquisar no youtube?")
    query = escutar()
    if not query:
        return

    fala("Entendi mano.")
    subprocess.Popen(["brave-browser",f"https://youtube.com/results?search_query={query.replace('','+')}"])

def Pesquisa():
    def escutar(max_tentativas=3):
        for _ in range(max_tentativas):
            comando = normalizar(capture_audio())

            if comando:
                if "não" in comando:
                    fala("Beleza voltando")
                    return
                return comando.lower().strip()


            fala("Não entendi, pode repetir?")

        fala("Não consegui ouvir você.")
        return None

    fala("Beleza só falar, o que voçê quer pesquisar?")
    query = escutar()
    if not query:
        return

    fala("Entendi mano.")
    subprocess.Popen(["brave-browser", f"https://www.google.com/search?q={query.replace('', '+')}"])

def quem_sou():
    fala("Voce sabe né? fui desenvolvido pelo Kauan ou retrô, ele me fez com código puro para que eu consiga controlar todo o sistema, ainda estou melhorando, mas é isso né")

def desligar():
    fala("Confirma desligamento do sistema? ")
    escolha = escutar()

    if not escolha:
        fala("Cancelando desligamento.")
        return

    if escolha in ["sim", "s", "claro", "pode", "ok","desligar","pode desligar","confirmo","comfirmo"]:
        fala("Beleza, desligando em 3 segundos")
        sleep(3)
        subprocess.run(["systemctl", "poweroff"])