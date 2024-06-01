import tkinter as tk
import sounddevice as sd
import wavio
import threading
import time
from PIL import Image, ImageTk
import os

textes = {
    "instructions": (
        "Instructions d'utilisation :\n"
        "1. Entrez un nom pour le fichier audio dans le champ de saisie.\n"
        "2. Cliquez sur 'Commencer l'enregistrement' pour démarrer l'enregistrement audio.\n"
        "3. Cliquez sur 'Arrêter l'enregistrement' pour terminer l'enregistrement avant la fin des 3 minutes.\n"
        "4. L'enregistrement sera automatiquement sauvegardé sous le nom que vous avez saisi.\n"
        "5. Le compte à rebours de 3 minutes s'affichera pendant l'enregistrement.\n"
    ),
    "commencer": "Commencer l'enregistrement",
    "arreter": "Arrêter l'enregistrement",
    "enregistrement_en_cours": "Enregistrement en cours... Appuyez sur Arrêt pour terminer.",
    "arret": "Enregistrement arrêté.",
    "resultat": "Vous avez saisi :",
    "timer_format": "{:02d}:{:02d}",
    "francais": "Français",
    "portugais": "Portugais",
}

def traduire_en_francais():
    global textes
    textes = {
        "instructions": (
            "Instructions d'utilisation :\n"
            "1. Entrez un nom pour le fichier audio dans le champ de saisie.\n"
            "2. Cliquez sur 'Commencer l'enregistrement' pour démarrer l'enregistrement audio.\n"
            "3. Cliquez sur 'Arrêter l'enregistrement' pour terminer l'enregistrement avant la fin des 3 minutes.\n"
            "4. L'enregistrement sera automatiquement sauvegardé sous le nom que vous avez saisi.\n"
            "5. Le compte à rebours de 3 minutes s'affichera pendant l'enregistrement.\n"
        ),
        "commencer": "Commencer l'enregistrement",
        "arreter": "Arrêter l'enregistrement",
        "enregistrement_en_cours": "Enregistrement en cours... Appuyez sur Arrêt pour terminer.",
        "arret": "Enregistrement arrêté.",
        "resultat": "Vous avez saisi :",
        "timer_format": "{:02d}:{:02d}",
        "francais": "Français",
        "portugais": "Portugais",
    }
    mettre_a_jour_interface()

def traduire_en_portugais():
    global textes
    textes = {
        "instructions": (
            "Instruções de uso:\n"
            "1. Digite um nome para o arquivo de áudio no campo de entrada.\n"
            "2. Clique em 'Iniciar gravação' para começar a gravação de áudio.\n"
            "3. Clique em 'Parar gravação' para terminar a gravação antes do fim dos 3 minutos.\n"
            "4. A gravação será automaticamente salva com o nome que você digitou.\n"
            "5. A contagem regressiva de 3 minutos aparecerá durante a gravação.\n"
        ),
        "commencer": "Iniciar gravação",
        "arreter": "Parar gravação",
        "enregistrement_en_cours": "Gravação em andamento... Pressione Parar para encerrar.",
        "arret": "Gravação encerrada.",
        "resultat": "Você digitou:",
        "timer_format": "{:02d}:{:02d}",
        "francais": "Francês",
        "portugais": "Português",
    }
    mettre_a_jour_interface()

def mettre_a_jour_interface():
    # Mettre à jour les textes des widgets avec les nouvelles traductions
    bouton_commencer.config(text=textes["commencer"])
    bouton_arreter.config(text=textes["arreter"])
    label_message.config(text=textes["enregistrement_en_cours"])
    label_resultat.config(text=textes["resultat"])
    label_timer.config(textvariable=variable_timer)

def commencer_enregistrement():
    global enregistrement_en_cours, enregistrement, thread_recording, timer_thread
    if not enregistrement_en_cours:
        enregistrement_en_cours = True
        label_message.config(text=textes["enregistrement_en_cours"])
        bouton_commencer.config(state=tk.DISABLED)
        bouton_arreter.config(state=tk.NORMAL)

        name = afficher_saisie()
        global fichier_audio
        dossier_audio = "audio"  # Nom du dossier
        if not os.path.exists(dossier_audio):  # Vérifier si le dossier existe, sinon le créer
            os.makedirs(dossier_audio)
        fichier_audio = os.path.join(dossier_audio, name + ".wav")  # Chemin complet du fichier audio

        # Démarrer le thread d'enregistrement
        thread_recording = threading.Thread(target=record_audio)
        thread_recording.start()

        # Démarrer le compte à rebours dans un thread séparé
        timer_thread = threading.Thread(target=compte_a_rebours, args=(3 * 60,))
        timer_thread.start()

