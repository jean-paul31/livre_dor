import utils

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
    "portugais": "Português",
    "fichier_existe": "Le fichier existe déjà. Veuillez choisir un autre nom."
}


def traduire_en_francais(context):
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
        "portugais": "Português",
        "fichier_existe": "Veuillez choisir un autre nom."
    }
    utils.mettre_a_jour_interface(context)


def traduire_en_anglais(context):
    global textes
    textes = {
        "instructions": (
            "Instructions for use:\n"
            "1. Enter a name for the audio file in the input field.\n"
            "2. Click 'Start Recording' to begin recording audio.\n"
            "3. Click 'Stop Recording' to end the recording before the 3-minute limit.\n"
            "4. The recording will be automatically saved under the name you entered.\n"
            "5. The 3-minute countdown will be displayed during the recording.\n"
        ),
        "commencer": "Start Recording",
        "arreter": "Stop Recording",
        "enregistrement_en_cours": "Recording in progress... Press Stop to finish.",
        "arret": "Recording stopped.",
        "resultat": "You entered:",
        "timer_format": "{:02d}:{:02d}",
        "francais": "French",
        "portugais": "Portuguese",
        "fichier_existe": "Please choose another name."
    }
    utils.mettre_a_jour_interface(context)


def traduire_en_espagnole(context):
    global textes
    textes = {
        "instructions": (
            "Instrucciones de uso:\n"
            "1. Introduce un nombre para el archivo de audio en el campo de entrada.\n"
            "2. Haz clic en 'Comenzar grabación' para iniciar la grabación de audio.\n"
            "3. Haz clic en 'Detener grabación' para finalizar la grabación antes de los 3 minutos.\n"
            "4. La grabación se guardará automáticamente con el nombre que has introducido.\n"
            "5. El contador de 3 minutos se mostrará durante la grabación.\n"
        ),
        "commencer": "Comenzar grabación",
        "arreter": "Detener grabación",
        "enregistrement_en_cours": "Grabación en curso... Pulsa Detener para finalizar.",
        "arret": "Grabación detenida.",
        "resultat": "Has introducido:",
        "timer_format": "{:02d}:{:02d}",
        "francais": "Francés",
        "portugais": "Portugués",
        "fichier_existe": "Por favor, elige otro nombre."
    }
    utils.mettre_a_jour_interface(context)


def traduire_en_portugais(context):
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
        "fichier_existe": "Por favor, escolha outro nome."
    }
    utils.mettre_a_jour_interface(context)


def traduire_en_japonnais(context):
    global textes
    textes = {
        "instructions": (
            "使用手順:\n"
            "1. オーディオファイルの名前を入力フィールドに入力してください。\n"
            "2. 「録音開始」をクリックしてオーディオ録音を開始します。\n"
            "3. 「録音停止」をクリックして、3分以内に録音を終了します。\n"
            "4. 録音は自動的に入力した名前で保存されます。\n"
            "5. 録音中に3分のカウントダウンが表示されます。\n"
        ),
        "commencer": "録音開始",
        "arreter": "録音停止",
        "enregistrement_en_cours": "録音中... 停止を押して終了します。",
        "arret": "録音終了。",
        "resultat": "入力した内容:",
        "timer_format": "{:02d}:{:02d}",
        "francais": "フランス語",
        "portugais": "ポルトガル語",
        "fichier_existe": "別の名前を選んでください。"
    }
    utils.mettre_a_jour_interface(context)


def traduire_en_chinois(context):
    global textes
    textes = {
        "instructions": (
            "使用说明:\n"
            "1. 在输入框中输入音频文件的名称。\n"
            "2. 点击“开始录音”以开始音频录制。\n"
            "3. 点击“停止录音”以在 3 分钟内停止录音。\n"
            "4. 录音将自动保存为您输入的名称。\n"
            "5. 录音过程中将显示 3 分钟倒计时。\n"
        ),
        "commencer": "开始录音",
        "arreter": "停止录音",
        "enregistrement_en_cours": "录音中... 按停止按钮结束录音。",
        "arret": "录音已停止。",
        "resultat": "您输入的是：",
        "timer_format": "{:02d}:{:02d}",
        "francais": "法语",
        "portugais": "葡萄牙语",
        "fichier_existe": "请选择另一个名称。"
    }
    utils.mettre_a_jour_interface(context)
