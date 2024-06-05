import requests
import base64
import json

# URL de votre API déployée sur Heroku
url = "https://tv1wdm122i.execute-api.eu-west-3.amazonaws.com/default/oma"
# url = "http://localhost:9000/2015-03-31/functions/function/invocations"

# Chemin vers l'image PNG que vous souhaitez envoyer
image_path = "test_data/3.png"
# api_key = "pst9MAyUZw2HKQhfKa1wt1SWQ0ElcanJ13d6OVcI"

# Lire l'image en binaire
# with open(image_path, "rb") as image_file:
#     print("image chargée", image_file)
#     payload = {"file": image_file}
#     # headers = {"Authorization": "Bearer " + api_key}
#     # response = requests.post(url, files=file)  # , headers=headers)

with open(image_path, "rb") as image_file:
    image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    # print(encoded_image)
    # encoded_image = "f"
    payload = {"file": encoded_image}

# Envoyer la requête POST avec les données de l'image
response = requests.post(url, json=payload)

# Vérifiez la réponse de l'API
if response.status_code == 200:
    data = response.json()
    nordwood_scale = data["nordwood_scale"]
    print(f"Nordwood Scale: {nordwood_scale}")
else:
    print(f"Failed to get a response, status code: {response.json()}")
