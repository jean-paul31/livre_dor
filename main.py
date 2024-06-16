import tkinter as tk
import sounddevice as sd
import wavio
import threading
import time
from PIL import Image, ImageTk
import os
import numpy as np

textes = {
    "instructions": (
        "Instructions d'utilisation :\n"
        "1. Entrez un nom pour le fichier audio dans le champ de saisie.\n"
        "2. Décrocher le combiné.\n"
        "3. Cliquez sur 'Commencer l'enregistrement' pour démarrer l'enregistrement audio.\n"
        "4. Cliquez sur 'Arrêter l'enregistrement' pour terminer l'enregistrement avant la fin des 3 minutes.\n"
        "5. L'enregistrement sera automatiquement sauvegardé sous le nom que vous avez saisi.\n"
        "6. Le compte à rebours de 3 minutes s'affichera pendant l'enregistrement.\n"
    ),
    "commencer": "Commencer l'enregistrement",
    "arreter": "Arrêter l'enregistrement",
    "enregistrement_en_cours": "Enregistrement en cours... Appuyez sur Arrêt pour terminer.",
    "arret": "Enregistrement arrêté.",
    "resultat": "Vous avez saisi :",
    "timer_format": "{:02d}:{:02d}",
    "francais": "Français",
    "portugais": "Português",
    "fichier_existe": "Le fichier existe déjà. Veuillez choisir un autre nom."
}

def traduire_en_francais():
    global textes
    textes = {
        "instructions": (
            "Instructions d'utilisation :\n"
            "1. Entrez un nom pour le fichier audio dans le champ de saisie.\n"
            "2. Décrocher le combiné.\n"
            "3. Cliquez sur 'Commencer l'enregistrement' pour démarrer l'enregistrement audio.\n"
            "4. Cliquez sur 'Arrêter l'enregistrement' pour terminer l'enregistrement avant la fin des 3 minutes.\n"
            "5. L'enregistrement sera automatiquement sauvegardé sous le nom que vous avez saisi.\n"
            "6. Le compte à rebours de 3 minutes s'affichera pendant l'enregistrement.\n"
        ),
        "commencer": "Commencer l'enregistrement",
        "arreter": "Arrêter l'enregistrement",
        "enregistrement_en_cours": "Enregistrement en cours... Appuyez sur Arrêt pour terminer.",
        "arret": "Enregistrement arrêté.",
        "resultat": "Vous avez saisi :",
        "timer_format": "{:02d}:{:02d}",
        "francais": "Français",
        "portugais": "Portugês",
        "fichier_existe": "Veuillez choisir un autre nom."
    }
    mettre_a_jour_interface()

def traduire_en_portugais():
    global textes
    textes = {
        "instructions": (
            "Instruções de uso:\n"
            "1. Digite um nome para o arquivo de áudio no campo de entrada.\n"
            "2. Levante o fone do gancho.\n"
            "3. Clique em 'Iniciar gravação' para começar a gravação de áudio.\n"
            "4. Clique em 'Parar gravação' para terminar a gravação antes do fim dos 3 minutos.\n"
            "5. A gravação será automaticamente salva com o nome que você digitou.\n"
            "6. A contagem regressiva de 3 minutos aparecerá durante a gravação.\n"
        ),
        "commencer": "Iniciar gravação",
        "arreter": "Parar gravação",
        "enregistrement_en_cours": "Gravação em andamento... Pressione Parar para encerrar.",
        "arret": "Gravação encerrada.",
        "resultat": "Você digitou:",
        "timer_format": "{:02d}:{:02d}",
        "francais": "Francês",
        "portugais": "Portugês",
        "fichier_existe": "Por favor, escolha outro nome."
    }
    mettre_a_jour_interface()

def mettre_a_jour_interface():
    bouton_commencer.config(text=textes["commencer"])
    bouton_arreter.config(text=textes["arreter"])
    label_message.config(text="")
    label_resultat.config(text=textes["resultat"])
    label_timer.config(textvariable=variable_timer)

    text_instructions.config(state=tk.NORMAL)
    text_instructions.delete(1.0, tk.END)
    text_instructions.insert(tk.END, textes["instructions"])
    text_instructions.config(state=tk.DISABLED)

def fichier_existe_deja(nom_fichier):
    dossier_audio = "audio"
    fichier_audio = os.path.join(dossier_audio, nom_fichier + ".wav")
    return os.path.isfile(fichier_audio)

