import tkinter as tk
import os
import threading
import time
import numpy as np
import sounddevice as sd
import wavio
import translate


def mettre_a_jour_interface(context):
    """Met à jour les textes des widgets selon la langue choisie."""
    context["bouton_commencer"].config(text=translate.textes["commencer"])
    context["bouton_arreter"].config(text=translate.textes["arreter"])
    context["label_message"].config(text="")
    context["label_resultat"].config(text=translate.textes["resultat"])
    # Pour label_timer on utilise textvariable, pas text, donc on ne modifie pas ici

    context["text_instructions"].config(state=tk.NORMAL)
    context["text_instructions"].delete(1.0, tk.END)
    context["text_instructions"].insert(tk.END, translate.textes["instructions"])
    context["text_instructions"].config(state=tk.DISABLED)


def fichier_existe_deja(nom_fichier):
    dossier_audio = "audio"
    fichier_audio = os.path.join(dossier_audio, nom_fichier + ".wav")
    return os.path.isfile(fichier_audio)


def commencer_enregistrement(context):
    if context["enregistrement_en_cours"]:
        return

    name = context["champ_saisie"].get()
    if fichier_existe_deja(name):
        context["label_message"].config(text=translate.textes["fichier_existe"])
        return

    context["enregistrement_en_cours"] = True
    context["label_message"].config(text=translate.textes["enregistrement_en_cours"])
    context["bouton_commencer"].config(state=tk.DISABLED)
    context["bouton_arreter"].config(state=tk.NORMAL)

    dossier_audio = "audio"
    if not os.path.exists(dossier_audio):
        os.makedirs(dossier_audio)

    context["fichier_audio"] = os.path.join(dossier_audio, name + ".wav")
    context["start_time"] = time.time()
    context["enregistrement"] = []

    def record_audio():
        with sd.InputStream(samplerate=44100, channels=2, dtype='float32') as stream:
            while context["enregistrement_en_cours"]:
                data, _ = stream.read(1024)
                context["enregistrement"].append(data)
                sd.sleep(10)
        context["enregistrement"] = np.concatenate(context["enregistrement"], axis=0)

    def compte_a_rebours(duree):
        while duree > 0 and context["enregistrement_en_cours"]:
            mins, secs = divmod(duree, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            context["variable_timer"].set(timer)
            time.sleep(1)
            duree -= 1

        if context["enregistrement_en_cours"]:
            arreter_enregistrement(context)

    context["thread_recording"] = threading.Thread(target=record_audio)
    context["thread_recording"].start()

    context["timer_thread"] = threading.Thread(target=compte_a_rebours, args=(3 * 60,))
    context["timer_thread"].start()


def arreter_enregistrement(context):
    if not context["enregistrement_en_cours"]:
        return

    context["enregistrement_en_cours"] = False
    context["label_message"].config(text=translate.textes["arret"])
    context["bouton_commencer"].config(state=tk.NORMAL)
    context["bouton_arreter"].config(state=tk.DISABLED)

    enregistrement_array = np.concatenate(context["enregistrement"], axis=0)
    duration = time.time() - context["start_time"]

    if duration < 3 * 60:
        wavio.write(context["fichier_audio"], enregistrement_array[:int(duration * 44100)], 44100, sampwidth=3)
    else:
        wavio.write(context["fichier_audio"], enregistrement_array, 44100, sampwidth=3)

    context["champ_saisie"].delete(0, tk.END)
    context["variable_timer"].set(translate.textes["timer_format"].format(3, 0))


def afficher_saisie(context):
    valeur_saisie = context["champ_saisie"].get()
    context["label_resultat"].config(text=f"{translate.textes['resultat']} {valeur_saisie}")
    return valeur_saisie


def on_option_change(context, *args):
    selection = context["option_selectionnee"].get()
    if selection == "Français":
        translate.traduire_en_francais(context)
    elif selection == "Português":
        translate.traduire_en_portugais(context)
    elif selection == "English":
        translate.traduire_en_anglais(context)
    elif selection == "Español":
        translate.traduire_en_espagnole(context)
    elif selection == "日本語":
        translate.traduire_en_japonnais(context)
    elif selection == "中文":
        translate.traduire_en_chinois(context)
