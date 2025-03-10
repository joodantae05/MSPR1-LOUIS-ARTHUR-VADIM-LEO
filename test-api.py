import json
import requests

# Chemin de votre fichier JSON
fichier_json = './resultats/data.json'

# Charger le fichier JSON
with open(fichier_json, 'r') as f:
    data = json.load(f)

# L'URL de l'API
url = 'http://172.20.30.16:8000/scan'

# Envoyer la requête POST avec les données JSON
response = requests.post(url, json=data)

# Vérifier la réponse de l'API
if response.status_code == 200:
    print("Données envoyées avec succès !")
else:
    print(f"Erreur lors de l'envoi des données: {response.status_code}")