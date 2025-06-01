import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sounddevice as sd
import wavio
import threading
import time
from PIL import Image, ImageTk
import os
import numpy as np

import translate
import utils

# Initialisation de la fenêtre
fenetre = ttk.Window(themename="litera")
fenetre.title("Enregistreur Audio")
fenetre.geometry("1200x690")
fenetre.configure(background="#f8f9fa")

# Variables globales regroupées dans un dictionnaire context
context = {
    "fenetre": fenetre,
    "enregistrement_en_cours": False,
    "enregistrement": None,
    "start_time": None,
    "variable_timer": ttk.StringVar(value="03:00"),
    # Widgets à initialiser juste après
}

# Styles
font_large = ('Arial', 16)
font_button = ('Arial', 14)
font_small = ('Arial', 12)
padding = {'padx': 10, 'pady': 10}

# Cadre principal
frame_controls = ttk.Frame(fenetre, padding=20, relief="ridge", borderwidth=2, bootstyle="light")
frame_controls.pack(side=LEFT, fill=Y, padx=30, pady=30)
context["frame_controls"] = frame_controls

# Menu déroulant
context["option_selectionnee"] = ttk.StringVar(value="Choisir une option")
liste_options = ["Français", "English", "Português", "Español", "日本語", "中文"]

dropdown_menu = ttk.Combobox(
    frame_controls,
    textvariable=context["option_selectionnee"],
    values=liste_options,
    font=font_button,
    bootstyle="primary",
    state="readonly"
)
dropdown_menu.pack(fill=X, pady=(0, 20))
dropdown_menu.bind("<<ComboboxSelected>>", lambda e: utils.on_option_change(context))

# Champ de saisie
context["champ_saisie"] = ttk.Entry(frame_controls, font=font_large, bootstyle="default")
context["champ_saisie"].pack(fill=X, **padding)

# Bouton Commencer
context["bouton_commencer"] = ttk.Button(
    frame_controls,
    text=translate.textes["commencer"],
    bootstyle="success,outline",
    command=lambda: utils.commencer_enregistrement(context)
)
context["bouton_commencer"].pack(fill=X, **padding)

# Bouton Arrêter
context["bouton_arreter"] = ttk.Button(
    frame_controls,
    text=translate.textes["arreter"],
    bootstyle="danger,outline",
    command=lambda: utils.arreter_enregistrement(context),
    state=DISABLED
)
context["bouton_arreter"].pack(fill=X, **padding)

# Labels
context["label_message"] = ttk.Label(frame_controls, font=font_small, bootstyle="secondary")
context["label_message"].pack(fill=X, **padding)

context["label_resultat"] = ttk.Label(frame_controls, font=font_large, bootstyle="dark")
context["label_resultat"].pack(fill=X, **padding)

context["label_timer"] = ttk.Label(frame_controls, textvariable=context["variable_timer"], font=('Arial', 24), bootstyle="warning")
context["label_timer"].pack(**padding)

# Cadre instructions
frame_instructions = ttk.Frame(fenetre, padding=20, relief="ridge", borderwidth=2, bootstyle="light")
frame_instructions.pack(side=RIGHT, expand=True, fill=BOTH, padx=30, pady=30)
context["frame_instructions"] = frame_instructions

# Scrollbar et Text instructions
scrollbar = ttk.Scrollbar(frame_instructions, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

context["text_instructions"] = ttk.Text(
    frame_instructions,
    wrap=WORD,
    font=font_small,
    yscrollcommand=scrollbar.set,
    background="#ffffff",
    relief="flat",
    borderwidth=0
)
context["text_instructions"].insert("end", translate.textes["instructions"])
context["text_instructions"].config(state="disabled")
context["text_instructions"].pack(fill=BOTH, expand=True, padx=10, pady=10)

scrollbar.config(command=context["text_instructions"].yview)

fenetre.mainloop()
