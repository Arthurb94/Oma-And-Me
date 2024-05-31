import requests
import time

# URL de votre API déployée sur Heroku
# url = "https://tv1wdm122i.execute-api.eu-west-3.amazonaws.com/default/oma"
url = "http://localhost:8000/predict"

# Chemin vers l'image PNG que vous souhaitez envoyer
image_path = "test_data/3.png"
# api_key = "pst9MAyUZw2HKQhfKa1wt1SWQ0ElcanJ13d6OVcI"

# Lire l'image en binaire
with open(image_path, "rb") as image_file:
    print("image chargée", image_file)
    files = {"file": image_file}
    # headers = {"Authorization": "Bearer " + api_key}
    response = requests.post(url, files=files)  # , headers=headers)


# Vérifiez la réponse de l'API
if response.status_code == 200:
    data = response.json()
    nordwood_scale = data["nordwood_scale"]

    print(f"Nordwood Scale: {nordwood_scale}")
else:
    print(f"Failed to get a response, status code: {response.status_code}")