def commencer_enregistrement():
    global enregistrement_en_cours, enregistrement, thread_recording, timer_thread, start_time
    if not enregistrement_en_cours:
        name = champ_saisie.get()
        if fichier_existe_deja(name):
            label_message.config(text=textes["fichier_existe"], fg='red')
            return
        
        enregistrement_en_cours = True
        label_message.config(text=textes["enregistrement_en_cours"], fg='black')
        bouton_commencer.config(state=tk.DISABLED)
        bouton_arreter.config(state=tk.NORMAL)

        global fichier_audio
        dossier_audio = "audio"
        if not os.path.exists(dossier_audio):
            os.makedirs(dossier_audio)
        fichier_audio = os.path.join(dossier_audio, name + ".wav")

        start_time = time.time()
        enregistrement = []
        thread_recording = threading.Thread(target=record_audio)
        thread_recording.start()

        timer_thread = threading.Thread(target=compte_a_rebours, args=(3 * 60,))
        timer_thread.start()

def record_audio():
    global enregistrement
    with sd.InputStream(samplerate=44100, channels=2, dtype='float32') as stream:
        while enregistrement_en_cours:
            enregistrement.append(stream.read(1024)[0])
            sd.sleep(10)
    enregistrement = np.concatenate(enregistrement, axis=0)

def arreter_enregistrement():
    global enregistrement_en_cours, timer_thread
    if enregistrement_en_cours:
        enregistrement_en_cours = False
        label_message.config(text=textes["arret"])
        bouton_commencer.config(state=tk.NORMAL)
        bouton_arreter.config(state=tk.DISABLED)

        enregistrement_array = np.concatenate(enregistrement, axis=0)

        duration = time.time() - start_time
        if duration < 3 * 60:
            wavio.write(fichier_audio, enregistrement_array[:int(duration * 44100)], 44100, sampwidth=3)
        else:
            wavio.write(fichier_audio, enregistrement_array, 44100, sampwidth=3)

        champ_saisie.delete(0, tk.END)
        variable_timer.set(textes["timer_format"].format(3, 0))

def afficher_saisie():
    valeur_saisie = champ_saisie.get()
    label_resultat.config(text=f"Vous avez saisi : {valeur_saisie}")
    return valeur_saisie

def compte_a_rebours(duree):
    while duree > 0 and enregistrement_en_cours:
        mins, secs = divmod(duree, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        variable_timer.set(timer)
        time.sleep(1)
        duree -= 1

    if enregistrement_en_cours:
        arreter_enregistrement()

fenetre = tk.Tk()
fenetre.title("Enregistreur Audio")
fenetre.geometry("1000x500")

frame_controls = tk.Frame(fenetre)
frame_controls.pack(side=tk.LEFT, padx=20, pady=20)

enregistrement_en_cours = False
enregistrement = None
start_time = None

champ_saisie = tk.Entry(frame_controls, font=('Arial', 16))
champ_saisie.pack(pady=10)

bouton_commencer = tk.Button(frame_controls, command=commencer_enregistrement)
bouton_commencer.config(font=('Arial', 14), background='#4CAF50', text=textes["commencer"], foreground='white', padx=20, pady=10)
bouton_commencer.pack(pady=10)

bouton_arreter = tk.Button(frame_controls, command=arreter_enregistrement, state=tk.DISABLED)
bouton_arreter.config(font=('Arial', 14), text=textes["arreter"], background='#FF0000', foreground='white', padx=20, pady=10)
bouton_arreter.pack(pady=10)

label_message = tk.Label(frame_controls, font=('Arial', 12))
label_message.pack(pady=10)

label_resultat = tk.Label(frame_controls, font=('Arial', 14))
label_resultat.pack(pady=10)

variable_timer = tk.StringVar(value="03:00")
label_timer = tk.Label(frame_controls, textvariable=variable_timer, font=('Arial', 24))
label_timer.pack(pady=10)

frame_instructions = tk.Frame(fenetre)
frame_instructions.pack(side=tk.RIGHT, padx=20, pady=20)

frame_buttons = tk.Frame(frame_instructions)
frame_buttons.pack(pady=10)

image_francais = Image.open("assets/Flag_of_France.svg.png")
image_francais = image_francais.resize((50, 30), Image.LANCZOS)
photo_francais = ImageTk.PhotoImage(image_francais)

image_portugais = Image.open("assets/Flag_of_Portugal.svg.png")
image_portugais = image_portugais.resize((50, 30), Image.LANCZOS)
photo_portugais = ImageTk.PhotoImage(image_portugais)

bouton_francais = tk.Button(frame_buttons, image=photo_francais, command=traduire_en_francais)
bouton_francais.pack(side=tk.LEFT, padx=5)

bouton_portugais = tk.Button(frame_buttons, image=photo_portugais, command=traduire_en_portugais)
bouton_portugais.pack(side=tk.LEFT, padx=5)

scrollbar = tk.Scrollbar(frame_instructions)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_instructions = tk.Text(frame_instructions, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=('Arial', 12))
text_instructions.insert(tk.END, textes["instructions"])
text_instructions.config(state=tk.DISABLED)
text_instructions.pack(padx=10, pady=10)

scrollbar.config(command=text_instructions.yview)

fenetre.mainloop()
