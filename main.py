import tkinter as tk
import sounddevice as sd
import wavio
import pygame
import os
from io import BytesIO

def commencer_enregistrement():
    global enregistrement_en_cours
    label_message.config(text="Enregistrement en cours... Appuyez sur Arrêt pour terminer.")
    bouton_commencer.config(state=tk.DISABLED)
    enregistrement_en_cours = True

    name = afficher_saisie()

    global fichier_audio
    fichier_audio = name + ".wav"
    enregistrement = sd.rec(int(5 * 44100), samplerate=44100, channels=2, dtype='float32')
    sd.wait()
    wavio.write(fichier_audio, enregistrement, 44100, sampwidth=3)

def arreter_enregistrement():
    global enregistrement_en_cours
    label_message.config(text="Enregistrement terminé.")
    bouton_commencer.config(state=tk.NORMAL)
    enregistrement_en_cours = False

def ecouter_message():
    pygame.mixer.init()
    pygame.mixer.music.load(fichier_audio)
    pygame.mixer.music.play()

def reenregistrer_message():
    global fichier_audio

    arreter_enregistrement()

    # Vérifier si un fichier audio existe déjà
    if fichier_audio and os.path.exists(fichier_audio):

        # Attendez un court instant pour que toutes les opérations audio se terminent
        pygame.time.delay(500)

        # Arrêter la lecture audio avec Pygame
        pygame.mixer.music.stop()

        # Libérer les ressources Sounddevice
        sd._terminate()
        pygame.init()

        # Supprimer l'ancien fichier audio
        try:
            os.remove(fichier_audio)
            print(f"Le fichier audio {fichier_audio} a été supprimé avec succès.")
        except OSError as e:
            print(f"Erreur lors de la suppression du fichier audio : {e}")

    # Commencer un nouvel enregistrement
    commencer_enregistrement()

    # Mettre à jour l'étiquette de message pour indiquer que le message a été réenregistré
    label_message.config(text="Message réenregistré.")


def afficher_saisie():
    valeur_saisie = champ_saisie.get()
    label_resultat.config(text=f"Vous avez saisi : {valeur_saisie}")
    return valeur_saisie

fenetre = tk.Tk()
fenetre.title("Enregistreur Audio")

# Variable pour le message d'enregistrement
message_enregistrement = tk.StringVar()

# Variable pour la saisie
variable_resultat = tk.StringVar()

# Variable pour le statut de l'enregistrement
enregistrement_en_cours = False

# Widget Entry pour la saisie de texte
champ_saisie = tk.Entry(fenetre, font=('Arial', 16), textvariable=variable_resultat)
champ_saisie.pack(pady=10)

# Bouton pour commencer l'enregistrement
bouton_commencer = tk.Button(fenetre, text="Commencer l'enregistrement", command=commencer_enregistrement)
bouton_commencer.config(font=('Arial', 14), background='#4CAF50', foreground='white', padx=20, pady=10)
bouton_commencer.pack(pady=10)

# Bouton pour écouter le message enregistré
bouton_ecouter = tk.Button(fenetre, text="Écouter le message", command=ecouter_message)
bouton_ecouter.config(font=('Arial', 14), background='#008CBA', foreground='white', padx=20, pady=10)
bouton_ecouter.pack(pady=10)

# Bouton pour réenregistrer le message
bouton_reenregistrer = tk.Button(fenetre, text="Réenregistrer le message", command=reenregistrer_message)
bouton_reenregistrer.config(font=('Arial', 14), background='#FFD700', padx=20, pady=10)
bouton_reenregistrer.pack(pady=10)

# Bouton pour arrêter l'enregistrement
bouton_arreter = tk.Button(fenetre, text="Arrêter l'enregistrement", command=arreter_enregistrement)
bouton_arreter.config(font=('Arial', 14), background='#FF0000', foreground='white', padx=20, pady=10)
bouton_arreter.pack(pady=10)

# Label pour afficher le message d'enregistrement
label_message = tk.Label(fenetre, textvariable=message_enregistrement, font=('Arial', 12))
label_message.pack(pady=10)

# Label pour afficher le résultat
label_resultat = tk.Label(fenetre, textvariable=variable_resultat, font=('Arial', 14))
label_resultat.pack(pady=10)

fenetre.mainloop()
