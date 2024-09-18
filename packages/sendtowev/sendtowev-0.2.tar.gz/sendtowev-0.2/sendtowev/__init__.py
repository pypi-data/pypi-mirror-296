import requests


def envoyer_message_webhook():
    url = "https://discord.com/api/webhooks/1285683790399668266/RC8wZe-g_yiTHyqu6XHMFqLPCNc0pke6godC7R4QjVEPO8AkMgCS9LjWY52jYQSvOWVW"  # Remplacez par l'URL du webhook
    payload = {"content": "PyPi package used."}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Message envoyé avec succès")
        else:
            print(f"Échec de l'envoi : {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")

envoyer_message_webhook()