def record_audio():
    global enregistrement
    enregistrement = sd.rec(int(180 * 44100), samplerate=44100, channels=2, dtype='float32')
    while enregistrement_en_cours:
        sd.sleep(100)  # Attendez un court instant
    sd.stop()

def arreter_enregistrement():
    global enregistrement_en_cours
    if enregistrement_en_cours:
        enregistrement_en_cours = False
        label_message.config(text=textes["arret"])
        bouton_commencer.config(state=tk.NORMAL)
        bouton_arreter.config(state=tk.DISABLED)
        time.sleep(0.5)  # Attente courte pour s'assurer que l'enregistrement est terminé
        wavio.write(fichier_audio, enregistrement, 44100, sampwidth=3)  # Sauvegarder l'enregistrement
        champ_saisie.delete(0, tk.END)  # Effacer le contenu du champ de saisie

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

    if enregistrement_en_cours:  # Arrêter l'enregistrement automatiquement à la fin du compte à rebours
        arreter_enregistrement()


fenetre = tk.Tk()
fenetre.title("Enregistreur Audio")

# Ajuster la taille de la fenêtre
fenetre.geometry("1000x500")

# Créer un frame pour les widgets de contrôle
frame_controls = tk.Frame(fenetre)
frame_controls.pack(side=tk.LEFT, padx=20, pady=20)

# Variable pour le statut de l'enregistrement
enregistrement_en_cours = False
enregistrement = None

# Widget Entry pour la saisie de texte
champ_saisie = tk.Entry(frame_controls, font=('Arial', 16))
champ_saisie.pack(pady=10)

# Bouton pour commencer l'enregistrement
bouton_commencer = tk.Button(frame_controls, command=commencer_enregistrement)
bouton_commencer.config(font=('Arial', 14), background='#4CAF50', text=textes["commencer"], foreground='white', padx=20, pady=10)
bouton_commencer.pack(pady=10)

# Bouton pour arrêter l'enregistrement
bouton_arreter = tk.Button(frame_controls, command=arreter_enregistrement, state=tk.DISABLED)
bouton_arreter.config(font=('Arial', 14), text=textes["arreter"], background='#FF0000', foreground='white', padx=20, pady=10)
bouton_arreter.pack(pady=10)

# Label pour afficher le message d'enregistrement
label_message = tk.Label(frame_controls, font=('Arial', 12))
label_message.pack(pady=10)

# Label pour afficher le résultat
label_resultat = tk.Label(frame_controls, font=('Arial', 14))
label_resultat.pack(pady=10)

# Label pour afficher le compte à rebours
variable_timer = tk.StringVar(value="03:00")
label_timer = tk.Label(frame_controls, textvariable=variable_timer, font=('Arial', 24))
label_timer.pack(pady=10)

# Créer un frame pour les instructions et les boutons de traduction
frame_instructions = tk.Frame(fenetre)
frame_instructions.pack(side=tk.RIGHT, padx=20, pady=20)

# Ajouter les boutons de traduction
frame_buttons = tk.Frame(frame_instructions)
frame_buttons.pack(pady=10)

# Charger les images des drapeaux
image_francais = Image.open("assets\Flag_of_France.svg.png")
image_francais = image_francais.resize((50, 30), Image.LANCZOS)
photo_francais = ImageTk.PhotoImage(image_francais)

image_portugais = Image.open("assets\Flag_of_Portugal.svg.png")
image_portugais = image_portugais.resize((50, 30), Image.LANCZOS)
photo_portugais = ImageTk.PhotoImage(image_portugais)

# Boutons avec les images des drapeaux
bouton_francais = tk.Button(frame_buttons, image=photo_francais, command=traduire_en_francais)
bouton_francais.pack(side=tk.LEFT, padx=5)

bouton_portugais = tk.Button(frame_buttons, image=photo_portugais, command=traduire_en_portugais)
bouton_portugais.pack(side=tk.LEFT, padx=5)

# Création de la scrollbar
scrollbar = tk.Scrollbar(frame_instructions)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Création du Text widget
text_instructions = tk.Text(frame_instructions, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=('Arial', 12))
text_instructions.insert(tk.END, textes["instructions"])
text_instructions.config(state=tk.DISABLED)  # Rendre le Text widget non éditable
text_instructions.pack(padx=10, pady=10)

# Configurer la scrollbar pour qu'elle contrôle le Text widget
scrollbar.config(command=text_instructions.yview)

fenetre.mainloop()
