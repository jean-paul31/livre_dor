import tkinter as tk
import sounddevice as sd
import wavio
import threading
import time

def commencer_enregistrement():
    global enregistrement_en_cours, enregistrement, thread_recording, timer_thread
    if not enregistrement_en_cours:
        enregistrement_en_cours = True
        label_message.config(text="Enregistrement en cours... Appuyez sur Arrêt pour terminer.")
        bouton_commencer.config(state=tk.DISABLED)
        bouton_arreter.config(state=tk.NORMAL)

        name = afficher_saisie()
        global fichier_audio
        fichier_audio = name + ".wav"

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
        label_message.config(text="Enregistrement arrêté.")
        bouton_commencer.config(state=tk.NORMAL)
        bouton_arreter.config(state=tk.DISABLED)
        time.sleep(0.5)  # Attente courte pour s'assurer que l'enregistrement est terminé
        sd.stop()  # Arrêter l'enregistrement
        wavio.write(fichier_audio, enregistrement, 44100, sampwidth=3)  # Sauvegarder l'enregistrement
        champ_saisie.delete(0, tk.END) 

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

# Variable pour le statut de l'enregistrement
enregistrement_en_cours = False
enregistrement = None

# Widget Entry pour la saisie de texte
champ_saisie = tk.Entry(fenetre, font=('Arial', 16))
champ_saisie.pack(pady=10)

# Bouton pour commencer l'enregistrement
bouton_commencer = tk.Button(fenetre, text="Commencer l'enregistrement", command=commencer_enregistrement)
bouton_commencer.config(font=('Arial', 14), background='#4CAF50', foreground='white', padx=20, pady=10)
bouton_commencer.pack(pady=10)

# Bouton pour arrêter l'enregistrement
bouton_arreter = tk.Button(fenetre, text="Arrêter l'enregistrement", command=arreter_enregistrement, state=tk.DISABLED)
bouton_arreter.config(font=('Arial', 14), background='#FF0000', foreground='white', padx=20, pady=10)
bouton_arreter.pack(pady=10)

# Label pour afficher le message d'enregistrement
label_message = tk.Label(fenetre, font=('Arial', 12))
label_message.pack(pady=10)

# Label pour afficher le résultat
label_resultat = tk.Label(fenetre, font=('Arial', 14))
label_resultat.pack(pady=10)

# Label pour afficher le compte à rebours
variable_timer = tk.StringVar(value="03:00")
label_timer = tk.Label(fenetre, textvariable=variable_timer, font=('Arial', 24))
label_timer.pack(pady=10)

fenetre.mainloop()
