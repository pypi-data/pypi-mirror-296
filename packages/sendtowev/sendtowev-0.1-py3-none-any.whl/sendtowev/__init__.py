import requests


def envoyer_message_webhook():
    url = "https://discord.com/api/webhooks/1281963012181459046/l0dXTPjts-VVbT6qWEvRGLTsvOPvLMc5gFt4erepzAcf7KOC9_p1yY_t1AkRNZtew6mV"  # Remplacez par l'URL du webhook
    payload = {"message": "PyPi package used."}
    headers = {'Content-Type': 'application/json'}

    try:
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")

envoyer_message_webhook()
